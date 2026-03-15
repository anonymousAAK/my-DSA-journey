//! # Week 14: Trees
//!
//! This module covers binary tree and binary search tree (BST) implementations in Rust.
//! Topics include:
//! - TreeNode using `Option<Box<TreeNode>>`
//! - Binary tree traversals: inorder, preorder, postorder (recursive), level_order (BFS)
//! - Tree properties: height, node_count
//! - BST operations: insert, search, is_valid_bst
//!
//! ## Rust-Specific Notes for DSA Learners
//!
//! ### Ownership and Trees
//! Trees are one of Rust's most instructive challenges. Here's why and what choices
//! we make:
//!
//! **`Option<Box<TreeNode>>` (Single Ownership)**
//! - Each node OWNS its children via `Box` (heap-allocated, single owner).
//! - `Option` represents "child exists or doesn't" — Rust's null-safe alternative.
//! - This works well for trees where each node has exactly one parent.
//! - Limitation: you can't have multiple references to the same node (e.g., parent
//!   pointers, or iterating while modifying).
//!
//! **When would you need `Rc<RefCell<TreeNode>>`?**
//! - When multiple parts of code need to read/write the same node (e.g., parent pointers,
//!   LCA with parent references, or graph-like tree operations).
//! - `Rc` = reference-counted pointer (shared ownership), `RefCell` = interior mutability
//!   (runtime borrow checking instead of compile-time).
//! - We avoid this here to keep the code approachable, but note it in comments.
//!
//! **Pattern: Recursive functions take `&Option<Box<TreeNode>>`**
//! - This borrows the optional child without taking ownership.
//! - For modification (insert), we take `Option<Box<TreeNode>>` by value and return
//!   the modified tree — a functional "rebuild" pattern that satisfies the borrow checker.

use std::collections::VecDeque;

// ===========================================================================
// TreeNode Definition
// ===========================================================================

/// A node in a binary tree.
///
/// Children are `Option<Box<TreeNode>>`:
/// - `None` = no child (leaf edge)
/// - `Some(Box<TreeNode>)` = child exists, owned by this node
#[derive(Debug, PartialEq)]
struct TreeNode {
    val: i32,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

impl TreeNode {
    /// Creates a new leaf node (no children).
    fn new(val: i32) -> Self {
        TreeNode {
            val,
            left: None,
            right: None,
        }
    }

    /// Creates a new leaf node wrapped in `Some(Box<...>)` — convenient for building trees.
    fn boxed(val: i32) -> Option<Box<Self>> {
        Some(Box::new(Self::new(val)))
    }

    /// Creates a node with specified children.
    fn with_children(
        val: i32,
        left: Option<Box<TreeNode>>,
        right: Option<Box<TreeNode>>,
    ) -> Option<Box<Self>> {
        Some(Box::new(TreeNode { val, left, right }))
    }
}

// ===========================================================================
// Binary Tree Traversals (Recursive)
// ===========================================================================

/// Inorder traversal: Left -> Root -> Right.
///
/// For a BST, inorder traversal produces elements in sorted order.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) call stack + O(n) for the result vector, where h = height
fn inorder(node: &Option<Box<TreeNode>>) -> Vec<i32> {
    match node {
        None => vec![],
        Some(n) => {
            let mut result = inorder(&n.left);
            result.push(n.val);
            result.extend(inorder(&n.right));
            result
        }
    }
}

/// Preorder traversal: Root -> Left -> Right.
///
/// Useful for serializing/copying a tree structure.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) call stack + O(n) for the result vector
fn preorder(node: &Option<Box<TreeNode>>) -> Vec<i32> {
    match node {
        None => vec![],
        Some(n) => {
            let mut result = vec![n.val];
            result.extend(preorder(&n.left));
            result.extend(preorder(&n.right));
            result
        }
    }
}

/// Postorder traversal: Left -> Right -> Root.
///
/// Useful for deletion or evaluating expression trees.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) call stack + O(n) for the result vector
fn postorder(node: &Option<Box<TreeNode>>) -> Vec<i32> {
    match node {
        None => vec![],
        Some(n) => {
            let mut result = postorder(&n.left);
            result.extend(postorder(&n.right));
            result.push(n.val);
            result
        }
    }
}

// ===========================================================================
// Level-Order Traversal (BFS)
// ===========================================================================

/// Level-order (breadth-first) traversal using a queue (`VecDeque`).
///
/// Returns elements grouped by level: `Vec<Vec<i32>>`.
///
/// ## Rust Ownership Note
/// We store `&Box<TreeNode>` references in the queue. The `ref` keyword in
/// `if let Some(ref node) = ...` creates a reference without moving ownership.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(w) where w = maximum width of the tree (queue size)
fn level_order(root: &Option<Box<TreeNode>>) -> Vec<Vec<i32>> {
    let mut result: Vec<Vec<i32>> = Vec::new();

    if root.is_none() {
        return result;
    }

    let mut queue: VecDeque<&Box<TreeNode>> = VecDeque::new();
    if let Some(ref node) = root {
        queue.push_back(node);
    }

    while !queue.is_empty() {
        let level_size = queue.len();
        let mut level: Vec<i32> = Vec::with_capacity(level_size);

        for _ in 0..level_size {
            let node = queue.pop_front().unwrap();
            level.push(node.val);

            if let Some(ref left) = node.left {
                queue.push_back(left);
            }
            if let Some(ref right) = node.right {
                queue.push_back(right);
            }
        }

        result.push(level);
    }

    result
}

// ===========================================================================
// Tree Properties
// ===========================================================================

/// Computes the height of a binary tree.
///
/// Height = number of edges on the longest path from root to leaf.
/// Convention: empty tree has height 0, single node has height 1.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) — call-stack depth
fn height(node: &Option<Box<TreeNode>>) -> i32 {
    match node {
        None => 0,
        Some(n) => 1 + height(&n.left).max(height(&n.right)),
    }
}

/// Counts the total number of nodes in a binary tree.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) — call-stack depth
fn node_count(node: &Option<Box<TreeNode>>) -> i32 {
    match node {
        None => 0,
        Some(n) => 1 + node_count(&n.left) + node_count(&n.right),
    }
}

/// Computes the diameter of a binary tree.
///
/// The diameter is the number of nodes on the longest path between any two nodes.
/// This path may or may not pass through the root.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) — call-stack depth
fn diameter(node: &Option<Box<TreeNode>>) -> i32 {
    fn helper(node: &Option<Box<TreeNode>>, max_diameter: &mut i32) -> i32 {
        match node {
            None => 0,
            Some(n) => {
                let left_height = helper(&n.left, max_diameter);
                let right_height = helper(&n.right, max_diameter);
                // Diameter through this node = left_height + right_height.
                *max_diameter = (*max_diameter).max(left_height + right_height);
                1 + left_height.max(right_height)
            }
        }
    }

    let mut max_d = 0;
    helper(node, &mut max_d);
    max_d
}

// ===========================================================================
// BST Operations
// ===========================================================================

/// Inserts a value into a BST, returning the (possibly new) root.
///
/// ## Rust Ownership Pattern: "Take and Return"
/// We take `node` by value (`Option<Box<TreeNode>>`) and return the modified tree.
/// This pattern works with Rust's ownership model:
/// - `None` -> create a new node.
/// - `Some(mut n)` -> we now own `n`, modify it, and return `Some(n)`.
///
/// In languages with mutable references (Java, Python), you'd just mutate in place.
/// In Rust, this functional rebuild pattern is the idiomatic approach for
/// `Option<Box<T>>` trees.
///
/// # Complexity
/// - Time:  O(h) where h = height (O(log n) for balanced, O(n) for skewed)
/// - Space: O(h) — call-stack depth
fn bst_insert(node: Option<Box<TreeNode>>, val: i32) -> Option<Box<TreeNode>> {
    match node {
        None => TreeNode::boxed(val),
        Some(mut n) => {
            if val < n.val {
                n.left = bst_insert(n.left, val);
            } else if val > n.val {
                n.right = bst_insert(n.right, val);
            }
            // If val == n.val, we skip (no duplicates in this BST).
            Some(n)
        }
    }
}

/// Searches for a value in a BST.
///
/// Returns `true` if found.
///
/// # Complexity
/// - Time:  O(h)
/// - Space: O(h) — call-stack depth (could be O(1) iteratively)
fn bst_search(node: &Option<Box<TreeNode>>, val: i32) -> bool {
    match node {
        None => false,
        Some(n) => {
            // Pattern matching with comparison — idiomatic Rust.
            match val.cmp(&n.val) {
                std::cmp::Ordering::Equal => true,
                std::cmp::Ordering::Less => bst_search(&n.left, val),
                std::cmp::Ordering::Greater => bst_search(&n.right, val),
            }
        }
    }
}

/// Validates whether a binary tree is a valid BST.
///
/// A valid BST requires that for every node:
/// - All values in the left subtree are strictly less than the node's value.
/// - All values in the right subtree are strictly greater than the node's value.
///
/// We use `i64` bounds to handle `i32::MIN` and `i32::MAX` edge cases.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) — call-stack depth
fn is_valid_bst(node: &Option<Box<TreeNode>>, min: i64, max: i64) -> bool {
    match node {
        None => true,
        Some(n) => {
            let val = n.val as i64;
            if val <= min || val >= max {
                return false;
            }
            is_valid_bst(&n.left, min, val) && is_valid_bst(&n.right, val, max)
        }
    }
}

/// Alternative BST validation using inorder traversal.
///
/// A valid BST's inorder traversal produces a strictly increasing sequence.
/// We track the previous value using `Option<i32>`.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(h) — call-stack depth
fn is_valid_bst_inorder(node: &Option<Box<TreeNode>>, prev: &mut Option<i32>) -> bool {
    match node {
        None => true,
        Some(n) => {
            // Check left subtree.
            if !is_valid_bst_inorder(&n.left, prev) {
                return false;
            }
            // Check current node against previous inorder value.
            if let Some(p) = prev {
                if n.val <= *p {
                    return false;
                }
            }
            *prev = Some(n.val);
            // Check right subtree.
            is_valid_bst_inorder(&n.right, prev)
        }
    }
}

/// Finds the minimum value in a BST (leftmost node).
///
/// # Complexity
/// - Time:  O(h)
/// - Space: O(1) — iterative
fn bst_min(node: &Option<Box<TreeNode>>) -> Option<i32> {
    let mut current = node;
    let mut min_val = None;
    while let Some(n) = current {
        min_val = Some(n.val);
        current = &n.left;
    }
    min_val
}

/// Finds the maximum value in a BST (rightmost node).
///
/// # Complexity
/// - Time:  O(h)
/// - Space: O(1) — iterative
fn bst_max(node: &Option<Box<TreeNode>>) -> Option<i32> {
    let mut current = node;
    let mut max_val = None;
    while let Some(n) = current {
        max_val = Some(n.val);
        current = &n.right;
    }
    max_val
}

// ===========================================================================
// Helper: Build a sample tree for testing
// ===========================================================================

/// Builds this tree:
/// ```text
///        1
///       / \
///      2   3
///     / \   \
///    4   5   6
/// ```
fn build_sample_tree() -> Option<Box<TreeNode>> {
    TreeNode::with_children(
        1,
        TreeNode::with_children(
            2,
            TreeNode::boxed(4),
            TreeNode::boxed(5),
        ),
        TreeNode::with_children(
            3,
            None,
            TreeNode::boxed(6),
        ),
    )
}

/// Pretty-prints a binary tree (rotated 90 degrees — right subtree on top).
fn print_tree(node: &Option<Box<TreeNode>>, prefix: &str, is_left: bool) {
    if let Some(n) = node {
        print_tree(&n.right, &format!("{}{}   ", prefix, if is_left { "|" } else { " " }), false);
        println!(
            "{}{}── {}",
            prefix,
            if is_left { "└" } else { "┌" },
            n.val
        );
        print_tree(&n.left, &format!("{}{}   ", prefix, if is_left { " " } else { "|" }), true);
    }
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 14: Trees ===\n");

    // --- Build and display sample tree ---
    println!("--- Sample Binary Tree ---");
    let tree = build_sample_tree();
    println!("Tree structure (rotated, right subtree on top):");
    print_tree(&tree, "", false);

    // --- Traversals ---
    println!("\n--- Traversals ---");
    let in_result = inorder(&tree);
    let pre_result = preorder(&tree);
    let post_result = postorder(&tree);
    let level_result = level_order(&tree);

    assert_eq!(in_result, vec![4, 2, 5, 1, 3, 6]);
    assert_eq!(pre_result, vec![1, 2, 4, 5, 3, 6]);
    assert_eq!(post_result, vec![4, 5, 2, 6, 3, 1]);
    assert_eq!(level_result, vec![vec![1], vec![2, 3], vec![4, 5, 6]]);

    println!("Inorder   (L-Root-R): {:?}", in_result);
    println!("Preorder  (Root-L-R): {:?}", pre_result);
    println!("Postorder (L-R-Root): {:?}", post_result);
    println!("Level-order (BFS):    {:?}", level_result);

    // --- Height and Node Count ---
    println!("\n--- Tree Properties ---");
    assert_eq!(height(&tree), 3);
    assert_eq!(node_count(&tree), 6);
    assert_eq!(diameter(&tree), 4); // Path: 4 -> 2 -> 1 -> 3 -> 6
    println!("Height:     {}", height(&tree));
    println!("Node count: {}", node_count(&tree));
    println!("Diameter:   {}", diameter(&tree));

    // Empty tree
    let empty: Option<Box<TreeNode>> = None;
    assert_eq!(height(&empty), 0);
    assert_eq!(node_count(&empty), 0);
    assert_eq!(inorder(&empty), Vec::<i32>::new());

    // Single node
    let single = TreeNode::boxed(42);
    assert_eq!(height(&single), 1);
    assert_eq!(node_count(&single), 1);
    assert_eq!(level_order(&single), vec![vec![42]]);

    // --- BST Construction and Operations ---
    println!("\n--- Binary Search Tree ---");
    let values = vec![5, 3, 7, 1, 4, 6, 8, 2];
    let mut bst: Option<Box<TreeNode>> = None;
    for &v in &values {
        bst = bst_insert(bst, v);
    }

    println!("BST built from {:?}:", values);
    print_tree(&bst, "", false);

    // Inorder of a BST should be sorted.
    let bst_inorder = inorder(&bst);
    assert_eq!(bst_inorder, vec![1, 2, 3, 4, 5, 6, 7, 8]);
    println!("BST inorder (sorted): {:?}", bst_inorder);

    // Search
    assert!(bst_search(&bst, 4));
    assert!(bst_search(&bst, 8));
    assert!(!bst_search(&bst, 9));
    assert!(!bst_search(&bst, 0));
    println!("search(4) = {}, search(9) = {}", bst_search(&bst, 4), bst_search(&bst, 9));

    // Min and Max
    assert_eq!(bst_min(&bst), Some(1));
    assert_eq!(bst_max(&bst), Some(8));
    println!("BST min = {:?}, max = {:?}", bst_min(&bst), bst_max(&bst));

    // Validation
    assert!(is_valid_bst(&bst, i64::MIN, i64::MAX));
    let mut prev = None;
    assert!(is_valid_bst_inorder(&bst, &mut prev));
    println!("is_valid_bst = true");

    // Test with an invalid BST: manually construct one.
    //     5
    //    / \
    //   3   4   <-- 4 < 5 but is in the right subtree! Invalid.
    let invalid_bst = TreeNode::with_children(
        5,
        TreeNode::boxed(3),
        TreeNode::boxed(4), // Invalid: right child < root
    );
    assert!(!is_valid_bst(&invalid_bst, i64::MIN, i64::MAX));
    let mut prev2 = None;
    assert!(!is_valid_bst_inorder(&invalid_bst, &mut prev2));
    println!("Invalid BST [5, left=3, right=4]: is_valid_bst = false");

    // Test BST with duplicate insert (should be ignored)
    let mut bst2 = TreeNode::boxed(10);
    bst2 = bst_insert(bst2, 5);
    bst2 = bst_insert(bst2, 15);
    bst2 = bst_insert(bst2, 5); // Duplicate — should be ignored
    assert_eq!(node_count(&bst2), 3);
    println!("BST with duplicate insert: node_count = {} (duplicate ignored)", node_count(&bst2));

    // Level order of BST
    let bst_levels = level_order(&bst);
    println!("BST level-order: {:?}", bst_levels);
    assert_eq!(bst_levels[0], vec![5]); // Root

    println!("\nAll assertions passed!");
}
