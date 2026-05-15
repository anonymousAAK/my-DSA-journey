/*
 * WEEK 21 - RUST ADVANCED DSA
 * Topic: Trie (Prefix Tree) + Binary Trie for Maximum XOR
 * File: 2.Trie.rs
 *
 * CONCEPT:
 *   Tries support prefix-keyed insert/search/startsWith in O(m). Each
 *   node has children, an is_end flag, and an optional word_count for
 *   prefix counting. A binary trie over integer bits computes Maximum
 *   XOR between any pair in O(n * B).
 *
 * KEY POINTS:
 *   - Children stored as fixed-size [Option<Box<TrieNode>>; 26].
 *   - Recursion vs borrow checker: we use index-based recursion and
 *     `Option::take` / `as_mut` to navigate children mutably.
 *   - Binary trie kept as flat Vec<[usize; 2]> to avoid borrow gymnastics
 *     on heap-allocated nodes.
 *
 * ALGORITHM / APPROACH:
 *   Same as Java reference: walk-or-create on insert, walk on search,
 *   recursive prune on delete. Greedy bit-walk for max_xor.
 *
 * RUST-SPECIFIC NOTES vs JAVA:
 *   - `Box<TrieNode>` for heap allocation; child slots are `Option<Box<>>`.
 *   - The borrow checker disallows holding two mutable references to the
 *     same Vec, so we navigate using indices in the flat binary trie.
 *   - Strings are UTF-8; `.bytes()` converts to u8 cheaply for ASCII.
 *   - Use `Vec<String>` for autocomplete results; build paths with a
 *     mutable `Vec<u8>` (or String) and pop after recursion.
 *
 * DRY RUN:
 *   Insert apple, app: shared a-p-p chain; "app" terminates after 3rd char.
 *   search("app") -> true; search("ap") -> false; starts_with("app") -> true.
 *   delete("app"): clears is_end on second 'p' but path remains for "apple".
 *
 *   max_xor([3,10,5,25,2,8]) -> 28 (5 ^ 25).
 *
 * COMPLEXITY:
 *   Trie ops: O(m). max_xor: O(n * B), B = bit length of max element.
 */

use std::collections::VecDeque;

const ALPHA: usize = 26;

#[derive(Default)]
pub struct TrieNode {
    children: [Option<Box<TrieNode>>; ALPHA],
    is_end: bool,
    word_count: i32,
}

#[derive(Default)]
pub struct Trie {
    root: TrieNode,
}

fn idx(c: u8) -> usize { (c - b'a') as usize }

impl Trie {
    pub fn new() -> Self { Trie::default() }

    pub fn insert(&mut self, word: &str) {
        let mut node = &mut self.root;
        for &b in word.as_bytes() {
            let i = idx(b);
            if node.children[i].is_none() {
                node.children[i] = Some(Box::new(TrieNode::default()));
            }
            node = node.children[i].as_mut().unwrap();
            node.word_count += 1;
        }
        node.is_end = true;
    }

    pub fn search(&self, word: &str) -> bool {
        let mut node = &self.root;
        for &b in word.as_bytes() {
            let i = idx(b);
            match &node.children[i] {
                Some(c) => node = c,
                None => return false,
            }
        }
        node.is_end
    }

    pub fn starts_with(&self, prefix: &str) -> bool {
        let mut node = &self.root;
        for &b in prefix.as_bytes() {
            let i = idx(b);
            match &node.children[i] {
                Some(c) => node = c,
                None => return false,
            }
        }
        true
    }

    pub fn count_with_prefix(&self, prefix: &str) -> i32 {
        let mut node = &self.root;
        for &b in prefix.as_bytes() {
            let i = idx(b);
            match &node.children[i] {
                Some(c) => node = c,
                None => return 0,
            }
        }
        node.word_count
    }

    pub fn autocomplete(&self, prefix: &str) -> Vec<String> {
        let mut node = &self.root;
        for &b in prefix.as_bytes() {
            let i = idx(b);
            match &node.children[i] {
                Some(c) => node = c,
                None => return vec![],
            }
        }
        let mut out = Vec::new();
        let mut buf: Vec<u8> = prefix.as_bytes().to_vec();
        Self::dfs_collect(node, &mut buf, &mut out);
        out
    }

    fn dfs_collect(node: &TrieNode, buf: &mut Vec<u8>, out: &mut Vec<String>) {
        if node.is_end {
            out.push(String::from_utf8(buf.clone()).unwrap());
        }
        for i in 0..ALPHA {
            if let Some(c) = &node.children[i] {
                buf.push(b'a' + i as u8);
                Self::dfs_collect(c, buf, out);
                buf.pop();
            }
        }
    }

    pub fn delete(&mut self, word: &str) -> bool {
        let bytes: Vec<u8> = word.as_bytes().to_vec();
        Self::delete_rec(&mut self.root, &bytes, 0)
    }

    fn delete_rec(node: &mut TrieNode, word: &[u8], i: usize) -> bool {
        if i == word.len() {
            if !node.is_end { return false; }
            node.is_end = false;
            return true;
        }
        let k = idx(word[i]);
        let child = match node.children[k].as_mut() {
            Some(c) => c,
            None => return false,
        };
        let deleted = Self::delete_rec(child, word, i + 1);
        if deleted {
            child.word_count -= 1;
            let no_children = child.children.iter().all(|c| c.is_none());
            if no_children && child.word_count == 0 {
                node.children[k] = None;
            }
        }
        deleted
    }
}

pub fn max_xor(nums: &[i32]) -> i32 {
    if nums.is_empty() { return 0; }
    let mx = *nums.iter().max().unwrap();
    let mut bits = 0;
    while (1 << bits) <= mx { bits += 1; }
    if bits == 0 { bits = 1; }

    let mut trie: Vec<[usize; 2]> = vec![[0, 0]];
    for &x in nums {
        let mut node = 0usize;
        for b in (0..bits).rev() {
            let bit = ((x >> b) & 1) as usize;
            if trie[node][bit] == 0 {
                trie.push([0, 0]);
                let new_idx = trie.len() - 1;
                trie[node][bit] = new_idx;
            }
            node = trie[node][bit];
        }
    }

    let mut best = 0i32;
    for &x in nums {
        let mut node = 0usize;
        let mut cur = 0i32;
        for b in (0..bits).rev() {
            let bit = ((x >> b) & 1) as usize;
            let want = 1 - bit;
            if trie[node][want] != 0 {
                cur |= 1 << b;
                node = trie[node][want];
            } else {
                node = trie[node][bit];
            }
        }
        if cur > best { best = cur; }
    }
    best
}

fn main() {
    // Silence unused warnings for VecDeque (kept for std-toolbox parity).
    let _ = VecDeque::<i32>::new();

    let mut trie = Trie::new();
    for w in ["apple","app","application","apply","apt","banana","band"] {
        trie.insert(w);
    }

    println!("=== Trie ===");
    println!("search('apple')     : {}", trie.search("apple"));
    println!("search('app')       : {}", trie.search("app"));
    println!("search('ap')        : {}", trie.search("ap"));
    println!("starts_with('app')  : {}", trie.starts_with("app"));
    println!("starts_with('xyz')  : {}", trie.starts_with("xyz"));

    let mut a = trie.autocomplete("app"); a.sort();
    println!("\nautocomplete('app'): {:?}", a);
    let mut b = trie.autocomplete("ban"); b.sort();
    println!("autocomplete('ban'): {:?}", b);
    println!("autocomplete('z')  : {:?}", trie.autocomplete("z"));

    trie.delete("app");
    println!("\nAfter deleting 'app':");
    println!("search('app')   : {}", trie.search("app"));
    println!("search('apple') : {}", trie.search("apple"));

    println!("\n=== Maximum XOR ===");
    println!("max_xor([3,10,5,25,2,8]) = {}", max_xor(&[3,10,5,25,2,8]));
    println!("max_xor([0,1,2])         = {}", max_xor(&[0,1,2]));
}
