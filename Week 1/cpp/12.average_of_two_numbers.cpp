/*
 * WEEK 1 - C++ FUNDAMENTALS
 * Topic: Average of Three Numbers
 * File: 12.average_of_two_numbers.cpp
 *
 * CONCEPT:
 * Read a name and three integers, then print the name and the average.
 * Be careful: `(a+b+c)/3` truncates because all operands are int.
 * Use `(a+b+c) / 3.0` (double divisor) to get a true mean.
 *
 * KEY POINTS:
 *  - int / int  -> int (truncated toward zero)
 *  - int / double -> double (mixed-type promotion)
 *  - `std::cout` prints int and double with sensible defaults
 *  - For controlled precision use `std::fixed << std::setprecision(2)`
 *
 * SYNTAX:
 *   int avg_int    = (a+b+c) / 3;       // truncated
 *   double avg_dbl = (a+b+c) / 3.0;      // exact (within double precision)
 *
 * DRY RUN:
 *  Stdin: "Bob 10 11 12"
 *    sum=33, int avg=11, double avg=11.0
 *  Stdin: "Bob 10 11 11"
 *    sum=32, int avg=10, double avg=10.6666...
 *
 * COMPLEXITY: O(1)
 */

#include <iostream>
#include <iomanip>
#include <string>

int main() {
    std::string name;
    int a, b, c;
    std::cin >> name >> a >> b >> c;

    int    avg_int = (a + b + c) / 3;       // Java-style int division
    double avg_dbl = (a + b + c) / 3.0;     // promoted to double

    std::cout << name << '\n';
    std::cout << "int average    = " << avg_int << '\n';
    std::cout << std::fixed << std::setprecision(4)
              << "double average = " << avg_dbl << '\n';

    return 0;
}

/*
 * NOTES:
 *  - The `/3.0` trick works in C++ exactly the same as in Java.
 *  - `std::fixed` + `std::setprecision(n)` are persistent stream manipulators.
 *  - For statistical helpers (mean, median) C++ has nothing in <numeric> for
 *    averages directly; you'd typically use `std::accumulate(...) / N`.
 */
