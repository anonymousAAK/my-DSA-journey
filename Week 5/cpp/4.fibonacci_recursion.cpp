/*
 * WEEK 5 - C++ FUNCTIONS & RECURSION
 * Topic: Fibonacci -- Naive, Memoised, Iterative
 * File: 4.fibonacci_recursion.cpp
 *
 * APPROACHES:
 *  1. Naive recursion: O(2^n).
 *  2. Memoisation: O(n) time, O(n) space.
 *  3. Iterative: O(n) time, O(1) space (with two rolling vars).
 *
 * KEY POINTS:
 *  - Use long long to delay overflow (fib(92) is the largest that fits).
 *  - Memo arrays should be sized + initialised with a sentinel (-1).
 */

#include <iostream>
#include <vector>

long long fib_naive(int n) {
    if (n <= 1) return n;
    return fib_naive(n - 1) + fib_naive(n - 2);
}

std::vector<long long> memo;
long long fib_memo(int n) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib_memo(n - 1) + fib_memo(n - 2);
}

long long fib_iter(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1;
    for (int i = 2; i <= n; ++i) {
        long long c = a + b;
        a = b; b = c;
    }
    return b;
}

int call_count = 0;
long long count_calls(int n) {
    ++call_count;
    if (n <= 1) return n;
    return count_calls(n - 1) + count_calls(n - 2);
}

int main() {
    memo.assign(100, -1);

    std::cout << "first 10 fibs: ";
    for (int i = 0; i < 10; ++i) std::cout << fib_iter(i) << ' ';
    std::cout << '\n';

    int n = 10;
    std::cout << "\nfib(" << n << "):\n";
    std::cout << "  Naive    : " << fib_naive(n) << '\n';
    std::cout << "  Memo     : " << fib_memo(n) << '\n';
    std::cout << "  Iter     : " << fib_iter(n) << '\n';

    int big = 45;
    std::cout << "\nfib(" << big << ") iter = " << fib_iter(big) << '\n';
    memo.assign(100, -1);
    std::cout << "fib(" << big << ") memo = " << fib_memo(big) << '\n';

    call_count = 0; count_calls(5);
    std::cout << "\nfib_naive(5) makes " << call_count << " recursive calls\n";
    return 0;
}

/*
 * NOTES:
 *  - Memo array sized for the maximum n you expect; resize as needed.
 *  - For n > 92, switch to __int128 or a big-integer library.
 *  - The iterative version uses O(1) extra space and is the production choice.
 */
