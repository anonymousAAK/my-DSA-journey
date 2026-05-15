/*
 * WEEK 5 - C++ FUNCTIONS & RECURSION
 * Topic: Common Recursion Patterns
 * File: 6.recursion_patterns.cpp
 *
 * PATTERNS:
 *  1. Linear (one self-call per invocation)
 *  2. Tail recursion (with accumulator)
 *  3. Mutual recursion (A calls B, B calls A)
 *  4. Helper / accumulator
 *  5. Subset enumeration (foundation of backtracking)
 *  6. Two-pointer recursion (palindrome)
 */

#include <iostream>
#include <string>
#include <vector>

// 1. Linear -- reverse a string
std::string reverse_str(const std::string& s) {
    if (s.empty()) return "";
    return reverse_str(s.substr(1)) + s[0];
}

// 2. Tail recursion via accumulator
long long fact_tail(int n, long long acc = 1) {
    if (n <= 1) return acc;
    return fact_tail(n - 1, n * acc);
}

// 3. Mutual recursion
bool is_odd(int n);
bool is_even(int n) { return n == 0 ? true : is_odd(n - 1); }
bool is_odd (int n) { return n == 0 ? false : is_even(n - 1); }

// 4. Helper -- digit sum
int digit_sum(int n) {
    if (n == 0) return 0;
    return (n % 10) + digit_sum(n / 10);
}

// 5. Subsets
void subsets(const std::vector<int>& arr, size_t idx, std::vector<int>& current) {
    if (idx == arr.size()) {
        std::cout << "{";
        for (size_t i = 0; i < current.size(); ++i) {
            if (i) std::cout << ",";
            std::cout << current[i];
        }
        std::cout << "}\n";
        return;
    }
    // exclude
    subsets(arr, idx + 1, current);
    // include
    current.push_back(arr[idx]);
    subsets(arr, idx + 1, current);
    current.pop_back();         // backtrack
}

// 6. Palindrome via two pointers
bool is_palindrome(const std::string& s, int left, int right) {
    if (left >= right) return true;
    if (s[left] != s[right]) return false;
    return is_palindrome(s, left + 1, right - 1);
}

int main() {
    std::cout << "reverse('hello') = " << reverse_str("hello") << '\n';
    std::cout << "fact_tail(5)   = " << fact_tail(5) << '\n';
    std::cout << "fact_tail(10)  = " << fact_tail(10) << '\n';
    std::cout << "is_even(4) = " << std::boolalpha << is_even(4) << '\n';
    std::cout << "is_odd(7)  = " << is_odd(7) << '\n';
    std::cout << "digit_sum(1234) = " << digit_sum(1234) << '\n';

    std::cout << "\nAll subsets of {1, 2, 3}:\n";
    std::vector<int> arr {1, 2, 3};
    std::vector<int> current;
    subsets(arr, 0, current);

    std::cout << "\nis_palindrome('racecar') = " << is_palindrome("racecar", 0, 6) << '\n';
    std::cout << "is_palindrome('hello')   = " << is_palindrome("hello",   0, 4) << '\n';

    return 0;
}

/*
 * NOTES:
 *  - C++ doesn't optimise tail calls reliably; use loops if depth matters.
 *  - The subset pattern is classic backtracking -- include/exclude tree.
 *  - For permutations / combinations, std::next_permutation and the
 *    <algorithm> header have non-recursive helpers.
 */
