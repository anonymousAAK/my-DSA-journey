/*
 * WEEK 21 - ADVANCED TREES
 * Topic: Segment Tree & Binary Indexed Tree (Fenwick Tree)
 *
 * =========================================
 * SEGMENT TREE
 * =========================================
 * Efficiently handle RANGE QUERIES and POINT UPDATES on an array.
 *
 * Examples:
 * - Range sum query: sum(l, r)
 * - Range min/max query: min(l, r)
 * - Point update: set arr[i] = val
 *
 * STRUCTURE: Binary tree where:
 * - Leaf nodes = array elements
 * - Internal nodes = aggregate (sum/min/max) of children
 * - Tree stored in array: node i has children 2i+1 and 2i+2
 *
 * Build: O(n)
 * Query: O(log n)
 * Update: O(log n)
 * Space: O(4n)
 *
 * =========================================
 * BINARY INDEXED TREE (BIT / FENWICK TREE)
 * =========================================
 * Simpler structure for prefix sum queries and point updates.
 * Uses clever bit manipulation: each index stores sum of a range.
 * Trick: a node at index i stores sum of i's last set bit count of elements.
 *
 * Update: O(log n)
 * Prefix sum query: O(log n)
 * Range sum [l,r]: prefixSum(r) - prefixSum(l-1)  O(log n)
 * Space: O(n)
 *
 * BIT is simpler to implement than Segment Tree for sum queries,
 * but Segment Tree is more general (handles min/max, range updates, etc.)
 */

public class SegmentTreeAndBIT {

    // =====================
    // SEGMENT TREE (for sum queries)
    // =====================
    static class SegmentTree {
        int[] tree;
        int n;

        SegmentTree(int[] arr) {
            n = arr.length;
            tree = new int[4 * n];
            build(arr, 0, 0, n - 1);
        }

        void build(int[] arr, int node, int start, int end) {
            if (start == end) {
                tree[node] = arr[start];
                return;
            }
            int mid = (start + end) / 2;
            build(arr, 2*node+1, start, mid);
            build(arr, 2*node+2, mid+1, end);
            tree[node] = tree[2*node+1] + tree[2*node+2];
        }

        // Point update: set arr[idx] = val
        void update(int node, int start, int end, int idx, int val) {
            if (start == end) { tree[node] = val; return; }
            int mid = (start + end) / 2;
            if (idx <= mid) update(2*node+1, start, mid, idx, val);
            else update(2*node+2, mid+1, end, idx, val);
            tree[node] = tree[2*node+1] + tree[2*node+2];
        }
        void update(int idx, int val) { update(0, 0, n-1, idx, val); }

        // Range sum query [l, r]
        int query(int node, int start, int end, int l, int r) {
            if (r < start || end < l) return 0; // no overlap
            if (l <= start && end <= r) return tree[node]; // full overlap
            // partial overlap
            int mid = (start + end) / 2;
            return query(2*node+1, start, mid, l, r)
                 + query(2*node+2, mid+1, end, l, r);
        }
        int query(int l, int r) { return query(0, 0, n-1, l, r); }
    }

    // =====================
    // BINARY INDEXED TREE (Fenwick Tree)
    // =====================
    static class BIT {
        int[] bit;
        int n;

        BIT(int n) { this.n = n; bit = new int[n + 1]; } // 1-indexed

        BIT(int[] arr) {
            n = arr.length;
            bit = new int[n + 1];
            for (int i = 0; i < n; i++) update(i + 1, arr[i]); // 1-indexed
        }

        // Add delta to index i (1-indexed)
        void update(int i, int delta) {
            for (; i <= n; i += i & (-i)) bit[i] += delta; // add last set bit
        }

        // Prefix sum [1..i]
        int prefixSum(int i) {
            int sum = 0;
            for (; i > 0; i -= i & (-i)) sum += bit[i]; // remove last set bit
            return sum;
        }

        // Range sum [l, r] (1-indexed)
        int rangeSum(int l, int r) { return prefixSum(r) - prefixSum(l - 1); }

        // Point update: set arr[i] to new value (need old value)
        void pointSet(int i, int oldVal, int newVal) { update(i, newVal - oldVal); }
    }

    public static void main(String[] args) {
        int[] arr = {1, 3, 5, 7, 9, 11};
        System.out.println("Array: {1, 3, 5, 7, 9, 11}");

        // Segment Tree
        System.out.println("\n=== Segment Tree ===");
        SegmentTree st = new SegmentTree(arr);
        System.out.println("sum(0,5) = " + st.query(0, 5)); // 36
        System.out.println("sum(1,3) = " + st.query(1, 3)); // 15
        System.out.println("sum(2,4) = " + st.query(2, 4)); // 21

        st.update(3, 10); // arr[3] = 10 (was 7)
        System.out.println("\nAfter update arr[3]=10:");
        System.out.println("sum(0,5) = " + st.query(0, 5)); // 39
        System.out.println("sum(1,3) = " + st.query(1, 3)); // 18

        // BIT
        System.out.println("\n=== Binary Indexed Tree (Fenwick Tree) ===");
        BIT bit = new BIT(arr);
        System.out.println("prefixSum(4) = " + bit.prefixSum(4)); // 1+3+5+7 = 16
        System.out.println("rangeSum(2,5) = " + bit.rangeSum(2, 5)); // 3+5+7+9 = 24
        System.out.println("rangeSum(1,6) = " + bit.rangeSum(1, 6)); // 36

        bit.update(4, 3); // add 3 to index 4 (arr[3] becomes 7+3=10)
        System.out.println("\nAfter adding 3 to index 4:");
        System.out.println("prefixSum(6) = " + bit.prefixSum(6)); // 39
        System.out.println("rangeSum(3,5) = " + bit.rangeSum(3, 5)); // 5+10+9 = 24
    }
}
