/*
 * WEEK 29 - JAVA ADVANCED TOPICS
 * Topic: Caching -- LRU, LFU, TTL
 * File: caching.java
 *
 * CONCEPT:
 *     Caches keep recently/usefully accessed values close to the consumer
 *     to avoid recomputation or slow backend reads. The eviction policy
 *     decides what to drop when the cache is full:
 *       - LRU (Least Recently Used): evict the entry untouched longest.
 *       - LFU (Least Frequently Used): evict the entry with the smallest
 *         access count; tie-break by recency.
 *       - TTL (Time To Live): each entry expires after a duration.
 *
 * KEY POINTS:
 *     - LRU: HashMap + doubly-linked list -> O(1) get/put.
 *     - LFU: HashMap of values + per-frequency LinkedHashMap buckets ->
 *       O(1) get/put with min-freq tracking.
 *     - TTL: store expiry timestamps; lazily evict on access.
 *     - Used by: Redis, Memcached, CPU caches, CDNs, browsers, IDE indexers.
 *
 * ALGORITHM / APPROACH:
 *     LRU.get(k):  move node k to head; return value.
 *     LRU.put(k):  if exists, update + move; else add at head; if size > cap
 *                  drop tail.
 *     LFU:         maintain freq buckets; bump key from freq f to f+1;
 *                  minFreq tracker for eviction; evict from minFreq bucket's
 *                  oldest entry.
 *     TTL:         expiresAt = now + ttl; on get, drop if past now.
 *
 * DRY RUN / EXAMPLE:
 *     LRU cap=2:
 *         put(1,1); put(2,2); get(1) -> 1 (1 becomes MRU)
 *         put(3,3) -> evicts 2 (LRU)
 *         get(2) -> -1 (miss)
 *     LFU cap=2:
 *         put(1,1); put(2,2); get(1); get(1); put(3,3)
 *         -> evict 2 (freq 1 < freq 3 for key 1).
 *
 * COMPLEXITY:
 *     LRU: O(1) per op. Space O(cap).
 *     LFU: O(1) per op amortised. Space O(cap).
 *     TTL: O(1) per op.
 */

// snake_case filename is fine; class Caching is package-private.

import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

class Caching {

    // -----------------------------------------------------------------------
    // LRU Cache via HashMap + doubly-linked list
    // -----------------------------------------------------------------------
    static class LRUCache {
        static class Node {
            int key, val;
            Node prev, next;
            Node(int k, int v) { key = k; val = v; }
        }

        final int cap;
        final Map<Integer, Node> map = new HashMap<>();
        final Node head = new Node(0, 0), tail = new Node(0, 0);

        LRUCache(int cap) {
            this.cap = cap;
            head.next = tail;
            tail.prev = head;
        }

        private void unlink(Node n) {
            n.prev.next = n.next;
            n.next.prev = n.prev;
        }

        private void addFront(Node n) {
            n.next = head.next;
            n.prev = head;
            head.next.prev = n;
            head.next = n;
        }

        int get(int key) {
            Node n = map.get(key);
            if (n == null) return -1;
            unlink(n);
            addFront(n);
            return n.val;
        }

        void put(int key, int val) {
            Node existing = map.get(key);
            if (existing != null) {
                existing.val = val;
                unlink(existing);
                addFront(existing);
                return;
            }
            Node n = new Node(key, val);
            addFront(n);
            map.put(key, n);
            if (map.size() > cap) {
                Node lru = tail.prev;
                unlink(lru);
                map.remove(lru.key);
            }
        }
    }

    // -----------------------------------------------------------------------
    // LFU Cache via per-frequency LinkedHashMap buckets
    // -----------------------------------------------------------------------
    static class LFUCache {
        final int cap;
        final Map<Integer, Integer> kv = new HashMap<>();
        final Map<Integer, Integer> kf = new HashMap<>();              // key -> freq
        final Map<Integer, LinkedHashMap<Integer, Boolean>> fk = new HashMap<>();
        int minFreq = 0;

        LFUCache(int cap) { this.cap = cap; }

        private void bump(int key) {
            int f = kf.get(key);
            fk.get(f).remove(key);
            if (fk.get(f).isEmpty()) {
                fk.remove(f);
                if (minFreq == f) minFreq = f + 1;
            }
            kf.put(key, f + 1);
            fk.computeIfAbsent(f + 1, k -> new LinkedHashMap<>()).put(key, true);
        }

        int get(int key) {
            if (!kv.containsKey(key)) return -1;
            bump(key);
            return kv.get(key);
        }

        void put(int key, int val) {
            if (cap <= 0) return;
            if (kv.containsKey(key)) {
                kv.put(key, val);
                bump(key);
                return;
            }
            if (kv.size() >= cap) {
                LinkedHashMap<Integer, Boolean> bucket = fk.get(minFreq);
                int evict = bucket.keySet().iterator().next();
                bucket.remove(evict);
                if (bucket.isEmpty()) fk.remove(minFreq);
                kv.remove(evict);
                kf.remove(evict);
            }
            kv.put(key, val);
            kf.put(key, 1);
            fk.computeIfAbsent(1, k -> new LinkedHashMap<>()).put(key, true);
            minFreq = 1;
        }
    }

    // -----------------------------------------------------------------------
    // TTL Cache
    // -----------------------------------------------------------------------
    static class TTLCache<K, V> {
        final long defaultTtlNanos;
        final Map<K, Object[]> data = new HashMap<>(); // value: {V value, Long expiresAt}

        TTLCache(double defaultTtlSeconds) {
            this.defaultTtlNanos = (long)(defaultTtlSeconds * 1_000_000_000L);
        }

        V get(K key) {
            Object[] item = data.get(key);
            if (item == null) return null;
            long expires = (long) item[1];
            if (expires < System.nanoTime()) {
                data.remove(key);
                return null;
            }
            @SuppressWarnings("unchecked")
            V v = (V) item[0];
            return v;
        }

        void put(K key, V value) { put(key, value, defaultTtlNanos); }

        void put(K key, V value, long ttlNanos) {
            data.put(key, new Object[]{value, System.nanoTime() + ttlNanos});
        }
    }

    public static void main(String[] args) throws InterruptedException {
        LRUCache lru = new LRUCache(2);
        lru.put(1, 1); lru.put(2, 2);
        System.out.println("LRU get(1) = " + lru.get(1));
        lru.put(3, 3);
        System.out.println("LRU get(2) = " + lru.get(2) + "  (expected -1)");

        LFUCache lfu = new LFUCache(2);
        lfu.put(1, 1); lfu.put(2, 2);
        lfu.get(1); lfu.get(1);    // freq(1) = 3
        lfu.put(3, 3);             // should evict 2
        System.out.println("LFU get(2) = " + lfu.get(2) + "  (expected -1)");
        System.out.println("LFU get(1) = " + lfu.get(1) + "  (expected 1)");
        System.out.println("LFU get(3) = " + lfu.get(3) + "  (expected 3)");

        TTLCache<String, String> ttl = new TTLCache<>(0.05);
        ttl.put("alpha", "value");
        System.out.println("TTL get(alpha) immediate = " + ttl.get("alpha"));
        Thread.sleep(60);
        System.out.println("TTL get(alpha) after expiry = " + ttl.get("alpha"));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in caching.py:
 *   - Java needs an explicit doubly-linked list for LRU; Python leans on
 *     OrderedDict.move_to_end which already does the same thing.
 *   - LinkedHashMap is the Java analogue of an OrderedDict and is what we
 *     use for the LFU per-frequency buckets.
 *   - System.nanoTime() replaces time.monotonic() for monotonic timing.
 *   - The companion system_design.java has an LRU; we mirror it and add LFU
 *     and TTL to match the Python and C++ splits.
 */
