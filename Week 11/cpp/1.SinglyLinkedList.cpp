/*
 * WEEK 11 - C++ DSA
 * Topic: Singly Linked List - Complete Implementation
 * File: 1.SinglyLinkedList.cpp
 *
 * CONCEPT:
 *   Sequential nodes connected by `next` pointers. The head is the only entry
 *   point. Differs from std::list (doubly linked) and std::forward_list
 *   (singly linked, but minimal API).
 *
 * KEY POINTS:
 *   - Each Node carries int data + Node* next (default nullptr).
 *   - We show two ownership flavours:
 *       * raw-pointer LinkedList (must `delete` in the destructor)
 *       * shared_ptr<Node> LinkedList (refcount, no manual delete)
 *   - Floyd's tortoise-and-hare for middle / cycle detection.
 *
 * ALGORITHM / APPROACH:
 *   insertAtHead: new node, splice at front.
 *   insertAtTail: walk until next == nullptr.
 *   insertAtIndex: walk to idx-1, splice in.
 *   deleteByValue: track previous; relink past the doomed node and free it.
 *   reverseIterative: 3-pointer (prev/curr/next) sweep.
 *   reverseRecursive: recurse to end, flip child->parent on unwind.
 *   findMiddle/hasCycle: slow steps 1, fast steps 2.
 *
 * C++-SPECIFIC NOTES:
 *   - Manual ownership: the raw-pointer version owns its nodes and frees them
 *     in ~LinkedList(); skip that and you leak memory (Java's GC saves you).
 *   - Use `nullptr` not 0 / NULL.
 *   - Use `throw std::out_of_range` instead of unchecked behavior.
 *   - shared_ptr-based version is shown briefly (deeply recursive destructors
 *     can blow the stack on huge lists; std::list/forward_list don't suffer
 *     from this, but the textbook version does).
 *
 * DRY RUN:
 *   Example 1: insertAtTail 1,2,3 -> [1->2->3->nullptr]
 *   Example 2: reverseIterative on [1->2->3]
 *     prev=null curr=1 -> next=2; 1->null; prev=1 curr=2
 *     prev=1    curr=2 -> next=3; 2->1;    prev=2 curr=3
 *     prev=2    curr=3 -> next=null; 3->2; prev=3 curr=null
 *     head = prev = 3 -> [3->2->1->nullptr]
 *
 * COMPLEXITY:
 *   insertHead/deleteHead: O(1)
 *   insertTail/insertAtIndex/deleteByValue/contains/size: O(n)
 *   reverseIterative: O(n) time, O(1) space
 *   reverseRecursive: O(n) time, O(n) recursion stack
 *   findMiddle/hasCycle: O(n) time, O(1) space
 */

#include <iostream>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>

// ==================== Raw-pointer version (primary) ====================

struct Node {
    int data;
    Node* next;
    explicit Node(int d) : data(d), next(nullptr) {}
};

class LinkedList {
public:
    LinkedList() = default;
    ~LinkedList() {
        while (head) {
            Node* nx = head->next;
            delete head;
            head = nx;
        }
    }
    // Disable copies to avoid double-free; allow moves.
    LinkedList(const LinkedList&) = delete;
    LinkedList& operator=(const LinkedList&) = delete;
    LinkedList(LinkedList&& other) noexcept : head(other.head) { other.head = nullptr; }
    LinkedList& operator=(LinkedList&& other) noexcept {
        if (this != &other) {
            this->~LinkedList();
            head = other.head;
            other.head = nullptr;
        }
        return *this;
    }

    void insertAtHead(int data) {
        Node* n = new Node(data);
        n->next = head;
        head = n;
    }

    void insertAtTail(int data) {
        Node* n = new Node(data);
        if (!head) { head = n; return; }
        Node* curr = head;
        while (curr->next) curr = curr->next;
        curr->next = n;
    }

    void insertAtIndex(int idx, int data) {
        if (idx < 0) throw std::out_of_range("Index out of bounds");
        if (idx == 0) { insertAtHead(data); return; }
        Node* curr = head;
        for (int i = 0; i < idx - 1 && curr; ++i) curr = curr->next;
        if (!curr) throw std::out_of_range("Index out of bounds");
        Node* n = new Node(data);
        n->next = curr->next;
        curr->next = n;
    }

    void deleteHead() {
        if (!head) return;
        Node* old = head;
        head = head->next;
        delete old;
    }

    bool deleteByValue(int val) {
        if (!head) return false;
        if (head->data == val) {
            Node* old = head;
            head = head->next;
            delete old;
            return true;
        }
        Node* curr = head;
        while (curr->next) {
            if (curr->next->data == val) {
                Node* old = curr->next;
                curr->next = old->next;
                delete old;
                return true;
            }
            curr = curr->next;
        }
        return false;
    }

    bool contains(int val) const {
        for (Node* c = head; c; c = c->next)
            if (c->data == val) return true;
        return false;
    }

    int size() const {
        int n = 0;
        for (Node* c = head; c; c = c->next) ++n;
        return n;
    }

    void reverseIterative() {
        Node* prev = nullptr;
        Node* curr = head;
        while (curr) {
            Node* nx = curr->next;
            curr->next = prev;
            prev = curr;
            curr = nx;
        }
        head = prev;
    }

    void reverseRecursive() { head = reverseRec(head); }

    Node* findMiddle() const {
        Node* slow = head;
        Node* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow;
    }

    bool hasCycle() const {
        Node* slow = head;
        Node* fast = head;
        while (fast && fast->next) {
            slow = slow->next;
            fast = fast->next->next;
            if (slow == fast) return true;
        }
        return false;
    }

    std::string toString() const {
        std::ostringstream os;
        os << "HEAD";
        for (Node* c = head; c; c = c->next) os << " -> " << c->data;
        os << " -> NULL";
        return os.str();
    }

    Node* head = nullptr;

private:
    static Node* reverseRec(Node* node) {
        if (!node || !node->next) return node;
        Node* nh = reverseRec(node->next);
        node->next->next = node;
        node->next = nullptr;
        return nh;
    }
};

// ==================== shared_ptr variant (brief) ====================
//
// This shows an alternate ownership model. shared_ptr<Node> automatically
// frees nodes when the last reference drops. BEWARE: a long chain destroys
// recursively which may stack-overflow; in production code break the chain
// in a loop inside the destructor before letting smart pointers do their job.

struct SNode {
    int data;
    std::shared_ptr<SNode> next;
    explicit SNode(int d) : data(d), next(nullptr) {}
};

class SharedList {
public:
    void push_front(int v) {
        auto n = std::make_shared<SNode>(v);
        n->next = head;
        head = n;
    }
    std::string toString() const {
        std::ostringstream os;
        os << "HEAD";
        for (auto c = head; c; c = c->next) os << " -> " << c->data;
        os << " -> NULL";
        return os.str();
    }

    ~SharedList() {
        // Iterative teardown to avoid deep recursive destructor calls.
        while (head) head = std::move(head->next);
    }

private:
    std::shared_ptr<SNode> head;
};

// ==================== main ====================

int main() {
    LinkedList list;
    for (int v : {1, 2, 3, 4, 5}) list.insertAtTail(v);
    std::cout << list.toString() << "\n";

    list.insertAtHead(0);
    std::cout << list.toString() << "\n";

    list.insertAtIndex(3, 99);
    std::cout << list.toString() << "\n";

    list.deleteByValue(99);
    std::cout << list.toString() << "\n";

    std::cout << "Size: " << list.size() << "\n";
    std::cout << "Contains 3: " << std::boolalpha << list.contains(3) << "\n";
    std::cout << "Contains 9: " << list.contains(9) << "\n";

    Node* mid = list.findMiddle();
    std::cout << "Middle: " << (mid ? mid->data : -1) << "\n";

    list.reverseIterative();
    std::cout << list.toString() << "\n";

    list.reverseRecursive();
    std::cout << list.toString() << "\n";

    std::cout << "Has cycle: " << list.hasCycle() << "\n";

    std::cout << "\n--- shared_ptr variant ---\n";
    SharedList s;
    s.push_front(3); s.push_front(2); s.push_front(1);
    std::cout << s.toString() << "\n";

    return 0;
}

/*
 * NOTES (vs. Java):
 * - Java automatically GC's nodes; here the destructor explicitly frees them.
 * - We delete copy ops to prevent shallow-copy double-free; Java doesn't have
 *   this hazard because everything is reference-counted by the GC.
 * - shared_ptr models reference semantics like Java references; unique_ptr
 *   would model exclusive ownership (closer to Rust's Box).
 * - std::forward_list is the STL singly-linked list; std::list is doubly
 *   linked. We rolled our own to mirror the Java exercise.
 */
