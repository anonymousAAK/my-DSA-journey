/*
 * WEEK 9 - C++ DSA
 * Topic: Quick Sort
 * File: 3.quick_sort.cpp
 *
 * CONCEPT:
 *     Pick a pivot, partition into < / > halves, recurse.
 *
 * KEY POINTS:
 *     - Lomuto and Hoare partition schemes both shown.
 *     - Randomised pivot avoids O(n^2) worst on adversarial input.
 *     - QuickSelect uses the same partition for average O(n) selection.
 *
 * ALGORITHM / APPROACH:
 *     Lomuto / Hoare partition + recursion (see code).
 *
 * C++-SPECIFIC NOTES:
 *     - std::mt19937 with a fixed seed for reproducibility.
 *     - std::uniform_int_distribution to pick a pivot index.
 *
 * DRY RUN:
 *     {10,7,8,9,1,5} Lomuto with pivot=5:
 *         scan -> swap 10 and 1 -> [1,7,8,9,10,5]
 *         final swap pivot -> [1,5,8,9,10,7]
 *         pivot at index 1; recurse left/right.
 *
 * COMPLEXITY:
 *     Average:  O(n log n) time, O(log n) stack
 *     Worst:    O(n^2) time
 *     Stable:   NO
 */

#include <iostream>
#include <vector>
#include <random>
#include <algorithm>

static std::mt19937 g_rng(42);

int lomutoPartition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j] <= pivot) {
            ++i;
            std::swap(arr[i], arr[j]);
        }
    }
    std::swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSortLomuto(std::vector<int>& arr, int low, int high) {
    if (low >= high) return;
    int p = lomutoPartition(arr, low, high);
    quickSortLomuto(arr, low, p - 1);
    quickSortLomuto(arr, p + 1, high);
}

int hoarePartition(std::vector<int>& arr, int low, int high) {
    int pivot = arr[low];
    int i = low - 1, j = high + 1;
    while (true) {
        do { ++i; } while (arr[i] < pivot);
        do { --j; } while (arr[j] > pivot);
        if (i >= j) return j;
        std::swap(arr[i], arr[j]);
    }
}

void quickSortHoare(std::vector<int>& arr, int low, int high) {
    if (low >= high) return;
    int p = hoarePartition(arr, low, high);
    quickSortHoare(arr, low, p);
    quickSortHoare(arr, p + 1, high);
}

void quickSortRandom(std::vector<int>& arr, int low, int high) {
    if (low >= high) return;
    std::uniform_int_distribution<int> dist(low, high);
    int pivotIdx = dist(g_rng);
    std::swap(arr[pivotIdx], arr[high]);
    int p = lomutoPartition(arr, low, high);
    quickSortRandom(arr, low, p - 1);
    quickSortRandom(arr, p + 1, high);
}

int quickSelect(std::vector<int>& arr, int low, int high, int k) {
    if (low == high) return arr[low];
    std::uniform_int_distribution<int> dist(low, high);
    int pivotIdx = dist(g_rng);
    std::swap(arr[pivotIdx], arr[high]);
    int p = lomutoPartition(arr, low, high);
    int rank = p - low + 1;
    if (rank == k)    return arr[p];
    else if (k < rank) return quickSelect(arr, low, p - 1, k);
    else               return quickSelect(arr, p + 1, high, k - rank);
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    std::vector<int> base = {10, 7, 8, 9, 1, 5};

    std::vector<int> arr1 = base;
    std::cout << "Lomuto QuickSort:\n";
    std::cout << "Before: "; print(arr1); std::cout << "\n";
    quickSortLomuto(arr1, 0, static_cast<int>(arr1.size()) - 1);
    std::cout << "After:  "; print(arr1); std::cout << "\n";

    std::vector<int> arr2 = base;
    std::cout << "\nHoare QuickSort:\n";
    std::cout << "Before: "; print(arr2); std::cout << "\n";
    quickSortHoare(arr2, 0, static_cast<int>(arr2.size()) - 1);
    std::cout << "After:  "; print(arr2); std::cout << "\n";

    std::vector<int> arr3 = base;
    std::cout << "\nRandomized QuickSort:\n";
    quickSortRandom(arr3, 0, static_cast<int>(arr3.size()) - 1);
    std::cout << "After:  "; print(arr3); std::cout << "\n";

    std::vector<int> worst = {1, 2, 3, 4, 5, 6, 7, 8};
    quickSortRandom(worst, 0, static_cast<int>(worst.size()) - 1);
    std::cout << "\nAlready sorted -> randomised: "; print(worst); std::cout << "\n";

    std::vector<int> arr4 = {3, 2, 1, 5, 6, 4};
    std::cout << "\nQuickSelect — kth smallest:\n";
    for (int k = 1; k <= static_cast<int>(arr4.size()); ++k) {
        std::vector<int> copy = arr4;
        std::cout << "k=" << k << ": "
                  << quickSelect(copy, 0, static_cast<int>(copy.size()) - 1, k) << "\n";
    }

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - <random> + std::mt19937 replaces java.util.Random.
 *     - std::nth_element (in <algorithm>) is the STL quickselect equivalent.
 *     - std::sort is faster in practice for general sorting; we hand-roll
 *       for instruction.
 */
