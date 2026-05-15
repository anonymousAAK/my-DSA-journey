# Capstone — Phase 5: Leaderboard Service with Range-Rank Queries

**Time estimate**: 12-15 hours over 2 weekends.
**Prerequisite weeks**: 21-24 (segment trees, Binary Indexed Trees / Fenwick trees, order-statistic structures, concurrency basics).
**Skill checked**: You can pick the right indexed-range structure for the access pattern, implement it from scratch, and wrap it in a service with a real API and tests.

## The Goal
Build a leaderboard service: clients submit `(user_id, score)` updates and query for things like "give me the top 10", "what's user X's rank?", "how many users have scores between 1000 and 2000?". The first two are easy with a sorted set; the third is what makes this a *DSA* capstone — implement it from scratch with a segment tree or Binary Indexed Tree (BIT) over the score domain. Bonus difficulty: handle 1M users without falling over.

## Functional Requirements
- HTTP endpoints (or gRPC; pick one):
  - `POST /score` body `{user_id, score}` — upsert. A user has one current score; submitting a new score replaces the old.
  - `GET /top/{N}` — top N users by score, descending.
  - `GET /rank/{user_id}` — that user's 1-based rank.
  - `GET /count?lo=X&hi=Y` — how many users have scores in `[X, Y]`.
  - `GET /percentile/{user_id}` — what percentile is this user in?
- Must handle 1M users and 10M score updates without crashing.
- Must reject malformed scores (non-integer, out of declared range) with a 400.
- Should support deleting a user (`DELETE /user/{user_id}`).

## Non-functional Requirements
- Performance: each `/count` and each `/rank` returns in under 5ms at the 99th percentile with 1M users in memory. (This is the whole point of the structure choice.)
- Memory: O(score_range + user_count). If your score range is 0..10^9, plan for coordinate compression.
- Code quality: the indexed range structure is its own module with its own tests, *separate* from the HTTP layer. You should be able to swap the BIT for a segment tree without touching the API code.
- Tests: at least 30 tests covering the data structure (random comparison against a brute-force reference), the API, and concurrency.

## Architecture Sketch

```
HTTP request
     |
     v
+-----------+      +-------------------+      +---------------------+
|  Router   | ---> | Validation layer  | ---> |  Leaderboard core   |
+-----------+      +-------------------+      +----------+----------+
                                                         |
                              +--------------------------+--------------+
                              |                                         |
                              v                                         v
                  +-----------+-----------+              +--------------+-----------+
                  | user_id -> score map  |              |  Fenwick tree on scores  |
                  | (hash map)            |              |  count[score]            |
                  +-----------------------+              +--------------------------+
                                                                       |
                                                                       v
                                                            range queries via
                                                            prefix sum differences
```

The hash map answers "what's user X's current score?" in O(1). The Fenwick tree, indexed by score (after compression if needed), answers "how many users have score ≤ S?" in O(log S). Combining the two: `rank(user) = total_users - prefixSum(score-1) + (off-by-one math)`. `count(lo, hi) = prefixSum(hi) - prefixSum(lo-1)`. `top(N)` requires a different structure — see below.

## Implementation Roadmap

1. **Day 1 (3-4h) — Fenwick tree from scratch + tests.**
   Write a `BIT` class with `update(i, delta)` and `query(i)` returning the prefix sum `sum(arr[0..i])`. Test it against a brute-force list implementation using property-based random tests: generate 1000 random ops, run both, compare results. **This step is where most students under-invest.** Bugs in the BIT are subtle and the API layer will mask them.

2. **Day 2 (3-4h) — Leaderboard core.**
   Wire the BIT to the user-score hash map. On `update(user, new_score)`: look up old score, `BIT.update(old_score, -1)` if exists, `BIT.update(new_score, +1)`, write the hash map. On `count(lo, hi)`: `BIT.query(hi) - BIT.query(lo-1)`. On `rank(user)`: `BIT.query(max_score) - BIT.query(score) + 1` (rank = number of users with strictly higher score, plus one — assuming ties get the same rank or a tied-rank policy you've declared).

   **Decide your tie-breaking policy explicitly and document it.** "1224" ranking (Olympic) and "1234" ranking (dense) give different answers for ties and the spec disagreement will produce a lot of wrong-feeling test failures if you skip this step.

3. **Day 3 (2-3h) — Top-N.**
   The BIT doesn't directly answer top-N. Options:
   - **(a)** Maintain a separate sorted structure (skip list, balanced BST, or a sorted std container) on (score, user_id). Top-N is a slice. Updates are O(log N).
   - **(b)** Use the BIT to "walk" — find the K-th largest by binary searching on the BIT (`O(log² N)` or `O(log N)` with the BIT-descent trick). Works for `top(N)` if N is small.
   - **(c)** Use a Fenwick tree of *sorted-buckets-by-score* with explicit user lists; iterate buckets descending until N collected.

   Pick (a) if you want the easy win; pick (b) for the DSA flex. Document the choice.

4. **Day 4 (3-4h) — HTTP layer, concurrency, polish.**
   Wrap the core in an HTTP server. Use a single `RwLock` around the whole core for the first pass — measure throughput, then decide whether to shard if you're not hitting your target. Add `/percentile`, which is just `rank / total_users`. Write a load-test script with `wrk` or `k6` and put numbers in the README.

## Stretch Goals
- Persistence: snapshot the state to disk every N seconds and rebuild on startup. The trick is making the snapshot non-blocking (copy-on-write or shadow-paging).
- Sharding: hash users into K shards, each with its own core. Top-N becomes a merge across shards.
- Time-windowed leaderboards: "top scorers this hour" — needs a sliding window over scores, much harder; consider a CountMinSketch or per-bucket counts.
- Replace the BIT with a segment tree that supports range updates. The tradeoff is constant-factor speed vs. flexibility.
- WebSocket pushes when a user crosses a rank threshold.

## Self-grading rubric
| Criterion | Points | What you're checking |
|-----------|--------|----------------------|
| Correctness on basic inputs | 30 | All five queries return mathematically correct answers against a brute-force reference |
| Handles edge cases | 20 | Empty leaderboard, user with no score, duplicate scores, negative scores if allowed, deletion |
| Algorithm choice is justified (commit message or README) | 15 | Why BIT over segment tree, why your top-N strategy, why your tie-break policy |
| Code is readable (function size, naming) | 15 | BIT module is reusable; HTTP layer doesn't know about BIT internals |
| Tests pass (≥80% coverage on core logic) | 10 | Property-based tests on the BIT are the highest-value tests in the project |
| Stretch goal implemented | 10 | Persistence is the most production-shaped; sharding is the most DSA-shaped |

## When you're done
- Push to a separate repo (or branch) and link it from your portfolio.
- Write a reflection essay in your `SOLUTION_JOURNAL.md`: where did you almost reach for SQL `ORDER BY` and what made you stay with the BIT?
- Compare your final architecture to a real product that does the same thing (see `case_studies/real_world/`). Redis' `ZADD` / `ZRANGE` / `ZRANK` are the canonical comparison — under the hood Redis uses a skip list plus a hash map, which is option (a) from Day 3. Why did Redis pick a skip list over a BIT? (Hint: top-N is *very* common and BIT is awkward at it.)
