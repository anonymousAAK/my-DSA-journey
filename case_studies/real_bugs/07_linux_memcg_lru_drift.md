# Bug Case Study: Linux page-cache LRU drifted under cgroups — workingsets evicted prematurely

**Project**: Linux kernel — `mm/vmscan.c`, the per-memcg LRU lists, and the introduction of the **workingset / refault distance** machinery (Johannes Weiner, 2014–2016). Approximate reconstruction of a class of bug heavily discussed on linux-mm and addressed across kernel 3.15 → 4.x.
**Date**: ~2013–2016
**Severity**: performance (sometimes drastic — multi-second I/O stalls under memory pressure)
**DSA principle**: a single global LRU is too coarse; the right structure depends on the access pattern — Week 11 (LRU cache) and Week 13 (multi-queue / CLOCK / 2Q variants)

## What happened

Linux's page-cache eviction policy is a variant of LRU implemented across two lists: an *active* list (recently and frequently used pages) and an *inactive* list (candidates for eviction). When memory pressure rises, the kernel scans the inactive list and reclaims pages from its tail.

This worked beautifully until cgroup memory controllers (memcg) became widely deployed. A *per-cgroup* LRU was added so that one container's eviction didn't blow away another container's pages. But the LRU lists were still pure LRU at the per-cgroup level — and two pathologies emerged:

1. **Streaming workloads thrashed**. A backup process that reads a 50 GB file once pushes 50 GB worth of pages onto the active list, evicting the database's hot working set even though the database pages will be needed again in a millisecond and the backup pages will never be touched again. Pure LRU has no way to distinguish "used once, ever" from "used once, but will be used again." This is the classic "LRU is unaware of *frequency*, only recency" problem.
2. **Refaults were invisible**. Once a hot page was evicted, the kernel knew when it came back (a major page fault) but had no memory of *how long it had been gone* — so it couldn't tell whether the eviction had been a mistake. Two different workloads (one whose evicted pages refault in 10 ms, one whose evicted pages never refault) looked identical to the LRU machinery.

The fix was a clever data-structure addition: a **refault distance ledger**. When the kernel evicts a page from cgroup X's inactive list, it stamps the page's metadata with the current value of the cgroup's *eviction counter*. If the page is ever read back in, the kernel subtracts that stamp from the current counter to compute "how many other pages were evicted while you were gone." If that distance is shorter than the active list — i.e., the page would have *fit* in memory had you been smarter about which page to evict — the page is promoted directly to the active list on refault. This is essentially the **2Q algorithm** (Johnson & Shasha, 1994) implemented as a counter trick instead of an explicit ghost list.

Combined with the existing CLOCK-like reference-bit handling and the per-memcg lists, this transformed memory pressure under containers from "thrash and pray" to "evict the right thing more often than not."

## The naive code

```c
/* simplified pre-workingset eviction */
struct page *evict_one(struct memcg *cg) {
    struct page *p = list_first_entry(&cg->lru_inactive, ...);
    if (page_referenced(p)) {
        /* second-chance: rotate to MRU end */
        list_move_tail(&p->lru, &cg->lru_inactive);
        return NULL;
    }
    list_del(&p->lru);
    return p;                              /* evicted — no memory it was ever here */
}

int fault_in_page(struct page *p, struct memcg *cg) {
    read_from_disk(p);
    list_add(&p->lru, &cg->lru_inactive);  /* always starts inactive — even if it was hot */
    return 0;
}
```

## The DSA insight

Pure LRU is "most-recently-used wins," full stop. That's a one-dimensional ranking on a fundamentally two-dimensional problem (recency *and* frequency, or recency *and* refault rate). The classical cache-eviction literature has a whole zoo of structures that try to capture the missing dimension:

- **2Q (Johnson–Shasha)**: an A1 queue for first-time-seen pages (FIFO), and an Am list for promoted pages (LRU). If a page in A1 is re-referenced, it gets promoted to Am — protecting "scanned once, never seen again" pages from displacing hot pages.
- **LRU-K**: track the last K references per page and evict the page with the oldest K-th reference.
- **ARC (Adaptive Replacement Cache)**: balance a recency list and a frequency list with a moving partition that adapts to the workload.
- **CLOCK / CLOCK-Pro**: approximate LRU using reference bits and a circular scan — much cheaper than a real linked list, used as the base of Linux's page cache.

The refault-distance trick is essentially a *compressed* ghost list: instead of remembering every evicted page (the 2Q way), remember a single integer counter and a per-page stamp. O(1) space per evicted page is the practical version of an O(n) ghost list. Same algorithmic spirit, much friendlier kernel-memory footprint.

The broader lesson: when LRU misbehaves, don't tune LRU — *change the structure*. Most caches in production code (filesystem, CPU, database buffer pool) are some hybrid that captures frequency or refault distance in addition to recency.

## The fix

```c
/* simplified workingset-aware version */
struct page *evict_one(struct memcg *cg) {
    struct page *p = list_first_entry(&cg->lru_inactive, ...);
    list_del(&p->lru);
    p->workingset_stamp = atomic_read(&cg->eviction_counter);  /* remember eviction time */
    atomic_inc(&cg->eviction_counter);
    return p;
}

int fault_in_page(struct page *p, struct memcg *cg) {
    read_from_disk(p);
    if (p->workingset_stamp) {
        uint64_t distance = atomic_read(&cg->eviction_counter) - p->workingset_stamp;
        if (distance < active_list_size(cg)) {
            /* this page would have fit — promote directly to active */
            list_add(&p->lru, &cg->lru_active);
            return 0;
        }
    }
    list_add(&p->lru, &cg->lru_inactive);
    return 0;
}
```

## What you can learn

- Pure LRU has known pathologies on streaming and mixed workloads. If your cache hit ratio surprises you, the eviction policy is the place to look before tuning the size.
- "Remember a tiny piece of state per eviction" is often the cheapest way to add frequency or refault awareness to an LRU. You don't need a full ghost list to get most of 2Q's benefit.
- Linux's page cache is a great real-world case study in cache-eviction algorithms — most "academic" structures (2Q, LRU-K, ARC) have at least one paper showing they beat the kernel's default on some workload, and the kernel has absorbed the ideas it can implement at O(1) per page.
- "What's the access pattern?" is the question whose answer dictates the structure. LRU assumes recency dominates; if it doesn't, change structures, don't tune parameters.

## Related curriculum
- Week 11 (LRU cache — the doubly-linked-list-plus-hash-map base)
- Week 13 (Sliding window — related "bounded recent history" intuition)
- Week 24 / capstone 5 (Cache architectures and sketches)
- `tests/cases/lru_cache.json` — extend the fixture with a scan workload and observe LRU vs. 2Q vs. ARC hit-rate differences
