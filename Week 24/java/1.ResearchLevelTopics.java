/*
 * WEEK 24 - RESEARCH-LEVEL TOPICS
 * Topic: Amortized Analysis, Randomized Algorithms, Advanced Data Structures
 *
 * This week introduces concepts at the boundary of competitive programming
 * and theoretical computer science research.
 *
 * =========================================
 * 1. AMORTIZED ANALYSIS
 * =========================================
 * Analyze average cost per operation over a SEQUENCE of operations,
 * even when individual operations may be expensive.
 *
 * Methods:
 * - Aggregate method: total cost / n operations
 * - Accounting method: prepay for future expensive operations
 * - Potential method: Φ(state) represents "stored energy"
 *
 * Classic example: Dynamic array (ArrayList) doubling
 * Each individual push: O(1) or O(n) for resize.
 * Amortized per push: O(1) — because resize happens rarely.
 *
 * =========================================
 * 2. SKIP LIST
 * =========================================
 * Probabilistic data structure: sorted linked list with express lanes.
 * Each element is promoted to higher levels with probability p (typically 1/2).
 *
 * Expected O(log n) for search, insert, delete.
 * Simpler to implement than balanced BSTs (AVL, Red-Black).
 * Used in: Redis sorted sets, LevelDB, ConcurrentSkipListMap (Java).
 *
 * =========================================
 * 3. BLOOM FILTER
 * =========================================
 * Space-efficient probabilistic set data structure.
 * Supports: add(x), mightContain(x)
 * - False positives possible: might say "yes" when element is not in set.
 * - No false negatives: if "no", element is definitely not in set.
 *
 * Multiple hash functions → multiple bit positions set.
 * Used in: databases (avoid disk lookups), web crawlers, spell checkers.
 *
 * =========================================
 * 4. RESERVOIR SAMPLING
 * =========================================
 * Randomly sample k items from a stream of unknown size N.
 * Each item ends up in the sample with equal probability k/N.
 * Time: O(N), Space: O(k) — single pass through stream!
 *
 * =========================================
 * 5. COUNT-MIN SKETCH
 * =========================================
 * Approximate frequency counting for a stream.
 * Uses d hash functions × w counters.
 * Space: O(d*w) instead of O(distinct_elements).
 * Error bound: with probability 1-δ, estimate is within ε*n of true frequency.
 */

import java.util.*;

public class ResearchLevelTopics {

    // =====================
    // AMORTIZED ANALYSIS: Dynamic Array (simplified)
    // =====================
    static class DynamicArray {
        int[] data = new int[1];
        int size = 0, capacity = 1;
        long totalCopies = 0; // track total copy operations for amortized analysis

        void push(int x) {
            if (size == capacity) {
                int[] newData = new int[capacity * 2];
                for (int i = 0; i < size; i++) { newData[i] = data[i]; totalCopies++; }
                data = newData;
                capacity *= 2;
            }
            data[size++] = x;
        }

        double amortizedCostPerOp() { return (double) totalCopies / size; }
    }

    // =====================
    // SKIP LIST (simplified demonstration)
    // =====================
    static class SkipList {
        static final int MAX_LEVEL = 16;
        static final double P = 0.5;
        Random rand = new Random(42);

        static class Node {
            int val;
            Node[] next;
            Node(int val, int level) { this.val = val; next = new Node[level + 1]; }
        }

        Node head = new Node(Integer.MIN_VALUE, MAX_LEVEL);
        int currentLevel = 0;

        int randomLevel() {
            int level = 0;
            while (rand.nextDouble() < P && level < MAX_LEVEL) level++;
            return level;
        }

        void insert(int val) {
            Node[] update = new Node[MAX_LEVEL + 1];
            Node curr = head;
            for (int i = currentLevel; i >= 0; i--) {
                while (curr.next[i] != null && curr.next[i].val < val) curr = curr.next[i];
                update[i] = curr;
            }
            int level = randomLevel();
            if (level > currentLevel) {
                for (int i = currentLevel + 1; i <= level; i++) update[i] = head;
                currentLevel = level;
            }
            Node newNode = new Node(val, level);
            for (int i = 0; i <= level; i++) { newNode.next[i] = update[i].next[i]; update[i].next[i] = newNode; }
        }

        boolean search(int val) {
            Node curr = head;
            for (int i = currentLevel; i >= 0; i--)
                while (curr.next[i] != null && curr.next[i].val < val) curr = curr.next[i];
            return curr.next[0] != null && curr.next[0].val == val;
        }

        void printLevel0() {
            Node curr = head.next[0];
            System.out.print("SkipList: ");
            while (curr != null) { System.out.print(curr.val + " "); curr = curr.next[0]; }
            System.out.println();
        }
    }

    // =====================
    // BLOOM FILTER (simplified: 2 hash functions)
    // =====================
    static class BloomFilter {
        boolean[] bits;
        int size;

        BloomFilter(int size) { this.size = size; bits = new boolean[size]; }

        int hash1(String s) { return Math.abs(s.hashCode()) % size; }
        int hash2(String s) { return Math.abs(s.hashCode() * 31 + 17) % size; }

        void add(String s) { bits[hash1(s)] = true; bits[hash2(s)] = true; }

        boolean mightContain(String s) { return bits[hash1(s)] && bits[hash2(s)]; }
    }

    // =====================
    // RESERVOIR SAMPLING — sample k items from stream
    // =====================
    static int[] reservoirSample(int[] stream, int k) {
        Random rand = new Random(42);
        int[] reservoir = Arrays.copyOf(stream, k);
        for (int i = k; i < stream.length; i++) {
            int j = rand.nextInt(i + 1); // random index in [0, i]
            if (j < k) reservoir[j] = stream[i]; // replace with probability k/(i+1)
        }
        return reservoir;
    }

    // =====================
    // COUNT-MIN SKETCH (d=3 hash functions, w=100 counters each)
    // =====================
    static class CountMinSketch {
        int[][] table;
        int d, w;
        int[] seeds;

        CountMinSketch(int d, int w) {
            this.d = d; this.w = w;
            table = new int[d][w];
            seeds = new int[d];
            Random r = new Random(42);
            for (int i = 0; i < d; i++) seeds[i] = r.nextInt();
        }

        void add(int x) {
            for (int i = 0; i < d; i++) table[i][Math.abs((x ^ seeds[i]) % w)]++;
        }

        int estimate(int x) {
            int min = Integer.MAX_VALUE;
            for (int i = 0; i < d; i++) min = Math.min(min, table[i][Math.abs((x ^ seeds[i]) % w)]);
            return min;
        }
    }

    public static void main(String[] args) {
        // Amortized Analysis
        System.out.println("=== Amortized Analysis: Dynamic Array ===");
        DynamicArray da = new DynamicArray();
        for (int i = 0; i < 100; i++) da.push(i);
        System.out.printf("After 100 pushes: total copies = %d, amortized = %.2f per op%n",
            da.totalCopies, da.amortizedCostPerOp());
        // Amortized ≈ 1.0 copies per push, proving O(1) amortized

        // Skip List
        System.out.println("\n=== Skip List ===");
        SkipList sl = new SkipList();
        for (int x : new int[]{3, 6, 7, 9, 12, 19, 17, 26, 21, 25}) sl.insert(x);
        sl.printLevel0();
        System.out.println("search(19): " + sl.search(19)); // true
        System.out.println("search(15): " + sl.search(15)); // false

        // Bloom Filter
        System.out.println("\n=== Bloom Filter ===");
        BloomFilter bf = new BloomFilter(1000);
        String[] words = {"apple", "banana", "cherry", "date", "elderberry"};
        for (String w : words) bf.add(w);
        System.out.println("'apple' in filter: " + bf.mightContain("apple"));     // true
        System.out.println("'cherry' in filter: " + bf.mightContain("cherry"));   // true
        System.out.println("'mango' in filter: " + bf.mightContain("mango"));     // probably false
        System.out.println("'xyz' in filter: " + bf.mightContain("xyz"));         // probably false

        // Reservoir Sampling
        System.out.println("\n=== Reservoir Sampling ===");
        int[] stream = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
        int[] sample = reservoirSample(stream, 5);
        System.out.println("Sample of 5 from stream [1..20]: " + Arrays.toString(sample));

        // Count-Min Sketch
        System.out.println("\n=== Count-Min Sketch ===");
        CountMinSketch cms = new CountMinSketch(3, 100);
        int[] data = {1,1,1,2,2,3,4,1,2,1,5,1,2,3,3,3};
        for (int x : data) cms.add(x);
        System.out.println("Estimated frequency of 1: " + cms.estimate(1)); // ≈ 6
        System.out.println("Estimated frequency of 2: " + cms.estimate(2)); // ≈ 4
        System.out.println("Estimated frequency of 3: " + cms.estimate(3)); // ≈ 4
        System.out.println("Estimated frequency of 5: " + cms.estimate(5)); // ≈ 1
        System.out.println("Estimated frequency of 9: " + cms.estimate(9)); // ≈ 0 (not added)
    }
}
