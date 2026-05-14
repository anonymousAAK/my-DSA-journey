/*
 * WEEK 24 - C++ ADVANCED DSA
 * Topic: Research-Level Topics (Amortized, Skip List, Bloom Filter,
 *        Reservoir Sampling, Count-Min Sketch)
 * File: 1.ResearchLevelTopics.cpp
 *
 * CONCEPT:
 *   Five techniques for advanced data-structure problems:
 *     1. Amortized analysis: dynamic-array doubling has O(1) amortized push.
 *     2. Skip List: probabilistic sorted list, expected O(log n) ops.
 *     3. Bloom filter: probabilistic set, no false negatives.
 *     4. Reservoir sampling: uniform k-sample from a stream of unknown size.
 *     5. Count-Min sketch: approximate frequency counts.
 *
 * KEY POINTS:
 *   - Geometric promotion in skip lists keeps expected height O(log n).
 *   - Bloom filter: more bits / hashes -> lower false-positive rate.
 *   - Reservoir step: keep stream[i] with probability k/(i+1).
 *   - Count-Min: estimate(x) = min over rows of table[r][hash_r(x)].
 *
 * ALGORITHM / APPROACH:
 *   See file headers in Java reference; identical operations.
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - std::mt19937 with a fixed seed for reproducibility.
 *   - std::vector<bool> for Bloom bitset (compact).
 *   - std::hash<std::string> as a quick hash; combine with seed via XOR.
 *
 * DRY RUN:
 *   DynamicArray push 100 times: total copies = 1+2+4+...+64 = 127, amortized 1.27.
 *   Bloom on {apple,banana,cherry,date,elderberry}: in-set queries true;
 *   out-of-set queries usually false.
 *
 * COMPLEXITY:
 *   DynamicArray push amortized O(1).
 *   SkipList expected O(log n) per op.
 *   Bloom O(k) per op, O(m) memory.
 *   Reservoir O(N) total, O(k) memory.
 *   Count-Min O(d) per op, O(d*w) memory.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <random>
#include <string>
#include <climits>

struct DynamicArray {
    std::vector<int> data{0};
    int size = 0, capacity = 1;
    long long total_copies = 0;

    void push(int x) {
        if (size == capacity) {
            std::vector<int> newData(capacity * 2);
            for (int i = 0; i < size; ++i) { newData[i] = data[i]; total_copies++; }
            data = std::move(newData);
            capacity *= 2;
        }
        data[size++] = x;
    }

    double amortized() const { return (double)total_copies / std::max(size, 1); }
};

struct SkipList {
    static constexpr int MAX_LEVEL = 16;
    static constexpr double P = 0.5;

    struct Node {
        int val;
        std::vector<Node*> next;
        Node(int v, int level) : val(v), next(level + 1, nullptr) {}
    };

    Node* head = new Node(INT_MIN, MAX_LEVEL);
    int currentLevel = 0;
    std::mt19937 rng{42};
    std::uniform_real_distribution<double> uni{0.0, 1.0};

    int randomLevel() {
        int level = 0;
        while (uni(rng) < P && level < MAX_LEVEL) level++;
        return level;
    }

    void insert(int val) {
        std::vector<Node*> update(MAX_LEVEL + 1, nullptr);
        Node* cur = head;
        for (int i = currentLevel; i >= 0; --i) {
            while (cur->next[i] && cur->next[i]->val < val) cur = cur->next[i];
            update[i] = cur;
        }
        int level = randomLevel();
        if (level > currentLevel) {
            for (int i = currentLevel + 1; i <= level; ++i) update[i] = head;
            currentLevel = level;
        }
        Node* n = new Node(val, level);
        for (int i = 0; i <= level; ++i) {
            n->next[i] = update[i]->next[i];
            update[i]->next[i] = n;
        }
    }

    bool search(int val) const {
        Node* cur = head;
        for (int i = currentLevel; i >= 0; --i)
            while (cur->next[i] && cur->next[i]->val < val) cur = cur->next[i];
        return cur->next[0] && cur->next[0]->val == val;
    }

    void print_level0() const {
        Node* cur = head->next[0];
        std::cout << "SkipList: ";
        while (cur) { std::cout << cur->val << " "; cur = cur->next[0]; }
        std::cout << "\n";
    }
};

struct BloomFilter {
    std::vector<bool> bits;
    int size;
    BloomFilter(int sz) : bits(sz, false), size(sz) {}
    int h1(const std::string& s) const { return (int)(std::hash<std::string>{}(s) % size); }
    int h2(const std::string& s) const { return (int)((std::hash<std::string>{}(s) * 31u + 17u) % size); }
    void add(const std::string& s) { bits[h1(s)] = true; bits[h2(s)] = true; }
    bool might_contain(const std::string& s) const { return bits[h1(s)] && bits[h2(s)]; }
};

std::vector<int> reservoir_sample(const std::vector<int>& stream, int k) {
    std::mt19937 rng(42);
    std::vector<int> reservoir(stream.begin(), stream.begin() + std::min<int>(k, (int)stream.size()));
    for (int i = k; i < (int)stream.size(); ++i) {
        std::uniform_int_distribution<int> dist(0, i);
        int j = dist(rng);
        if (j < k) reservoir[j] = stream[i];
    }
    return reservoir;
}

struct CountMinSketch {
    int d, w;
    std::vector<std::vector<int>> table;
    std::vector<int> seeds;

    CountMinSketch(int d_, int w_) : d(d_), w(w_), table(d_, std::vector<int>(w_, 0)), seeds(d_) {
        std::mt19937 rng(42);
        for (int i = 0; i < d; ++i) seeds[i] = (int)rng();
    }

    int idx(int x, int row) const {
        int h = (x ^ seeds[row]) % w;
        if (h < 0) h += w;
        return h;
    }

    void add(int x) { for (int r = 0; r < d; ++r) table[r][idx(x, r)]++; }

    int estimate(int x) const {
        int m = INT_MAX;
        for (int r = 0; r < d; ++r) m = std::min(m, table[r][idx(x, r)]);
        return m;
    }
};

int main() {
    std::cout << "=== Amortized Analysis: Dynamic Array ===\n";
    DynamicArray da;
    for (int i = 0; i < 100; ++i) da.push(i);
    std::cout << "After 100 pushes: total copies = " << da.total_copies
              << ", amortized = " << da.amortized() << " per op\n";

    std::cout << "\n=== Skip List ===\n";
    SkipList sl;
    for (int x : {3, 6, 7, 9, 12, 19, 17, 26, 21, 25}) sl.insert(x);
    sl.print_level0();
    std::cout << std::boolalpha;
    std::cout << "search(19): " << sl.search(19) << "\n";
    std::cout << "search(15): " << sl.search(15) << "\n";

    std::cout << "\n=== Bloom Filter ===\n";
    BloomFilter bf(1000);
    for (auto& w : std::vector<std::string>{"apple","banana","cherry","date","elderberry"}) bf.add(w);
    std::cout << "'apple' in filter: "  << bf.might_contain("apple")  << "\n";
    std::cout << "'cherry' in filter: " << bf.might_contain("cherry") << "\n";
    std::cout << "'mango' in filter: "  << bf.might_contain("mango")  << "\n";
    std::cout << "'xyz' in filter: "    << bf.might_contain("xyz")    << "\n";

    std::cout << "\n=== Reservoir Sampling ===\n";
    std::vector<int> stream;
    for (int i = 1; i <= 20; ++i) stream.push_back(i);
    auto sample = reservoir_sample(stream, 5);
    std::cout << "Sample of 5 from stream [1..20]: ";
    for (int v : sample) std::cout << v << " ";
    std::cout << "\n";

    std::cout << "\n=== Count-Min Sketch ===\n";
    CountMinSketch cms(3, 100);
    std::vector<int> data = {1,1,1,2,2,3,4,1,2,1,5,1,2,3,3,3};
    for (int x : data) cms.add(x);
    for (int v : {1,2,3,5,9})
        std::cout << "Estimated frequency of " << v << ": " << cms.estimate(v) << "\n";
    return 0;
}
