/*
 * WEEK 7 - C++ DSA
 * Topic: KMP String Search
 * File: 3.kmp_search.cpp
 *
 * CONCEPT:
 *     Find all occurrences of pattern P in text T in O(n + m) using KMP
 *     and its longest-proper-prefix-suffix (LPS) array.
 *
 * KEY POINTS:
 *     - LPS[i] = length of the longest proper prefix of P[0..i] that
 *       is also a suffix.
 *     - On a mismatch, jump j = LPS[j-1] instead of restarting.
 *     - Builds in O(m), searches in O(n).
 *
 * ALGORITHM / APPROACH:
 *     buildLPS:
 *         len_ = 0; i = 1; lps[0] = 0
 *         while i < m:
 *             if P[i] == P[len_]: len_++; lps[i]=len_; i++
 *             elif len_ != 0:    len_ = lps[len_-1]
 *             else:              lps[i] = 0; i++
 *     kmpSearch: see code.
 *
 * C++-SPECIFIC NOTES:
 *     - std::vector<int> for LPS; std::vector<int> for positions.
 *     - std::string indexing is O(1).
 *
 * DRY RUN:
 *     pattern "AABA"
 *         lps = [0, 1, 0, 1]
 *     text "AABAACAADAABAABA"
 *         matches at indices 0, 9, 12.
 *
 * COMPLEXITY:
 *     Build LPS : O(m), O(m) space
 *     KMP search: O(n + m), O(m) space
 */

#include <iostream>
#include <string>
#include <vector>

std::vector<int> buildLPS(const std::string& pattern) {
    int m = static_cast<int>(pattern.size());
    std::vector<int> lps(m, 0);
    if (m == 0) return lps;
    int len = 0, i = 1;
    while (i < m) {
        if (pattern[i] == pattern[len]) {
            ++len;
            lps[i] = len;
            ++i;
        } else if (len != 0) {
            len = lps[len - 1];
        } else {
            lps[i] = 0;
            ++i;
        }
    }
    return lps;
}

std::vector<int> kmpSearch(const std::string& text, const std::string& pattern) {
    std::vector<int> positions;
    int n = static_cast<int>(text.size()), m = static_cast<int>(pattern.size());
    if (m == 0 || m > n) return positions;
    std::vector<int> lps = buildLPS(pattern);
    int i = 0, j = 0;
    while (i < n) {
        if (text[i] == pattern[j]) { ++i; ++j; }
        if (j == m) {
            positions.push_back(i - j);
            j = lps[j - 1];
        } else if (i < n && text[i] != pattern[j]) {
            if (j != 0) j = lps[j - 1];
            else        ++i;
        }
    }
    return positions;
}

std::vector<int> naiveSearch(const std::string& text, const std::string& pattern) {
    std::vector<int> positions;
    int n = static_cast<int>(text.size()), m = static_cast<int>(pattern.size());
    if (m == 0) return positions;
    for (int i = 0; i <= n - m; ++i) {
        bool ok = true;
        for (int j = 0; j < m; ++j) {
            if (text[i + j] != pattern[j]) { ok = false; break; }
        }
        if (ok) positions.push_back(i);
    }
    return positions;
}

void printVec(const std::vector<int>& v) {
    std::cout << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        std::cout << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    std::cout << "]";
}

int main() {
    std::string text1 = "AABAACAADAABAABA";
    std::string pat1 = "AABA";
    std::cout << "Text:    " << text1 << "\n";
    std::cout << "Pattern: " << pat1 << "\n";
    std::cout << "KMP found at:   "; printVec(kmpSearch(text1, pat1));   std::cout << "\n";
    std::cout << "Naive found at: "; printVec(naiveSearch(text1, pat1)); std::cout << "\n";

    std::string text2 = "AAAAABAAABA";
    std::string pat2 = "AAAA";
    std::cout << "\nText:    " << text2 << "\n";
    std::cout << "Pattern: " << pat2 << "\n";
    std::cout << "LPS: "; printVec(buildLPS(pat2)); std::cout << "\n";
    std::cout << "KMP found at: "; printVec(kmpSearch(text2, pat2)); std::cout << "\n";

    std::cout << "\nKMP(\"hello\",\"xyz\") = "; printVec(kmpSearch("hello","xyz")); std::cout << "\n";
    std::cout << "KMP(\"hi\",\"hello\") = "; printVec(kmpSearch("hi","hello")); std::cout << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::string and std::vector<int> replace String and ArrayList<Integer>.
 *     - Indexing is O(1) and identical to Java's charAt(i).
 *     - No boxing — vector<int> stores primitives directly.
 */
