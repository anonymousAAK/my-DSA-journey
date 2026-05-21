# Bug Case Study: Linux's O(n) scheduler couldn't survive 1000-process workloads

**Project**: Linux kernel (the 2.4 → 2.6 → CFS scheduler evolution). The "O(1) scheduler" landed in 2.6.0 (Dec 2003); the Completely Fair Scheduler (CFS, heap-backed) replaced it in 2.6.23 (Oct 2007).
**Date**: 2001–2007
**Severity**: performance (latency, fairness, soft real-time)
**DSA principle**: choice of data structure dictates worst-case cost — Week 15 (heaps) and Week 12 (linked structures)

## What happened

Pre-2.6 Linux had an O(n) scheduler: every time the kernel needed to pick the next runnable task, it walked a single linked list of *all* runnable processes and computed a "goodness" score for each, picking the maximum. On a desktop with 30 processes this was invisible. On a server with thousands of threads — or a build farm running `make -j1000` — picking the next task could itself burn a noticeable slice of CPU, and the cost grew linearly with the number of runnable tasks. Latency spiked, fairness degraded, and the kernel literally spent more time deciding what to do than doing it.

Ingo Molnár's "O(1) scheduler" replaced the list with **two arrays of 140 priority queues** (one active, one expired) plus a bitmap that recorded which priority levels had a non-empty queue. Picking the next task became "find the lowest set bit in the bitmap, take the head of that queue" — O(1) regardless of the number of runnable tasks. It shipped in 2.6.0 and ruled for ~four years.

But O(1) had its own pathology: the heuristics that decided "this task is interactive, give it a bonus" were a tangle of ad-hoc rules that misclassified workloads (notably audio and video). In 2007 Con Kolivas's "Rotating Staircase Deadline" prototype showed a *cleaner* model — fair scheduling via virtual runtime — and Ingo Molnár generalized it into CFS, backed by a **red-black tree** keyed by per-task virtual runtime. Pick the next task = leftmost node = O(log n). Inserting a task back after a timeslice = O(log n). Slightly more work per scheduling decision than O(1), but the data-structure shape eliminated the heuristics — fairness fell out of the structure itself.

## The naive code

```c
// 2.4-era pseudocode: walk the entire runqueue.
struct task *pick_next(struct runqueue *rq) {
    struct task *best = NULL;
    int best_score = INT_MIN;
    for_each_task(t, rq) {                    // O(n)
        int s = goodness(t, current);         // ad-hoc heuristic
        if (s > best_score) {
            best_score = s;
            best = t;
        }
    }
    return best;
}
```

## The DSA insight

This is the canonical "what data structure should I use for *find min / find max repeatedly*?" question that Week 15 frames.

- A flat list gives O(1) insert and O(n) extract.
- A sorted array gives O(n) insert and O(1) extract.
- A binary heap gives O(log n) insert and O(log n) extract — and a flat array of 140 priority bins gives O(1) for both *when keys come from a small discrete set*.
- A balanced BST (RB-tree) gives O(log n) for everything *plus* in-order traversal — useful when "next task" needs more than just the max.

The O(1) scheduler exploited the fact that priority is a small bounded integer (0–139): bitmap + per-priority FIFO is the textbook bucketed-priority-queue trick. CFS later traded that constant-factor for the *flexibility* of a continuous key (vruntime is a 64-bit value, not a bucket index), accepting O(log n) in exchange for a simpler, fairer model.

The lesson isn't "O(1) is always best" — CFS chose O(log n) intentionally because the smaller, more uniform algorithm beat the larger, faster-but-hacky one. **Asymptotic class matters, but the constant factor and the policy clarity matter just as much.**

## The fix

```c
// O(1) scheduler (sketch)
struct prio_array {
    unsigned long bitmap[BITS_TO_LONGS(MAX_PRIO)];
    struct list_head queue[MAX_PRIO];          // 140 FIFOs
};

struct task *pick_next(struct runqueue *rq) {
    int idx = sched_find_first_bit(rq->active->bitmap);  // O(1)
    return list_first_entry(&rq->active->queue[idx], ...);
}

// CFS (sketch): RB-tree keyed by vruntime.
struct task *pick_next_cfs(struct cfs_rq *rq) {
    struct rb_node *left = rb_first_cached(&rq->tasks_timeline);  // O(1) amortised
    return rb_entry(left, struct sched_entity, run_node)->task;
}
```

## What you can learn

- "Walk a list and pick the max" is fine for n < ~100 and a disaster for n > ~10,000. Read your call site's expected n before picking a structure.
- A bucketed priority queue (bitmap + FIFO per bucket) is unbeatably fast when keys come from a small discrete domain — schedulers, packet queues, event-loop wheels all use it.
- When the policy is "fair share over time," a self-balancing BST keyed by *amount-already-served* is a beautiful match — the data structure encodes fairness so you don't need heuristics.
- A simpler O(log n) design can beat a complex O(1) one if the simplicity removes a whole category of bugs (the O(1) interactivity heuristics).

## Related curriculum
- Week 15 (Heaps and priority queues)
- Week 12 (Stacks, queues, deques)
- Week 21 (Self-balancing BSTs) — for the CFS RB-tree angle
- `tests/cases/heap_basics.json` — try implementing a bucketed priority queue and benchmarking against `heapq` for small-integer priorities
