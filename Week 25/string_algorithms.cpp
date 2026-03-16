/**
 * Week 25: String Algorithms
 * ===========================
 * This file covers fundamental string matching and pattern search algorithms.
 *
 * Topics covered:
 *     1. KMP (Knuth-Morris-Pratt) Pattern Matching
 *     2. Rabin-Karp String Matching (rolling hash)
 *     3. Z-Algorithm for Pattern Matching
 *
 * Each algorithm includes:
 *     - Problem statement
 *     - Step-by-step approach explanation
 *     - Time / space complexity analysis
 *     - Example usage via main driver
 *
 * Compile: g++ -std=c++17 -O2 -o string_algorithms string_algorithms.cpp
 */

#include <iostream>
#include <string>
#include <vector>

using std::cout;
using std::endl;
using std::string;
using std::vector;

// ===========================================================================
// 1. KMP (Knuth-Morris-Pratt) Pattern Matching
// ===========================================================================
// Problem:
//   Given a text T of length n and a pattern P of length m, find all
//   occurrences of P in T.
//
// Approach:
//   1. Build the LPS (Longest Proper Prefix which is also a Suffix) array
//      for the pattern.
//      lps[i] = length of the longest proper prefix of P[0..i] that is
//      also a suffix of P[0..i].
//   2. Scan the text with two pointers (i for text, j for pattern).
//      On a mismatch after j matches, set j = lps[j-1] and continue,
//      skipping characters we already know must match.
//
// Complexity:
//   Time  : O(n + m)  — linear in the combined length
//   Space : O(m)      — for the LPS array

/**
 * Build the LPS (failure function) array for the given pattern.
 *
 * lps[i] = length of the longest proper prefix of pattern[0..i]
 * that is also a suffix of that substring.
 *
 * Time : O(m)
 * Space: O(m)
 */
vector<int> kmp_build_lps(const string& pattern) {
    int m = static_cast<int>(pattern.size());
    vector<int> lps(m, 0);
    int length = 0;  // length of previous longest prefix-suffix
    int i = 1;

    while (i < m) {
        if (pattern[i] == pattern[length]) {
            length++;
            lps[i] = length;
            i++;
        } else {
            if (length != 0) {
                // Fall back — do NOT increment i
                length = lps[length - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

/**
 * Return a vector of starting indices where pattern occurs in text
 * using the Knuth-Morris-Pratt algorithm.
 *
 * Time : O(n + m)
 * Space: O(m)
 */
vector<int> kmp_search(const string& text, const string& pattern) {
    vector<int> results;
    int n = static_cast<int>(text.size());
    int m = static_cast<int>(pattern.size());
    if (m == 0) return results;

    vector<int> lps = kmp_build_lps(pattern);
    int i = 0;  // index into text
    int j = 0;  // index into pattern

    while (i < n) {
        if (text[i] == pattern[j]) {
            i++;
            j++;
        }

        if (j == m) {
            // Full match found at index i - j
            results.push_back(i - j);
            j = lps[j - 1];  // look for next overlapping match
        } else if (i < n && text[i] != pattern[j]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }
    return results;
}

// ===========================================================================
// 2. Rabin-Karp String Matching
// ===========================================================================
// Problem:
//   Find all occurrences of pattern P in text T using a rolling hash
//   to achieve expected linear time.
//
// Approach:
//   1. Compute the hash of the pattern and the first window of text.
//   2. Slide the window one character at a time. Update the hash in O(1)
//      by removing the outgoing character and adding the incoming one.
//   3. On hash match, verify character by character to rule out
//      spurious hits (hash collisions).
//
// Hash function:
//   H(s) = (s[0]*d^(m-1) + s[1]*d^(m-2) + ... + s[m-1]) mod q
//   d = 256 (alphabet size), q = a large prime.
//
// Complexity:
//   Time  : O(n + m) expected, O(n*m) worst-case (many collisions)
//   Space : O(1) extra (besides the output vector)

/**
 * Return a vector of starting indices where pattern occurs in text
 * using the Rabin-Karp rolling-hash algorithm.
 *
 * Time : O(n + m) expected
 * Space: O(1) extra
 */
vector<int> rabin_karp_search(const string& text, const string& pattern) {
    const long long BASE = 256;
    const long long PRIME = 1000000007LL;

    vector<int> results;
    int n = static_cast<int>(text.size());
    int m = static_cast<int>(pattern.size());
    if (m == 0 || m > n) return results;

    // h = BASE^(m-1) mod PRIME — used to remove the leading digit
    long long h = 1;
    for (int i = 0; i < m - 1; i++) {
        h = (h * BASE) % PRIME;
    }

    // Compute initial hashes for pattern and first window of text
    long long p_hash = 0, t_hash = 0;
    for (int i = 0; i < m; i++) {
        p_hash = (BASE * p_hash + pattern[i]) % PRIME;
        t_hash = (BASE * t_hash + text[i]) % PRIME;
    }

    // Slide the window over the text
    for (int i = 0; i <= n - m; i++) {
        // If hashes match, verify character by character
        if (p_hash == t_hash) {
            if (text.substr(i, m) == pattern) {
                results.push_back(i);
            }
        }

        // Compute hash for the next window (if there is one)
        if (i < n - m) {
            t_hash = (BASE * (t_hash - text[i] * h) + text[i + m]) % PRIME;
            if (t_hash < 0) t_hash += PRIME;
        }
    }
    return results;
}

// ===========================================================================
// 3. Z-Algorithm for Pattern Matching
// ===========================================================================
// Problem:
//   Given a string S, compute the Z-array where Z[i] is the length of
//   the longest substring starting at index i that is also a prefix of S.
//   For pattern matching: build P + '$' + T and check where Z[i] == |P|.
//
// Approach:
//   Maintain a "Z-box" [l, r) — the interval of the rightmost substring
//   matching a prefix. For each new position i:
//     - If i < r, reuse previously computed info: Z[i] = min(r-i, Z[i-l]).
//     - Extend character by character.
//     - Update [l, r) if extended past r.
//
// Complexity:
//   Time  : O(n)  — each character compared at most twice
//   Space : O(n)  — for the Z-array

/**
 * Compute the Z-array for string s.
 *
 * Z[0] is defined as 0.
 * Z[i] = length of the longest substring starting at s[i]
 *        that matches a prefix of s.
 *
 * Time : O(n)
 * Space: O(n)
 */
vector<int> z_function(const string& s) {
    int n = static_cast<int>(s.size());
    vector<int> z(n, 0);
    int l = 0, r = 0;  // Z-box boundaries [l, r)

    for (int i = 1; i < n; i++) {
        if (i < r) {
            // Inside the current Z-box; reuse known info
            z[i] = std::min(r - i, z[i - l]);
        }

        // Try to extend the match
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
            z[i]++;
        }

        // Update the Z-box if we went past r
        if (i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    return z;
}

/**
 * Find all occurrences of pattern in text using the Z-algorithm.
 *
 * Builds the concatenated string pattern + '$' + text and checks
 * positions where Z[i] == pattern.length().
 *
 * Time : O(n + m)
 * Space: O(n + m)
 */
vector<int> z_search(const string& text, const string& pattern) {
    vector<int> results;
    if (pattern.empty()) return results;

    string concat = pattern + "$" + text;
    vector<int> z = z_function(concat);
    int m = static_cast<int>(pattern.size());

    for (int i = m + 1; i < static_cast<int>(concat.size()); i++) {
        if (z[i] == m) {
            results.push_back(i - m - 1);  // map back to text index
        }
    }
    return results;
}

// ===========================================================================
// Helper: print a vector
// ===========================================================================
void print_vec(const vector<int>& v) {
    cout << "[";
    for (size_t i = 0; i < v.size(); i++) {
        cout << v[i];
        if (i + 1 < v.size()) cout << ", ";
    }
    cout << "]";
}

// ===========================================================================
// Driver / demo
// ===========================================================================
int main() {
    string text = "ABABDABACDABABCABAB";
    string pattern = "ABABCABAB";

    cout << "============================================================" << endl;
    cout << "Week 25 — String Algorithms  (C++)" << endl;
    cout << "============================================================" << endl;
    cout << "\nText   : " << text << endl;
    cout << "Pattern: " << pattern << "\n" << endl;

    // KMP
    auto kmp_res = kmp_search(text, pattern);
    cout << "[KMP]        Matches at indices : ";
    print_vec(kmp_res);
    cout << endl;

    // Rabin-Karp
    auto rk_res = rabin_karp_search(text, pattern);
    cout << "[Rabin-Karp] Matches at indices : ";
    print_vec(rk_res);
    cout << endl;

    // Z-algorithm
    auto z_res = z_search(text, pattern);
    cout << "[Z-algo]     Matches at indices : ";
    print_vec(z_res);
    cout << endl;

    // Overlapping matches example
    cout << "\n--- Overlapping-match example ---" << endl;
    string text2 = "AAAAAA";
    string pattern2 = "AAA";
    cout << "Text   : " << text2 << endl;
    cout << "Pattern: " << pattern2 << endl;
    cout << "[KMP]        Matches at indices : ";
    print_vec(kmp_search(text2, pattern2));
    cout << endl;
    cout << "[Rabin-Karp] Matches at indices : ";
    print_vec(rabin_karp_search(text2, pattern2));
    cout << endl;
    cout << "[Z-algo]     Matches at indices : ";
    print_vec(z_search(text2, pattern2));
    cout << endl;

    // Z-array demo
    cout << "\n--- Z-array demo ---" << endl;
    string demo = "aabxaab";
    auto z_arr = z_function(demo);
    cout << "String  : " << demo << endl;
    cout << "Z-array : ";
    print_vec(z_arr);
    cout << endl;

    return 0;
}
