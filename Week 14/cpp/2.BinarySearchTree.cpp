/*
 * WEEK 14 - C++ DSA
 * Topic: Binary Search Tree (BST)
 * File: 2.BinarySearchTree.cpp
 *
 * CONCEPT:
 *   For every node, all keys in left subtree < node < all keys in right
 *   subtree. Search/insert/delete are O(h).
 *
 * KEY POINTS:
 *   - 3 cases for delete: leaf, one child, two children (replace with
 *     inorder successor).
 *   - Validate via min/max bounds passed down the recursion.
 *   - LCA in BST: walk down; first node where p,q split (or one matches).
 *
 * ALGORITHM / APPROACH: identical to Java file.
 *
 * C++-SPECIFIC NOTES:
 *   - We use raw Node* with an explicit destroy() function.
 *   - LONG_MIN / LONG_MAX bounds (or std::numeric_limits<long long>) used
 *     for validation, mirroring Java.
 *
 * DRY RUN:
 *   Insert 5,3,7,1,4,6,8 -> sorted order on inorder is 1 3 4 5 6 7 8.
 *   Delete 3: subtree successor = 4; result inorder 1 4 5 6 7 8.
 *   Delete 5 (root): successor = 6; result inorder 1 4 6 7 8.
 *
 * COMPLEXITY:
 *   insert/search/delete: O(h)
 *   isValidBST: O(n)
 *   lca: O(h)
 *   kthSmallest: O(h+k)
 */

#include <iostream>
#include <limits>
#include <stack>
#include <vector>

struct Node {
    int val;
    Node* left = nullptr;
    Node* right = nullptr;
    explicit Node(int v) : val(v) {}
};

class BST {
public:
    BST() : root(nullptr) {}
    ~BST() { destroy(root); }
    BST(const BST&) = delete;
    BST& operator=(const BST&) = delete;

    void insert(int v) { root = insertRec(root, v); }
    bool search(int v) const { return searchRec(root, v); }
    void erase(int v) { root = deleteRec(root, v); }

    std::vector<int> sortedValues() const {
        std::vector<int> out;
        inorder(root, out);
        return out;
    }

    bool isValidBST() const {
        return validate(root,
                        std::numeric_limits<long long>::min(),
                        std::numeric_limits<long long>::max());
    }

    int lca(int p, int q) const {
        Node* n = root;
        while (n) {
            if (p < n->val && q < n->val) n = n->left;
            else if (p > n->val && q > n->val) n = n->right;
            else return n->val;
        }
        return -1;
    }

    int kthSmallest(int k) const {
        std::stack<Node*> st;
        Node* curr = root;
        int cnt = 0;
        while (curr || !st.empty()) {
            while (curr) { st.push(curr); curr = curr->left; }
            curr = st.top(); st.pop();
            if (++cnt == k) return curr->val;
            curr = curr->right;
        }
        return -1;
    }

private:
    Node* root;

    static void destroy(Node* n) {
        if (!n) return;
        destroy(n->left); destroy(n->right);
        delete n;
    }

    static Node* insertRec(Node* n, int v) {
        if (!n) return new Node(v);
        if (v < n->val) n->left = insertRec(n->left, v);
        else if (v > n->val) n->right = insertRec(n->right, v);
        return n;
    }

    static bool searchRec(Node* n, int v) {
        if (!n) return false;
        if (v == n->val) return true;
        return v < n->val ? searchRec(n->left, v) : searchRec(n->right, v);
    }

    static Node* minNode(Node* n) {
        while (n->left) n = n->left;
        return n;
    }

    static Node* deleteRec(Node* n, int v) {
        if (!n) return nullptr;
        if (v < n->val) n->left = deleteRec(n->left, v);
        else if (v > n->val) n->right = deleteRec(n->right, v);
        else {
            if (!n->left)  { Node* r = n->right; delete n; return r; }
            if (!n->right) { Node* l = n->left;  delete n; return l; }
            Node* succ = minNode(n->right);
            n->val = succ->val;
            n->right = deleteRec(n->right, succ->val);
        }
        return n;
    }

    static void inorder(Node* n, std::vector<int>& out) {
        if (!n) return;
        inorder(n->left, out);
        out.push_back(n->val);
        inorder(n->right, out);
    }

    static bool validate(Node* n, long long lo, long long hi) {
        if (!n) return true;
        if (n->val <= lo || n->val >= hi) return false;
        return validate(n->left, lo, n->val) && validate(n->right, n->val, hi);
    }
};

int main() {
    BST bst;
    for (int v : {5, 3, 7, 1, 4, 6, 8}) bst.insert(v);

    std::cout << "Inserted: 5,3,7,1,4,6,8\n";
    std::cout << "Inorder (sorted): ";
    for (int v : bst.sortedValues()) std::cout << v << " ";
    std::cout << "\n";

    std::cout << "Search 4: " << std::boolalpha << bst.search(4) << "\n";
    std::cout << "Search 9: " << bst.search(9) << "\n";
    std::cout << "Is valid BST: " << bst.isValidBST() << "\n";

    std::cout << "LCA(1,4) = " << bst.lca(1, 4) << "\n";
    std::cout << "LCA(1,8) = " << bst.lca(1, 8) << "\n";
    std::cout << "LCA(6,8) = " << bst.lca(6, 8) << "\n";

    std::cout << "2nd smallest: " << bst.kthSmallest(2) << "\n";
    std::cout << "5th smallest: " << bst.kthSmallest(5) << "\n";

    bst.erase(3);
    std::cout << "\nAfter deleting 3: ";
    for (int v : bst.sortedValues()) std::cout << v << " ";
    std::cout << "\n";

    bst.erase(5);
    std::cout << "After deleting root (5): ";
    for (int v : bst.sortedValues()) std::cout << v << " ";
    std::cout << "\n";

    return 0;
}

/*
 * NOTES (vs. Java):
 * - Java GC frees tree nodes; we destroy() recursively.
 * - We use std::numeric_limits<long long> for unbounded sentinels (Java
 *   uses Long.MIN_VALUE / MAX_VALUE).
 * - kthSmallest is iterative with std::stack<Node*>; equivalent to the
 *   Java recursive helper with mutable counter array.
 */
