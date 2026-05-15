/*
 * WEEK 29 - JAVA ADVANCED TOPICS
 * Topic: Consistent Hashing with Virtual Nodes
 * File: consistent_hashing.java
 *
 * CONCEPT:
 *     Plain hash-mod-N sharding breaks badly when you add or remove a node:
 *     most keys remap. Consistent hashing arranges hash space as a circle
 *     (0..2^64-1), places each node at multiple points (virtual nodes /
 *     VNs), and assigns a key to the *next* virtual node clockwise. Adding
 *     a node only displaces a 1/N fraction of keys.
 *
 * KEY POINTS:
 *     - Used by: DynamoDB, Cassandra, Memcached clients, Akka, Riak, CDNs.
 *     - Virtual nodes per physical node ensure balanced load and smooth
 *       rebalancing.
 *     - Lookup is O(log(N*V)) via TreeMap.ceilingEntry.
 *     - Removal is symmetric: only neighbours of the removed node inherit
 *       its keys.
 *
 * ALGORITHM / APPROACH:
 *     add_node(name):    for i in range(vnodes): ring[hash(name + "#VN" + i)] = name
 *     remove_node(name): delete all VN entries belonging to it
 *     get_node(key):     find smallest ring entry >= hash(key); wrap if none
 *
 * DRY RUN / EXAMPLE:
 *     ring = empty; add A, B, C with V=150 -> 450 ring entries.
 *     get_node("user:1001"): hash to long, ceilingEntry returns the
 *     next clockwise virtual node and we return its owning physical node.
 *     Adding D moves ~25% of keys to D's neighbourhood.
 *
 * COMPLEXITY:
 *     Time:  add/remove O(V log(NV)); get O(log(NV)).
 *     Space: O(NV).
 */

// snake_case filename is fine; class ConsistentHashing is package-private.

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Map;
import java.util.TreeMap;

class ConsistentHashing {

    static class ConsistentHashRing {
        final int vnodes;
        final TreeMap<Long, String> ring = new TreeMap<>();

        ConsistentHashRing(int vnodes) { this.vnodes = vnodes; }

        long hash(String key) {
            try {
                byte[] d = MessageDigest.getInstance("SHA-256")
                    .digest(key.getBytes(StandardCharsets.UTF_8));
                long h = 0;
                for (int i = 0; i < 8; i++) h = (h << 8) | (d[i] & 0xFF);
                return h;
            } catch (NoSuchAlgorithmException e) {
                throw new RuntimeException(e);
            }
        }

        void addNode(String name) {
            for (int i = 0; i < vnodes; i++) ring.put(hash(name + "#VN" + i), name);
        }

        void removeNode(String name) {
            for (int i = 0; i < vnodes; i++) ring.remove(hash(name + "#VN" + i));
        }

        String getNode(String key) {
            if (ring.isEmpty()) return null;
            Map.Entry<Long, String> e = ring.ceilingEntry(hash(key));
            return (e != null ? e : ring.firstEntry()).getValue();
        }
    }

    public static void main(String[] args) {
        ConsistentHashRing ring = new ConsistentHashRing(150);
        for (String n : new String[]{"server-A", "server-B", "server-C"}) ring.addNode(n);

        String[] keys = {"user:1001", "session:xyz", "order:42"};
        for (String k : keys) System.out.println("  " + k + " -> " + ring.getNode(k));

        System.out.println("\nAfter removing server-B:");
        ring.removeNode("server-B");
        for (String k : keys) System.out.println("  " + k + " -> " + ring.getNode(k));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in consistent_hashing.py:
 *   - Java has java.util.TreeMap (a Red-Black tree); ceilingEntry is the
 *     exact equivalent of bisect_right + wrap-around.
 *   - We compose the long hash from the top 8 bytes of SHA-256, matching
 *     int.from_bytes(digest[:8], 'big') in Python.
 *   - The companion system_design.java already contains a near-identical
 *     ConsistentHashRing; this file restates it stand-alone for parity
 *     with the per-topic split.
 */
