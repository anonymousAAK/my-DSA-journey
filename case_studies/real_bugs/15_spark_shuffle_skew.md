# Bug Case Study: Spark stage straggling because one key had 90% of the rows

**Project**: Apache Spark — the shuffle stage in `groupByKey` / `reduceByKey` / SQL aggregations / joins. The class of bug — partition skew — is documented in Spark's own performance tuning guide and is the most common root cause of "one task takes 6 hours, the other 199 finish in 6 minutes" incidents.
**Date**: ongoing pattern, addressed in stages: skew-aware joins (Spark 3.0 AQE, 2020), `salting` recipes documented since ~2014
**Severity**: performance (jobs that should take 10 minutes take 6+ hours; cluster-resource waste; missed SLAs)
**DSA principle**: hash partitioning gives uniform partitions only when the key distribution is uniform — Week 16 (hashing) + Week 17 (graph partitioning analogy)

## What happened

Spark distributes work by hash-partitioning data on a key: `partition_id = hash(key) % num_partitions`. When you `groupByKey` or join, all rows with the same key end up on the same partition, where a single executor processes them. This is great when keys are evenly distributed — each executor gets ~1/N of the work.

It is *terrible* when one key dominates. A common shape:

- A `user_id` column in an event log where 60% of events are from the *anonymous / null* user.
- A `country` join where 40% of rows are from one country.
- A `customer_id` log where one whale customer accounts for half the traffic.
- A web-server access-log analysis grouped by `referrer` where `null` and `direct` together are 80% of rows.

In each case, hash partitioning sends all the dominant-key rows to *one* executor. That executor has to process tens of GB while every other executor handles a few hundred MB. The job's runtime is dominated by the slowest executor — Amdahl's law in its purest form. Spark logs show "199 of 200 tasks complete in 8 min; task 47 still running after 4 hours."

The first commonly-deployed fix is **salting**: append a small random suffix to the skewed key, do a partial aggregation, then strip the suffix and do a final aggregation. The skewed key is artificially split into S buckets (the "salt" factor), spreading its load across S executors.

Spark 3.0's **Adaptive Query Execution (AQE)** adds automated skew handling for joins: at runtime, Spark notices a partition that's much bigger than the median, splits *just that partition* into sub-partitions, and replicates the join's other side as needed. This requires no code changes and handles the common case for SQL/DataFrame jobs.

## The naive code

```scala
// One partition becomes a tar pit if any key dominates.
val perUserCount = events
  .groupByKey(_.userId)
  .mapValues(_.size)
  .collect()
```

```sql
-- Same hazard in SparkSQL:
SELECT user_id, COUNT(*) FROM events GROUP BY user_id;
-- If 60% of rows have user_id = NULL, one reducer gets 60% of the work.
```

## The DSA insight

A hash function `h(key) → partition_id` is a *uniform* assignment **over keys**, not **over rows**. If every key has the same number of rows, you get uniform partitions. If keys are skewed, your partitions inherit the skew exactly. The hash function can't "smooth" a skewed input distribution by construction — it's a pure function of the key, and the key's frequency lives outside its domain.

The Week 17 / graph-partitioning analogy: this is the same hazard as partitioning a graph for parallel processing. If you partition vertices uniformly but one vertex has 1000x more edges than the average, the executor that owns that vertex does 1000x more work. Graph systems (Pregel, GraphX, PowerGraph) solved this by *splitting the vertex*: replicate the heavy vertex across multiple partitions and merge results, which is exactly the "salting" trick generalized.

The deeper algorithmic point: **load balance requires balancing the *work*, not the *key space*.** Hash partitioning balances the key space; that only balances work when the work-per-key is uniform. When it isn't, you need a strategy that's aware of per-key cost:

- **Salting**: explicit per-key fanout for known hot keys.
- **Range partitioning with histograms**: bucket boundaries chosen to balance row counts.
- **Skew-join with broadcast**: if one side of a join is small for the skewed key, broadcast that side and avoid the shuffle entirely for that key.
- **Adaptive runtime repartitioning** (Spark AQE, Flink, Dremel): observe partition sizes mid-job and rebalance.

## The fix

```scala
// Manual salting: split the skewed key into S buckets.
val SALT = 16
import scala.util.Random
val salted = events.map { e =>
  val key = if (e.userId == null || isHot(e.userId)) {
    (e.userId, Random.nextInt(SALT))               // hot keys get a salt
  } else {
    (e.userId, 0)
  }
  (key, 1L)
}

val partial = salted.reduceByKey(_ + _)            // S partial sums per hot key
val finalCounts = partial
  .map { case ((uid, _), cnt) => (uid, cnt) }
  .reduceByKey(_ + _)                              // small final reduction
```

```sql
-- Or in SparkSQL with AQE enabled (Spark 3.0+):
SET spark.sql.adaptive.enabled = true;
SET spark.sql.adaptive.skewJoin.enabled = true;
-- The engine notices and splits skewed partitions at runtime.
```

## What you can learn

- Hash partitioning balances *keys*, not *work*. If you know your key distribution is skewed, plan for it; if you don't know, instrument it.
- "Salting" is the universal pattern: split a hot key by appending a random suffix, do the per-bucket work, then aggregate. It applies far beyond Spark — sharded databases, MapReduce, Flink, even Redis cluster's slot rebalancing use the same idea.
- "P99 stage time / median stage time" is the metric to watch. A healthy job has that ratio < ~3; a skewed job has it 10-100x.
- The graph-partitioning literature (METIS, vertex-cut, edge-cut) generalizes this story: heavy vertices need replication, just like heavy keys need salting.

## Related curriculum
- Week 16 (Hashing — partitioning is hash-based; non-uniform key distributions break the load assumption)
- Week 17 (Graphs — graph partitioning and vertex-cut models)
- Week 29 (System design — sharding and rebalancing strategies)
- `tests/cases/group_by.json` — synthesize a skewed key distribution and measure shuffle imbalance with and without salting
