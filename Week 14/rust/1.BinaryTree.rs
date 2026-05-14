/*
 * WEEK 14 - RUST DSA
 * Topic: Binary Tree - Structure, Traversals, Properties
 * File: 1.BinaryTree.rs
 *
 * CONCEPT:
 *   Hierarchical structure; each node has left/right children. We use
 *   Option<Box<Node>> for owned children — same pattern as the Week 11
 *   linked list, just two children per node.
 *
 * KEY POINTS:
 *   - Traversals: inorder/preorder/postorder/level-order.
 *   - Iterative inorder uses an explicit stack of borrowed references.
 *   - Diameter computed in one DFS using a single scratch variable.
 *
 * ALGORITHM / APPROACH:
 *   Same as Java/Python/C++ versions.
 *
 * RUST-SPECIFIC NOTES:
 *   - Box<Node> gives single ownership; iterators borrow non-mutably so we
 *     can do DFS without borrow-checker fights.
 *   - Iterative inorder needs `&Node` references on a stack; lifetimes work
 *     out because the tree itself outlives the traversal.
 *   - Mirror is in-place; we use std::mem::swap for child pointers.
 *
 * DRY RUN:
 *   Sample tree (1 root, 2/3 children, 4/5/6/7 grandchildren):
 *     Inorder    -> 4 2 5 1 6 3 7
 *     Preorder   -> 1 2 4 5 3 6 7
 *     Postorder  -> 4 5 2 6 7 3 1
 *     Level-order-> [[1],[2,3],[4,5,6,7]]
 *     Height = 3, Count = 7, Diameter = 4.
 *
 * COMPLEXITY:
 *   All traversals O(n) time, O(h) recursion stack.
 */

use std::collections::VecDeque;

pub struct Node {
    pub val: i32,
    pub left: Option<Box<Node>>,
    pub right: Option<Box<Node>>,
}

impl Node {
    pub fn new(v: i32) -> Box<Node> { Box::new(Node { val: v, left: None, right: None }) }
}

pub fn build_sample_tree() -> Box<Node> {
    let mut r = Node::new(1);
    let mut l = Node::new(2);
    let mut rr = Node::new(3);
    l.left  = Some(Node::new(4));
    l.right = Some(Node::new(5));
    rr.left  = Some(Node::new(6));
    rr.right = Some(Node::new(7));
    r.left  = Some(l);
    r.right = Some(rr);
    r
}

pub fn inorder(root: &Node, out: &mut Vec<i32>) {
    if let Some(l) = &root.left { inorder(l, out); }
    out.push(root.val);
    if let Some(r) = &root.right { inorder(r, out); }
}

pub fn preorder(root: &Node, out: &mut Vec<i32>) {
    out.push(root.val);
    if let Some(l) = &root.left { preorder(l, out); }
    if let Some(r) = &root.right { preorder(r, out); }
}

pub fn postorder(root: &Node, out: &mut Vec<i32>) {
    if let Some(l) = &root.left { postorder(l, out); }
    if let Some(r) = &root.right { postorder(r, out); }
    out.push(root.val);
}

pub fn level_order(root: &Node) -> Vec<Vec<i32>> {
    let mut out: Vec<Vec<i32>> = Vec::new();
    let mut q: VecDeque<&Node> = VecDeque::new();
    q.push_back(root);
    while !q.is_empty() {
        let n = q.len();
        let mut level = Vec::with_capacity(n);
        for _ in 0..n {
            let cur = q.pop_front().unwrap();
            level.push(cur.val);
            if let Some(l) = &cur.left  { q.push_back(l); }
            if let Some(r) = &cur.right { q.push_back(r); }
        }
        out.push(level);
    }
    out
}

pub fn inorder_iterative(root: &Node) -> Vec<i32> {
    let mut out = Vec::new();
    let mut stack: Vec<&Node> = Vec::new();
    let mut curr: Option<&Node> = Some(root);
    while curr.is_some() || !stack.is_empty() {
        while let Some(n) = curr {
            stack.push(n);
            curr = n.left.as_deref();
        }
        let n = stack.pop().unwrap();
        out.push(n.val);
        curr = n.right.as_deref();
    }
    out
}

pub fn height(root: Option<&Node>) -> i32 {
    match root {
        None => 0,
        Some(n) => 1 + height(n.left.as_deref()).max(height(n.right.as_deref())),
    }
}

pub fn count_nodes(root: Option<&Node>) -> i32 {
    match root {
        None => 0,
        Some(n) => 1 + count_nodes(n.left.as_deref()) + count_nodes(n.right.as_deref()),
    }
}

pub fn diameter(root: &Node) -> i32 {
    fn go(n: &Node, best: &mut i32) -> i32 {
        let l = if let Some(c) = &n.left  { go(c, best) } else { 0 };
        let r = if let Some(c) = &n.right { go(c, best) } else { 0 };
        if l + r > *best { *best = l + r; }
        1 + l.max(r)
    }
    let mut best = 0;
    go(root, &mut best);
    best
}

pub fn mirror(root: &mut Node) {
    std::mem::swap(&mut root.left, &mut root.right);
    if let Some(l) = root.left.as_deref_mut()  { mirror(l); }
    if let Some(r) = root.right.as_deref_mut() { mirror(r); }
}

fn main() {
    let mut root = build_sample_tree();

    let mut v = Vec::new(); inorder(&root, &mut v);
    println!("Inorder:     {:?}", v);
    let mut v = Vec::new(); preorder(&root, &mut v);
    println!("Preorder:    {:?}", v);
    let mut v = Vec::new(); postorder(&root, &mut v);
    println!("Postorder:   {:?}", v);
    println!("Level-order: {:?}", level_order(&root));
    println!("Inorder it:  {:?}", inorder_iterative(&root));

    println!("\nHeight:    {}", height(Some(&root)));
    println!("Node count:{}", count_nodes(Some(&root)));
    println!("Diameter:  {}", diameter(&root));

    mirror(&mut root);
    let mut v = Vec::new(); inorder(&root, &mut v);
    println!("\nAfter mirror:");
    println!("Inorder: {:?}", v);
}

/*
 * NOTES (vs. Java):
 * - Box<Node> models exclusive ownership. Java references are like Rust's
 *   Rc<Node> conceptually (shared, GC'd) — we don't need that here.
 * - Iterative inorder borrows the tree non-mutably; lifetimes elide cleanly
 *   because the tree (`root`) lives for the duration of the call.
 * - mirror() takes &mut Node — Rust's borrow checker forbids us from
 *   accidentally reading the tree elsewhere while mirroring.
 * - diameter uses a captured `&mut i32` closure variable to track the max.
 */
