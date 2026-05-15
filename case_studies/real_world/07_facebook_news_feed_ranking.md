# How Ranking Interacts with Sorting + Priority Queues

## The problem

Facebook's News Feed ranks thousands of candidate posts per user per visit. Each user has hundreds of friends, follows hundreds of pages, may be in dozens of groups. For each session, the feed serves the "best" ~30 posts. The candidate set per user is in the low thousands; the ranking is done by an ML model that scores each candidate with a relevance prediction. Then we sort and emit the top 30. All within ~100ms of you opening the app.

## Why the obvious approach didn't work

Naive approach: pull all candidate posts, score each with the ML model, sort descending, output top 30. Mathematically this is "score → sort → top-K," which is correct. It scales badly for two reasons:

1. **The candidate set is too big.** Pulling every post from every connection over the last 7 days could be tens of thousands of candidates. Running an ML model on tens of thousands of items per user is too expensive at Facebook scale.
2. **Sorting all candidates is wasteful when you only need top-30.** Full sort is O(n log n). For top-K, **partial sort** via a min-heap is O(n log K), which for K=30 is about 5 bits cheaper per element, but more importantly it pipelines beautifully with the scoring step.

## What they actually use

The feed-ranking pipeline is roughly:

1. **Inventory generation**: pull a few thousand candidates from each user's connections, group memberships, etc. Use a coarse first-pass filter (recent, not already seen, not blocked, etc.) to cut from "tens of thousands" to a few thousand.

2. **Light ranker**: a cheap model (linear or small MLP, perhaps a few features) scores all candidates. Use this to **prune** down to a few hundred. This is where heap-based top-K matters: maintain a min-heap of size K=300 across the streamed candidates, only invoke the expensive ranker on what survives. O(N log K) instead of full sort.

3. **Heavy ranker**: a large neural net scores the remaining ~300 candidates. This is where the bulk of the ranking signal comes from. Final output is sorted by score.

4. **Diversification and integrity**: rerank to avoid showing 8 posts from the same friend in a row, downweight sensitive content, etc. Custom logic.

5. **Top-K extraction**: take the top 30 after diversification.

The "K-largest with a heap" pattern (Week 11) is used at multiple stages of this pipeline. At each stage, you're asking "give me the top X under some scoring function" — and at each stage, a min-heap of size X gives you O(n log X) instead of O(n log n).

There's another structure-y trick: **time-decay**. Posts get a recency factor in their score so older posts decay out. Equivalent to a min-heap with a TTL — sort of like the Phase 3 LRU+TTL cache, but for "candidate posts" rather than cache entries.

## The tradeoff

The big tradeoff is **multi-stage ranking**: cheap-first pass to prune, expensive model on the survivors. This is a recall-vs-precision tradeoff. The light ranker has high recall (cheaply scoring everything, retaining anything that might be good) but low precision (its scores aren't super accurate). The heavy ranker has high precision but is invoked on a small candidate set. Without the cascade, you'd either run the heavy model on too much (slow) or run only the cheap model (worse ranking quality).

Another tradeoff: **caching the candidate scoring**. If you scored a candidate during a recent session, can you reuse the score 5 minutes later? Yes-ish — recent scores are a good prior, but user context changes (just read a post → don't re-show). Facebook treats scores as ephemeral but caches *inventory* aggressively.

A subtle tradeoff: **online learning**. The ranker is constantly retrained on user behavior — every click, dwell, like is a label. The freshness of the model versus the cost of pushing new weights to thousands of serving machines is itself a system-design problem (out of scope here, but it's why feed systems are also a streaming-ML problem).

## You can implement a toy version of this using Week 11 + Week 15

- Week 11 (heaps) — implement the top-K-with-min-heap pattern. Stream a million scores through a heap of size 30, keep only the top 30.
- Week 15 (sorting algorithms) — implement partial sort and benchmark against full sort. You'll see that for K << N, the heap-based partial sort dramatically outperforms.

Build a toy feed: generate fake users with friends, fake posts with random features (recency, likes, author affinity), score them with a simple linear function, return the top 10. Add a cheap "light ranker" prefilter, see how it lets you handle 10x more candidates at the same latency.

A stretch project: build a two-stage pipeline. Stage 1: heuristic score on all candidates, keep top 100 via heap. Stage 2: more expensive score (maybe loaded from a learned model) on the 100, sort, return top 10. Measure latency vs. ranking quality with synthetic ground-truth. You'll have built a tiny version of what runs at every major social-media company.

The deeper pattern is **filter-then-rank**, and it shows up everywhere there's expensive scoring and cheap filtering: search engines (where it's called "candidate retrieval + reranking"), e-commerce ranking, recommender systems (#2 Discover Weekly), ad auctions. The min-heap is the structural backbone that makes the pruning step linear-time.
