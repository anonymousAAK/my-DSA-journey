/*
 * =============================================================================
 * Week 9 - Sorting (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Bubble Sort
 *   2. Selection Sort
 *   3. Insertion Sort
 *   4. Merge Sort (with inversion count)
 *   5. Quick Sort (Lomuto partition + randomized pivot)
 *   6. Quick Select (kth smallest element)
 *   7. Counting Sort
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// HELPER: print vector
// =============================================================================
void printVec(const vector<int>& v, const string& label = "") {
    if (!label.empty()) cout << label << ": ";
    cout << "[";
    for (size_t i = 0; i < v.size(); ++i) {
        cout << v[i] << (i + 1 < v.size() ? ", " : "");
    }
    cout << "]" << endl;
}

// =============================================================================
// 1. BUBBLE SORT
// =============================================================================
// Time: O(n^2) worst/avg, O(n) best (already sorted with early stop)
// Space: O(1)
// Stable: Yes
void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        bool swapped = false;
        for (int j = 0; j < n - 1 - i; ++j) {
            if (arr[j] > arr[j + 1]) {
                swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;  // early termination if already sorted
    }
}

// =============================================================================
// 2. SELECTION SORT
// =============================================================================
// Time: O(n^2) always (no early stop)
// Space: O(1)
// Stable: No (standard version)
void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n - 1; ++i) {
        int minIdx = i;
        for (int j = i + 1; j < n; ++j) {
            if (arr[j] < arr[minIdx]) minIdx = j;
        }
        if (minIdx != i) swap(arr[i], arr[minIdx]);
    }
}

// =============================================================================
// 3. INSERTION SORT
// =============================================================================
// Time: O(n^2) worst/avg, O(n) best (nearly sorted)
// Space: O(1)
// Stable: Yes
// Excellent for small arrays and nearly sorted data.
void insertionSort(vector<int>& arr) {
    int n = arr.size();
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

// =============================================================================
// 4. MERGE SORT (with Inversion Count)
// =============================================================================
// Time: O(n log n) always
// Space: O(n) for temporary arrays
// Stable: Yes
//
// An inversion is a pair (i, j) where i < j but arr[i] > arr[j].
// Merge sort naturally counts inversions during the merge step.

long long mergeAndCount(vector<int>& arr, int left, int mid, int right) {
    vector<int> temp;
    temp.reserve(right - left + 1);
    int i = left, j = mid + 1;
    long long inversions = 0;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp.push_back(arr[i++]);
        } else {
            // arr[i] > arr[j], so all remaining elements in left half
            // (from i to mid) form inversions with arr[j].
            inversions += (mid - i + 1);
            temp.push_back(arr[j++]);
        }
    }
    while (i <= mid) temp.push_back(arr[i++]);
    while (j <= right) temp.push_back(arr[j++]);

    copy(temp.begin(), temp.end(), arr.begin() + left);
    return inversions;
}

long long mergeSortAndCount(vector<int>& arr, int left, int right) {
    if (left >= right) return 0;
    int mid = left + (right - left) / 2;
    long long inversions = 0;
    inversions += mergeSortAndCount(arr, left, mid);
    inversions += mergeSortAndCount(arr, mid + 1, right);
    inversions += mergeAndCount(arr, left, mid, right);
    return inversions;
}

// Convenience wrapper for merge sort (returns inversion count)
long long mergeSort(vector<int>& arr) {
    if (arr.empty()) return 0;
    return mergeSortAndCount(arr, 0, static_cast<int>(arr.size()) - 1);
}

// =============================================================================
// 5. QUICK SORT (Lomuto Partition + Randomized Pivot)
// =============================================================================
// Time: O(n log n) avg, O(n^2) worst (mitigated by random pivot)
// Space: O(log n) avg call stack
// Stable: No

// Lomuto partition: pivot = arr[hi], partitions into [<=pivot | >pivot]
// Returns final position of pivot.
int lomutoPartition(vector<int>& arr, int lo, int hi) {
    int pivot = arr[hi];
    int i = lo - 1;  // boundary of elements <= pivot
    for (int j = lo; j < hi; ++j) {
        if (arr[j] <= pivot) {
            swap(arr[++i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[hi]);
    return i + 1;
}

// Randomized partition: swap random element to hi, then Lomuto
int randomizedPartition(vector<int>& arr, int lo, int hi) {
    static mt19937 rng(42);  // fixed seed for reproducibility
    int randIdx = uniform_int_distribution<int>(lo, hi)(rng);
    swap(arr[randIdx], arr[hi]);
    return lomutoPartition(arr, lo, hi);
}

void quickSortHelper(vector<int>& arr, int lo, int hi) {
    if (lo >= hi) return;
    int pivot = randomizedPartition(arr, lo, hi);
    quickSortHelper(arr, lo, pivot - 1);
    quickSortHelper(arr, pivot + 1, hi);
}

void quickSort(vector<int>& arr) {
    if (arr.empty()) return;
    quickSortHelper(arr, 0, static_cast<int>(arr.size()) - 1);
}

// =============================================================================
// 6. QUICK SELECT (Kth Smallest Element)
// =============================================================================
// Time: O(n) average, O(n^2) worst
// Space: O(1) iterative tail optimization
// Uses randomized partition for better average performance.
int quickSelect(vector<int>& arr, int lo, int hi, int k) {
    // k is 0-indexed: kth smallest has index k after sorting
    while (lo <= hi) {
        int pivotIdx = randomizedPartition(arr, lo, hi);
        if (pivotIdx == k) return arr[pivotIdx];
        else if (pivotIdx < k) lo = pivotIdx + 1;
        else hi = pivotIdx - 1;
    }
    return -1;  // should not reach here for valid input
}

// Find kth smallest (1-indexed for user convenience)
int kthSmallest(vector<int> arr, int k) {  // copy intentional
    return quickSelect(arr, 0, static_cast<int>(arr.size()) - 1, k - 1);
}

// =============================================================================
// 7. COUNTING SORT
// =============================================================================
// Time: O(n + k) where k = range of values
// Space: O(k) for count array + O(n) for output
// Stable: Yes
// Only works for non-negative integers (or can be adapted with offset).
vector<int> countingSort(const vector<int>& arr) {
    if (arr.empty()) return {};

    auto [minIt, maxIt] = minmax_element(arr.begin(), arr.end());  // C++17
    int minVal = *minIt, maxVal = *maxIt;
    int range = maxVal - minVal + 1;

    vector<int> count(range, 0);
    for (int x : arr) count[x - minVal]++;

    // Build prefix sum for stable sort
    for (int i = 1; i < range; ++i) count[i] += count[i - 1];

    // Build output in reverse for stability
    vector<int> output(arr.size());
    for (int i = static_cast<int>(arr.size()) - 1; i >= 0; --i) {
        output[--count[arr[i] - minVal]] = arr[i];
    }
    return output;
}

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 9: Sorting (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Bubble Sort ---
    cout << "\n--- 1. Bubble Sort ---" << endl;
    {
        vector<int> arr = {64, 34, 25, 12, 22, 11, 90};
        printVec(arr, "Before");
        bubbleSort(arr);
        printVec(arr, "After ");
    }

    // --- 2. Selection Sort ---
    cout << "\n--- 2. Selection Sort ---" << endl;
    {
        vector<int> arr = {29, 10, 14, 37, 13};
        printVec(arr, "Before");
        selectionSort(arr);
        printVec(arr, "After ");
    }

    // --- 3. Insertion Sort ---
    cout << "\n--- 3. Insertion Sort ---" << endl;
    {
        vector<int> arr = {12, 11, 13, 5, 6};
        printVec(arr, "Before");
        insertionSort(arr);
        printVec(arr, "After ");

        // Nearly sorted (best case)
        vector<int> arr2 = {1, 2, 4, 3, 5};
        printVec(arr2, "Nearly sorted before");
        insertionSort(arr2);
        printVec(arr2, "Nearly sorted after ");
    }

    // --- 4. Merge Sort (with inversion count) ---
    cout << "\n--- 4. Merge Sort (with Inversion Count) ---" << endl;
    {
        vector<int> arr = {5, 3, 2, 4, 1};
        printVec(arr, "Before");
        long long inv = mergeSort(arr);
        printVec(arr, "After ");
        cout << "Inversion count: " << inv << " (expected 8)" << endl;

        vector<int> arr2 = {1, 2, 3, 4, 5};
        long long inv2 = mergeSort(arr2);
        cout << "Sorted array inversions: " << inv2 << " (expected 0)" << endl;

        vector<int> arr3 = {5, 4, 3, 2, 1};
        long long inv3 = mergeSort(arr3);
        cout << "Reverse array inversions: " << inv3 << " (expected 10)" << endl;
    }

    // --- 5. Quick Sort ---
    cout << "\n--- 5. Quick Sort (Randomized Lomuto) ---" << endl;
    {
        vector<int> arr = {10, 80, 30, 90, 40, 50, 70};
        printVec(arr, "Before");
        quickSort(arr);
        printVec(arr, "After ");

        // Test with duplicates
        vector<int> arr2 = {3, 1, 4, 1, 5, 9, 2, 6, 5, 3};
        printVec(arr2, "With dups before");
        quickSort(arr2);
        printVec(arr2, "With dups after ");
    }

    // --- 6. Quick Select ---
    cout << "\n--- 6. Quick Select (Kth Smallest) ---" << endl;
    {
        vector<int> arr = {7, 2, 1, 6, 8, 5, 3, 4};
        cout << "Array: [7,2,1,6,8,5,3,4]" << endl;
        for (int k = 1; k <= 5; ++k) {
            cout << "  " << k << "th smallest = " << kthSmallest(arr, k) << endl;
        }
    }

    // --- 7. Counting Sort ---
    cout << "\n--- 7. Counting Sort ---" << endl;
    {
        vector<int> arr = {4, 2, 2, 8, 3, 3, 1};
        printVec(arr, "Before");
        auto sorted = countingSort(arr);
        printVec(sorted, "After ");

        // Test with negative numbers (using offset internally)
        vector<int> arr2 = {-5, 3, -2, 0, 1, -5, 3};
        printVec(arr2, "With negatives before");
        auto sorted2 = countingSort(arr2);
        printVec(sorted2, "With negatives after ");
    }

    // --- Comparison Summary ---
    cout << "\n--- Sorting Algorithm Comparison ---" << endl;
    cout << "| Algorithm      | Best     | Average   | Worst    | Space | Stable |" << endl;
    cout << "|----------------|----------|-----------|----------|-------|--------|" << endl;
    cout << "| Bubble         | O(n)     | O(n^2)    | O(n^2)   | O(1)  | Yes    |" << endl;
    cout << "| Selection      | O(n^2)   | O(n^2)    | O(n^2)   | O(1)  | No     |" << endl;
    cout << "| Insertion      | O(n)     | O(n^2)    | O(n^2)   | O(1)  | Yes    |" << endl;
    cout << "| Merge          | O(nlogn) | O(nlogn)  | O(nlogn) | O(n)  | Yes    |" << endl;
    cout << "| Quick          | O(nlogn) | O(nlogn)  | O(n^2)   | O(lgn)| No     |" << endl;
    cout << "| Counting       | O(n+k)   | O(n+k)    | O(n+k)   | O(k)  | Yes    |" << endl;

    cout << "\n========================================" << endl;
    cout << " All Week 9 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
