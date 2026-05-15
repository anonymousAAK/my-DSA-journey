/*
 * WEEK 14 - C++ DSA
 * Topic: Binary Tree - Structure, Traversals, Properties
 * File: 1.BinaryTree.cpp
 *
 * CONCEPT:
 *   A hierarchical structure where each node has at most two children
 *   (left, right). Topmost is the root.
 *
 * KEY POINTS:
 *   - Traversals: inorder, preorder, postorder, level-order (BFS).
 *   - Properties: height, count, diameter, mirror.
 *
 * ALGORITHM / APPROACH:
 *   See Week 14 Java file. Same algorithms.
 *
 * C++-SPECIFIC NOTES:
 *   - We use raw `Node*` for the tree and free everything in main() with a
 *     post-order delete. Could use std::unique_ptr<Node> for automatic
 *     ownership.
 *   - std::queue<Node*> for BFS; std::stack<Node*> for iterative inorder.
 *   - Diameter uses a captured-by-ref `int` for the running max; in Java
 *     this is a static field.
 *
 * DRY RUN:
 *   Sample tree (1 root, 2/3 children, 4/5/6/7 grandchildren):
 *     Inorder    -> 4 2 5 1 6 3 7
 *     Preorder   -> 1 2 4 5 3 6 7
 *     Postorder  -> 4 5 2 6 7 3 1
 *     Level-order-> [[1],[2,3],[4,5,6,7]]
 *     Height = 3, Count = 7, Diameter = 4.
 *
 * COMPLEXITY:
 *   All traversals O(n) time, O(h) space.
 */

#include <iostream>
#include <queue>
#include <sstream>
#include <stack>
#include <vector>

struct Node {
    int val;
    Node* left = nullptr;
    Node* right = nullptr;
    explicit Node(int v) : val(v) {}
};

Node* buildSampleTree() {
    Node* r = new Node(1);
    r->left = new Node(2); r->right = new Node(3);
    r->left->left = new Node(4); r->left->right = new Node(5);
    r->right->left = new Node(6); r->right->right = new Node(7);
    return r;
}

void freeTree(Node* root) {
    if (!root) return;
    freeTree(root->left); freeTree(root->right);
    delete root;
}

void inorderHelper(Node* n, std::vector<int>& out) {
    if (!n) return;
    inorderHelper(n->left, out);
    out.push_back(n->val);
    inorderHelper(n->right, out);
}
std::vector<int> inorder(Node* root) { std::vector<int> v; inorderHelper(root, v); return v; }

void preorderHelper(Node* n, std::vector<int>& out) {
    if (!n) return;
    out.push_back(n->val);
    preorderHelper(n->left, out);
    preorderHelper(n->right, out);
}
std::vector<int> preorder(Node* root) { std::vector<int> v; preorderHelper(root, v); return v; }

void postorderHelper(Node* n, std::vector<int>& out) {
    if (!n) return;
    postorderHelper(n->left, out);
    postorderHelper(n->right, out);
    out.push_back(n->val);
}
std::vector<int> postorder(Node* root) { std::vector<int> v; postorderHelper(root, v); return v; }

std::vector<std::vector<int>> levelOrder(Node* root) {
    std::vector<std::vector<int>> out;
    if (!root) return out;
    std::queue<Node*> q; q.push(root);
    while (!q.empty()) {
        std::size_t lvl = q.size();
        std::vector<int> level;
        for (std::size_t i = 0; i < lvl; ++i) {
            Node* n = q.front(); q.pop();
            level.push_back(n->val);
            if (n->left)  q.push(n->left);
            if (n->right) q.push(n->right);
        }
        out.push_back(level);
    }
    return out;
}

std::vector<int> inorderIterative(Node* root) {
    std::vector<int> out;
    std::stack<Node*> st;
    Node* curr = root;
    while (curr || !st.empty()) {
        while (curr) { st.push(curr); curr = curr->left; }
        curr = st.top(); st.pop();
        out.push_back(curr->val);
        curr = curr->right;
    }
    return out;
}

int height(Node* root) {
    if (!root) return 0;
    return 1 + std::max(height(root->left), height(root->right));
}

int countNodes(Node* root) {
    if (!root) return 0;
    return 1 + countNodes(root->left) + countNodes(root->right);
}

static int diameter_helper(Node* n, int& best) {
    if (!n) return 0;
    int l = diameter_helper(n->left, best);
    int r = diameter_helper(n->right, best);
    if (l + r > best) best = l + r;
    return 1 + std::max(l, r);
}
int diameter(Node* root) { int best = 0; diameter_helper(root, best); return best; }

void mirror(Node* root) {
    if (!root) return;
    std::swap(root->left, root->right);
    mirror(root->left);
    mirror(root->right);
}

template<typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream os; os << "[";
    for (std::size_t i = 0; i < v.size(); ++i) { if (i) os << ", "; os << v[i]; }
    os << "]"; return os.str();
}

std::string lvl_str(const std::vector<std::vector<int>>& v) {
    std::ostringstream os; os << "[";
    for (std::size_t i = 0; i < v.size(); ++i) { if (i) os << ", "; os << vec_str(v[i]); }
    os << "]"; return os.str();
}

int main() {
    Node* root = buildSampleTree();

    std::cout << "Inorder:     " << vec_str(inorder(root)) << "\n";
    std::cout << "Preorder:    " << vec_str(preorder(root)) << "\n";
    std::cout << "Postorder:   " << vec_str(postorder(root)) << "\n";
    std::cout << "Level-order: " << lvl_str(levelOrder(root)) << "\n";
    std::cout << "Inorder it:  " << vec_str(inorderIterative(root)) << "\n";

    std::cout << "\nHeight:    " << height(root) << "\n";
    std::cout << "Node count:" << countNodes(root) << "\n";
    std::cout << "Diameter:  " << diameter(root) << "\n";

    mirror(root);
    std::cout << "\nAfter mirror:\n";
    std::cout << "Inorder: " << vec_str(inorder(root)) << "\n";

    freeTree(root);
    return 0;
}

/*
 * NOTES (vs. Java):
 * - Java GC reclaims tree nodes; we delete manually via post-order traversal.
 * - std::queue (FIFO) and std::stack (LIFO) are STL adapters.
 * - We pass `int& best` to capture the running max in diameter (closure
 *   equivalent); Java uses a static field.
 */
