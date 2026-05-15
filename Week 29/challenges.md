# Week 29 — Hard Mode Challenges (Boss Level)

**Rules of the game:**
1. Pick a challenge. Don't look at any code in this week's `java/`, `python/`, `cpp/`, or `rust/` folders.
2. Restate the problem in your own words. Write down constraints.
3. Sketch the approach on paper.
4. Implement in any language. No copy-pasting from this repo.
5. Test against the inputs given.
6. THEN diff against the canonical solution. What did you do differently? Was your version slower? Cleaner? Buggier in some edge case?
7. Fill in a `SOLUTION_JOURNAL.md` entry for the problem.

---

## Challenge 1: Token Bucket Rate Limiter (Per-User)

**Spec**:
Implement a rate limiter as a class with the API `allow(userId, timestamp) -> bool`. Each user has independent bucket capacity `C` tokens, refill rate `R` tokens/second. A call is allowed iff at least 1 token is available; the bucket refills lazily on each call (do **not** spin up a background thread). Use a hashmap keyed by user.

Read a sequence of `(userId, timestamp_ms)` calls from stdin and print `ALLOW` / `DENY` for each.

**Constraints**:
- `1 <= C <= 1000`, `0.1 <= R <= 1000`, up to `10^6` ops
- Time: O(1) per call
- Memory: O(distinct users)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `C=2 R=1 / (alice, 0)(alice, 0)(alice, 0)(alice, 1000)(alice, 2000)` | `ALLOW ALLOW DENY ALLOW ALLOW` |
| `C=5 R=1 / (bob, 0)(bob, 100)(bob, 200)(bob, 300)(bob, 400)(bob, 500)` | `ALLOW ALLOW ALLOW ALLOW ALLOW DENY` |

**Stretch**: Distributed rate limiting — multiple servers share the bucket. Discuss Redis + Lua script or sliding-window counters.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 2: Consistent Hash Ring With Virtual Nodes

**Spec**:
Implement a consistent hash ring with `V` virtual nodes per real node. API: `addNode(name)`, `removeNode(name)`, `getNode(key) -> name`. Hash function: any deterministic 64-bit hash (e.g., FNV-1a or your custom). The ring is a sorted structure (TreeMap-equivalent) of `hash -> nodeName`.

Read a sequence of operations and print the output of each `getNode`. Then report (a) the standard deviation of keys-per-node for `10^5` random keys and (b) the fraction of keys remapped when one node is removed (should be ≈ `1 / numNodes`).

**Constraints**:
- Up to 100 real nodes, `V = 100` virtual per node
- Time: O(log(N*V)) per op
- Memory: O(N * V)

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| `addNode A / addNode B / addNode C / getNode key1 / getNode key2 ...` | deterministic per-key mapping |
| remove `B`; the keys previously on B redistribute across A and C only | confirmed |

**Stretch**: Replace TreeMap with a flat sorted array + binary search; benchmark vs. the tree version.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 3: LFU Cache With O(1) Operations

**Spec**:
Implement a Least-Frequently-Used cache with capacity `C`. `put(key, value)` and `get(key)` both in true **O(1)** worst case. Ties (same frequency): evict the least recently used among them.

Data structure: hashmap `key -> (value, freq, nodeInFreqList)` + a doubly linked list of frequency buckets, each bucket being a doubly linked list of (key, value) nodes ordered by recency. Maintain a pointer to the minimum-frequency bucket.

**Constraints**:
- `1 <= C <= 10^5`, up to `10^6` ops
- Time: O(1) per op
- Memory: O(C)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `C=2 / put 1 1 / put 2 2 / get 1 / put 3 3 / get 2 / get 3 / put 4 4 / get 1 / get 3 / get 4` | (verify by hand) |
| `C=0 / put 1 1 / get 1` | `-1` |

**Stretch**: Add `getOrCompute(key, computeFn)` — load-through cache.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 4: Sharded Counter With Eventual Consistency

**Spec**:
Implement a counter that supports `increment(shard_id)` and `total() -> sum across shards`. Increments are O(1); reads must scan all shards. Simulate `k` shards; each `increment` is routed to a random shard (or by `hash(thread_id) % k`). Demonstrate that increment-heavy workloads benefit from sharding because shards reduce contention.

Bonus: implement a version with "lazy total" — cache the total and invalidate on increment; reads return cached total if no increments since last computation.

**Constraints**:
- `k` shards, up to `10^7` ops
- Time: O(1) increment, O(k) total
- Memory: O(k)

**Test inputs**:
| Input | Expected output |
|-------|-----------------|
| `k=4 / inc * 10 (any shards) / total` | `10` |
| `k=1 / inc / inc / total` | `2` |
| `k=10 / 1M random increments / total` | `1000000` |

**Stretch**: Concurrent test: spawn `T` threads each doing 1M increments; verify total = `T * 1M` and measure throughput vs. a single non-sharded `AtomicLong`.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?

---

## Challenge 5: Bounded Blocking Queue Without `synchronized`

**Spec**:
Implement a thread-safe bounded blocking queue (`put` blocks if full, `take` blocks if empty) using only `ReentrantLock` and `Condition` (Java) / mutex + condvars (other langs). Capacity `C`. Test with a single producer + single consumer, multiple producers + single consumer, multiple of both.

In your journal: explain why two condition variables (not one) is preferable, and why `signalAll` may be needed in some implementations vs. `signal`.

**Constraints**:
- `1 <= C <= 10^5`
- Operations: `put`, `take`, `tryPut(timeout)`, `tryTake(timeout)`
- Memory: O(C)

**Test inputs**:
| Input | Expected behavior |
|-------|-------------------|
| 1 producer of 1M ints, 1 consumer | consumer receives all 1M in order |
| 4 producers + 4 consumers | each produced item received exactly once |
| `tryPut` on a full queue with 50ms timeout | returns false after ~50ms |

**Stretch**: Implement the same queue lock-free using atomic CAS on head/tail pointers (Michael–Scott queue) — significantly harder.

**Self-check questions** (answer in your journal):
- What's your complexity? Is it tight?
- What did you trade off vs. the canonical solution?
- What edge case did you almost miss?
