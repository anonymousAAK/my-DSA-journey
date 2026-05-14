/*
 * =============================================================================
 * Week 21 — Advanced Trees  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. SegmentTree class  (build, range_query, point_update) — sum queries
 *   2. FenwickTree / BIT  (update, prefix_sum, range_sum)
 *   3. Trie class         (insert, search, starts_with)
 *
 * Complexity cheat-sheet
 * ----------------------
 *   SegmentTree::build          O(n)
 *   SegmentTree::range_query    O(log n)
 *   SegmentTree::point_update   O(log n)
 *   SegmentTree  space          O(4n)
 *
 *   FenwickTree::update         O(log n)
 *   FenwickTree::prefix_sum     O(log n)
 *   FenwickTree::range_sum      O(log n)
 *   FenwickTree  space          O(n)
 *
 *   Trie::insert                O(L)   L = word length
 *   Trie::search                O(L)
 *   Trie::starts_with           O(L)
 *   Trie  space                 O(total characters * ALPHA)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o advanced_trees advanced_trees.cpp && ./advanced_trees
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <memory>
#include <cassert>
#include <sstream>
#include <numeric>

// ---------------------------------------------------------------------------
// 1. Segment Tree — range sum queries + point updates
// ---------------------------------------------------------------------------
class SegmentTree {
public:
    // Build from an array — O(n).
    explicit SegmentTree(const std::vector<int>& data)
        : n_(static_cast<int>(data.size())), tree_(4 * data.size(), 0)
    {
        if (n_ > 0) build(data, 1, 0, n_ - 1);
    }

    // Range sum query [l, r] inclusive — O(log n).
    [[nodiscard]] long long range_query(int l, int r) const {
        return query(1, 0, n_ - 1, l, r);
    }

    // Point update: arr[idx] += delta — O(log n).
    void point_update(int idx, int delta) {
        update(1, 0, n_ - 1, idx, delta);
    }

    [[nodiscard]] int size() const { return n_; }

private:
    int n_;
    std::vector<long long> tree_;

    void build(const std::vector<int>& data, int node, int start, int end) {
        if (start == end) {
            tree_[node] = data[start];
            return;
        }
        int mid = (start + end) / 2;
        build(data, 2 * node, start, mid);
        build(data, 2 * node + 1, mid + 1, end);
        tree_[node] = tree_[2 * node] + tree_[2 * node + 1];
    }

    long long query(int node, int start, int end, int l, int r) const {
        if (r < start || end < l) return 0;          // no overlap
        if (l <= start && end <= r) return tree_[node]; // total overlap
        int mid = (start + end) / 2;
        return query(2 * node, start, mid, l, r)
             + query(2 * node + 1, mid + 1, end, l, r);
    }

    void update(int node, int start, int end, int idx, int delta) {
        if (start == end) {
            tree_[node] += delta;
            return;
        }
        int mid = (start + end) / 2;
        if (idx <= mid) update(2 * node, start, mid, idx, delta);
        else            update(2 * node + 1, mid + 1, end, idx, delta);
        tree_[node] = tree_[2 * node] + tree_[2 * node + 1];
    }
};

// ---------------------------------------------------------------------------
// 2. Fenwick Tree (Binary Indexed Tree) — 1-indexed
// ---------------------------------------------------------------------------
class FenwickTree {
public:
    explicit FenwickTree(int n) : n_(n), tree_(n + 1, 0) {}

    // Construct from data — O(n log n) simple version.
    explicit FenwickTree(const std::vector<int>& data)
        : n_(static_cast<int>(data.size())), tree_(data.size() + 1, 0)
    {
        for (int i = 0; i < n_; ++i) update(i + 1, data[i]);
    }

    // Add delta to index i (1-indexed) — O(log n).
    void update(int i, int delta) {
        for (; i <= n_; i += i & (-i))
            tree_[i] += delta;
    }

    // Prefix sum [1..i] — O(log n).
    [[nodiscard]] long long prefix_sum(int i) const {
        long long s = 0;
        for (int x = i; x > 0; x -= x & (-x))
            s += tree_[x];
        return s;
    }

    // Range sum [l..r] (1-indexed) — O(log n).
    [[nodiscard]] long long range_sum(int l, int r) const {
        return prefix_sum(r) - prefix_sum(l - 1);
    }

private:
    int n_;
    std::vector<long long> tree_;
};

// ---------------------------------------------------------------------------
// 3. Trie — prefix tree for lowercase English letters
// ---------------------------------------------------------------------------
class Trie {
public:
    Trie() : root_(std::make_unique<Node>()) {}

    // Insert a word — O(L).
    void insert(const std::string& word) {
        Node* cur = root_.get();
        for (char ch : word) {
            int idx = ch - 'a';
            if (!cur->children[idx]) {
                cur->children[idx] = std::make_unique<Node>();
            }
            cur = cur->children[idx].get();
        }
        cur->is_end = true;
    }

    // Search for exact word — O(L).
    [[nodiscard]] bool search(const std::string& word) const {
        const Node* node = find_node(word);
        return node != nullptr && node->is_end;
    }

    // Check if any word starts with prefix — O(L).
    [[nodiscard]] bool starts_with(const std::string& prefix) const {
        return find_node(prefix) != nullptr;
    }

private:
    static constexpr int ALPHA = 26;

    struct Node {
        std::unique_ptr<Node> children[ALPHA]{};
        bool is_end = false;
    };

    std::unique_ptr<Node> root_;

    [[nodiscard]] const Node* find_node(const std::string& prefix) const {
        const Node* cur = root_.get();
        for (char ch : prefix) {
            int idx = ch - 'a';
            if (!cur->children[idx]) return nullptr;
            cur = cur->children[idx].get();
        }
        return cur;
    }
};

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 21: Advanced Trees ===\n\n";

    // ---- 1. Segment Tree ----
    {
        std::cout << "-- Segment Tree --\n";
        std::vector<int> data = {1, 3, 5, 7, 9, 11};
        SegmentTree st(data);

        // Sum of [1..3] = 3+5+7 = 15
        auto q1 = st.range_query(1, 3);
        assert(q1 == 15);
        std::cout << "  sum[1..3] = " << q1 << "\n";

        // Sum of [0..5] = 1+3+5+7+9+11 = 36
        auto q2 = st.range_query(0, 5);
        assert(q2 == 36);
        std::cout << "  sum[0..5] = " << q2 << "\n";

        // Update index 3: 7 += 3 => 10
        st.point_update(3, 3);
        auto q3 = st.range_query(1, 3);
        assert(q3 == 18);
        std::cout << "  after update(3, +3): sum[1..3] = " << q3 << "\n\n";
    }

    // ---- 2. Fenwick Tree ----
    {
        std::cout << "-- Fenwick Tree (BIT) --\n";
        std::vector<int> data = {1, 3, 5, 7, 9, 11};
        FenwickTree ft(data);

        // prefix_sum(4) = 1+3+5+7 = 16 (1-indexed)
        auto p4 = ft.prefix_sum(4);
        assert(p4 == 16);
        std::cout << "  prefix_sum(4) = " << p4 << "\n";

        // range_sum(2, 5) = 3+5+7+9 = 24
        auto r = ft.range_sum(2, 5);
        assert(r == 24);
        std::cout << "  range_sum(2,5) = " << r << "\n";

        // Update index 3 (1-indexed): add 10
        ft.update(3, 10);
        auto p4_after = ft.prefix_sum(4);
        assert(p4_after == 26);
        std::cout << "  after update(3, +10): prefix_sum(4) = " << p4_after << "\n\n";
    }

    // ---- 3. Trie ----
    {
        std::cout << "-- Trie --\n";
        Trie trie;
        trie.insert("apple");
        trie.insert("app");
        trie.insert("application");
        trie.insert("bat");

        assert(trie.search("apple"));
        assert(trie.search("app"));
        assert(!trie.search("ap"));
        assert(trie.starts_with("ap"));
        assert(trie.starts_with("app"));
        assert(!trie.starts_with("baz"));
        assert(trie.search("bat"));

        std::cout << "  search(\"apple\")     = true\n";
        std::cout << "  search(\"app\")       = true\n";
        std::cout << "  search(\"ap\")        = false\n";
        std::cout << "  starts_with(\"ap\")   = true\n";
        std::cout << "  starts_with(\"baz\")  = false\n";
    }

    std::cout << "\nAll Week 21 tests passed.\n";
    return 0;
}
