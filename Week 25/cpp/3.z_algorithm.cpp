/*
 * WEEK 25 - C++ ADVANCED DSA
 * Topic: Z-Algorithm for Pattern Matching
 * File: 3.z_algorithm.cpp
 *
 * CONCEPT:
 *     For a string S the Z-array Z[i] = length of the longest prefix of S
 *     that starts at S[i]. Computed in O(n) by reusing previously found
 *     matches inside a moving "Z-box". Pattern matching becomes:
 *         build C = P + '$' + T, compute Z(C), report Z[i] == |P|.
 *
 * KEY POINTS:
 *     - The Z-box [l, r) is the right-most match of a prefix encountered.
 *     - If i < r, Z[i] = min(r - i, Z[i - l]) BEFORE attempting to extend.
 *     - Each character of S participates in at most two char-comparisons.
 *
 * ALGORITHM / APPROACH:
 *     z[0] = 0; l = r = 0
 *     for i in 1..n:
 *         if i < r: z[i] = min(r-i, z[i-l])
 *         while i+z[i] < n and s[z[i]] == s[i+z[i]]: z[i]++
 *         if i+z[i] > r: l = i; r = i+z[i]
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *     - std::min from <algorithm>.
 *     - Concatenation produces a fresh std::string; size is n + m + 1.
 *
 * DRY RUN:
 *     S = "aabxaab" -> Z = [0,1,0,0,3,1,0].
 *     C = "ABABCABAB$ABABDABACDABABCABAB"; Z[20] = 9 -> match at 10.
 *
 * COMPLEXITY:
 *     Time  : O(n + m)
 *     Space : O(n + m)
 *
 * Compile: g++ -std=c++17 -O2 3.z_algorithm.cpp -o zalg
 */

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using std::cout;
using std::endl;
using std::string;
using std::vector;

vector<int> z_function(const string& s) {
    int n = static_cast<int>(s.size());
    vector<int> z(n, 0);
    int l = 0, r = 0;
    for (int i = 1; i < n; i++) {
        if (i < r) z[i] = std::min(r - i, z[i - l]);
        while (i + z[i] < n && s[z[i]] == s[i + z[i]]) z[i]++;
        if (i + z[i] > r) { l = i; r = i + z[i]; }
    }
    return z;
}

vector<int> search(const string& text, const string& pattern) {
    vector<int> results;
    if (pattern.empty()) return results;
    string concat = pattern + "$" + text;
    vector<int> z = z_function(concat);
    int m = static_cast<int>(pattern.size());
    for (int i = m + 1; i < static_cast<int>(concat.size()); i++) {
        if (z[i] == m) results.push_back(i - m - 1);
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
    cout << "=== Z-Algorithm (C++) ===" << endl;
    string demo = "aabxaab";
    cout << "String : " << demo << endl;
    cout << "Z-array: "; print_vec(z_function(demo)); cout << endl;   // [0,1,0,0,3,1,0]

    string text = "ABABDABACDABABCABAB";
    string pattern = "ABABCABAB";
    cout << "\nText   : " << text << endl;
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
 *     - Pure syntactic translation; std::min vs Math.min, vector vs int[].
 *     - Same single-pass O(n) inner logic.
 */
