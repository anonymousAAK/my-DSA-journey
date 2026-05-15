/*
 * WEEK 3 - C++ LOOPS & NUMBER THEORY
 * Topic: All Prime Numbers up to N
 * File: 10.all_prime_number.cpp
 *
 * PROBLEM:
 *  Print every prime in [2, N], one per line.
 *
 * KEY POINTS:
 *  - Trial division (naive O(N^2) or O(N*sqrt N)).
 *  - Sieve of Eratosthenes O(N log log N) for many primes up to N.
 *
 * DRY RUN (N=10):
 *  2, 3, 5, 7
 */

#include <iostream>
#include <vector>

bool is_prime(int n) {
    if (n < 2) return false;
    if (n % 2 == 0) return n == 2;
    for (int j = 3; (long long)j * j <= n; j += 2) {
        if (n % j == 0) return false;
    }
    return true;
}

std::vector<int> sieve(int n) {
    std::vector<bool> composite(n + 1, false);
    if (n >= 0) composite[0] = true;
    if (n >= 1) composite[1] = true;
    for (int i = 2; (long long)i * i <= n; ++i) {
        if (!composite[i]) {
            for (int j = i * i; j <= n; j += i) composite[j] = true;
        }
    }
    std::vector<int> primes;
    for (int i = 2; i <= n; ++i) if (!composite[i]) primes.push_back(i);
    return primes;
}

int main() {
    int n;
    if (!(std::cin >> n)) { n = 30; std::cout << "(demo n=30)\n"; }

    for (int i = 2; i <= n; ++i) {
        if (is_prime(i)) std::cout << i << '\n';
    }

    auto primes = sieve(n);
    std::cout << "# sieve up to " << n << ":";
    for (int p : primes) std::cout << ' ' << p;
    std::cout << '\n';
    return 0;
}

/*
 * NOTES:
 *  - Use `(long long)j * j` to prevent overflow when j is large.
 *  - The sieve is the right tool when you need many primes; trial division
 *    is fine for ad-hoc primality of a single number.
 *  - For 64-bit primes, prefer Miller-Rabin (probabilistic).
 */
