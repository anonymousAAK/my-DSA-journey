/*
 * WEEK 2 - C++ CONTROL FLOW
 * Topic: Fahrenheit -> Celsius Table
 * File: 6.fahrenheit_to_celsius_table.cpp
 *
 * PROBLEM:
 *  Given start S, end E, step W, print (F, C) pairs where
 *  C = (F - 32) * 5 / 9, for F = S, S+W, ..., <= E.
 *
 * CONCEPT:
 *  Integer arithmetic truncates the Celsius value -- exact same behaviour
 *  as Java. For a precise float result use `(F - 32) * 5.0 / 9.0`.
 *
 * KEY POINTS:
 *  - int / int truncates toward zero.
 *  - `(int) ((F - 32) * 5.0 / 9.0)` is the precise -> truncated path.
 *  - Loop pattern: while (S <= E) { ... S += W; }
 *
 * DRY RUN:
 *  S=32, E=212, W=20
 *    F=32  -> C=0
 *    F=52  -> C=11
 *    ...
 *    F=212 -> C=100
 *
 * COMPLEXITY: O((E - S)/W).
 */

#include <iostream>

int main() {
    int S, E, W;
    if (!(std::cin >> S >> E >> W)) {
        // Demo defaults if no input piped
        S = 32; E = 212; W = 20;
        std::cout << "(demo S=32 E=212 W=20)\n";
    }
    if (W <= 0) {
        std::cerr << "step W must be > 0\n";
        return 1;
    }

    for (int F = S; F <= E; F += W) {
        int  C_int = (F - 32) * 5 / 9;            // matches Java
        double C_d = (F - 32) * 5.0 / 9.0;        // precise
        std::cout << F << " " << C_int
                  << "   (precise: " << C_d << ")\n";
    }
    return 0;
}

/*
 * NOTES:
 *  - C++ truncates int/int just like Java (toward zero).
 *  - Always pick the divisor's type carefully -- use `5.0/9.0` if you want a double.
 *  - Range-based for cannot count by W directly; we use a classic `for`.
 */
