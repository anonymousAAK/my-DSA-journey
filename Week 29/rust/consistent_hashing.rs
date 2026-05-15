// WEEK 29 - RUST ADVANCED TOPICS
// Topic: Consistent Hashing with Virtual Nodes
// File: consistent_hashing.rs
//
// CONCEPT:
//   Map nodes and keys onto a hash ring 0..u64::MAX; each key belongs to
//   the next node clockwise. Virtual nodes per physical node balance load
//   and keep rebalancing localised. Adding or removing a node displaces
//   only ~1/N of keys.
//
// KEY POINTS:
//   - BTreeMap<u64, String> gives O(log(NV)) lookup via range().
//   - Used by Cassandra, DynamoDB, memcached clients, etc.
//   - 100-200 virtual nodes per server is typical.
//
// ALGORITHM / APPROACH:
//   add(node):    for i in 0..V: ring[hash(node + "#VN" + i)] = node
//   remove(node): remove those keys
//   get(key):     first key in ring >= hash(key); wrap to first if at end
//
// RUST-SPECIFIC NOTES:
//   - BTreeMap::range(h..) gives the "ceiling" iterator we need.
//   - DefaultHasher is OK for demos; for stable cross-process hashing use
//     a fixed-seed SipHasher or SHA-256.
//
// DRY RUN / EXAMPLE:
//   Add A, B, C with V=150 -> 450 entries. Query several keys before and
//   after removing B to see only ~1/3 of keys move.
//
// COMPLEXITY:
//   Time: add/remove O(V log(NV)); get O(log(NV)).
//   Space O(NV).

use std::collections::BTreeMap;
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};

pub struct ConsistentHashRing {
    v: usize,
    ring: BTreeMap<u64, String>,
}

impl ConsistentHashRing {
    pub fn new(vnodes: usize) -> Self { Self { v: vnodes, ring: BTreeMap::new() } }

    fn hash(s: &str) -> u64 {
        let mut h = DefaultHasher::new();
        s.hash(&mut h);
        h.finish()
    }

    pub fn add_node(&mut self, name: &str) {
        for i in 0..self.v {
            let key = format!("{}#VN{}", name, i);
            self.ring.insert(Self::hash(&key), name.to_string());
        }
    }
    pub fn remove_node(&mut self, name: &str) {
        for i in 0..self.v {
            let key = format!("{}#VN{}", name, i);
            self.ring.remove(&Self::hash(&key));
        }
    }
    pub fn get_node(&self, key: &str) -> Option<&str> {
        if self.ring.is_empty() { return None; }
        let h = Self::hash(key);
        if let Some((_, n)) = self.ring.range(h..).next() {
            return Some(n.as_str());
        }
        self.ring.iter().next().map(|(_, n)| n.as_str())
    }
}

fn main() {
    let mut ring = ConsistentHashRing::new(150);
    for n in ["server-A", "server-B", "server-C"] { ring.add_node(n); }
    for k in ["user:1001", "session:xyz", "order:42"] {
        println!("  {} -> {}", k, ring.get_node(k).unwrap_or("(empty)"));
    }
    println!("\nAfter removing server-B:");
    ring.remove_node("server-B");
    for k in ["user:1001", "session:xyz", "order:42"] {
        println!("  {} -> {}", k, ring.get_node(k).unwrap_or("(empty)"));
    }
}

// NOTES
// -----
// Differences from Java:
//   * BTreeMap::range(h..).next() replaces TreeMap.ceilingEntry.
//   * DefaultHasher used here; for cross-process stability use SipHasher
//     with a fixed seed or a cryptographic hash.
