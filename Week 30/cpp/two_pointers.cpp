/*
 * WEEK 30 - C++ ADVANCED TOPICS
 * Topic: Two Pointers Pattern
 * File: two_pointers.cpp
 *
 * CONCEPT:
 *   Two indices move through an array (often sorted) under monotonic rules.
 *   Each index advances at most n times -> O(n) or O(n log n) overall.
 *
 * KEY POINTS:
 *   - On sorted input, sum a[l]+a[r] is monotone in l/r; advance based on
 *     comparison with target.
 *   - For container/area problems, always shrink the smaller side.
 *
 * ALGORITHM / APPROACH:
 *   TWO SUM SORTED: l=0,r=n-1; shift by sign of s vs target.
 *   3SUM:           sort + iterate i + two-pointer inside.
 *   MAX AREA:       shrink lower wall each step.
 *   REMOVE DUPS:    write pointer + read pointer in a sorted array.
 *
 * C++-SPECIFIC NOTES:
 *   - std::sort with default comparator for int.
 *   - std::vector::push_back + initializer_list for clean triple insertion.
 *
 * DRY RUN / EXAMPLE:
 *   twoSumII [2,7,11,15], t=9 -> {1,2}.
 *   3Sum [-1,0,1,2,-1,-4]   -> [[-1,-1,2],[-1,0,1]].
 *   max area [1,8,6,2,5,4,8,3,7] -> 49.
 *
 * COMPLEXITY:
 *   Two-sum O(n); 3Sum O(n^2); Max area O(n).
 */

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

pair<int,int> twoSumII(vector<int>& nums, int target) {
    int l = 0, r = (int)nums.size() - 1;
    while (l < r) {
        int s = nums[l] + nums[r];
        if (s == target) return {l + 1, r + 1};
        if (s < target) ++l; else --r;
    }
    return {-1, -1};
}

vector<vector<int>> threeSum(vector<int> nums) {
    sort(nums.begin(), nums.end());
    vector<vector<int>> out;
    int n = (int)nums.size();
    for (int i = 0; i < n - 2; ++i) {
        if (i > 0 && nums[i] == nums[i-1]) continue;
        int l = i + 1, r = n - 1;
        while (l < r) {
            int s = nums[i] + nums[l] + nums[r];
            if (s == 0) {
                out.push_back({nums[i], nums[l], nums[r]});
                while (l < r && nums[l] == nums[l+1]) ++l;
                while (l < r && nums[r] == nums[r-1]) --r;
                ++l; --r;
            } else if (s < 0) ++l;
            else --r;
        }
    }
    return out;
}

int maxArea(const vector<int>& h) {
    int l = 0, r = (int)h.size() - 1, best = 0;
    while (l < r) {
        best = max(best, (r - l) * min(h[l], h[r]));
        if (h[l] < h[r]) ++l; else --r;
    }
    return best;
}

int removeDuplicatesSorted(vector<int>& nums) {
    if (nums.empty()) return 0;
    int w = 1;
    for (int r = 1; r < (int)nums.size(); ++r)
        if (nums[r] != nums[w-1]) nums[w++] = nums[r];
    return w;
}

int main() {
    vector<int> arr = {2,7,11,15};
    auto p = twoSumII(arr, 9);
    cout << "Two Sum II [2,7,11,15] t=9: " << p.first << " " << p.second << "\n";

    auto triples = threeSum({-1,0,1,2,-1,-4});
    cout << "3Sum:";
    for (auto& t : triples) { cout << " ["; for (int x : t) cout << x << ","; cout << "]"; }
    cout << "\n";

    cout << "Max area: " << maxArea({1,8,6,2,5,4,8,3,7}) << "\n";

    vector<int> v = {0,0,1,1,1,2,2,3,3,4};
    int n = removeDuplicatesSorted(v);
    cout << "After removeDuplicates: len=" << n << " prefix:";
    for (int i = 0; i < n; ++i) cout << " " << v[i];
    cout << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - std::sort + index-based two-pointer; same algorithm.
 *   - We add removeDuplicatesSorted (LC 26) to broaden the pattern.
 */
