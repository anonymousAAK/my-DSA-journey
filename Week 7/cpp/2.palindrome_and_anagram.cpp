/*
 * WEEK 7 - C++ DSA
 * Topic: Palindrome & Anagram
 * File: 2.palindrome_and_anagram.cpp
 *
 * CONCEPT:
 *     Palindrome: same forwards and backwards.
 *     Anagram   : same characters with same frequencies.
 *
 * KEY POINTS:
 *     - Two-pointer palindrome runs in O(n) time, O(1) space.
 *     - Three anagram approaches: sort, frequency-array, std::map.
 *
 * ALGORITHM / APPROACH:
 *     Palindrome (basic):
 *         l = 0, r = n-1
 *         while l < r:
 *             if s[l] != s[r]: return false
 *             ++l; --r
 *         return true
 *     Palindrome (alphanumeric):
 *         skip non-alnum chars on both ends; lower-case compare.
 *
 * C++-SPECIFIC NOTES:
 *     - std::isalnum / std::tolower live in <cctype>; cast to unsigned char.
 *     - std::sort over a std::string sorts characters lexicographically.
 *     - std::unordered_map<char,int> mirrors Java HashMap for unicode-style use.
 *
 * DRY RUN:
 *     "racecar" -> palindrome (true)
 *     "race a car" ignoring punctuation -> false
 *     "listen" vs "silent" -> sorted both = "eilnst" -> anagram
 *
 * COMPLEXITY:
 *     Palindrome    : O(n) time, O(1) space
 *     Sort anagram  : O(n log n)
 *     Freq anagram  : O(n) (26-element array)
 *     Map  anagram  : O(n)
 */

#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <unordered_map>
#include <cctype>

bool isPalindrome(const std::string& s) {
    int l = 0, r = static_cast<int>(s.size()) - 1;
    while (l < r) {
        if (s[l] != s[r]) return false;
        ++l; --r;
    }
    return true;
}

bool isPalindromeIgnoreNonAlpha(const std::string& s) {
    int l = 0, r = static_cast<int>(s.size()) - 1;
    auto alnum = [](char c) { return std::isalnum(static_cast<unsigned char>(c)); };
    auto lower = [](char c) { return static_cast<char>(std::tolower(static_cast<unsigned char>(c))); };
    while (l < r) {
        while (l < r && !alnum(s[l])) ++l;
        while (l < r && !alnum(s[r])) --r;
        if (lower(s[l]) != lower(s[r])) return false;
        ++l; --r;
    }
    return true;
}

bool isAnagramSort(std::string a, std::string b) {
    if (a.size() != b.size()) return false;
    std::sort(a.begin(), a.end());
    std::sort(b.begin(), b.end());
    return a == b;
}

bool isAnagramFreq(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) return false;
    int freq[26] = {0};
    for (char c : a) freq[c - 'a']++;
    for (char c : b) {
        freq[c - 'a']--;
        if (freq[c - 'a'] < 0) return false;
    }
    return true;
}

bool isAnagramMap(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) return false;
    std::unordered_map<char,int> m;
    for (char c : a) m[c]++;
    for (char c : b) {
        auto it = m.find(c);
        if (it == m.end() || it->second == 0) return false;
        --(it->second);
    }
    return true;
}

int main() {
    std::cout << "=== Palindrome ===\n";
    for (const char* t : {"racecar", "hello", "level", "madam", "a", ""}) {
        std::cout << "isPalindrome(\"" << t << "\") = "
                  << (isPalindrome(t) ? "true" : "false") << "\n";
    }

    std::cout << "\nisPalindromeIgnoreNonAlpha:\n";
    std::string s1 = "A man, a plan, a canal: Panama";
    std::cout << '"' << s1 << "\" = "
              << (isPalindromeIgnoreNonAlpha(s1) ? "true" : "false") << "\n";
    std::string s2 = "race a car";
    std::cout << '"' << s2 << "\" = "
              << (isPalindromeIgnoreNonAlpha(s2) ? "true" : "false") << "\n";

    std::cout << "\n=== Anagram ===\n";
    std::vector<std::pair<std::string,std::string>> pairs = {
        {"listen","silent"}, {"eat","tea"}, {"hello","world"},
        {"anagram","nagaram"}
    };
    for (auto& [a,b] : pairs) {
        std::cout << '"' << a << "\" vs \"" << b << "\":\n";
        std::cout << "  Sort: " << (isAnagramSort(a, b) ? "true" : "false") << "\n";
        std::cout << "  Freq: " << (isAnagramFreq(a, b) ? "true" : "false") << "\n";
        std::cout << "  Map:  " << (isAnagramMap(a, b) ? "true" : "false") << "\n";
    }

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - <cctype> functions need unsigned-char casts for UB-safety.
 *     - std::sort works directly on std::string (a contiguous buffer).
 *     - std::unordered_map mirrors Java HashMap; structured bindings give
 *       (key, value) pairs cleanly.
 */
