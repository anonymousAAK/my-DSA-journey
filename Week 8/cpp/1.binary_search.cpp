/*
 * WEEK 8 - C++ DSA
 * Topic: Binary Search
 * File: 1.binary_search.cpp
 *
 * CONCEPT:
 *     Find a value in a sorted vector in O(log n) by halving the search
 *     interval each step.
 *
 * KEY POINTS:
 *     - PREREQUISITE: vector must be sorted.
 *     - Compute mid as low + (high - low) / 2 to avoid overflow.
 *     - Variants: first/last occurrence, count, rotated-array search.
 *
 * ALGORITHM / APPROACH:
 *     Standard iterative:
 *         low = 0; high = n - 1
 *         while (low <= high) {
 *             mid = low + (high - low) / 2
 *             if arr[mid] == target return mid
 *             else if arr[mid] < target low = mid + 1
 *             else high = mid - 1
 *         }
 *         return -1
 *
 * C++-SPECIFIC NOTES:
 *     - <algorithm> provides std::lower_bound / std::upper_bound /
 *       std::binary_search; we implement manually for instruction.
 *     - Be careful with size_t vs int when high may go to -1.
 *
 * DRY RUN:
 *     [-5,-2,0,1,3,5,7,9,11], target=5:
 *         low=0 high=8 mid=4 arr[4]=3 < 5 -> low=5
 *         low=5 high=8 mid=6 arr[6]=7 > 5 -> high=5
 *         low=5 high=5 mid=5 arr[5]=5 -> return 5
 *
 * COMPLEXITY:
 *     Time:  O(log n)
 *     Space: O(1) iterative, O(log n) recursive
 */

#include <iostream>
#include <vector>
#include <algorithm>

int binarySearch(const std::vector<int>& arr, int target) {
    int low = 0, high = static_cast<int>(arr.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}

int binarySearchRec(const std::vector<int>& arr, int target, int low, int high) {
    if (low > high) return -1;
    int mid = low + (high - low) / 2;
    if (arr[mid] == target) return mid;
    else if (arr[mid] < target) return binarySearchRec(arr, target, mid + 1, high);
    else return binarySearchRec(arr, target, low, mid - 1);
}

int firstOccurrence(const std::vector<int>& arr, int target) {
    int low = 0, high = static_cast<int>(arr.size()) - 1, result = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) { result = mid; high = mid - 1; }
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return result;
}

int lastOccurrence(const std::vector<int>& arr, int target) {
    int low = 0, high = static_cast<int>(arr.size()) - 1, result = -1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) { result = mid; low = mid + 1; }
        else if (arr[mid] < target) low = mid + 1;
        else high = mid - 1;
    }
    return result;
}

int countOccurrences(const std::vector<int>& arr, int target) {
    int first = firstOccurrence(arr, target);
    if (first == -1) return 0;
    return lastOccurrence(arr, target) - first + 1;
}

int searchRotated(const std::vector<int>& arr, int target) {
    int low = 0, high = static_cast<int>(arr.size()) - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) return mid;
        if (arr[low] <= arr[mid]) {                      // left half sorted
            if (arr[low] <= target && target < arr[mid]) high = mid - 1;
            else                                          low  = mid + 1;
        } else {                                          // right half sorted
            if (arr[mid] < target && target <= arr[high]) low  = mid + 1;
            else                                          high = mid - 1;
        }
    }
    return -1;
}

int main() {
    std::vector<int> sorted = {-5, -2, 0, 1, 3, 5, 7, 9, 11};
    std::cout << "Array: [-5,-2,0,1,3,5,7,9,11]\n";
    std::cout << "binarySearch(5) = " << binarySearch(sorted, 5) << "\n";
    std::cout << "binarySearch(0) = " << binarySearch(sorted, 0) << "\n";
    std::cout << "binarySearch(4) = " << binarySearch(sorted, 4) << "\n";
    std::cout << "binarySearchRec(7) = "
              << binarySearchRec(sorted, 7, 0, static_cast<int>(sorted.size()) - 1) << "\n";

    std::vector<int> withDups = {1, 2, 2, 2, 3, 4, 4, 5};
    std::cout << "\nArray with duplicates: [1,2,2,2,3,4,4,5]\n";
    std::cout << "firstOccurrence(2) = " << firstOccurrence(withDups, 2) << "\n";
    std::cout << "lastOccurrence(2)  = " << lastOccurrence(withDups, 2) << "\n";
    std::cout << "countOccurrences(2) = " << countOccurrences(withDups, 2) << "\n";
    std::cout << "countOccurrences(4) = " << countOccurrences(withDups, 4) << "\n";
    std::cout << "countOccurrences(6) = " << countOccurrences(withDups, 6) << "\n";

    std::vector<int> rotated = {4, 5, 6, 7, 0, 1, 2};
    std::cout << "\nRotated array: [4,5,6,7,0,1,2]\n";
    std::cout << "searchRotated(0) = " << searchRotated(rotated, 0) << "\n";
    std::cout << "searchRotated(6) = " << searchRotated(rotated, 6) << "\n";
    std::cout << "searchRotated(3) = " << searchRotated(rotated, 3) << "\n";

    // STL alternative
    auto it = std::lower_bound(sorted.begin(), sorted.end(), 5);
    std::cout << "\nlower_bound(5) idx = " << (it - sorted.begin()) << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - <algorithm> already has std::binary_search, std::lower_bound,
 *       std::upper_bound — the standard library equivalents.
 *     - Avoid using size_t arithmetic that can underflow; cast to int for
 *       indices that may decrease past zero.
 */
