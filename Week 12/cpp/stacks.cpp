/*
 * =============================================================================
 * Week 12 - Stacks (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Stack implementation using vector
 *   2. Balanced parentheses checker
 *   3. Next Greater Element (monotonic stack)
 *   4. Min Stack (O(1) getMin)
 *   5. Postfix (Reverse Polish Notation) evaluation
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// 1. STACK IMPLEMENTATION USING VECTOR
// =============================================================================
// All operations: O(1) amortized
template <typename T>
class Stack {
    vector<T> data_;

public:
    // Push element onto stack — O(1) amortized
    void push(const T& val) {
        data_.push_back(val);
    }

    // Pop top element — O(1)
    // Throws if empty.
    void pop() {
        if (data_.empty()) throw runtime_error("Stack underflow");
        data_.pop_back();
    }

    // Peek at top element — O(1)
    T& top() {
        if (data_.empty()) throw runtime_error("Stack is empty");
        return data_.back();
    }

    const T& top() const {
        if (data_.empty()) throw runtime_error("Stack is empty");
        return data_.back();
    }

    bool empty() const { return data_.empty(); }
    size_t size() const { return data_.size(); }
};

// =============================================================================
// 2. BALANCED PARENTHESES
// =============================================================================
// Checks if a string of brackets (){}[] is balanced.
// Time: O(n)   Space: O(n) worst case
bool isBalanced(const string& s) {
    stack<char> st;
    unordered_map<char, char> match = {{')', '('}, {'}', '{'}, {']', '['}};

    for (char c : s) {
        if (c == '(' || c == '{' || c == '[') {
            st.push(c);
        } else if (match.count(c)) {
            if (st.empty() || st.top() != match[c]) return false;
            st.pop();
        }
        // Ignore non-bracket characters
    }
    return st.empty();
}

// =============================================================================
// 3. NEXT GREATER ELEMENT (Monotonic Stack)
// =============================================================================
// For each element, find the next element to the right that is greater.
// If none, the result is -1.
// Time: O(n)   Space: O(n)
//
// Key insight: maintain a monotonically decreasing stack. When we encounter
// an element greater than stack top, it is the "next greater" for that top.
vector<int> nextGreaterElement(const vector<int>& arr) {
    int n = arr.size();
    vector<int> result(n, -1);
    stack<int> st;  // stores indices

    for (int i = 0; i < n; ++i) {
        // Pop all elements smaller than arr[i]; arr[i] is their next greater
        while (!st.empty() && arr[st.top()] < arr[i]) {
            result[st.top()] = arr[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}

// Next Greater Element (circular array variant)
// Time: O(n)   Space: O(n)
vector<int> nextGreaterElementCircular(const vector<int>& arr) {
    int n = arr.size();
    vector<int> result(n, -1);
    stack<int> st;

    // Traverse the array twice to simulate circular behavior
    for (int i = 0; i < 2 * n; ++i) {
        int idx = i % n;
        while (!st.empty() && arr[st.top()] < arr[idx]) {
            result[st.top()] = arr[idx];
            st.pop();
        }
        if (i < n) st.push(i);  // only push during first pass
    }
    return result;
}

// =============================================================================
// 4. MIN STACK
// =============================================================================
// Stack that supports push, pop, top, and getMin in O(1).
// Space: O(n) for the auxiliary min stack.
//
// Optimization: instead of storing every min, only push to minStack when
// the new value is <= current min. Pop from minStack only when the popped
// value equals current min.
class MinStack {
    stack<int> mainStack_;
    stack<int> minStack_;

public:
    // Push — O(1)
    void push(int val) {
        mainStack_.push(val);
        if (minStack_.empty() || val <= minStack_.top()) {
            minStack_.push(val);
        }
    }

    // Pop — O(1)
    void pop() {
        if (mainStack_.empty()) throw runtime_error("Stack underflow");
        if (mainStack_.top() == minStack_.top()) {
            minStack_.pop();
        }
        mainStack_.pop();
    }

    // Top — O(1)
    int top() const {
        if (mainStack_.empty()) throw runtime_error("Stack is empty");
        return mainStack_.top();
    }

    // Get minimum — O(1)
    int getMin() const {
        if (minStack_.empty()) throw runtime_error("Stack is empty");
        return minStack_.top();
    }

    bool empty() const { return mainStack_.empty(); }
};

// =============================================================================
// 5. POSTFIX EXPRESSION EVALUATION
// =============================================================================
// Evaluate a Reverse Polish Notation expression.
// Tokens are numbers and operators (+, -, *, /).
// Time: O(n)   Space: O(n) for the stack
int evalPostfix(const vector<string>& tokens) {
    stack<int> st;

    for (const auto& token : tokens) {
        if (token == "+" || token == "-" || token == "*" || token == "/") {
            // Pop two operands (note order: second is popped first)
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();
            int result;
            if (token == "+") result = a + b;
            else if (token == "-") result = a - b;
            else if (token == "*") result = a * b;
            else result = a / b;  // integer division (truncates toward zero)
            st.push(result);
        } else {
            st.push(stoi(token));
        }
    }
    return st.top();
}

// =============================================================================
// HELPER: print vector
// =============================================================================
void printVec(const vector<int>& v, const string& label = "") {
    if (!label.empty()) cout << label << ": ";
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        cout << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    cout << "]" << endl;
}

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 12: Stacks (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Custom Stack ---
    cout << "\n--- 1. Stack Implementation ---" << endl;
    {
        Stack<int> st;
        for (int x : {10, 20, 30, 40}) st.push(x);
        cout << "Top: " << st.top() << " (expected 40)" << endl;
        cout << "Size: " << st.size() << " (expected 4)" << endl;
        st.pop();
        cout << "After pop, top: " << st.top() << " (expected 30)" << endl;

        // Test with strings
        Stack<string> strSt;
        strSt.push("hello");
        strSt.push("world");
        cout << "String stack top: " << strSt.top() << endl;
    }

    // --- 2. Balanced Parentheses ---
    cout << "\n--- 2. Balanced Parentheses ---" << endl;
    {
        vector<pair<string, bool>> tests = {
            {"()", true},
            {"()[]{}", true},
            {"(]", false},
            {"([)]", false},
            {"{[]}", true},
            {"", true},
            {"((()))", true},
            {"({[})", false},
        };
        for (const auto& [expr, expected] : tests) {
            bool result = isBalanced(expr);
            cout << "\"" << expr << "\" -> "
                 << (result ? "balanced" : "not balanced")
                 << (result == expected ? "  [PASS]" : "  [FAIL]") << endl;
        }
    }

    // --- 3. Next Greater Element ---
    cout << "\n--- 3. Next Greater Element ---" << endl;
    {
        vector<int> arr = {4, 5, 2, 25, 7, 18};
        printVec(arr, "Array");
        printVec(nextGreaterElement(arr), "NGE  ");
        // Expected: [5, 25, 25, -1, 18, -1]

        vector<int> arr2 = {1, 3, 2, 4};
        printVec(arr2, "Array");
        printVec(nextGreaterElement(arr2), "NGE  ");
        // Expected: [3, 4, 4, -1]

        cout << "\nCircular NGE:" << endl;
        vector<int> arr3 = {1, 2, 1};
        printVec(arr3, "Array");
        printVec(nextGreaterElementCircular(arr3), "NGE  ");
        // Expected: [2, -1, 2]

        vector<int> arr4 = {3, 1, 2, 4};
        printVec(arr4, "Array");
        printVec(nextGreaterElementCircular(arr4), "NGE  ");
        // Expected: [4, 2, 4, -1]
    }

    // --- 4. Min Stack ---
    cout << "\n--- 4. Min Stack ---" << endl;
    {
        MinStack ms;
        ms.push(5);
        cout << "Push 5, min = " << ms.getMin() << endl;
        ms.push(3);
        cout << "Push 3, min = " << ms.getMin() << endl;
        ms.push(7);
        cout << "Push 7, min = " << ms.getMin() << endl;
        ms.push(2);
        cout << "Push 2, min = " << ms.getMin() << endl;
        ms.push(2);
        cout << "Push 2, min = " << ms.getMin() << endl;
        ms.pop();
        cout << "Pop,    min = " << ms.getMin() << " (still 2)" << endl;
        ms.pop();
        cout << "Pop,    min = " << ms.getMin() << " (back to 3)" << endl;
        ms.pop();
        cout << "Pop,    min = " << ms.getMin() << " (still 3)" << endl;
        ms.pop();
        cout << "Pop,    min = " << ms.getMin() << " (back to 5)" << endl;
    }

    // --- 5. Postfix Evaluation ---
    cout << "\n--- 5. Postfix Evaluation ---" << endl;
    {
        // "3 4 + 2 * 7 /" => ((3+4)*2)/7 = 2
        vector<string> expr1 = {"3", "4", "+", "2", "*", "7", "/"};
        cout << "3 4 + 2 * 7 / = " << evalPostfix(expr1) << " (expected 2)" << endl;

        // "2 1 + 3 *" => (2+1)*3 = 9
        vector<string> expr2 = {"2", "1", "+", "3", "*"};
        cout << "2 1 + 3 * = " << evalPostfix(expr2) << " (expected 9)" << endl;

        // "4 13 5 / +" => 4+(13/5) = 6
        vector<string> expr3 = {"4", "13", "5", "/", "+"};
        cout << "4 13 5 / + = " << evalPostfix(expr3) << " (expected 6)" << endl;

        // "10 6 9 3 + -11 * / * 17 + 5 +"
        vector<string> expr4 = {"10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"};
        cout << "10 6 9 3 + -11 * / * 17 + 5 + = " << evalPostfix(expr4)
             << " (expected 22)" << endl;
    }

    cout << "\n========================================" << endl;
    cout << " All Week 12 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
