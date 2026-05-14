/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: Increment / Decrement Operators
 * File: 6.increment_decrement_operator.cpp
 *
 * CONCEPT:
 *  C++ has both prefix (++a, --a) and postfix (a++, a--) forms. Prefix
 *  modifies first, then yields the new value; postfix yields the OLD value
 *  and then modifies. For built-in ints there's no performance difference,
 *  but for iterators / heavy types prefer prefix.
 *
 * KEY POINTS:
 *  - ++a   -> increment, return new value
 *  - a++   -> return old value, then increment
 *  - In a for-loop header (`++i` vs `i++`), the result is identical because
 *    the value isn't used.
 *  - Order of evaluation in complex expressions like `a + a++` is UNSEQUENCED
 *    in C++ -- this is undefined behaviour (Java guarantees left-to-right).
 *
 * DRY RUN:
 *  a = 5
 *  cout << a++  -> prints 5, a becomes 6
 *  cout << ++a  -> a becomes 7, prints 7
 */

#include <iostream>
#include <vector>

int main() {
    int a = 5;
    std::cout << "initial a = " << a << '\n';

    std::cout << "a++  = " << a++ << '\n';   // prints 5, a -> 6
    std::cout << "now a = " << a << '\n';

    std::cout << "++a  = " << ++a << '\n';   // a -> 7, prints 7
    std::cout << "now a = " << a << '\n';

    std::cout << "a--  = " << a-- << '\n';   // prints 7, a -> 6
    std::cout << "now a = " << a << '\n';

    std::cout << "--a  = " << --a << '\n';   // a -> 5, prints 5
    std::cout << "now a = " << a << '\n';

    // In loops -- prefer prefix for non-trivial types
    std::vector<int> v {10, 20, 30, 40, 50};
    std::cout << "i++ loop: ";
    for (size_t i = 0; i < v.size(); i++) std::cout << v[i] << ' ';
    std::cout << '\n';
    std::cout << "++i loop: ";
    for (size_t i = 0; i < v.size(); ++i) std::cout << v[i] << ' ';
    std::cout << '\n';

    return 0;
}

/*
 * NOTES:
 *  - For built-in types there's no perf difference; use whichever is clearer.
 *  - For iterators (`++it`) and complex types prefer PREFIX because the
 *    postfix version creates a temporary copy.
 *  - DO NOT mix multiple unsequenced modifications of the same variable in
 *    one expression: `a = a++ + ++a;` is UB.
 */
