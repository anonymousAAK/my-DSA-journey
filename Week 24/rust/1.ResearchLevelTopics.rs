/*
 * WEEK 24 - RUST ADVANCED DSA
 * Topic: Research-Level Topics (Amortized, Skip List, Bloom, Reservoir, Count-Min)
 * File: 1.ResearchLevelTopics.rs
 *
 * CONCEPT:
 *   Same five topics as the Java reference: dynamic-array doubling
 *   demonstrates amortized O(1) push; skip list with geometric promotion;
 *   Bloom filter with two hash functions; reservoir sampling; Count-Min sketch.
 *
 * KEY POINTS:
 *   - We use index-based skip-list nodes stored in a flat Vec<SkipNode>.
 *     This sidesteps Rust's tree-pointer aliasing pain: each node is
 *     identified by a usize index, and forward pointers are indexes.
 *   - rand crate is not part of std; we use a tiny linear-congruential
 *     PRNG (LCG) for portability.
 *
 * ALGORITHM / APPROACH:
 *   DynamicArray.push: double on full; track total copies.
 *   SkipList.insert: collect update[i] indexes top-down; pick random level;
 *                    splice new node at each level.
 *   BloomFilter:    h1(s) and h2(s) bits set on add; both must be set for hit.
 *   Reservoir: keep stream[i] with probability k/(i+1).
 *   CountMin:  table[r][hash_r(x)] increment; estimate = row-wise min.
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - Pointer-based linked structures are awkward in safe Rust; storing
 *     all nodes in a Vec and using `usize` "handles" is the idiomatic
 *     workaround. The classic alternative is `Rc<RefCell<Node>>` for
 *     shared ownership, which we mention but avoid here.
 *   - DefaultHasher gives a fast non-cryptographic hash for Bloom.
 *
 * DRY RUN:
 *   100 pushes into DynamicArray: total_copies = 127 (1+2+...+64),
 *   amortized = 1.27 per op.
 *   Skip list ends sorted: [3,6,7,9,12,17,19,21,25,26].
 *   Bloom on {apple,banana,cherry,date,elderberry}: in-set queries true.
 *
 * COMPLEXITY:
 *   DynamicArray push: amortized O(1).
 *   SkipList op: expected O(log n).
 *   Bloom: O(k) per op.
 *   Reservoir: O(N) total, O(k) memory.
 *   Count-Min: O(d) per op.
 */

use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

// Tiny LCG so the file doesn't depend on the rand crate.
struct Lcg(u64);
impl Lcg {
    fn new(seed: u64) -> Self { Lcg(seed.max(1)) }
    fn next_u64(&mut self) -> u64 {
        self.0 = self.0.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        self.0
    }
    fn next_f64(&mut self) -> f64 {
        (self.next_u64() >> 11) as f64 / (1u64 << 53) as f64
    }
    fn next_range(&mut self, lo: usize, hi_inclusive: usize) -> usize {
        let span = (hi_inclusive - lo + 1) as u64;
        lo + (self.next_u64() % span) as usize
    }
}

// ---------- Dynamic Array (amortized analysis) ----------
pub struct DynamicArray {
    data: Vec<i64>,
    size: usize,
    capacity: usize,
    pub total_copies: u64,
}

impl DynamicArray {
    pub fn new() -> Self { DynamicArray { data: vec![0], size: 0, capacity: 1, total_copies: 0 } }
    pub fn push(&mut self, x: i64) {
        if self.size == self.capacity {
            let mut new_data = vec![0i64; self.capacity * 2];
            for i in 0..self.size { new_data[i] = self.data[i]; self.total_copies += 1; }
            self.data = new_data;
            self.capacity *= 2;
        }
        self.data[self.size] = x;
        self.size += 1;
    }
    pub fn amortized(&self) -> f64 {
        self.total_copies as f64 / self.size.max(1) as f64
    }
}

// ---------- Skip List (index-based; nodes live in a Vec) ----------
const SL_MAX_LEVEL: usize = 16;
const SL_P: f64 = 0.5;
const NIL: usize = usize::MAX;

struct SkipNode {
    val: i64,
    next: [usize; SL_MAX_LEVEL + 1],
}

pub struct SkipList {
    nodes: Vec<SkipNode>,
    head: usize,
    current_level: usize,
    rng: Lcg,
}

impl SkipList {
    pub fn new() -> Self {
        let head_node = SkipNode { val: i64::MIN, next: [NIL; SL_MAX_LEVEL + 1] };
        SkipList { nodes: vec![head_node], head: 0, current_level: 0, rng: Lcg::new(42) }
    }

    fn random_level(&mut self) -> usize {
        let mut lvl = 0;
        while self.rng.next_f64() < SL_P && lvl < SL_MAX_LEVEL { lvl += 1; }
        lvl
    }

    pub fn insert(&mut self, val: i64) {
        let mut update = [NIL; SL_MAX_LEVEL + 1];
        let mut cur = self.head;
        for i in (0..=self.current_level).rev() {
            loop {
                let nxt = self.nodes[cur].next[i];
                if nxt != NIL && self.nodes[nxt].val < val { cur = nxt; }
                else { break; }
            }
            update[i] = cur;
        }
        let lvl = self.random_level();
        if lvl > self.current_level {
            for i in (self.current_level + 1)..=lvl { update[i] = self.head; }
            self.current_level = lvl;
        }
        let new_idx = self.nodes.len();
        let mut new_node = SkipNode { val, next: [NIL; SL_MAX_LEVEL + 1] };
        for i in 0..=lvl {
            new_node.next[i] = self.nodes[update[i]].next[i];
        }
        self.nodes.push(new_node);
        for i in 0..=lvl {
            self.nodes[update[i]].next[i] = new_idx;
        }
    }

    pub fn search(&self, val: i64) -> bool {
        let mut cur = self.head;
        for i in (0..=self.current_level).rev() {
            loop {
                let nxt = self.nodes[cur].next[i];
                if nxt != NIL && self.nodes[nxt].val < val { cur = nxt; }
                else { break; }
            }
        }
        let nxt = self.nodes[cur].next[0];
        nxt != NIL && self.nodes[nxt].val == val
    }

    pub fn to_vec(&self) -> Vec<i64> {
        let mut out = Vec::new();
        let mut cur = self.nodes[self.head].next[0];
        while cur != NIL {
            out.push(self.nodes[cur].val);
            cur = self.nodes[cur].next[0];
        }
        out
    }
}

// ---------- Bloom Filter ----------
pub struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
}

impl BloomFilter {
    pub fn new(size: usize) -> Self { BloomFilter { bits: vec![false; size], size } }
    fn h1(&self, s: &str) -> usize {
        let mut h = DefaultHasher::new(); s.hash(&mut h);
        (h.finish() as usize) % self.size
    }
    fn h2(&self, s: &str) -> usize {
        let mut h = DefaultHasher::new(); s.hash(&mut h);
        let v = h.finish().wrapping_mul(31).wrapping_add(17);
        (v as usize) % self.size
    }
    pub fn add(&mut self, s: &str) { let a = self.h1(s); let b = self.h2(s); self.bits[a] = true; self.bits[b] = true; }
    pub fn might_contain(&self, s: &str) -> bool { self.bits[self.h1(s)] && self.bits[self.h2(s)] }
}

// ---------- Reservoir Sampling ----------
pub fn reservoir_sample(stream: &[i64], k: usize) -> Vec<i64> {
    let mut rng = Lcg::new(42);
    let mut reservoir: Vec<i64> = stream.iter().take(k).copied().collect();
    for i in k..stream.len() {
        let j = rng.next_range(0, i);
        if j < k { reservoir[j] = stream[i]; }
    }
    reservoir
}

// ---------- Count-Min Sketch ----------
pub struct CountMinSketch {
    d: usize,
    w: usize,
    table: Vec<Vec<u32>>,
    seeds: Vec<i64>,
}

impl CountMinSketch {
    pub fn new(d: usize, w: usize) -> Self {
        let mut rng = Lcg::new(42);
        let seeds: Vec<i64> = (0..d).map(|_| rng.next_u64() as i64).collect();
        CountMinSketch { d, w, table: vec![vec![0u32; w]; d], seeds }
    }
    fn idx(&self, x: i64, row: usize) -> usize {
        let h = (x ^ self.seeds[row]) % self.w as i64;
        ((h + self.w as i64) % self.w as i64) as usize
    }
    pub fn add(&mut self, x: i64) {
        for r in 0..self.d { let i = self.idx(x, r); self.table[r][i] += 1; }
    }
    pub fn estimate(&self, x: i64) -> u32 {
        let mut m = u32::MAX;
        for r in 0..self.d { m = m.min(self.table[r][self.idx(x, r)]); }
        m
    }
}

fn main() {
    println!("=== Amortized Analysis: Dynamic Array ===");
    let mut da = DynamicArray::new();
    for i in 0..100 { da.push(i); }
    println!("After 100 pushes: total copies = {}, amortized = {:.2} per op",
             da.total_copies, da.amortized());

    println!("\n=== Skip List ===");
    let mut sl = SkipList::new();
    for x in [3i64, 6, 7, 9, 12, 19, 17, 26, 21, 25] { sl.insert(x); }
    println!("SkipList: {:?}", sl.to_vec());
    println!("search(19): {}", sl.search(19));
    println!("search(15): {}", sl.search(15));

    println!("\n=== Bloom Filter ===");
    let mut bf = BloomFilter::new(1000);
    for w in ["apple","banana","cherry","date","elderberry"] { bf.add(w); }
    println!("'apple' in filter: {}",  bf.might_contain("apple"));
    println!("'cherry' in filter: {}", bf.might_contain("cherry"));
    println!("'mango' in filter: {}",  bf.might_contain("mango"));
    println!("'xyz' in filter: {}",    bf.might_contain("xyz"));

    println!("\n=== Reservoir Sampling ===");
    let stream: Vec<i64> = (1..=20).collect();
    println!("Sample of 5 from stream [1..20]: {:?}", reservoir_sample(&stream, 5));

    println!("\n=== Count-Min Sketch ===");
    let mut cms = CountMinSketch::new(3, 100);
    for &x in &[1,1,1,2,2,3,4,1,2,1,5,1,2,3,3,3i64] { cms.add(x); }
    for v in [1,2,3,5,9i64] {
        println!("Estimated frequency of {}: {}", v, cms.estimate(v));
    }
}
