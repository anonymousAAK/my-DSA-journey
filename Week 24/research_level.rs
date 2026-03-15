//! WEEK 24 — Rust: Research-Level Topics
//! Bloom filter, reservoir sampling, count-min sketch, approximation algorithms.

use std::collections::{HashMap, HashSet};

// === BLOOM FILTER ===
struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
    num_hashes: usize,
}

impl BloomFilter {
    fn new(size: usize, num_hashes: usize) -> Self {
        BloomFilter { bits: vec![false; size], size, num_hashes }
    }

    fn hash(&self, item: &str, seed: usize) -> usize {
        let mut h: u64 = seed as u64;
        for b in item.bytes() {
            h = h.wrapping_mul(31).wrapping_add(b as u64);
        }
        (h as usize) % self.size
    }

    fn add(&mut self, item: &str) {
        for i in 0..self.num_hashes {
            let pos = self.hash(item, i * 1000 + 7);
            self.bits[pos] = true;
        }
    }

    fn might_contain(&self, item: &str) -> bool {
        (0..self.num_hashes).all(|i| self.bits[self.hash(item, i * 1000 + 7)])
    }
}

// === RESERVOIR SAMPLING ===
/// Sample k items uniformly from a stream. Time: O(n), Space: O(k).
fn reservoir_sample(stream: &[i32], k: usize) -> Vec<i32> {
    let mut reservoir: Vec<i32> = stream[..k].to_vec();
    let mut rng_state: u64 = 42; // simple LCG for deterministic demo
    for i in k..stream.len() {
        // Simple PRNG
        rng_state = rng_state.wrapping_mul(6364136223846793005).wrapping_add(1);
        let j = (rng_state >> 33) as usize % (i + 1);
        if j < k {
            reservoir[j] = stream[i];
        }
    }
    reservoir
}

// === COUNT-MIN SKETCH ===
struct CountMinSketch {
    table: Vec<Vec<i32>>,
    d: usize,
    w: usize,
    seeds: Vec<u64>,
}

impl CountMinSketch {
    fn new(d: usize, w: usize) -> Self {
        let seeds: Vec<u64> = (0..d).map(|i| (i as u64 + 1) * 2654435761).collect();
        CountMinSketch { table: vec![vec![0; w]; d], d, w, seeds }
    }

    fn hash_fn(&self, x: i32, seed: u64) -> usize {
        ((x as u64).wrapping_mul(seed).wrapping_add(seed >> 3)) as usize % self.w
    }

    fn add(&mut self, x: i32) {
        for i in 0..self.d {
            let pos = self.hash_fn(x, self.seeds[i]);
            self.table[i][pos] += 1;
        }
    }

    fn estimate(&self, x: i32) -> i32 {
        (0..self.d)
            .map(|i| self.table[i][self.hash_fn(x, self.seeds[i])])
            .min()
            .unwrap_or(0)
    }
}

// === VERTEX COVER (2-approximation) ===
fn vertex_cover_2approx(v: usize, edges: &[(usize, usize)]) -> HashSet<usize> {
    let mut covered = vec![false; v];
    let mut cover = HashSet::new();
    for &(u, w) in edges {
        if !covered[u] && !covered[w] {
            covered[u] = true;
            covered[w] = true;
            cover.insert(u);
            cover.insert(w);
        }
    }
    cover
}

// === GREEDY SET COVER ===
fn greedy_set_cover(universe_size: usize, sets: &[HashSet<usize>]) -> Vec<usize> {
    let mut uncovered: HashSet<usize> = (0..universe_size).collect();
    let mut chosen = Vec::new();
    while !uncovered.is_empty() {
        let best_idx = (0..sets.len())
            .max_by_key(|&i| sets[i].intersection(&uncovered).count())
            .unwrap();
        if sets[best_idx].intersection(&uncovered).count() == 0 { break; }
        chosen.push(best_idx);
        for &x in &sets[best_idx] { uncovered.remove(&x); }
    }
    chosen
}

fn main() {
    // Bloom Filter
    println!("=== Bloom Filter ===");
    let mut bf = BloomFilter::new(1000, 3);
    for w in &["apple", "banana", "cherry", "date"] { bf.add(w); }
    for test in &["apple", "cherry", "mango", "xyz"] {
        println!("  '{}': {}", test, bf.might_contain(test));
    }

    // Reservoir Sampling
    println!("\n=== Reservoir Sampling ===");
    let stream: Vec<i32> = (1..=100).collect();
    let sample = reservoir_sample(&stream, 5);
    println!("  5 from [1..100]: {:?}", sample);

    // Count-Min Sketch
    println!("\n=== Count-Min Sketch ===");
    let mut cms = CountMinSketch::new(3, 100);
    for &x in &[1,1,1,2,2,3,4,1,2,1,5,1,2,3,3,3] { cms.add(x); }
    for x in [1, 2, 3, 5, 9] {
        println!("  freq({}) ≈ {}", x, cms.estimate(x));
    }

    // Vertex Cover
    println!("\n=== Vertex Cover (2-approx) ===");
    let edges = vec![(0,1), (0,2), (1,3), (2,3), (3,4)];
    let cover = vertex_cover_2approx(5, &edges);
    println!("  Cover: {:?}, size: {}", cover, cover.len());

    // Set Cover
    println!("\n=== Greedy Set Cover ===");
    let sets: Vec<HashSet<usize>> = vec![
        [0,1,2].iter().cloned().collect(),
        [3,4,5].iter().cloned().collect(),
        [4,5,6,7].iter().cloned().collect(),
        [0,3,8].iter().cloned().collect(),
        [2,7,9].iter().cloned().collect(),
    ];
    let chosen = greedy_set_cover(10, &sets);
    println!("  Chosen sets: {:?}", chosen);
}
