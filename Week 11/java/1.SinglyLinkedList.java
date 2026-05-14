/*
 * WEEK 11 - LINKED LISTS
 * Topic: Singly Linked List — Complete Implementation
 *
 * STRUCTURE: Node(data, next) — each node points to the next.
 * Last node's next = null (marks the end).
 *
 * ADVANTAGES over arrays:
 * - O(1) insertion/deletion at head (no shifting)
 * - Dynamic size (no pre-allocation needed)
 *
 * DISADVANTAGES:
 * - O(n) access by index (no random access)
 * - Extra memory for 'next' pointer
 * - Poor cache performance (nodes scattered in memory)
 *
 * OPERATIONS:
 * Operation          | Time    | Notes
 * -------------------|---------|-----------------------------
 * insertAtHead       | O(1)    |
 * insertAtTail       | O(n)    | O(1) with tail pointer
 * insertAtIndex      | O(n)    |
 * deleteAtHead       | O(1)    |
 * deleteByValue      | O(n)    |
 * search             | O(n)    |
 * reverseIterative   | O(n)    | O(1) space
 * reverseRecursive   | O(n)    | O(n) space
 * findMiddle         | O(n)    | Floyd's slow/fast pointer
 * hasCycle           | O(n)    | Floyd's algorithm
 */

public class SinglyLinkedList {

    // Node class
    static class Node {
        int data;
        Node next;
        Node(int data) { this.data = data; this.next = null; }
    }

    static class LinkedList {
        Node head;

        // Insert at head — O(1)
        void insertAtHead(int data) {
            Node newNode = new Node(data);
            newNode.next = head;
            head = newNode;
        }

        // Insert at tail — O(n)
        void insertAtTail(int data) {
            Node newNode = new Node(data);
            if (head == null) { head = newNode; return; }
            Node curr = head;
            while (curr.next != null) curr = curr.next;
            curr.next = newNode;
        }

        // Insert at given index (0-indexed) — O(n)
        void insertAtIndex(int idx, int data) {
            if (idx == 0) { insertAtHead(data); return; }
            Node curr = head;
            for (int i = 0; i < idx - 1 && curr != null; i++) curr = curr.next;
            if (curr == null) throw new IndexOutOfBoundsException("Index out of bounds");
            Node newNode = new Node(data);
            newNode.next = curr.next;
            curr.next = newNode;
        }

        // Delete head — O(1)
        void deleteHead() {
            if (head == null) return;
            head = head.next;
        }

        // Delete first occurrence of value — O(n)
        boolean deleteByValue(int val) {
            if (head == null) return false;
            if (head.data == val) { head = head.next; return true; }
            Node curr = head;
            while (curr.next != null) {
                if (curr.next.data == val) { curr.next = curr.next.next; return true; }
                curr = curr.next;
            }
            return false;
        }

        // Search — O(n)
        boolean contains(int val) {
            Node curr = head;
            while (curr != null) {
                if (curr.data == val) return true;
                curr = curr.next;
            }
            return false;
        }

        // Reverse — iterative, O(n) time, O(1) space
        void reverseIterative() {
            Node prev = null, curr = head, next;
            while (curr != null) {
                next = curr.next;
                curr.next = prev;
                prev = curr;
                curr = next;
            }
            head = prev;
        }

        // Reverse — recursive
        Node reverseRec(Node node) {
            if (node == null || node.next == null) return node;
            Node newHead = reverseRec(node.next);
            node.next.next = node;
            node.next = null;
            return newHead;
        }
        void reverseRecursive() { head = reverseRec(head); }

        // Find middle — Floyd's slow/fast pointer
        // slow moves 1 step, fast moves 2 steps → when fast reaches end, slow is at middle
        Node findMiddle() {
            Node slow = head, fast = head;
            while (fast != null && fast.next != null) {
                slow = slow.next;
                fast = fast.next.next;
            }
            return slow; // middle node
        }

        // Detect cycle — Floyd's algorithm
        boolean hasCycle() {
            Node slow = head, fast = head;
            while (fast != null && fast.next != null) {
                slow = slow.next;
                fast = fast.next.next;
                if (slow == fast) return true; // cycle detected
            }
            return false;
        }

        // Length
        int size() {
            int count = 0;
            Node curr = head;
            while (curr != null) { count++; curr = curr.next; }
            return count;
        }

        // Print list
        void print() {
            Node curr = head;
            StringBuilder sb = new StringBuilder("HEAD -> ");
            while (curr != null) {
                sb.append(curr.data);
                if (curr.next != null) sb.append(" -> ");
                curr = curr.next;
            }
            sb.append(" -> NULL");
            System.out.println(sb);
        }
    }

    public static void main(String[] args) {
        LinkedList list = new LinkedList();

        // Build list
        list.insertAtTail(1);
        list.insertAtTail(2);
        list.insertAtTail(3);
        list.insertAtTail(4);
        list.insertAtTail(5);
        list.print(); // HEAD -> 1 -> 2 -> 3 -> 4 -> 5 -> NULL

        list.insertAtHead(0);
        list.print(); // 0 -> 1 -> 2 -> 3 -> 4 -> 5

        list.insertAtIndex(3, 99);
        list.print(); // 0 -> 1 -> 2 -> 99 -> 3 -> 4 -> 5

        list.deleteByValue(99);
        list.print(); // 0 -> 1 -> 2 -> 3 -> 4 -> 5

        System.out.println("Size: " + list.size());
        System.out.println("Contains 3: " + list.contains(3));
        System.out.println("Contains 9: " + list.contains(9));

        // Middle node
        Node mid = list.findMiddle();
        System.out.println("Middle: " + mid.data); // 3

        // Reverse
        list.reverseIterative();
        list.print(); // 5 -> 4 -> 3 -> 2 -> 1 -> 0

        list.reverseRecursive();
        list.print(); // back to 0 -> 1 -> 2 -> 3 -> 4 -> 5

        // Cycle detection
        System.out.println("Has cycle: " + list.hasCycle()); // false
        // Create cycle for testing: tail.next = head
        // (not doing this to avoid infinite loop in print)
    }
}
