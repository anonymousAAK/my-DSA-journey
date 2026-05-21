# Bug Case Study: MongoDB `skip(N).limit(20)` is O(N) — and N got big

**Project**: MongoDB (and the *same* hazard in SQL with `OFFSET N`, in Elasticsearch's `from` parameter, in DynamoDB before cursor-based pagination, and in essentially every REST API that exposes a `?page=N` parameter). Concretely documented in MongoDB's own pagination guide and in Stack-Overflow-tier postmortems too numerous to count.
**Date**: ongoing pattern; the most-cited "production incident" period was ~2013–2018 as social-feed apps scaled past a few hundred thousand documents per collection
**Severity**: performance (timeouts on late pages; CPU and I/O burned linearly in page number)
**DSA principle**: indexed lookup is O(log n); offset is O(offset) — Week 8 (binary search / index choice)

## What happened

A common pagination pattern in MongoDB:

```js
db.events.find({ user_id: "abc" })
         .sort({ ts: -1 })
         .skip(page * 20)
         .limit(20);
```

Looks fine. Works fine for page 1. Works fine for page 50. Then page 100,000 — driven by an indexer / scraper / power user — times out. The query log shows MongoDB scanning *2 million documents* to serve a 20-document response.

Why: `skip(N)` is not magic. The database doesn't have a precomputed "20-at-a-time" cursor; it must produce the first N documents matching the filter (in sorted order), throw them away, and then return the next 20. Even with an index on `(user_id, ts)`, walking the index 2 million entries deep is O(N) work, *per query*. A few dozen scrapers paginating to page 100k simultaneously is a multi-million-document-scan workload, and the database CPU pegs.

The classic incident shape: a media site's mobile app prefetches "the next page" aggressively. Most users never go past page 5. A small group of users (or a misbehaving client, or a security scanner) walks pages 1..N sequentially. The site's p99 latency cliffs around page 200; by page 1000 the database is on fire.

The fix is **cursor-based pagination** (also called "keyset pagination" or "seek pagination"): instead of skipping by count, you remember the *last value* and ask for "records after that value." With an index on the sort key, this is O(log n) per page regardless of how deep you are.

## The naive code

```js
// O(N) per page — pages get slower the deeper you go.
function getPage(userId, page) {
  return db.events.find({ user_id: userId })
                  .sort({ ts: -1 })
                  .skip(page * 20)
                  .limit(20)
                  .toArray();
}
```

Equivalent SQL hazard:

```sql
-- Postgres / MySQL: same problem.
SELECT * FROM events
 WHERE user_id = $1
 ORDER BY ts DESC
 OFFSET 20000
 LIMIT 20;
-- Server must produce the first 20020 rows internally to discard 20000.
```

## The DSA insight

A B-tree (or any sorted index) supports two fundamentally different operations cheaply:

1. **Point and range lookup by key**: O(log n + k) where k is the number of results.
2. **Iteration in sorted order from a given start key**: O(log n) to find the start, O(k) to yield k results.

It does *not* support "go to the N-th entry by ordinal position" cheaply unless the index also maintains a per-node count of descendants — and most database indexes don't, because that count must be updated on every insert/delete and the overhead isn't worth it for the rare use case.

The Week 8 mental model: think of an index as a binary search tree, and pagination as a question. "Give me page 1000 of 20" asks "what's the 20000th element in sorted order?" — a *selection* (order-statistic) query, which requires either a tree augmented with subtree sizes (O(log n)) or a linear walk (O(N)). MongoDB's index doesn't have augmented sizes; the linear walk is what you pay for.

"Give me 20 entries with ts older than X" asks a *range* query, which the index supports natively in O(log n + k). Same data, same index — different question, exponentially different cost. That's the entire payoff of cursor-based pagination.

## The fix

```js
// Cursor-based — pass the last ts of the previous page.
function getPage(userId, beforeTs) {
  const query = { user_id: userId };
  if (beforeTs) query.ts = { $lt: beforeTs };
  return db.events.find(query)
                  .sort({ ts: -1 })
                  .limit(20)
                  .toArray();
  // Caller passes back the ts of the last document on the next call.
}
```

```sql
-- Postgres equivalent — keyset pagination:
SELECT * FROM events
 WHERE user_id = $1
   AND (ts, id) < ($last_ts, $last_id)    -- composite key avoids ts-tie pitfalls
 ORDER BY ts DESC, id DESC
 LIMIT 20;
```

The `(ts, id)` composite key handles ties cleanly — without `id`, two events with the same `ts` could cause you to skip or duplicate a row at page boundaries.

When you need a "page N of M" UI affordance (rare in modern apps; common in older paginated tables), maintain an external materialized "index by page" or accept that deep-page latency will degrade, and rate-limit deep-page access at the gateway.

## What you can learn

- `OFFSET N` / `skip(N)` is O(N) in essentially every database. Use it only when N is bounded by a UI cap (≤ ~1000).
- Cursor-based pagination is O(log n) per page and trivially distributable; the API change is small but transformative.
- The same hazard exists in many guises: `LIMIT m OFFSET n`, `from`/`size` in Elasticsearch, `start_index` in some REST APIs, `cursor=int(offset)` in poorly-designed paginators. Recognise the shape, not just the syntax.
- "What question am I asking this index?" is the right framing: range vs. ordinal-position have very different costs, and only the index designer knows which it supports cheaply.

## Related curriculum
- Week 8 (Binary search & search-on-answer — and index structures by extension)
- Week 14 (BSTs — order-statistic trees with subtree counts)
- Week 21 (Self-balancing BSTs and B-trees — what indexes actually are)
- `tests/cases/binary_search.json` — implement a "K-th element in sorted order" query both with and without subtree-size augmentation, and measure
