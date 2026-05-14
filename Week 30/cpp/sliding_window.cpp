/*
 * WEEK 30 - C++ ADVANCED TOPICS
 * Topic: Sliding Window Pattern
 * File: sliding_window.cpp
 *
 * CONCEPT:
 *   Maintain a window [l, r] over a sequence; grow on the right; shrink on
 *   the left when an invariant breaks. Each element enters and leaves the
 *   window at most once -> O(n) total work.
 *
 * KEY POINTS:
 *   - Common state: hash map of counts, running sum, monotonic deque.
 *   - Fixed-size: slide one step at a time.
 *   - Variable-size: grow right, shrink left while invariant violated.
 *   - Canonical problems: longest unique substring (LC 3), min window
 *     substring (LC 76), longest k-distinct (LC 340), max sliding window
 *     (LC 239).
 *
 * ALGORITHM / APPROACH:
 *   l = 0
 *   for r in 0..n:
 *     add a[r] to window state
 *     while invariant violated: remove a[l]; l++
 *     update best
 *
 * C++-SPECIFIC NOTES:
 *   - std::unordered_map<char,int> for character counts.
 *   - std::deque<int> for the monotonic-deque variant.
 *
 * DRY RUN / EXAMPLE:
 *   "abcabcbb" -> 3.  minWindow("ADOBECODEBANC","ABC") -> "BANC".
 *   maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3) -> [3,3,5,5,6,7].
 *
 * COMPLEXITY:
 *   Time O(n). Space O(charset) or O(window).
 */

#include <iostream>
#include <string>
#include <vector>
#include <deque>
#include <unordered_map>
#include <climits>
#include <algorithm>

using namespace std;

int lengthOfLongestSubstring(const string& s) {
    unordered_map<char,int> last;
    int left = 0, best = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
        char c = s[r];
        auto it = last.find(c);
        if (it != last.end() && it->second >= left) left = it->second + 1;
        last[c] = r;
        best = max(best, r - left + 1);
    }
    return best;
}

string minWindow(const string& s, const string& t) {
    if (s.size() < t.size() || t.empty()) return "";
    unordered_map<char,int> need, window;
    for (char c : t) need[c]++;
    int required = (int)need.size(), formed = 0;
    int left = 0, bestLen = INT_MAX, bestLeft = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
        char c = s[r];
        window[c]++;
        if (need.count(c) && window[c] == need[c]) ++formed;
        while (formed == required) {
            if (r - left + 1 < bestLen) { bestLen = r - left + 1; bestLeft = left; }
            char lc = s[left++];
            window[lc]--;
            if (need.count(lc) && window[lc] < need[lc]) --formed;
        }
    }
    return bestLen == INT_MAX ? "" : s.substr(bestLeft, bestLen);
}

int longestKDistinct(const string& s, int k) {
    if (k == 0 || s.empty()) return 0;
    unordered_map<char,int> counts;
    int left = 0, best = 0;
    for (int r = 0; r < (int)s.size(); ++r) {
        ++counts[s[r]];
        while ((int)counts.size() > k) {
            if (--counts[s[left]] == 0) counts.erase(s[left]);
            ++left;
        }
        best = max(best, r - left + 1);
    }
    return best;
}

vector<int> maxSlidingWindow(const vector<int>& nums, int k) {
    deque<int> dq;
    vector<int> out;
    for (int i = 0; i < (int)nums.size(); ++i) {
        while (!dq.empty() && nums[dq.back()] <= nums[i]) dq.pop_back();
        dq.push_back(i);
        if (dq.front() == i - k) dq.pop_front();
        if (i >= k - 1) out.push_back(nums[dq.front()]);
    }
    return out;
}

int main() {
    cout << "Longest unique 'abcabcbb': " << lengthOfLongestSubstring("abcabcbb") << "\n";
    cout << "Min window 'ADOBECODEBANC','ABC': \"" << minWindow("ADOBECODEBANC", "ABC") << "\"\n";
    cout << "Longest 2-distinct 'eceba': " << longestKDistinct("eceba", 2) << "\n";
    cout << "Max sliding window [1,3,-1,-3,5,3,6,7] k=3:";
    for (int x : maxSlidingWindow({1,3,-1,-3,5,3,6,7}, 3)) cout << " " << x;
    cout << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - std::unordered_map for char counts; .count() check is more concise.
 *   - std::deque<int> for the monotonic-deque variant.
 *   - We add longestKDistinct (LC 340) and maxSlidingWindow (LC 239) on top
 *     of the Java file's existing problems.
 */
