// Week 29: System Design - LRU Cache, Trie Autocomplete
use std::collections::HashMap;

// === LRU Cache (simplified with Vec-based DLL) ===
struct LRUCache {
    capacity: usize,
    cache: HashMap<i32, (i32, usize)>, // key -> (value, order)
    order: usize,
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

// === Trie Autocomplete ===
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_end: bool,
    freq: i32,
}

impl TrieNode {
    fn new() -> Self { TrieNode { children: HashMap::new(), is_end: false, freq: 0 } }
}

struct AutoComplete { root: TrieNode }

impl AutoComplete {
    fn new() -> Self { AutoComplete { root: TrieNode::new() } }

    fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for ch in word.chars() {
            node = node.children.entry(ch).or_insert_with(TrieNode::new);
        }
        node.is_end = true;
        node.freq += 1;
    }

    fn suggest(&self, prefix: &str, k: usize) -> Vec<String> {
        let mut node = &self.root;
        for ch in prefix.chars() {
            match node.children.get(&ch) {
                Some(child) => node = child,
                None => return vec![],
            }
        }
        let mut results = Vec::new();
        Self::dfs(node, &mut prefix.to_string(), &mut results);
        results.sort_by(|a, b| b.0.cmp(&a.0));
        results.into_iter().take(k).map(|(_, w)| w).collect()
    }

    fn dfs(node: &TrieNode, path: &mut String, results: &mut Vec<(i32, String)>) {
        if node.is_end { results.push((node.freq, path.clone())); }
        for (&ch, child) in &node.children {
            path.push(ch);
            Self::dfs(child, path, results);
            path.pop();
        }
    }
}

fn main() {
    let mut cache = LRUCache::new(2);
    cache.put(1, 1); cache.put(2, 2);
    println!("LRU get(1): {}", cache.get(1));
    cache.put(3, 3);
    println!("LRU get(2): {}", cache.get(2));

    let mut ac = AutoComplete::new();
    for w in &["cat","car","card","care"] { ac.insert(w); }
    println!("Autocomplete 'car': {:?}", ac.suggest("car", 3));
}
