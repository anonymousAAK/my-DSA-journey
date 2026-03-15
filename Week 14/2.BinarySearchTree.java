/*
 * WEEK 14 - TREES
 * Topic: Binary Search Tree (BST)
 *
 * BST PROPERTY: For every node:
 * - All values in LEFT subtree < node.val
 * - All values in RIGHT subtree > node.val
 *
 * This property makes search, insert, delete all O(h) where h = height.
 * - Balanced BST: h = O(log n) → O(log n) operations
 * - Unbalanced BST: h = O(n) → O(n) operations (degenerates to linked list)
 *
 * OPERATIONS:
 * - Search:  Compare and go left/right
 * - Insert:  Search for correct position, add new leaf
 * - Delete:  Three cases:
 *   1. Leaf node: just remove
 *   2. One child: replace with child
 *   3. Two children: replace with inorder successor (smallest in right subtree)
 *
 * VALIDATION: A tree is a valid BST if inorder traversal is strictly increasing.
 *
 * LCA (Lowest Common Ancestor) in BST:
 * - If both p,q < root: LCA is in left subtree
 * - If both p,q > root: LCA is in right subtree
 * - Otherwise: root is the LCA
 * Time: O(h)
 */

public class BinarySearchTree {

    static class Node {
        int val;
        Node left, right;
        Node(int val) { this.val = val; }
    }

    static class BST {
        Node root;

        // Insert — O(h)
        Node insert(Node node, int val) {
            if (node == null) return new Node(val);
            if (val < node.val) node.left = insert(node.left, val);
            else if (val > node.val) node.right = insert(node.right, val);
            // val == node.val: duplicate, do nothing (or handle as needed)
            return node;
        }
        void insert(int val) { root = insert(root, val); }

        // Search — O(h)
        boolean search(Node node, int val) {
            if (node == null) return false;
            if (val == node.val) return true;
            return val < node.val ? search(node.left, val) : search(node.right, val);
        }
        boolean search(int val) { return search(root, val); }

        // Minimum value (leftmost node)
        Node minNode(Node node) {
            while (node.left != null) node = node.left;
            return node;
        }

        // Delete — O(h)
        Node delete(Node node, int val) {
            if (node == null) return null;
            if (val < node.val) {
                node.left = delete(node.left, val);
            } else if (val > node.val) {
                node.right = delete(node.right, val);
            } else {
                // Found the node to delete
                if (node.left == null) return node.right;   // case 1 & 2
                if (node.right == null) return node.left;   // case 2
                // Case 3: two children — replace with inorder successor
                Node successor = minNode(node.right);
                node.val = successor.val;
                node.right = delete(node.right, successor.val);
            }
            return node;
        }
        void delete(int val) { root = delete(root, val); }

        // Inorder traversal (gives sorted order)
        void inorderPrint(Node node) {
            if (node == null) return;
            inorderPrint(node.left);
            System.out.print(node.val + " ");
            inorderPrint(node.right);
        }
        void printSorted() { inorderPrint(root); System.out.println(); }

        // Validate BST — check that inorder traversal is strictly increasing
        // More efficient: pass min/max bounds down
        boolean isValidBST(Node node, long min, long max) {
            if (node == null) return true;
            if (node.val <= min || node.val >= max) return false;
            return isValidBST(node.left, min, node.val)
                && isValidBST(node.right, node.val, max);
        }
        boolean isValidBST() { return isValidBST(root, Long.MIN_VALUE, Long.MAX_VALUE); }

        // LCA in BST — O(h)
        Node lca(Node node, int p, int q) {
            if (node == null) return null;
            if (p < node.val && q < node.val) return lca(node.left, p, q);
            if (p > node.val && q > node.val) return lca(node.right, p, q);
            return node; // split point — this is the LCA
        }
        int lca(int p, int q) {
            Node result = lca(root, p, q);
            return result != null ? result.val : -1;
        }

        // Kth smallest element (inorder traversal, stop at kth)
        int kthSmallest(int k) {
            int[] count = {0};
            int[] result = {-1};
            kthHelper(root, k, count, result);
            return result[0];
        }
        void kthHelper(Node node, int k, int[] count, int[] result) {
            if (node == null) return;
            kthHelper(node.left, k, count, result);
            count[0]++;
            if (count[0] == k) { result[0] = node.val; return; }
            kthHelper(node.right, k, count, result);
        }
    }

    public static void main(String[] args) {
        BST bst = new BST();
        int[] vals = {5, 3, 7, 1, 4, 6, 8};
        for (int v : vals) bst.insert(v);

        System.out.println("Inserted: 5, 3, 7, 1, 4, 6, 8");
        System.out.print("Inorder (sorted): ");
        bst.printSorted(); // 1 3 4 5 6 7 8

        System.out.println("Search 4: " + bst.search(4)); // true
        System.out.println("Search 9: " + bst.search(9)); // false
        System.out.println("Is valid BST: " + bst.isValidBST()); // true

        System.out.println("LCA(1, 4) = " + bst.lca(1, 4)); // 3
        System.out.println("LCA(1, 8) = " + bst.lca(1, 8)); // 5
        System.out.println("LCA(6, 8) = " + bst.lca(6, 8)); // 7

        System.out.println("2nd smallest: " + bst.kthSmallest(2)); // 3
        System.out.println("5th smallest: " + bst.kthSmallest(5)); // 6

        // Delete
        bst.delete(3);
        System.out.print("\nAfter deleting 3: ");
        bst.printSorted(); // 1 4 5 6 7 8

        bst.delete(5); // root deletion
        System.out.print("After deleting root (5): ");
        bst.printSorted(); // 1 4 6 7 8
    }
}
