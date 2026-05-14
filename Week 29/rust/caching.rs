// WEEK 29 - RUST ADVANCED TOPICS
// Topic: Caching - LRU, LFU and TTL
// File: caching.rs
//
// CONCEPT:
//   Caches accelerate access to recurring queries by storing values in
//   limited fast storage. Eviction policy decides what to drop:
//     - LRU: drop least recently used.
//     - LFU: drop least frequently used.
//     - TTL: drop after a deadline.
//
// KEY POINTS:
//   - LRU: ordered map of (key, val); on touch move to back.
//   - LFU: HashMap of (val, freq, list iter) + freq -> VecDeque<key>.
//   - TTL: HashMap<K, (V, Instant)>; lazy eviction on access.
//
// ALGORITHM / APPROACH:
//   LRU touch: remove(key); insert at back. On overflow drop front.
//   LFU touch: bump freq; move key from bucket f to f+1.
//
// RUST-SPECIFIC NOTES:
//   - LRU here uses a simple `VecDeque<K>` ordering + `HashMap<K, V>`;
//     O(n) move-to-back. For production use the `lru` crate or hand-roll
//     a doubly-linked list with raw pointers.
//   - LFU uses HashMap<K, (V, freq)> + HashMap<freq, VecDeque<K>>.
//   - std::time::Instant is the monotonic clock.
//
// DRY RUN / EXAMPLE:
//   LRU cap=2: put(1,1); put(2,2); get(1)=Some(1); put(3,3) evicts 2.
//   LFU cap=2: get(1) twice -> freq 3; put(3,3) evicts 2 (freq 1).
//
// COMPLEXITY:
//   This LRU is O(n) per op for simplicity; the LFU is O(1) amortised.

use std::collections::{HashMap, VecDeque};
use std::time::{Duration, Instant};
use std::thread;

pub struct LRUCache {
    cap: usize,
    order: VecDeque<i32>,                  // front = least recent, back = most recent
    map: HashMap<i32, i32>,
}

impl LRUCache {
    pub fn new(cap: usize) -> Self {
        Self { cap, order: VecDeque::new(), map: HashMap::new() }
    }
    fn touch(&mut self, key: i32) {
        if let Some(pos) = self.order.iter().position(|&k| k == key) {
            self.order.remove(pos);
        }
        self.order.push_back(key);
    }
    pub fn get(&mut self, key: i32) -> i32 {
        match self.map.get(&key).copied() {
            Some(v) => { self.touch(key); v }
            None => -1,
        }
    }
    pub fn put(&mut self, key: i32, val: i32) {
        if self.map.contains_key(&key) {
            self.map.insert(key, val);
            self.touch(key);
            return;
        }
        if self.map.len() == self.cap {
            if let Some(evict) = self.order.pop_front() {
                self.map.remove(&evict);
            }
        }
        self.map.insert(key, val);
        self.order.push_back(key);
    }
}

pub struct LFUCache {
    cap: usize,
    min_freq: u32,
    kv: HashMap<i32, (i32, u32)>,                  // key -> (value, freq)
    freq_keys: HashMap<u32, VecDeque<i32>>,        // freq -> LRU within bucket
}

impl LFUCache {
    pub fn new(cap: usize) -> Self {
        Self { cap, min_freq: 0, kv: HashMap::new(), freq_keys: HashMap::new() }
    }
    fn bump(&mut self, key: i32) {
        if let Some((val, freq)) = self.kv.get(&key).copied() {
            // Remove from old bucket
            if let Some(bucket) = self.freq_keys.get_mut(&freq) {
                if let Some(pos) = bucket.iter().position(|&k| k == key) {
                    bucket.remove(pos);
                }
                if bucket.is_empty() {
                    self.freq_keys.remove(&freq);
                    if self.min_freq == freq { self.min_freq += 1; }
                }
            }
            let new_f = freq + 1;
            self.kv.insert(key, (val, new_f));
            self.freq_keys.entry(new_f).or_default().push_back(key);
        }
    }
    pub fn get(&mut self, key: i32) -> i32 {
        if !self.kv.contains_key(&key) { return -1; }
        let val = self.kv[&key].0;
        self.bump(key);
        val
    }
    pub fn put(&mut self, key: i32, val: i32) {
        if self.cap == 0 { return; }
        if self.kv.contains_key(&key) {
            let f = self.kv[&key].1;
            self.kv.insert(key, (val, f));
            self.bump(key);
            return;
        }
        if self.kv.len() >= self.cap {
            if let Some(bucket) = self.freq_keys.get_mut(&self.min_freq) {
                if let Some(evict) = bucket.pop_front() {
                    self.kv.remove(&evict);
                    if bucket.is_empty() { self.freq_keys.remove(&self.min_freq); }
                }
            }
        }
        self.kv.insert(key, (val, 1));
        self.freq_keys.entry(1).or_default().push_back(key);
        self.min_freq = 1;
    }
}

pub struct TTLCache {
    default_ttl: Duration,
    store: HashMap<String, (String, Instant)>,
}

impl TTLCache {
    pub fn new(default_ttl_ms: u64) -> Self {
        Self { default_ttl: Duration::from_millis(default_ttl_ms), store: HashMap::new() }
    }
    pub fn put(&mut self, k: &str, v: &str) {
        self.store.insert(k.to_string(), (v.to_string(), Instant::now() + self.default_ttl));
    }
    pub fn get(&mut self, k: &str) -> Option<String> {
        if let Some((v, dl)) = self.store.get(k) {
            if *dl >= Instant::now() {
                return Some(v.clone());
            }
        }
        self.store.remove(k);
        None
    }
}

fn main() {
    let mut lru = LRUCache::new(2);
    lru.put(1, 1); lru.put(2, 2);
    println!("LRU get(1) = {}", lru.get(1));
    lru.put(3, 3);
    println!("LRU get(2) = {}  (expected -1)", lru.get(2));

    let mut lfu = LFUCache::new(2);
    lfu.put(1, 1); lfu.put(2, 2);
    lfu.get(1); lfu.get(1);
    lfu.put(3, 3);
    println!("LFU get(2) = {}  (expected -1)", lfu.get(2));
    println!("LFU get(1) = {}  (expected 1)", lfu.get(1));
    println!("LFU get(3) = {}  (expected 3)", lfu.get(3));

    let mut ttl = TTLCache::new(50);
    ttl.put("alpha", "value");
    println!("TTL get(alpha) imm.: {:?}", ttl.get("alpha"));
    thread::sleep(Duration::from_millis(60));
    println!("TTL get(alpha) later: {:?}", ttl.get("alpha"));
}

// NOTES
// -----
// Differences from Java:
//   * Rust lacks a built-in ordered hashmap; our LRU uses a VecDeque +
//     HashMap, accepting O(n) touch for simplicity (the `lru` crate offers
//     O(1)).
//   * std::time::Instant is the monotonic clock counterpart of Java's
//     System.nanoTime.
//   * No third-party crates used — pure std for portability.
