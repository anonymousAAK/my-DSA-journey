//! # Week 24: Research-Level Algorithms
//!
//! This module covers probabilistic data structures, randomized algorithms,
//! and approximation algorithms for NP-hard problems.
//!
//! ## Complexity Summary
//! | Algorithm               | Time          | Space    | Notes                    |
//! |------------------------|---------------|----------|--------------------------|
//! | Bloom Filter (insert)  | O(k)          | O(m)     | k hash functions, m bits |
//! | Bloom Filter (query)   | O(k)          | O(1)     | False positives possible |
//! | Reservoir Sampling     | O(n)          | O(k)     | k = sample size          |
//! | Count-Min Sketch       | O(d) per op   | O(d * w) | d hash functions, w width|
//! | Vertex Cover 2-approx  | O(V + E)      | O(V)     | At most 2x optimal       |
//! | Greedy Set Cover       | O(n * m)      | O(n)     | O(ln n) approximation    |

use std::collections::{HashMap, HashSet};

// =============================================================================
// Bloom Filter — Probabilistic set membership
// =============================================================================

/// A Bloom filter: a space-efficient probabilistic data structure that can
/// tell you either "possibly in set" or "definitely not in set."
///
/// # How It Works
/// - Uses a bit array of size `m` and `k` independent hash functions.
/// - **Insert**: hash the element with each function, set those k bits.
/// - **Query**: hash the element, check if ALL k bits are set.
///   - If any bit is 0 → definitely NOT in the set.
///   - If all bits are 1 → POSSIBLY in the set (false positive possible).
///
/// # False Positive Rate
/// Approximately `(1 - e^(-kn/m))^k` where n = number of inserted elements.
///
/// # No False Negatives
/// If an element was inserted, all its bits are set → query always returns true.
///
/// # Ownership
/// The `BloomFilter` owns its bit array (`Vec<bool>`). Elements are hashed
/// by value (using `&str`), so no ownership transfer occurs on insert/query.
struct BloomFilter {
    bits: Vec<bool>,
    size: usize,
    num_hashes: usize,
}

impl BloomFilter {
    /// Creates a new Bloom filter with `size` bits and `num_hashes` hash functions.
    fn new(size: usize, num_hashes: usize) -> Self {
        BloomFilter {
            bits: vec![false; size],
            size,
            num_hashes,
        }
    }

    /// Generates `num_hashes` different hash values for the given item.
    ///
    /// Uses the double hashing technique: `h_i(x) = (h1(x) + i * h2(x)) % m`
    /// where h1 and h2 are two independent hash functions.
    /// This is a well-known technique to simulate k hash functions from two.
    fn get_hashes(&self, item: &str) -> Vec<usize> {
        // Simple hash function 1: djb2
        let mut h1: u64 = 5381;
        for byte in item.bytes() {
            h1 = h1.wrapping_mul(33).wrapping_add(byte as u64);
        }

        // Simple hash function 2: sdbm
        let mut h2: u64 = 0;
        for byte in item.bytes() {
            h2 = (byte as u64)
                .wrapping_add(h2.wrapping_shl(6))
                .wrapping_add(h2.wrapping_shl(16))
                .wrapping_sub(h2);
        }

        (0..self.num_hashes)
            .map(|i| {
                let combined = h1.wrapping_add((i as u64).wrapping_mul(h2));
                (combined % self.size as u64) as usize
            })
            .collect()
    }

    /// Inserts an item into the Bloom filter.
    ///
    /// # Complexity
    /// - Time: O(k) where k = number of hash functions
    fn insert(&mut self, item: &str) {
        for idx in self.get_hashes(item) {
            self.bits[idx] = true;
        }
    }

    /// Checks if an item might be in the set.
    ///
    /// Returns `true` if the item is POSSIBLY in the set (may be a false
    /// positive), or `false` if the item is DEFINITELY NOT in the set.
    ///
    /// # Complexity
    /// - Time: O(k)
    fn might_contain(&self, item: &str) -> bool {
        self.get_hashes(item).iter().all(|&idx| self.bits[idx])
    }
}

// =============================================================================
// Reservoir Sampling — Uniform random sample from a stream
// =============================================================================

/// Selects `k` items uniformly at random from a stream of unknown length.
///
/// # Algorithm (Vitter's Algorithm R)
/// 1. Fill the reservoir with the first `k` items.
/// 2. For the i-th item (i >= k), generate a random index `j` in `[0, i]`.
///    If `j < k`, replace `reservoir[j]` with the current item.
///
/// # Proof of Correctness
/// After processing `n` items, each item has probability `k/n` of being in
/// the reservoir. This is proven by induction.
///
/// # Complexity
/// - Time: O(n) — single pass through the stream
/// - Space: O(k) — only the reservoir is stored
///
/// # Note on Randomness
/// Uses a simple linear congruential generator (LCG) for reproducibility
/// in tests. In production, use a proper RNG from the `rand` crate.
fn reservoir_sampling(stream: &[i32], k: usize, seed: u64) -> Vec<i32> {
    let mut reservoir = Vec::with_capacity(k);
    let mut rng_state = seed;

    // Simple LCG for deterministic "random" numbers
    let mut next_random = move || -> u64 {
        rng_state = rng_state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        rng_state
    };

    for (i, &item) in stream.iter().enumerate() {
        if i < k {
            reservoir.push(item);
        } else {
            let j = (next_random() % (i as u64 + 1)) as usize;
            if j < k {
                reservoir[j] = item;
            }
        }
    }

    reservoir
}

// =============================================================================
// Count-Min Sketch — Frequency estimation
// =============================================================================

/// A Count-Min Sketch for approximate frequency counting.
///
/// # How It Works
/// - Uses a 2D array of counters: `d` rows (hash functions) x `w` columns.
/// - **Update(x, delta)**: for each row i, hash x to column h_i(x), add delta.
/// - **Query(x)**: return the MINIMUM count across all d rows for x.
///
/// # Error Bounds
/// - Never underestimates (counts are always >= true frequency).
/// - Overestimates by at most `epsilon * ||a||_1` with probability `1 - delta`,
///   where `w = ceil(e / epsilon)` and `d = ceil(ln(1/delta))`.
///
/// # Complexity
/// - Update: O(d)
/// - Query: O(d)
/// - Space: O(d * w)
struct CountMinSketch {
    table: Vec<Vec<i64>>,
    width: usize,
    depth: usize,
}

impl CountMinSketch {
    /// Creates a new Count-Min Sketch with the given dimensions.
    fn new(width: usize, depth: usize) -> Self {
        CountMinSketch {
            table: vec![vec![0i64; width]; depth],
            width,
            depth,
        }
    }

    /// Hash function for row `i` applied to `item`.
    fn hash(&self, item: &str, row: usize) -> usize {
        let mut h: u64 = (row as u64).wrapping_mul(0x517cc1b727220a95);
        for byte in item.bytes() {
            h = h.wrapping_mul(31).wrapping_add(byte as u64);
        }
        (h % self.width as u64) as usize
    }

    /// Increments the count of `item` by `delta`.
    ///
    /// # Complexity
    /// - Time: O(d) where d = depth (number of hash functions)
    fn update(&mut self, item: &str, delta: i64) {
        for row in 0..self.depth {
            let col = self.hash(item, row);
            self.table[row][col] += delta;
        }
    }

    /// Estimates the frequency of `item`.
    ///
    /// Returns the minimum count across all rows — this is the tightest
    /// upper bound on the true count.
    ///
    /// # Complexity
    /// - Time: O(d)
    fn estimate(&self, item: &str) -> i64 {
        (0..self.depth)
            .map(|row| {
                let col = self.hash(item, row);
                self.table[row][col]
            })
            .min()
            .unwrap_or(0)
    }
}

// =============================================================================
// Vertex Cover 2-Approximation
// =============================================================================

/// Finds an approximate vertex cover using the 2-approximation algorithm.
///
/// # Problem
/// A vertex cover is a set of vertices such that every edge has at least one
/// endpoint in the set. Finding the minimum vertex cover is NP-hard.
///
/// # Algorithm
/// 1. While there are uncovered edges:
///    a. Pick any uncovered edge (u, v).
///    b. Add BOTH u and v to the cover.
///    c. Remove all edges incident to u or v.
///
/// # Approximation Guarantee
/// The result is at most 2x the optimal. Proof: the edges picked form a
/// matching (no two share an endpoint), and the optimal must include at least
/// one endpoint of each matching edge → our solution uses exactly 2 per
/// matching edge → at most 2x optimal.
///
/// # Complexity
/// - Time: O(V + E)
/// - Space: O(V)
fn vertex_cover_2approx(n: usize, edges: &[(usize, usize)]) -> Vec<usize> {
    let mut covered = vec![false; n];
    let mut cover = Vec::new();

    for &(u, v) in edges {
        // If neither endpoint is in the cover, add both
        if !covered[u] && !covered[v] {
            covered[u] = true;
            covered[v] = true;
            cover.push(u);
            cover.push(v);
        }
    }

    cover
}

// =============================================================================
// Greedy Set Cover
// =============================================================================

/// Approximates the minimum set cover using a greedy algorithm.
///
/// # Problem
/// Given a universe U of elements and a collection of subsets S1, S2, ..., Sm,
/// find the minimum number of subsets that cover all elements in U.
/// This is NP-hard.
///
/// # Algorithm
/// Repeatedly pick the subset that covers the most uncovered elements until
/// all elements are covered.
///
/// # Approximation Guarantee
/// The greedy algorithm achieves an O(ln n) approximation ratio, where n = |U|.
/// Specifically, it uses at most H(n) * OPT subsets, where H(n) is the
/// n-th harmonic number.
///
/// # Complexity
/// - Time: O(n * m * max_set_size) in the worst case
/// - Space: O(n) for tracking covered elements
///
/// # Parameters
/// - `universe_size`: number of elements (0-indexed: 0 to universe_size-1)
/// - `sets`: collection of subsets, each as a `Vec<usize>`
///
/// # Returns
/// Indices of the selected subsets.
fn greedy_set_cover(universe_size: usize, sets: &[Vec<usize>]) -> Vec<usize> {
    let mut uncovered: HashSet<usize> = (0..universe_size).collect();
    let mut selected = Vec::new();
    let mut used = vec![false; sets.len()];

    while !uncovered.is_empty() {
        // Find the set that covers the most uncovered elements
        let mut best_idx = None;
        let mut best_count = 0;

        for (i, set) in sets.iter().enumerate() {
            if used[i] {
                continue;
            }
            let count = set.iter().filter(|e| uncovered.contains(e)).count();
            if count > best_count {
                best_count = count;
                best_idx = Some(i);
            }
        }

        match best_idx {
            Some(idx) => {
                used[idx] = true;
                selected.push(idx);
                for &elem in &sets[idx] {
                    uncovered.remove(&elem);
                }
            }
            None => break, // No set can cover remaining elements
        }
    }

    selected
}

// =============================================================================
// Main — Test cases
// =============================================================================

fn main() {
    println!("=== Week 24: Research-Level Algorithms ===\n");

    // --- Bloom Filter ---
    println!("--- Bloom Filter ---");
    let mut bf = BloomFilter::new(1000, 5);

    let words = vec!["apple", "banana", "cherry", "date", "elderberry"];
    for word in &words {
        bf.insert(word);
    }

    // These should all return true (no false negatives)
    for word in &words {
        assert!(bf.might_contain(word), "False negative for '{}'!", word);
        println!("  might_contain(\"{}\") = true", word);
    }

    // These are likely false (but false positives are possible)
    let absent = vec!["fig", "grape", "kiwi", "lemon", "mango"];
    let mut false_positives = 0;
    for word in &absent {
        if bf.might_contain(word) {
            false_positives += 1;
        }
        println!("  might_contain(\"{}\") = {}", word, bf.might_contain(word));
    }
    println!("  False positives: {}/{}", false_positives, absent.len());
    println!("PASS: No false negatives detected\n");

    // --- Reservoir Sampling ---
    println!("--- Reservoir Sampling ---");
    let stream: Vec<i32> = (1..=100).collect();
    let sample = reservoir_sampling(&stream, 5, 42);
    println!("Stream: 1..100, k=5");
    println!("Sample: {:?}", sample);
    assert_eq!(sample.len(), 5);
    // All sampled values should be in the stream range
    for &val in &sample {
        assert!(val >= 1 && val <= 100);
    }

    // Statistical test: run many times and check distribution
    let mut counts = HashMap::new();
    for seed in 0..10000u64 {
        let s = reservoir_sampling(&stream, 1, seed);
        *counts.entry(s[0]).or_insert(0) += 1;
    }
    // Each element should appear roughly 100 times (10000/100)
    // We just verify that we sample from a reasonable range
    println!("  Distinct values sampled (k=1, 10000 trials): {}", counts.len());
    assert!(counts.len() > 50, "Sampling should cover most of the stream");
    println!("PASS\n");

    // --- Count-Min Sketch ---
    println!("--- Count-Min Sketch ---");
    let mut cms = CountMinSketch::new(100, 5);

    // Insert with known frequencies
    for _ in 0..10 { cms.update("apple", 1); }
    for _ in 0..20 { cms.update("banana", 1); }
    for _ in 0..5 { cms.update("cherry", 1); }

    let est_apple = cms.estimate("apple");
    let est_banana = cms.estimate("banana");
    let est_cherry = cms.estimate("cherry");
    let est_absent = cms.estimate("dragonfruit");

    println!("  estimate(\"apple\") = {} (true: 10)", est_apple);
    println!("  estimate(\"banana\") = {} (true: 20)", est_banana);
    println!("  estimate(\"cherry\") = {} (true: 5)", est_cherry);
    println!("  estimate(\"dragonfruit\") = {} (true: 0)", est_absent);

    // Count-Min Sketch never underestimates
    assert!(est_apple >= 10);
    assert!(est_banana >= 20);
    assert!(est_cherry >= 5);
    assert!(est_absent >= 0);
    println!("PASS: No underestimates detected\n");

    // --- Vertex Cover 2-Approximation ---
    println!("--- Vertex Cover (2-Approximation) ---");
    // Triangle graph: 0-1, 1-2, 2-0 (optimal cover = 2 vertices)
    let edges = vec![(0, 1), (1, 2), (2, 0)];
    let cover = vertex_cover_2approx(3, &edges);
    println!("  Graph: triangle (0-1, 1-2, 2-0)");
    println!("  Cover: {:?}", cover);
    // Verify it's a valid cover
    for &(u, v) in &edges {
        assert!(cover.contains(&u) || cover.contains(&v),
            "Edge ({}, {}) not covered!", u, v);
    }
    // 2-approximation: at most 2 * OPT = 2 * 2 = 4
    assert!(cover.len() <= 4);
    println!("  Cover size: {} (optimal: 2, guarantee: <= 4)", cover.len());

    // Star graph: center 0, leaves 1-4
    let star_edges = vec![(0, 1), (0, 2), (0, 3), (0, 4)];
    let star_cover = vertex_cover_2approx(5, &star_edges);
    println!("  Star graph cover: {:?}", star_cover);
    for &(u, v) in &star_edges {
        assert!(star_cover.contains(&u) || star_cover.contains(&v));
    }
    println!("PASS\n");

    // --- Greedy Set Cover ---
    println!("--- Greedy Set Cover ---");
    // Universe: {0, 1, 2, 3, 4}
    // Sets: S0={0,1,2}, S1={2,3}, S2={3,4}, S3={0,2,4}
    let sets = vec![
        vec![0, 1, 2],
        vec![2, 3],
        vec![3, 4],
        vec![0, 2, 4],
    ];
    let selected = greedy_set_cover(5, &sets);
    println!("  Universe: {{0,1,2,3,4}}");
    println!("  Sets: {:?}", sets);
    println!("  Selected set indices: {:?}", selected);

    // Verify all elements are covered
    let mut covered: HashSet<usize> = HashSet::new();
    for &idx in &selected {
        for &elem in &sets[idx] {
            covered.insert(elem);
        }
    }
    for i in 0..5 {
        assert!(covered.contains(&i), "Element {} not covered!", i);
    }
    println!("  All elements covered: true");
    println!("  Number of sets used: {} (optimal: 2)", selected.len());
    println!("PASS\n");

    println!("All Week 24 tests passed!");
}
