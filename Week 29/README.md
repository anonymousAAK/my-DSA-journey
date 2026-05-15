# Week 29

> Self-check: `./scripts/journey quiz 29` — run the mastery checkpoints for this week.

Each topic is implemented in all five languages: **Java, Python, C++, Rust, and Web (HTML/JS)**. The Java track is the primary detailed walkthrough; the others mirror it with idiomatic constructs.

## Topic index

| # | Topic | Java | Python | C++ | Rust | Web |
|---|-------|------|--------|-----|------|-----|
| 1 | caching | `java/caching.java` | `python/caching.py` | `cpp/caching.cpp` | `rust/caching.rs` | `web/caching.html` |
| 2 | consistent hashing | `java/consistent_hashing.java` | `python/consistent_hashing.py` | `cpp/consistent_hashing.cpp` | `rust/consistent_hashing.rs` | `web/consistent_hashing.html` |
| 3 | message queues | `java/message_queues.java` | `python/message_queues.py` | `cpp/message_queues.cpp` | `rust/message_queues.rs` | `web/message_queues.html` |
| 4 | rate limiting | `java/rate_limiting.java` | `python/rate_limiting.py` | `cpp/rate_limiting.cpp` | `rust/rate_limiting.rs` | `web/rate_limiting.html` |
| 5 | sharding | `java/sharding.java` | `python/sharding.py` | `cpp/sharding.cpp` | `rust/sharding.rs` | `web/sharding.html` |
| 6 | system design | `java/system_design.java` | `python/system_design.py` | `cpp/system_design.cpp` | `rust/system_design.rs` | — |

## Survey companions

Cross-cutting files that summarize the week or provide an interactive overview:

| Topic | Java | Python | C++ | Rust | Web |
|-------|------|--------|-----|------|-----|
| Interactive index | — | — | — | — | `web/index.html` |

## How to run a topic file

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

## Topic roadmap

- **1. caching**
- **2. consistent hashing**
- **3. message queues**
- **4. rate limiting**
- **5. sharding**
- **6. system design**

## Tradeoff Matrix

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

## Anti-patterns to avoid

- **Caching without a TTL** — entries live forever, drift from the source of truth, and you'll be debugging "why is the user seeing 3-day-old data" for the rest of the quarter. Always set a TTL, even a generous one.
- **Read-through cache with thundering herd on key expiry** — when a hot key expires, N concurrent requests all miss and stampede the DB. Use single-flight, request coalescing, or stagger expiries with jitter.
- **Hashing user IDs to shards with `id % N`** — adding a single node remaps almost every key. Use consistent hashing, or sharding by hash-range, so a topology change only moves O(1/N) of the data.
- **Building a message queue on top of a DB table and polling** — works for hundreds of messages/sec, falls over past that. Use a purpose-built queue (Kafka, SQS, RabbitMQ) before you scale.
- **Treating rate limiting as a single-node problem when the service is horizontally scaled** — N replicas each enforcing `M` requests/sec allows `N·M` total. Use a shared store (Redis with Lua) or a sticky-routing layer.

## Reflection prompts

- Which topic this week was hardest, and what made it hard?
- Was there a pattern you didn't recognize and had to be told about? Which one?
- If you had to teach consistent hashing to someone with only one minute, what's the one sentence you'd use?
- Looking at last week's anti-patterns list, did you commit any of them this week? Why?
- What's one problem you'd want to revisit in 3 weeks to see if you've internalized the pattern?
