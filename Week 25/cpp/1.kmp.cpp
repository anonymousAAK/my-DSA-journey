/*
 * WEEK 25 - C++ ADVANCED DSA
 * Topic: KMP (Knuth-Morris-Pratt) Pattern Matching
 * File: 1.kmp.cpp
 *
 * CONCEPT:
 *     Find all occurrences of pattern P (length m) in text T (length n) in
 *     O(n + m) time by precomputing an LPS / failure-function array so the
 *     text pointer never moves backwards.
 *
 * KEY POINTS:
 *     - lps[i] = length of the longest PROPER prefix of P[0..i] that is also
 *       a suffix of P[0..i].
 *     - On full match, j = lps[j-1] keeps overlapping matches alive.
 *     - Building lps is KMP applied to P against itself.
 *
 * ALGORITHM / APPROACH:
 *     build_lps:
 *         length = 0; i = 1
 *         while i < m:
 *             if P[i] == P[length]: length++; lps[i] = length; i++
 *             else if length: length = lps[length - 1]
 *             else:           lps[i] = 0; i++
 *
 *     search:
 *         i = j = 0
 *         while i < n:
 *             if T[i] == P[j]: i++; j++
 *             if j == m: result.push_back(i - j); j = lps[j-1]
 *             else if i < n and T[i] != P[j]: j = j ? lps[j-1] : (i++, 0)
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *     - std::string indexing is O(1).
 *     - Use static_cast<int> when comparing size() (size_t) with int.
 *     - std::vector<int> serves as both lps and result container.
 *
 * DRY RUN:
 *     P = "ABABCABAB", lps = [0,0,1,2,0,1,2,3,4]
 *     T = "ABABDABACDABABCABAB" -> match at index 10.
 *     P = "AAA", T = "AAAAAA" -> matches [0,1,2,3].
 *
 * COMPLEXITY:
 *     Time  : O(n + m)
 *     Space : O(m)
 *
 * Compile: g++ -std=c++17 -O2 1.kmp.cpp -o kmp
 */

#include <iostream>
#include <string>
#include <vector>

using std::cout;
using std::endl;
using std::string;
using std::vector;

vector<int> build_lps(const string& pattern) {
    int m = static_cast<int>(pattern.size());
    vector<int> lps(m, 0);
    int length = 0;
    int i = 1;
    while (i < m) {
        if (pattern[i] == pattern[length]) {
            length++;
            lps[i] = length;
            i++;
        } else if (length != 0) {
            length = lps[length - 1];
        } else {
            lps[i] = 0;
            i++;
        }
    }
    return lps;
}

vector<int> search(const string& text, const string& pattern) {
    vector<int> results;
    int n = static_cast<int>(text.size());
    int m = static_cast<int>(pattern.size());
    if (m == 0) return results;

    vector<int> lps = build_lps(pattern);
    int i = 0, j = 0;
    while (i < n) {
        if (text[i] == pattern[j]) { i++; j++; }
        if (j == m) {
            results.push_back(i - j);
            j = lps[j - 1];
        } else if (i < n && text[i] != pattern[j]) {
            if (j != 0) j = lps[j - 1];
            else i++;
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
    cout << "=== KMP Pattern Matching (C++) ===" << endl;
    string text = "ABABDABACDABABCABAB";
    string pattern = "ABABCABAB";
    cout << "Text   : " << text << endl;
    cout << "Pattern: " << pattern << endl;
    cout << "LPS    : "; print_vec(build_lps(pattern)); cout << endl;
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
 *     - Direct port; only syntactic differences (vector vs ArrayList,
 *       size_t vs int, std::string vs java.lang.String).
 *     - C++ has no built-in std::vector printer, so a tiny helper does it.
 */
