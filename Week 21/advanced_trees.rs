//! # Week 21: Advanced Tree Data Structures
//!
//! This module covers three powerful tree-based data structures used for
//! range queries, prefix sums, and string operations.
//!
//! ## Complexity Summary
//! | Structure    | Build   | Query    | Update   | Space |
//! |-------------|---------|----------|----------|-------|
//! | Segment Tree| O(n)    | O(log n) | O(log n) | O(n)  |
//! | Fenwick Tree| O(n)    | O(log n) | O(log n) | O(n)  |
//! | Trie        | —       | O(L)     | O(L)     | O(A*L*n)|
//!
//! Where L = string length, A = alphabet size, n = number of elements/strings.

use std::collections::HashMap;

// =============================================================================
// Segment Tree — Range sum queries with point updates
// =============================================================================

/// A segment tree for range sum queries and point updates.
///
/// # Structure
/// The tree is stored in a flat array of size `4 * n` (to handle all levels).
/// Node `i` covers a range `[lo, hi]` of the original array:
/// - Left child: `2 * i + 1`
/// - Right child: `2 * i + 2`
/// - Leaf nodes store individual elements.
/// - Internal nodes store the sum of their children.
///
/// # Ownership
/// The `SegmentTree` owns both the tree array and the original data size.
/// All operations use `&self` or `&mut self` — no shared mutable state.
struct SegmentTree {
    tree: Vec<i64>,
    n: usize,
}

impl SegmentTree {
    /// Builds a segment tree from the given data.
    ///
    /// # Complexity
    /// - Time: O(n) — each node is computed once
    /// - Space: O(n) — the tree array is at most 4n
    fn build(data: &[i64]) -> Self {
        let n = data.len();
        let mut tree = vec![0i64; 4 * n];
        if n > 0 {
            Self::build_helper(&mut tree, data, 0, 0, n - 1);
        }
        SegmentTree { tree, n }
    }

    fn build_helper(tree: &mut Vec<i64>, data: &[i64], node: usize, lo: usize, hi: usize) {
        if lo == hi {
            tree[node] = data[lo];
            return;
        }
        let mid = lo + (hi - lo) / 2;
        Self::build_helper(tree, data, 2 * node + 1, lo, mid);
        Self::build_helper(tree, data, 2 * node + 2, mid + 1, hi);
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
    }

    /// Queries the sum over range `[ql, qr]` (inclusive).
    ///
    /// # Complexity
    /// - Time: O(log n) — at most 2 nodes per level are partially overlapping
    fn query(&self, ql: usize, qr: usize) -> i64 {
        self.query_helper(0, 0, self.n - 1, ql, qr)
    }

    fn query_helper(&self, node: usize, lo: usize, hi: usize, ql: usize, qr: usize) -> i64 {
        // No overlap
        if qr < lo || hi < ql {
            return 0;
        }
        // Total overlap
        if ql <= lo && hi <= qr {
            return self.tree[node];
        }
        // Partial overlap — recurse on both children
        let mid = lo + (hi - lo) / 2;
        let left = self.query_helper(2 * node + 1, lo, mid, ql, qr);
        let right = self.query_helper(2 * node + 2, mid + 1, hi, ql, qr);
        left + right
    }

    /// Updates the value at index `idx` to `val`.
    ///
    /// # Complexity
    /// - Time: O(log n) — updates one path from leaf to root
    fn update(&mut self, idx: usize, val: i64) {
        self.update_helper(0, 0, self.n - 1, idx, val);
    }

    fn update_helper(&mut self, node: usize, lo: usize, hi: usize, idx: usize, val: i64) {
        if lo == hi {
            self.tree[node] = val;
            return;
        }
        let mid = lo + (hi - lo) / 2;
        if idx <= mid {
            self.update_helper(2 * node + 1, lo, mid, idx, val);
        } else {
            self.update_helper(2 * node + 2, mid + 1, hi, idx, val);
        }
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2];
    }
}

// =============================================================================
// Fenwick Tree (Binary Indexed Tree) — Prefix sums with point updates
// =============================================================================

/// A Fenwick tree (Binary Indexed Tree) for efficient prefix sum queries
/// and point updates.
///
/// # Key Insight
/// Uses the binary representation of indices. Each index `i` is responsible
/// for a range of elements determined by the lowest set bit of `i`.
///
/// - `i & (-i)` gives the lowest set bit (using two's complement).
/// - **Update**: add to index `i`, then `i += i & (-i)` to propagate.
/// - **Query**: sum from 1 to `i`, then `i -= i & (-i)` to traverse.
///
/// # Note
/// Uses 1-based indexing internally for clean bit manipulation.
struct FenwickTree {
    tree: Vec<i64>,
    n: usize,
}

impl FenwickTree {
    /// Creates a Fenwick tree of size `n` initialized to all zeros.
    fn new(n: usize) -> Self {
        FenwickTree {
            tree: vec![0i64; n + 1], // 1-indexed
            n,
        }
    }

    /// Builds a Fenwick tree from initial data.
    ///
    /// # Complexity
    /// - Time: O(n) using the optimized build method
    fn from_data(data: &[i64]) -> Self {
        let n = data.len();
        let mut tree = vec![0i64; n + 1];

        // Copy data to 1-indexed positions
        for i in 0..n {
            tree[i + 1] = data[i];
        }

        // Propagate values to parent nodes
        for i in 1..=n {
            let parent = i + (i & i.wrapping_neg());
            if parent <= n {
                tree[parent] += tree[i];
            }
        }

        FenwickTree { tree, n }
    }

    /// Adds `delta` to the element at position `idx` (0-indexed).
    ///
    /// # Complexity
    /// - Time: O(log n)
    fn update(&mut self, idx: usize, delta: i64) {
        let mut i = idx + 1; // Convert to 1-indexed
        while i <= self.n {
            self.tree[i] += delta;
            i += i & i.wrapping_neg(); // Move to parent
        }
    }

    /// Returns the prefix sum from index 0 to `idx` (inclusive, 0-indexed).
    ///
    /// # Complexity
    /// - Time: O(log n)
    fn prefix_sum(&self, idx: usize) -> i64 {
        let mut sum = 0i64;
        let mut i = idx + 1; // Convert to 1-indexed
        while i > 0 {
            sum += self.tree[i];
            i -= i & i.wrapping_neg(); // Move to responsible ancestor
        }
        sum
    }

    /// Returns the sum over range `[left, right]` (inclusive, 0-indexed).
    ///
    /// # Complexity
    /// - Time: O(log n)
    fn range_sum(&self, left: usize, right: usize) -> i64 {
        if left == 0 {
            self.prefix_sum(right)
        } else {
            self.prefix_sum(right) - self.prefix_sum(left - 1)
        }
    }
}

// =============================================================================
// Trie (Prefix Tree)
// =============================================================================

/// A node in the Trie. Each node stores its children in a `HashMap<char, TrieNode>`.
///
/// # Design Choice
/// Using `HashMap` instead of a fixed-size array allows handling any character
/// set (not just lowercase English). The trade-off is slightly higher overhead
/// per node but better space efficiency for sparse tries.
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_end: bool,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode {
            children: HashMap::new(),
            is_end: false,
        }
    }
}

/// A Trie (prefix tree) for efficient string operations.
///
/// # Operations
/// - `insert`: Add a word to the trie — O(L)
/// - `search`: Check if an exact word exists — O(L)
/// - `starts_with`: Check if any word starts with a prefix — O(L)
///
/// Where L is the length of the word/prefix.
struct Trie {
    root: TrieNode,
}

impl Trie {
    fn new() -> Self {
        Trie {
            root: TrieNode::new(),
        }
    }

    /// Inserts a word into the trie.
    ///
    /// # Complexity
    /// - Time: O(L) where L is the word length
    /// - Space: O(L) in the worst case (all new nodes)
    ///
    /// # Ownership
    /// Uses `entry` API to traverse/create nodes. The `or_insert_with`
    /// pattern lazily creates new `TrieNode`s only when needed.
    fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(TrieNode::new);
        }
        node.is_end = true;
    }

    /// Returns `true` if the exact word is in the trie.
    ///
    /// # Complexity
    /// - Time: O(L)
    fn search(&self, word: &str) -> bool {
        match self.find_node(word) {
            Some(node) => node.is_end,
            None => false,
        }
    }

    /// Returns `true` if any word in the trie starts with the given prefix.
    ///
    /// # Complexity
    /// - Time: O(L) where L is the prefix length
    fn starts_with(&self, prefix: &str) -> bool {
        self.find_node(prefix).is_some()
    }

    /// Helper: traverses the trie following `s` and returns the final node,
    /// or `None` if the path doesn't exist.
    fn find_node(&self, s: &str) -> Option<&TrieNode> {
        let mut node = &self.root;
        for ch in s.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return None,
            }
        }
        Some(node)
    }
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 21: Advanced Trees ===\n");

    // --- Segment Tree ---
    println!("--- Segment Tree ---");
    let data = vec![1, 3, 5, 7, 9, 11];
    let mut st = SegmentTree::build(&data);

    println!("Data: {:?}", data);
    let sum_0_2 = st.query(0, 2);
    println!("Sum [0..2] = {} (expected 9)", sum_0_2);
    assert_eq!(sum_0_2, 9); // 1 + 3 + 5

    let sum_all = st.query(0, 5);
    println!("Sum [0..5] = {} (expected 36)", sum_all);
    assert_eq!(sum_all, 36);

    let sum_3_4 = st.query(3, 4);
    println!("Sum [3..4] = {} (expected 16)", sum_3_4);
    assert_eq!(sum_3_4, 16); // 7 + 9

    // Update index 2 from 5 to 10
    st.update(2, 10);
    let sum_0_2_after = st.query(0, 2);
    println!("After update(2, 10): Sum [0..2] = {} (expected 14)", sum_0_2_after);
    assert_eq!(sum_0_2_after, 14); // 1 + 3 + 10
    println!("PASS\n");

    // --- Fenwick Tree ---
    println!("--- Fenwick Tree ---");
    let data = vec![1i64, 3, 5, 7, 9, 11];
    let mut ft = FenwickTree::from_data(&data);

    println!("Data: {:?}", data);
    let ps3 = ft.prefix_sum(3);
    println!("prefix_sum(3) = {} (expected 16)", ps3);
    assert_eq!(ps3, 16); // 1+3+5+7

    let rs = ft.range_sum(2, 4);
    println!("range_sum(2, 4) = {} (expected 21)", rs);
    assert_eq!(rs, 21); // 5+7+9

    // Add 5 to index 2 (value goes from 5 to 10)
    ft.update(2, 5);
    let ps3_after = ft.prefix_sum(3);
    println!("After update(2, +5): prefix_sum(3) = {} (expected 21)", ps3_after);
    assert_eq!(ps3_after, 21); // 1+3+10+7

    let rs_after = ft.range_sum(0, 5);
    println!("range_sum(0, 5) = {} (expected 41)", rs_after);
    assert_eq!(rs_after, 41); // 1+3+10+7+9+11
    println!("PASS\n");

    // --- Trie ---
    println!("--- Trie ---");
    let mut trie = Trie::new();
    trie.insert("apple");
    trie.insert("app");
    trie.insert("application");
    trie.insert("banana");

    assert!(trie.search("apple"));
    println!("search(\"apple\") = true");

    assert!(trie.search("app"));
    println!("search(\"app\") = true");

    assert!(!trie.search("appl"));
    println!("search(\"appl\") = false (not a complete word)");

    assert!(trie.starts_with("appl"));
    println!("starts_with(\"appl\") = true");

    assert!(trie.starts_with("ban"));
    println!("starts_with(\"ban\") = true");

    assert!(!trie.starts_with("cat"));
    println!("starts_with(\"cat\") = false");

    assert!(!trie.search("banana_split"));
    println!("search(\"banana_split\") = false");
    println!("PASS\n");

    println!("All Week 21 tests passed!");
}
