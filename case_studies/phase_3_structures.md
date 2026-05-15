# Phase 3: Data Structures — TTL + LRU Cache for a Database

## The Word Problem

> Our read traffic is murdering the primary DB. We need an in-process cache layer. Each cached row has a TTL — some are 30s, some are an hour, some are 24h — that part is per-table and the ORM gives us the TTL when we set. Cache should hold ~1M entries before evicting. When full, evict the entry that hasn't been read in the longest. Also expired entries should disappear "soonish" — we can tolerate them being stale-but-evicted lazily on access, but please don't let a million dead entries pin our memory. Need this to be sub-microsecond per op since it's on the hot path for every page render.

## Step 1: Restate the problem precisely

We need a key-value store supporting:

- `get(key) -> value | MISS`: return value if present AND not expired; otherwise MISS.
- `put(key, value, ttl_seconds)`: store the value with an absolute expiry = now + ttl.
- **Capacity**: ~1M entries. When full and we `put` a new entry, **evict the least-recently-used** non-expired entry. (We should obviously prefer to evict an expired entry first if any are available — free win.)
- **Expiry**: expired entries should be reclaimable. Either lazily on access, or proactively in the background.
- **All ops sub-microsecond expected.** That means O(1) amortized for `get` and `put`, and definitely no scans.

## Step 2: Identify constraints

- Capacity: ~1M entries. At, say, 200 bytes/entry overhead → 200 MB. Acceptable.
- Time budget: sub-µs per op → no traversals, no full scans. Hash-based lookup is mandatory.
- Concurrency: PM didn't mention it, but "every page render" implies multithreaded. Note it as a follow-up; for now we design single-threaded and discuss locking at the end.
- Edge cases:
  - `put` an existing key (should refresh value + TTL + recency, NOT add a duplicate).
  - `get` an expired key (return MISS, evict it).
  - TTL = 0 or negative (immediately expired — reject? store as expired? — clarify).
  - Capacity = 0 (degenerate; reject or no-op).
  - All entries expired and we try to `put` (should evict an expired one, not "evict LRU among live").
  - Same expiry time on many entries.

## Step 3: Brute force first

Naive approach: a dict for storage, with each value being `(value, last_access_time, expiry_time)`.

- `get`: O(1) lookup, check expiry, update `last_access_time`. Fine.
- `put` when full: scan all 1M entries to find the min `last_access_time` not yet expired → **O(n)** per eviction. At 1M entries this is maybe 5ms in pure Python. Way over budget.
- Lazy expiry: works on access, but if a million 30-second entries expire and no one reads them, they sit forever. Memory creeps.

So the brute force is correct, but `put` is too slow when the cache is full, and there's no proactive expiry.

## Step 4: Identify wasted work

- **LRU eviction scans everything to find the oldest.** We're recomputing "who is oldest?" every eviction. The answer changes by exactly one entry per `get`. We should maintain it incrementally.
- **Expiry scans everything to find expired entries.** Same issue. Expirations happen at known future times — we should keep them in *sorted* order by expiry, so we can find the next-to-expire in O(1) and the expired-set in O(k) where k is the number we actually evict.
- **`last_access_time` is a timestamp, but we don't actually care about the value — only the order.** A doubly-linked list maintains order without timestamps.

## Step 5: Optimize

We need two indexes over the same set of entries:

1. **Recency order** → doubly-linked list. Head = most recently used, tail = least.
2. **Expiry order** → min-heap keyed on expiry timestamp.

Plus the **hash map** from key to its node, so we can find an entry in O(1).

This is the classic **LRU cache** (Week 12) augmented with a heap (Week 11) for TTL.

### Data layout

```
class Node:
    key, value, expiry_ts
    prev, next      # doubly-linked list pointers

table:    dict[key -> Node]
list:     doubly-linked list, head = MRU, tail = LRU
exp_heap: min-heap of (expiry_ts, key, node_ref)
```

### Operations

**`get(key)`**
1. Look up in `table`. If not found → MISS.
2. If `node.expiry_ts <= now` → remove from list, remove from table, return MISS. (Lazy expiry.)
3. Else → move node to head of list, return value. O(1).

**`put(key, value, ttl)`**
1. If key already exists: update value, expiry; move to head; **push a new entry into the heap** (we don't remove the stale heap entry — we use the "lazy heap" trick).
2. Else if size < capacity: insert new node at head, add to table, push onto heap.
3. Else (cache full): we need to evict.
   - First, **opportunistically drain expired entries from the heap top.** While `heap.peek().expiry_ts <= now`, pop, look up in table, if still present and the heap entry's expiry matches the node's current expiry, evict it. (The matching check is what makes the lazy-heap-stale-entry trick work.)
   - If after draining we have room, insert.
   - Otherwise, evict the **tail of the linked list** (the LRU entry), then insert.

All operations are O(1) amortized (the heap ops are O(log n), but n=1M means log n ≈ 20 — fine, and they're only invoked on eviction).

### The "stale heap entry" trick

When we `put` an existing key, we update its expiry, but the old expiry is still sitting in the heap. We don't try to find and remove it (that's O(n) in a heap). Instead, when we pop from the heap, we check: does the node still exist? Does its current expiry match what we popped? If not, **discard and pop the next one**. The heap can be 2-3x larger than the cache, but operations remain O(log n) amortized.

### Proactive expiry

Optionally run a background pass that drains expired entries from the heap top once per second. This bounds memory bloat from the lazy approach.

## Step 6: Implementation gotchas

- **Move-to-head on `get` is a mutation.** Concurrent reads will trample each other. Need a lock or a more clever scheme (e.g., segmented LRU, or accept "approximate LRU" via clock algorithm — Redis does this).
- **Time source**: don't call `time.time()` 10x per op. Cache `now` once per top-level call. And use a monotonic clock; wall-clock can go backwards (NTP).
- **Heap entries holding node references** prevent the node from being GC'd after eviction. Hold weak refs, or just hold the key and re-lookup.
- **Off-by-one on expiry**: is `expiry_ts == now` expired or live? Pick one (usually expired → `<=`) and stick with it.
- **`put` of an already-expired entry** (`ttl=0`): just don't insert, or insert and let `get` see it expired. Either is defensible; document.
- **Eviction while iterating the heap** during the opportunistic drain: don't re-enter `put`/`get`, just direct linked-list and table operations.
- **Memory**: each entry now has a Node (24 bytes + pointers in CPython, more), an entry in the dict (~120 bytes/entry overhead amortized), and a heap entry (~80 bytes). 200 bytes/entry was optimistic; budget closer to 300.

## Step 7: Verification

- Basic: `put(a, 1, 60); get(a)` → 1.
- Expiry: `put(a, 1, 0.001); sleep(0.01); get(a)` → MISS.
- LRU order: fill to capacity, access in some pattern, add one more, verify the right one got evicted.
- TTL prefers expired victim: fill capacity, let half expire, insert one more, verify an expired entry was reclaimed (not LRU).
- Stale heap entries: put(a, 1, 60), put(a, 2, 1), wait 1s, put many others — verify no double-eviction.
- Stress test: random ops at scale, compare against a slow O(n) reference cache (dict + manual scan).
- Concurrency (when added): hammer with N threads, verify no node is in the linked list twice, no key missing from table while in list.

## Step 8: Reflection

What made this hard: composing **three** data structures (hash map, linked list, heap) so they stay consistent under every operation. Single-structure problems are easy. Multi-structure problems are where bugs live — every mutation has to update every index, or the structures drift apart and you start serving deleted entries.

Pattern: **augmented data structure**. We have a primary access pattern (get by key → hash map), an eviction policy (LRU → linked list), and a secondary index (by expiry → heap). The fundamental skill is **knowing what index to add for what query** without making every other operation slow.

Curriculum tie-in:

- Week 11 (heaps) for the expiry index.
- Week 12 (linked lists) for the recency order. The doubly-linked-list-plus-hash-map combo IS the LRU pattern, and you should be able to write it from memory by the end of Phase 3.
- Week 13 (hash tables) for the primary lookup.

Where else this pattern lives:

- Browser tab caches.
- CPU caches (L1/L2/L3 use approximate-LRU because exact LRU is too expensive in hardware).
- DNS resolvers (Phase B real-world #4).
- The buffer pool in every relational database.
