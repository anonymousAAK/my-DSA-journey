/*
 * WEEK 2 — C++ Control Flow & Loops
 * Covers: if/else, while/do-while/for, break/continue, switch
 * Equivalent to Java Week 2.
 */

#include <iostream>
#include <cmath>
#include <vector>
using namespace std;

// Sum even and odd digits — O(d) time, O(1) space
pair<int, int> sumEvenOddDigits(int n) {
    int evenSum = 0, oddSum = 0;
    n = abs(n);
    while (n > 0) {
        int digit = n % 10;
        if (digit % 2 == 0) evenSum += digit;
        else oddSum += digit;
        n /= 10;
    }
    return {evenSum, oddSum};
}

// All factors — O(sqrt(n)) time
vector<int> factors(int n) {
    vector<int> result;
    for (int i = 1; i * i <= n; i++) {
        if (n % i == 0) {
            result.push_back(i);
            if (i != n / i) result.push_back(n / i);
        }
    }
    sort(result.begin(), result.end());
    return result;
}

// Power x^n — O(n) time
long long power(int x, int n) {
    long long result = 1;
    for (int i = 0; i < n; i++) result *= x;
    return result;
}

int main() {
    // --- If / Else ---
    int x = 42;
    if (x > 100) cout << "Big" << endl;
    else if (x > 10) cout << "Medium" << endl;
    else cout << "Small" << endl;

    // Ternary
    string status = (x % 2 == 0) ? "even" : "odd";
    cout << x << " is " << status << endl;

    // --- While Loop: Multiplication Table ---
    cout << "\n--- While Loop ---" << endl;
    int n = 7, i = 1;
    while (i <= 10) {
        cout << n << " x " << i << " = " << n * i << endl;
        i++;
    }

    // --- For Loop ---
    cout << "\n--- For Loop ---" << endl;
    cout << "1 to 5: ";
    for (int i = 1; i <= 5; i++) cout << i << " ";
    cout << endl;

    cout << "5 to 1: ";
    for (int i = 5; i >= 1; i--) cout << i << " ";
    cout << endl;

    cout << "Even 0-10: ";
    for (int i = 0; i <= 10; i += 2) cout << i << " ";
    cout << endl;

    // --- Sum Even/Odd Digits ---
    cout << "\n--- Even/Odd Digit Sum ---" << endl;
    int nums[] = {1234, 9876, 555};
    for (int num : nums) {
        auto [e, o] = sumEvenOddDigits(num); // C++17 structured bindings
        cout << num << ": even=" << e << ", odd=" << o << endl;
    }

    // --- Factors ---
    cout << "\n--- Factors ---" << endl;
    for (int num : {12, 28, 7}) {
        cout << "Factors of " << num << ": ";
        for (int f : factors(num)) cout << f << " ";
        cout << endl;
    }

    // --- Power ---
    cout << "\n--- Power ---" << endl;
    cout << "2^10 = " << power(2, 10) << endl;
    cout << "3^5 = " << power(3, 5) << endl;

    // --- F to C table ---
    cout << "\n--- F to C ---" << endl;
    printf("%5s | %8s\n", "F", "C");
    for (int f = 32; f <= 212; f += 20) {
        double c = (f - 32) * 5.0 / 9.0;
        printf("%5d | %8.2f\n", f, c);
    }

    // --- Break / Continue ---
    cout << "\n--- Break: first prime after 20 ---" << endl;
    for (int n = 21; n < 100; n++) {
        bool isPrime = true;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) { isPrime = false; break; }
        }
        if (isPrime) { cout << n << endl; break; }
    }

    cout << "Non-multiples of 3 (1-15): ";
    for (int i = 1; i <= 15; i++) {
        if (i % 3 == 0) continue;
        cout << i << " ";
    }
    cout << endl;

    // --- Switch ---
    cout << "\n--- Switch ---" << endl;
    int day = 3;
    switch (day) {
        case 1: cout << "Monday" << endl; break;
        case 2: cout << "Tuesday" << endl; break;
        case 3: cout << "Wednesday" << endl; break;
        default: cout << "Other" << endl;
    }

    return 0;
}
