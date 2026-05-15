/*
 * WEEK 30 - JAVA ADVANCED TOPICS
 * Topic: Fast & Slow Pointers (Floyd's Tortoise and Hare)
 * File: fast_slow_pointers.java
 *
 * CONCEPT:
 *     Use two pointers traversing the same sequence at different speeds:
 *     slow advances by 1, fast by 2. If a cycle exists they must
 *     eventually coincide. After the meeting, additional walks pinpoint
 *     the cycle entry. The same idea generalises to any deterministic
 *     next-state function (digit-square chain for the Happy Number
 *     problem).
 *
 * KEY POINTS:
 *     - O(n) time, O(1) space -- perfect for "detect a loop without
 *       modifying the structure" or "no extra memory".
 *     - To find the cycle entry: reset one pointer to head, advance both
 *       one step at a time until they meet again.
 *     - Works on linked lists, integer sequences, graphs with deterministic
 *       edges.
 *
 * ALGORITHM / APPROACH:
 *     HAS CYCLE:
 *         slow = fast = head
 *         while fast != null && fast.next != null:
 *             slow = slow.next; fast = fast.next.next
 *             if slow == fast: return true
 *         return false
 *     CYCLE START:
 *         on collision: entry = head; advance entry and slow by 1; meet = entry
 *     HAPPY NUMBER:
 *         slow = n; fast = n
 *         do { slow = step(slow); fast = step(step(fast)); } while slow != fast
 *         return slow == 1
 *     MIDDLE OF LIST:
 *         slow = fast = head
 *         while fast != null && fast.next != null: ...
 *         return slow
 *
 * DRY RUN / EXAMPLE:
 *     List 1 -> 2 -> 3 -> back to 2 (cycle). hasCycle returns true;
 *     detectCycleStart returns the node with value 2.
 *     isHappy(19) -> true; isHappy(2) -> false.
 *
 * COMPLEXITY:
 *     Time:  O(n).
 *     Space: O(1).
 */

// snake_case filename is fine; class FastSlowPointers is package-private.

class FastSlowPointers {

    static class ListNode {
        int val;
        ListNode next;
        ListNode(int v) { val = v; }
        ListNode(int v, ListNode n) { val = v; next = n; }
    }

    /** LC 141 - cycle detection. */
    static boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }

    /** LC 142 - cycle start. */
    static ListNode detectCycleStart(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) {
                ListNode entry = head;
                while (entry != slow) { entry = entry.next; slow = slow.next; }
                return entry;
            }
        }
        return null;
    }

    /** LC 876 - middle of a linked list. */
    static ListNode middleOfList(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;
    }

    private static int digitSquareSum(int n) {
        int s = 0;
        while (n > 0) {
            int d = n % 10;
            s += d * d;
            n /= 10;
        }
        return s;
    }

    /** LC 202 - happy number. */
    static boolean isHappy(int n) {
        int slow = n, fast = n;
        do {
            slow = digitSquareSum(slow);
            fast = digitSquareSum(digitSquareSum(fast));
        } while (slow != fast);
        return slow == 1;
    }

    public static void main(String[] args) {
        // Cyclic list 1 -> 2 -> 3 -> back to 2
        ListNode a = new ListNode(1);
        ListNode b = new ListNode(2);
        ListNode c = new ListNode(3);
        a.next = b; b.next = c; c.next = b;
        System.out.println("hasCycle: " + hasCycle(a));
        ListNode start = detectCycleStart(a);
        System.out.println("Cycle starts at value: " + (start == null ? "null" : start.val));

        // Acyclic 1 -> 2 -> 3 -> 4 -> 5
        ListNode n1 = new ListNode(1, new ListNode(2, new ListNode(3,
                       new ListNode(4, new ListNode(5)))));
        System.out.println("Middle value: " + middleOfList(n1).val);

        System.out.println("isHappy(19): " + isHappy(19));
        System.out.println("isHappy(2):  " + isHappy(2));
    }
}

/*
 * NOTES
 * -----
 * Differences from the Python implementation in fast_slow_pointers.py:
 *   - Java compares node identity with == (Python uses `is`).
 *   - ListNode is a plain inner class with a constructor; Python used a
 *     @dataclass with default None.
 *   - The companion interview_patterns.java covers the same primitives;
 *     this file is a focused stand-alone topic for parity with the splits.
 */
