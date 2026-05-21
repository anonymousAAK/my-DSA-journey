# Bug Case Study: Sort libraries DoS'd by sorted input — introsort to the rescue

**Project**: SGI STL `std::sort` (pre-introsort), early Java `Arrays.sort` (pre-2009 dual-pivot quicksort era), Python's pre-Timsort `list.sort` (pre-2.3), most C libraries' `qsort` (POSIX). The concrete "adversarial input attack on textbook quicksort" was the subject of McIlroy's classic 1999 paper "A Killer Adversary for Quicksort."
**Date**: 1990s–2000s (the long mitigation arc)
**Severity**: performance / availability (quadratic blowup → request timeouts → DoS)
**DSA principle**: quicksort's expected O(n log n) is over *random* inputs; specific inputs can force O(n²) — Week 9 (sorting)

## What happened

Classical (Hoare-partition) quicksort picks a pivot from the array and partitions the rest around it. When the pivot is the *median*, the recursion depth is `log n` and total work is `n log n`. When the pivot is the *minimum* (or maximum), the recursion splits the array into 0 and n-1 — recursion depth is n, total work is n². Picking the pivot poorly enough on every recursive call turns quicksort into a DoS vector.

The classical pivot-selection rules and their failure modes:

- **First element** — fails on already-sorted or reverse-sorted input (the single most common real-world shape).
- **Last element** — same; just a mirror.
- **Random** — fails with negligible probability in theory, but McIlroy's 1999 paper showed how an *adversary who can see the source code* can construct an input that triggers worst case for any deterministic pivot-from-input rule, including median-of-three.
- **Median of three (first, middle, last)** — fails on the "Musser ill-killer" sequence and similar constructions; ~2x harder to attack but still attackable.

The real-world incidents:

1. A web framework used `Arrays.sort` on user-supplied input as part of a "deduplicate and order" step in a query parser. An attacker submitted a 100k-element pre-sorted list; sort took ~30 seconds; the request thread was tied up; ten such requests in parallel exhausted the thread pool and the site went down. The fix (Java 7) replaced single-pivot quicksort with dual-pivot quicksort *and* added introspection — see below.
2. The `qsort(3)` implementations in several BSDs had the same hazard; sshd used `qsort` to order keys in some code paths, and adversarial inputs could slow a key exchange to the point of timeout.

The fix that swept the field is **introsort** (Musser, 1997): start with quicksort, but track recursion depth; if it exceeds `2 × log₂(n)`, switch to heapsort for the remainder of *that* recursive call. Heapsort is O(n log n) worst-case; introsort guarantees overall O(n log n) worst-case while keeping quicksort's excellent average-case constant factors. C++'s `std::sort` requires introsort behaviour since C++11; Java moved to dual-pivot quicksort plus depth limits; Python switched to Timsort entirely (a different family — adaptive merge — that's O(n log n) worst case by construction).

## The naive code

```c
void quicksort(int *a, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = a[lo];                                // first-element pivot — danger
    int i = lo, j = hi;
    while (i < j) {
        while (i < j && a[j] >= pivot) j--;
        while (i < j && a[i] <= pivot) i++;
        if (i < j) swap(&a[i], &a[j]);
    }
    swap(&a[lo], &a[i]);
    quicksort(a, lo, i - 1);
    quicksort(a, i + 1, hi);
}
```

Adversarial input: `[1, 2, 3, 4, ..., n]`. Pivot is always the minimum. Recursion depth = n. Total comparisons = n × (n-1) / 2.

## The DSA insight

Quicksort is **average-case optimal** (n log n expected over uniformly random permutations) but **not worst-case optimal**. Anywhere you use it on input you don't control, you should ask:

1. Can the input be adversarial?
2. Can the input be already-sorted (most common real-world bad case)?
3. What's the worst-case ceiling I'm willing to pay?

The Week 9 menu of choices, with worst-case guarantees:

| Algorithm        | Average      | Worst case   | Stable? | Notes                          |
|------------------|--------------|--------------|---------|--------------------------------|
| Quicksort        | O(n log n)   | O(n²)        | No      | Best constants on random input |
| Heapsort         | O(n log n)   | O(n log n)   | No      | Bad cache behavior             |
| Mergesort        | O(n log n)   | O(n log n)   | Yes     | O(n) extra space               |
| Timsort          | O(n)         | O(n log n)   | Yes     | Exploits "runs" in input       |
| Introsort        | O(n log n)   | O(n log n)   | No      | Quicksort + heapsort fallback  |
| Dual-pivot QS    | O(n log n)   | O(n²)*       | No      | Java 7+; rare worst case       |

(*With randomization + introsort-style depth limit in production implementations.)

The introsort move — "use the fast algorithm with the bad worst case, and *detect* when you've hit the bad case to fall back to a slower algorithm with a good worst case" — is a pattern worth memorizing. The same trick appears in: regex engines (Thompson-NFA fallback for catastrophic-backtracking patterns), hash-table probing (switch to a tree when a single bucket exceeds K entries — Java 8 HashMap does this), and skip-list rebalancing.

## The fix

```c
void introsort_impl(int *a, int lo, int hi, int depth_limit) {
    while (hi - lo > THRESHOLD) {
        if (depth_limit == 0) {
            heapsort(a + lo, hi - lo + 1);            // O(n log n) guaranteed
            return;
        }
        int p = partition(a, lo, hi, median_of_three(a, lo, hi));
        introsort_impl(a, p + 1, hi, depth_limit - 1);
        hi = p - 1;                                   // tail-recursion-eliminated
    }
    insertion_sort(a, lo, hi);                        // small arrays
}

void sort(int *a, size_t n) {
    introsort_impl(a, 0, n - 1, 2 * floor_log2(n));
}
```

## What you can learn

- Quicksort is fast *on average*; check whether your call site can see worst-case input before you bet the SLA on it.
- "Sorted or reverse-sorted" is not a rare adversarial input — it's an extremely common natural input (timestamps, IDs, paginated query results).
- The introsort pattern (start with the fast algorithm, detect badness, fall back to a guaranteed-good algorithm) is broadly applicable.
- Stable, predictable sorts (Timsort, mergesort) are worth their slightly worse constants whenever the input distribution is unknown or adversarial.

## Related curriculum
- Week 9 (Sorting — quicksort, mergesort, heapsort, Timsort)
- Week 24 (Amortized & worst-case analysis)
- `tests/cases/quicksort.json` — extend the fixture with adversarial inputs (sorted, reverse-sorted, all-equal) and measure runtime
