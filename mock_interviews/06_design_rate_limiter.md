# Mock Interview: Design a Rate Limiter

**Setup**: Tech lead at a fictional payments API, Cleartender. Candidate has 2 years of experience and has used Redis but never designed a limiter.

**Difficulty**: Design (no single "right" answer)
**Topic**: Weeks 22-25 (system design, queues, sliding windows, distributed counters).

---

## Transcript

**Interviewer**: Design a rate limiter for an HTTP API. You decide the rest.

> 🔍 **What's happening here**: An open prompt. The interviewer wants to see how you scope. Don't pick a design and start typing. Pick the *questions* and start asking.

**Candidate**: Let me scope first. A few questions:
1. What scale — req/s per user, total req/s?
2. Is the limit per user, per IP, per API key, or some combination?
3. What's the limit shape — "100 requests per minute" or "no two requests within X ms"?
4. What's the response when over limit — 429 with retry-after, or queue the request?
5. Is it a single service or distributed across many servers?
6. Hard guarantees (never exceed) or soft (best-effort with drift acceptable)?

**Interviewer**: Pick reasonable answers and walk me through your reasoning.

> 🔍 **What's happening here**: A senior interviewer will sometimes refuse to constrain you, to see if you can pick sensible defaults and justify them. Don't get stuck.

**Candidate**: Reasonable defaults:
1. ~50k QPS total, ~10 req/s peak per user.
2. Per API key, since IPs are noisy behind NAT and per-user requires auth context anyway.
3. "N requests per rolling window of T seconds" — most common ask.
4. 429 with `Retry-After` header.
5. Distributed: many edge nodes accepting traffic.
6. Soft: a few percent overshoot is fine; under-counting is the worse failure since it locks out legit users.

**Interviewer**: Algorithms?

**Candidate**: The classical options:
- **Fixed window counter**: bucket requests by `floor(now / T)`. Simple but suffers from boundary bursts — a client can fire 2N requests in 2 seconds straddling a window boundary.
- **Sliding window log**: store every request's timestamp, evict timestamps older than T. Exact, but memory is O(N) per key.
- **Sliding window counter**: keep counters for the current and previous window, estimate `current_count + prev_count × overlap_fraction`. Bounded memory, ~1% error, the most common production choice.
- **Token bucket**: refill `r` tokens/sec, capacity `B`. Each request consumes 1. Cheap, supports bursts up to `B`. Used by AWS API Gateway, Stripe-style limits.
- **Leaky bucket**: enqueue requests, drain at rate `r`. Smooths traffic but adds latency, used more for shaping than for limiting.

> 🔍 **What's happening here**: The candidate enumerated five algorithms with one-line tradeoffs each. This is the right level of breadth before depth. A common failure mode is to immediately commit to "token bucket because Redis has INCR" without surveying.

**Interviewer**: Which would you build?

**Candidate**: Depends on whether bursts are user-friendly or user-hostile. For a public payments API, bursts are usually fine (legitimate users batch sometimes), so token bucket. For a write endpoint that protects a fragile downstream, leaky bucket because the smoothing is the point. For pure abuse prevention, sliding window counter because it has the tightest "no more than N per T" guarantee without per-request storage.

I'll go with **token bucket** since the spec says public HTTP API.

**Interviewer**: Storage?

**Candidate**: Per-key state is `(tokens, last_refill_ts)`. The refresh formula on a request is:

```
elapsed = now - last_refill_ts
tokens = min(B, tokens + elapsed * r)
if tokens >= 1:
    tokens -= 1
    allow
else:
    deny, retry_after = (1 - tokens) / r
last_refill_ts = now
```

For a single server, in-process map suffices. For distributed, the state must be shared. Two architectures:

**(a) Centralized**: Redis with a Lua script implementing the formula atomically. Each request does one Redis round-trip. Bottleneck: Redis CPU and the network hop. At 50k QPS that's 50k Redis ops/sec — comfortable for a single Redis instance but a tail-latency tax (~1ms added per request).

**(b) Decentralized with periodic reconciliation**: each edge node holds local token buckets. Periodically (every 100ms) it pushes deltas to a central store and pulls updates. Faster (no per-request hop) but allows over-limit by up to one reconciliation interval × edge-node count.

> 🔍 **What's happening here**: The candidate didn't say "I'd use Redis" and stop. They gave the *latency cost* of the centralized design and the *correctness cost* of the decentralized one. That's the actual design tradeoff.

**Interviewer**: Pick one.

**Candidate**: Centralized Redis with Lua, until benchmarks force me off it. The decentralized version is significantly more complex (reconciliation, conflict-free merge, node-departure handling) and only worth it if Redis is the bottleneck. Start simple, measure, then upgrade.

**Interviewer**: Show me the Lua.

**Candidate**:

```lua
-- KEYS[1] = bucket key; ARGV: now, refill_rate, capacity
local key       = KEYS[1]
local now       = tonumber(ARGV[1])
local rate      = tonumber(ARGV[2])
local cap       = tonumber(ARGV[3])

local data = redis.call("HMGET", key, "tokens", "ts")
local tokens = tonumber(data[1])
local ts     = tonumber(data[2])
if tokens == nil then
  tokens = cap
  ts = now
end
local elapsed = math.max(0, now - ts)
tokens = math.min(cap, tokens + elapsed * rate)

local allowed = 0
if tokens >= 1 then
  tokens = tokens - 1
  allowed = 1
end

redis.call("HMSET", key, "tokens", tokens, "ts", now)
redis.call("EXPIRE", key, math.ceil(cap / rate) + 1)

return {allowed, tokens}
```

**Candidate**: A few notes on this:
- Lua means atomicity — no compare-and-swap dance.
- `EXPIRE` based on `cap / rate` lets idle buckets self-clean instead of leaking memory.
- I'm returning the remaining tokens so the application can populate `X-RateLimit-Remaining`.

> 🔍 **What's happening here**: Naming the *operational* concerns — memory leak, response headers — moves the candidate from "I can solve the problem" to "I have shipped this kind of thing".

**Interviewer**: What happens if Redis is down?

**Candidate**: The choice is fail-open (allow all requests) or fail-closed (deny all). For a *quota* limiter — billing-tied — fail-closed. For an abuse limiter that protects downstream services, fail-open is dangerous (you lose your protection just when you might need it most). For an abuse limiter, I'd fall back to an in-process limiter with a much tighter local limit, plus an alert.

**Interviewer**: How do you test this?

**Candidate**: Unit tests on the Lua refresh formula with frozen time. Integration tests with `testcontainers` running real Redis. Load tests with `wrk` to confirm 429s appear at the configured threshold and not before. Specifically, a test that fires 2N requests in 2T seconds straddling a window boundary and asserts that no more than N+epsilon were allowed, to verify we don't have the fixed-window bug.

**Interviewer**: Last question. A customer has 100 services hitting your API and asks for a fair-share limit — none of their services should starve another. How?

**Candidate**: That's a hierarchical bucket: a parent bucket for the customer with rate `R`, and child buckets per service. A request consumes from the child first; the child refills from the parent. This way no single service can drain everything but slack flows where needed. Or, if "fair" means strict equal share, use round-robin / weighted-fair-queueing scheduling on a leaky bucket, where each service has its own queue and the drain rotates.

> 🔍 **What's happening here**: The candidate named two distinct interpretations of "fair-share" (hierarchical vs. round-robin) before picking one. Many candidates would pick one interpretation and accidentally answer the wrong question.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill*.

---

## What was tested
- Clarifying questions: ✅ scoped six dimensions cleanly
- Brute force first: N/A — design problem; survey-then-commit is the analog
- Complexity-driven optimization: ✅ traded Redis RTT against eventual consistency
- Edge cases without prompting: ✅ Redis down, idle buckets, fair-share
- Communication while coding: ✅ annotated the Lua with operational notes
- Handling interviewer hints: ✅ "pick one" → committed cleanly

## Reflection prompts for the learner
- The candidate defaulted to fail-closed for billing, fail-open caveat for abuse. Pick a real product you use and guess which model they use. Why?
- Implement the sliding window counter as a Lua script. Where does the rounding error come from?
- Re-read the "Algorithms" section and write down which algorithm a *DDoS protection* layer should use. (Hint: it's the one that gives an attacker the worst burst margin.)
