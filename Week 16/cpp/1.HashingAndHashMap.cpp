/*
 * WEEK 16 - C++ DSA
 * Topic: Hashing Fundamentals + Classic HashMap Problems
 * File: 1.HashingAndHashMap.cpp
 *
 * CONCEPT:
 *     A hash table maps keys to array slots through a hash function so that
 *     insert / find / erase are O(1) average. C++ exposes this via
 *     std::unordered_map and std::unordered_set (since C++11).
 *
 * KEY POINTS:
 *     - std::unordered_map<K,V>: hash table; average O(1).
 *     - std::map<K,V>: red-black tree; O(log n) but ordered.
 *     - Default load-factor threshold ~ 1.0; rehash via .rehash() / .reserve().
 *     - Custom types need a std::hash specialization or a hash functor.
 *     - Collisions are handled with chaining (each bucket holds a linked list
 *       of nodes).
 *
 * ALGORITHM / APPROACH:
 *     For each problem we (1) choose a key that captures the invariant,
 *     (2) probe the hash table in O(1), (3) update or insert the key.
 *
 * C++-SPECIFIC NOTES:
 *     - Use `auto it = map.find(key); if (it != map.end())` to avoid two lookups.
 *     - Since C++17, structured bindings: `for (auto& [k, v] : map)`.
 *     - Use `emplace`/`try_emplace` to avoid copies.
 *     - Pre-allocate with `.reserve(n)` when n is known to skip rehashes.
 *     - For sortable hash keys (anagrams), `std::string` works because
 *       std::hash<std::string> exists.
 *
 * DRY RUN:
 *     Example A — twoSum({2,7,11,15}, 9)
 *         i=0 x=2 complement=7 not in seen -> insert {2:0}
 *         i=1 x=7 complement=2  found at 0 -> return {0,1}
 *
 *     Example B — hasZeroSumSubarray({4,2,-3,1,6})
 *         seen={0} sum=0
 *         x=4  sum=4  not in seen -> insert
 *         x=2  sum=6  not in seen -> insert
 *         x=-3 sum=3  not in seen -> insert
 *         x=1  sum=4  HIT (subarray 2,-3,1 sums to 0) -> true
 *
 * COMPLEXITY:
 *     twoSum                 O(n) time, O(n) space
 *     frequency              O(n) time, O(n) space
 *     groupAnagrams          O(n * k log k) time, O(n*k) space
 *     hasZeroSumSubarray     O(n) time, O(n) space
 *     subarraySum            O(n) time, O(n) space
 *     longestConsecutive     O(n) average time, O(n) space
 */

#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>

// PROBLEM 1: Two Sum
std::vector<int> twoSum(const std::vector<int>& nums, int target) {
    std::unordered_map<int,int> seen;            // value -> index
    seen.reserve(nums.size());
    for (int i = 0; i < (int)nums.size(); ++i) {
        int complement = target - nums[i];
        auto it = seen.find(complement);
        if (it != seen.end()) return {it->second, i};
        seen.emplace(nums[i], i);
    }
    return {-1, -1};
}

// PROBLEM 2: Frequency
std::unordered_map<int,int> frequency(const std::vector<int>& arr) {
    std::unordered_map<int,int> freq;
    freq.reserve(arr.size());
    for (int x : arr) ++freq[x];                  // operator[] inserts default 0
    return freq;
}

// PROBLEM 3: Group Anagrams
std::vector<std::vector<std::string>> groupAnagrams(const std::vector<std::string>& strs) {
    std::unordered_map<std::string, std::vector<std::string>> groups;
    for (const auto& s : strs) {
        std::string key = s;
        std::sort(key.begin(), key.end());        // canonical anagram form
        groups[key].push_back(s);
    }
    std::vector<std::vector<std::string>> out;
    out.reserve(groups.size());
    for (auto& [_, vec] : groups) out.push_back(std::move(vec));
    return out;
}

// PROBLEM 4: Subarray With Zero Sum
bool hasZeroSumSubarray(const std::vector<int>& arr) {
    std::unordered_set<long long> prefixSums{0}; // include empty prefix
    long long sum = 0;
    for (int x : arr) {
        sum += x;
        if (prefixSums.count(sum)) return true;
        prefixSums.insert(sum);
    }
    return false;
}

int subarraySum(const std::vector<int>& nums, int k) {
    std::unordered_map<long long,int> counts;
    counts[0] = 1;
    long long sum = 0;
    int total = 0;
    for (int x : nums) {
        sum += x;
        auto it = counts.find(sum - k);
        if (it != counts.end()) total += it->second;
        ++counts[sum];
    }
    return total;
}

// PROBLEM 5: Longest Consecutive Sequence
int longestConsecutive(const std::vector<int>& nums) {
    std::unordered_set<int> s(nums.begin(), nums.end());
    int best = 0;
    for (int x : s) {
        if (s.find(x - 1) == s.end()) {           // start of a run
            int length = 1;
            while (s.find(x + length) != s.end()) ++length;
            if (length > best) best = length;
        }
    }
    return best;
}

// ---------- driver ----------
template <typename T>
void printVec(const std::vector<T>& v) {
    std::cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        std::cout << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    std::cout << "]";
}

int main() {
    std::cout << "=== Two Sum ===\n";
    printVec(twoSum({2,7,11,15}, 9)); std::cout << "\n";   // [0, 1]
    printVec(twoSum({3,2,4}, 6));     std::cout << "\n";   // [1, 2]

    std::cout << "\n=== Frequency Count ===\n";
    auto fr = frequency({1,3,2,3,1,1,4});
    for (auto& [k,v] : fr) std::cout << k << "->" << v << "  ";
    std::cout << "\n";

    std::cout << "\n=== Group Anagrams ===\n";
    auto groups = groupAnagrams({"eat","tea","tan","ate","nat","bat"});
    for (auto& g : groups) { printVec(g); std::cout << "\n"; }

    std::cout << "\n=== Subarray With Zero Sum ===\n";
    std::cout << std::boolalpha;
    std::cout << hasZeroSumSubarray({4,2,-3,1,6})  << "\n"; // true
    std::cout << hasZeroSumSubarray({4,2,0,1,6})   << "\n"; // true
    std::cout << hasZeroSumSubarray({-3,2,3,1,6})  << "\n"; // false

    std::cout << "\n=== Subarray Sum == k ===\n";
    std::cout << subarraySum({1,1,1}, 2) << "\n";  // 2
    std::cout << subarraySum({1,2,3}, 3) << "\n";  // 2

    std::cout << "\n=== Longest Consecutive Sequence ===\n";
    std::cout << longestConsecutive({100,4,200,1,3,2}) << "\n";          // 4
    std::cout << longestConsecutive({0,3,7,2,5,8,4,6,0,1}) << "\n";      // 9
}

/*
 * NOTES (C++ vs Java):
 *   - Java has only one HashMap; C++ distinguishes std::unordered_map (hash)
 *     and std::map (balanced BST). Pick the right one.
 *   - operator[] on map default-constructs the value if absent (handy for
 *     counters); Java requires merge() or getOrDefault().
 *   - find() returns an iterator; comparing to .end() avoids a double lookup,
 *     unlike Java's containsKey + get pattern.
 *   - reserve(n) skips rehashes — there's no Java equivalent except passing
 *     initialCapacity to the constructor.
 *   - C++ values are by-value; use std::move when transferring into result
 *     containers to avoid copies.
 *   - Custom keys need either std::hash<T> specialization or a Hash functor
 *     template parameter; in Java you override hashCode/equals.
 */
