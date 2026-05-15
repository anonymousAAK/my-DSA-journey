/*
 * WEEK 11 - C++ DSA
 * Topic: Merge Two Sorted Lists + LRU Cache
 * File: 2.MergeSortedListsAndLRU.cpp
 *
 * CONCEPT:
 *   PART A - Merge two sorted singly-linked lists by re-wiring nodes (no
 *            allocation). Sentinel dummy head simplifies the loop.
 *   PART B - LRU cache: hashmap (unordered_map) + intrusive doubly-linked
 *            list of (key,value) nodes. get/put both O(1).
 *
 * KEY POINTS:
 *   - Merge: walk both lists, attach smaller head, splice tail.
 *   - LRU: head sentinel is MRU side; tail sentinel is LRU side.
 *   - Eviction: when at capacity on insert, drop tail->prev.
 *
 * ALGORITHM / APPROACH:
 *   merge: while both non-empty pick smaller; attach remainder; return
 *          dummy.next.
 *   LRU.get(k): not in map -> -1; else move to front, return value.
 *   LRU.put(k, v): if present update + move to front; else if full evict
 *                  LRU; insert new node after head sentinel.
 *
 * C++-SPECIFIC NOTES:
 *   - We use std::unordered_map<int, DLNode*> for O(1) lookup. The DLL nodes
 *     are owned by the cache; destructor walks and deletes them.
 *   - C++17 structured bindings, `nullptr`, and uniform initialization.
 *   - Could equivalently use std::list<std::pair<int,int>> + iterator map —
 *     the STL `std::list::splice` is O(1) and is the canonical idiom. We
 *     also include that variant for comparison.
 *   - The classic answer in modern C++ is just `std::list` + map of iters.
 *
 * DRY RUN:
 *   merge [1,2,4] + [1,3,4]:
 *     1<=1 -> attach l1; advance
 *     2 vs 1 -> attach l2; advance
 *     2 vs 3 -> attach l1; advance
 *     4 vs 3 -> attach l2; advance
 *     4 vs 4 -> attach l1; advance; l1 done
 *     attach l2 remainder
 *     result: 1 -> 1 -> 2 -> 3 -> 4 -> 4
 *
 *   LRUCache(3): put(1,1) put(2,2) put(3,3) get(1) put(4,4)
 *     after put(3,3): MRU [3] [2] [1] LRU
 *     after get(1):   MRU [1] [3] [2] LRU
 *     after put(4,4): full -> evict 2  -> MRU [4] [1] [3] LRU
 *
 * COMPLEXITY:
 *   merge: O(m+n) time, O(1) space.
 *   LRU get/put: O(1) avg time, O(capacity) space.
 */

#include <iostream>
#include <list>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>

// ---------- PART A: Merge sorted lists ----------

struct ListNode {
    int val;
    ListNode* next;
    explicit ListNode(int v) : val(v), next(nullptr) {}
};

ListNode* buildList(const std::vector<int>& vs) {
    ListNode dummy(0);
    ListNode* curr = &dummy;
    for (int v : vs) {
        curr->next = new ListNode(v);
        curr = curr->next;
    }
    return dummy.next;
}

void freeList(ListNode* head) {
    while (head) { ListNode* nx = head->next; delete head; head = nx; }
}

std::string printList(ListNode* head) {
    std::ostringstream os;
    bool first = true;
    while (head) {
        if (!first) os << " -> ";
        os << head->val;
        first = false;
        head = head->next;
    }
    return os.str();
}

ListNode* mergeSortedLists(ListNode* l1, ListNode* l2) {
    ListNode dummy(0);
    ListNode* curr = &dummy;
    while (l1 && l2) {
        if (l1->val <= l2->val) { curr->next = l1; l1 = l1->next; }
        else                    { curr->next = l2; l2 = l2->next; }
        curr = curr->next;
    }
    curr->next = l1 ? l1 : l2;
    return dummy.next;
}

// ---------- PART B: LRU Cache (hand-rolled DLL + unordered_map) ----------

class LRUCache {
public:
    explicit LRUCache(int cap) : capacity(cap) {
        head = new DLNode(0, 0);
        tail = new DLNode(0, 0);
        head->next = tail;
        tail->prev = head;
    }
    ~LRUCache() {
        DLNode* curr = head;
        while (curr) {
            DLNode* nx = curr->next;
            delete curr;
            curr = nx;
        }
    }
    LRUCache(const LRUCache&) = delete;
    LRUCache& operator=(const LRUCache&) = delete;

    int get(int key) {
        auto it = map.find(key);
        if (it == map.end()) return -1;
        DLNode* node = it->second;
        removeNode(node);
        insertAfterHead(node);
        return node->val;
    }

    void put(int key, int value) {
        auto it = map.find(key);
        if (it != map.end()) {
            DLNode* node = it->second;
            node->val = value;
            removeNode(node);
            insertAfterHead(node);
            return;
        }
        if (static_cast<int>(map.size()) == capacity) {
            DLNode* lru = tail->prev;
            removeNode(lru);
            map.erase(lru->key);
            delete lru;
        }
        DLNode* n = new DLNode(key, value);
        insertAfterHead(n);
        map[key] = n;
    }

    std::string state() const {
        std::ostringstream os;
        os << "Cache (MRU->LRU): ";
        bool first = true;
        for (DLNode* c = head->next; c != tail; c = c->next) {
            if (!first) os << " -> ";
            os << "[" << c->key << "=" << c->val << "]";
            first = false;
        }
        return os.str();
    }

private:
    struct DLNode {
        int key, val;
        DLNode* prev = nullptr;
        DLNode* next = nullptr;
        DLNode(int k, int v) : key(k), val(v) {}
    };

    int capacity;
    std::unordered_map<int, DLNode*> map;
    DLNode* head;
    DLNode* tail;

    void removeNode(DLNode* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }
    void insertAfterHead(DLNode* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }
};

// ---------- LRU using std::list (idiomatic STL variant) ----------

class LRUCacheStdList {
public:
    explicit LRUCacheStdList(int cap) : capacity(cap) {}

    int get(int key) {
        auto it = map.find(key);
        if (it == map.end()) return -1;
        // splice the iterator's node to the front (O(1))
        order.splice(order.begin(), order, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = map.find(key);
        if (it != map.end()) {
            it->second->second = value;
            order.splice(order.begin(), order, it->second);
            return;
        }
        if (static_cast<int>(order.size()) == capacity) {
            map.erase(order.back().first);
            order.pop_back();
        }
        order.emplace_front(key, value);
        map[key] = order.begin();
    }

    std::string state() const {
        std::ostringstream os;
        os << "Cache (MRU->LRU): ";
        bool first = true;
        for (const auto& [k, v] : order) {
            if (!first) os << " -> ";
            os << "[" << k << "=" << v << "]";
            first = false;
        }
        return os.str();
    }

private:
    int capacity;
    std::list<std::pair<int, int>> order;
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> map;
};

// ---------- main ----------

int main() {
    std::cout << "=== Merge Sorted Lists ===\n";
    ListNode* l1 = buildList({1, 2, 4});
    ListNode* l2 = buildList({1, 3, 4});
    ListNode* m1 = mergeSortedLists(l1, l2);
    std::cout << "Merged: " << printList(m1) << "\n";
    freeList(m1);

    ListNode* l3 = buildList({1, 3, 5, 7});
    ListNode* l4 = buildList({2, 4, 6, 8, 10});
    ListNode* m2 = mergeSortedLists(l3, l4);
    std::cout << "Merged: " << printList(m2) << "\n";
    freeList(m2);

    std::cout << "\n=== LRU Cache (DLL + unordered_map, capacity=3) ===\n";
    LRUCache cache(3);
    cache.put(1, 1); std::cout << cache.state() << "\n";
    cache.put(2, 2); std::cout << cache.state() << "\n";
    cache.put(3, 3); std::cout << cache.state() << "\n";
    std::cout << "get(1) = " << cache.get(1) << "\n";
    std::cout << cache.state() << "\n";
    cache.put(4, 4);
    std::cout << cache.state() << "\n";
    std::cout << "get(2) = " << cache.get(2) << "\n";
    std::cout << "get(3) = " << cache.get(3) << "\n";
    std::cout << "get(4) = " << cache.get(4) << "\n";
    std::cout << cache.state() << "\n";

    std::cout << "\n=== LRU Cache (std::list variant) ===\n";
    LRUCacheStdList sc(3);
    sc.put(1, 1); sc.put(2, 2); sc.put(3, 3);
    std::cout << sc.state() << "\n";
    sc.get(1);
    std::cout << "after get(1): " << sc.state() << "\n";
    sc.put(4, 4);
    std::cout << "after put(4,4): " << sc.state() << "\n";

    return 0;
}

/*
 * NOTES (vs. Java):
 * - Java's HashMap is unordered_map here; LinkedHashMap (with access-order)
 *   is the closest analogue to our LRUCacheStdList combo.
 * - Java's GC frees evicted DL nodes; we explicitly delete them.
 * - The std::list approach uses O(1) `splice` to move a node to the front
 *   while keeping the iterator stable — that iterator stability is the key
 *   property that lets the unordered_map index remain valid.
 */
