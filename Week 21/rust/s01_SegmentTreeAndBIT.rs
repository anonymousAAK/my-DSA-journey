/*
 * WEEK 21 - RUST ADVANCED DSA
 * Topic: Segment Tree & Binary Indexed Tree (Fenwick Tree)
 * File: 1.SegmentTreeAndBIT.rs
 *
 * CONCEPT:
 *   Segment Tree: array-of-intervals tree giving O(log n) range queries
 *   and O(log n) point updates. Binary Indexed Tree (BIT / Fenwick):
 *   compact, 1-indexed array using i & -i for an implicit tree, supporting
 *   O(log n) prefix sum and updates.
 *
 * KEY POINTS:
 *   - Segment tree allocated as 4*n; children at 2k+1 and 2k+2.
 *   - BIT is 1-indexed; (i as i64 & -(i as i64)) computes lowest set bit.
 *   - BIT range_sum(l,r) = prefix(r) - prefix(l-1).
 *
 * ALGORITHM / APPROACH:
 *   Segment tree:
 *     build / update / query are recursive on (node, lo, hi).
 *   BIT:
 *     update(i, delta): while i<=n: bit[i] += delta; i += lowbit(i)
 *     prefix(i):        while i>0:  s   += bit[i]; i -= lowbit(i)
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - All fields are private by default; expose via methods.
 *   - Recursive helpers must thread &mut self carefully — borrow checker
 *     forbids holding two &mut into the same Vec, so we use index math.
 *   - Use `i32` for parity with Java; for production use generics with
 *     traits like `Add` / `Default`.
 *   - Lowbit on signed integer: `(i as i64) & -(i as i64)` then cast back.
 *   - `usize` for array indices; conversions between i32/usize are explicit.
 *
 * DRY RUN:
 *   arr = [1,3,5,7,9,11].
 *   SegmentTree.query(1,3) -> 15 (3+5+7).
 *   After update(3,10): query(0,5) -> 39, query(1,3) -> 18.
 *   BIT.prefix_sum(4) -> 16; range_sum(2,5) -> 24.
 *
 * COMPLEXITY:
 *   Segment Tree: build O(n); query/update O(log n); space O(4n).
 *   BIT:          build O(n log n); query/update O(log n); space O(n).
 */

pub struct SegmentTree {
    n: usize,
    tree: Vec<i64>,
}

impl SegmentTree {
    pub fn new(arr: &[i64]) -> Self {
        let n = arr.len();
        let cap = 4 * n.max(1);
        let mut st = SegmentTree { n, tree: vec![0; cap] };
        if n > 0 {
            st.build(arr, 0, 0, n - 1);
        }
        st
    }

    fn build(&mut self, a: &[i64], node: usize, lo: usize, hi: usize) {
        if lo == hi {
            self.tree[node] = a[lo];
            return;
        }
        let mid = (lo + hi) / 2;
        self.build(a, 2*node + 1, lo, mid);
        self.build(a, 2*node + 2, mid + 1, hi);
        self.tree[node] = self.tree[2*node + 1] + self.tree[2*node + 2];
    }

    pub fn update(&mut self, idx: usize, val: i64) {
        let n = self.n;
        self.update_rec(0, 0, n - 1, idx, val);
    }

    fn update_rec(&mut self, node: usize, lo: usize, hi: usize, idx: usize, val: i64) {
        if lo == hi { self.tree[node] = val; return; }
        let mid = (lo + hi) / 2;
        if idx <= mid { self.update_rec(2*node + 1, lo, mid, idx, val); }
        else          { self.update_rec(2*node + 2, mid + 1, hi, idx, val); }
        self.tree[node] = self.tree[2*node + 1] + self.tree[2*node + 2];
    }

    pub fn query(&self, l: usize, r: usize) -> i64 {
        self.query_rec(0, 0, self.n - 1, l, r)
    }

    fn query_rec(&self, node: usize, lo: usize, hi: usize, l: usize, r: usize) -> i64 {
        if r < lo || hi < l { return 0; }
        if l <= lo && hi <= r { return self.tree[node]; }
        let mid = (lo + hi) / 2;
        self.query_rec(2*node + 1, lo, mid, l, r)
        + self.query_rec(2*node + 2, mid + 1, hi, l, r)
    }
}

pub struct Bit {
    n: usize,
    bit: Vec<i64>,
}

impl Bit {
    pub fn with_size(n: usize) -> Self { Bit { n, bit: vec![0; n + 1] } }

    pub fn from_slice(arr: &[i64]) -> Self {
        let mut b = Bit::with_size(arr.len());
        for (i, &v) in arr.iter().enumerate() { b.update(i + 1, v); }
        b
    }

    fn lowbit(i: usize) -> usize {
        let s = i as i64;
        (s & -s) as usize
    }

    pub fn update(&mut self, mut i: usize, delta: i64) {
        while i <= self.n {
            self.bit[i] += delta;
            i += Bit::lowbit(i);
        }
    }

    pub fn prefix_sum(&self, mut i: usize) -> i64 {
        let mut s = 0i64;
        while i > 0 {
            s += self.bit[i];
            i -= Bit::lowbit(i);
        }
        s
    }

    pub fn range_sum(&self, l: usize, r: usize) -> i64 {
        self.prefix_sum(r) - self.prefix_sum(l - 1)
    }
}

fn main() {
    let arr: Vec<i64> = vec![1, 3, 5, 7, 9, 11];
    println!("Array: {:?}", arr);

    println!("\n=== Segment Tree ===");
    let mut st = SegmentTree::new(&arr);
    println!("sum(0,5) = {}", st.query(0, 5)); // 36
    println!("sum(1,3) = {}", st.query(1, 3)); // 15
    println!("sum(2,4) = {}", st.query(2, 4)); // 21

    st.update(3, 10);
    println!("\nAfter update arr[3]=10:");
    println!("sum(0,5) = {}", st.query(0, 5)); // 39
    println!("sum(1,3) = {}", st.query(1, 3)); // 18

    println!("\n=== Binary Indexed Tree (Fenwick Tree) ===");
    let mut b = Bit::from_slice(&arr);
    println!("prefix_sum(4)  = {}", b.prefix_sum(4));      // 16
    println!("range_sum(2,5) = {}", b.range_sum(2, 5));    // 24
    println!("range_sum(1,6) = {}", b.range_sum(1, 6));    // 36

    b.update(4, 3);
    println!("\nAfter adding 3 to index 4:");
    println!("prefix_sum(6)  = {}", b.prefix_sum(6));      // 39
    println!("range_sum(3,5) = {}", b.range_sum(3, 5));    // 24
}
