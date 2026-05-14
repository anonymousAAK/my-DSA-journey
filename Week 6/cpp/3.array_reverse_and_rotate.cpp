/*
 * WEEK 6 - C++ DSA
 * Topic: Array Reverse and Rotate
 * File: 3.array_reverse_and_rotate.cpp
 *
 * CONCEPT:
 *     1. Reverse a vector in place using two pointers.
 *     2. Left/right rotate by k via the reversal algorithm
 *        (3 sub-reversals; O(n) time, O(1) space).
 *
 * KEY POINTS:
 *     - Reduce k modulo n before rotating.
 *     - The reversal algorithm beats the naive O(n*k) shift.
 *
 * ALGORITHM / APPROACH:
 *     reverse(arr, l, r): swap(l,r), l++, r--, while l < r
 *     leftRotate(arr,k): k%=n;
 *         reverse(arr, 0, k-1)
 *         reverse(arr, k, n-1)
 *         reverse(arr, 0, n-1)
 *     rightRotate(arr,k) = leftRotate(arr, n - (k % n))
 *
 * C++-SPECIFIC NOTES:
 *     - std::reverse(first, last) (header <algorithm>) is the STL
 *       built-in; the manual version is included for instruction.
 *     - std::rotate(first, mid, last) implements left rotation in
 *       one call.
 *     - std::swap performs the swap idiomatically.
 *
 * DRY RUN:
 *     [1,2,3,4,5] reversed -> [5,4,3,2,1]
 *     [1,2,3,4,5] left rotate by 2:
 *         rev(0,1):  [2,1,3,4,5]
 *         rev(2,4):  [2,1,5,4,3]
 *         rev(0,4):  [3,4,5,1,2]
 *
 * COMPLEXITY:
 *     Reverse : O(n) time, O(1) space
 *     Rotate  : O(n) time, O(1) space
 */

#include <iostream>
#include <vector>
#include <algorithm>

void reverseRange(std::vector<int>& arr, int l, int r) {
    while (l < r) {
        std::swap(arr[l], arr[r]);
        ++l; --r;
    }
}

void reverseArray(std::vector<int>& arr) {
    if (!arr.empty()) reverseRange(arr, 0, static_cast<int>(arr.size()) - 1);
}

void leftRotate(std::vector<int>& arr, int k) {
    int n = static_cast<int>(arr.size());
    if (n == 0) return;
    k %= n;
    if (k == 0) return;
    reverseRange(arr, 0, k - 1);
    reverseRange(arr, k, n - 1);
    reverseRange(arr, 0, n - 1);
}

void rightRotate(std::vector<int>& arr, int k) {
    int n = static_cast<int>(arr.size());
    if (n == 0) return;
    leftRotate(arr, n - (k % n));
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    // Reverse
    std::vector<int> arr1 = {1, 2, 3, 4, 5};
    std::cout << "Original: "; print(arr1); std::cout << "\n";
    reverseArray(arr1);
    std::cout << "Reversed: "; print(arr1); std::cout << "\n";

    // Left rotate
    std::vector<int> arr2 = {1, 2, 3, 4, 5};
    std::cout << "\nOriginal:         "; print(arr2); std::cout << "\n";
    leftRotate(arr2, 2);
    std::cout << "Left Rotate by 2: "; print(arr2); std::cout << "\n";

    // Right rotate
    std::vector<int> arr3 = {1, 2, 3, 4, 5};
    std::cout << "\nOriginal:          "; print(arr3); std::cout << "\n";
    rightRotate(arr3, 2);
    std::cout << "Right Rotate by 2: "; print(arr3); std::cout << "\n";

    // Edge cases
    std::vector<int> single = {42};
    leftRotate(single, 5);
    std::cout << "\nSingle element rotated: "; print(single); std::cout << "\n";

    std::vector<int> empty;
    leftRotate(empty, 3);
    std::cout << "Empty array: "; print(empty); std::cout << "\n";

    // STL alternatives
    std::vector<int> alt = {1, 2, 3, 4, 5};
    std::rotate(alt.begin(), alt.begin() + 2, alt.end());
    std::cout << "\nstd::rotate left by 2: "; print(alt); std::cout << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::swap, std::reverse, std::rotate are STL freebies.
 *     - References (`std::vector<int>&`) cleanly express in-place mutation.
 *     - Be explicit about signed vs unsigned to avoid wrap-around when
 *       computing (right - left).
 */
