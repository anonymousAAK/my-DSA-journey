/*
 * =============================================================================
 * Week 14 - Trees (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   PART A — Binary Tree:
 *     1. Traversals: inorder, preorder, postorder (recursive + iterative)
 *     2. Level-order traversal (BFS)
 *     3. Height of tree
 *     4. Diameter of tree
 *     5. Mirror / invert a binary tree
 *
 *   PART B — Binary Search Tree (BST):
 *     6. Insert
 *     7. Search
 *     8. Delete
 *     9. Validate BST
 *     10. Lowest Common Ancestor (LCA)
 *     11. Kth smallest element (inorder)
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// TREE NODE
// =============================================================================
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v) : val(v), left(nullptr), right(nullptr) {}
    TreeNode(int v, TreeNode* l, TreeNode* r) : val(v), left(l), right(r) {}
};

// =============================================================================
// HELPER: build tree from level-order array (using -1 as null sentinel)
// =============================================================================
TreeNode* buildTree(const vector<int>& vals) {
    if (vals.empty() || vals[0] == -1) return nullptr;
    TreeNode* root = new TreeNode(vals[0]);
    queue<TreeNode*> q;
    q.push(root);
    int i = 1;
    while (!q.empty() && i < static_cast<int>(vals.size())) {
        TreeNode* node = q.front(); q.pop();
        if (i < static_cast<int>(vals.size()) && vals[i] != -1) {
            node->left = new TreeNode(vals[i]);
            q.push(node->left);
        }
        ++i;
        if (i < static_cast<int>(vals.size()) && vals[i] != -1) {
            node->right = new TreeNode(vals[i]);
            q.push(node->right);
        }
        ++i;
    }
    return root;
}

void freeTree(TreeNode* root) {
    if (!root) return;
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}

void printVec(const vector<int>& v, const string& label = "") {
    if (!label.empty()) cout << label << ": ";
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        cout << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    cout << "]" << endl;
}

// ==========================================
// PART A: BINARY TREE
// ==========================================

// =============================================================================
// 1a. INORDER TRAVERSAL (Left, Root, Right)
// =============================================================================

// Recursive — Time: O(n)  Space: O(h) call stack, h = height
void inorderRecursive(TreeNode* root, vector<int>& result) {
    if (!root) return;
    inorderRecursive(root->left, result);
    result.push_back(root->val);
    inorderRecursive(root->right, result);
}

// Iterative using explicit stack — Time: O(n)  Space: O(h)
vector<int> inorderIterative(TreeNode* root) {
    vector<int> result;
    stack<TreeNode*> st;
    TreeNode* curr = root;
    while (curr || !st.empty()) {
        while (curr) {
            st.push(curr);
            curr = curr->left;
        }
        curr = st.top(); st.pop();
        result.push_back(curr->val);
        curr = curr->right;
    }
    return result;
}

// =============================================================================
// 1b. PREORDER TRAVERSAL (Root, Left, Right)
// =============================================================================

// Recursive — Time: O(n)  Space: O(h)
void preorderRecursive(TreeNode* root, vector<int>& result) {
    if (!root) return;
    result.push_back(root->val);
    preorderRecursive(root->left, result);
    preorderRecursive(root->right, result);
}

// Iterative — Time: O(n)  Space: O(h)
vector<int> preorderIterative(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    stack<TreeNode*> st;
    st.push(root);
    while (!st.empty()) {
        TreeNode* node = st.top(); st.pop();
        result.push_back(node->val);
        // Push right first so left is processed first (LIFO)
        if (node->right) st.push(node->right);
        if (node->left) st.push(node->left);
    }
    return result;
}

// =============================================================================
// 1c. POSTORDER TRAVERSAL (Left, Right, Root)
// =============================================================================

// Recursive — Time: O(n)  Space: O(h)
void postorderRecursive(TreeNode* root, vector<int>& result) {
    if (!root) return;
    postorderRecursive(root->left, result);
    postorderRecursive(root->right, result);
    result.push_back(root->val);
}

// Iterative using two stacks — Time: O(n)  Space: O(n)
vector<int> postorderIterative(TreeNode* root) {
    vector<int> result;
    if (!root) return result;
    stack<TreeNode*> st1, st2;
    st1.push(root);
    while (!st1.empty()) {
        TreeNode* node = st1.top(); st1.pop();
        st2.push(node);
        if (node->left) st1.push(node->left);
        if (node->right) st1.push(node->right);
    }
    while (!st2.empty()) {
        result.push_back(st2.top()->val);
        st2.pop();
    }
    return result;
}

// =============================================================================
// 2. LEVEL-ORDER TRAVERSAL (BFS)
// =============================================================================
// Time: O(n)   Space: O(w) where w = max width of tree
vector<vector<int>> levelOrder(TreeNode* root) {
    vector<vector<int>> result;
    if (!root) return result;
    queue<TreeNode*> q;
    q.push(root);
    while (!q.empty()) {
        int size = q.size();
        vector<int> level;
        for (int i = 0; i < size; ++i) {
            TreeNode* node = q.front(); q.pop();
            level.push_back(node->val);
            if (node->left) q.push(node->left);
            if (node->right) q.push(node->right);
        }
        result.push_back(move(level));
    }
    return result;
}

// =============================================================================
// 3. HEIGHT OF TREE
// =============================================================================
// Time: O(n)   Space: O(h)
int height(TreeNode* root) {
    if (!root) return 0;
    return 1 + max(height(root->left), height(root->right));
}

// =============================================================================
// 4. DIAMETER OF TREE
// =============================================================================
// Diameter = longest path between any two nodes (number of edges).
// Time: O(n)   Space: O(h)
int diameterHelper(TreeNode* root, int& maxDia) {
    if (!root) return 0;
    int leftH = diameterHelper(root->left, maxDia);
    int rightH = diameterHelper(root->right, maxDia);
    maxDia = max(maxDia, leftH + rightH);  // path through this node
    return 1 + max(leftH, rightH);
}

int diameter(TreeNode* root) {
    int maxDia = 0;
    diameterHelper(root, maxDia);
    return maxDia;
}

// =============================================================================
// 5. MIRROR / INVERT BINARY TREE
// =============================================================================
// Time: O(n)   Space: O(h)
TreeNode* mirror(TreeNode* root) {
    if (!root) return nullptr;
    swap(root->left, root->right);
    mirror(root->left);
    mirror(root->right);
    return root;
}

// ==========================================
// PART B: BINARY SEARCH TREE
// ==========================================

// =============================================================================
// 6. BST INSERT
// =============================================================================
// Time: O(h) avg O(log n), worst O(n) for skewed tree
// Space: O(h) recursive
TreeNode* bstInsert(TreeNode* root, int val) {
    if (!root) return new TreeNode(val);
    if (val < root->val)
        root->left = bstInsert(root->left, val);
    else if (val > root->val)
        root->right = bstInsert(root->right, val);
    // Duplicate values ignored
    return root;
}

// =============================================================================
// 7. BST SEARCH
// =============================================================================
// Time: O(h)   Space: O(1) iterative
TreeNode* bstSearch(TreeNode* root, int val) {
    while (root) {
        if (val == root->val) return root;
        root = (val < root->val) ? root->left : root->right;
    }
    return nullptr;
}

// =============================================================================
// 8. BST DELETE
// =============================================================================
// Time: O(h)   Space: O(h) recursive
// Three cases:
//   - Node is a leaf: just remove it
//   - Node has one child: replace with child
//   - Node has two children: replace with inorder successor (smallest in right subtree)

TreeNode* findMin(TreeNode* root) {
    while (root->left) root = root->left;
    return root;
}

TreeNode* bstDelete(TreeNode* root, int val) {
    if (!root) return nullptr;
    if (val < root->val) {
        root->left = bstDelete(root->left, val);
    } else if (val > root->val) {
        root->right = bstDelete(root->right, val);
    } else {
        // Found the node to delete
        if (!root->left) {
            TreeNode* temp = root->right;
            delete root;
            return temp;
        }
        if (!root->right) {
            TreeNode* temp = root->left;
            delete root;
            return temp;
        }
        // Two children: replace with inorder successor
        TreeNode* successor = findMin(root->right);
        root->val = successor->val;
        root->right = bstDelete(root->right, successor->val);
    }
    return root;
}

// =============================================================================
// 9. VALIDATE BST
// =============================================================================
// Time: O(n)   Space: O(h)
// Uses min/max range approach.
bool isValidBSTHelper(TreeNode* root, long long minVal, long long maxVal) {
    if (!root) return true;
    if (root->val <= minVal || root->val >= maxVal) return false;
    return isValidBSTHelper(root->left, minVal, root->val) &&
           isValidBSTHelper(root->right, root->val, maxVal);
}

bool isValidBST(TreeNode* root) {
    return isValidBSTHelper(root, LLONG_MIN, LLONG_MAX);
}

// =============================================================================
// 10. LOWEST COMMON ANCESTOR (BST)
// =============================================================================
// Time: O(h)   Space: O(1) iterative
// In a BST, if both values are less than root, LCA is in left subtree.
// If both are greater, LCA is in right subtree.
// Otherwise, root is the LCA (the split point).
TreeNode* lcaBST(TreeNode* root, int p, int q) {
    while (root) {
        if (p < root->val && q < root->val)
            root = root->left;
        else if (p > root->val && q > root->val)
            root = root->right;
        else
            return root;  // split point
    }
    return nullptr;
}

// LCA for general binary tree (not necessarily BST)
// Time: O(n)   Space: O(h)
TreeNode* lcaGeneral(TreeNode* root, int p, int q) {
    if (!root) return nullptr;
    if (root->val == p || root->val == q) return root;
    TreeNode* left = lcaGeneral(root->left, p, q);
    TreeNode* right = lcaGeneral(root->right, p, q);
    if (left && right) return root;  // p and q are in different subtrees
    return left ? left : right;
}

// =============================================================================
// 11. KTH SMALLEST IN BST
// =============================================================================
// Inorder traversal of BST gives sorted order.
// Time: O(h + k)   Space: O(h)
int kthSmallest(TreeNode* root, int k) {
    stack<TreeNode*> st;
    TreeNode* curr = root;
    int count = 0;
    while (curr || !st.empty()) {
        while (curr) {
            st.push(curr);
            curr = curr->left;
        }
        curr = st.top(); st.pop();
        if (++count == k) return curr->val;
        curr = curr->right;
    }
    return -1;  // k is out of bounds
}

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 14: Trees (C++)" << endl;
    cout << "========================================" << endl;

    // Build a binary tree:
    //         1
    //        / \
    //       2   3
    //      / \   \
    //     4   5   6
    TreeNode* root = buildTree({1, 2, 3, 4, 5, -1, 6});

    // --- PART A: Binary Tree ---
    cout << "\n=== PART A: Binary Tree ===" << endl;

    // --- 1. Traversals ---
    cout << "\n--- 1. Traversals ---" << endl;
    {
        vector<int> inR, preR, postR;
        inorderRecursive(root, inR);
        preorderRecursive(root, preR);
        postorderRecursive(root, postR);

        printVec(inR, "Inorder (recursive) ");
        printVec(inorderIterative(root), "Inorder (iterative) ");
        printVec(preR, "Preorder (recursive)");
        printVec(preorderIterative(root), "Preorder (iterative)");
        printVec(postR, "Postorder (recursive)");
        printVec(postorderIterative(root), "Postorder (iterative)");
    }

    // --- 2. Level Order ---
    cout << "\n--- 2. Level-Order Traversal ---" << endl;
    {
        auto levels = levelOrder(root);
        for (size_t i = 0; i < levels.size(); ++i) {
            printVec(levels[i], "  Level " + to_string(i));
        }
    }

    // --- 3. Height ---
    cout << "\n--- 3. Height ---" << endl;
    cout << "Height: " << height(root) << " (expected 3)" << endl;

    // --- 4. Diameter ---
    cout << "\n--- 4. Diameter ---" << endl;
    cout << "Diameter: " << diameter(root) << " (expected 4)" << endl;

    // --- 5. Mirror ---
    cout << "\n--- 5. Mirror/Invert ---" << endl;
    {
        vector<int> before;
        inorderRecursive(root, before);
        printVec(before, "Before mirror (inorder)");
        mirror(root);
        vector<int> after;
        inorderRecursive(root, after);
        printVec(after, "After mirror (inorder) ");
        mirror(root);  // mirror back for BST tests
    }

    freeTree(root);

    // --- PART B: Binary Search Tree ---
    cout << "\n\n=== PART B: Binary Search Tree ===" << endl;

    // Build BST by inserting: 50, 30, 70, 20, 40, 60, 80
    //          50
    //        /    \
    //      30      70
    //     / \     / \
    //   20  40  60  80
    cout << "\n--- 6. BST Insert ---" << endl;
    TreeNode* bst = nullptr;
    for (int v : {50, 30, 70, 20, 40, 60, 80}) {
        bst = bstInsert(bst, v);
    }
    printVec(inorderIterative(bst), "BST Inorder");
    // Expected: [20, 30, 40, 50, 60, 70, 80]

    // --- 7. BST Search ---
    cout << "\n--- 7. BST Search ---" << endl;
    for (int target : {40, 25, 70}) {
        TreeNode* found = bstSearch(bst, target);
        cout << "Search " << target << ": "
             << (found ? "found" : "not found") << endl;
    }

    // --- 8. BST Delete ---
    cout << "\n--- 8. BST Delete ---" << endl;
    {
        bst = bstDelete(bst, 20);  // leaf
        printVec(inorderIterative(bst), "After delete 20 (leaf)     ");

        bst = bstDelete(bst, 30);  // one child
        printVec(inorderIterative(bst), "After delete 30 (one child)");

        bst = bstDelete(bst, 50);  // two children
        printVec(inorderIterative(bst), "After delete 50 (two child)");
    }

    freeTree(bst);

    // Rebuild BST for remaining tests
    bst = nullptr;
    for (int v : {50, 30, 70, 20, 40, 60, 80}) {
        bst = bstInsert(bst, v);
    }

    // --- 9. Validate BST ---
    cout << "\n--- 9. Validate BST ---" << endl;
    cout << "Is valid BST: " << (isValidBST(bst) ? "yes" : "no") << endl;

    // Create an invalid BST
    TreeNode* invalid = new TreeNode(5,
        new TreeNode(1),
        new TreeNode(4, new TreeNode(3), new TreeNode(6)));
    cout << "Invalid tree is BST: " << (isValidBST(invalid) ? "yes" : "no") << endl;
    freeTree(invalid);

    // --- 10. LCA ---
    cout << "\n--- 10. Lowest Common Ancestor ---" << endl;
    {
        auto testLCA = [&](int p, int q) {
            TreeNode* lca = lcaBST(bst, p, q);
            cout << "LCA(" << p << ", " << q << ") = "
                 << (lca ? to_string(lca->val) : "null") << endl;
        };
        testLCA(20, 40);  // Expected: 30
        testLCA(20, 80);  // Expected: 50
        testLCA(60, 80);  // Expected: 70
        testLCA(20, 30);  // Expected: 30
    }

    // --- 11. Kth Smallest ---
    cout << "\n--- 11. Kth Smallest in BST ---" << endl;
    for (int k = 1; k <= 7; ++k) {
        cout << "  k=" << k << ": " << kthSmallest(bst, k) << endl;
    }

    freeTree(bst);

    cout << "\n========================================" << endl;
    cout << " All Week 14 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
