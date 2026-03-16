// Week 30: Interview Patterns
#include <iostream>
#include <vector>
#include <unordered_map>
#include <queue>
#include <algorithm>
using namespace std;

// Two Sum II (LC 167)
vector<int> twoSum(vector<int>& nums, int target) {
    int l = 0, r = nums.size()-1;
    while (l < r) {
        int s = nums[l]+nums[r];
        if (s == target) return {l, r};
        s < target ? l++ : r--;
    }
    return {};
}

// Longest Substring Without Repeating (LC 3)
int lengthOfLongestSubstring(string s) {
    unordered_map<char,int> idx;
    int left = 0, mx = 0;
    for (int r = 0; r < (int)s.size(); r++) {
        if (idx.count(s[r]) && idx[s[r]] >= left) left = idx[s[r]]+1;
        idx[s[r]] = r;
        mx = max(mx, r-left+1);
    }
    return mx;
}

// Happy Number (LC 202)
int nextNum(int n) { int t=0; while(n) { int d=n%10; t+=d*d; n/=10; } return t; }
bool isHappy(int n) {
    int slow=n, fast=nextNum(n);
    while (fast!=1 && slow!=fast) { slow=nextNum(slow); fast=nextNum(nextNum(fast)); }
    return fast==1;
}

// Merge Intervals (LC 56)
vector<vector<int>> merge(vector<vector<int>>& intervals) {
    sort(intervals.begin(), intervals.end());
    vector<vector<int>> merged = {intervals[0]};
    for (int i = 1; i < (int)intervals.size(); i++) {
        if (intervals[i][0] <= merged.back()[1])
            merged.back()[1] = max(merged.back()[1], intervals[i][1]);
        else merged.push_back(intervals[i]);
    }
    return merged;
}

// Kth Largest (LC 215)
int findKthLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int n : nums) { heap.push(n); if ((int)heap.size() > k) heap.pop(); }
    return heap.top();
}

int main() {
    vector<int> nums = {2,7,11,15};
    auto ts = twoSum(nums, 9);
    cout << "Two Sum: [" << ts[0] << "," << ts[1] << "]" << endl;
    cout << "Longest substring: " << lengthOfLongestSubstring("abcabcbb") << endl;
    cout << "Happy 19: " << (isHappy(19) ? "true" : "false") << endl;
    vector<vector<int>> intervals = {{1,3},{2,6},{8,10},{15,18}};
    auto merged = merge(intervals);
    cout << "Merge: "; for (auto& m : merged) cout << "[" << m[0] << "," << m[1] << "]"; cout << endl;
    vector<int> arr = {3,2,1,5,6,4};
    cout << "3rd largest: " << findKthLargest(arr, 3) << endl;
}
