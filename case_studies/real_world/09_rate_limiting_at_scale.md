# Token Bucket vs Sliding Window at Cloudflare/AWS

## The problem

A public API needs to throttle clients. Each client is allowed, say, 1,000 requests per minute. Above that, return HTTP 429. The naïve implementation breaks in a dozen ways at scale: clock skew between machines, bursty legitimate traffic, distributed state across thousands of front-ends, the desire to support multiple rate-limit tiers (per second, per minute, per day) on the same client. Cloudflare processes tens of millions of req/sec at edge; AWS API Gateway is similar. Their rate limiter has to be both algorithmically right and operationally fast.

## Why the obvious approach didn't work

**Naïve fixed window**: maintain a counter per client, reset every minute. Pseudo-code: `if counter[client] > limit: reject; else: counter[client] += 1`. Simple, but **terrible** because of edge effects: a client can send 1,000 requests in the last second of minute N and 1,000 more in the first second of minute N+1 — 2,000 requests in 2 seconds, but the algorithm thinks they were two distinct minutes. The "limit per minute" promise is violated.

**Naïve sliding window**: store every timestamp of every request, count those in the last 60 seconds. Correct, but at scale it's a per-client list of potentially 1,000 timestamps, mutated on every request. Memory and write amplification kill you at edge scale.

You need an algorithm that:
- Doesn't have edge effects.
- Uses O(1) memory per client.
- Doesn't require precise clocks across the fleet.
- Works in a distributed setting where any of N front-ends might handle the next request.

## What they actually use

Two main algorithms dominate, often combined:

### Token bucket

Each client has a "bucket" with a max capacity (e.g., 1,000 tokens) that refills at a steady rate (e.g., 1,000 tokens per minute = ~16.6 per second). Each request consumes 1 token. If the bucket has tokens, accept and decrement. If empty, reject.

The genius is the storage: each bucket is just **two numbers**: `tokens_remaining` and `last_refill_time`. On request:
```
elapsed = now - last_refill_time
tokens = min(capacity, tokens + elapsed * refill_rate)
last_refill_time = now
if tokens >= 1: tokens -= 1, accept
else: reject
```

O(1) memory, O(1) per request, naturally handles bursts up to the bucket capacity. The catch: bursty clients can spike to `capacity` instantaneously, then have to wait for the bucket to refill. This is usually a feature — legitimate bursts (a user batch-fetching) are allowed, sustained abuse is not.

### Sliding window with bucketed counters

A compromise between "perfect sliding window" and "fixed window." Divide the window into sub-buckets (e.g., 60 1-second buckets for a 1-minute window). Count requests per bucket. To get the count in the last 60 seconds, sum the 60 most recent buckets.

This eliminates the fixed-window edge effect: as time advances, the oldest bucket falls off and a new one starts. Storage is O(B) buckets per client. Some implementations use exponentially decaying counters instead — even smaller memory, slightly less precise.

A common refinement, used by Cloudflare: **weighted sliding window approximation**. Instead of B buckets, keep just two adjacent fixed-window counters and linearly interpolate: `estimate = current_count + previous_count * (1 - elapsed_in_current / window_size)`. This is two integers per client — same cost as token bucket — and the error is bounded and acceptable in practice.

### Distributed state

The hardest part isn't the algorithm — it's that requests from one client may hit any of 100 edge servers. Options:

1. **Per-server local limits.** Easy, but each server allows the full limit, so total system limit = N × per-server limit. Sloppy but cheap.
2. **Shared counter via Redis/Memcached.** Every request issues one INCR. Adds latency. Tolerable if Redis is colocated; painful otherwise.
3. **Sharded counters with consistent hashing.** Each client's counter lives on one designated cache node (consistent hashing — Phase B real-world #3). The chosen front-end issues one local INCR to one specific cache node.
4. **Probabilistic distributed limits.** Cloudflare uses techniques where each edge server tracks an estimated global rate and probabilistically rejects requests based on whether the estimate exceeds the limit. The estimate is propagated via gossip. Slightly over-permissive at the edges of the limit, but extremely cheap.

AWS API Gateway leans heavily on token bucket with sharded Redis-style counters. Cloudflare leans more on probabilistic distributed limits at the edge with a backing centralized store for hard limits.

## The tradeoff

The classic tradeoffs:

- **Bursts vs. smoothness**: token bucket allows bursts up to capacity. Sliding window enforces smooth rate. Pick based on what feels right for your users.
- **Precision vs. memory**: bucketed sliding window with 60 buckets is more accurate than 2-bucket interpolation, but uses 30x more storage. At scale, 30x matters.
- **Local vs. global**: Local is fast and slack on the global limit. Global is precise but adds latency on every request. Most large-scale systems do *layered* limits — local-coarse for the cheap reject path, global-precise for the hard limit.
- **Time precision**: token bucket only needs delta times, so it tolerates clock skew within a request's latency window. Sliding window cares about absolute time. Clock skew across data centers can be hundreds of milliseconds — relevant.

## You can implement a toy version of this using Week 11 + Week 14

- Week 14 (queues / deques) — implement a literal sliding-window with a deque of timestamps. Pop old ones, push new ones, count length. Correct but expensive.
- Week 11 (heaps) — alternatively use a sorted structure of timestamps. Useful for thinking about "what's the oldest entry still in the window."
- For token bucket: implement it as a Python class with `acquire(n=1)` returning bool. 20 lines.

A weekend project: build a tiny rate-limited HTTP service. Use Flask + a per-IP token bucket in a dict (local state). Hit it with a script that bursts 100 requests, see 100 succeed; sleep 1 sec, send 100, see only 16 succeed. Now switch to a sliding-window deque algorithm, repeat. See where they behave differently.

Stretch: simulate distributed state with two "servers" sharing a Redis backend, hit them in parallel from a script. You'll quickly see the gotchas — race conditions on read-modify-write, the need for `INCR` rather than `GET; SET`, the question of what happens when Redis is briefly unreachable. These are exactly the questions edge providers spend engineering time on.

The deep lesson: rate limiting looks trivial until you put it in production. Then it becomes a fascinating microcosm of *every* distributed-systems concern: clock skew, eventual consistency, hot keys, failure modes, accuracy-vs-cost tradeoffs. The Week 11/14 data structures are the *trivial* part; the *distributed* part is where the engineering lives.
