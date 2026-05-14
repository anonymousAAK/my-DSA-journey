/*
 * WEEK 6 - C++ DSA
 * Topic: Linear Search
 * File: 2.linear_search.cpp
 *
 * CONCEPT:
 *     Sequentially scan a vector for a target value; works on any
 *     vector regardless of order.
 *
 * KEY POINTS:
 *     - Returns first index of target, or -1 if absent.
 *     - Variants: last index, count, single-pass min/max.
 *     - For small N this can outperform binary search due to cache.
 *
 * ALGORITHM / APPROACH:
 *     for (size_t i = 0; i < arr.size(); ++i)
 *         if (arr[i] == target) return (int)i;
 *     return -1;
 *
 * C++-SPECIFIC NOTES:
 *     - std::find / std::find_if (header <algorithm>) do this in one
 *       call; we keep an explicit loop for instruction.
 *     - std::minmax_element returns iterators for both min and max.
 *
 * DRY RUN:
 *     arr = {4,2,7,1,9,3,7,5}
 *     search(7): hit at i=2 -> return 2
 *     search(6): scans all -> return -1
 *     last(7) : updates idx at i=2,6 -> return 6
 *
 * COMPLEXITY:
 *     Best:    O(1)
 *     Average: O(n)
 *     Worst:   O(n)
 *     Space:   O(1)
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <utility>

int linearSearch(const std::vector<int>& arr, int target) {
    for (std::size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] == target) return static_cast<int>(i);
    }
    return -1;
}

int linearSearchLast(const std::vector<int>& arr, int target) {
    int last = -1;
    for (std::size_t i = 0; i < arr.size(); ++i) {
        if (arr[i] == target) last = static_cast<int>(i);
    }
    return last;
}

int countOccurrences(const std::vector<int>& arr, int target) {
    int count = 0;
    for (int v : arr) if (v == target) ++count;
    return count;
}

std::pair<int,int> findMinMax(const std::vector<int>& arr) {
    if (arr.empty()) throw std::invalid_argument("Empty array");
    int mn = arr[0], mx = arr[0];
    for (int v : arr) {
        if (v < mn) mn = v;
        if (v > mx) mx = v;
    }
    return {mn, mx};
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i) {
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    }
    std::cout << "]";
}

int main() {
    std::vector<int> arr = {4, 2, 7, 1, 9, 3, 7, 5};
    std::cout << "Array: "; print(arr); std::cout << "\n";

    std::cout << "linearSearch(7) = " << linearSearch(arr, 7) << "\n";       // 2
    std::cout << "linearSearch(6) = " << linearSearch(arr, 6) << "\n";       // -1
    std::cout << "linearSearchLast(7) = " << linearSearchLast(arr, 7) << "\n"; // 6
    std::cout << "countOccurrences(7) = " << countOccurrences(arr, 7) << "\n"; // 2
    std::cout << "countOccurrences(6) = " << countOccurrences(arr, 6) << "\n"; // 0

    auto [mn, mx] = findMinMax(arr);
    std::cout << "Min = " << mn << ", Max = " << mx << "\n"; // 1, 9

    // STL alternative
    auto it = std::find(arr.begin(), arr.end(), 7);
    std::cout << "std::find(7) index = "
              << (it == arr.end() ? -1 : static_cast<int>(it - arr.begin()))
              << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::find returns an iterator; convert to index via subtraction.
 *     - Structured bindings (`auto [mn, mx] = ...`) replace returning a 2-array.
 *     - std::pair<int,int> is the natural return type for two values.
 *     - Throw std::invalid_argument instead of IllegalArgumentException.
 */
