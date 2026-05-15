/*
 * WEEK 29 - JAVA ADVANCED TOPICS
 * Topic: Sharding Strategies
 * File: sharding.java
 *
 * CONCEPT:
 *     Sharding partitions data across multiple nodes so each holds a subset
 *     of the key space. Three common strategies:
 *       1. Range-based:   sort keys, contiguous ranges per shard (good for
 *                         range scans; risk of hot ranges).
 *       2. Hash-based:    shard = hash(key) mod N (good distribution; bad
 *                         rebalancing on N change -- see consistent hashing).
 *       3. Directory-based / lookup: a metadata service maps key -> shard
 *                         (max flexibility, extra hop).
 *
 *     Each strategy trades off write amplification, range-query latency
 *     and rebalance cost.
 *
 * KEY POINTS:
 *     - Range shards keep keys contiguous: fast prefix / range scans, but
 *       hot ranges (e.g. time-sorted writes) bottleneck on one shard.
 *     - Hash shards spread keys evenly but break locality.
 *     - Directory shards give per-key control but require a coordinator
 *       cluster.
 *
 * ALGORITHM / APPROACH:
 *     RANGE:        sort shard boundaries; binary-search by key.
 *     HASH:         shardIdx = hash(key) mod N (we use SHA-256 -> long).
 *     DIRECTORY:    look up key in a registry (HashMap in this demo).
 *
 * DRY RUN / EXAMPLE:
 *     range boundaries = ['c','m','t']:
 *         'apple'->0, 'banana'->0, 'cat'->1, 'mango'->2, 'tiger'->3.
 *     hash N=4: 'user:42' -> some deterministic value mod 4.
 *     directory: explicit mapping registered by the user.
 *
 * COMPLEXITY:
 *     Range: O(log shards).
 *     Hash : O(L) where L is key length (for hashing).
 *     Dir  : O(1).
 */

// snake_case filename is fine; class Sharding is package-private.

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Sharding {

    /** Range-based router: each shard handles keys in [b[i-1], b[i]). */
    static class RangeShardRouter {
        final String[] boundaries;
        RangeShardRouter(String[] boundaries) {
            this.boundaries = boundaries.clone();
            Arrays.sort(this.boundaries);
        }

        int route(String key) {
            // Equivalent of Python's bisect_right.
            int lo = 0, hi = boundaries.length;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (boundaries[mid].compareTo(key) <= 0) lo = mid + 1;
                else hi = mid;
            }
            return lo;
        }
    }

    /** Hash-based router: shardIdx = SHA256(key) mod N. */
    static class HashShardRouter {
        final int n;
        HashShardRouter(int n) { this.n = n; }

        int route(String key) {
            try {
                byte[] d = MessageDigest.getInstance("SHA-256")
                    .digest(key.getBytes(StandardCharsets.UTF_8));
                long h = 0;
                for (int i = 0; i < 8; i++) h = (h << 8) | (d[i] & 0xFF);
                // Make non-negative for modulo arithmetic.
                return (int) Math.floorMod(h, (long) n);
            } catch (NoSuchAlgorithmException e) {
                throw new RuntimeException(e);
            }
        }
    }

    /** Directory router: explicit key -> shard registry. */
    static class DirectoryShardRouter {
        final Map<String, Integer> registry = new HashMap<>();
        void assign(String key, int shard) { registry.put(key, shard); }
        int route(String key) { return registry.getOrDefault(key, -1); }
    }

    public static void main(String[] args) {
        RangeShardRouter range = new RangeShardRouter(new String[]{"c", "m", "t"});
        for (String k : new String[]{"apple", "banana", "cat", "mango", "tiger"})
            System.out.println("range " + k + " -> shard " + range.route(k));

        HashShardRouter hash = new HashShardRouter(4);
        for (String k : new String[]{"user:42", "user:43", "order:99", "session:xyz"})
            System.out.println("hash  " + k + " -> shard " + hash.route(k));

        DirectoryShardRouter dir = new DirectoryShardRouter();
        dir.assign("hot-customer:Acme", 0);
        dir.assign("hot-customer:Globex", 1);
        System.out.println("dir   'hot-customer:Acme' -> shard " + dir.route("hot-customer:Acme"));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in sharding.py:
 *   - Java has no built-in bisect; we open-code bisect_right.
 *   - Python's hashlib.sha256(...).digest() maps to MessageDigest in Java;
 *     we wrap the checked NoSuchAlgorithmException in a RuntimeException.
 *   - Math.floorMod ensures non-negative shard indices when the top 8 bytes
 *     of the digest interpret as a negative signed long.
 *   - The companion system_design.java does NOT cover sharding; we add it
 *     here to mirror the Python / C++ / Rust splits.
 */
