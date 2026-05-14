/*
 * WEEK 14 - RUST DSA
 * Topic: Binary Search Tree (BST)
 * File: 2.BinarySearchTree.rs
 *
 * CONCEPT:
 *   Standard BST: left < node < right invariant. Search/insert/delete are
 *   O(h). We use Option<Box<Node>> for owned children.
 *
 * KEY POINTS:
 *   - 3 cases for delete: leaf / one child / two children (replace with
 *     inorder successor).
 *   - Validate by passing min/max bounds down.
 *   - LCA: walk down; first split (or match) is the LCA.
 *
 * ALGORITHM / APPROACH: see Java/Python/C++ files.
 *
 * RUST-SPECIFIC NOTES:
 *   - Recursive insert/delete use Option<Box<Node>> in/out so we can
 *     re-link subtrees safely without complicated mutable aliasing.
 *   - We use Option<Box<Node>>::take() during delete to move ownership
 *     out of the slot.
 *   - For sorted_values we collect inorder into a Vec<i32>.
 *
 * DRY RUN:
 *   Insert 5,3,7,1,4,6,8 -> inorder = 1,3,4,5,6,7,8.
 *   Delete 3 (two children): successor 4 -> 1,4,5,6,7,8.
 *   Delete root (5): successor 6 -> 1,4,6,7,8.
 *
 * COMPLEXITY:
 *   insert/search/delete: O(h)
 *   sorted_values: O(n)
 *   lca / kth_smallest: O(h) / O(h+k)
 */

use std::cmp::Ordering;

pub struct Node {
    pub val: i32,
    pub left: Option<Box<Node>>,
    pub right: Option<Box<Node>>,
}

impl Node {
    fn new(v: i32) -> Box<Node> { Box::new(Node { val: v, left: None, right: None }) }
}

pub struct BST {
    pub root: Option<Box<Node>>,
}

impl BST {
    pub fn new() -> Self { BST { root: None } }

    pub fn insert(&mut self, v: i32) {
        Self::insert_rec(&mut self.root, v);
    }

    fn insert_rec(slot: &mut Option<Box<Node>>, v: i32) {
        match slot {
            None => *slot = Some(Node::new(v)),
            Some(n) => match v.cmp(&n.val) {
                Ordering::Less => Self::insert_rec(&mut n.left, v),
                Ordering::Greater => Self::insert_rec(&mut n.right, v),
                Ordering::Equal => {} // ignore duplicate
            },
        }
    }

    pub fn search(&self, v: i32) -> bool {
        let mut cur = self.root.as_deref();
        while let Some(n) = cur {
            match v.cmp(&n.val) {
                Ordering::Equal => return true,
                Ordering::Less => cur = n.left.as_deref(),
                Ordering::Greater => cur = n.right.as_deref(),
            }
        }
        false
    }

    pub fn delete(&mut self, v: i32) {
        let root = self.root.take();
        self.root = Self::delete_rec(root, v);
    }

    fn min_val(node: &Node) -> i32 {
        let mut cur = node;
        while let Some(l) = cur.left.as_deref() { cur = l; }
        cur.val
    }

    fn delete_rec(node: Option<Box<Node>>, v: i32) -> Option<Box<Node>> {
        let mut node = match node {
            None => return None,
            Some(n) => n,
        };
        match v.cmp(&node.val) {
            Ordering::Less => {
                let l = node.left.take();
                node.left = Self::delete_rec(l, v);
                Some(node)
            }
            Ordering::Greater => {
                let r = node.right.take();
                node.right = Self::delete_rec(r, v);
                Some(node)
            }
            Ordering::Equal => {
                // Cases 1, 2, 3
                if node.left.is_none() { return node.right.take(); }
                if node.right.is_none() { return node.left.take(); }
                let succ_val = Self::min_val(node.right.as_deref().unwrap());
                node.val = succ_val;
                let r = node.right.take();
                node.right = Self::delete_rec(r, succ_val);
                Some(node)
            }
        }
    }

    pub fn sorted_values(&self) -> Vec<i32> {
        let mut out = Vec::new();
        fn go(n: Option<&Node>, out: &mut Vec<i32>) {
            if let Some(n) = n {
                go(n.left.as_deref(), out);
                out.push(n.val);
                go(n.right.as_deref(), out);
            }
        }
        go(self.root.as_deref(), &mut out);
        out
    }

    pub fn is_valid_bst(&self) -> bool {
        fn check(n: Option<&Node>, lo: i64, hi: i64) -> bool {
            match n {
                None => true,
                Some(n) => {
                    let v = n.val as i64;
                    if v <= lo || v >= hi { return false; }
                    check(n.left.as_deref(), lo, v) && check(n.right.as_deref(), v, hi)
                }
            }
        }
        check(self.root.as_deref(), i64::MIN, i64::MAX)
    }

    pub fn lca(&self, p: i32, q: i32) -> Option<i32> {
        let mut cur = self.root.as_deref();
        while let Some(n) = cur {
            if p < n.val && q < n.val { cur = n.left.as_deref(); }
            else if p > n.val && q > n.val { cur = n.right.as_deref(); }
            else { return Some(n.val); }
        }
        None
    }

    pub fn kth_smallest(&self, k: i32) -> Option<i32> {
        let mut stack: Vec<&Node> = Vec::new();
        let mut cur = self.root.as_deref();
        let mut cnt = 0;
        while cur.is_some() || !stack.is_empty() {
            while let Some(n) = cur { stack.push(n); cur = n.left.as_deref(); }
            let n = stack.pop().unwrap();
            cnt += 1;
            if cnt == k { return Some(n.val); }
            cur = n.right.as_deref();
        }
        None
    }
}

fn main() {
    let mut bst = BST::new();
    for v in [5, 3, 7, 1, 4, 6, 8] { bst.insert(v); }

    println!("Inserted: 5,3,7,1,4,6,8");
    println!("Inorder (sorted): {:?}", bst.sorted_values());

    println!("Search 4: {}", bst.search(4));
    println!("Search 9: {}", bst.search(9));
    println!("Is valid BST: {}", bst.is_valid_bst());

    println!("LCA(1,4) = {:?}", bst.lca(1, 4));
    println!("LCA(1,8) = {:?}", bst.lca(1, 8));
    println!("LCA(6,8) = {:?}", bst.lca(6, 8));

    println!("2nd smallest: {:?}", bst.kth_smallest(2));
    println!("5th smallest: {:?}", bst.kth_smallest(5));

    bst.delete(3);
    println!("\nAfter deleting 3: {:?}", bst.sorted_values());

    bst.delete(5);
    println!("After deleting root (5): {:?}", bst.sorted_values());
}

/*
 * NOTES (vs. Java):
 * - Java mutates `node.left = ...` directly using object references; in
 *   Rust we move ownership in/out via `Option::take()` and re-store.
 * - i64 bounds replace Java's Long.MIN/MAX_VALUE.
 * - Search/lca/kth use iterative loops to keep the borrow checker happy
 *   (no recursive borrowing).
 */
