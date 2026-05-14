/*
 * WEEK 6 - C++ DSA
 * Topic: Prefix Sum & Kadane's Algorithm
 * File: 4.prefix_sum_and_kadane.cpp
 *
 * CONCEPT:
 *     Prefix sum: build P[i] = arr[0]+...+arr[i] in O(n); answer any
 *     range sum [l,r] in O(1) as P[r] - (l ? P[l-1] : 0).
 *     Kadane: maximum contiguous subarray sum in O(n) via the DP
 *         current = max(arr[i], current + arr[i])
 *         best    = max(best, current)
 *
 * KEY POINTS:
 *     - Always seed Kadane with arr[0] to handle all-negative arrays.
 *     - Extended Kadane tracks (start, end) indices.
 *     - std::partial_sum (header <numeric>) is the STL prefix-sum.
 *
 * ALGORITHM / APPROACH:
 *     buildPrefix:
 *         P[0] = arr[0]; P[i] = P[i-1] + arr[i]
 *     rangeSum(l,r):
 *         (l == 0) ? P[r] : P[r] - P[l-1]
 *     kadane:
 *         best = current = arr[0]
 *         for i in [1..n): current = max(arr[i], current+arr[i]);
 *                          best    = max(best, current)
 *         return best
 *
 * C++-SPECIFIC NOTES:
 *     - Use long long for prefix sums to avoid overflow on large n.
 *     - std::max is in <algorithm>.
 *     - Tuple/array returns can use std::tuple or struct.
 *
 * DRY RUN:
 *     arr = {3,-1,2,4,-3,7}; P = {3,2,4,8,5,12}
 *     rangeSum(1,4) = 5 - 3 = 2
 *
 *     Kadane on {-2,1,-3,4,-1,2,1,-5,4}:
 *         current/best track to (6, [4,-1,2,1])
 *
 * COMPLEXITY:
 *     Prefix : O(n) build, O(1) per query, O(n) space
 *     Kadane : O(n) time, O(1) space
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <tuple>

std::vector<long long> buildPrefix(const std::vector<int>& arr) {
    std::size_t n = arr.size();
    std::vector<long long> prefix(n);
    if (n == 0) return prefix;
    prefix[0] = arr[0];
    for (std::size_t i = 1; i < n; ++i) prefix[i] = prefix[i - 1] + arr[i];
    return prefix;
}

long long rangeSum(const std::vector<long long>& prefix, int l, int r) {
    if (l == 0) return prefix[r];
    return prefix[r] - prefix[l - 1];
}

int maxSubarraySum(const std::vector<int>& arr) {
    int best = arr[0], current = arr[0];
    for (std::size_t i = 1; i < arr.size(); ++i) {
        current = std::max(arr[i], current + arr[i]);
        best = std::max(best, current);
    }
    return best;
}

std::tuple<int,int,int> maxSubarrayWithIndices(const std::vector<int>& arr) {
    int best = arr[0], current = arr[0];
    int start = 0, end = 0, tempStart = 0;
    for (std::size_t i = 1; i < arr.size(); ++i) {
        if (arr[i] > current + arr[i]) {
            current = arr[i];
            tempStart = static_cast<int>(i);
        } else {
            current += arr[i];
        }
        if (current > best) {
            best = current;
            start = tempStart;
            end = static_cast<int>(i);
        }
    }
    return {best, start, end};
}

void printVec(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

void printVec(const std::vector<long long>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    std::vector<int> arr = {3, -1, 2, 4, -3, 7};
    auto prefix = buildPrefix(arr);
    std::cout << "Array:  "; printVec(arr);    std::cout << "\n";
    std::cout << "Prefix: "; printVec(prefix); std::cout << "\n";
    std::cout << "Sum of arr[1..4] = " << rangeSum(prefix, 1, 4) << "\n";
    std::cout << "Sum of arr[0..5] = " << rangeSum(prefix, 0, 5) << "\n";
    std::cout << "Sum of arr[2..2] = " << rangeSum(prefix, 2, 2) << "\n";

    std::vector<int> test1 = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
    std::cout << "\nArray: "; printVec(test1); std::cout << "\n";
    std::cout << "Max subarray sum: " << maxSubarraySum(test1) << "\n";
    auto [best, s, e] = maxSubarrayWithIndices(test1);
    std::cout << "Max sum: " << best << " | Subarray arr[" << s << ".." << e << "] = [";
    for (int i = s; i <= e; ++i) std::cout << test1[i] << (i < e ? ", " : "");
    std::cout << "]\n";

    std::vector<int> allNeg = {-5, -1, -8, -3};
    std::cout << "\nAll-negative: "; printVec(allNeg); std::cout << "\n";
    std::cout << "Max sum: " << maxSubarraySum(allNeg) << "\n";

    std::vector<int> single = {42};
    std::cout << "\nSingle element [42]: max sum = "
              << maxSubarraySum(single) << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::partial_sum can build the prefix array in one call.
 *     - std::max takes any number of args via initializer_list overload.
 *     - long long is safer for accumulations than int.
 *     - Structured bindings make tuple returns ergonomic.
 */
