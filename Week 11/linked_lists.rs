//! # Week 11: Linked Lists
//!
//! This module covers linked list implementations and related algorithms in Rust.
//! Topics include:
//! - Singly linked list using `Option<Box<Node>>` with push_front, push_back,
//!   pop_front, reverse, and display
//! - Merge two sorted lists (using `Vec<i32>` for simplicity)
//! - LRU Cache using `HashMap` + `VecDeque`
//!
//! ## Rust-Specific Notes for DSA Learners
//!
//! ### Why Linked Lists Are Hard in Rust
//! Rust's ownership model makes linked lists notoriously tricky:
//! - Each node can have exactly ONE owner. `Box<Node>` gives us single ownership.
//! - `Option<Box<Node>>` represents "either a node or nothing" — Rust's way of
//!   handling null pointers safely (no null pointer exceptions!).
//! - Doubly linked lists need shared ownership (`Rc<RefCell<Node>>`) or unsafe code
//!   because two nodes point to each other.
//! - For production Rust code, prefer `std::collections::LinkedList` or `VecDeque`.
//!
//! ### Design Choices
//! - We implement a singly linked list with `Option<Box<Node>>` to demonstrate
//!   the core pattern without excessive complexity.
//! - For merge sorted lists, we use `Vec<i32>` to avoid wrestling with two
//!   mutable linked list borrows simultaneously.
//! - The LRU cache uses `HashMap` + `VecDeque` — a practical Rust approach that
//!   avoids the complexity of a hand-rolled doubly linked list.

use std::collections::HashMap;
use std::collections::VecDeque;
use std::fmt;

// ===========================================================================
// Singly Linked List
// ===========================================================================

/// A node in the singly linked list.
///
/// `next` is `Option<Box<Node>>`:
/// - `None` means this is the last node.
/// - `Some(Box<Node>)` means there's a next node, owned by this node.
#[derive(Debug)]
struct Node {
    value: i32,
    next: Option<Box<Node>>,
}

/// A singly linked list.
///
/// `head` owns the first node (if any). Each node owns the next, forming a chain.
/// When the list is dropped, Rust drops each node in sequence — no memory leaks.
#[derive(Debug)]
struct LinkedList {
    head: Option<Box<Node>>,
    size: usize,
}

impl LinkedList {
    /// Creates an empty linked list.
    fn new() -> Self {
        LinkedList {
            head: None,
            size: 0,
        }
    }

    /// Pushes a value to the front of the list.
    ///
    /// The new node takes ownership of the current head, becoming the new head.
    ///
    /// # Complexity
    /// - Time:  O(1)
    /// - Space: O(1)
    fn push_front(&mut self, value: i32) {
        // `self.head.take()` moves the current head out, leaving `None` in its place.
        // This is a key Rust pattern — it avoids borrowing issues.
        let new_node = Box::new(Node {
            value,
            next: self.head.take(),
        });
        self.head = Some(new_node);
        self.size += 1;
    }

    /// Pushes a value to the back of the list.
    ///
    /// We traverse to the last node and attach the new node there.
    ///
    /// # Complexity
    /// - Time:  O(n)
    /// - Space: O(1)
    fn push_back(&mut self, value: i32) {
        let new_node = Box::new(Node {
            value,
            next: None,
        });

        // Navigate to the last node using a mutable reference.
        // `Option::as_mut()` gives `Option<&mut Box<Node>>` without taking ownership.
        let mut current = &mut self.head;
        while let Some(ref mut node) = current {
            if node.next.is_none() {
                node.next = Some(new_node);
                self.size += 1;
                return;
            }
            current = &mut node.next;
        }

        // If list was empty, set head.
        self.head = Some(new_node);
        self.size += 1;
    }

    /// Removes and returns the front element.
    ///
    /// Uses `take()` to move the head out, then sets head to the next node.
    ///
    /// # Complexity
    /// - Time:  O(1)
    /// - Space: O(1)
    fn pop_front(&mut self) -> Option<i32> {
        // `map` transforms `Option<Box<Node>>` into `Option<i32>` after extracting.
        self.head.take().map(|node| {
            self.head = node.next;
            self.size -= 1;
            node.value
        })
    }

    /// Reverses the linked list in place.
    ///
    /// Classic iterative reversal: maintain `prev` and `current`, re-point each
    /// node's `next` to `prev`.
    ///
    /// In Rust, we use `take()` extensively to move ownership between nodes
    /// without violating the borrow checker.
    ///
    /// # Complexity
    /// - Time:  O(n)
    /// - Space: O(1)
    fn reverse(&mut self) {
        let mut prev: Option<Box<Node>> = None;
        let mut current = self.head.take();

        while let Some(mut node) = current {
            // Save next node.
            let next = node.next.take();
            // Point current node's next to prev.
            node.next = prev;
            // Advance: prev = current, current = next.
            prev = Some(node);
            current = next;
        }

        self.head = prev;
    }

    /// Returns the list as a Vec for easy comparison in tests.
    fn to_vec(&self) -> Vec<i32> {
        let mut result = Vec::new();
        let mut current = &self.head;
        while let Some(node) = current {
            result.push(node.value);
            current = &node.next;
        }
        result
    }

    /// Returns the number of elements.
    fn len(&self) -> usize {
        self.size
    }

    /// Returns true if the list is empty.
    fn is_empty(&self) -> bool {
        self.size == 0
    }
}

/// Display implementation for the linked list.
///
/// Prints like: `1 -> 2 -> 3 -> None`
impl fmt::Display for LinkedList {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let mut current = &self.head;
        while let Some(node) = current {
            write!(f, "{} -> ", node.value)?;
            current = &node.next;
        }
        write!(f, "None")
    }
}

// ===========================================================================
// Merge Two Sorted Lists (using Vec<i32>)
// ===========================================================================

/// Merges two sorted `Vec<i32>` into a single sorted `Vec<i32>`.
///
/// This is the classic merge step from merge sort. We use `Vec<i32>` because
/// merging two `Option<Box<Node>>` linked lists in Rust requires careful
/// ownership juggling — `Vec` is simpler and equally instructive.
///
/// # Complexity
/// - Time:  O(n + m)
/// - Space: O(n + m) — the output vector
fn merge_sorted_lists(a: &[i32], b: &[i32]) -> Vec<i32> {
    let mut result = Vec::with_capacity(a.len() + b.len());
    let mut i = 0;
    let mut j = 0;

    while i < a.len() && j < b.len() {
        if a[i] <= b[j] {
            result.push(a[i]);
            i += 1;
        } else {
            result.push(b[j]);
            j += 1;
        }
    }

    // Append remaining elements using slice extension — idiomatic Rust.
    result.extend_from_slice(&a[i..]);
    result.extend_from_slice(&b[j..]);

    result
}

// ===========================================================================
// LRU Cache (HashMap + VecDeque)
// ===========================================================================

/// A simplified LRU (Least Recently Used) cache.
///
/// ## Implementation Strategy
/// - `HashMap<i32, i32>` stores key-value pairs for O(1) lookup.
/// - `VecDeque<i32>` maintains access order (most recent at back).
/// - On `get` or `put`, we move the key to the back of the deque.
/// - On eviction (capacity exceeded), we remove the front of the deque.
///
/// ## Caveat
/// This simplified version has O(n) removal from the middle of VecDeque.
/// A production LRU cache would use a doubly linked list with HashMap pointers
/// for O(1) operations (see `std::collections::LinkedList` or the `lru` crate).
///
/// # Complexity (per operation)
/// - `get`:  O(n) worst case due to VecDeque scan (O(1) amortized in practice)
/// - `put`:  O(n) worst case
struct LRUCache {
    capacity: usize,
    map: HashMap<i32, i32>,
    order: VecDeque<i32>, // Front = least recently used, back = most recently used.
}

impl LRUCache {
    fn new(capacity: usize) -> Self {
        LRUCache {
            capacity,
            map: HashMap::new(),
            order: VecDeque::new(),
        }
    }

    /// Gets the value for `key`, marking it as most recently used.
    /// Returns `None` if the key doesn't exist.
    fn get(&mut self, key: i32) -> Option<i32> {
        if let Some(&value) = self.map.get(&key) {
            // Move key to back (most recently used).
            self.move_to_back(key);
            Some(value)
        } else {
            None
        }
    }

    /// Inserts or updates a key-value pair.
    /// If the cache exceeds capacity, evicts the least recently used entry.
    fn put(&mut self, key: i32, value: i32) {
        if self.map.contains_key(&key) {
            // Update existing key.
            self.map.insert(key, value);
            self.move_to_back(key);
        } else {
            // Evict if at capacity.
            if self.map.len() >= self.capacity {
                if let Some(lru_key) = self.order.pop_front() {
                    self.map.remove(&lru_key);
                }
            }
            self.map.insert(key, value);
            self.order.push_back(key);
        }
    }

    /// Moves a key to the back of the order deque.
    fn move_to_back(&mut self, key: i32) {
        // Find and remove the key from its current position.
        // This is O(n) — the tradeoff for using VecDeque instead of a linked list.
        if let Some(pos) = self.order.iter().position(|&k| k == key) {
            self.order.remove(pos);
        }
        self.order.push_back(key);
    }

    /// Returns the current number of entries.
    fn len(&self) -> usize {
        self.map.len()
    }
}

impl fmt::Display for LRUCache {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "LRU[")?;
        for (i, key) in self.order.iter().enumerate() {
            if i > 0 {
                write!(f, ", ")?;
            }
            write!(f, "{}={}", key, self.map[key])?;
        }
        write!(f, "]")
    }
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 11: Linked Lists ===\n");

    // --- Singly Linked List ---
    println!("--- Singly Linked List ---");

    let mut list = LinkedList::new();
    assert!(list.is_empty());

    // push_front
    list.push_front(3);
    list.push_front(2);
    list.push_front(1);
    assert_eq!(list.to_vec(), vec![1, 2, 3]);
    assert_eq!(list.len(), 3);
    println!("After push_front(3, 2, 1): {}", list);

    // push_back
    list.push_back(4);
    list.push_back(5);
    assert_eq!(list.to_vec(), vec![1, 2, 3, 4, 5]);
    println!("After push_back(4, 5):     {}", list);

    // pop_front
    let val = list.pop_front();
    assert_eq!(val, Some(1));
    assert_eq!(list.to_vec(), vec![2, 3, 4, 5]);
    println!("After pop_front():         {} (popped {})", list, val.unwrap());

    // reverse
    list.reverse();
    assert_eq!(list.to_vec(), vec![5, 4, 3, 2]);
    println!("After reverse():           {}", list);

    // Pop all
    let mut popped = Vec::new();
    while let Some(v) = list.pop_front() {
        popped.push(v);
    }
    assert_eq!(popped, vec![5, 4, 3, 2]);
    assert!(list.is_empty());
    println!("Popped all: {:?}, list is now empty: {}", popped, list);

    // Edge case: reverse empty list
    list.reverse();
    assert!(list.is_empty());

    // Edge case: pop from empty
    assert_eq!(list.pop_front(), None);

    // --- Merge Sorted Lists ---
    println!("\n--- Merge Sorted Lists ---");
    let a = vec![1, 3, 5, 7];
    let b = vec![2, 4, 6, 8, 10];
    let merged = merge_sorted_lists(&a, &b);
    assert_eq!(merged, vec![1, 2, 3, 4, 5, 6, 7, 8, 10]);
    println!("merge({:?}, {:?}) = {:?}", a, b, merged);

    // One empty
    let merged2 = merge_sorted_lists(&[1, 2, 3], &[]);
    assert_eq!(merged2, vec![1, 2, 3]);

    // Both empty
    let merged3 = merge_sorted_lists(&[], &[]);
    assert!(merged3.is_empty());

    // Duplicates
    let merged4 = merge_sorted_lists(&[1, 1, 3], &[1, 2, 3]);
    assert_eq!(merged4, vec![1, 1, 1, 2, 3, 3]);
    println!("merge([1,1,3], [1,2,3]) = {:?}", merged4);

    // --- LRU Cache ---
    println!("\n--- LRU Cache ---");
    let mut cache = LRUCache::new(3);

    cache.put(1, 10);
    cache.put(2, 20);
    cache.put(3, 30);
    println!("After inserting 1=10, 2=20, 3=30: {}", cache);
    assert_eq!(cache.get(1), Some(10));
    println!("get(1) = {:?} -> {}", Some(10), cache);

    // Insert 4 — should evict key 2 (least recently used, since we just accessed 1).
    cache.put(4, 40);
    assert_eq!(cache.len(), 3);
    assert_eq!(cache.get(2), None); // Evicted!
    assert_eq!(cache.get(3), Some(30));
    assert_eq!(cache.get(4), Some(40));
    println!("After put(4, 40) [evicts 2]: {}", cache);
    println!("get(2) = {:?} (evicted)", cache.get(2));

    // Update existing key
    cache.put(3, 300);
    assert_eq!(cache.get(3), Some(300));
    println!("After put(3, 300) [update]: {}", cache);

    // Insert 5 — should evict key 1.
    cache.put(5, 50);
    assert_eq!(cache.get(1), None); // Evicted!
    println!("After put(5, 50) [evicts 1]: {}", cache);

    println!("\nAll assertions passed!");
}
