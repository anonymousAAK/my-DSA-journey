# Phase 5 — Leaderboard Service (reference implementation)

A Fenwick tree (BIT) backing a stdlib HTTP API. ~200 lines, zero dependencies.

```
$ python leaderboard.py     # starts on :8765, runs a demo, then shuts down
$ python test_leaderboard.py
```

## Endpoints

| Method | Path                | Body                                | Returns                                              |
|--------|---------------------|-------------------------------------|------------------------------------------------------|
| POST   | `/score`            | `{"player": str, "score": int}`     | `{"ok": true, ...}`                                  |
| GET    | `/rank/<player>`    | —                                   | `{"player": ..., "rank": int, "score": int}`         |
| GET    | `/top/<k>`          | —                                   | `[{"player": ..., "score": int}, ...]` (up to k)     |
| GET    | `/range/<lo>/<hi>`  | —                                   | `{"count": int}` (players with score in [lo, hi])    |

Score range is `[1, max_score]` (default 10 000). Ties share the same rank (competition style: 1, 1, 3).

## Why a Fenwick tree, not a sorted list

Naive options and their cost for "how many players have score > X":

| Structure              | `set_score` | `rank_of`     | `count_in_range` |
|------------------------|-------------|---------------|------------------|
| `dict` + `sorted()` on read | O(1) | O(N log N) | O(N) |
| `list` kept sorted (`bisect.insort`) | O(N) shift | O(log N) | O(log N) |
| `SortedList` (sortedcontainers) | O(log N) | O(log N) | O(log N) |
| **Fenwick tree over score bins** | **O(log M)** | **O(log M)** | **O(log M)** |

where N = players, M = max possible score. For a leaderboard where scores are bounded integers (game points, ELO buckets, percentile bands), the BIT wins on both updates *and* queries, and the constant factor is small — a 10 000-entry BIT is 40 KB of ints.

The key insight: we don't store one entry per player in the tree. We store *one bucket per score value*, where each bucket counts how many players currently have that score. To rank a player, we ask the BIT how many *buckets above this player's score* are non-empty (`range_sum(score+1, max_score)`) and add 1.

This is the same trick competitive programmers use for "number of inversions" and "k-th smallest element after updates."

## Trade-offs vs. Redis ZSET

Redis `ZSET` is the production answer for this problem at scale. Quick comparison:

| Concern | This BIT | Redis ZSET |
|---------|----------|------------|
| Setup | None — single Python process | Run `redis-server`, configure persistence |
| Single op latency | O(log M) in-process — microseconds | O(log N) over the network — milliseconds |
| Score *granularity* | Integer bins; 10 000 buckets = 10 000 distinct ranks | Arbitrary doubles; ranks are dense |
| Memory | O(M) — empty buckets cost RAM | O(N) — only stored players cost RAM |
| Persistence / replication | None | RDB snapshots, AOF, replicas, Sentinel |
| Throughput ceiling | Pretty much GIL-bound, ~10k req/s | 100k+ ops/sec/instance, clusterable |
| Sharding | DIY | Redis Cluster, hash slots |

The BIT shines when scores are naturally bucketed (game points 0..10 000) and you want zero ops overhead. ZSET wins when scores are real-valued, you need cross-process access, or you outgrow a single Python process.

## Concurrency caveat

All state mutations sit behind one `threading.Lock`. The Python GIL would serialize anyway, but the lock guards the *invariant* between `self.scores[player]` and the BIT bucket — they must be updated together or `rank_of` returns nonsense. If you swap in a non-GIL runtime (PyPy STM, Jython, multi-process), the lock is what keeps you correct.

## Known limits

- **No auth, no rate-limiting** at the HTTP layer (the TinyURL capstone covers rate limiting). For a real service, put it behind a reverse proxy that does both.
- **No persistence.** Server restart = empty leaderboard. Add an append-only log of `set_score` events to replay on boot.
- **Score range is fixed at construction time.** Resizing the BIT means copying everything; rare for a leaderboard but worth knowing.
- **Top-K is O(N log N)** because it sorts the full `dict`. For top-K of a huge leaderboard, you'd walk the BIT from the top score downward and stop after k — exercise for the reader.
