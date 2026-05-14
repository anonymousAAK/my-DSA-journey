/*
 * WEEK 14 - TREES
 * Topic: Binary Tree — Structure, Traversals, Properties
 *
 * TREE: A hierarchical data structure.
 * BINARY TREE: Each node has at most 2 children (left, right).
 *
 * TERMINOLOGY:
 * - Root: top node (no parent)
 * - Leaf: node with no children
 * - Height: longest path from root to leaf
 * - Depth of node: distance from root
 * - Level = Depth + 1
 *
 * TRAVERSALS:
 * - Inorder   (L → Root → R): gives sorted order for BST
 * - Preorder  (Root → L → R): used for tree serialization/copying
 * - Postorder (L → R → Root): used for tree deletion
 * - Level-order (BFS): level by level
 *
 * PROPERTIES:
 * - Height:   O(log n) for balanced, O(n) for skewed
 * - Diameter: longest path between any two nodes
 *
 * All traversals: Time O(n), Space O(h) recursion stack
 * Level-order: Time O(n), Space O(w) where w = max width
 */

import java.util.*;

public class BinaryTree {

    static class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    // --- BUILD TREE (for testing) ---
    //         1
    //       /   \
    //      2     3
    //     / \   / \
    //    4   5 6   7
    static Node buildSampleTree() {
        Node root = new Node(1);
        root.left = new Node(2);
        root.right = new Node(3);
        root.left.left = new Node(4);
        root.left.right = new Node(5);
        root.right.left = new Node(6);
        root.right.right = new Node(7);
        return root;
    }

    // --- TRAVERSALS ---

    static List<Integer> inorder(Node root) {
        List<Integer> result = new ArrayList<>();
        inorderHelper(root, result);
        return result;
    }
    static void inorderHelper(Node node, List<Integer> result) {
        if (node == null) return;
        inorderHelper(node.left, result);
        result.add(node.val);
        inorderHelper(node.right, result);
    }

    static List<Integer> preorder(Node root) {
        List<Integer> result = new ArrayList<>();
        preorderHelper(root, result);
        return result;
    }
    static void preorderHelper(Node node, List<Integer> result) {
        if (node == null) return;
        result.add(node.val);
        preorderHelper(node.left, result);
        preorderHelper(node.right, result);
    }

    static List<Integer> postorder(Node root) {
        List<Integer> result = new ArrayList<>();
        postorderHelper(root, result);
        return result;
    }
    static void postorderHelper(Node node, List<Integer> result) {
        if (node == null) return;
        postorderHelper(node.left, result);
        postorderHelper(node.right, result);
        result.add(node.val);
    }

    // Level-order (BFS)
    static List<List<Integer>> levelOrder(Node root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        Queue<Node> queue = new LinkedList<>();
        queue.offer(root);
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> level = new ArrayList<>();
            for (int i = 0; i < levelSize; i++) {
                Node node = queue.poll();
                level.add(node.val);
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            result.add(level);
        }
        return result;
    }

    // Iterative inorder (useful when recursion depth is large)
    static List<Integer> inorderIterative(Node root) {
        List<Integer> result = new ArrayList<>();
        Deque<Node> stack = new ArrayDeque<>();
        Node curr = root;
        while (curr != null || !stack.isEmpty()) {
            while (curr != null) { stack.push(curr); curr = curr.left; }
            curr = stack.pop();
            result.add(curr.val);
            curr = curr.right;
        }
        return result;
    }

    // --- PROPERTIES ---

    static int height(Node root) {
        if (root == null) return 0;
        return 1 + Math.max(height(root.left), height(root.right));
    }

    static int countNodes(Node root) {
        if (root == null) return 0;
        return 1 + countNodes(root.left) + countNodes(root.right);
    }

    // Diameter: longest path between any two nodes (may not pass through root)
    static int diameterResult = 0;
    static int diameterHelper(Node root) {
        if (root == null) return 0;
        int leftH = diameterHelper(root.left);
        int rightH = diameterHelper(root.right);
        diameterResult = Math.max(diameterResult, leftH + rightH);
        return 1 + Math.max(leftH, rightH);
    }
    static int diameter(Node root) {
        diameterResult = 0;
        diameterHelper(root);
        return diameterResult;
    }

    // Mirror of a tree (in-place)
    static void mirror(Node root) {
        if (root == null) return;
        Node temp = root.left; root.left = root.right; root.right = temp;
        mirror(root.left);
        mirror(root.right);
    }

    public static void main(String[] args) {
        Node root = buildSampleTree();

        System.out.println("Inorder:     " + inorder(root));         // 4,2,5,1,6,3,7
        System.out.println("Preorder:    " + preorder(root));        // 1,2,4,5,3,6,7
        System.out.println("Postorder:   " + postorder(root));       // 4,5,2,6,7,3,1
        System.out.println("Level-order: " + levelOrder(root));      // [[1],[2,3],[4,5,6,7]]
        System.out.println("Inorder (iterative): " + inorderIterative(root));

        System.out.println("\nHeight:      " + height(root));        // 3
        System.out.println("Node count:  " + countNodes(root));     // 7
        System.out.println("Diameter:    " + diameter(root));       // 4 (4-2-1-3-7 or similar)

        mirror(root);
        System.out.println("\nAfter mirror:");
        System.out.println("Inorder: " + inorder(root));            // 7,3,6,1,5,2,4
    }
}
