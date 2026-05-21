# Week 29 — System Design for Engineers

> Self-check: `./scripts/journey quiz 29`  |  Next session: `./scripts/journey next`

## Today's session (~45 min)

1. **Concept** (10 min) — Read [`python/caching.py`](python/caching.py) (CONCEPT + KEY POINTS blocks).
2. **Recognize the pattern** (5 min) — Try drills 1-5 in [`patterns.md`](patterns.md) cold.
3. **Implement from spec** (20 min) — Pick Challenge 1 from [`challenges.md`](challenges.md). Code it in `workbook/week_29/attempts/`.
4. **Verify YOUR code** (5 min) — `./scripts/journey verify lru_data_structures workbook/week_29/attempts/<your-file>.py`
5. **Mastery quiz** (5 min) — `./scripts/journey quiz 29`

If you got stuck: open [`python/caching.py`](python/caching.py) and diff against your attempt.
If you finish early: drills 6-10 in `patterns.md`, or Challenge 2.

**Primary language: Python.** Want to compare implementations? See the per-language table below.

---

## Topic overview

This week covers **System Design for Engineers**. You'll touch: caching, consistent hashing, message queues, rate limiting, sharding, system design. The flagship algorithm/concept for the week is implemented in all five languages, and the Python file listed in Today's session is the canonical walkthrough.

## Related materials

| Resource | Use it when |
|----------|-------------|
| Mock interview: [`mock_interviews/06_design_rate_limiter.md`](../mock_interviews/06_design_rate_limiter.md) | A system-design conversation about rate limiting |
| Mock interview: [`mock_interviews/07_consistent_hashing_deep_dive.md`](../mock_interviews/07_consistent_hashing_deep_dive.md) | A deep-dive system-design conversation on consistent hashing |
| [`problems.md`](problems.md) | You want extra practice with company-tagged problems |

## Reference: per-language topic index

<details>
<summary>All implementations (Java / Python / C++ / Rust / Web)</summary>

**Topic index**


| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | caching | `java/caching.java` | `python/caching.py` | `cpp/caching.cpp` | `rust/caching.rs` | `web/caching.html` |
| 2 | consistent hashing | `java/consistent_hashing.java` | `python/consistent_hashing.py` | `cpp/consistent_hashing.cpp` | `rust/consistent_hashing.rs` | `web/consistent_hashing.html` |
| 3 | message queues | `java/message_queues.java` | `python/message_queues.py` | `cpp/message_queues.cpp` | `rust/message_queues.rs` | `web/message_queues.html` |
| 4 | rate limiting | `java/rate_limiting.java` | `python/rate_limiting.py` | `cpp/rate_limiting.cpp` | `rust/rate_limiting.rs` | `web/rate_limiting.html` |
| 5 | sharding | `java/sharding.java` | `python/sharding.py` | `cpp/sharding.cpp` | `rust/sharding.rs` | `web/sharding.html` |
| 6 | system design | `java/system_design.java` | `python/system_design.py` | `cpp/system_design.cpp` | `rust/system_design.rs` | — |

**Survey companions**


Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Interactive index | — | — | — | — | `web/index.html` |

**Topic roadmap**


- **1. caching**
- **2. consistent hashing**
- **3. message queues**
- **4. rate limiting**
- **5. sharding**
- **6. system design**

</details>

## Reference: tradeoff matrix

<details>
<summary>Approach x Time x Space x When-to-prefer</summary>


Flagship topic: System design building blocks (caching, consistent hashing, rate limiting, sharding, message queues).

| Approach (caching strategy) | Read latency | Write latency | Consistency | When to prefer |
|----------|------|--------|-------|----------------|
| Cache-aside (lazy) | Fast on hit, slow on miss | Fast (DB only) | Eventual | Default; read-heavy workloads |
| Read-through | Fast on hit | Fast | Eventual | When the cache layer abstracts the DB |
| Write-through | Fast on hit | Slower (cache + DB) | Strong (cache ↔ DB) | When stale reads are unacceptable |
| Write-behind / write-back | Fast on hit | Fastest writes | Weakest (data-loss risk) | Write-heavy with tolerance for some loss |
| Refresh-ahead | Fastest | Same as DB | Eventual | Predictable hot keys |

| Approach (rate limiting) | Memory | Burst handling | When to prefer |
|----------|------|--------|----------------|
| Fixed window | O(1) per key | Spikes at window edges | Simple per-user counters |
| Sliding window log | O(N) requests | Exact | Low traffic, precise enforcement |
| Sliding window counter | O(1) | Approximate, smooth | Good general default |
| Token bucket | O(1) | Allows controlled bursts | API gateways |
| Leaky bucket | O(1) | Smooths to fixed rate | Strict throughput shaping |

| Approach (sharding) | Rebalancing cost | Hot-spot risk | When to prefer |
|----------|------|--------|----------------|
| Hash modulo N | O(data) on every resize | Low if hash is good | Fixed cluster size |
| Consistent hashing | O(data/N) per node change | Higher for unfortunate keys | Dynamic clusters |
| Consistent hashing + virtual nodes | O(data/N) | Low | Production default |
| Range-based | Cheap key moves | Hot ranges possible | Range scans needed |

</details>

## Reference: anti-patterns to avoid

<details>
<summary>Common mistakes specific to this week's topic</summary>


- **Caching without a TTL** — entries live forever, drift from the source of truth, and you'll be debugging "why is the user seeing 3-day-old data" for the rest of the quarter. Always set a TTL, even a generous one.
- **Read-through cache with thundering herd on key expiry** — when a hot key expires, N concurrent requests all miss and stampede the DB. Use single-flight, request coalescing, or stagger expiries with jitter.
- **Hashing user IDs to shards with `id % N`** — adding a single node remaps almost every key. Use consistent hashing, or sharding by hash-range, so a topology change only moves O(1/N) of the data.
- **Building a message queue on top of a DB table and polling** — works for hundreds of messages/sec, falls over past that. Use a purpose-built queue (Kafka, SQS, RabbitMQ) before you scale.
- **Treating rate limiting as a single-node problem when the service is horizontally scaled** — N replicas each enforcing `M` requests/sec allows `N·M` total. Use a shared store (Redis with Lua) or a sticky-routing layer.

</details>

## Reference: how to run a topic file

<details>
<summary>Java / Python / C++ / Rust / Web one-liners</summary>


From the week's directory:

```bash
# Java
javac java/<file>.java && java -cp java <ClassName>

# Python
python3 python/<file>.py

# C++
g++ -std=c++17 cpp/<file>.cpp -o /tmp/a && /tmp/a

# Rust
rustc --edition 2021 rust/<file>.rs -o /tmp/a && /tmp/a

# Web — open in a browser
open web/<file>.html   # macOS
xdg-open web/<file>.html   # Linux
```

</details>

## Reflection prompts


- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach consistent hashing to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
