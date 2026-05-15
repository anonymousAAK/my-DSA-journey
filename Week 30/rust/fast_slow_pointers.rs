// WEEK 30 - RUST ADVANCED TOPICS
// Topic: Fast & Slow Pointers (Floyd's Tortoise and Hare)
// File: fast_slow_pointers.rs
//
// CONCEPT:
//   Two cursors at speeds 1 and 2 over the same sequence; meeting implies
//   a cycle. Same idea applies to deterministic next-state functions
//   (Happy Number).
//
// KEY POINTS:
//   - O(n) time, O(1) space.
//   - For cycle entry: reset one cursor to head, walk both 1-step.
//
// ALGORITHM / APPROACH:
//   HAS CYCLE / DETECT START / MIDDLE / HAPPY: see code.
//
// RUST-SPECIFIC NOTES:
//   - Linked list with safe Rust + Box<Option<...>> doesn't model cycles
//     (ownership constraints). We model nodes by index in a Vec<Node> for
//     simplicity — this also keeps unsafe out.
//   - For Happy Number we operate on integers directly, no nodes needed.
//
// DRY RUN / EXAMPLE:
//   Vec-backed list 1 -> 2 -> 3 -> back to 2: has_cycle=true, entry=2.
//   is_happy(19)=true, is_happy(2)=false.
//
// COMPLEXITY:
//   Time O(n)   Space O(1)

#[derive(Clone, Copy, Debug)]
pub struct Node { pub val: i32, pub next: Option<usize> }

pub struct LinkedList { pub nodes: Vec<Node>, pub head: Option<usize> }

impl LinkedList {
    pub fn new() -> Self { Self { nodes: Vec::new(), head: None } }
    pub fn push_back(&mut self, v: i32) -> usize {
        let idx = self.nodes.len();
        self.nodes.push(Node { val: v, next: None });
        if self.head.is_none() {
            self.head = Some(idx);
        } else {
            let mut cur = self.head.unwrap();
            while let Some(n) = self.nodes[cur].next { cur = n; }
            self.nodes[cur].next = Some(idx);
        }
        idx
    }
    pub fn link(&mut self, from: usize, to: usize) { self.nodes[from].next = Some(to); }
}

pub fn has_cycle(list: &LinkedList) -> bool {
    let (mut slow, mut fast) = (list.head, list.head);
    while let (Some(s), Some(f)) = (slow, fast) {
        let next_fast = list.nodes[f].next;
        if next_fast.is_none() { return false; }
        slow = list.nodes[s].next;
        fast = list.nodes[next_fast.unwrap()].next;
        if slow == fast { return true; }
    }
    false
}

pub fn detect_cycle_start(list: &LinkedList) -> Option<usize> {
    let (mut slow, mut fast) = (list.head, list.head);
    while let (Some(s), Some(f)) = (slow, fast) {
        let next_fast = list.nodes[f].next?;
        slow = list.nodes[s].next;
        fast = list.nodes[next_fast].next;
        if slow == fast {
            let mut entry = list.head;
            while entry != slow {
                entry = list.nodes[entry.unwrap()].next;
                slow  = list.nodes[slow.unwrap()].next;
            }
            return entry;
        }
    }
    None
}

pub fn middle(list: &LinkedList) -> Option<usize> {
    let (mut slow, mut fast) = (list.head, list.head);
    while let Some(f) = fast {
        if let Some(nf) = list.nodes[f].next {
            slow = list.nodes[slow.unwrap()].next;
            fast = list.nodes[nf].next;
        } else { break; }
    }
    slow
}

fn digit_square_sum(mut n: i32) -> i32 {
    let mut s = 0;
    while n > 0 { let d = n % 10; s += d * d; n /= 10; }
    s
}

pub fn is_happy(n: i32) -> bool {
    let (mut slow, mut fast) = (n, n);
    loop {
        slow = digit_square_sum(slow);
        fast = digit_square_sum(digit_square_sum(fast));
        if slow == fast { return slow == 1; }
    }
}

fn main() {
    let mut list = LinkedList::new();
    let a = list.push_back(1);
    let b = list.push_back(2);
    let c = list.push_back(3);
    list.link(c, b); // cycle: 1 -> 2 -> 3 -> 2 -> ...
    let _ = a;
    println!("has_cycle: {}", has_cycle(&list));
    if let Some(idx) = detect_cycle_start(&list) {
        println!("cycle start val: {}", list.nodes[idx].val);
    }

    let mut acyclic = LinkedList::new();
    for v in [1,2,3,4,5] { acyclic.push_back(v); }
    if let Some(idx) = middle(&acyclic) {
        println!("middle val: {}", acyclic.nodes[idx].val);
    }

    println!("is_happy(19): {}", is_happy(19));
    println!("is_happy(2):  {}", is_happy(2));
}

// NOTES
// -----
// Differences from Java:
//   * Safe Rust pointer-graphs are awkward; we model nodes via Vec indices
//     to avoid borrow-checker pain and unsafe.
//   * Functions take &LinkedList rather than passing raw pointers.
