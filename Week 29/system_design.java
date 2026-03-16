// Week 29: System Design - Consistent Hashing, LRU Cache, Rate Limiter, Trie, Merkle Tree

import java.util.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

public class system_design {

    // === Consistent Hashing with Virtual Nodes ===
    // Used by: DynamoDB, Cassandra, load balancers
    // Lookup: O(log(N*V)) via TreeMap ceiling   Space: O(N*V)
    static class ConsistentHashRing {
        TreeMap<Long, String> ring = new TreeMap<>();
        int vnodes;

        ConsistentHashRing(int vnodes) { this.vnodes = vnodes; }

        long hash(String key) {
            try {
                byte[] d = MessageDigest.getInstance("SHA-256").digest(key.getBytes());
                long h = 0;
                for (int i = 0; i < 8; i++) h = (h << 8) | (d[i] & 0xFF);
                return h;
            } catch (NoSuchAlgorithmException e) { throw new RuntimeException(e); }
        }

        // O(V * log(N*V))
        void addNode(String node) {
            for (int i = 0; i < vnodes; i++) ring.put(hash(node + "#VN" + i), node);
        }

        // O(V * log(N*V))
        void removeNode(String node) {
            for (int i = 0; i < vnodes; i++) ring.remove(hash(node + "#VN" + i));
        }

        // O(log(N*V)) — walk clockwise to next virtual node
        String getNode(String key) {
            if (ring.isEmpty()) return null;
            Map.Entry<Long, String> e = ring.ceilingEntry(hash(key));
            return (e != null ? e : ring.firstEntry()).getValue();
        }
    }

    // === LRU Cache (HashMap + Doubly Linked List) ===
    // O(1) get and put, O(capacity) space
    static class LRUCache {
        class Node { int key, val; Node prev, next; Node(int k, int v) { key=k; val=v; } }
        int capacity;
        Map<Integer, Node> cache = new HashMap<>();
        Node head = new Node(0,0), tail = new Node(0,0);

        LRUCache(int cap) { capacity = cap; head.next = tail; tail.prev = head; }
        void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }
        void addFront(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }

        int get(int key) {
            if (!cache.containsKey(key)) return -1;
            Node n = cache.get(key); remove(n); addFront(n);
            return n.val;
        }
        void put(int key, int val) {
            if (cache.containsKey(key)) remove(cache.get(key));
            Node n = new Node(key, val); addFront(n); cache.put(key, n);
            if (cache.size() > capacity) { Node lru = tail.prev; remove(lru); cache.remove(lru.key); }
        }
    }

    // === Token Bucket Rate Limiter ===
    // Allows bursts up to capacity, enforces average rate
    // O(1) per request, O(1) space per limiter
    // Used by: API gateways (Stripe, AWS), nginx
    static class TokenBucket {
        int maxTokens;
        double refillRate, tokens;
        long lastRefill;

        TokenBucket(int maxTokens, double refillRate) {
            this.maxTokens = maxTokens;
            this.refillRate = refillRate;
            this.tokens = maxTokens;
            this.lastRefill = System.nanoTime();
        }

        synchronized boolean allowRequest() {
            long now = System.nanoTime();
            tokens = Math.min(maxTokens, tokens + (now - lastRefill) / 1e9 * refillRate);
            lastRefill = now;
            if (tokens >= 1) { tokens--; return true; }
            return false; // 429 Too Many Requests
        }
    }

    // === Trie Autocomplete with Frequency Ranking ===
    // Insert: O(L)   Search: O(L + M + K log K)   Space: O(N*L)
    // Used by: search engines, IDE completion, phone keyboards
    static class TrieNode { Map<Character,TrieNode> children = new HashMap<>(); boolean isEnd; int freq; }
    static class AutoComplete {
        TrieNode root = new TrieNode();
        void insert(String word, int freq) {
            TrieNode n = root;
            for (char c : word.toCharArray()) { n.children.putIfAbsent(c, new TrieNode()); n = n.children.get(c); }
            n.isEnd = true; n.freq += freq;
        }
        void insert(String word) { insert(word, 1); }

        List<String> suggest(String prefix, int k) {
            TrieNode n = root;
            for (char c : prefix.toCharArray()) { if (!n.children.containsKey(c)) return List.of(); n = n.children.get(c); }
            List<int[]> results = new ArrayList<>(); List<String> words = new ArrayList<>();
            dfs(n, new StringBuilder(prefix), words, results);
            PriorityQueue<int[]> pq = new PriorityQueue<>((a,b) -> b[0]-a[0]);
            for (int i = 0; i < results.size(); i++) pq.offer(new int[]{results.get(i)[0], i});
            List<String> out = new ArrayList<>();
            while (!pq.isEmpty() && out.size() < k) out.add(words.get(pq.poll()[1]));
            return out;
        }
        void dfs(TrieNode n, StringBuilder sb, List<String> words, List<int[]> freqs) {
            if (n.isEnd) { words.add(sb.toString()); freqs.add(new int[]{n.freq}); }
            for (var e : n.children.entrySet()) { sb.append(e.getKey()); dfs(e.getValue(), sb, words, freqs); sb.deleteCharAt(sb.length()-1); }
        }
    }

    // === Merkle Tree with Proof Verification ===
    // Build: O(N)   Proof/Verify: O(log N)   Space: O(N)
    // Used by: Bitcoin, Git, IPFS, DynamoDB anti-entropy
    static class MerkleTree {
        List<List<String>> tree = new ArrayList<>(); // [0]=leaves, [last]=[root]

        static String sha256(String input) {
            try {
                byte[] d = MessageDigest.getInstance("SHA-256").digest(input.getBytes());
                StringBuilder sb = new StringBuilder();
                for (byte b : d) sb.append(String.format("%02x", b));
                return sb.toString();
            } catch (NoSuchAlgorithmException e) { throw new RuntimeException(e); }
        }

        MerkleTree(List<String> data) {
            List<String> leaves = new ArrayList<>();
            for (String d : data) leaves.add(sha256(d));
            if (leaves.size() % 2 != 0) leaves.add(leaves.get(leaves.size() - 1));

            tree.add(new ArrayList<>(leaves));
            List<String> cur = leaves;
            while (cur.size() > 1) {
                List<String> next = new ArrayList<>();
                for (int i = 0; i < cur.size(); i += 2) {
                    String right = (i + 1 < cur.size()) ? cur.get(i + 1) : cur.get(i);
                    next.add(sha256(cur.get(i) + right));
                }
                tree.add(next);
                cur = next;
            }
        }

        String root() { return tree.get(tree.size() - 1).get(0); }

        // Returns list of (siblingHash, siblingIsLeft) — O(log N)
        List<Map.Entry<String, Boolean>> getProof(int index) {
            List<Map.Entry<String, Boolean>> proof = new ArrayList<>();
            int idx = index;
            for (int level = 0; level < tree.size() - 1; level++) {
                List<String> layer = tree.get(level);
                if (idx % 2 == 0) {
                    String sib = (idx + 1 < layer.size()) ? layer.get(idx + 1) : layer.get(idx);
                    proof.add(Map.entry(sib, false));
                } else {
                    proof.add(Map.entry(layer.get(idx - 1), true));
                }
                idx /= 2;
            }
            return proof;
        }

        // Recompute hash path and compare to root — O(log N)
        static boolean verifyProof(String data, List<Map.Entry<String, Boolean>> proof, String root) {
            String cur = sha256(data);
            for (var entry : proof) {
                cur = entry.getValue()
                    ? sha256(entry.getKey() + cur)
                    : sha256(cur + entry.getKey());
            }
            return cur.equals(root);
        }
    }

    public static void main(String[] args) {
        System.out.println("=== WEEK 29: System Design for Engineers ===\n");

        // 1. Consistent Hashing
        System.out.println("--- Consistent Hashing ---");
        ConsistentHashRing ring = new ConsistentHashRing(150);
        ring.addNode("server-A"); ring.addNode("server-B"); ring.addNode("server-C");
        for (String k : new String[]{"user:1001", "session:xyz", "order:42"})
            System.out.println("  " + k + " -> " + ring.getNode(k));
        ring.removeNode("server-B");
        System.out.println("After removing server-B:");
        for (String k : new String[]{"user:1001", "session:xyz", "order:42"})
            System.out.println("  " + k + " -> " + ring.getNode(k));

        // 2. LRU Cache
        System.out.println("\n--- LRU Cache ---");
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1); cache.put(2, 2);
        System.out.println("get(1): " + cache.get(1));
        cache.put(3, 3);
        System.out.println("get(2): " + cache.get(2)); // -1 (evicted)

        // 3. Rate Limiter
        System.out.println("\n--- Token Bucket Rate Limiter ---");
        TokenBucket tb = new TokenBucket(5, 2.0);
        for (int i = 1; i <= 7; i++)
            System.out.println("  Request " + i + ": " + (tb.allowRequest() ? "ALLOWED" : "REJECTED"));

        // 4. Trie Autocomplete
        System.out.println("\n--- Trie Autocomplete ---");
        AutoComplete ac = new AutoComplete();
        ac.insert("system design", 50); ac.insert("system call", 30);
        ac.insert("systematic", 20); ac.insert("syntax", 10);
        System.out.println("Top 3 for 'sys': " + ac.suggest("sys", 3));

        // 5. Merkle Tree
        System.out.println("\n--- Merkle Tree ---");
        MerkleTree mt = new MerkleTree(List.of("tx1:A->B:50", "tx2:B->C:30", "tx3:C->D:20", "tx4:D->E:10"));
        System.out.println("Root: " + mt.root().substring(0, 16) + "...");
        var proof = mt.getProof(2);
        System.out.println("Proof valid:  " + MerkleTree.verifyProof("tx3:C->D:20", proof, mt.root()));
        System.out.println("Tampered:     " + MerkleTree.verifyProof("tx3:C->D:99", proof, mt.root()));
    }
}
