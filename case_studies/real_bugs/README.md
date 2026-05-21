# Real bugs from open-source curriculum

> Fifteen short case studies of real (or class-of) bugs from well-known open-source projects, each one where the root-cause insight was a data-structure or algorithm principle from this curriculum. Use these to internalize that the DSA you're learning isn't trivia — it's exactly the kind of thinking that prevents production fires.

Each essay follows the same shape: what went wrong, the naive code, the DSA insight, the fix, takeaways, and links back to the relevant week. Pick the one that matches the week you're currently studying, read it in 5-10 minutes, and you'll have a concrete "this thing I'm learning has shipped to production and broken when someone got it wrong" anchor for the topic.

Honesty note: where a specific commit or issue link is known, it's named. Where the case is documented across many incidents but no single canonical reference exists, the essay says "approximate reconstruction of a class of bug seen in X" — the pattern is real, the specific commit may be composite.

---

| # | Case | Curriculum tie | Class |
|---:|------|---------------:|------|
| 01 | [CPython dict-ordering surprise](01_cpython_dict_ordering.md) | Week 16 | correctness |
| 02 | [Linux O(n) → O(1) → CFS scheduler](02_linux_o1_scheduler.md) | Week 15 / 12 | performance |
| 03 | [React reconciler list keys (O(n²) DOM churn)](03_react_list_keys.md) | Week 16 / 18 | performance |
| 04 | [Git `pack-objects` memory blowup](04_git_pack_objects_memory.md) | Week 13 | performance |
| 05 | [Postgres `ANALYZE` histogram on skewed columns](05_postgres_analyze_histograms.md) | Week 8 / 15 | performance |
| 06 | [V8 hash flooding → SipHash mitigation](06_v8_hash_flooding.md) | Week 16 | security |
| 07 | [Linux memcg LRU drift → workingset/refault](07_linux_memcg_lru_drift.md) | Week 11 / 13 | performance |
| 08 | [Consistent-hashing ring imbalance (no vnodes)](08_consistent_hashing_imbalance.md) | Week 16 / capstone 6 | performance |
| 09 | [Bloom filter sized for the wrong N](09_bloom_filter_misconfigured.md) | Week 16 | correctness |
| 10 | [Twitter Snowflake collisions on clock rewind](10_snowflake_clock_skew.md) | Week 17 / 29 | correctness |
| 11 | [`ArrayList` 1.5x vs 2x growth tradeoffs](11_arraylist_growth_factor.md) | Week 6 | performance |
| 12 | [Quicksort DoS on sorted input → introsort](12_quicksort_adversarial_input.md) | Week 9 | performance |
| 13 | [DNS Kaminsky cache poisoning (predictable IDs)](13_dns_kaminsky.md) | Week 16 / 29 | security |
| 14 | [MongoDB `skip(N)` is O(N) → cursor pagination](14_mongodb_skip_pagination.md) | Week 8 | performance |
| 15 | [Spark shuffle skew → salting / AQE](15_spark_shuffle_skew.md) | Week 16 / 17 | performance |

---

## How to use these

- **Match to your current week.** If you're on Week 11 (LRU), read #7 (memcg). If you're on Week 16 (hashing), you have your pick — #1, #3, #6, #8, #9, #13 all hit it from different angles.
- **Read once, fast.** 5-10 minutes per essay. Don't take notes the first pass; just absorb the story.
- **Try the fixture.** Each essay ends with a `tests/cases/...` pointer suggesting how to extend a canonical fixture to reproduce the bug. Do that for the one or two that bite you hardest.
- **Use them in review.** When `./scripts/journey review` surfaces a skill from a week where one of these bugs lives, re-skim the essay alongside the skill. The story is the recall hook.

## How to use these in mock interviews

Each of these is a *fantastic* "tell me about a time when…" answer, even though the time wasn't yours. Specifically: "If I were designing X, the failure mode I'd watch for is the one Spark hit with shuffle skew — hash partitioning balances keys, not work, so I'd plan to instrument per-partition size and have a salting fallback ready." That's senior-engineer-level reasoning, and it costs you 10 minutes of reading per essay.

## Related curriculum

- [`case_studies/real_world/`](../real_world/) — 15 longer essays that map *algorithms* to *real products* (the inverse framing).
- [`docs/MASTERY.md`](../../docs/MASTERY.md) — the mastery-check system; this README is meant to be read alongside the weekly quizzes.
- [`docs/SPACED_REPETITION.md`](../../docs/SPACED_REPETITION.md) — how to interleave these bug essays with the FSRS review schedule.
