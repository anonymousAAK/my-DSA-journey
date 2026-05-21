# Bug Case Study: Twitter Snowflake-style IDs collide when the clock rewinds

**Project**: Twitter Snowflake (open-sourced 2010, later retired but the design lives on in Discord, Sony, Instagram's variant, and dozens of clones). The class of bug — NTP step-back producing duplicate IDs — is documented in Snowflake's own README and in the Cockroach/CrateDB/Sonyflake forks that handle it differently.
**Date**: 2010–present (the design choice; specific incidents documented through ~2016)
**Severity**: correctness (duplicate primary keys, foreign-key violations, broken at-most-once semantics)
**DSA principle**: a monotonic ID generator is a DAG of (time, sequence) tuples whose total order *requires* time to be monotonic — Week 17 (DAGs) / Week 29 (system design)

## What happened

Snowflake generates 64-bit IDs with the layout `[1 sign | 41 timestamp_ms | 10 worker_id | 12 sequence]`. Within a single millisecond a worker can mint 4096 IDs (sequence 0..4095); across milliseconds the timestamp portion advances and the sequence resets. Properties the design promises:

- IDs are **roughly time-sortable** (timestamp is the high bits).
- IDs are **globally unique** as long as worker IDs are unique.
- ID generation is **decentralized** — no network round-trip per ID.

All three rely on the system clock being monotonic. When NTP "steps" the clock backward (a common occurrence on freshly-booted nodes, after long network partitions, or when an admin runs `ntpdate`), the worker can re-mint a (timestamp, worker, sequence) triple it has already used. The result: a primary-key collision that's invisible at insert time if your database accepts duplicates with `ON CONFLICT DO NOTHING`, or a hard failure if it doesn't.

The historically reported failure mode at Twitter (and in the postmortems of several Snowflake-clone deployments since): an NTP step of a few hundred milliseconds after a node restart, followed by an immediate burst of writes, produced a few dozen ID collisions per affected worker. Because the IDs are also used as DAG-edge identifiers in some downstream systems (timelines as DAGs of tweets, for instance), the duplicates broke topological assumptions further downstream — cycles appeared where none should exist.

## The naive code

```java
public synchronized long nextId() {
    long now = System.currentTimeMillis();
    if (now == lastMs) {
        seq = (seq + 1) & SEQ_MASK;
        if (seq == 0) {
            now = waitNextMs(lastMs);   // saturated this ms, wait for the next
        }
    } else {
        seq = 0;
    }
    lastMs = now;
    return ((now - EPOCH) << 22) | (workerId << 12) | seq;
    // BUG: if `now < lastMs` (clock rewind), we silently emit IDs we've
    //      already minted, because `now == lastMs` is false and we reset seq.
}
```

## The DSA insight

Think of the ID space as a **DAG**: each ID is a node, and each "next ID" is an edge from one node to its successor. For the DAG to be a valid total order (the property the rest of the system depends on), the edge-adding operation must produce strictly increasing nodes. That's a *graph invariant*: no two edges should land on the same node.

The clock provides the high bits of every new node. As long as the clock is monotonic, the high bits alone guarantee uniqueness across milliseconds (and the sequence handles within-millisecond uniqueness). Break monotonicity, and the high bits start repeating. Without an explicit invariant check, the generator obediently mints duplicates.

The right fix uses one of three patterns:

1. **Refuse-on-rewind.** If `now < lastMs`, throw — wait for the clock to catch up before generating any IDs. Trades availability for correctness. Snowflake's reference implementation does this.
2. **Logical clock (Lamport-style).** Use `max(now, lastMs)` as the timestamp portion; if the wall clock drifts backward, the generator's internal clock just doesn't move until the wall clock catches up. This is exactly the Lamport timestamp pattern from distributed-systems folklore.
3. **Hybrid logical clock (HLC).** Combine wall-clock and a logical counter so the IDs stay roughly time-ordered even across nodes whose clocks disagree. CockroachDB's MVCC timestamps use HLCs for exactly this reason; the math is short and the property is strong.

The Week 17 / Week 29 frame: the ID generator is a tiny example of a **causality-preserving structure**. The data structure you choose (plain timestamp vs. logical clock vs. HLC) directly determines which invariants you can maintain across faults like clock skew.

## The fix

```java
public synchronized long nextId() {
    long now = System.currentTimeMillis();
    if (now < lastMs) {
        // Option A: refuse. Loses availability briefly; never produces dupes.
        long drift = lastMs - now;
        if (drift > MAX_TOLERABLE_DRIFT_MS) {
            throw new ClockMovedBackwardsException(drift);
        }
        now = lastMs;                       // Option B: logical clock — clamp forward.
    }
    if (now == lastMs) {
        seq = (seq + 1) & SEQ_MASK;
        if (seq == 0) now = waitNextMs(lastMs);
    } else {
        seq = 0;
    }
    lastMs = now;
    return ((now - EPOCH) << 22) | (workerId << 12) | seq;
}
```

For multi-DC deployments, switch to an HLC:

```
hlc.l = max(physical_now, hlc.l, peer_hlc.l)
hlc.c = (hlc.l == previous_hlc.l) ? hlc.c + 1 : 0
id    = (hlc.l << 16) | (hlc.c << 10) | worker_id
```

## What you can learn

- "Use the wall clock as the high bits of an ID" works only if you also enforce that the wall clock is monotonic. Any time you depend on a wall clock for correctness, write down what happens when it lies to you.
- Three standard patterns cover this: refuse, clamp (Lamport), or HLC. Pick based on availability vs. correctness vs. cross-node ordering needs.
- The DAG / graph perspective generalizes: any structure whose invariants depend on a "time" axis (event sourcing, MVCC, CRDTs, vector clocks) needs an explicit story for what "time" means and what happens when the source of truth misbehaves.
- Snowflake-likes are common; clock-skew handling is *not* common in clones. Auditing your in-house ID generator for this pattern takes ten minutes and pays off the first time NTP misbehaves.

## Related curriculum
- Week 17 (Graphs and DAGs — partial vs. total order)
- Week 29 (System design — ID generation, clock skew, distributed correctness)
- `tests/cases/topological_sort.json` — model an ID stream as a DAG, inject a duplicate, and watch the topo-sort fail
