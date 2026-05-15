/*
 * WEEK 12 - C++ DSA
 * Topic: Stack Implementation + Classic Problems
 * File: 1.StackImplementation.cpp
 *
 * CONCEPT:
 *   LIFO container. push/pop/top/empty all O(1). STL provides std::stack
 *   (adapter) and std::vector (which makes a great underlying container).
 *
 * KEY POINTS:
 *   - ArrayStack<T>: fixed-capacity templated stack (educational).
 *   - MinStack: track running mins in a parallel stack.
 *   - Classic problems: balanced parens, next greater, postfix eval.
 *
 * ALGORITHM / APPROACH:
 *   See Week 12 Java file — same algorithms.
 *
 * C++-SPECIFIC NOTES:
 *   - We use std::vector<int> as the implementation — it's contiguous and
 *     amortized O(1) push_back / pop_back.
 *   - std::stack<int> would be the standard library choice; we roll our own
 *     to mirror the Java exercise.
 *   - Throw std::runtime_error / std::out_of_range on misuse.
 *
 * DRY RUN:
 *   Same as Java/Python files (balanced "([]{})" -> true; NGE [4,5,2,10,8]
 *   -> [5,10,10,-1,-1]; postfix "3 4 + 2 *" -> 14).
 *
 * COMPLEXITY:
 *   push/pop/peek: O(1); next-greater & postfix overall O(n).
 */

#include <iostream>
#include <sstream>
#include <stdexcept>
#include <stack>
#include <string>
#include <vector>

// ---------- Templated array-based stack (educational) ----------

template <typename T>
class ArrayStack {
public:
    explicit ArrayStack(std::size_t capacity) : cap(capacity) { data.reserve(capacity); }
    void push(const T& x) {
        if (data.size() == cap) throw std::runtime_error("Stack overflow");
        data.push_back(x);
    }
    T pop() {
        if (data.empty()) throw std::runtime_error("Stack underflow");
        T x = data.back(); data.pop_back(); return x;
    }
    const T& peek() const {
        if (data.empty()) throw std::runtime_error("Stack is empty");
        return data.back();
    }
    bool empty() const { return data.empty(); }
    std::size_t size() const { return data.size(); }
private:
    std::size_t cap;
    std::vector<T> data;
};

// ---------- MinStack ----------

class MinStack {
public:
    void push(int x) {
        s.push(x);
        m.push(m.empty() ? x : std::min(x, m.top()));
    }
    int pop() {
        int x = s.top(); s.pop(); m.pop();
        return x;
    }
    int peek() const { return s.top(); }
    int getMin() const { return m.top(); }
private:
    std::stack<int> s, m;
};

// ---------- Classic problems ----------

bool isBalanced(const std::string& s) {
    std::stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else if (c == ')' || c == ']' || c == '}') {
            if (st.empty()) return false;
            char top = st.top(); st.pop();
            if (c == ')' && top != '(') return false;
            if (c == ']' && top != '[') return false;
            if (c == '}' && top != '{') return false;
        }
    }
    return st.empty();
}

std::vector<int> nextGreaterElement(const std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    std::vector<int> result(n, -1);
    std::stack<int> st;  // indices
    for (int i = 0; i < n; ++i) {
        while (!st.empty() && arr[i] > arr[st.top()]) {
            result[st.top()] = arr[i];
            st.pop();
        }
        st.push(i);
    }
    return result;
}

int evalPostfix(const std::string& expr) {
    std::stack<int> st;
    std::istringstream iss(expr);
    std::string tok;
    while (iss >> tok) {
        if (tok == "+" || tok == "-" || tok == "*" || tok == "/") {
            int b = st.top(); st.pop();
            int a = st.top(); st.pop();
            if (tok == "+") st.push(a + b);
            else if (tok == "-") st.push(a - b);
            else if (tok == "*") st.push(a * b);
            else st.push(a / b);  // C++ integer division truncates toward zero
        } else {
            st.push(std::stoi(tok));
        }
    }
    return st.top();
}

template<typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream os;
    os << "[";
    for (std::size_t i = 0; i < v.size(); ++i) { if (i) os << ", "; os << v[i]; }
    os << "]";
    return os.str();
}

int main() {
    // Array stack
    std::cout << "=== Array Stack ===\n";
    ArrayStack<int> as(10);
    as.push(1); as.push(2); as.push(3);
    std::cout << "peek: " << as.peek() << "\n";
    std::cout << "pop:  " << as.pop()  << "\n";
    std::cout << "pop:  " << as.pop()  << "\n";
    std::cout << "size: " << as.size() << "\n";

    // Min stack
    std::cout << "\n=== Min Stack ===\n";
    MinStack ms;
    ms.push(5); ms.push(3); ms.push(7); ms.push(2);
    std::cout << "peek: " << ms.peek() << ", min: " << ms.getMin() << "\n";
    ms.pop();
    std::cout << "After pop -- peek: " << ms.peek() << ", min: " << ms.getMin() << "\n";

    // Balanced parens
    std::cout << "\n=== Balanced Parentheses ===\n";
    for (auto& t : {std::string("([]{})"), std::string("(])"),
                    std::string("((()))"), std::string("{[}]"),
                    std::string("")}) {
        std::cout << '"' << t << "\": " << std::boolalpha << isBalanced(t) << "\n";
    }

    // Next Greater Element
    std::cout << "\n=== Next Greater Element ===\n";
    std::vector<int> arr = {4, 5, 2, 10, 8};
    std::cout << "Array: " << vec_str(arr) << "\n";
    std::cout << "NGE:   " << vec_str(nextGreaterElement(arr)) << "\n";

    // Postfix eval
    std::cout << "\n=== Postfix Evaluation ===\n";
    std::cout << "\"3 4 +\" = "        << evalPostfix("3 4 +") << "\n";
    std::cout << "\"3 4 + 2 *\" = "    << evalPostfix("3 4 + 2 *") << "\n";
    std::cout << "\"15 7 1 1 + - / 3 * 2 1 1 + + -\" = "
              << evalPostfix("15 7 1 1 + - / 3 * 2 1 1 + + -") << "\n";

    return 0;
}

/*
 * NOTES (vs. Java):
 * - Java's recommended stack is ArrayDeque; here it's std::stack adapter.
 * - Templates give us a single generic ArrayStack<T> — Java uses generics
 *   that are erased at runtime; C++ templates are monomorphized.
 * - Integer division: both Java and C++ truncate toward zero (different
 *   from Python's // which floors).
 */
