// Week 29: System Design - LRU Cache, Consistent Hashing, Rate Limiter, Trie, Merkle Tree

import java.util.*;
import java.security.MessageDigest;

public class system_design {

    // === LRU Cache ===
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

    // === Trie Autocomplete ===
    static class TrieNode { Map<Character,TrieNode> children = new HashMap<>(); boolean isEnd; int freq; }
    static class AutoComplete {
        TrieNode root = new TrieNode();
        void insert(String word) {
            TrieNode n = root;
            for (char c : word.toCharArray()) { n.children.putIfAbsent(c, new TrieNode()); n = n.children.get(c); }
            n.isEnd = true; n.freq++;
        }
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

    public static void main(String[] args) {
        LRUCache cache = new LRUCache(2);
        cache.put(1, 1); cache.put(2, 2);
        System.out.println("LRU get(1): " + cache.get(1));
        cache.put(3, 3);
        System.out.println("LRU get(2): " + cache.get(2)); // -1

        AutoComplete ac = new AutoComplete();
        for (String w : new String[]{"cat","car","card","care"}) ac.insert(w);
        System.out.println("Autocomplete 'car': " + ac.suggest("car", 3));
    }
}
