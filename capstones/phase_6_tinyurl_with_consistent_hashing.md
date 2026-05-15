# Capstone — Phase 6: TinyURL with Consistent Hashing, Rate Limiting, and In-Memory KV

**Time estimate**: 14-18 hours over 2 weekends.
**Prerequisite weeks**: 25-30 (consistent hashing, rate limiting, sharding, in-memory data structures, distributed systems basics).
**Skill checked**: You can build a small but realistic distributed system end-to-end, exercising every meta-skill the curriculum has trained: data-structure choice, complexity reasoning, concurrency, system design tradeoffs, and operational thinking.

## The Goal
Build a TinyURL-style service prototype. The user POSTs a long URL and gets back a short code; the user GETs the short code and is redirected (or, for the prototype, returned the long URL). Behind the API live three pieces of substance:
1. A **consistent-hash ring** that maps short codes to one of K storage shards.
2. A **token-bucket rate limiter** per client.
3. A **tiny in-memory KV store** per shard with TTL support.

This is the capstone — the one that ties everything together. The "right" answer is "use Redis", and you must demonstrate you can build the moving parts well enough to *not* use it.

## Functional Requirements
- HTTP API:
  - `POST /shorten` body `{url, ttl_seconds?}` returns `{short_code, expires_at}`.
  - `GET /{short_code}` returns 302 redirect to the long URL, or 404 if missing/expired, or 410 if explicitly deleted, or 429 if rate-limited.
  - `DELETE /{short_code}` removes a mapping.
  - `GET /stats` returns per-shard size and hit counts.
- Must run with K ≥ 3 shards (in-process is fine; separate goroutines/threads or even separate processes is better).
- Must use consistent hashing with virtual nodes for shard assignment.
- Must enforce a per-IP rate limit (default: 10 shorten requests/sec, 100 redirects/sec).
- Must expire entries past their TTL.
- Should provide a `/admin/rebalance` endpoint that adds or removes a shard and triggers key migration.

## Non-functional Requirements
- Performance: 5k QPS of redirect lookups on a laptop with K=3 shards. Shorten can be slower (writes are rarer). Measure and report.
- Memory: don't leak expired entries — implement either lazy expiration on access plus a periodic janitor, or an expiration heap.
- Code quality: four modules — `hashring`, `kv`, `ratelimiter`, `api`. Each is independently testable. The `api` module imports the other three and contains zero data-structure logic.
- Tests: at least 40 tests across the four modules, plus an end-to-end integration test that exercises shorten → redirect → expire → 404.

## Architecture Sketch

```
                       client
                         |
                         v
                +--------+-------+
                |    HTTP API    |
                +--------+-------+
                         |
        +----------------+-----------------+
        |                |                 |
        v                v                 v
 +------+-------+ +------+-------+  +------+---------+
 | Rate limiter | |  Hash ring   |  | Code generator |
 | (token bkt)  | | get_shard()  |  | random base62  |
 +--------------+ +------+-------+  +----------------+
                         |
            +------------+------------+
            |            |            |
            v            v            v
       +---------+ +---------+   +---------+
       | Shard A | | Shard B | ..| Shard K |
       | KV+TTL  | | KV+TTL  |   | KV+TTL  |
       +---------+ +---------+   +---------+
```

## Implementation Roadmap

1. **Day 1 (3-4h) — Hash ring + KV store, in isolation.**
   Build the hash ring (revisit transcript 07 — there's a working implementation there) with 100 virtual nodes per physical node. Build the KV store as a hash map with a per-entry `expires_at` timestamp; expose `put(k, v, ttl)`, `get(k)` (returning None if expired), `delete(k)`. Test both modules thoroughly in isolation, no API yet.

2. **Day 2 (3-4h) — Rate limiter + code generator.**
   Implement the token-bucket limiter. State per client: `(tokens: float, last_refill_ts: float)`. Atomic update under a per-client lock (or `sync.Map`-style fine-grained locking). Limiter has two configurable instances: one for `/shorten`, one for redirects.

   Code generator: random 7-character base62. Collision-handling strategy: on insert, if the code already exists, regenerate up to 3 times, then error. Document the collision probability vs. URL count.

3. **Day 3 (4-5h) — API + wiring.**
   Wire it all up. `POST /shorten`: rate-limit check → generate code → `hashring.get_shard(code)` → shard.put. `GET /{code}`: rate-limit check → `hashring.get_shard(code)` → shard.get → 302 or 404. Add structured logs and basic Prometheus-style counters (in-process).

4. **Day 4 (2-3h) — Rebalancing.**
   This is the meaty part. When `/admin/rebalance` adds a shard:
   - Compute the new ring.
   - For each key in *every* existing shard, check if `new_ring.get_shard(key) == old_ring.get_shard(key)`. If not, copy it to the new shard. Delete from the old shard *after* the new shard confirms write.
   - Block writes during the operation (simplest correct approach) OR support double-write during migration (much harder).
   For removal, route keys forward to the new owner before deleting.

   Test: shorten 1000 URLs, add a shard, verify all 1000 are still retrievable and that approximately 1/K of them have moved.

5. **Day 5 (2-3h) — Polish.**
   `/stats` endpoint. README with: architecture diagram, throughput numbers, the rebalancing test result, and a section called "Why didn't you just use Redis?" — answer it honestly. Run the load test.

## Stretch Goals
- Persistence: write each shard's contents to a snapshot file every 5 minutes, replay on startup.
- Bounded-load consistent hashing (the Google variant) so hot keys don't crater one shard.
- Custom short codes: the user supplies a code in the `POST` body; the server validates uniqueness.
- Analytics: count hits per code; expose `/stats/{code}` with hit count and last-access timestamp.
- Authentication: API keys per client, with different rate limits per tier.
- Distribute the shards across actual processes communicating over TCP, not in-process goroutines.

## Self-grading rubric
| Criterion | Points | What you're checking |
|-----------|--------|----------------------|
| Correctness on basic inputs | 30 | Shorten and redirect roundtrip, TTL expiration, 404 on missing |
| Handles edge cases | 20 | Code collision, rate-limit boundary at exactly N requests, expired-but-not-yet-evicted, rebalance during concurrent reads |
| Algorithm choice is justified (commit message or README) | 15 | Why consistent hashing over modulo, why token bucket over sliding window, the "Why didn't you use Redis?" section |
| Code is readable (function size, naming) | 15 | Four modules with clean boundaries; API module is mostly handler wiring |
| Tests pass (≥80% coverage on core logic) | 10 | Integration test that triggers rebalance is the crown jewel |
| Stretch goal implemented | 10 | Persistence is most production-shaped; bounded-load is most DSA-shaped |

## When you're done
- Push to a separate repo (or branch) and host it. Link from your portfolio. This is *the* project to point recruiters at; it touches every layer.
- Write a reflection essay in your `SOLUTION_JOURNAL.md`: which subsystem ended up bigger than expected, which felt smaller, where would you go next? Did the curriculum prepare you for the bits that surprised you?
- Compare your final architecture to a real product that does the same thing (see `case_studies/real_world/`). Bitly's engineering blog has posts on their shortener architecture; so does YOURLS. Read them after you ship yours — you will understand them in a way you couldn't have before.
- This is the last capstone. Write a short retrospective for the whole 30-week journey: which weeks were under-weighted, which were over-weighted, what would you tell a past version of yourself starting from Week 1? Drop it in the journal.
