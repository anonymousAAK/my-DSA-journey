/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Total Salary Calculation
 * File: 7.total_salary.cpp
 *
 * PROBLEM:
 *  totalSalary = basic + hra + da + allow - pf
 *    hra = 20%, da = 50%, pf = 11% of basic
 *    allow = 1700/1500/1300 for grade A/B/C(else)
 *  Round to nearest integer and print.
 *
 * CONCEPT:
 *  if/else-if chain to select the allowance, then arithmetic and rounding
 *  with `std::lround` (half-away-from-zero) to match Java's `Math.round`.
 *
 * KEY POINTS:
 *  - `std::lround(x)` rounds to nearest long, half away from zero.
 *  - `std::round(x)` returns a double (also half-away-from-zero).
 *  - C++ supports `if (cond) ... else if (cond) ... else ...` exactly like Java.
 *
 * DRY RUN:
 *  basic=10000, grade='A'
 *    hra=2000, da=5000, allow=1700, pf=1100
 *    total = 17600
 *
 * COMPLEXITY: O(1).
 */

#include <iostream>
#include <cmath>

int main() {
    int basic; char grade;
    if (!(std::cin >> basic >> grade)) {
        basic = 10000; grade = 'A';
        std::cout << "(demo basic=10000 grade=A)\n";
    }

    double hra = 0.20 * basic;
    double da  = 0.50 * basic;
    double pf  = 0.11 * basic;

    int allow;
    if      (grade == 'A') allow = 1700;
    else if (grade == 'B') allow = 1500;
    else                   allow = 1300;

    double total = basic + hra + da + allow - pf;
    long   ans   = std::lround(total);   // half away from zero (like Math.round)
    std::cout << ans << '\n';
    return 0;
}

/*
 * NOTES:
 *  - Java's Math.round(double) rounds half-UP (positive infinity). C++'s
 *    std::lround rounds half AWAY FROM ZERO -- they match for positive totals.
 *  - For currency, prefer fixed-point or a decimal library; doubles incur
 *    base-2 rounding error.
 */
