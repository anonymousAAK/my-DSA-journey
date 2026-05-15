/*
 * WEEK 30 - C++ ADVANCED TOPICS
 * Topic: Fast & Slow Pointers (Floyd's Tortoise and Hare)
 * File: fast_slow_pointers.cpp
 *
 * CONCEPT:
 *   Two pointers move at speeds 1 and 2. If there is a cycle they collide;
 *   after collision, walking from head and the meeting point at speed 1
 *   meets at the cycle entry. Same idea works for any deterministic
 *   next-state function (Happy Number).
 *
 * KEY POINTS:
 *   - O(n) time, O(1) space.
 *   - Used in linked-list cycle detection, finding middle node, and
 *     deterministic integer sequences.
 *
 * ALGORITHM / APPROACH:
 *   HAS CYCLE / DETECT START:
 *     slow=fast=head; advance until they meet
 *     reset entry=head; walk both 1-step until they meet again -> start
 *   MIDDLE:
 *     when fast hits end, slow is at the middle
 *   HAPPY NUMBER:
 *     same trick on digit-square successor function
 *
 * C++-SPECIFIC NOTES:
 *   - Owning ListNode pointers; we leak in the demo for brevity.
 *
 * DRY RUN / EXAMPLE:
 *   1 -> 2 -> 3 -> back to 2: hasCycle=true, start=node(2).
 *   isHappy(19)=true, isHappy(2)=false.
 *
 * COMPLEXITY:
 *   Time O(n); Space O(1).
 */

#include <iostream>
using namespace std;

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v) : val(v), next(nullptr) {}
};

bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

ListNode* detectCycleStart(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* entry = head;
            while (entry != slow) { entry = entry->next; slow = slow->next; }
            return entry;
        }
    }
    return nullptr;
}

ListNode* middleOfList(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) { slow = slow->next; fast = fast->next->next; }
    return slow;
}

int digitSquareSum(int n) {
    int s = 0;
    while (n > 0) { int d = n % 10; s += d*d; n /= 10; }
    return s;
}

bool isHappy(int n) {
    int slow = n, fast = n;
    do {
        slow = digitSquareSum(slow);
        fast = digitSquareSum(digitSquareSum(fast));
    } while (slow != fast);
    return slow == 1;
}

int main() {
    auto* a = new ListNode(1);
    auto* b = new ListNode(2);
    auto* c = new ListNode(3);
    a->next = b; b->next = c; c->next = b;
    cout << "hasCycle: " << boolalpha << hasCycle(a) << "\n";
    cout << "cycle start val: " << detectCycleStart(a)->val << "\n";

    auto* n1 = new ListNode(1);
    n1->next = new ListNode(2);
    n1->next->next = new ListNode(3);
    n1->next->next->next = new ListNode(4);
    n1->next->next->next->next = new ListNode(5);
    cout << "middle val: " << middleOfList(n1)->val << "\n";

    cout << "isHappy(19): " << boolalpha << isHappy(19) << "\n";
    cout << "isHappy(2):  " << boolalpha << isHappy(2) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Raw pointers + manual new; production code would use smart pointers.
 *   - Same algorithmic structure; pointer arithmetic is equivalent.
 */
