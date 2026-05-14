/*
 * =============================================================================
 * Week 16 — Hash Tables & Hashing  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. two_sum                      — classic two-sum with unordered_map
 *   2. frequency_count              — count element frequencies
 *   3. group_anagrams               — group strings by sorted-key
 *   4. subarray_sum_equals_k        — prefix-sum + hash-map
 *   5. longest_consecutive_sequence — O(n) using unordered_set
 *
 * Complexity cheat-sheet
 * ----------------------
 *   two_sum                    O(n)  avg    |  Space O(n)
 *   frequency_count            O(n)  avg    |  Space O(n)
 *   group_anagrams             O(n * m log m) avg  |  Space O(n * m)
 *   subarray_sum_equals_k      O(n)  avg    |  Space O(n)
 *   longest_consecutive_seq    O(n)  avg    |  Space O(n)
 *
 *   (avg assumes O(1) hash lookups; worst-case can degrade to O(n) per lookup)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o hashing hashing.cpp && ./hashing
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <algorithm>
#include <cassert>
#include <sstream>
#include <optional>

// ---------------------------------------------------------------------------
// Helper — pretty-print vectors
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// 1. Two Sum — return indices of two elements that sum to target
// ---------------------------------------------------------------------------
// Complexity:  Time O(n) avg  |  Space O(n)
std::optional<std::pair<int,int>> two_sum(const std::vector<int>& nums, int target) {
    std::unordered_map<int,int> seen;   // value -> index

    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
        int complement = target - nums[i];
        if (auto it = seen.find(complement); it != seen.end()) {
            return std::make_pair(it->second, i);
        }
        seen[nums[i]] = i;
    }
    return std::nullopt;  // no solution
}

// ---------------------------------------------------------------------------
// 2. Frequency Count
// ---------------------------------------------------------------------------
// Complexity:  Time O(n) avg  |  Space O(n)
std::unordered_map<int,int> frequency_count(const std::vector<int>& nums) {
    std::unordered_map<int,int> freq;
    for (int x : nums) ++freq[x];
    return freq;
}

// ---------------------------------------------------------------------------
// 3. Group Anagrams
// ---------------------------------------------------------------------------
// Complexity:  Time O(n * m log m) avg  |  Space O(n * m)
//              n = number of strings, m = max string length
std::vector<std::vector<std::string>> group_anagrams(const std::vector<std::string>& strs) {
    std::unordered_map<std::string, std::vector<std::string>> groups;

    for (const auto& s : strs) {
        std::string key = s;
        std::sort(key.begin(), key.end());   // canonical form
        groups[key].push_back(s);
    }

    std::vector<std::vector<std::string>> result;
    result.reserve(groups.size());
    for (auto& [key, group] : groups) {
        result.push_back(std::move(group));
    }
    return result;
}

// ---------------------------------------------------------------------------
// 4. Subarray Sum Equals K — count subarrays whose sum == k
// ---------------------------------------------------------------------------
// Idea: prefix_sum[j] - prefix_sum[i] == k  =>  prefix_sum[i] == prefix_sum[j] - k
// Complexity:  Time O(n) avg  |  Space O(n)
int subarray_sum_equals_k(const std::vector<int>& nums, int k) {
    std::unordered_map<int,int> prefix_count;
    prefix_count[0] = 1;   // empty prefix

    int sum = 0, count = 0;
    for (int x : nums) {
        sum += x;
        if (auto it = prefix_count.find(sum - k); it != prefix_count.end()) {
            count += it->second;
        }
        ++prefix_count[sum];
    }
    return count;
}

// ---------------------------------------------------------------------------
// 5. Longest Consecutive Sequence
// ---------------------------------------------------------------------------
// Complexity:  Time O(n) avg  |  Space O(n)
// Each element is visited at most twice (once as a potential start, once while
// extending), giving O(n) total work.
int longest_consecutive_sequence(const std::vector<int>& nums) {
    std::unordered_set<int> num_set(nums.begin(), nums.end());

    int best = 0;
    for (int n : num_set) {
        // Only start counting from the beginning of a sequence.
        if (num_set.count(n - 1)) continue;

        int length = 1;
        int cur = n;
        while (num_set.count(cur + 1)) {
            ++cur;
            ++length;
        }
        best = std::max(best, length);
    }
    return best;
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 16: Hash Tables & Hashing ===\n\n";

    // ---- 1. Two Sum ----
    {
        std::cout << "-- Two Sum --\n";
        std::vector<int> nums = {2, 7, 11, 15};
        auto res = two_sum(nums, 9);
        assert(res.has_value());
        auto [i, j] = *res;
        assert(nums[i] + nums[j] == 9);
        std::cout << "  nums=" << vec_str(nums) << " target=9 => indices (" << i << ", " << j << ")\n";

        auto none = two_sum(nums, 100);
        assert(!none.has_value());
        std::cout << "  target=100 => no solution (correct)\n\n";
    }

    // ---- 2. Frequency Count ----
    {
        std::cout << "-- Frequency Count --\n";
        std::vector<int> nums = {1, 2, 2, 3, 3, 3};
        auto freq = frequency_count(nums);
        assert(freq[1] == 1 && freq[2] == 2 && freq[3] == 3);
        std::cout << "  {1,2,2,3,3,3} => ";
        for (auto& [k,v] : freq) std::cout << k << ":" << v << " ";
        std::cout << "\n\n";
    }

    // ---- 3. Group Anagrams ----
    {
        std::cout << "-- Group Anagrams --\n";
        std::vector<std::string> strs = {"eat", "tea", "tan", "ate", "nat", "bat"};
        auto groups = group_anagrams(strs);
        std::cout << "  input: [\"eat\",\"tea\",\"tan\",\"ate\",\"nat\",\"bat\"]\n";
        std::cout << "  groups (" << groups.size() << "):\n";
        for (const auto& g : groups) {
            std::cout << "    [";
            for (std::size_t i = 0; i < g.size(); ++i) {
                if (i) std::cout << ", ";
                std::cout << "\"" << g[i] << "\"";
            }
            std::cout << "]\n";
        }
        assert(groups.size() == 3);
        std::cout << "\n";
    }

    // ---- 4. Subarray Sum Equals K ----
    {
        std::cout << "-- Subarray Sum Equals K --\n";
        std::vector<int> nums = {1, 1, 1};
        int cnt = subarray_sum_equals_k(nums, 2);
        assert(cnt == 2);
        std::cout << "  nums=" << vec_str(nums) << " k=2 => count=" << cnt << "\n";

        std::vector<int> nums2 = {1, 2, 3};
        int cnt2 = subarray_sum_equals_k(nums2, 3);
        assert(cnt2 == 2);  // [1,2] and [3]
        std::cout << "  nums=" << vec_str(nums2) << " k=3 => count=" << cnt2 << "\n\n";
    }

    // ---- 5. Longest Consecutive Sequence ----
    {
        std::cout << "-- Longest Consecutive Sequence --\n";
        std::vector<int> nums = {100, 4, 200, 1, 3, 2};
        int len = longest_consecutive_sequence(nums);
        assert(len == 4);  // 1,2,3,4
        std::cout << "  nums=" << vec_str(nums) << " => " << len << "\n";

        std::vector<int> nums2 = {0, 3, 7, 2, 5, 8, 4, 6, 0, 1};
        int len2 = longest_consecutive_sequence(nums2);
        assert(len2 == 9);  // 0..8
        std::cout << "  nums=" << vec_str(nums2) << " => " << len2 << "\n";
    }

    std::cout << "\nAll Week 16 tests passed.\n";
    return 0;
}
