// Week 29: System Design - Consistent Hashing, LRU Cache, Rate Limiter, Trie, Merkle Tree

use std::collections::{BTreeMap, BinaryHeap, HashMap};
use std::cmp::Reverse;
use std::time::Instant;

// FNV-1a hash (portable, non-cryptographic). Use SHA-256 crate in production.
fn fnv_hash(data: &str) -> u64 {
    let mut h: u64 = 14695981039346656037;
    for b in data.bytes() { h ^= b as u64; h = h.wrapping_mul(1099511628211); }
    h
}
fn hash_hex(data: &str) -> String {
    let h1 = fnv_hash(data);
    let h2 = fnv_hash(&format!("{}\x01", data));
    format!("{:016x}{:016x}", h1, h2)
}

// === Consistent Hashing with Virtual Nodes ===
// Used by: DynamoDB, Cassandra, load balancers
// Lookup: O(log(N*V)) via BTreeMap   Space: O(N*V)
struct ConsistentHashRing {
    ring: BTreeMap<u64, String>,
    vnodes: usize,
}

impl ConsistentHashRing {
    fn new(vnodes: usize) -> Self {
        ConsistentHashRing { ring: BTreeMap::new(), vnodes }
    }

    // O(V * log(N*V))
    fn add_node(&mut self, node: &str) {
        for i in 0..self.vnodes {
            let h = fnv_hash(&format!("{}#VN{}", node, i));
            self.ring.insert(h, node.to_string());
        }
    }

    // O(V * log(N*V))
    fn remove_node(&mut self, node: &str) {
        for i in 0..self.vnodes {
            let h = fnv_hash(&format!("{}#VN{}", node, i));
            self.ring.remove(&h);
        }
    }

    // O(log(N*V)) — walk clockwise to next virtual node
    fn get_node(&self, key: &str) -> Option<&str> {
        if self.ring.is_empty() { return None; }
        let h = fnv_hash(key);
        // range(h..) gives first entry >= h; wrap around if needed
        let entry = self.ring.range(h..).next()
            .or_else(|| self.ring.iter().next());
        entry.map(|(_, v)| v.as_str())
    }
}

// === LRU Cache ===
// Uses HashMap + Vec-based ordering. For true O(1), use a linked list crate.
// This version: O(1) amortized get, O(N) eviction scan (simplified for clarity).
// Space: O(capacity)
struct LRUCache {
    capacity: usize,
    cache: HashMap<i32, (i32, u64)>, // key -> (value, access_order)
    order: u64,
}

impl LRUCache {
    fn new(capacity: usize) -> Self {
        LRUCache { capacity, cache: HashMap::new(), order: 0 }
    }
    fn get(&mut self, key: i32) -> i32 {
        if let Some(entry) = self.cache.get_mut(&key) {
            self.order += 1;
            entry.1 = self.order;
            entry.0
        } else { -1 }
    }
    fn put(&mut self, key: i32, value: i32) {
        self.order += 1;
        if self.cache.contains_key(&key) {
            self.cache.insert(key, (value, self.order));
            return;
        }
        if self.cache.len() == self.capacity {
            let lru_key = *self.cache.iter().min_by_key(|e| (e.1).1).unwrap().0;
            self.cache.remove(&lru_key);
        }
        self.cache.insert(key, (value, self.order));
    }
}

// === Token Bucket Rate Limiter ===
// Allows bursts up to capacity, enforces average rate.
// O(1) per request, O(1) space. Used by: API gateways, nginx
struct TokenBucket {
    max_tokens: f64,
    refill_rate: f64, // tokens per second
    tokens: f64,
    last_refill: Instant,
}

impl TokenBucket {
    fn new(max_tokens: u32, refill_rate: f64) -> Self {
        TokenBucket {
            max_tokens: max_tokens as f64,
            refill_rate,
            tokens: max_tokens as f64,
            last_refill: Instant::now(),
        }
    }

    fn allow_request(&mut self) -> bool {  // O(1)
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_refill).as_secs_f64();
        self.tokens = (self.tokens + elapsed * self.refill_rate).min(self.max_tokens);
        self.last_refill = now;
        if self.tokens >= 1.0 { self.tokens -= 1.0; true }
        else { false } // 429 Too Many Requests
    }
}

// === Trie Autocomplete with Frequency Ranking ===
// Insert: O(L)   Search: O(L + M + K log K)   Space: O(N*L)
// Used by: search engines, IDE completion, phone keyboards
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_end: bool,
    freq: i32,
    word: String,
}

impl TrieNode {
    fn new() -> Self {
        TrieNode { children: HashMap::new(), is_end: false, freq: 0, word: String::new() }
    }
}

struct AutoComplete { root: TrieNode }

impl AutoComplete {
    fn new() -> Self { AutoComplete { root: TrieNode::new() } }

    fn insert(&mut self, word: &str, freq: i32) {  // O(L)
        let mut node = &mut self.root;
        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(TrieNode::new);
        }
        node.is_end = true;
        node.freq += freq;
        node.word = word.to_string();
    }

    fn suggest(&self, prefix: &str, k: usize) -> Vec<String> {  // O(L + M + K log K)
        let mut node = &self.root;
        for ch in prefix.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return vec![],
            }
        }
        // Min-heap (via Reverse) to keep top-K by frequency
        let mut heap: BinaryHeap<Reverse<(i32, String)>> = BinaryHeap::new();
        Self::dfs(node, &mut heap, k);

        let mut results: Vec<_> = heap.into_iter().map(|Reverse((f, w))| (f, w)).collect();
        results.sort_by(|a, b| b.0.cmp(&a.0)); // descending frequency
        results.into_iter().map(|(_, w)| w).collect()
    }

    fn dfs(node: &TrieNode, heap: &mut BinaryHeap<Reverse<(i32, String)>>, k: usize) {
        if node.is_end {
            if heap.len() < k {
                heap.push(Reverse((node.freq, node.word.clone())));
            } else if let Some(&Reverse((min_freq, _))) = heap.peek() {
                if node.freq > min_freq {
                    heap.pop();
                    heap.push(Reverse((node.freq, node.word.clone())));
                }
            }
        }
        for child in node.children.values() {
            Self::dfs(child, heap, k);
        }
    }
}

// === Merkle Tree with Proof Verification ===
// Build: O(N)   Proof/Verify: O(log N)   Space: O(N)
// Used by: Bitcoin, Git, IPFS, DynamoDB anti-entropy
struct MerkleTree {
    tree: Vec<Vec<String>>,  // [0]=leaves, [last]=[root]
}

impl MerkleTree {
    fn new(data: &[&str]) -> Self {
        let mut leaves: Vec<String> = data.iter().map(|d| hash_hex(d)).collect();
        if leaves.len() % 2 != 0 { let last = leaves.last().unwrap().clone(); leaves.push(last); }

        let mut tree = vec![leaves.clone()];
        let mut cur = leaves;
        while cur.len() > 1 {
            let mut next = Vec::new();
            for i in (0..cur.len()).step_by(2) {
                let right = if i + 1 < cur.len() { &cur[i + 1] } else { &cur[i] };
                next.push(hash_hex(&format!("{}{}", cur[i], right)));
            }
            tree.push(next.clone());
            cur = next;
        }
        MerkleTree { tree }
    }

    fn root(&self) -> &str { &self.tree.last().unwrap()[0] }

    // Proof: list of (sibling_hash, sibling_is_left) — O(log N)
    fn get_proof(&self, mut idx: usize) -> Vec<(String, bool)> {
        let mut proof = Vec::new();
        for level in 0..self.tree.len() - 1 {
            let layer = &self.tree[level];
            if idx % 2 == 0 {
                let sib = if idx + 1 < layer.len() { &layer[idx + 1] } else { &layer[idx] };
                proof.push((sib.clone(), false));
            } else {
                proof.push((layer[idx - 1].clone(), true));
            }
            idx /= 2;
        }
        proof
    }

    // Recompute hash path and compare to root — O(log N)
    fn verify_proof(data: &str, proof: &[(String, bool)], root: &str) -> bool {
        let mut cur = hash_hex(data);
        for (sib, is_left) in proof {
            cur = if *is_left {
                hash_hex(&format!("{}{}", sib, cur))
            } else {
                hash_hex(&format!("{}{}", cur, sib))
            };
        }
        cur == root
    }
}

fn main() {
    println!("=== WEEK 29: System Design for Engineers (Rust) ===\n");

    // 1. Consistent Hashing
    println!("--- Consistent Hashing ---");
    let mut ring = ConsistentHashRing::new(150);
    ring.add_node("server-A"); ring.add_node("server-B"); ring.add_node("server-C");
    println!("Ring size: {}", ring.ring.len());
    for key in &["user:1001", "session:xyz", "order:42"] {
        println!("  {} -> {}", key, ring.get_node(key).unwrap_or("none"));
    }
    ring.remove_node("server-B");
    println!("After removing server-B:");
    for key in &["user:1001", "session:xyz", "order:42"] {
        println!("  {} -> {}", key, ring.get_node(key).unwrap_or("none"));
    }

    // 2. LRU Cache
    println!("\n--- LRU Cache ---");
    let mut cache = LRUCache::new(2);
    cache.put(1, 1); cache.put(2, 2);
    println!("get(1): {}", cache.get(1));
    cache.put(3, 3);
    println!("get(2): {}", cache.get(2)); // -1 (evicted)

    // 3. Rate Limiter
    println!("\n--- Token Bucket Rate Limiter ---");
    let mut tb = TokenBucket::new(5, 2.0);
    for i in 1..=7 {
        println!("  Request {}: {}", i, if tb.allow_request() { "ALLOWED" } else { "REJECTED" });
    }

    // 4. Trie Autocomplete
    println!("\n--- Trie Autocomplete ---");
    let mut ac = AutoComplete::new();
    ac.insert("system design", 50); ac.insert("system call", 30);
    ac.insert("systematic", 20); ac.insert("syntax", 10);
    println!("Top 3 for 'sys': {:?}", ac.suggest("sys", 3));

    // 5. Merkle Tree
    println!("\n--- Merkle Tree ---");
    let mt = MerkleTree::new(&["tx1:A->B:50", "tx2:B->C:30", "tx3:C->D:20", "tx4:D->E:10"]);
    println!("Root: {}...", &mt.root()[..16]);
    let proof = mt.get_proof(2);
    println!("Proof valid: {}", MerkleTree::verify_proof("tx3:C->D:20", &proof, mt.root()));
    println!("Tampered:    {}", MerkleTree::verify_proof("tx3:C->D:99", &proof, mt.root()));
}
