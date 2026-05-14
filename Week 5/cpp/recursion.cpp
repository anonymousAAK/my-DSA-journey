/*
 * =============================================================================
 * Week 5 - Functions & Recursion (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Factorial (recursive + iterative)
 *   2. Fibonacci (naive recursive, memoized, iterative)
 *   3. Tower of Hanoi
 *   4. Fast Power (exponentiation by squaring)
 *   5. Recursion Patterns:
 *      - Reverse a string
 *      - Digit sum
 *      - Palindrome check
 *      - Generate all subsets (power set)
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// 1. FACTORIAL
// =============================================================================

// Recursive factorial
// Time: O(n)   Space: O(n) call stack
long long factorialRecursive(int n) {
    if (n <= 1) return 1;
    return static_cast<long long>(n) * factorialRecursive(n - 1);
}

// Iterative factorial
// Time: O(n)   Space: O(1)
long long factorialIterative(int n) {
    long long result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}

// =============================================================================
// 2. FIBONACCI
// =============================================================================

// Naive recursive fibonacci
// Time: O(2^n) — exponential, many overlapping subproblems
// Space: O(n)  — call stack depth
long long fibNaive(int n) {
    if (n <= 1) return n;
    return fibNaive(n - 1) + fibNaive(n - 2);
}

// Memoized fibonacci (top-down DP)
// Time: O(n)   Space: O(n) memo table + O(n) call stack
long long fibMemo(int n, unordered_map<int, long long>& memo) {
    if (n <= 1) return n;
    if (auto it = memo.find(n); it != memo.end()) {
        return it->second;  // C++17 init-statement in if
    }
    memo[n] = fibMemo(n - 1, memo) + fibMemo(n - 2, memo);
    return memo[n];
}

// Convenience wrapper
long long fibMemo(int n) {
    unordered_map<int, long long> memo;
    return fibMemo(n, memo);
}

// Iterative fibonacci (bottom-up)
// Time: O(n)   Space: O(1)
long long fibIterative(int n) {
    if (n <= 1) return n;
    long long prev2 = 0, prev1 = 1;
    for (int i = 2; i <= n; ++i) {
        long long curr = prev1 + prev2;
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}

// =============================================================================
// 3. TOWER OF HANOI
// =============================================================================

// Classic Tower of Hanoi
// Time: O(2^n)   Space: O(n) call stack
// Moves n disks from 'source' to 'target' using 'auxiliary'
void towerOfHanoi(int n, char source, char target, char auxiliary,
                  vector<string>& moves) {
    if (n == 0) return;
    towerOfHanoi(n - 1, source, auxiliary, target, moves);
    moves.push_back(string(1, source) + " -> " + string(1, target));
    towerOfHanoi(n - 1, auxiliary, target, source, moves);
}

// =============================================================================
// 4. FAST POWER (Exponentiation by Squaring)
// =============================================================================

// Recursive fast power
// Time: O(log n)   Space: O(log n) call stack
// Computes base^exp % mod
long long fastPowRecursive(long long base, long long exp, long long mod) {
    if (exp == 0) return 1;
    long long half = fastPowRecursive(base, exp / 2, mod);
    half = (half * half) % mod;
    if (exp % 2 == 1) {
        half = (half * (base % mod)) % mod;
    }
    return half;
}

// Iterative fast power
// Time: O(log n)   Space: O(1)
long long fastPowIterative(long long base, long long exp, long long mod) {
    long long result = 1;
    base %= mod;
    while (exp > 0) {
        if (exp & 1) {
            result = (result * base) % mod;
        }
        exp >>= 1;
        base = (base * base) % mod;
    }
    return result;
}

// =============================================================================
// 5. RECURSION PATTERNS
// =============================================================================

// --- 5a. Reverse a string recursively ---
// Time: O(n)   Space: O(n) call stack + O(n) for new strings
string reverseStringRecursive(const string& s) {
    if (s.size() <= 1) return s;
    return reverseStringRecursive(s.substr(1)) + s[0];
}

// In-place reverse using recursion (two-pointer style)
// Time: O(n)   Space: O(n) call stack
void reverseInPlace(string& s, int left, int right) {
    if (left >= right) return;
    swap(s[left], s[right]);
    reverseInPlace(s, left + 1, right - 1);
}

// --- 5b. Digit sum ---
// Time: O(log10(n)) i.e. number of digits   Space: O(log10(n)) call stack
int digitSum(int n) {
    if (n < 0) n = -n;  // handle negative
    if (n < 10) return n;
    return (n % 10) + digitSum(n / 10);
}

// --- 5c. Palindrome check (recursive) ---
// Time: O(n)   Space: O(n) call stack
bool isPalindromeRecursive(const string& s, int left, int right) {
    if (left >= right) return true;
    if (s[left] != s[right]) return false;
    return isPalindromeRecursive(s, left + 1, right - 1);
}

bool isPalindromeRecursive(const string& s) {
    return isPalindromeRecursive(s, 0, static_cast<int>(s.size()) - 1);
}

// --- 5d. Generate all subsets (power set) ---
// Time: O(n * 2^n)  — 2^n subsets, each up to size n
// Space: O(n * 2^n) for storing all subsets + O(n) recursion depth
void generateSubsets(const vector<int>& nums, int index,
                     vector<int>& current, vector<vector<int>>& result) {
    if (index == static_cast<int>(nums.size())) {
        result.push_back(current);
        return;
    }
    // Exclude nums[index]
    generateSubsets(nums, index + 1, current, result);
    // Include nums[index]
    current.push_back(nums[index]);
    generateSubsets(nums, index + 1, current, result);
    current.pop_back();  // backtrack
}

vector<vector<int>> allSubsets(const vector<int>& nums) {
    vector<vector<int>> result;
    vector<int> current;
    generateSubsets(nums, 0, current, result);
    return result;
}

// Iterative subset generation using bitmask
// Time: O(n * 2^n)   Space: O(n * 2^n) for result
vector<vector<int>> allSubsetsBitmask(const vector<int>& nums) {
    int n = nums.size();
    int total = 1 << n;  // 2^n
    vector<vector<int>> result;
    result.reserve(total);
    for (int mask = 0; mask < total; ++mask) {
        vector<int> subset;
        for (int i = 0; i < n; ++i) {
            if (mask & (1 << i)) {
                subset.push_back(nums[i]);
            }
        }
        result.push_back(move(subset));
    }
    return result;
}

// =============================================================================
// HELPER: print a vector
// =============================================================================
template <typename T>
void printVec(const vector<T>& v, const string& label = "") {
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
    cout << " Week 5: Functions & Recursion (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Factorial ---
    cout << "\n--- 1. Factorial ---" << endl;
    for (int n : {0, 1, 5, 10, 20}) {
        cout << n << "! = " << factorialRecursive(n)
             << "  (iterative: " << factorialIterative(n) << ")" << endl;
    }

    // --- 2. Fibonacci ---
    cout << "\n--- 2. Fibonacci ---" << endl;
    cout << "Naive (small n only): ";
    for (int i = 0; i <= 10; ++i) cout << fibNaive(i) << " ";
    cout << endl;

    cout << "Memoized:             ";
    for (int i = 0; i <= 10; ++i) cout << fibMemo(i) << " ";
    cout << endl;

    cout << "Iterative:            ";
    for (int i = 0; i <= 10; ++i) cout << fibIterative(i) << " ";
    cout << endl;

    cout << "fib(40) memoized  = " << fibMemo(40) << endl;
    cout << "fib(40) iterative = " << fibIterative(40) << endl;

    // --- 3. Tower of Hanoi ---
    cout << "\n--- 3. Tower of Hanoi (3 disks) ---" << endl;
    {
        vector<string> moves;
        towerOfHanoi(3, 'A', 'C', 'B', moves);
        for (const auto& m : moves) cout << "  " << m << endl;
        cout << "Total moves: " << moves.size() << " (expected 2^3 - 1 = 7)" << endl;
    }

    // --- 4. Fast Power ---
    cout << "\n--- 4. Fast Power ---" << endl;
    {
        long long mod = 1'000'000'007;
        cout << "2^10 mod 1e9+7 = " << fastPowRecursive(2, 10, mod)
             << " (expected 1024)" << endl;
        cout << "3^20 mod 1e9+7 = " << fastPowIterative(3, 20, mod)
             << " (expected " << (long long)pow(3, 20) << ")" << endl;
        cout << "2^30 iterative = " << fastPowIterative(2, 30, mod)
             << " (expected 1073741824)" << endl;
    }

    // --- 5a. Reverse String ---
    cout << "\n--- 5a. Reverse String ---" << endl;
    {
        string s = "recursion";
        cout << "Original: " << s << endl;
        cout << "Reversed (recursive copy): " << reverseStringRecursive(s) << endl;
        string s2 = s;
        reverseInPlace(s2, 0, s2.size() - 1);
        cout << "Reversed (in-place):       " << s2 << endl;
    }

    // --- 5b. Digit Sum ---
    cout << "\n--- 5b. Digit Sum ---" << endl;
    for (int n : {0, 7, 123, 9999, -456}) {
        cout << "digitSum(" << n << ") = " << digitSum(n) << endl;
    }

    // --- 5c. Palindrome Check ---
    cout << "\n--- 5c. Palindrome (Recursive) ---" << endl;
    for (const auto& s : {"racecar", "hello", "madam", "a", ""}) {
        cout << "\"" << s << "\" -> "
             << (isPalindromeRecursive(s) ? "palindrome" : "not palindrome") << endl;
    }

    // --- 5d. Subsets ---
    cout << "\n--- 5d. All Subsets ---" << endl;
    {
        vector<int> nums = {1, 2, 3};
        auto subs = allSubsets(nums);
        cout << "Recursive subsets of {1,2,3} (" << subs.size() << " total):" << endl;
        for (const auto& sub : subs) printVec(sub, "  ");

        cout << "\nBitmask subsets of {1,2,3}:" << endl;
        auto subs2 = allSubsetsBitmask(nums);
        for (const auto& sub : subs2) printVec(sub, "  ");
    }

    cout << "\n========================================" << endl;
    cout << " All Week 5 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
