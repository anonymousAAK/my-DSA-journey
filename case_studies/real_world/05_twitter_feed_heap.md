# How Priority Queues Power a Real-Time Feed

## The problem

When you open Twitter (or any timeline-based social app — Mastodon, Bluesky, Instagram), you see a stream of posts ordered by some notion of "what's most relevant or recent." For a single user that's a manageable computation. For *every* user, where each follows hundreds or thousands of others, where new posts arrive at ~thousands per second globally — naively recomputing each feed on each page load is impossible.

The real problem has two sides. **Read-side**: when a user opens the app, return their top-N timeline in <100ms. **Write-side**: when someone posts, ensure their followers' timelines reflect it within seconds.

## Why the obvious approach didn't work

**Pull-on-read** (the obvious approach): when user U opens the app, look at the people U follows, pull recent posts from each, merge-sort them by time, return top N. For a user following 1,000 accounts, that's 1,000 fetches → merge → cut to 50. Even with parallelism, p99 latency is bad, and the work scales linearly with how many accounts the user follows. Power users with 5,000 follows are the worst case, and they're also your most active users. Disaster.

**Push-on-write** (the inverse): when user A posts, immediately write the post ID into the timeline of every one of A's followers. Reads are now O(1) — just fetch your precomputed timeline. But: when Lady Gaga posts to 80 million followers, you have to do 80 million writes for one tweet. Celebrity fanout is a different disaster.

## What they actually use

The production answer is **a hybrid** built around priority queues at multiple layers.

For most users (those with normal follower counts), Twitter uses **push-on-write**. Each user has a precomputed timeline stored in Redis-like in-memory storage as a sorted set (which is internally a skip-list — itself a heap-like ordered structure) keyed on timestamp or score. New posts get pushed; old posts get evicted when the timeline exceeds, say, 800 entries.

For **celebrities** (a small number with millions of followers), push-on-write is too expensive. Instead, their posts are stored separately. When a follower opens the app, the system **merges**:
1. Their precomputed push-on-write timeline.
2. Recent posts from any celebrities they follow (a small list, fetched live).
3. Then runs the **ranking model** to score and re-order the merged set.

The merge is a classic **k-way merge using a min-heap** (Week 11): one entry per source, heap keyed on score, pop the top, advance that source. This produces a sorted-by-score output in O(N log K) where K is the number of sources.

Then a min-heap of size N is used to extract the top-N highest-scoring posts after the ML model assigns each a relevance score. The heap pattern — push everyone, pop the worst whenever heap exceeds N — gives you "top N out of millions" in linear time with O(N) memory. This is exactly the Week 11 "Top-K elements" problem at scale.

## The tradeoff

The big tradeoff is **read latency vs. write amplification**. Pure push is fast to read, expensive to write at celebrity scale. Pure pull is fast to write, expensive at read. Hybrid is more complex but bounds both — at the cost of more code paths and harder debugging.

A subtler tradeoff: **freshness vs. ranking quality**. Pure-recency feeds (chronological order) need just a merge. Ranked feeds need to score posts using a model, which means the candidate set has to be retrieved first — that's the heap-merge step — *before* you can rank, *before* you cut to top-N. Every step adds latency. Twitter's choice (and Facebook's, Phase B real-world #7) was that quality wins; users tolerate ~150ms extra to get a smarter timeline. Bluesky and Mastodon often lean chronological for their "no algorithm" philosophy — that's a product decision driven by, in part, this engineering tradeoff.

Another: **eviction policy on the timeline cache**. Old posts age out by FIFO or score-based criteria. Inactive users get their timelines garbage-collected entirely — when they return, the timeline is rebuilt lazily. Yet another LRU-shaped problem on top of the heaps.

## You can implement a toy version of this using Week 11

- Week 11 (heaps / priority queues) — the foundational structure. Implement a min-heap from scratch, then use it for "top-K elements from a stream."
- Implement a k-way merge: given K sorted lists, output the merged sorted list using a min-heap of size K. This is the same algorithm Twitter uses to merge celebrity-posts with your precomputed timeline.
- Build a toy timeline service: users follow each other, posts have timestamps and scores, a feed endpoint returns the top 50 most-recent-and-highest-scored posts from people you follow. Use a heap for ranking. You'll find that with a few thousand users it's already fast — and you'll see immediately why naïve scans wouldn't be.

For a stretch: implement a fanout simulator. Track wall-clock cost of a celebrity-vs.-normal-user post. You'll feel the asymmetry that drives the hybrid design.

The deep lesson: **a priority queue isn't a data structure, it's an interface.** "Give me the next-best item, repeatedly" is the abstraction that powers feeds, schedulers, event simulations, Dijkstra (#1), Huffman coding, and a hundred other systems. The Week 11 lesson is one of the most universally applicable in the curriculum.
