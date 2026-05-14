/*
 * WEEK 3 — C++ Advanced Loops & Number Theory Basics
 * Covers: Fibonacci, primes (with Sieve), binary conversion, bitwise operators.
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
using namespace std;

// Fibonacci — O(n) time, O(1) space
long long fibonacci(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) { long long t = a + b; a = b; b = t; }
    return b;
}

// Primality test — O(sqrt(n))
bool isPrime(int n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; (long long)i * i <= n; i += 6)
        if (n % i == 0 || n % (i + 2) == 0) return false;
    return true;
}

// Sieve of Eratosthenes — O(n log log n)
vector<int> sieve(int limit) {
    vector<bool> isP(limit + 1, true);
    isP[0] = isP[1] = false;
    for (int i = 2; (long long)i * i <= limit; i++)
        if (isP[i]) for (int j = i*i; j <= limit; j += i) isP[j] = false;
    vector<int> primes;
    for (int i = 2; i <= limit; i++) if (isP[i]) primes.push_back(i);
    return primes;
}

// Reverse number — O(d)
int reverseNumber(int n) {
    bool neg = n < 0; n = abs(n);
    int rev = 0;
    while (n > 0) { rev = rev * 10 + n % 10; n /= 10; }
    return neg ? -rev : rev;
}

// Decimal to binary string
string decToBin(int n) {
    if (n == 0) return "0";
    string s;
    while (n > 0) { s += (char)('0' + n % 2); n /= 2; }
    reverse(s.begin(), s.end());
    return s;
}

// Binary string to decimal
int binToDec(const string& s) {
    int result = 0;
    for (char c : s) result = result * 2 + (c - '0');
    return result;
}

// Count set bits — O(number of set bits) using Brian Kernighan's trick
int countSetBits(int n) {
    int count = 0;
    while (n) { n &= n - 1; count++; }
    return count;
}

int main() {
    // Fibonacci
    cout << "--- Fibonacci ---" << endl;
    cout << "First 10: ";
    for (int i = 0; i < 10; i++) cout << fibonacci(i) << " ";
    cout << endl;

    // Primes
    cout << "\n--- Primes ---" << endl;
    cout << "isPrime(17): " << boolalpha << isPrime(17) << endl;
    cout << "isPrime(20): " << isPrime(20) << endl;
    auto primes = sieve(50);
    cout << "Primes to 50: ";
    for (int p : primes) cout << p << " ";
    cout << endl;

    // Reverse
    cout << "\n--- Reverse ---" << endl;
    for (int n : {1234, -567, 1000})
        cout << "reverse(" << n << ") = " << reverseNumber(n) << endl;

    // Binary conversion
    cout << "\n--- Binary ---" << endl;
    for (int n : {0, 5, 10, 42, 255}) {
        string b = decToBin(n);
        cout << n << " -> " << b << " -> " << binToDec(b) << endl;
    }

    // Bitwise
    cout << "\n--- Bitwise ---" << endl;
    int a = 12, b = 10;
    cout << "a & b  = " << (a & b)  << endl;  // 8
    cout << "a | b  = " << (a | b)  << endl;  // 14
    cout << "a ^ b  = " << (a ^ b)  << endl;  // 6
    cout << "~a     = " << (~a)     << endl;  // -13
    cout << "a << 2 = " << (a << 2) << endl;  // 48
    cout << "a >> 2 = " << (a >> 2) << endl;  // 3

    // Bit tricks
    cout << "\nSet bits in 13: " << countSetBits(13) << endl;    // 3
    cout << "Set bits in 255: " << countSetBits(255) << endl;    // 8
    cout << "16 is power of 2: " << boolalpha << (16 > 0 && (16 & 15) == 0) << endl;
    cout << "20 is power of 2: " << (20 > 0 && (20 & 19) == 0) << endl;

    return 0;
}
