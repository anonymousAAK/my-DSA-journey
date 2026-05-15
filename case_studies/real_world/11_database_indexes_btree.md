# B-trees vs LSM Trees vs Hash Indexes

## The problem

A relational database needs to find rows fast. The table might have a billion rows; finding by primary key needs to be sub-millisecond. The database also needs to insert, update, and delete rows, *and* support range queries (`WHERE created_at BETWEEN ? AND ?`). All this while the data lives on disk — far slower than RAM — and while concurrent transactions are mutating things.

Which data structure should the database use to index its rows? The answer surprises people: not the in-memory hash table you'd reach for in a Python project. The classic answer is the **B-tree**, with two important challengers: the **LSM tree** (for write-heavy workloads) and the **hash index** (for exact-match-only workloads).

## Why the obvious approach didn't work

The in-memory choice — a hash table — fails on disk for two reasons:

1. **No range queries.** A hash table tells you "is this key present?" not "give me all keys between X and Y in sorted order." Range scans are essential for SQL.
2. **Cache-unfriendly on disk.** A hash table places keys randomly across disk. Each lookup is one I/O. Disks (and SSDs) reward sequential access — sometimes 100x faster than random — and hash tables make every access random.

The in-memory choice — a balanced BST (red-black tree, AVL) — fails on disk for a different reason: too many node visits per lookup. A BST with 1B keys is ~30 levels deep, so 30 disk I/Os per lookup. At 100µs per random SSD read (back-of-envelope), that's 3 ms — too slow.

You need a tree that's **wide and shallow** — high fanout per node, low depth, optimized for the disk I/O unit (the page, typically 4KB-16KB).

## What they actually use

### B-trees (and B+trees, the variant most databases actually use)

A B+tree node holds many keys (hundreds to thousands), and points to many children. For a billion rows with ~500 entries per node, the tree is just 3-4 levels deep. A point lookup is 3-4 disk reads — easily under a millisecond, often satisfied entirely from RAM since the upper levels of the tree are tiny and pin in cache.

B+trees are **sorted**, so range queries are O(log n) to find the start + sequential traversal of the leaf level. This is why every relational DB primary key uses a B+tree by default: Postgres, MySQL/InnoDB, SQL Server, Oracle, SQLite. Decades of disk-friendly tuning are baked in.

Inserts and deletes are well-defined but **mutating B+tree pages on disk causes write amplification**: changing one row in a page rewrites the entire page (4-16 KB). For write-heavy workloads, that's a problem.

### LSM trees (Log-Structured Merge trees)

Used by Cassandra, RocksDB, LevelDB, ScyllaDB, modern Elasticsearch, the newer storage engines of MyRocks. The idea: never modify data in place. New writes go to an in-memory sorted structure (a "memtable," often a skip list — itself a Week 12 cousin). When the memtable fills, flush to disk as an immutable "SSTable" (sorted file). Reads check memtable + each SSTable. Periodically, a background compaction merges SSTables to keep the read amplification bounded.

LSM trees absorb writes much faster than B+trees — appends to memtable + occasional bulk sequential writes during flush/compaction. The cost: reads may touch multiple SSTables, so they're slower than B+tree reads in the worst case. **Bloom filters** (Phase B real-world #10) are used per SSTable so reads can skip files that definitely don't contain the key.

LSM is the right call when **writes dominate reads** (telemetry, time-series, event logs). B+tree is the right call when **reads dominate or are mixed** (OLTP).

### Hash indexes

Some databases (Postgres has them; Redis uses them for everything) offer hash indexes for exact-match lookups. Fastest possible for `WHERE col = ?` queries: O(1) average. But no range support, no ordering. Niche. Mostly used as **secondary** indexes when you know the column is only queried with equality.

## The tradeoff

The fundamental tradeoff is **read amplification vs. write amplification vs. space amplification**, plus the secondary question of **range vs. point queries**.

| Structure | Read amp | Write amp | Range | Point |
|---|---|---|---|---|
| B+tree | Low (log n disk reads) | Medium (page rewrite) | Yes | Yes |
| LSM | Medium (k SSTables) | Low (sequential appends) | Yes | Yes (with Bloom) |
| Hash | Lowest (1 disk read) | Lowest | No | Yes |

There's also a **space** tradeoff that LSM amplifies: redundant copies in SSTables before compaction can roughly double on-disk size. B+trees don't have this, but they have **internal fragmentation** from half-full pages after deletes.

And one more: **concurrency**. B+trees use latches/locks on individual pages. LSM trees are append-mostly and thus tend to have simpler concurrency stories. This is partly why LSM databases scaled out earlier — fewer locking pitfalls.

## You can implement a toy version of this using Week 12-13 + Week 25

- Week 12-13 (trees + hashing) — implement an in-memory B-tree. Choose a small fanout (say, 4) for educational visibility; 30-line node structures. Implement insert and search.
- Week 25 (advanced — DBs and storage) — implement a tiny LSM tree: an in-memory sorted dict as memtable, flush to a file on disk when it hits N entries. Read by checking memtable then iterating the files. Implement merge.

A weekend project: benchmark both. Insert 1M random keys, then do 100k random reads. Measure throughput. Then do 1M sequential writes. You'll see B-tree reads dominate; LSM writes dominate. The tradeoff is *visible* in microbenchmarks.

Stretch: add a Bloom filter per LSM SSTable, watch read latency drop on the no-match cases.

The deep lesson: data structures aren't chosen in isolation; they're chosen for **the access pattern of the workload**. The right answer in a write-heavy time-series database is *wrong* in an OLTP-heavy transactional database — and vice versa. This is the foundational realization of database engineering. Once you internalize it, you stop asking "which is the best index?" and start asking "which is best *for what*?"
