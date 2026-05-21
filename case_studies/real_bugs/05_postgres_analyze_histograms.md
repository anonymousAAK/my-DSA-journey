# Bug Case Study: Postgres `ANALYZE` produced bad histograms on skewed columns

**Project**: PostgreSQL — `src/backend/commands/analyze.c` and the `pg_statistic` planner stats. Approximate reconstruction of a class of bug that drove multiple rounds of fixes to the planner statistics (`default_statistics_target`, the introduction of `most_common_values`, MCV scaling improvements in 9.x / 10).
**Date**: long-running theme; specific overhauls in 8.4 (auto-ANALYZE), 10 (MCV improvements), 14 (extended statistics)
**Severity**: performance (catastrophic plan choice; a 50 ms query suddenly takes 50 minutes)
**DSA principle**: sample-based percentile estimation needs the right sampling primitive — Week 8 (binary search / order statistics) and Week 15 (reservoir / sketching)

## What happened

The Postgres planner picks join orders and access paths by estimating "how many rows will this predicate match?" That estimate comes from `pg_statistic`, which stores per-column histograms and most-common-value (MCV) lists, built by `ANALYZE`. `ANALYZE` doesn't read the whole table — that would be far too expensive on a billion-row table — it draws a *bounded* sample (default ~30,000 rows, set by `default_statistics_target`) and computes summary statistics from that sample.

The bugs came in three flavors:

1. **Pure-random row sampling doesn't preserve order statistics on skewed columns.** If 99.9% of `status` values are `'ok'` and 0.1% are `'error'`, a 30k-row sample probably contains 0 `'error'` rows; the planner concludes the value doesn't exist; `WHERE status='error'` is estimated to match 0 rows; the planner picks a nested-loop join that's catastrophic on the ~10k actual error rows.
2. **Sorting the whole table to compute exact percentiles is impossible at scale.** Early proposals to fix the skew problem suggested "just take more samples / sort them and pick the K-th." On a 10 TB table that's a TB-scale sort. The original `ANALYZE` code did do a sort-based percentile on the sample — that's fine because the sample is bounded, but it doesn't help with the skew issue, because the sample missed the rare values entirely.
3. **MCV-list cliff effects.** Postgres compensates with a separate "most common values" list — explicit top-K values with their frequencies. But the list was capped at `default_statistics_target` entries (default 100), and when a column had ~120 high-frequency values, the lowest-frequency MCV got *much* better estimates than the highest-frequency non-MCV, producing wildly different row estimates for adjacent values.

The fix arc spanned years: bumping `default_statistics_target`, improving MCV inclusion thresholds, and (in PG14) shipping multi-column "extended statistics" so the planner could estimate joint distributions instead of pretending columns were independent.

## The naive code

```c
/* simplified original sampling */
SampleRows *take_sample(Relation rel, int target_rows) {
    SampleRows *s = palloc(sizeof(*s));
    for (int i = 0; i < target_rows; i++) {
        BlockNumber blk = random_block(rel);
        OffsetNumber off = random_offset_in_block(blk);
        s->rows[i] = read_tuple(blk, off);          // uniform random sample
    }
    return s;
}

/* and then compute percentiles by sort-based selection: */
qsort(s->rows, n, sizeof(Datum), cmp);              // O(n log n)
for (int i = 0; i < HIST_BUCKETS; i++)
    hist[i] = s->rows[i * n / HIST_BUCKETS];        // O(1) per bucket
```

This is fine for evenly distributed columns. It's a disaster for a status enum where one value is 99.9% of rows: the sample contains 0 of the rare values, and the histogram doesn't know they exist.

## The DSA insight

There are *two* algorithmic concepts in tension here.

- **Reservoir sampling (Vitter)** gives you a uniform random sample of size k from a stream of unknown length in one pass, O(n) time, O(k) space. Postgres' `ANALYZE` is approximately reservoir sampling (with block-level optimizations).
- **Quickselect / selection-based percentiles** can find the K-th order statistic in O(n) expected without sorting (Hoare partition). Useful when you've decided your sample size is fixed, but a *uniform* sample is the wrong thing to ask for when the distribution is skewed.

The deeper insight: **the right sampling primitive depends on the question you're asking**. Uniform sampling is right for "what's the median?" — because the median is robust to skew. It's wrong for "what's the frequency of the rarest interesting value?" — because that value, by construction, is unlikely to be in your sample.

The proper tools for skewed-frequency estimation are *sketches*: Count-Min Sketch for approximate frequency, HyperLogLog for cardinality, Misra-Gries / Space-Saving for heavy hitters. These give probabilistic guarantees that uniform sampling cannot. Postgres' MCV list is, in spirit, a Space-Saving sketch — the bug was that its size was capped too small for many real workloads, and that "below the cap" values fell off a frequency cliff.

## The fix

```sql
-- 1. Use the knob that exists:
ALTER TABLE events ALTER COLUMN status SET STATISTICS 1000;
-- bigger sample, bigger MCV list, fewer cliffs.

-- 2. For correlated columns, ask the planner for joint stats (PG14+):
CREATE STATISTICS events_status_kind (dependencies, ndistinct)
    ON status, kind FROM events;

ANALYZE events;
```

And the conceptual fix inside `ANALYZE`: scale the MCV list smoothly with the column's actual heavy-hitter mass, not with a fixed cap; use the sample to *bound* MCV inclusion rather than to *constitute* it directly. See Postgres commits around the 10.x improvements (`compute_scalar_stats`).

## What you can learn

- "Take a uniform random sample, then sort to get percentiles" is fine for **dense, low-skew columns** and dangerous for **skewed columns**.
- The K-th order statistic of a sample is O(n) via quickselect — don't sort the whole sample if you only want a handful of percentiles. (Week 8 / Week 9.)
- Frequency estimation on skewed data needs a *sketch*, not a sample. Sketches give you probabilistic guarantees about the heavy tail that sampling literally cannot.
- Tuning knobs like `default_statistics_target` exist as the user-visible escape hatch for an algorithmic limitation. Knowing *why* the knob exists is the difference between "guess and tweak" and "set it to the right value once."

## Related curriculum
- Week 8 (Binary search, including search-on-answer for percentile-style queries)
- Week 9 (Sorting & selection — quickselect for the K-th element)
- Week 15 (Heap-backed top-K, the natural representation of an MCV list)
- Week 24 / capstone 5 (Sketches: Count-Min, HyperLogLog) — the proper tool for the skew-aware case
- `tests/cases/topk_heap.json` — adapt to a streaming top-K and compare against a Space-Saving sketch on a skewed input
