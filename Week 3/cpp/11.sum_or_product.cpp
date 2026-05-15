/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Sum or Product of First N Naturals
 * File: 11.sum_or_product.cpp
 *
 * PROBLEM:
 *  N and choice C: 1 -> sum, 2 -> product, else -> -1.
 *
 * KEY POINTS:
 *  - Sum identity: 0 ; product identity: 1.
 *  - Closed-forms: sum = n*(n+1)/2 ; product = n!
 *  - long long for the product to delay overflow.
 *
 * DRY RUN:
 *  N=5, C=1 -> 15
 *  N=5, C=2 -> 120
 */

#include <iostream>

int main() {
    int n, choice;
    if (!(std::cin >> n >> choice)) {
        n = 5; choice = 1;
        std::cout << "(demo N=5 C=1)\n";
    }

    if (choice == 1) {
        long long sum = (long long)n * (n + 1) / 2;
        std::cout << sum << '\n';
    } else if (choice == 2) {
        long long product = 1;
        for (int i = 2; i <= n; ++i) product *= i;
        std::cout << product << '\n';
    } else {
        std::cout << -1 << '\n';
    }
    return 0;
}

/*
 * NOTES:
 *  - 21! already overflows int64. Use BigInteger libraries for larger n.
 *  - The closed-form sum is O(1); the loop sum is O(n).
 */
