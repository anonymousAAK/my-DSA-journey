/*
 * WEEK 1 — C++ Fundamentals
 * Equivalent to Java Week 1: hello world, variables, data types, operators, I/O.
 *
 * C++ is statically typed, compiled, and gives low-level memory control.
 * It's the dominant language in competitive programming.
 *
 * Compile: g++ -std=c++17 -O2 -o fundamentals fundamentals.cpp
 * Run:     ./fundamentals
 */

#include <iostream>
#include <string>
#include <cmath>       // for pow, sqrt
#include <climits>     // for INT_MAX, INT_MIN
#include <cfloat>      // for DBL_MAX
#include <typeinfo>    // for typeid

using namespace std;

int main() {
    // --- Hello World ---
    cout << "Hello, World!" << endl;

    // --- Variables ---
    // C++ has explicit types like Java, but also has 'auto' for type inference
    int age = 25;
    double height = 5.9;
    char grade = 'A';          // single character (unlike Python, C++ has char)
    bool isStudent = true;
    string name = "Alice";     // std::string (not char*)
    auto score = 95.5;         // compiler deduces: double

    cout << "Name: " << name << ", Age: " << age
         << ", Height: " << height << ", Grade: " << grade << endl;

    // --- Data Types and Sizes ---
    cout << "\n--- Data Type Sizes ---" << endl;
    cout << "char:      " << sizeof(char)      << " byte(s)"  << endl;  // 1
    cout << "short:     " << sizeof(short)     << " byte(s)"  << endl;  // 2
    cout << "int:       " << sizeof(int)       << " byte(s)"  << endl;  // 4
    cout << "long long: " << sizeof(long long) << " byte(s)"  << endl;  // 8
    cout << "float:     " << sizeof(float)     << " byte(s)"  << endl;  // 4
    cout << "double:    " << sizeof(double)    << " byte(s)"  << endl;  // 8
    cout << "bool:      " << sizeof(bool)      << " byte(s)"  << endl;  // 1

    // Ranges
    cout << "\nint range:       [" << INT_MIN << ", " << INT_MAX << "]" << endl;
    cout << "long long range: [" << LLONG_MIN << ", " << LLONG_MAX << "]" << endl;

    // --- Type Casting ---
    double pi = 3.14159;
    int truncated = (int)pi;                // C-style cast: 3
    int truncated2 = static_cast<int>(pi);  // C++ style (preferred)
    double promoted = (double)age;           // int → double

    cout << "\n--- Type Casting ---" << endl;
    cout << "(int)3.14159 = " << truncated << endl;
    cout << "(double)25   = " << promoted << endl;
    cout << "5 / 2   = " << (5 / 2)   << " (integer division)" << endl;
    cout << "5.0 / 2 = " << (5.0 / 2) << " (float division)" << endl;

    // --- Arithmetic Operators ---
    int a = 17, b = 5;
    cout << "\n--- Arithmetic (" << a << " and " << b << ") ---" << endl;
    cout << "a + b  = " << (a + b)  << endl;  // 22
    cout << "a - b  = " << (a - b)  << endl;  // 12
    cout << "a * b  = " << (a * b)  << endl;  // 85
    cout << "a / b  = " << (a / b)  << endl;  // 3 (integer division!)
    cout << "a % b  = " << (a % b)  << endl;  // 2
    cout << "pow(a,b) = " << pow(a, b) << endl; // 1419857 (from <cmath>)

    // --- Comparison & Logical ---
    cout << "\n--- Comparison ---" << endl;
    cout << boolalpha;  // print true/false instead of 1/0
    cout << "5 == 5: " << (5 == 5) << endl;
    cout << "5 != 3: " << (5 != 3) << endl;
    cout << "5 > 3:  " << (5 > 3)  << endl;

    cout << "\n--- Logical ---" << endl;
    cout << "true && false: " << (true && false) << endl;
    cout << "true || false: " << (true || false) << endl;
    cout << "!true:         " << (!true) << endl;

    // --- Bitwise Operators ---
    cout << "\n--- Bitwise ---" << endl;
    cout << "5 & 3  = " << (5 & 3)  << endl;  // 1
    cout << "5 | 3  = " << (5 | 3)  << endl;  // 7
    cout << "5 ^ 3  = " << (5 ^ 3)  << endl;  // 6
    cout << "~5     = " << (~5)     << endl;   // -6
    cout << "5 << 1 = " << (5 << 1) << endl;   // 10
    cout << "5 >> 1 = " << (5 >> 1) << endl;   // 2

    // --- User Input ---
    cout << "\n--- Input ---" << endl;
    cout << "Enter a number: ";
    int num;
    if (cin >> num) {
        cout << "Double of " << num << " is " << num * 2 << endl;
    } else {
        cout << "(No input available)" << endl;
    }

    // --- String Operations ---
    string s = "Hello, C++!";
    cout << "\n--- String Operations ---" << endl;
    cout << "String:   " << s << endl;
    cout << "Length:   " << s.length() << endl;
    cout << "s[0]:     " << s[0] << endl;
    cout << "substr:   " << s.substr(0, 5) << endl;  // "Hello"
    cout << "find:     " << s.find("C++") << endl;    // 7
    cout << "append:   " << (s + " Welcome!") << endl;

    // Reverse a string
    string rev = s;
    reverse(rev.begin(), rev.end());
    cout << "Reversed: " << rev << endl;

    // --- Arrays (C-style and std::vector preview) ---
    int arr[] = {10, 20, 30, 40, 50};
    int arrSize = sizeof(arr) / sizeof(arr[0]);
    cout << "\n--- Array ---" << endl;
    cout << "Array: ";
    for (int i = 0; i < arrSize; i++) cout << arr[i] << " ";
    cout << endl;

    // Range-based for loop (C++11)
    cout << "Range-based: ";
    for (int x : arr) cout << x << " ";
    cout << endl;

    return 0;
}
