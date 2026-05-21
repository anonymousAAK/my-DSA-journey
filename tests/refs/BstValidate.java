/*
 * Reference Java implementation for tests/cases/bst_validate.json.
 *
 * Tree is encoded as a LeetCode-style level-order list with `null` for
 * missing children (passed in as a List<Long> with possible nulls). The
 * driver reconstructs the tree and validates strict BST bounds.
 */
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;

public class BstValidate {
    private static class Node {
        long val;
        Node left, right;
        Node(long v) { this.val = v; }
    }

    private static Node build(List<Long> values) {
        if (values.isEmpty() || values.get(0) == null) return null;
        Node root = new Node(values.get(0));
        Deque<Node> q = new ArrayDeque<>();
        q.offer(root);
        int i = 1;
        while (!q.isEmpty() && i < values.size()) {
            Node node = q.poll();
            if (i < values.size()) {
                Long v = values.get(i++);
                if (v != null) { node.left = new Node(v); q.offer(node.left); }
            }
            if (i < values.size()) {
                Long v = values.get(i++);
                if (v != null) { node.right = new Node(v); q.offer(node.right); }
            }
        }
        return root;
    }

    private static boolean check(Node n, long lo, long hi, boolean hasLo, boolean hasHi) {
        if (n == null) return true;
        if (hasLo && n.val <= lo) return false;
        if (hasHi && n.val >= hi) return false;
        return check(n.left, lo, n.val, hasLo, true)
            && check(n.right, n.val, hi, true, hasHi);
    }

    public static boolean isValidBST(List<Long> values) {
        Node root = build(values);
        return check(root, 0, 0, false, false);
    }
}
