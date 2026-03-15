/*
 * =============================================================================
 * Week 24 — Research-Level Topics  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. Bloom Filter           (using std::bitset, multiple hash functions)
 *   2. Reservoir Sampling     (Algorithm R — uniform sample of k items)
 *   3. Count-Min Sketch       (frequency estimation with sub-linear space)
 *   4. Vertex Cover 2-Approx  (greedy edge-picking)
 *   5. Greedy Set Cover       (O(log n)-approximation)
 *
 * Complexity cheat-sheet
 * ----------------------
 *   Bloom Filter
 *     insert       O(k) per item, k = number of hash functions
 *     query        O(k)
 *     false positive rate  ~ (1 - e^(-kn/m))^k
 *     Space        O(m) bits
 *
 *   Reservoir Sampling
 *     Time         O(n)          |  Space O(k)
 *
 *   Count-Min Sketch
 *     update       O(d) per item, d = number of hash functions (rows)
 *     query        O(d)
 *     Space        O(d * w)
 *
 *   Vertex Cover 2-Approx
 *     Time         O(V + E)      |  Space O(V)
 *     Approximation ratio: 2
 *
 *   Greedy Set Cover
 *     Time         O(|U| * |S|)  |  Space O(|U| + |S|)
 *     Approximation ratio: O(ln n)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o research_level research_level.cpp && ./research_level
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <bitset>
#include <string>
#include <random>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <unordered_set>
#include <numeric>
#include <functional>
#include <climits>

// ---------------------------------------------------------------------------
// Helper
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// 1. Bloom Filter — probabilistic set membership
// ---------------------------------------------------------------------------
// Uses std::bitset<M> with K independent hash functions.
// False positives possible; false negatives impossible.
// Complexity:  insert/query O(K)  |  Space O(M) bits
template <std::size_t M = 1024, int K = 3>
class BloomFilter {
public:
    BloomFilter() {
        bits_.reset();
        // Initialize K hash seeds.
        std::mt19937 gen(42);
        for (int i = 0; i < K; ++i) seeds_[i] = gen();
    }

    void insert(const std::string& item) {
        for (int i = 0; i < K; ++i) {
            bits_.set(hash(item, i) % M);
        }
    }

    // Returns true if item *might* be in the set; false if definitely not.
    [[nodiscard]] bool possibly_contains(const std::string& item) const {
        for (int i = 0; i < K; ++i) {
            if (!bits_.test(hash(item, i) % M)) return false;
        }
        return true;
    }

    [[nodiscard]] std::size_t bit_count() const { return bits_.count(); }

private:
    std::bitset<M> bits_;
    std::size_t seeds_[K]{};

    // Simple hash combining std::hash with a seed.
    [[nodiscard]] std::size_t hash(const std::string& item, int idx) const {
        std::size_t h = std::hash<std::string>{}(item);
        // Combine with seed for independence.
        h ^= seeds_[idx] + 0x9e3779b9 + (h << 6) + (h >> 2);
        return h;
    }
};

// ---------------------------------------------------------------------------
// 2. Reservoir Sampling — Algorithm R
// ---------------------------------------------------------------------------
// Select k items uniformly at random from a stream of unknown length.
// Complexity:  Time O(n)  |  Space O(k)
template <typename T>
std::vector<T> reservoir_sampling(const std::vector<T>& stream, int k,
                                  unsigned seed = 12345) {
    std::mt19937 gen(seed);
    std::vector<T> reservoir;

    for (int i = 0; i < static_cast<int>(stream.size()); ++i) {
        if (i < k) {
            reservoir.push_back(stream[i]);
        } else {
            // Replace element j with probability k/(i+1).
            std::uniform_int_distribution<int> dist(0, i);
            int j = dist(gen);
            if (j < k) {
                reservoir[j] = stream[i];
            }
        }
    }
    return reservoir;
}

// ---------------------------------------------------------------------------
// 3. Count-Min Sketch — frequency estimation
// ---------------------------------------------------------------------------
// A probabilistic data structure for estimating element frequencies.
// Overestimates are possible; underestimates are not.
// Complexity:  update/query O(D)  |  Space O(D * W)
class CountMinSketch {
public:
    // D = number of hash functions (depth), W = number of counters per row (width)
    CountMinSketch(int d, int w) : d_(d), w_(w), table_(d, std::vector<int>(w, 0)) {
        std::mt19937 gen(42);
        seeds_.resize(d);
        for (int i = 0; i < d; ++i) seeds_[i] = gen();
    }

    void update(const std::string& item, int count = 1) {
        for (int i = 0; i < d_; ++i) {
            int idx = hash(item, i);
            table_[i][idx] += count;
        }
    }

    // Returns estimated frequency (always >= true frequency).
    [[nodiscard]] int query(const std::string& item) const {
        int min_val = INT_MAX;
        for (int i = 0; i < d_; ++i) {
            int idx = hash(item, i);
            min_val = std::min(min_val, table_[i][idx]);
        }
        return min_val;
    }

private:
    int d_, w_;
    std::vector<std::vector<int>> table_;
    std::vector<std::size_t> seeds_;

    [[nodiscard]] int hash(const std::string& item, int row) const {
        std::size_t h = std::hash<std::string>{}(item);
        h ^= seeds_[row] + 0x9e3779b9 + (h << 6) + (h >> 2);
        return static_cast<int>(h % w_);
    }
};

// ---------------------------------------------------------------------------
// 4. Vertex Cover — 2-Approximation
// ---------------------------------------------------------------------------
// Greedy: repeatedly pick an uncovered edge and add both endpoints.
// Guarantees a cover at most 2x the optimal.
// Complexity:  Time O(V + E)  |  Space O(V)
std::vector<int> vertex_cover_2approx(int n, const std::vector<std::pair<int,int>>& edges) {
    std::vector<bool> in_cover(n, false);
    std::vector<int> cover;

    for (auto [u, v] : edges) {
        if (!in_cover[u] && !in_cover[v]) {
            in_cover[u] = true;
            in_cover[v] = true;
            cover.push_back(u);
            cover.push_back(v);
        }
    }
    return cover;
}

// ---------------------------------------------------------------------------
// 5. Greedy Set Cover
// ---------------------------------------------------------------------------
// Given a universe U and a collection of subsets S1..Sm, find a minimum
// collection of subsets that covers U.  NP-hard; greedy achieves O(ln n).
// Complexity:  Time O(|U| * |S|)  |  Space O(|U| + |S|)
std::vector<int> greedy_set_cover(int universe_size,
                                  const std::vector<std::vector<int>>& sets) {
    std::unordered_set<int> uncovered;
    for (int i = 0; i < universe_size; ++i) uncovered.insert(i);

    std::vector<bool> used(sets.size(), false);
    std::vector<int> chosen;

    while (!uncovered.empty()) {
        // Pick the set that covers the most uncovered elements.
        int best_idx = -1;
        int best_count = 0;

        for (int i = 0; i < static_cast<int>(sets.size()); ++i) {
            if (used[i]) continue;
            int count = 0;
            for (int elem : sets[i]) {
                if (uncovered.count(elem)) ++count;
            }
            if (count > best_count) {
                best_count = count;
                best_idx = i;
            }
        }

        if (best_idx == -1) break;  // can't cover remaining elements

        used[best_idx] = true;
        chosen.push_back(best_idx);
        for (int elem : sets[best_idx]) {
            uncovered.erase(elem);
        }
    }
    return chosen;
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 24: Research-Level Topics ===\n\n";

    // 1. Bloom Filter
    {
        std::cout << "-- Bloom Filter --\n";
        BloomFilter<2048, 5> bf;
        bf.insert("apple");
        bf.insert("banana");
        bf.insert("cherry");

        assert(bf.possibly_contains("apple"));
        assert(bf.possibly_contains("banana"));
        assert(bf.possibly_contains("cherry"));
        // "mango" was never inserted — should very likely be false.
        // (Bloom filters can have false positives, but with 2048 bits and
        // only 3 items, the probability is negligible.)
        bool fp = bf.possibly_contains("mango");
        std::cout << "  contains(\"apple\"):  true\n";
        std::cout << "  contains(\"banana\"): true\n";
        std::cout << "  contains(\"mango\"): " << std::boolalpha << fp
                  << " (expected false)\n";
        std::cout << "  bits set: " << bf.bit_count() << " / 2048\n\n";
    }

    // 2. Reservoir Sampling
    {
        std::cout << "-- Reservoir Sampling --\n";
        std::vector<int> stream(100);
        std::iota(stream.begin(), stream.end(), 0);  // 0..99

        int k = 5;
        auto sample = reservoir_sampling(stream, k);
        assert(static_cast<int>(sample.size()) == k);
        std::cout << "  stream: 0..99,  k=" << k << "\n";
        std::cout << "  sample: " << vec_str(sample) << "\n";

        // Verify uniform distribution over many trials.
        std::vector<int> freq(100, 0);
        for (int trial = 0; trial < 10000; ++trial) {
            auto s = reservoir_sampling(stream, k, trial);
            for (int x : s) ++freq[x];
        }
        // Each element should appear ~500 times (10000 * 5/100).
        int min_f = *std::min_element(freq.begin(), freq.end());
        int max_f = *std::max_element(freq.begin(), freq.end());
        std::cout << "  10000 trials: min_freq=" << min_f << " max_freq=" << max_f
                  << " (expected ~500)\n\n";
    }

    // 3. Count-Min Sketch
    {
        std::cout << "-- Count-Min Sketch --\n";
        CountMinSketch cms(5, 100);  // 5 hash functions, width 100

        cms.update("apple", 10);
        cms.update("banana", 5);
        cms.update("cherry", 3);
        cms.update("apple", 5);

        int qa = cms.query("apple");
        int qb = cms.query("banana");
        int qc = cms.query("cherry");
        int qd = cms.query("dragonfruit");

        std::cout << "  apple:       " << qa << " (true: 15)\n";
        std::cout << "  banana:      " << qb << " (true: 5)\n";
        std::cout << "  cherry:      " << qc << " (true: 3)\n";
        std::cout << "  dragonfruit: " << qd << " (true: 0)\n";
        // CMS never underestimates.
        assert(qa >= 15);
        assert(qb >= 5);
        assert(qc >= 3);
        assert(qd >= 0);
        std::cout << "\n";
    }

    // 4. Vertex Cover 2-Approximation
    {
        std::cout << "-- Vertex Cover (2-Approximation) --\n";
        // Graph:  0-1, 1-2, 2-3, 3-4, 0-3
        std::vector<std::pair<int,int>> edges = {{0,1}, {1,2}, {2,3}, {3,4}, {0,3}};
        auto cover = vertex_cover_2approx(5, edges);
        std::cout << "  edges: [(0,1),(1,2),(2,3),(3,4),(0,3)]\n";
        std::cout << "  cover: " << vec_str(cover) << "  size=" << cover.size() << "\n";

        // Verify: every edge has at least one endpoint in the cover.
        std::unordered_set<int> cover_set(cover.begin(), cover.end());
        for (auto [u, v] : edges) {
            assert(cover_set.count(u) || cover_set.count(v));
        }
        // Optimal vertex cover has size 2 (e.g., {1, 3}), so 2-approx <= 4.
        assert(cover.size() <= 4);
        std::cout << "  all edges covered (verified)\n\n";
    }

    // 5. Greedy Set Cover
    {
        std::cout << "-- Greedy Set Cover --\n";
        // Universe: {0, 1, 2, 3, 4}
        // Sets:
        //   S0 = {0, 1, 2}
        //   S1 = {2, 3}
        //   S2 = {3, 4}
        //   S3 = {0, 2, 4}
        std::vector<std::vector<int>> sets = {
            {0, 1, 2},
            {2, 3},
            {3, 4},
            {0, 2, 4}
        };
        auto chosen = greedy_set_cover(5, sets);
        std::cout << "  universe: {0,1,2,3,4}\n";
        std::cout << "  chosen sets: " << vec_str(chosen) << "\n";

        // Verify coverage.
        std::unordered_set<int> covered;
        for (int idx : chosen) {
            for (int elem : sets[idx]) covered.insert(elem);
        }
        for (int i = 0; i < 5; ++i) assert(covered.count(i));
        std::cout << "  all elements covered (verified)\n";
        std::cout << "  sets used: " << chosen.size()
                  << " (optimal: 2, e.g. S0+S2)\n";
    }

    std::cout << "\nAll Week 24 tests passed.\n";
    return 0;
}
