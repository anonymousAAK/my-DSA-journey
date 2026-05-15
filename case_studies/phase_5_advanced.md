# Phase 5: Advanced — Live Leaderboard with Range-Sum Queries

## The Word Problem

> The online judge team wants a "regional scoreboard" feature. Users have integer scores that change *constantly* during contests — like 50 updates per second per contest, and we run ~30 concurrent contests. They want the UI to show "sum of scores for users ranked 100-200" and similar range queries in real time. Right now they `SELECT SUM(score) FROM users ORDER BY score LIMIT 100 OFFSET 100` and the DB falls over above ~50k users. Each contest has up to 500k users. Help.

## Step 1: Restate the problem precisely

We have a dynamic ordered set of (user_id, score) pairs. We need to support:

- **Update**: change user u's score from x to y.
- **Range sum by rank**: given rank range [l, r], return the sum of scores of the users ranked l through r (1-indexed, by score descending).

"Ranked l..r" is the tricky bit — it's not a range over user IDs or over time; it's a range over the *sort order*, which is itself changing on every update.

## Step 2: Identify constraints

- Up to 500k users per contest.
- ~50 updates/sec/contest × 30 contests = 1,500 updates/sec total. Per contest, that's 50/sec.
- Range queries: assume similar rate, say 50/sec per contest, often invoked by many viewers.
- Time budget: real-time means well under 100ms end-to-end. The data structure itself should be sub-millisecond.
- Memory: 500k × constant per user → tens of MB per contest. Fine.
- Edge cases:
  - Many users with identical scores (huge ties at score=0 at the start of a contest).
  - Score deltas of 0 (no-op, but don't crash).
  - User with score = 0 ranked vs. unranked? Define: everyone in the contest is ranked.
  - Range queries that exceed the user count.
  - Negative scores (some judges have penalties).

## Step 3: Brute force first

The current SQL approach: full sort on every query. O(n log n) per query, n = 500k → 5M ops, maybe 50ms in C, hundreds of ms in a generic DB query plan. Plus the DB doesn't benefit from incremental maintenance — every query is fresh.

Sort + array brute force in memory: maintain an array sorted by score descending. On update, binary-search to find the user, remove, re-insert at the new position. Removal/insertion in a sorted array is O(n) → 500k ops per update. That's 50/sec × 500k = 25M ops/sec just on updates. Range sum query is O(r - l) → fast. Updates dominate.

We need updates AND queries to both be sub-millisecond.

## Step 4: Identify wasted work

The core question: can we get **both** point-update AND range-sum to be polylog?

Plain arrays: O(1) update, O(n) range-sum, or vice versa with prefix sums.

Prefix sums: O(1) range-sum, O(n) update (every prefix from the updated index to the end changes).

This is the classic motivation for **Fenwick Tree (BIT)** or **Segment Tree** — Week 22 territory. Both give O(log n) for *both* update and range-sum.

But there's a twist: our "index" isn't a user ID, it's a **rank**. And rank changes on every update. We can't just have a tree indexed by user ID; we need indices keyed on the *score order*.

Re-framing: build a tree indexed by **score value** (treat scores as the coordinate). At each score, store the count of users with that score and the sum of their scores. Then:

- "Sum of top-k scores" = sum over the top-k slots in score-descending order.
- "Sum of users ranked l..r" = sum of top-r minus sum of top-(l-1).

Now both operations reduce to: in a BIT/segment tree indexed by score, find the value `s` such that the count of users with score ≥ s is exactly some k, and grab the sum.

## Step 5: Optimize

**Segment tree indexed by score, storing (count, sum) at each leaf.**

Score range: contest-dependent. Let's say scores are bounded in [-10^6, 10^6]. Build a tree on that range (or compress coordinates from the actual scores in play). 2M leaves → segment tree of ~4M nodes. Per contest, manageable.

Each node stores:
- `count`: number of users with score in this leaf's range.
- `sum`: sum of scores of those users.

**Update (change u's score from x to y)**:
- At leaf x: count -= 1, sum -= x. Propagate up.
- At leaf y: count += 1, sum += y. Propagate up.
- O(log range) per update. Range = ~2M, log = 21. ~21 ops per propagation × 2 = 42 ops per update. Trivial.

**Range-sum-by-rank [l..r]**:
- Compute `top_sum(k)` = sum of top-k scores via tree descent: at each node, if the right child has count ≥ remaining_k, descend right; else take the right child's full sum and descend left with remaining_k -= right.count. O(log range).
- Answer = `top_sum(r) - top_sum(l-1)`. Two descents → ~42 ops.

Both ops are well under a microsecond in compiled languages, comfortably sub-ms in Python.

### Coordinate compression

If score values are sparse (e.g., scores are doubles or huge integers), compress to ranks of unique scores. Pre-scan once, build a sorted list of unique scores, map score → compressed index. Tree size = number of distinct scores, not score range.

### Handling ties

Multiple users at the same score: the tree handles this naturally — the leaf stores `count` users contributing `sum` total. The order *within* a tied bucket is arbitrary, which is usually fine for a leaderboard ("top 100" doesn't care which 100 if ten are tied at #95-105). If the product wants stable ordering, secondary sort by user_id and tag each user with a unique `(score, -user_id)` key before inserting.

### Why BIT might also work

A Fenwick Tree (Binary Indexed Tree, also Week 22) supports the same ops with smaller constants and less code. For *sums only*, it's superior to a segment tree. The reason we lean segment tree here is the "find k-th largest" operation, which is more natural on a segment tree (descend by count). On a BIT it's possible via binary lifting but more fiddly.

## Step 6: Implementation gotchas

- **Coordinate compression** must include *all scores that will ever appear*. If scores can change to new values mid-contest, you must use the full possible range, or implement a dynamic / order-statistic tree (balanced BST). The simplest production answer: clamp scores to a bounded range (judges usually do).
- **Negative scores**: shift the coordinate so the smallest possible score maps to index 0.
- **Concurrency**: a single segment tree is not thread-safe. Use one tree per contest plus a per-contest lock; contests are independent, so this scales fine. If a single contest has a hot contention point, consider sharding by score-bucket and aggregating across shards.
- **Memory**: 4M nodes × (4 bytes count + 8 bytes sum) = 48 MB per contest. With 30 contests, 1.4 GB. Use coordinate compression to bring this down 10-100x.
- **Off-by-one**: rank 1 = "best score" — make sure your `top_sum(k)` agrees with the UI's "1-indexed top of leaderboard."
- **Update of nonexistent user**: defend (silently ignore or raise).
- **Reset between contests**: rebuild trees from scratch, don't try to "clear" in place — easy to leave stale state.

## Step 7: Verification

- Toy contest: 5 users, scores [10, 20, 30, 40, 50]. `top_sum(3)` = 120 (50+40+30). Update user 3 from 50 to 5. `top_sum(3)` = 40 + 30 + 20 = 90.
- Ties: 5 users, scores all 10. `top_sum(2)` = 20.
- Stress test: 100k users, random scores, random updates, compare against a `sorted-list` brute force on each query. Run 10k operations.
- Concurrency test: 8 threads doing mixed updates/queries against per-contest locks; verify no torn reads or sum mismatches.

## Step 8: Reflection

What made this hard: the query and update are on **different views** of the data. The user identifies a leaderboard slot ("ranks 100-200"), the update identifies a user ("change u's score"). The data structure has to bridge those two access patterns.

Pattern: **augmented order-statistic tree** — a tree where every internal node has aggregates of its subtree (count + sum), enabling order-statistic queries to descend by those aggregates. The general technique applies any time you need "rank queries + updates" together.

Curriculum tie-in:
- Week 22 (segment trees, BITs).
- Week 23 (binary search on the tree, including the "find k-th" descent).
- Coordinate compression (Week 21 string/array preprocessing tricks).

Where this pattern lives:
- Game leaderboards (literally this).
- Time-series databases ("sum over the last 5 minutes of metric M").
- Inversion counting (Week 22 classic exercise).
- "What's the median of a stream so far" (two heaps OR an order-statistic tree).
- Range-tree-based geometry queries.

The leap from "I can do range queries on a static array" to "I can do range queries while the data is changing" is the entire reason segment trees exist. Once it clicks, an enormous class of problems becomes routine.
