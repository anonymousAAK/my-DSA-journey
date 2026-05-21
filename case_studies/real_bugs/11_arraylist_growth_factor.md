# Bug Case Study: JVM `ArrayList` grows at 1.5x — why neither 1.5x nor 2x is "right"

**Project**: OpenJDK `java.util.ArrayList`, .NET `List<T>` (2x), Go's `append` (1.25x for large slices), Python's `list` (~1.125x for large lists). Approximate reconstruction of the perennial debate visible in the JDK mailing lists, the Folly `fbvector` paper, and Andrei Alexandrescu's 2018 talk.
**Date**: ongoing (Java's 1.5x has been the default since 1.5; Folly's `fbvector` defaulted to 1.5x explicitly to enable in-place reallocation on jemalloc; Python tuned its factor in the 2.x → 3.x era)
**Severity**: performance (memory fragmentation, allocator pressure, occasional OOM that's "spiky" not steady)
**DSA principle**: amortized analysis of dynamic-array growth — Week 6 (arrays / amortized cost)

## What happened

Every dynamic-array implementation (`ArrayList`, `vector`, `List<T>`, Python `list`, Go slice) has the same shape: a backing array of capacity C, a current size n ≤ C, and a "grow" routine that allocates a bigger array, copies, and replaces when n hits C. The question: by *what factor* do you grow?

The textbook answer "2x amortizes append to O(1)" is true but incomplete. The hidden tradeoffs:

- **2x growth**: amortized cost is `2.0` array writes per append (the geometric series sums to 2). Wasted memory at peak is up to 50% (you've just doubled and only used half). Critically, **2x growth makes in-place reallocation impossible**: when you free a block of size C and allocate 2C, the new block can never reuse the old block's address — even concatenated with the previously-freed neighbors, the freed region is only C, never 2C. The allocator must move you somewhere else, every single time.
- **1.5x growth**: amortized cost is `3.0` (slightly worse than 2x). But the geometric series `1 + 1.5 + 1.5² + ...` has the property that the sum of all *previously freed* blocks eventually exceeds the *next* block, which means a contiguous allocator can sometimes reuse the freed memory in place. The exact crossover is at the third or fourth realloc; in practice it means about a third of reallocs on jemalloc/tcmalloc can avoid the copy entirely.
- **<1.5x growth** (Python uses ~1.125 for large lists, Go uses 1.25): even better in-place behavior, even more allocator-friendly, at the cost of *more frequent* reallocs (still amortized O(1), just with a larger constant).

The "bug" angle: a JVM service serving a large request used Java `ArrayList` to accumulate ~10 GB of response chunks. Each grow caused a 1.5x copy. The allocator (default G1) was unable to find a contiguous 15 GB region after the heap had been fragmented by previous requests, and the application threw `OutOfMemoryError` even though `Runtime.freeMemory()` reported 30 GB free. The fix was either `ArrayList.ensureCapacity(expected_total)` to pre-size, or switching to a chunked structure (`ArrayDeque` of `byte[]`).

A symmetric bug appeared in Python: a streaming JSON parser built a `list` of 200M small dict entries; the 1.125x growth meant ~50 reallocs *and* ~5% memory overhead, which sounds fine, but the *peak* memory during the last realloc was 2x the final list size, OOM-killing the process at the very end.

## The naive code

```java
// Roughly what ArrayList does:
public boolean add(E e) {
    if (size == elementData.length) {
        int newCap = elementData.length + (elementData.length >> 1);  // 1.5x
        elementData = Arrays.copyOf(elementData, newCap);             // O(C) copy
    }
    elementData[size++] = e;
    return true;
}
```

Caller (the bug):
```java
List<byte[]> chunks = new ArrayList<>();
while ((chunk = stream.read()) != null) {
    chunks.add(chunk);              // unbounded growth, repeated realloc
}
```

## The DSA insight

The geometric-series amortized argument is short:

```
Insert n items.
Reallocs happen at sizes 1, 2, 4, ..., n  (for 2x growth).
Total copy cost = 1 + 2 + 4 + ... + n ≈ 2n.
Per-insert amortized cost = 2 = O(1).
```

For a factor `r > 1`, the sum is `n × r / (r - 1)`. Plug in r = 2 → factor 2. Plug in r = 1.5 → factor 3. Plug in r = 1.125 → factor 9. The amortized analysis cleanly explains the cost tradeoff and is the kind of derivation Week 6 walks through with pictures.

But amortized analysis alone tells you about **average cost per insert** — it does *not* tell you about:

- The *variance* of per-insert latency (the realloc spikes are O(n)).
- The *allocator behavior* (which is the real reason 1.5x exists in `ArrayList`).
- The *peak* memory (which is what causes OOMs).
- The *cache locality* (a fresh allocation invalidates any prefetched cache lines from the old array).

So "what's the right growth factor?" doesn't have a universal answer — it depends on the allocator (jemalloc favors 1.5x, system malloc doesn't care), the workload (steady inserts vs. one-shot bulk vs. many-small-lists), and the language's runtime (the GC's tolerance for short-lived large allocations matters in JVM/CLR).

## The fix

```java
// 1. Pre-size when you can estimate the total:
List<byte[]> chunks = new ArrayList<>(expectedChunkCount);

// 2. Use a chunked structure when you cannot:
Deque<byte[]> chunks = new ArrayDeque<>();      // node-per-chunk, no realloc

// 3. For very large append-heavy workloads, consider rope / segmented arrays.
```

```python
# Python equivalent: pre-allocate, or stream-process so you never hold the whole thing.
items = [None] * expected_n           # or: itertools.chain / generators
```

## What you can learn

- The growth factor of every dynamic array is a *design decision*, not a free constant. Read the docs of whichever language/runtime you're in, and know what factor it uses before you build a 10 GB list.
- Amortized O(1) per append does *not* mean steady O(1) per append. The reallocs are huge latency spikes; pre-size to avoid them when the size is predictable.
- A "low" growth factor (1.125, 1.25, 1.5) trades amortized cost for allocator friendliness — meaningful on jemalloc/tcmalloc, mostly irrelevant on systems with naive `malloc`.
- When peak memory matters more than amortized cost (very large lists, memory-pressured environments), switch from a contiguous dynamic array to a chunked / segmented structure. Same big-O, much smaller peak.

## Related curriculum
- Week 6 (Arrays — amortized analysis, in-place vs. copy-on-grow)
- Week 24 (Amortized analysis — full treatment)
- `tests/cases/dynamic_array.json` — instrument the canonical fixture to plot per-insert latency vs. insert index, and observe the realloc spikes
