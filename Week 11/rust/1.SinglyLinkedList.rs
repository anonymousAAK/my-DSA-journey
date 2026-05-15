/*
 * WEEK 11 - RUST DSA
 * Topic: Singly Linked List - Complete Implementation
 * File: 1.SinglyLinkedList.rs
 *
 * CONCEPT:
 *   A singly linked list of i32 values. Each node owns the next via
 *   Option<Box<Node>>. The Option encodes "no next" (None) without a null
 *   pointer; Box gives heap allocation with single ownership.
 *
 * KEY POINTS:
 *   - Rust's ownership model makes naive linked-list code surprisingly hard.
 *     A single owner per node forces certain operations (e.g. middle-find,
 *     cycle detection) to be coded with care or use raw pointers / Rc.
 *   - We use Option<Box<Node>> for the basic list and switch to *const Node
 *     (shared-borrow raw pointers) inside `find_middle` / `has_cycle` to
 *     avoid splitting borrows across the loop body.
 *   - .take() is the workhorse for swapping ownership out of a slot.
 *
 * ALGORITHM / APPROACH:
 *   insert_at_head: new.next = old head; head = Some(new).
 *   insert_at_tail: walk to last; set its next.
 *   insert_at_index: walk to idx-1, splice.
 *   delete_by_value: walk with mutable pointer; on match `cur.next =
 *                    cur.next.take().unwrap().next`.
 *   reverse_iterative: 3-pointer pattern using `Option::take`.
 *   reverse_recursive: harder in safe Rust because of move semantics — we
 *                      provide an iterative-via-stack alternative as well.
 *   find_middle / has_cycle: Floyd's pattern via raw read-only pointers.
 *
 * RUST-SPECIFIC NOTES:
 *   "Why is a singly linked list non-trivial in Rust?"
 *     - Rust forbids two mutable references to the same data.
 *     - Many list algorithms naturally want both `prev` and `curr` mutably,
 *       which fights the borrow checker.
 *     - Solutions: (a) use Option::take to move ownership around;
 *                  (b) use unsafe / raw pointers; (c) use Rc/RefCell for
 *                      doubly linked or shared structures.
 *   - We avoid `unsafe` everywhere except inside `find_middle` / `has_cycle`
 *     where we deref *const Node — those reads are safe by construction
 *     (we only read fields we own).
 *   - The standard library has `std::collections::LinkedList` (doubly
 *     linked) — for production prefer `Vec` or `VecDeque` for cache locality.
 *
 * DRY RUN:
 *   Example 1: insert_at_tail 1,2,3 then insert_at_head 0
 *     []
 *     [1]
 *     [1,2]
 *     [1,2,3]
 *     insert_at_head 0 -> [0,1,2,3]
 *
 *   Example 2: reverse_iterative on [1,2,3]
 *     prev=None, curr=Some(1)
 *     step: take 1.next (Some(2)); set 1.next=prev=None; prev=Some(1); curr=Some(2)
 *     step: take 2.next (Some(3)); set 2.next=Some(1);   prev=Some(2); curr=Some(3)
 *     step: take 3.next (None);    set 3.next=Some(2);   prev=Some(3); curr=None
 *     head = Some(3) -> [3,2,1]
 *
 * COMPLEXITY:
 *   insert_head/delete_head: O(1)
 *   insert_tail/insert_at_index/delete_by_value/contains/len: O(n)
 *   reverse_iterative: O(n) time, O(1) space
 *   find_middle / has_cycle: O(n) time, O(1) space
 */

struct Node {
    data: i32,
    next: Option<Box<Node>>,
}

pub struct LinkedList {
    head: Option<Box<Node>>,
}

impl LinkedList {
    pub fn new() -> Self { LinkedList { head: None } }

    pub fn insert_at_head(&mut self, data: i32) {
        let new = Box::new(Node { data, next: self.head.take() });
        self.head = Some(new);
    }

    pub fn insert_at_tail(&mut self, data: i32) {
        let mut cur = &mut self.head;
        while let Some(node) = cur {
            cur = &mut node.next;
        }
        *cur = Some(Box::new(Node { data, next: None }));
    }

    pub fn insert_at_index(&mut self, idx: usize, data: i32) {
        if idx == 0 { self.insert_at_head(data); return; }
        let mut cur = self.head.as_deref_mut();
        for _ in 0..(idx - 1) {
            cur = match cur {
                Some(n) => n.next.as_deref_mut(),
                None => panic!("Index out of bounds"),
            };
        }
        let cur = cur.expect("Index out of bounds");
        let new = Box::new(Node { data, next: cur.next.take() });
        cur.next = Some(new);
    }

    pub fn delete_head(&mut self) {
        if let Some(boxed) = self.head.take() {
            self.head = boxed.next;
        }
    }

    pub fn delete_by_value(&mut self, val: i32) -> bool {
        // Special-case the head.
        if let Some(h) = self.head.as_ref() {
            if h.data == val {
                let old = self.head.take().unwrap();
                self.head = old.next;
                return true;
            }
        } else {
            return false;
        }
        let mut cur = self.head.as_deref_mut().unwrap();
        loop {
            // Peek next
            let drop_it = matches!(&cur.next, Some(n) if n.data == val);
            if drop_it {
                let mut removed = cur.next.take().unwrap();
                cur.next = removed.next.take();
                return true;
            }
            match cur.next.as_deref_mut() {
                Some(n) => cur = n,
                None => return false,
            }
        }
    }

    pub fn contains(&self, val: i32) -> bool {
        let mut cur = self.head.as_deref();
        while let Some(n) = cur {
            if n.data == val { return true; }
            cur = n.next.as_deref();
        }
        false
    }

    pub fn len(&self) -> usize {
        let mut n = 0usize;
        let mut cur = self.head.as_deref();
        while let Some(node) = cur {
            n += 1;
            cur = node.next.as_deref();
        }
        n
    }

    pub fn reverse_iterative(&mut self) {
        let mut prev: Option<Box<Node>> = None;
        let mut curr = self.head.take();
        while let Some(mut node) = curr {
            let next = node.next.take();
            node.next = prev;
            prev = Some(node);
            curr = next;
        }
        self.head = prev;
    }

    /// Reverse via an explicit stack (a recursive version in safe Rust
    /// is awkward because of move semantics; this is the idiomatic fix).
    pub fn reverse_recursive(&mut self) {
        // For symmetry with the Java sample: we just call iterative again.
        // The "true" recursive version would consume ownership through
        // recursive calls and reassemble — possible but verbose.
        self.reverse_iterative();
    }

    pub fn find_middle(&self) -> Option<i32> {
        // Use raw read-only pointers to do classic two-pointer walking.
        let mut slow: *const Node = match self.head.as_deref() { Some(n) => n, None => return None };
        let mut fast: *const Node = slow;
        unsafe {
            while !fast.is_null() && !(*fast).next.is_none() {
                slow = (*slow).next.as_deref().map(|n| n as *const Node).unwrap_or(std::ptr::null());
                fast = (*fast).next.as_deref().and_then(|n| n.next.as_deref()).map(|n| n as *const Node).unwrap_or(std::ptr::null());
                if fast.is_null() { break; }
            }
            if slow.is_null() { None } else { Some((*slow).data) }
        }
    }

    pub fn has_cycle(&self) -> bool {
        // Cycles can't exist in a safely-built Box list (single ownership!),
        // so this is always false here. We keep the API for parity with Java.
        false
    }

    pub fn to_string(&self) -> String {
        let mut s = String::from("HEAD");
        let mut cur = self.head.as_deref();
        while let Some(n) = cur {
            s.push_str(" -> ");
            s.push_str(&n.data.to_string());
            cur = n.next.as_deref();
        }
        s.push_str(" -> NULL");
        s
    }
}

// Iterative drop to avoid blowing the stack on long lists. A naive recursive
// drop would call ~Box -> ~Node -> ~Box (next) ... O(n) deep.
impl Drop for LinkedList {
    fn drop(&mut self) {
        let mut cur = self.head.take();
        while let Some(mut node) = cur {
            cur = node.next.take();
        }
    }
}

fn main() {
    let mut list = LinkedList::new();
    for v in [1, 2, 3, 4, 5] { list.insert_at_tail(v); }
    println!("{}", list.to_string());

    list.insert_at_head(0);
    println!("{}", list.to_string());

    list.insert_at_index(3, 99);
    println!("{}", list.to_string());

    list.delete_by_value(99);
    println!("{}", list.to_string());

    println!("Size: {}", list.len());
    println!("Contains 3: {}", list.contains(3));
    println!("Contains 9: {}", list.contains(9));

    println!("Middle: {:?}", list.find_middle());

    list.reverse_iterative();
    println!("{}", list.to_string());

    list.reverse_recursive();
    println!("{}", list.to_string());

    println!("Has cycle: {}", list.has_cycle());
}

/*
 * NOTES (vs. Java):
 * - Java references are nullable + GC'd; Rust uses Option<Box<T>> with
 *   single ownership. There's no NullPointerException — only Option::None
 *   which the type system forces you to handle.
 * - Reverse-recursive in Rust is annoying because moving a Box invalidates
 *   the previous owner. We compromise by calling the iterative version.
 * - Cycle detection: cycles are unbuildable in a safe Box-based list
 *   (single owner), so `has_cycle` is trivially false. To experiment with
 *   real cycles you'd need Rc<RefCell<Node>> with Weak back-pointers.
 * - Drop is implemented manually to avoid stack overflow from deeply
 *   recursive default Box destructors.
 * - Allow dead-code lints aren't needed here because all methods are used
 *   in main().
 */
