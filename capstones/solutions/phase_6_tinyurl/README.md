# Phase 6 — TinyURL with Consistent Hashing (reference implementation)

```
$ python tinyurl.py           # self-demo
$ python test_tinyurl.py
```

## What's here

A single-file (`tinyurl.py`) in-memory URL shortener that exercises the three
ideas the capstone targets:

1. **Base62 short codes.** Bijective `encode_base62 / decode_base62`. We hand
   out auto-increment ids, encode them as base62 → that's the short code.
   No collisions, codes are deterministic, and `len(encode_base62(10**9))` is
   6 characters.

2. **Consistent hash ring.** `ConsistentHashRing` with 64 virtual nodes per
   physical node. Keys land on the next vnode clockwise on a 64-bit hash
   circle. Adding a node moves only ~1/N of keys; removing one moves only
   the keys that were on that node. The test
   (`test_ring_rebalance_property`) asserts the fraction empirically.

3. **In-memory KV per shard.** Just `dict[str, str]` per `Shard`. The
   `TinyURL` service routes every put/get through the ring.

4. **Token-bucket rate limiter.** Per-IP, configured at construction time
   (`capacity` tokens, `rate` per second). The test pinches `rate=0` so the
   bucket behaves like a strict semaphore, and a separate test exercises the
   refill path with synthetic timestamps.

## Why these specific choices

- **Base62, not random short codes.** Random short codes need a collision
  check on every insert. Base62 of an auto-increment id is collision-free by
  construction and gives sortable, monotonic codes. The trade-off is that
  consecutive codes leak the request order — fine for a teaching
  implementation, not for a production shortener (use a Feistel network or
  encrypt the id if you care about that).

- **Consistent hashing with virtual nodes.** Without vnodes, the load on
  each physical node depends on how its single hash lands relative to its
  neighbours — easily 2x or 3x skew. With 64 vnodes per node the variance
  drops to roughly 1/√64 ≈ 12% per node, which the test enforces (15%–35%
  total movement when adding to a 3-node cluster).

- **Token bucket, not leaky bucket or fixed window.** Token bucket allows
  short bursts (up to `capacity`) while keeping the long-term rate bounded
  by `rate`. This matches what most real APIs expose. Fixed window is
  simpler but suffers from "double traffic at the window boundary." Sliding
  log is more precise but holds per-IP timestamp arrays.

## Production-version critique

This reference impl is missing every interesting production concern. The
honest list:

- **Persistence.** Right now an `s.remove_shard()` re-homes the data, but
  process death loses everything. Real systems back the KV with disk
  (LevelDB, RocksDB, or just append-only logs) or talk to a database.
- **Replication.** A single copy of each key sits on a single shard. The
  classic fix is replication factor R: walk *R* clockwise positions on the
  ring and write to each. Reads can use quorum.
- **Background rebalance on `add_shard`.** The demo deliberately skips
  re-homing on `add_shard` so you can *see* where the lost keys go. In
  production you'd kick off a streaming migration from the old owner to the
  new one, with hand-off coordinated by a control plane.
- **Hot-shard handling.** Consistent hashing distributes *keys*, not
  *traffic*. If `goog.le/google` gets 100x the resolves of any other code,
  one shard burns. Solutions: per-key counters + replicating hot keys, or a
  read-through CDN cache in front of the resolve endpoint.
- **Monitoring.** No metrics emitted. Production wants p50/p99 latency per
  endpoint, rate-limit rejection counts, ring movement events, shard
  health.
- **Network layer.** The Phase 5 capstone exposes endpoints with
  `http.server`. This one stayed in-process so the consistent-hash logic
  isn't drowned out by HTTP plumbing. Wiring it up is mechanical.

## Where this links to Weeks 24-30

- **Week 25 (load balancing & sharding).** This is the *concrete* example
  the chapter abstracts. The ring + vnode count + rebalance trade-off lives
  here.
- **Week 26 (caching).** Read-through cache in front of `resolve()` is the
  standard mitigation for hot codes; the case study covers Memcached/Redis
  patterns.
- **Week 27 (rate limiting).** The token bucket here is the simplest
  version; the case study covers distributed rate limiting (sliding window
  + Redis lua) for when one process isn't enough.
- **Week 29 (system design interviews).** TinyURL is the canonical
  whiteboard question. Reading this implementation, then *defending the
  things missing from it*, is exactly the conversation you want to have
  in that interview.

## Known limits

- All state is in-process; the "ring" is conceptual. A real ring would have
  separate processes/machines whose membership is tracked by a coordinator
  (etcd, Zookeeper, or gossip).
- MD5 truncated to 64 bits is used for hashing. Not cryptographic; that's
  fine for sharding, where uniformity is the only requirement.
- The rate limiter's `_buckets` dict grows unbounded with distinct IPs.
  Real systems either evict idle buckets or use a fixed-size LRU.
