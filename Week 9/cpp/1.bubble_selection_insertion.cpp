/*
 * WEEK 9 - C++ DSA
 * Topic: Bubble / Selection / Insertion Sort
 * File: 1.bubble_selection_insertion.cpp
 *
 * CONCEPT:
 *     Three classic O(n^2) elementary sorts; differ in swaps,
 *     stability, and best-case behaviour.
 *
 * KEY POINTS:
 *     Bubble:    early-stop O(n) best; stable.
 *     Selection: O(n) swaps; not stable.
 *     Insertion: O(n) best on nearly-sorted; stable; used in hybrid sorts.
 *
 * ALGORITHM / APPROACH:
 *     See per-function code; identical to Java.
 *
 * C++-SPECIFIC NOTES:
 *     - std::swap and references give clean in-place code.
 *     - std::sort (introsort) is the production sort; we hand-roll here.
 *
 * DRY RUN:
 *     arr = {64, 25, 12, 22, 11}
 *     bubble pass1: {25,12,22,11,64}
 *     bubble pass2: {12,22,11,25,64}
 *     bubble pass3: {12,11,22,25,64}
 *     bubble pass4: {11,12,22,25,64} (no swaps, done)
 *
 * COMPLEXITY:
 *     Bubble    : O(n^2) avg/worst, O(n) best, O(1) space, stable.
 *     Selection : O(n^2), O(1) space, not stable.
 *     Insertion : O(n^2) avg/worst, O(n) best, O(1) space, stable.
 */

#include <iostream>
#include <vector>
#include <algorithm>

void bubbleSort(std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; ++j) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void selectionSort(std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n - 1; ++i) {
        int minIdx = i;
        for (int j = i + 1; j < n; ++j) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        if (minIdx != i) std::swap(arr[i], arr[minIdx]);
    }
}

void insertionSort(std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    for (int i = 1; i < n; ++i) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            --j;
        }
        arr[j + 1] = key;
    }
}

long long countInversions(const std::vector<int>& arr) {
    long long count = 0;
    int n = static_cast<int>(arr.size());
    for (int i = 0; i < n; ++i)
        for (int j = i + 1; j < n; ++j)
            if (arr[i] > arr[j]) ++count;
    return count;
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    std::vector<int> base = {64, 25, 12, 22, 11};

    std::vector<int> arr1 = base;
    std::cout << "Bubble Sort:\n";
    std::cout << "Before: "; print(arr1); std::cout << "\n";
    bubbleSort(arr1);
    std::cout << "After:  "; print(arr1); std::cout << "\n";

    std::vector<int> arr2 = base;
    std::cout << "\nSelection Sort:\n";
    std::cout << "Before: "; print(arr2); std::cout << "\n";
    selectionSort(arr2);
    std::cout << "After:  "; print(arr2); std::cout << "\n";

    std::vector<int> arr3 = base;
    std::cout << "\nInsertion Sort:\n";
    std::cout << "Before: "; print(arr3); std::cout << "\n";
    insertionSort(arr3);
    std::cout << "After:  "; print(arr3); std::cout << "\n";

    std::vector<int> already = {1, 2, 3, 4, 5};
    std::cout << "\nAlready sorted — bubble sort:\n";
    std::cout << "Before: "; print(already); std::cout << "\n";
    bubbleSort(already);
    std::cout << "After:  "; print(already); std::cout << "\n";

    std::vector<int> inv = {5, 3, 1, 4, 2};
    std::cout << "\nArray: "; print(inv); std::cout << "\n";
    std::cout << "Inversions: " << countInversions(inv) << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::swap removes the temp-variable boilerplate.
 *     - std::sort uses introsort (quicksort + heapsort fallback + insertion
 *       for small ranges) — fast and stable-ish (use std::stable_sort for
 *       guaranteed stability).
 *     - long long suits inversion counts that can be quadratic in n.
 */
