// Week 30: Interview Patterns & Mastery
// Two Pointers, Sliding Window, Fast & Slow Pointers, Merge Intervals, Top-K Elements
#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
#include <climits>
using namespace std;

// =========================================================================
// TWO POINTERS
// =========================================================================

// Two Sum II - sorted array (LC 167) - Time: O(n), Space: O(1)
vector<int> twoSumII(const vector<int>& nums, int target) {
    int l = 0, r = (int)nums.size() - 1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s == target) return {l + 1, r + 1}; // 1-indexed
        s < target ? l++ : r--;
    }
    return {};
}

// 3Sum (LC 15) - Time: O(n^2), Space: O(1) extra
vector<vector<int>> threeSum(vector<int>& nums) {
    vector<vector<int>> result;
    sort(nums.begin(), nums.end());
    int n = (int)nums.size();
    for (int i = 0; i < n - 2; i++) {
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = n - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (s == 0) {
                result.push_back({nums[i], nums[l], nums[r]});
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++; r--;
            } else if (s < 0) l++;
            else r--;
        }
    }
    return result;
}

// Container With Most Water (LC 11) - Time: O(n), Space: O(1)
int maxArea(const vector<int>& height) {
    int l = 0, r = (int)height.size() - 1, best = 0;
    while (l < r) {
        best = max(best, (r - l) * min(height[l], height[r]));
        if (height[l] < height[r]) l++;
        else r--;
    }
    return best;
}

// =========================================================================
// SLIDING WINDOW
// =========================================================================

// Longest Substring Without Repeating Characters (LC 3) - Time: O(n), Space: O(min(n, charset))
int lengthOfLongestSubstring(const string& s) {
    unordered_map<char, int> idx;
    int left = 0, mx = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        if (idx.count(s[r]) && idx[s[r]] >= left)
            left = idx[s[r]] + 1;
        idx[s[r]] = r;
        mx = max(mx, r - left + 1);
    }
    return mx;
}

// Minimum Window Substring (LC 76) - Time: O(n + m), Space: O(m)
string minWindow(const string& s, const string& t) {
    if (s.size() < t.size()) return "";
    unordered_map<char, int> need, window;
    for (char c : t) need[c]++;

    int required = (int)need.size(), formed = 0, left = 0;
    int bestLen = INT_MAX, bestLeft = 0;

    for (int r = 0; r < (int)s.size(); r++) {
        char c = s[r];
        window[c]++;
        if (need.count(c) && window[c] == need[c]) formed++;

        while (formed == required) {
            if (r - left + 1 < bestLen) {
                bestLen = r - left + 1;
                bestLeft = left;
            }
            char lc = s[left];
            window[lc]--;
            if (need.count(lc) && window[lc] < need[lc]) formed--;
            left++;
        }
    }
    return bestLen == INT_MAX ? "" : s.substr(bestLeft, bestLen);
}

// =========================================================================
// FAST & SLOW POINTERS
// =========================================================================

struct ListNode {
    int val;
    ListNode* next;
    ListNode(int v) : val(v), next(nullptr) {}
};

// Linked List Cycle Detection (LC 141) - Time: O(n), Space: O(1)
bool hasCycle(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;
    }
    return false;
}

// Cycle Start Detection (LC 142) - Time: O(n), Space: O(1)
ListNode* detectCycleStart(ListNode* head) {
    ListNode* slow = head;
    ListNode* fast = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            ListNode* entry = head;
            while (entry != slow) { entry = entry->next; slow = slow->next; }
            return entry;
        }
    }
    return nullptr;
}

// Happy Number (LC 202) - Time: O(log n), Space: O(1)
int digitSquareSum(int n) {
    int t = 0;
    while (n > 0) { int d = n % 10; t += d * d; n /= 10; }
    return t;
}

bool isHappy(int n) {
    int slow = n, fast = n;
    do {
        slow = digitSquareSum(slow);
        fast = digitSquareSum(digitSquareSum(fast));
    } while (slow != fast);
    return slow == 1;
}

// =========================================================================
// MERGE INTERVALS
// =========================================================================

// Merge Intervals (LC 56) - Time: O(n log n), Space: O(n)
vector<vector<int>> mergeIntervals(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> merged = {intervals[0]};
    for (int i = 1; i < (int)intervals.size(); i++) {
        if (intervals[i][0] <= merged.back()[1])
            merged.back()[1] = max(merged.back()[1], intervals[i][1]);
        else
            merged.push_back(intervals[i]);
    }
    return merged;
}

// Insert Interval (LC 57) - Time: O(n), Space: O(n)
vector<vector<int>> insertInterval(const vector<vector<int>>& intervals, vector<int> newIv) {
    vector<vector<int>> result;
    int i = 0, n = (int)intervals.size();

    // Add intervals ending before newIv starts
    while (i < n && intervals[i][1] < newIv[0]) result.push_back(intervals[i++]);

    // Merge overlapping intervals with newIv
    while (i < n && intervals[i][0] <= newIv[1]) {
        newIv[0] = min(newIv[0], intervals[i][0]);
        newIv[1] = max(newIv[1], intervals[i][1]);
        i++;
    }
    result.push_back(newIv);

    // Add remaining
    while (i < n) result.push_back(intervals[i++]);
    return result;
}

// =========================================================================
// TOP-K ELEMENTS
// =========================================================================

// Kth Largest Element (LC 215) - Time: O(n log k), Space: O(k)
int findKthLargest(const vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int n : nums) {
        heap.push(n);
        if ((int)heap.size() > k) heap.pop();
    }
    return heap.top();
}

// Top K Frequent Elements (LC 347) - Time: O(n log k), Space: O(n)
vector<int> topKFrequent(const vector<int>& nums, int k) {
    unordered_map<int, int> freq;
    for (int n : nums) freq[n]++;

    // Min-heap of (frequency, value)
    using P = pair<int, int>;
    priority_queue<P, vector<P>, greater<P>> heap;
    for (auto& [val, cnt] : freq) {
        heap.push({cnt, val});
        if ((int)heap.size() > k) heap.pop();
    }

    vector<int> result;
    while (!heap.empty()) { result.push_back(heap.top().second); heap.pop(); }
    return result;
}

// Top K Frequent - Bucket Sort (LC 347) - Time: O(n), Space: O(n)
vector<int> topKFrequentBucket(const vector<int>& nums, int k) {
    unordered_map<int, int> freq;
    for (int n : nums) freq[n]++;

    int sz = (int)nums.size();
    vector<vector<int>> buckets(sz + 1);
    for (auto& [val, cnt] : freq) buckets[cnt].push_back(val);

    vector<int> result;
    for (int i = sz; i >= 0 && (int)result.size() < k; i--)
        for (int v : buckets[i]) { result.push_back(v); if ((int)result.size() == k) break; }
    return result;
}

// =========================================================================
// HELPERS
// =========================================================================

void printVec(const vector<int>& v) {
    cout << "[";
    for (int i = 0; i < (int)v.size(); i++) { if (i) cout << ","; cout << v[i]; }
    cout << "]";
}

void printIntervals(const vector<vector<int>>& ivs) {
    for (auto& iv : ivs) cout << "[" << iv[0] << "," << iv[1] << "] ";
    cout << endl;
}

// =========================================================================
// MAIN
// =========================================================================

int main() {
    cout << "=== TWO POINTERS ===" << endl;
    auto ts = twoSumII({2, 7, 11, 15}, 9);
    cout << "Two Sum II [2,7,11,15] t=9: "; printVec(ts); cout << endl;

    vector<int> nums3 = {-1, 0, 1, 2, -1, -4};
    auto trips = threeSum(nums3);
    cout << "3Sum: "; for (auto& t : trips) { printVec(t); cout << " "; } cout << endl;

    cout << "Max Area [1,8,6,2,5,4,8,3,7]: " << maxArea({1,8,6,2,5,4,8,3,7}) << endl;

    cout << "\n=== SLIDING WINDOW ===" << endl;
    cout << "Longest unique 'abcabcbb': " << lengthOfLongestSubstring("abcabcbb") << endl;
    cout << "Min window 'ADOBECODEBANC','ABC': " << minWindow("ADOBECODEBANC", "ABC") << endl;

    cout << "\n=== FAST & SLOW ===" << endl;
    cout << "Happy 19: " << (isHappy(19) ? "true" : "false") << endl;
    cout << "Happy 2: " << (isHappy(2) ? "true" : "false") << endl;

    ListNode* a = new ListNode(1);
    ListNode* b = new ListNode(2);
    ListNode* c = new ListNode(3);
    a->next = b; b->next = c; c->next = b;
    cout << "Cycle: " << (hasCycle(a) ? "true" : "false")
         << ", starts at: " << detectCycleStart(a)->val << endl;

    cout << "\n=== MERGE INTERVALS ===" << endl;
    vector<vector<int>> intervals = {{1,3},{2,6},{8,10},{15,18}};
    cout << "Merged: "; printIntervals(mergeIntervals(intervals));
    cout << "Inserted: "; printIntervals(insertInterval({{1,3},{6,9}}, {2,5}));

    cout << "\n=== TOP-K ===" << endl;
    cout << "Kth largest k=2: " << findKthLargest({3,2,1,5,6,4}, 2) << endl;
    cout << "Top 2 frequent: "; printVec(topKFrequent({1,1,1,2,2,3}, 2)); cout << endl;
    cout << "Top 2 bucket: "; printVec(topKFrequentBucket({1,1,1,2,2,3}, 2)); cout << endl;

    delete a; delete b; delete c;
    return 0;
}
