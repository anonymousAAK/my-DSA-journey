/*
 * =============================================================================
 * Week 8 - Searching (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Binary search (iterative + recursive)
 *   2. First and last occurrence (lower_bound / upper_bound)
 *   3. Search in rotated sorted array
 *   4. Binary search on answer:
 *      a. Integer square root
 *      b. Koko eating bananas
 *      c. Ship packages within D days
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// 1. BINARY SEARCH
// =============================================================================

// Iterative binary search
// Time: O(log n)   Space: O(1)
int binarySearchIterative(const vector<int>& arr, int target) {
    int lo = 0, hi = static_cast<int>(arr.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;  // avoids overflow
        if (arr[mid] == target) return mid;
        else if (arr[mid] < target) lo = mid + 1;
        else hi = mid - 1;
    }
    return -1;  // not found
}

// Recursive binary search
// Time: O(log n)   Space: O(log n) call stack
int binarySearchRecursive(const vector<int>& arr, int target, int lo, int hi) {
    if (lo > hi) return -1;
    int mid = lo + (hi - lo) / 2;
    if (arr[mid] == target) return mid;
    if (arr[mid] < target)
        return binarySearchRecursive(arr, target, mid + 1, hi);
    return binarySearchRecursive(arr, target, lo, mid - 1);
}

int binarySearchRecursive(const vector<int>& arr, int target) {
    return binarySearchRecursive(arr, target, 0, static_cast<int>(arr.size()) - 1);
}

// =============================================================================
// 2. FIRST AND LAST OCCURRENCE
// =============================================================================

// Find first occurrence of target (leftmost position)
// Time: O(log n)   Space: O(1)
int firstOccurrence(const vector<int>& arr, int target) {
    int lo = 0, hi = static_cast<int>(arr.size()) - 1;
    int result = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) {
            result = mid;
            hi = mid - 1;  // keep searching left
        } else if (arr[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}

// Find last occurrence of target (rightmost position)
// Time: O(log n)   Space: O(1)
int lastOccurrence(const vector<int>& arr, int target) {
    int lo = 0, hi = static_cast<int>(arr.size()) - 1;
    int result = -1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) {
            result = mid;
            lo = mid + 1;  // keep searching right
        } else if (arr[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}

// Count occurrences of target in sorted array
// Time: O(log n)   Space: O(1)
int countOccurrences(const vector<int>& arr, int target) {
    int first = firstOccurrence(arr, target);
    if (first == -1) return 0;
    return lastOccurrence(arr, target) - first + 1;
}

// =============================================================================
// 3. SEARCH IN ROTATED SORTED ARRAY
// =============================================================================
// Array was sorted then rotated (e.g., [4,5,6,7,0,1,2]).
// All elements are distinct.
// Time: O(log n)   Space: O(1)
int searchRotated(const vector<int>& arr, int target) {
    int lo = 0, hi = static_cast<int>(arr.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) return mid;

        // Determine which half is sorted
        if (arr[lo] <= arr[mid]) {
            // Left half is sorted
            if (arr[lo] <= target && target < arr[mid]) {
                hi = mid - 1;
            } else {
                lo = mid + 1;
            }
        } else {
            // Right half is sorted
            if (arr[mid] < target && target <= arr[hi]) {
                lo = mid + 1;
            } else {
                hi = mid - 1;
            }
        }
    }
    return -1;
}

// =============================================================================
// 4. BINARY SEARCH ON ANSWER
// =============================================================================

// --- 4a. Integer Square Root ---
// Find floor(sqrt(n))
// Time: O(log n)   Space: O(1)
long long intSqrt(long long n) {
    if (n < 0) return -1;  // error
    long long lo = 0, hi = n;
    long long result = 0;
    while (lo <= hi) {
        long long mid = lo + (hi - lo) / 2;
        if (mid <= n / mid) {  // mid*mid <= n, but avoids overflow
            result = mid;
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return result;
}

// --- 4b. Koko Eating Bananas ---
// Koko has piles of bananas. She can eat at speed k bananas/hour.
// Each hour, she picks a pile and eats min(pile, k) bananas.
// Find minimum k such that she finishes all piles within h hours.
// Time: O(n * log(max_pile))   Space: O(1)
long long hoursToEat(const vector<int>& piles, int speed) {
    long long hours = 0;
    for (int pile : piles) {
        hours += (pile + speed - 1) / speed;  // ceil division
    }
    return hours;
}

int minEatingSpeed(const vector<int>& piles, int h) {
    int lo = 1;
    int hi = *max_element(piles.begin(), piles.end());
    int result = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (hoursToEat(piles, mid) <= h) {
            result = mid;
            hi = mid - 1;  // try smaller speed
        } else {
            lo = mid + 1;
        }
    }
    return result;
}

// --- 4c. Ship Packages Within D Days ---
// weights[i] = weight of i-th package. Must ship in order.
// Find minimum ship capacity to ship all within D days.
// Time: O(n * log(sum_weights))   Space: O(1)
int daysNeeded(const vector<int>& weights, int capacity) {
    int days = 1;
    int currentLoad = 0;
    for (int w : weights) {
        if (currentLoad + w > capacity) {
            ++days;
            currentLoad = 0;
        }
        currentLoad += w;
    }
    return days;
}

int shipWithinDays(const vector<int>& weights, int D) {
    int lo = *max_element(weights.begin(), weights.end());
    int hi = accumulate(weights.begin(), weights.end(), 0);
    int result = hi;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (daysNeeded(weights, mid) <= D) {
            result = mid;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    return result;
}

// =============================================================================
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 8: Searching (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Binary Search ---
    cout << "\n--- 1. Binary Search ---" << endl;
    {
        vector<int> arr = {1, 3, 5, 7, 9, 11, 13, 15};
        for (int target : {7, 1, 15, 6}) {
            int idxI = binarySearchIterative(arr, target);
            int idxR = binarySearchRecursive(arr, target);
            cout << "Search " << target << ": iterative=" << idxI
                 << ", recursive=" << idxR << endl;
        }
    }

    // --- 2. First/Last Occurrence ---
    cout << "\n--- 2. First/Last Occurrence ---" << endl;
    {
        vector<int> arr = {1, 2, 2, 2, 3, 4, 4, 5};
        for (int target : {2, 4, 3, 6}) {
            cout << "Target " << target << ": first=" << firstOccurrence(arr, target)
                 << ", last=" << lastOccurrence(arr, target)
                 << ", count=" << countOccurrences(arr, target) << endl;
        }
    }

    // --- 3. Search in Rotated Array ---
    cout << "\n--- 3. Search in Rotated Sorted Array ---" << endl;
    {
        vector<int> arr = {4, 5, 6, 7, 0, 1, 2};
        for (int target : {0, 3, 6, 4, 2}) {
            cout << "Search " << target << " in [4,5,6,7,0,1,2]: index="
                 << searchRotated(arr, target) << endl;
        }
    }

    // --- 4a. Integer Square Root ---
    cout << "\n--- 4a. Integer Square Root ---" << endl;
    for (long long n : {0LL, 1LL, 4LL, 8LL, 16LL, 100LL, 2147483647LL}) {
        cout << "sqrt(" << n << ") = " << intSqrt(n) << endl;
    }

    // --- 4b. Koko Eating Bananas ---
    cout << "\n--- 4b. Koko Eating Bananas ---" << endl;
    {
        vector<int> piles1 = {3, 6, 7, 11};
        cout << "Piles [3,6,7,11], h=8: k=" << minEatingSpeed(piles1, 8)
             << " (expected 4)" << endl;

        vector<int> piles2 = {30, 11, 23, 4, 20};
        cout << "Piles [30,11,23,4,20], h=5: k=" << minEatingSpeed(piles2, 5)
             << " (expected 30)" << endl;

        cout << "Piles [30,11,23,4,20], h=6: k=" << minEatingSpeed(piles2, 6)
             << " (expected 23)" << endl;
    }

    // --- 4c. Ship Packages ---
    cout << "\n--- 4c. Ship Packages Within D Days ---" << endl;
    {
        vector<int> weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
        cout << "Weights [1..10], D=5: capacity=" << shipWithinDays(weights, 5)
             << " (expected 15)" << endl;

        vector<int> weights2 = {3, 2, 2, 4, 1, 4};
        cout << "Weights [3,2,2,4,1,4], D=3: capacity=" << shipWithinDays(weights2, 3)
             << " (expected 6)" << endl;
    }

    cout << "\n========================================" << endl;
    cout << " All Week 8 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
