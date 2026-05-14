/*
 * =============================================================================
 * Week 7 - Strings (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Palindrome check (two-pointer)
 *   2. Anagram check (sorting method + frequency array)
 *   3. Reverse words in a string
 *   4. String compression (run-length encoding)
 *   5. KMP pattern matching algorithm
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// 1. PALINDROME CHECK (Two-Pointer)
// =============================================================================
// Time: O(n)   Space: O(1)
bool isPalindrome(const string& s) {
    int left = 0, right = static_cast<int>(s.size()) - 1;
    while (left < right) {
        if (s[left] != s[right]) return false;
        ++left;
        --right;
    }
    return true;
}

// Alphanumeric-only palindrome check (ignores case and non-alphanumeric chars)
// Time: O(n)   Space: O(1)
bool isPalindromeAlphanumeric(const string& s) {
    int left = 0, right = static_cast<int>(s.size()) - 1;
    while (left < right) {
        while (left < right && !isalnum(s[left])) ++left;
        while (left < right && !isalnum(s[right])) --right;
        if (tolower(s[left]) != tolower(s[right])) return false;
        ++left;
        --right;
    }
    return true;
}

// =============================================================================
// 2. ANAGRAM CHECK
// =============================================================================

// Method 1: Sort both strings and compare
// Time: O(n log n)   Space: O(n) for copies (or O(1) if modifying in-place)
bool isAnagramSort(string a, string b) {
    if (a.size() != b.size()) return false;
    sort(a.begin(), a.end());
    sort(b.begin(), b.end());
    return a == b;
}

// Method 2: Frequency array (for lowercase English letters)
// Time: O(n)   Space: O(1) — fixed 26-char array
bool isAnagramFreq(const string& a, const string& b) {
    if (a.size() != b.size()) return false;
    array<int, 26> freq{};  // zero-initialized
    for (char c : a) freq[c - 'a']++;
    for (char c : b) freq[c - 'a']--;
    // If all frequencies are zero, strings are anagrams
    return all_of(freq.begin(), freq.end(), [](int f) { return f == 0; });
}

// General anagram check (supports any characters via unordered_map)
// Time: O(n)   Space: O(k) where k = distinct characters
bool isAnagramGeneral(const string& a, const string& b) {
    if (a.size() != b.size()) return false;
    unordered_map<char, int> freq;
    for (char c : a) freq[c]++;
    for (char c : b) {
        if (--freq[c] < 0) return false;
    }
    return true;
}

// =============================================================================
// 3. REVERSE WORDS IN A STRING
// =============================================================================
// "  hello   world  " -> "world hello"
// Time: O(n)   Space: O(n) for result
string reverseWords(const string& s) {
    // Extract words using stringstream
    istringstream iss(s);
    vector<string> words;
    string word;
    while (iss >> word) {
        words.push_back(move(word));
    }
    // Reverse and join
    reverse(words.begin(), words.end());
    string result;
    for (size_t i = 0; i < words.size(); ++i) {
        if (i > 0) result += ' ';
        result += words[i];
    }
    return result;
}

// In-place approach (reverse entire string, then reverse each word)
// Time: O(n)   Space: O(1) extra (modifying the string in-place)
string reverseWordsInPlace(string s) {
    // Step 1: Remove extra spaces and trim
    int n = s.size();
    int i = 0, j = 0;
    while (j < n) {
        while (j < n && s[j] == ' ') ++j;           // skip leading spaces
        if (j < n && i > 0) s[i++] = ' ';            // add single space between words
        while (j < n && s[j] != ' ') s[i++] = s[j++]; // copy word
    }
    s.resize(i);

    // Step 2: Reverse the entire string
    reverse(s.begin(), s.end());

    // Step 3: Reverse each word individually
    int start = 0;
    for (int k = 0; k <= static_cast<int>(s.size()); ++k) {
        if (k == static_cast<int>(s.size()) || s[k] == ' ') {
            reverse(s.begin() + start, s.begin() + k);
            start = k + 1;
        }
    }
    return s;
}

// =============================================================================
// 4. STRING COMPRESSION (Run-Length Encoding)
// =============================================================================
// "aabcccccaaa" -> "a2b1c5a3"
// Only compress if result is shorter; otherwise return original.
// Time: O(n)   Space: O(n)
string compress(const string& s) {
    if (s.empty()) return s;
    string compressed;
    int count = 1;
    for (size_t i = 1; i <= s.size(); ++i) {
        if (i < s.size() && s[i] == s[i - 1]) {
            ++count;
        } else {
            compressed += s[i - 1];
            compressed += to_string(count);
            count = 1;
        }
    }
    return (compressed.size() < s.size()) ? compressed : s;
}

// =============================================================================
// 5. KMP PATTERN MATCHING
// =============================================================================

// Build the LPS (Longest Proper Prefix which is also Suffix) array
// Time: O(m) where m = pattern length
// Space: O(m)
vector<int> buildLPS(const string& pattern) {
    int m = pattern.size();
    vector<int> lps(m, 0);
    int len = 0;  // length of previous longest prefix suffix
    int i = 1;
    while (i < m) {
        if (pattern[i] == pattern[len]) {
            lps[i++] = ++len;
        } else {
            if (len != 0) {
                len = lps[len - 1];  // don't increment i
            } else {
                lps[i++] = 0;
            }
        }
    }
    return lps;
}

// KMP search: find all occurrences of pattern in text
// Time: O(n + m) where n = text length, m = pattern length
// Space: O(m) for LPS array
vector<int> kmpSearch(const string& text, const string& pattern) {
    vector<int> result;
    if (pattern.empty()) return result;

    int n = text.size(), m = pattern.size();
    vector<int> lps = buildLPS(pattern);

    int i = 0;  // index in text
    int j = 0;  // index in pattern
    while (i < n) {
        if (text[i] == pattern[j]) {
            ++i;
            ++j;
        }
        if (j == m) {
            result.push_back(i - j);  // match found at index (i - j)
            j = lps[j - 1];
        } else if (i < n && text[i] != pattern[j]) {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                ++i;
            }
        }
    }
    return result;
}

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 7: Strings (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Palindrome Check ---
    cout << "\n--- 1. Palindrome Check ---" << endl;
    for (const auto& s : {"racecar", "hello", "madam", "abcba", ""}) {
        cout << "\"" << s << "\" -> "
             << (isPalindrome(s) ? "palindrome" : "not palindrome") << endl;
    }
    cout << "\nAlphanumeric palindrome:" << endl;
    for (const auto& s : {"A man, a plan, a canal: Panama", "race a car", " "}) {
        cout << "\"" << s << "\" -> "
             << (isPalindromeAlphanumeric(s) ? "palindrome" : "not palindrome") << endl;
    }

    // --- 2. Anagram Check ---
    cout << "\n--- 2. Anagram Check ---" << endl;
    {
        auto test = [](const string& a, const string& b) {
            cout << "\"" << a << "\" vs \"" << b << "\" -> "
                 << "sort:" << isAnagramSort(a, b)
                 << "  freq:" << isAnagramFreq(a, b)
                 << "  general:" << isAnagramGeneral(a, b) << endl;
        };
        test("listen", "silent");
        test("hello", "world");
        test("anagram", "nagaram");
        test("rat", "car");
    }

    // --- 3. Reverse Words ---
    cout << "\n--- 3. Reverse Words ---" << endl;
    {
        auto test = [](const string& s) {
            cout << "\"" << s << "\"" << endl;
            cout << "  stream:   \"" << reverseWords(s) << "\"" << endl;
            cout << "  in-place: \"" << reverseWordsInPlace(s) << "\"" << endl;
        };
        test("the sky is blue");
        test("  hello   world  ");
        test("a");
    }

    // --- 4. String Compression ---
    cout << "\n--- 4. String Compression ---" << endl;
    for (const auto& s : {"aabcccccaaa", "abc", "aabb", "aaaaaaa"}) {
        cout << "\"" << s << "\" -> \"" << compress(s) << "\"" << endl;
    }

    // --- 5. KMP Pattern Matching ---
    cout << "\n--- 5. KMP Pattern Matching ---" << endl;
    {
        auto test = [](const string& text, const string& pattern) {
            auto matches = kmpSearch(text, pattern);
            cout << "Text: \"" << text << "\"  Pattern: \"" << pattern << "\"" << endl;
            cout << "  Found at indices: [";
            for (size_t i = 0; i < matches.size(); ++i) {
                cout << matches[i] << (i + 1 < matches.size() ? ", " : "");
            }
            cout << "]" << endl;
        };
        test("ABABDABACDABABCABAB", "ABABCABAB");
        test("aaaaaa", "aa");
        test("hello world", "world");
        test("abcdef", "xyz");

        // Show LPS array
        string pat = "ABABCABAB";
        auto lps = buildLPS(pat);
        cout << "\nLPS array for \"" << pat << "\": [";
        for (size_t i = 0; i < lps.size(); ++i) {
            cout << lps[i] << (i + 1 < lps.size() ? ", " : "");
        }
        cout << "]" << endl;
    }

    cout << "\n========================================" << endl;
    cout << " All Week 7 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
