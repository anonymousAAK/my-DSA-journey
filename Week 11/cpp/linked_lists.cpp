/*
 * =============================================================================
 * Week 11 - Linked Lists (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Singly Linked List:
 *      - Insert (head, tail, at position)
 *      - Delete (head, tail, by value)
 *      - Reverse (iterative + recursive)
 *      - Find middle (slow/fast pointer)
 *      - Cycle detection (Floyd's algorithm)
 *   2. Merge two sorted linked lists
 *   3. LRU Cache (using std::list + std::unordered_map)
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features: structured bindings, optional, smart pointers
 * for memory safety discussions.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// SINGLY LINKED LIST NODE
// =============================================================================
struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v) : val(v), next(nullptr) {}
    ListNode(int v, ListNode* n) : val(v), next(n) {}
};

// =============================================================================
// HELPER: create linked list from vector, print list
// =============================================================================
ListNode* createList(const vector<int>& vals) {
    ListNode dummy(0);
    ListNode* tail = &dummy;
    for (int v : vals) {
        tail->next = new ListNode(v);
        tail = tail->next;
    }
    return dummy.next;
}

void printList(ListNode* head, const string& label = "") {
    if (!label.empty()) cout << label << ": ";
    while (head) {
        cout << head->val;
        if (head->next) cout << " -> ";
        head = head->next;
    }
    cout << " -> NULL" << endl;
}

void freeList(ListNode* head) {
    while (head) {
        ListNode* tmp = head;
        head = head->next;
        delete tmp;
    }
}

// =============================================================================
// 1a. INSERT AT HEAD
// =============================================================================
// Time: O(1)   Space: O(1)
ListNode* insertAtHead(ListNode* head, int val) {
    return new ListNode(val, head);
}

// =============================================================================
// 1b. INSERT AT TAIL
// =============================================================================
// Time: O(n)   Space: O(1)
ListNode* insertAtTail(ListNode* head, int val) {
    ListNode* newNode = new ListNode(val);
    if (!head) return newNode;
    ListNode* curr = head;
    while (curr->next) curr = curr->next;
    curr->next = newNode;
    return head;
}

// =============================================================================
// 1c. INSERT AT POSITION (0-indexed)
// =============================================================================
// Time: O(n)   Space: O(1)
ListNode* insertAtPosition(ListNode* head, int val, int pos) {
    if (pos == 0) return insertAtHead(head, val);
    ListNode* curr = head;
    for (int i = 0; i < pos - 1 && curr; ++i) curr = curr->next;
    if (!curr) return head;  // position out of bounds
    ListNode* newNode = new ListNode(val, curr->next);
    curr->next = newNode;
    return head;
}

// =============================================================================
// 1d. DELETE BY VALUE (first occurrence)
// =============================================================================
// Time: O(n)   Space: O(1)
ListNode* deleteByValue(ListNode* head, int val) {
    if (!head) return nullptr;
    if (head->val == val) {
        ListNode* tmp = head->next;
        delete head;
        return tmp;
    }
    ListNode* curr = head;
    while (curr->next && curr->next->val != val) {
        curr = curr->next;
    }
    if (curr->next) {
        ListNode* tmp = curr->next;
        curr->next = tmp->next;
        delete tmp;
    }
    return head;
}

// =============================================================================
// 1e. REVERSE (Iterative)
// =============================================================================
// Time: O(n)   Space: O(1)
ListNode* reverseIterative(ListNode* head) {
    ListNode* prev = nullptr;
    ListNode* curr = head;
    while (curr) {
        ListNode* next = curr->next;
        curr->next = prev;
        prev = curr;
        curr = next;
    }
    return prev;
}

// =============================================================================
// 1f. REVERSE (Recursive)
// =============================================================================
// Time: O(n)   Space: O(n) call stack
ListNode* reverseRecursive(ListNode* head) {
    if (!head || !head->next) return head;
    ListNode* newHead = reverseRecursive(head->next);
    head->next->next = head;
    head->next = nullptr;
    return newHead;
}

// =============================================================================
// 1g. FIND MIDDLE (Slow/Fast Pointer)
// =============================================================================
// Time: O(n)   Space: O(1)
// For even-length lists, returns the second middle node.
ListNode* findMiddle(ListNode* head) {
    if (!head) return nullptr;
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
    }
    return slow;
}

// =============================================================================
// 1h. CYCLE DETECTION (Floyd's Algorithm)
// =============================================================================
// Time: O(n)   Space: O(1)
// Returns the node where the cycle starts, or nullptr if no cycle.
ListNode* detectCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;

    // Phase 1: detect if cycle exists
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            // Phase 2: find cycle start
            slow = head;
            while (slow != fast) {
                slow = slow->next;
                fast = fast->next;
            }
            return slow;
        }
    }
    return nullptr;  // no cycle
}

bool hasCycle(ListNode* head) {
    return detectCycle(head) != nullptr;
}

// =============================================================================
// 2. MERGE TWO SORTED LINKED LISTS
// =============================================================================
// Time: O(m + n)   Space: O(1) extra (reuses existing nodes)
ListNode* mergeSortedLists(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* tail = &dummy;

    while (l1 && l2) {
        if (l1->val <= l2->val) {
            tail->next = l1;
            l1 = l1->next;
        } else {
            tail->next = l2;
            l2 = l2->next;
        }
        tail = tail->next;
    }
    tail->next = l1 ? l1 : l2;
    return dummy.next;
}

// =============================================================================
// 3. LRU CACHE
// =============================================================================
// Uses std::list (doubly linked list) + unordered_map for O(1) operations.
//
// get(key):  O(1) average
// put(key, value): O(1) average
// Space: O(capacity)
class LRUCache {
    int capacity_;
    // list stores {key, value} pairs; front = most recently used
    list<pair<int, int>> cache_;
    // maps key -> iterator in the list
    unordered_map<int, list<pair<int, int>>::iterator> map_;

public:
    LRUCache(int capacity) : capacity_(capacity) {}

    // Get value for key. Returns -1 if not found.
    // Time: O(1) average
    int get(int key) {
        auto it = map_.find(key);
        if (it == map_.end()) return -1;

        // Move accessed item to front (most recently used)
        cache_.splice(cache_.begin(), cache_, it->second);
        return it->second->second;
    }

    // Put key-value pair. Evicts LRU item if at capacity.
    // Time: O(1) average
    void put(int key, int value) {
        auto it = map_.find(key);
        if (it != map_.end()) {
            // Key exists: update value and move to front
            it->second->second = value;
            cache_.splice(cache_.begin(), cache_, it->second);
            return;
        }

        // Evict LRU (back of list) if at capacity
        if (static_cast<int>(cache_.size()) == capacity_) {
            auto& [lruKey, lruVal] = cache_.back();  // C++17 structured binding
            map_.erase(lruKey);
            cache_.pop_back();
        }

        // Insert new item at front
        cache_.emplace_front(key, value);
        map_[key] = cache_.begin();
    }

    void printState() const {
        cout << "  Cache (MRU->LRU): ";
        for (const auto& [k, v] : cache_) {
            cout << "[" << k << ":" << v << "] ";
        }
        cout << endl;
    }
};

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 11: Linked Lists (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Singly Linked List Operations ---
    cout << "\n--- 1. Singly Linked List Operations ---" << endl;
    {
        ListNode* head = createList({1, 2, 3, 4, 5});
        printList(head, "Original");

        head = insertAtHead(head, 0);
        printList(head, "Insert 0 at head");

        head = insertAtTail(head, 6);
        printList(head, "Insert 6 at tail");

        head = insertAtPosition(head, 99, 3);
        printList(head, "Insert 99 at pos 3");

        head = deleteByValue(head, 99);
        printList(head, "Delete 99");

        head = deleteByValue(head, 0);
        printList(head, "Delete 0 (head)");

        // Find middle
        ListNode* mid = findMiddle(head);
        cout << "Middle element: " << (mid ? to_string(mid->val) : "null") << endl;

        // Reverse iterative
        head = reverseIterative(head);
        printList(head, "Reversed (iterative)");

        // Reverse recursive (back to original order)
        head = reverseRecursive(head);
        printList(head, "Reversed back (recursive)");

        freeList(head);
    }

    // --- Cycle Detection ---
    cout << "\n--- Cycle Detection ---" << endl;
    {
        // Create a list with a cycle: 1->2->3->4->5->3 (cycle at node 3)
        ListNode* n1 = new ListNode(1);
        ListNode* n2 = new ListNode(2);
        ListNode* n3 = new ListNode(3);
        ListNode* n4 = new ListNode(4);
        ListNode* n5 = new ListNode(5);
        n1->next = n2; n2->next = n3; n3->next = n4; n4->next = n5;
        n5->next = n3;  // cycle!

        ListNode* cycleStart = detectCycle(n1);
        cout << "Cycle starts at node with value: "
             << (cycleStart ? to_string(cycleStart->val) : "no cycle") << endl;

        // Clean up (break cycle first)
        n5->next = nullptr;
        freeList(n1);

        // No cycle test
        ListNode* noCycle = createList({1, 2, 3});
        cout << "No-cycle list has cycle: " << (hasCycle(noCycle) ? "yes" : "no") << endl;
        freeList(noCycle);
    }

    // --- 2. Merge Sorted Lists ---
    cout << "\n--- 2. Merge Two Sorted Lists ---" << endl;
    {
        ListNode* l1 = createList({1, 3, 5, 7});
        ListNode* l2 = createList({2, 4, 6, 8});
        printList(l1, "List 1");
        printList(l2, "List 2");

        ListNode* merged = mergeSortedLists(l1, l2);
        printList(merged, "Merged");
        freeList(merged);

        // Edge: one empty
        ListNode* l3 = createList({1, 2, 3});
        ListNode* merged2 = mergeSortedLists(l3, nullptr);
        printList(merged2, "Merge with empty");
        freeList(merged2);
    }

    // --- 3. LRU Cache ---
    cout << "\n--- 3. LRU Cache ---" << endl;
    {
        LRUCache cache(3);
        cout << "Put (1,10), (2,20), (3,30):" << endl;
        cache.put(1, 10);
        cache.put(2, 20);
        cache.put(3, 30);
        cache.printState();

        cout << "Get(1) = " << cache.get(1) << endl;
        cache.printState();  // 1 should be at front now

        cout << "Put (4,40) - should evict key 2:" << endl;
        cache.put(4, 40);
        cache.printState();

        cout << "Get(2) = " << cache.get(2) << " (should be -1, evicted)" << endl;

        cout << "Put (3,300) - update existing key 3:" << endl;
        cache.put(3, 300);
        cache.printState();

        cout << "Get(3) = " << cache.get(3) << " (should be 300)" << endl;
    }

    cout << "\n========================================" << endl;
    cout << " All Week 11 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
