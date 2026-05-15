// WEEK 29 - RUST ADVANCED TOPICS
// Topic: Sharding Strategies
// File: sharding.rs
//
// CONCEPT:
//   Partition data across N nodes. Three approaches:
//     - Range: ordered key intervals per shard.
//     - Hash:  shard = hash(key) mod N.
//     - Directory: explicit map of key -> shard.
//
// KEY POINTS:
//   - Range supports range scans but risks hot ranges.
//   - Hash distributes uniformly but breaks locality.
//   - Directory is flexible at the cost of a metadata hop.
//
// ALGORITHM / APPROACH:
//   RANGE:    binary search (slice::partition_point) over sorted boundaries.
//   HASH:     DefaultHasher; hash(key) % N.
//   DIRECTORY: HashMap<String, usize>.
//
// RUST-SPECIFIC NOTES:
//   - `partition_point` is the Rust idiom for upper_bound.
//   - DefaultHasher is fine for demos; use SipHash with a fixed key (or
//     SHA-2 from RustCrypto) for cross-process stability.
//
// DRY RUN / EXAMPLE:
//   range bounds ["c","m","t"]: "apple"->0, "cat"->1, "mango"->2, "tiger"->3.
//
// COMPLEXITY:
//   Range O(log shards); Hash O(L); Dir O(1).

use std::collections::HashMap;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

pub struct RangeShardRouter { b: Vec<String> }

impl RangeShardRouter {
    pub fn new(mut b: Vec<String>) -> Self { b.sort(); Self { b } }
    pub fn route(&self, key: &str) -> usize {
        self.b.partition_point(|x| x.as_str() <= key)
    }
}

pub struct HashShardRouter { n: usize }
impl HashShardRouter {
    pub fn new(n: usize) -> Self { Self { n } }
    pub fn route(&self, key: &str) -> usize {
        let mut h = DefaultHasher::new();
        key.hash(&mut h);
        (h.finish() as usize) % self.n
    }
}

pub struct DirectoryShardRouter { map: HashMap<String, usize> }
impl DirectoryShardRouter {
    pub fn new() -> Self { Self { map: HashMap::new() } }
    pub fn assign(&mut self, k: &str, s: usize) { self.map.insert(k.to_string(), s); }
    pub fn route(&self, k: &str) -> isize {
        self.map.get(k).map(|&x| x as isize).unwrap_or(-1)
    }
}

fn main() {
    let rng = RangeShardRouter::new(vec!["c".to_string(), "m".to_string(), "t".to_string()]);
    for k in ["apple", "banana", "cat", "mango", "tiger"] {
        println!("range {} -> shard {}", k, rng.route(k));
    }
    let hsh = HashShardRouter::new(4);
    for k in ["user:42", "user:43", "order:99", "session:xyz"] {
        println!("hash  {} -> shard {}", k, hsh.route(k));
    }
    let mut dr = DirectoryShardRouter::new();
    dr.assign("hot-customer:Acme", 0);
    dr.assign("hot-customer:Globex", 1);
    println!("dir   hot-customer:Acme -> shard {}", dr.route("hot-customer:Acme"));
}

// NOTES
// -----
// Differences from Java:
//   * slice::partition_point replaces Java's Collections.binarySearch.
//   * Rust's DefaultHasher is salted differently on each process; for
//     cross-process stability use SipHash with a fixed key or SHA-2.
