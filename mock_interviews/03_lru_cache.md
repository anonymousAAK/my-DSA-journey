# Mock Interview: Design an LRU Cache

**Setup**: Staff engineer interviewer at a fictional CDN company, Edgewise. Candidate has 2 years of experience and has used `functools.lru_cache` but never implemented one.

**Difficulty**: Medium-Hard
**Topic**: Weeks 4-5 (linked lists, hash maps) plus Week 13 (design discipline).

---

## Transcript

**Interviewer**: Design an LRU cache. Support `get(key)` and `put(key, value)`. Both should be O(1) average.

**Candidate**: Quick framing: "LRU" means we evict the *least recently used* entry once capacity is exceeded. "Used" includes both reads and writes, correct?

**Interviewer**: Correct. A `get` that hits counts as use; a `put` of an existing key counts as use; a `put` of a new key is the most recent.

> 🔍 **What's happening here**: The candidate disambiguated "used" because real LRU variants differ here (some count writes only). Confirming the spec out loud is cheap insurance.

**Candidate**: Capacity is a constructor parameter? Fixed for the life of the cache? What about concurrency?

**Interviewer**: Fixed at construction. Single-threaded for now; we may follow up on concurrency.

**Candidate**: Got it. The shape of the solution is well known: hash map plus doubly linked list. The hash map gives O(1) key → node lookup. The doubly linked list gives O(1) insertion, deletion at any node, and O(1) move-to-front. Without the doubly linked structure, deleting the LRU node when the map points only to the value would force a scan.

> 🔍 **What's happening here**: The candidate didn't just name the data structures; they justified each. "Why a *doubly* linked list" is the question many candidates flunk in follow-ups.

**Interviewer**: Why doubly linked rather than singly?

**Candidate**: Because we delete by node, not by predecessor. To remove a node from a singly linked list in O(1), you have to know its predecessor, which means another pointer per node or a scan. With prev/next pointers per node, the map can hand us the exact node and we splice it out in constant time.

**Interviewer**: Sketch the interface and the eviction flow.

**Candidate**: I'll use a sentinel head and sentinel tail to avoid null checks. Convention: head.next is the most recently used; tail.prev is the LRU. On `get(k)`: if present, splice node out and re-insert just after head. On `put(k, v)`: if present, update value and move to front; if absent and at capacity, evict tail.prev (remove from list and from map) before inserting.

```python
class _Node:
    __slots__ = ("k", "v", "prev", "nxt")
    def __init__(self, k, v):
        self.k = k; self.v = v
        self.prev = self.nxt = None

class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[object, _Node] = {}
        self.head = _Node(None, None)
        self.tail = _Node(None, None)
        self.head.nxt = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        node.prev.nxt = node.nxt
        node.nxt.prev = node.prev

    def _insert_front(self, node: _Node) -> None:
        node.nxt = self.head.nxt
        node.prev = self.head
        self.head.nxt.prev = node
        self.head.nxt = node

    def get(self, key) -> object | None:
        node = self.map.get(key)
        if node is None:
            return None
        self._remove(node)
        self._insert_front(node)
        return node.v

    def put(self, key, value) -> None:
        node = self.map.get(key)
        if node is not None:
            node.v = value
            self._remove(node)
            self._insert_front(node)
            return
        if len(self.map) == self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.k]
        new_node = _Node(key, value)
        self.map[key] = new_node
        self._insert_front(new_node)
```

> 🔍 **What's happening here**: The candidate extracted two private helpers (`_remove`, `_insert_front`) BEFORE writing get/put. That keeps the public methods short enough to read on one screen, which is a real interview-grading axis even if no one says it aloud.

**Interviewer**: Walk me through capacity=2, then `put(1,1) put(2,2) get(1) put(3,3) get(2) put(4,4) get(1) get(3) get(4)`.

**Candidate**: After `put(1,1)` list is 1. After `put(2,2)`: 2,1. `get(1)` returns 1, list becomes 1,2. `put(3,3)` exceeds capacity, evict 2 (tail.prev). List: 3,1. `get(2)` returns None. `put(4,4)` evicts 1. List: 4,3. `get(1)` is None. `get(3)` returns 3, list: 3,4. `get(4)` returns 4, list: 4,3.

> 🔍 **What's happening here**: Walking the example after the code, in plain language, lets the interviewer catch a bug they suspect without you noticing. If you skip this step they have to read your code line-by-line, which costs you their attention.

**Interviewer**: What if `get` is called with a key never inserted?

**Candidate**: Returns None per the code. If the spec requires `-1` (LeetCode style) or raises, easy change.

**Interviewer**: Now make it thread-safe.

> 🔍 **What's happening here**: The pivot to concurrency is where many candidates flail. The right move is to first ask what level of safety is required — reentrancy, multiple writers, lock granularity — before reaching for a tool.

**Candidate**: First, what's the access pattern? Read-heavy, write-heavy, or balanced? And do you need strict LRU semantics under contention, or is approximate LRU okay if it buys throughput?

**Interviewer**: Read-heavy, and approximate LRU is fine.

**Candidate**: Then I'd consider two options. (1) Coarse lock: wrap every operation in a single mutex. Simple, correct, but the lock is contended on every read because reads mutate the list. (2) Approximate LRU like Redis or Caffeine: shard the cache into K independent LRUs by `hash(key) % K`, each with its own lock — concurrency scales with K. Or replace strict recency tracking with a CLOCK or TinyLFU policy, which only updates an atomic counter on read, dramatically reducing write-on-read contention.

**Interviewer**: Which would you ship?

**Candidate**: For a 2-week prototype, sharded coarse-locking. For production on a hot path, I'd reach for Caffeine (JVM) or moka (Rust) — both implement TinyLFU which has higher hit rates than LRU and is built to be concurrent. I would not reimplement TinyLFU from scratch.

> 🔍 **What's happening here**: The candidate refused to over-engineer in the interview and refused to under-engineer for production. Both are pragmatic signals.

**Interviewer**: One more — what if entries have TTLs?

**Candidate**: Two indexes. The LRU list/map as before, plus a min-heap or a timer wheel keyed by expiration. On access, lazily check if the entry has expired and treat it as a miss if so. Run a periodic janitor to evict from the heap to bound memory of dead entries.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill*.

---

## What was tested
- Clarifying questions: ✅ "use" semantics, concurrency, capacity-change
- Brute force first: N/A — design problem, but the candidate sketched the *shape* before coding
- Complexity-driven optimization: ✅ justified DLL over SLL
- Edge cases without prompting: ✅ unknown key, repeated put, capacity hit on update
- Communication while coding: ✅ extracted helpers up front
- Handling interviewer hints: ✅ pivoted cleanly to concurrency by re-clarifying

## Reflection prompts for the learner
- Sentinel nodes vs. nullable head/tail — which would *you* default to and why? Re-write the code without sentinels and count the extra null checks.
- The candidate said "I would not reimplement TinyLFU from scratch." Was that a confident answer or a dodge? When is it which?
- Sketch the TTL variant. Where do races between the janitor and `get` hide?
