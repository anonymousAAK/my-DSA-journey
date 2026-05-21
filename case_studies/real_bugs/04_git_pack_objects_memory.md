# Bug Case Study: `git gc` OOMs on big repos because the delta-window is unbounded

**Project**: Git `pack-objects` / `git gc` / `git repack`. Approximate reconstruction of a class of bug repeatedly reported across the Git mailing list and the GitHub / GitLab operations teams; concretely visible in the `--window-memory` and `pack.windowMemory` config that exist to mitigate it.
**Date**: ~2007–2015 (multiple rounds of fixes; `--window-memory` shipped in Git 1.5.x; further refinements in the 2.x series)
**Severity**: performance / availability (OOM kills, multi-hour `gc` runs)
**DSA principle**: a sliding window must have an explicit size bound — Week 13 (sliding window)

## What happened

Git stores history as a content-addressed object graph: every blob, tree, and commit is keyed by its SHA-1. To keep the repository small, `git gc` periodically *packs* loose objects into a single pack file, and inside that pack file each object is stored either in full or as a **delta against another similar object** (xdelta-style binary diff).

Finding the best base object to delta against is the hard part. `pack-objects` sorts candidates by `(type, size, suffix-of-pathname, mtime)` so that similar objects are adjacent in the sort, then runs a sliding window over the sorted list: for each candidate, it tries to delta it against the previous *k* objects, picks the smallest delta, and writes that. The window size is `pack.window` (default 10).

The bug: the window holds the *uncompressed contents* of the previous k objects in memory at once, because computing a binary diff against an object requires that object in memory. If your repo contains 500 MB Photoshop files, ten of them in a 10-wide window is 5 GB of resident memory per worker thread. With `pack.threads=8` (the default on modern boxes) and a few hundred large blobs in the sort, `git gc` would suddenly try to hold 40 GB of object payload and the kernel OOM-killer would step in. CI runs of `git gc --aggressive` on monorepos (Linux kernel, Chromium, AOSP) were the most-cited cases.

The "naive sliding window" lesson here is structural: the window's *count* was bounded (k = 10) but its *memory cost* was not.

## The naive code

```c
/* pseudocode of the original loop */
struct object_entry *window[WINDOW_SIZE];   // bounded by COUNT, not BYTES
size_t cursor = 0;

for (size_t i = 0; i < n_candidates; i++) {
    struct object_entry *cur = sorted[i];
    void *cur_data = read_full_object(cur);             // can be hundreds of MB
    for (size_t j = 0; j < WINDOW_SIZE && window[j]; j++) {
        try_delta(cur, cur_data, window[j]);            // both buffers in RAM
    }
    free(window[cursor]->data);
    window[cursor] = cur;                               // never freed unless evicted
    cursor = (cursor + 1) % WINDOW_SIZE;
}
```

## The DSA insight

A *sliding window* is only well-defined if you've committed to what quantity you're sliding over. Week 13 frames the canonical case as "longest substring with at most K distinct characters" — there the window's invariant is "≤ K distinct chars," and the window grows/shrinks to enforce that invariant.

`pack-objects` had two invariants worth caring about: window *length* (number of objects to compare against) and window *memory* (bytes of object data resident). The original code enforced only the first. When object sizes vary by 4–5 orders of magnitude (a 100-byte commit message vs. a 500 MB binary blob), bounding count alone is meaningless.

The fix is the "two-pointer / variable-window" pattern: shrink the window from the left whenever a global resource invariant is violated, not just when a count is exceeded. That's exactly what `--window-memory` did — when adding the new object would push the resident bytes above the threshold, evict from the left until it fits.

The same pattern shows up in TCP's congestion window (cwnd is bounded in bytes, not packets, for the same reason), Kafka's `replica.fetch.max.bytes`, and every connection pool that uses both `max-connections` and `max-memory` limits.

## The fix

```c
struct object_entry *window[WINDOW_SIZE];
size_t window_bytes = 0;
size_t window_memory_limit = pack_window_memory;

for (size_t i = 0; i < n_candidates; i++) {
    struct object_entry *cur = sorted[i];
    void *cur_data = read_full_object(cur);

    /* shrink from the left until the new entry fits the byte budget */
    while (window_count > 0 &&
           window_bytes + cur->size > window_memory_limit) {
        struct object_entry *oldest = pop_left(window);
        window_bytes -= oldest->size;
        free(oldest->data);
    }

    for (size_t j = 0; j < window_count; j++) {
        try_delta(cur, cur_data, window[j]);
    }
    push_right(window, cur);
    window_bytes += cur->size;
}
```

(Real Git also has per-thread memory accounting and a global cap, but the shape is exactly the variable-window pattern.)

## What you can learn

- A sliding window without an explicit *size* invariant — and especially one without a *memory* invariant when element sizes vary wildly — is a memory bomb waiting for a workload that triggers it.
- "Count-bounded" and "memory-bounded" are different invariants. Pick the one that matches the resource you actually care about; sometimes you need both.
- Whenever you write `for j in window: do_work(j)` and `do_work` touches a buffer whose size is *data-dependent*, ask: what's my worst-case bytes-resident-at-once? If you can't answer in one breath, you have a bug.
- Configuration knobs like `pack.windowMemory` exist because the team learned this the hard way; new code should bake the byte cap in from day one, not as an opt-in.

## Related curriculum
- Week 13 (Sliding window)
- Week 11 (LRU cache) — same eviction-from-the-left machinery
- `tests/cases/sliding_window_max.json` — adapt the fixture to bound by sum-of-element-sizes, not count, and see how the answer changes
