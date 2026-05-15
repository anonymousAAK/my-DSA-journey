/*
 * WEEK 9 - C++ DSA
 * Topic: Merge Sort
 * File: 2.merge_sort.cpp
 *
 * CONCEPT:
 *     Recursive divide-and-conquer: split, sort halves, merge.
 *
 * KEY POINTS:
 *     - Stable; O(n log n) all cases; O(n) auxiliary space.
 *     - Useful for external sorting and inversion counting.
 *
 * ALGORITHM / APPROACH:
 *     mergeSort(arr, lo, hi):
 *         if lo >= hi: return
 *         mid = lo + (hi - lo) / 2
 *         mergeSort(arr, lo, mid)
 *         mergeSort(arr, mid + 1, hi)
 *         merge(arr, lo, mid, hi)
 *
 * C++-SPECIFIC NOTES:
 *     - std::vector slicing requires constructing temporary subvectors.
 *     - long long for inversion count; can be quadratic in n.
 *     - std::stable_sort offers the standard library equivalent.
 *
 * DRY RUN:
 *     {38,27,43,3,9,82,10} -> {3,9,10,27,38,43,82}
 *     Inversions of {2,4,1,3,5} = 3.
 *
 * COMPLEXITY:
 *     Time: O(n log n)  Space: O(n)  Stable.
 */

#include <iostream>
#include <vector>

void merge(std::vector<int>& arr, int left, int mid, int right) {
    std::vector<int> L(arr.begin() + left, arr.begin() + mid + 1);
    std::vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);
    int i = 0, j = 0, k = left;
    while (i < static_cast<int>(L.size()) && j < static_cast<int>(R.size())) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else              arr[k++] = R[j++];
    }
    while (i < static_cast<int>(L.size())) arr[k++] = L[i++];
    while (j < static_cast<int>(R.size())) arr[k++] = R[j++];
}

void mergeSort(std::vector<int>& arr, int left, int right) {
    if (left >= right) return;
    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

void mergeSort(std::vector<int>& arr) {
    if (arr.empty()) return;
    mergeSort(arr, 0, static_cast<int>(arr.size()) - 1);
}

// --- BONUS: count inversions during merge ---
long long mergeCount(std::vector<int>& arr, int left, int mid, int right) {
    std::vector<int> L(arr.begin() + left, arr.begin() + mid + 1);
    std::vector<int> R(arr.begin() + mid + 1, arr.begin() + right + 1);
    long long inv = 0;
    int i = 0, j = 0, k = left;
    while (i < static_cast<int>(L.size()) && j < static_cast<int>(R.size())) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else {
            inv += static_cast<long long>(L.size()) - i;
            arr[k++] = R[j++];
        }
    }
    while (i < static_cast<int>(L.size())) arr[k++] = L[i++];
    while (j < static_cast<int>(R.size())) arr[k++] = R[j++];
    return inv;
}

long long mergeSortCount(std::vector<int>& arr, int left, int right) {
    if (left >= right) return 0;
    int mid = left + (right - left) / 2;
    long long inv = mergeSortCount(arr, left, mid);
    inv += mergeSortCount(arr, mid + 1, right);
    inv += mergeCount(arr, left, mid, right);
    return inv;
}

long long countInversions(std::vector<int> arr) {
    if (arr.empty()) return 0;
    return mergeSortCount(arr, 0, static_cast<int>(arr.size()) - 1);
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    std::vector<int> arr = {38, 27, 43, 3, 9, 82, 10};
    std::cout << "Before: "; print(arr); std::cout << "\n";
    mergeSort(arr);
    std::cout << "After:  "; print(arr); std::cout << "\n";

    std::vector<int> single = {5};
    mergeSort(single);
    std::cout << "\nSingle: "; print(single); std::cout << "\n";

    std::vector<int> already = {1, 2, 3, 4, 5};
    mergeSort(already);
    std::cout << "Already sorted: "; print(already); std::cout << "\n";

    std::vector<int> reverse = {5, 4, 3, 2, 1};
    mergeSort(reverse);
    std::cout << "Reverse sorted: "; print(reverse); std::cout << "\n";

    std::cout << "\n=== Count Inversions ===\n";
    std::vector<std::vector<int>> tests = {
        {2, 4, 1, 3, 5},
        {5, 3, 1, 4, 2},
        {1, 2, 3}
    };
    for (auto& t : tests) {
        std::cout << "[";
        for (std::size_t i = 0; i < t.size(); ++i)
            std::cout << t[i] << (i + 1 < t.size() ? ", " : "");
        std::cout << "] -> inversions: " << countInversions(t) << "\n";
    }

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - Temporary subvectors L, R replace Arrays.copyOfRange.
 *     - countInversions takes its argument by value, leaving the caller's
 *       vector untouched (we sort the copy).
 *     - std::stable_sort gives the equivalent built-in routine.
 */
