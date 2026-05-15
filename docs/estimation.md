# Estimation Drills — Order-of-Magnitude Thinking

> The single most valuable interview/contest skill that isn't taught explicitly: *back-of-the-envelope sizing*. Will this fit in time? Will it fit in RAM? Is this complexity even plausible? Most "I don't know which algorithm to use" stalls are actually "I haven't done the arithmetic." Do the arithmetic.

This file is 25 drills. Try each one before scrolling to the answer key. The numbers are approximate on purpose — the goal is the right *order of magnitude*, not three significant figures.

---

## Reference numbers to memorize

Burn these into long-term memory. Everything else is derived.

| Operation | Rough cost | Notes |
|---|---|---|
| L1 cache access | ~1 ns | A few clock cycles. |
| L2 cache access | ~4 ns | |
| Main RAM access | ~100 ns | About 100× L1. |
| Branch mispredict | ~5 ns | Worse than a cache hit. |
| Hash-map op (Java/Python) | ~100–500 ns | Hashing + a probe + a comparison. |
| SSD random read (4 KB) | ~100 μs (10⁵ ns) | About 1000× RAM. |
| HDD seek | ~10 ms (10⁷ ns) | About 100,000× RAM. |
| Network round-trip (same data center) | ~500 μs | |
| Network round-trip (cross-continent) | ~100 ms | |
| Modern CPU throughput | ~10⁹ simple ops / sec | One op per ns is the ceiling, not the average. |
| Typical contest budget | ~10⁸ ops / sec | Realistic with the constant factor of an interpreted-ish language. |
| 1 GB RAM | ~2.5×10⁸ ints (4 bytes) or ~10⁸ longs |
| 64-bit pointer | 8 bytes | A Java/Python object is much larger. |

---

## Section A — Time-budget questions (Q1–Q6)

**Q1.** N = 10⁶, algorithm is O(N²), each inner op is 100 ns. Time limit 2 s. Fits?

**Q2.** N = 10⁵, algorithm is O(N log N), inner op is 50 ns. Time limit 1 s. Fits?

**Q3.** N = 20, you want to enumerate all subsets (2^N) and check each in O(N). Per-check cost 10 ns. Fits in 1 s?

**Q4.** You wrote an O(N³) DP for N = 500. Inner op is 30 ns. Time limit 3 s. Fits?

**Q5.** You're benchmarking Python. Each "simple op" costs ~100 ns (it's interpreted). N = 10⁶, algorithm is O(N log N). Time limit 2 s. Fits?

**Q6.** You have 10⁹ items and need to count distinct values. Hash insert is ~200 ns. Time limit 60 s (offline batch). Fits?

---

## Section B — Memory questions (Q7–Q11)

**Q7.** You have 8 GB of RAM. You want to sort a 50 GB file from disk. Plain in-memory sort — possible? If not, what changes?

**Q8.** A graph has 10⁶ vertices and 10⁷ edges. Adjacency matrix or adjacency list? (Assume each entry is 4 bytes.)

**Q9.** DP table is `dp[N][W]` with N = 1000, W = 10⁵, ints. Memory cost?

**Q10.** A trie storing 10⁶ English words, average length 8, ASCII. Naive 26-child array per node — rough memory? What if you switch to a hash-map per node?

**Q11.** You have 4 GB free. You want to load a 12 GB dataset. Three realistic strategies?

---

## Section C — Hardware gap questions (Q12–Q14)

**Q12.** Rank by latency, smallest to largest: SSD random read, L1 cache hit, RAM access, network round-trip across the Atlantic. What's the ratio between the slowest and the fastest?

**Q13.** "Cheap, medium, expensive" operations — give one example of each, with the nanosecond range.

**Q14.** Why is `O(N)` not always faster than `O(N log N)` in practice? (One-sentence answer.)

---

## Section D — Big-O recognition (Q15–Q19)

For each snippet, give the time complexity in terms of N.

**Q15.**
```
for i in 0..N:
  for j in i..N:
    do_O1_thing()
```

**Q16.**
```
function f(n):
  if n <= 1: return 1
  return f(n-1) + f(n-1)
```

**Q17.**
```
i = N
while i > 0:
  do_O1_thing()
  i = i // 2
```

**Q18.**
```
for i in 0..N:
  j = 1
  while j < N:
    do_O1_thing()
    j = j * 2
```

**Q19.**
```
function f(n):
  if n <= 1: return 1
  return f(n/2) + f(n/2) + linear_scan_of_n_items()
```

---

## Section E — Reverse Big-O (Q20–Q25)

Given the target complexity, name the *kind* of algorithm that fits. (Multiple answers are fine.)

**Q20.** O(log N) per query on a static array — what kind?

**Q21.** O(log N) per query on a *changing* array supporting range sum — what kind?

**Q22.** O(N) preprocessing, O(1) per query, "is the sum of `arr[l..r]` equal to X?" — what kind?

**Q23.** O(N + M) where N = nodes and M = edges, on an unweighted graph — what kind?

**Q24.** O(2^N · N) on N up to 20 — what kind?

**Q25.** O(N log N) total, "find the K-th smallest after each insertion" — what kind?

---

## Answer key

### Section A — Time

**A1.** O(N²) at N=10⁶ is 10¹² ops. At 100 ns each that's 10⁵ seconds — about 28 hours. **No.** You need an O(N) or O(N log N) algorithm.

**A2.** 10⁵ · log₂(10⁵) ≈ 10⁵ · 17 ≈ 1.7×10⁶ ops. At 50 ns each that's 8.5×10⁷ ns ≈ 0.085 s. **Yes, easily.**

**A3.** 2²⁰ · 20 ≈ 2.1×10⁷ ops. At 10 ns each ≈ 0.21 s. **Yes.** This is the canonical "subset enumeration is fine for N ≤ 20" result.

**A4.** 500³ = 1.25×10⁸ ops. At 30 ns each ≈ 3.75 s. **Marginal — probably no.** You need to shave a factor with constant-factor tricks (cache-friendly traversal, removing the inner branch) or find an O(N² log N) approach.

**A5.** Python adds a ~10× constant. 10⁶ · log₂(10⁶) ≈ 2×10⁷ ops. At 100 ns each = 2 s. **Right on the edge — risky.** Drop to `numpy`/vectorization or accept that pure-Python will TLE in many judges.

**A6.** 10⁹ · 200 ns = 200 s. **Doesn't fit in 60 s.** You'd switch to a probabilistic structure like HyperLogLog (~constant memory, ~1% error), or shard and parallelize, or sort externally and run a merge-count.

### Section B — Memory

**A7.** **Not possible in memory.** External merge sort: split into ~8 GB chunks, sort each chunk in RAM, write to disk, then K-way merge with small per-chunk buffers. Disk I/O dominates the runtime, so minimize passes — that's what makes "external" sorts a different algorithmic family.

**A8.** Matrix: 10⁶ × 10⁶ × 4 bytes = 4×10¹² bytes = 4 TB. **No.** Adjacency list: ~2×10⁷ entries × 4 bytes = 80 MB. **Use the list.** Matrix only wins when the graph is dense (E ≈ V²) and small.

**A9.** 10³ · 10⁵ · 4 bytes = 4×10⁸ bytes = 400 MB. **Too big for a 256 MB limit.** Rolling array (`dp[2][W]` or `dp[W]` if updates allow) brings it to 800 KB or 400 KB.

**A10.** 26-child array, 8-byte pointers: each node ≈ 208 bytes. Total nodes ≈ 10⁶ × 8 = 8×10⁶. Memory ≈ 1.6 GB — **way too much**. Hash-map-per-node: each node carries only its actual children, so ~2–3 entries on average. Memory drops to a few hundred MB. Better still: a single contiguous array of `(node_id, char) → child_id`, or compressed tries (radix/Patricia).

**A11.** (i) Stream / chunked processing — never load all of it. (ii) Use a memory-mapped file (`mmap`) and let the OS page in only what you touch. (iii) Compress the in-memory representation (varints, bit-packing, columnar). All three are common in practice.

### Section C — Hardware

**A12.** L1 (~1 ns) < RAM (~100 ns) < SSD (~10⁵ ns) < Transatlantic RTT (~10⁸ ns). The slowest is ~10⁸× the fastest. *Eight orders of magnitude.* This is why "where the data lives" dominates real-world performance.

**A13.** Cheap: integer arithmetic, register-resident — ~1 ns. Medium: a hash map operation, a cache miss to RAM — ~100 ns to ~1 μs. Expensive: a disk read, a remote API call — ~10⁴ ns to ~10⁸ ns. *Five orders of magnitude separate cheap from expensive.* Algorithmic choices that change asymptotic complexity matter; constant-factor tweaks within the same tier rarely matter.

**A14.** Constant factors and cache behavior. A tight O(N log N) sort over a contiguous array (mergesort/timsort with sequential access) often beats a "linear" algorithm that hashes every element (random memory access, allocations) — the asymptotic winner isn't always the wall-clock winner for moderate N.

### Section D — Big-O recognition

**A15.** O(N²). Sum of `1 + 2 + … + N = N(N+1)/2`.

**A16.** O(2^N). Each call spawns two of size N−1; depth N; total nodes ~2^N.

**A17.** O(log N). The variable halves each iteration.

**A18.** O(N log N). Outer loop N, inner loop log₂N.

**A19.** O(N log N). Recurrence `T(N) = 2T(N/2) + O(N)` — the master theorem's most famous case (merge sort).

### Section E — Reverse Big-O

**A20.** Binary search, or any precomputed structure: prefix sums, sparse table for RMQ, etc.

**A21.** Fenwick tree (BIT) or segment tree.

**A22.** Prefix sums — compute `pref[i] = arr[0] + … + arr[i-1]`, then `arr[l..r] = pref[r+1] - pref[l]` in O(1).

**A23.** BFS or DFS — every linear-time graph algorithm runs in O(V + E).

**A24.** Bitmask DP — N up to ~20 is the dead giveaway. Each subset is a state; transitions iterate over members. TSP, assignment, set-cover.

**A25.** Two heaps (a max-heap for the lower half, a min-heap for the upper half), or an order-statistic tree. Each insert is O(log N), total O(N log N). Same technique that solves running-median.

---

## How to use this file

Once a week, pick five at random and re-do them without looking. The first time you do them they're a quiz. The fifth time they're a reflex. The reflex is the point — when a problem says `N ≤ 10⁶` you should *immediately* feel that O(N²) is dead, with no conscious arithmetic. That feeling is what frees your attention to actually solve the problem.
