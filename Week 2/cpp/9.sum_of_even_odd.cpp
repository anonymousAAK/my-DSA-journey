/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Sum of Even / Odd Digits
 * File: 9.sum_of_even_odd.cpp
 *
 * PROBLEM:
 *  Read integer N; output the sum of even digits, then the sum of odd digits.
 *
 * CONCEPT:
 *  Repeatedly peel off the last digit with `% 10` and `/= 10`. Classify each
 *  digit by parity.
 *
 * KEY POINTS:
 *  - `%` and `/` are integer operators here.
 *  - `n` must be non-negative for the simple loop; take std::abs(n) first.
 *  - O(d) where d = number of digits.
 *
 * DRY RUN:
 *  13245 -> digits 5,4,2,3,1
 *    even = 4+2 = 6
 *    odd  = 5+3+1 = 9
 *  Output: "6 9"
 */

#include <iostream>
#include <cstdlib>

int main() {
    int n;
    if (!(std::cin >> n)) { n = 13245; std::cout << "(demo n=13245)\n"; }
    n = std::abs(n);

    int even_sum = 0, odd_sum = 0;
    while (n > 0) {
        int d = n % 10;
        if (d % 2 == 0) even_sum += d;
        else            odd_sum  += d;
        n /= 10;
    }
    std::cout << even_sum << " " << odd_sum << '\n';
    return 0;
}

/*
 * NOTES:
 *  - C++ `%` follows the sign of the dividend (like Java). Take abs() to avoid
 *    surprises with negative input.
 *  - For really large numbers (beyond long long), parse as a std::string and
 *    iterate characters instead.
 */
