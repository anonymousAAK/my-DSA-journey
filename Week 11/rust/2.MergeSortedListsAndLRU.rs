/*
 * WEEK 11 - RUST DSA
 * Topic: Merge Two Sorted Lists + LRU Cache
 * File: 2.MergeSortedListsAndLRU.rs
 *
 * CONCEPT:
 *   PART A - Merge two sorted singly-linked lists by re-wiring nodes.
 *   PART B - LRU cache using a HashMap<K, key-position> + VecDeque<K> for the
 *            usage order. We also describe how the `lru` crate would be used
 *            in production.
 *
 * KEY POINTS:
 *   - Rust's ownership rules push us toward different data structures than
 *     Java's classic "DLL + HashMap<K, Node>" pattern. The intrusive doubly
 *     linked list with two mut-borrowed nodes per operation is famously
 *     hostile to the borrow checker without unsafe.
 *   - VecDeque + HashMap<K, V> still gives O(1) get/put if you treat the
 *     deque as your usage log AND clean stale entries lazily — but exact
 *     O(1) requires a true linked structure.
 *   - For correctness AND O(1), the standard trick is HashMap<K, V> +
 *     ordered indices using std::collections::LinkedList with cursor APIs
 *     (still nightly), OR the third-party `lru` crate.
 *   - We provide a clean O(n) eviction LRU here (find LRU by linear scan)
 *     for clarity, and document what would change to make it O(1).
 *
 * ALGORITHM / APPROACH:
 *   merge: standard 2-pointer with sentinel.
 *   LRU.get(k): if absent return None; else move k to "front" of usage
 *               vector, return value.
 *   LRU.put(k,v): update or insert; if over capacity, evict LRU (back of
 *                 usage vector).
 *
 * RUST-SPECIFIC NOTES:
 *   - We use Option<Box<ListNode>> for the merge, just like the Week 11
 *     SinglyLinkedList file.
 *   - VecDeque has O(1) push/pop on either end and O(n) middle removal.
 *     For the LRU we keep a `Vec<K>` ordered MRU-first; moving an existing
 *     key to front is O(n) (linear find + remove). Acceptable for teaching;
 *     for production use the `lru` crate (constant-time via intrusive list).
 *
 * DRY RUN:
 *   merge [1,2,4] + [1,3,4]:
 *     Same trace as the other languages: 1 -> 1 -> 2 -> 3 -> 4 -> 4
 *
 *   LRUCache(3):
 *     put(1,1): map={1:1}, order=[1]
 *     put(2,2): map={1:1,2:2}, order=[2,1]
 *     put(3,3): map={1:1,2:2,3:3}, order=[3,2,1]
 *     get(1) -> 1; order=[1,3,2]
 *     put(4,4): full -> evict 2; order=[4,1,3]
 *     get(2) -> None
 *
 * COMPLEXITY:
 *   merge: O(m+n)
 *   LRU get/put (this implementation): O(capacity) due to Vec move-to-front.
 *   With proper intrusive DLL (or `lru` crate): O(1) get/put.
 */

use std::collections::HashMap;

// ---------- PART A: Merge sorted lists ----------

#[derive(Debug)]
struct ListNode {
    val: i32,
    next: Option<Box<ListNode>>,
}

fn build_list(vs: &[i32]) -> Option<Box<ListNode>> {
    let mut head: Option<Box<ListNode>> = None;
    for &v in vs.iter().rev() {
        head = Some(Box::new(ListNode { val: v, next: head }));
    }
    head
}

fn print_list(mut head: Option<&ListNode>) -> String {
    let mut parts = Vec::new();
    while let Some(n) = head {
        parts.push(n.val.to_string());
        head = n.next.as_deref();
    }
    parts.join(" -> ")
}

fn merge_sorted_lists(
    mut l1: Option<Box<ListNode>>,
    mut l2: Option<Box<ListNode>>,
) -> Option<Box<ListNode>> {
    let mut dummy: Box<ListNode> = Box::new(ListNode { val: 0, next: None });
    // Use a raw mutable pointer trick via &mut Option<Box<ListNode>>.
    let mut tail: &mut Option<Box<ListNode>> = &mut dummy.next;
    loop {
        match (l1.as_ref(), l2.as_ref()) {
            (None, None) => break,
            (Some(_), None) => { *tail = l1.take(); break; }
            (None, Some(_)) => { *tail = l2.take(); break; }
            (Some(a), Some(b)) => {
                if a.val <= b.val {
                    let mut n = l1.take().unwrap();
                    l1 = n.next.take();
                    *tail = Some(n);
                } else {
                    let mut n = l2.take().unwrap();
                    l2 = n.next.take();
                    *tail = Some(n);
                }
                tail = &mut tail.as_mut().unwrap().next;
            }
        }
    }
    dummy.next
}

// ---------- PART B: LRU Cache ----------

pub struct LruCache {
    capacity: usize,
    map: HashMap<i32, i32>,
    /// Order: front = most recently used, back = least recently used.
    order: Vec<i32>,
}

impl LruCache {
    pub fn new(capacity: usize) -> Self {
        Self { capacity, map: HashMap::new(), order: Vec::with_capacity(capacity) }
    }

    pub fn get(&mut self, key: i32) -> Option<i32> {
        let v = *self.map.get(&key)?;
        self.touch(key);
        Some(v)
    }

    pub fn put(&mut self, key: i32, value: i32) {
        if self.map.contains_key(&key) {
            self.map.insert(key, value);
            self.touch(key);
            return;
        }
        if self.map.len() == self.capacity {
            if let Some(lru) = self.order.pop() {
                self.map.remove(&lru);
            }
        }
        self.order.insert(0, key);
        self.map.insert(key, value);
    }

    fn touch(&mut self, key: i32) {
        if let Some(pos) = self.order.iter().position(|&k| k == key) {
            self.order.remove(pos);
            self.order.insert(0, key);
        }
    }

    pub fn state(&self) -> String {
        let mut s = String::from("Cache (MRU->LRU): ");
        let parts: Vec<String> = self.order.iter()
            .map(|k| format!("[{}={}]", k, self.map[k]))
            .collect();
        s.push_str(&parts.join(" -> "));
        s
    }
}

// ---------- main ----------

fn main() {
    println!("=== Merge Sorted Lists ===");
    let l1 = build_list(&[1, 2, 4]);
    let l2 = build_list(&[1, 3, 4]);
    let m1 = merge_sorted_lists(l1, l2);
    println!("Merged: {}", print_list(m1.as_deref()));

    let l3 = build_list(&[1, 3, 5, 7]);
    let l4 = build_list(&[2, 4, 6, 8, 10]);
    let m2 = merge_sorted_lists(l3, l4);
    println!("Merged: {}", print_list(m2.as_deref()));

    println!("\n=== LRU Cache (capacity=3) ===");
    let mut cache = LruCache::new(3);
    cache.put(1, 1); println!("{}", cache.state());
    cache.put(2, 2); println!("{}", cache.state());
    cache.put(3, 3); println!("{}", cache.state());
    println!("get(1) = {:?}", cache.get(1));
    println!("{}", cache.state());
    cache.put(4, 4);
    println!("{}", cache.state());
    println!("get(2) = {:?}", cache.get(2));
    println!("get(3) = {:?}", cache.get(3));
    println!("get(4) = {:?}", cache.get(4));
    println!("{}", cache.state());
}

/*
 * NOTES (vs. Java):
 * - Java's intrusive DLL + HashMap<K, Node> pattern is hard to express in
 *   safe Rust. The cleanest options are:
 *     1) The `lru` crate (uses unsafe internally for an intrusive list).
 *     2) std::collections::LinkedList + Cursor API (currently nightly-only
 *        for full mutation power).
 *     3) Roll your own with raw pointers + unsafe.
 *   Our teaching version is O(capacity) per op via a Vec used as usage log;
 *   for capacity small (typical) this is fine.
 * - Where Java throws on null, Rust uses Option<i32> as a return type so
 *   the caller is forced to handle missing keys.
 * - Box<ListNode> means each node is heap-allocated and singly owned —
 *   the same shape as the Week 11 SinglyLinkedList.
 */
