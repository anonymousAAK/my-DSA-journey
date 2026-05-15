/*
 * WEEK 25 - C++ ADVANCED DSA
 * Topic: Rabin-Karp String Matching (rolling hash)
 * File: 2.rabin_karp.cpp
 *
 * CONCEPT:
 *     Slide a fixed-size window of T and compare its rolling-hash fingerprint
 *     to the hash of P. On a hash collision verify literally. Expected
 *     runtime is O(n + m).
 *
 * KEY POINTS:
 *     - Polynomial rolling hash mod a large prime, BASE = 256.
 *     - h = BASE^(m-1) mod PRIME used to subtract the outgoing character.
 *     - Always verify a candidate window literally — hashes can collide.
 *     - Worst case O(n*m) under adversarial input.
 *
 * ALGORITHM / APPROACH:
 *     h = BASE^(m-1) mod PRIME
 *     compute p_hash and the first t_hash
 *     for i in 0..n-m:
 *         if p_hash == t_hash and T[i..i+m] == P: report i
 *         t_hash = (BASE * (t_hash - T[i]*h) + T[i+m]) mod PRIME
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *     - Use long long to stay clear of overflow before mod.
 *     - text.substr(i, m) materialises a copy on each candidate; for hot
 *       paths replace with a hand-written compare loop.
 *     - char promotes to int naturally when arithmetic is performed.
 *
 * DRY RUN:
 *     P = "AAA", T = "AAAAAA". h = 256^2 mod PRIME = 65536.
 *     p_hash = ((65*256 + 65)*256 + 65) = 4_276_545 (within mod).
 *     Each window shares the same fingerprint -> matches [0,1,2,3].
 *
 * COMPLEXITY:
 *     Time  : O(n + m) expected, O(n*m) worst.
 *     Space : O(1) extra.
 *
 * Compile: g++ -std=c++17 -O2 2.rabin_karp.cpp -o rk
 */

#include <iostream>
#include <string>
#include <vector>

using std::cout;
using std::endl;
using std::string;
using std::vector;

vector<int> search(const string& text, const string& pattern) {
    const long long BASE  = 256;
    const long long PRIME = 1000000007LL;

    vector<int> results;
    int n = static_cast<int>(text.size());
    int m = static_cast<int>(pattern.size());
    if (m == 0 || m > n) return results;

    long long h = 1;
    for (int i = 0; i < m - 1; i++) h = (h * BASE) % PRIME;

    long long p_hash = 0, t_hash = 0;
    for (int i = 0; i < m; i++) {
        p_hash = (BASE * p_hash + static_cast<unsigned char>(pattern[i])) % PRIME;
        t_hash = (BASE * t_hash + static_cast<unsigned char>(text[i]))    % PRIME;
    }

    for (int i = 0; i <= n - m; i++) {
        if (p_hash == t_hash) {
            if (text.compare(i, m, pattern) == 0) {
                results.push_back(i);
            }
        }
        if (i < n - m) {
            t_hash = (BASE * (t_hash - static_cast<unsigned char>(text[i]) * h)
                      + static_cast<unsigned char>(text[i + m])) % PRIME;
            if (t_hash < 0) t_hash += PRIME;
        }
    }
    return results;
}

static void print_vec(const vector<int>& v) {
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        cout << v[i];
        if (i + 1 < v.size()) cout << ", ";
    }
    cout << "]";
}

int main() {
    cout << "=== Rabin-Karp Pattern Matching (C++) ===" << endl;
    string text = "ABABDABACDABABCABAB";
    string pattern = "ABABCABAB";
    cout << "Text   : " << text << endl;
    cout << "Pattern: " << pattern << endl;
    cout << "Matches: "; print_vec(search(text, pattern)); cout << endl;   // [10]

    cout << "\n--- Overlapping matches ---" << endl;
    string t2 = "AAAAAA", p2 = "AAA";
    cout << "Text   : " << t2 << endl;
    cout << "Pattern: " << p2 << endl;
    cout << "Matches: "; print_vec(search(t2, p2)); cout << endl;          // [0,1,2,3]
    return 0;
}

/*
 * NOTES (vs Java baseline):
 *     - C++ promotes char to int implicitly; we cast to unsigned char first
 *       so non-ASCII bytes (>= 0x80) don't become negative in the hash.
 *     - text.compare(i, m, pattern) avoids materialising a temporary string
 *       that Java's substring/equals chain would in the textbook version.
 */
