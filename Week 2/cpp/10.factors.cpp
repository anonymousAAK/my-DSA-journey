/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Factors of N (excluding 1 and N)
 * File: 10.factors.cpp
 *
 * PROBLEM:
 *  Print all i in [2, n/2] such that n % i == 0.
 *
 * KEY POINTS:
 *  - Trial division loop.
 *  - The sqrt(n) optimisation cuts the work but doesn't change the answer.
 *  - O(n) brute force; O(sqrt n) optimised.
 *
 * DRY RUN:
 *  n=12 -> factors: 2 3 4 6
 *  n=7  -> (prime) no factors
 */

#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 12; std::cout << "(demo n=12)\n"; }

    // Brute force O(n/2)
    std::cout << "factors of " << n << ":";
    for (int i = 2; i <= n / 2; ++i) {
        if (n % i == 0) std::cout << ' ' << i;
    }
    std::cout << '\n';

    // O(sqrt n) variant
    std::vector<int> facs;
    for (int i = 2; (long long)i * i <= n; ++i) {
        if (n % i == 0) {
            facs.push_back(i);
            if (i != n / i) facs.push_back(n / i);
        }
    }
    std::sort(facs.begin(), facs.end());
    std::cout << "sqrt-version:";
    for (int x : facs) if (x != n) std::cout << ' ' << x;
    std::cout << '\n';
    return 0;
}

/*
 * NOTES:
 *  - `(long long)i * i` prevents overflow when computing i*i for large i.
 *  - The sqrt(n) loop emits divisors in pairs and needs a final sort.
 *  - For prime-checking, abort as soon as you find a factor.
 */
