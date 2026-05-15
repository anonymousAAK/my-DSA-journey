/*
 * WEEK 21 - C++ ADVANCED DSA
 * Topic: Segment Tree & Binary Indexed Tree (Fenwick Tree)
 * File: 1.SegmentTreeAndBIT.cpp
 *
 * CONCEPT:
 *   Segment Tree: a binary tree of intervals supporting O(log n) range
 *   queries (sum/min/max/...) and O(log n) point updates over an array.
 *   BIT (Fenwick Tree): an implicit tree stored in a flat array using
 *   the i & -i trick to support O(log n) prefix-sum queries and updates.
 *
 * KEY POINTS:
 *   - Segment tree allocated as `4 * n` to safely cover any tree shape.
 *   - Children: 2*node+1 (left), 2*node+2 (right).
 *   - BIT is 1-indexed; "lowest set bit" (i & -i) walks the implicit tree.
 *   - BIT range [l, r] = prefix(r) - prefix(l-1).
 *
 * ALGORITHM / APPROACH:
 *   Segment tree (sum):
 *     build / update / query are recursive; combine via sum.
 *   BIT:
 *     update(i, delta):  while i<=n: bit[i]+=delta; i += i & -i
 *     prefix(i):         while i>0:  s += bit[i]; i -= i & -i
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - Use `struct` (public-by-default) for terse data-structure types.
 *   - `std::vector<int>` replaces Java arrays; size set at construction.
 *   - INT_MAX / 2 sentinel avoids overflow when added.
 *   - No need for "@SuppressWarnings"; templates would generalise the
 *     aggregator but we keep it concrete for clarity.
 *
 * DRY RUN:
 *   arr = {1,3,5,7,9,11}
 *   SegmentTree.query(1,3):
 *     splits across mid=2; left subtree returns 3+5=8 from [1..2],
 *     right subtree returns 7 from [3..3] -> total 15.
 *   BIT.prefix(4) = bit[4] = 1+3+5+7 = 16.
 *   BIT.range_sum(2,5) = prefix(5) - prefix(1) = 25 - 1 = 24.
 *
 * COMPLEXITY:
 *   Segment Tree: build O(n), query/update O(log n), space O(4n).
 *   BIT:          build O(n log n), query/update O(log n), space O(n).
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <climits>

struct SegmentTree {
    int n;
    std::vector<int> tree;

    SegmentTree(const std::vector<int>& arr) : n((int)arr.size()), tree(4 * std::max(n, 1), 0) {
        if (n) build(arr, 0, 0, n - 1);
    }

    void build(const std::vector<int>& a, int node, int lo, int hi) {
        if (lo == hi) { tree[node] = a[lo]; return; }
        int mid = (lo + hi) / 2;
        build(a, 2*node + 1, lo, mid);
        build(a, 2*node + 2, mid + 1, hi);
        tree[node] = tree[2*node + 1] + tree[2*node + 2];
    }

    void update(int idx, int val) { update(0, 0, n - 1, idx, val); }
    void update(int node, int lo, int hi, int idx, int val) {
        if (lo == hi) { tree[node] = val; return; }
        int mid = (lo + hi) / 2;
        if (idx <= mid) update(2*node + 1, lo, mid, idx, val);
        else            update(2*node + 2, mid + 1, hi, idx, val);
        tree[node] = tree[2*node + 1] + tree[2*node + 2];
    }

    int query(int l, int r) const { return query(0, 0, n - 1, l, r); }
    int query(int node, int lo, int hi, int l, int r) const {
        if (r < lo || hi < l) return 0;             // disjoint
        if (l <= lo && hi <= r) return tree[node];  // fully inside
        int mid = (lo + hi) / 2;
        return query(2*node + 1, lo, mid, l, r)
             + query(2*node + 2, mid + 1, hi, l, r);
    }
};

struct BIT {
    int n;
    std::vector<int> bit;

    explicit BIT(int n_) : n(n_), bit(n_ + 1, 0) {}
    explicit BIT(const std::vector<int>& arr) : n((int)arr.size()), bit(arr.size() + 1, 0) {
        for (int i = 0; i < n; ++i) update(i + 1, arr[i]);
    }

    void update(int i, int delta) {
        for (; i <= n; i += i & -i) bit[i] += delta;
    }

    int prefix_sum(int i) const {
        int s = 0;
        for (; i > 0; i -= i & -i) s += bit[i];
        return s;
    }

    int range_sum(int l, int r) const { return prefix_sum(r) - prefix_sum(l - 1); }

    void point_set(int i, int oldVal, int newVal) { update(i, newVal - oldVal); }
};

int main() {
    std::vector<int> arr = {1, 3, 5, 7, 9, 11};
    std::cout << "Array: {1, 3, 5, 7, 9, 11}\n";

    std::cout << "\n=== Segment Tree ===\n";
    SegmentTree st(arr);
    std::cout << "sum(0,5) = " << st.query(0, 5) << "\n";  // 36
    std::cout << "sum(1,3) = " << st.query(1, 3) << "\n";  // 15
    std::cout << "sum(2,4) = " << st.query(2, 4) << "\n";  // 21

    st.update(3, 10);
    std::cout << "\nAfter update arr[3]=10:\n";
    std::cout << "sum(0,5) = " << st.query(0, 5) << "\n";  // 39
    std::cout << "sum(1,3) = " << st.query(1, 3) << "\n";  // 18

    std::cout << "\n=== Binary Indexed Tree (Fenwick Tree) ===\n";
    BIT bit(arr);
    std::cout << "prefix_sum(4)  = " << bit.prefix_sum(4)  << "\n";  // 16
    std::cout << "range_sum(2,5) = " << bit.range_sum(2,5) << "\n";  // 24
    std::cout << "range_sum(1,6) = " << bit.range_sum(1,6) << "\n";  // 36

    bit.update(4, 3);
    std::cout << "\nAfter adding 3 to index 4:\n";
    std::cout << "prefix_sum(6)  = " << bit.prefix_sum(6)  << "\n";  // 39
    std::cout << "range_sum(3,5) = " << bit.range_sum(3,5) << "\n";  // 24

    return 0;
}
