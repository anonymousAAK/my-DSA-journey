# Week 29 — Pattern Recognition Drills

These problems are described in plain English. For each one, identify which system-design pattern applies and write a 1-line justification. **Don't code anything yet.** Try without peeking at the answer key.

## Drills

### 1. Design a service that allows at most 100 requests per user per minute, with sub-millisecond per-check overhead.
Pattern: ______
Why: ______

### 2. Design an in-process cache of fixed capacity that evicts the least-recently-used entry on overflow, supporting O(1) get/put.
Pattern: ______
Why: ______

### 3. Design a distributed key-value store that needs to scale storage across thousands of nodes; minimize data movement when nodes are added or removed.
Pattern: ______
Why: ______

### 4. Design a feed service that aggregates posts from millions of users. Reads are 100x more frequent than writes. Optimize for read latency.
Pattern: ______
Why: ______

### 5. Design a unique-ID generator that produces globally-unique sortable 64-bit IDs across thousands of machines without a central coordinator.
Pattern: ______
Why: ______

### 6. Distractor: Design an in-memory hash map that supports O(1) get/put. (System design?)
Pattern: ______
Why: ______

### 7. Design a real-time analytics service that must report approximate cardinality (distinct users) over a stream of billions of events using kilobytes of memory.
Pattern: ______
Why: ______

### 8. Design a worker fleet that pulls jobs from a queue, processes them, and acknowledges only on success. Jobs must not be lost on worker crash.
Pattern: ______
Why: ______

### 9. Design a service that fans out a single write into thousands of reads (e.g., a celebrity tweet). What architectural pattern handles this?
Pattern: ______
Why: ______

### 10. Design a load balancer that routes the same user consistently to the same backend even when backends are added/removed.
Pattern: ______
Why: ______

---

## Answer Key

<details><summary>Click to reveal</summary>

1. **Pattern**: Token-bucket or leaky-bucket rate limiter. **Why**: per-key state with refill rate; O(1) per check; can shard by user.
2. **Pattern**: LRU cache = doubly linked list + hashmap. **Why**: hashmap for O(1) lookup, DLL for O(1) move-to-front and tail-evict.
3. **Pattern**: Consistent hashing. **Why**: hash ring with virtual nodes — adding/removing a node reshuffles only 1/N of keys.
4. **Pattern**: Fan-out-on-write (precomputed feeds) + cache. **Why**: read-heavy workload → push cost into write path.
5. **Pattern**: Snowflake-style ID (timestamp + machineId + sequence). **Why**: bit-packing yields uncoordinated, time-ordered IDs.
6. **Pattern**: Distractor — that's a data structure (Week 16), not a system. **Why**: no scaling, durability, or distribution concerns; recognize the boundary.
7. **Pattern**: HyperLogLog. **Why**: probabilistic cardinality with ~1.5KB memory and ~2% error.
8. **Pattern**: At-least-once delivery + idempotent processing + ack-on-success. **Why**: visibility timeout / leasing pattern (SQS/Kafka style).
9. **Pattern**: Hybrid push/pull (fan-out on read for high-fanout accounts). **Why**: pure push explodes; pull on-demand for celebrity sources.
10. **Pattern**: Consistent hashing on user ID (sticky routing). **Why**: stability under membership changes.

</details>
