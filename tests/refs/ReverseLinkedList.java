/*
 * Reference Java implementation for tests/cases/reverse_linked_list.json.
 * Builds a singly linked list from values, reverses iteratively, and
 * serialises back to an array.
 */
public class ReverseLinkedList {
    private static class Node {
        long val;
        Node next;
        Node(long v, Node n) { this.val = v; this.next = n; }
    }

    public static long[] reverseList(long[] vals) {
        Node head = null;
        for (int i = vals.length - 1; i >= 0; --i) {
            head = new Node(vals[i], head);
        }
        Node prev = null, curr = head;
        while (curr != null) {
            Node nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        long[] out = new long[vals.length];
        int i = 0;
        for (Node n = prev; n != null; n = n.next) out[i++] = n.val;
        return out;
    }
}
