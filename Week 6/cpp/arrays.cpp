/*
 * =============================================================================
 * Week 6 - Arrays (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Reverse array (two-pointer)
 *   2. Rotate array (reversal algorithm)
 *   3. Prefix sum + range query
 *   4. Kadane's algorithm (maximum subarray sum)
 *   5. Dutch National Flag (3-way partition)
 *   6. Missing number (sum method + XOR method)
 *   7. Find duplicate (Floyd's tortoise and hare)
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// 1. REVERSE ARRAY (Two-Pointer)
// =============================================================================
// Time: O(n)   Space: O(1)
void reverseArray(vector<int>& arr, int left, int right) {
    while (left < right) {
        swap(arr[left++], arr[right--]);
    }
}

void reverseArray(vector<int>& arr) {
    reverseArray(arr, 0, static_cast<int>(arr.size()) - 1);
}

// =============================================================================
// 2. ROTATE ARRAY (Reversal Algorithm)
// =============================================================================
// Rotate array right by k positions
// Time: O(n)   Space: O(1) — three reverses, each O(n)
// Example: [1,2,3,4,5] rotated right by 2 => [4,5,1,2,3]
void rotateRight(vector<int>& arr, int k) {
    int n = arr.size();
    if (n == 0) return;
    k = ((k % n) + n) % n;  // handle negative and k > n
    // Step 1: reverse entire array
    reverseArray(arr, 0, n - 1);
    // Step 2: reverse first k elements
    reverseArray(arr, 0, k - 1);
    // Step 3: reverse remaining elements
    reverseArray(arr, k, n - 1);
}

// Rotate left by k positions
// Time: O(n)   Space: O(1)
void rotateLeft(vector<int>& arr, int k) {
    int n = arr.size();
    if (n == 0) return;
    k = ((k % n) + n) % n;
    rotateRight(arr, n - k);
}

// =============================================================================
// 3. PREFIX SUM + RANGE QUERY
// =============================================================================

// Build prefix sum array
// Time: O(n)   Space: O(n)
// prefix[i] = arr[0] + arr[1] + ... + arr[i-1]
// prefix[0] = 0 (sentinel)
vector<long long> buildPrefixSum(const vector<int>& arr) {
    int n = arr.size();
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; ++i) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    return prefix;
}

// Range sum query [l, r] inclusive (0-indexed)
// Time: O(1) per query after O(n) preprocessing
long long rangeSum(const vector<long long>& prefix, int l, int r) {
    return prefix[r + 1] - prefix[l];
}

// =============================================================================
// 4. KADANE'S ALGORITHM (Maximum Subarray Sum)
// =============================================================================
// Time: O(n)   Space: O(1)
// Returns {maxSum, startIndex, endIndex} using structured bindings
tuple<long long, int, int> kadane(const vector<int>& arr) {
    long long maxSum = arr[0];
    long long currentSum = arr[0];
    int start = 0, end = 0, tempStart = 0;

    for (int i = 1; i < static_cast<int>(arr.size()); ++i) {
        if (currentSum + arr[i] < arr[i]) {
            currentSum = arr[i];
            tempStart = i;
        } else {
            currentSum += arr[i];
        }
        if (currentSum > maxSum) {
            maxSum = currentSum;
            start = tempStart;
            end = i;
        }
    }
    return {maxSum, start, end};
}

// =============================================================================
// 5. DUTCH NATIONAL FLAG (3-Way Partition)
// =============================================================================
// Sort array of 0s, 1s, and 2s in a single pass
// Time: O(n)   Space: O(1)
// Uses three pointers: low, mid, high
void dutchNationalFlag(vector<int>& arr) {
    int low = 0, mid = 0, high = static_cast<int>(arr.size()) - 1;
    while (mid <= high) {
        if (arr[mid] == 0) {
            swap(arr[low++], arr[mid++]);
        } else if (arr[mid] == 1) {
            ++mid;
        } else {  // arr[mid] == 2
            swap(arr[mid], arr[high--]);
        }
    }
}

// =============================================================================
// 6. MISSING NUMBER
// =============================================================================

// Sum method: array has n numbers from 0..n with one missing
// Time: O(n)   Space: O(1)
int missingNumberSum(const vector<int>& nums) {
    int n = nums.size();
    long long expectedSum = static_cast<long long>(n) * (n + 1) / 2;
    long long actualSum = 0;
    for (int x : nums) actualSum += x;
    return static_cast<int>(expectedSum - actualSum);
}

// XOR method: XOR of 0..n XOR all elements leaves the missing number
// Time: O(n)   Space: O(1)
int missingNumberXOR(const vector<int>& nums) {
    int n = nums.size();
    int xorAll = 0;
    for (int i = 0; i <= n; ++i) xorAll ^= i;
    for (int x : nums) xorAll ^= x;
    return xorAll;
}

// =============================================================================
// 7. FIND DUPLICATE (Floyd's Cycle Detection)
// =============================================================================
// Array has n+1 integers in range [1, n], exactly one duplicate.
// Treat array as a linked list: index -> arr[index].
// Time: O(n)   Space: O(1)
int findDuplicate(const vector<int>& nums) {
    // Phase 1: detect cycle (tortoise and hare)
    int slow = nums[0];
    int fast = nums[0];
    do {
        slow = nums[slow];
        fast = nums[nums[fast]];
    } while (slow != fast);

    // Phase 2: find entrance to cycle (= duplicate value)
    slow = nums[0];
    while (slow != fast) {
        slow = nums[slow];
        fast = nums[fast];
    }
    return slow;
}

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
// MAIN — Test Cases
// =============================================================================
int main() {
    cout << "========================================" << endl;
    cout << " Week 6: Arrays (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Reverse Array ---
    cout << "\n--- 1. Reverse Array ---" << endl;
    {
        vector<int> arr = {1, 2, 3, 4, 5};
        printVec(arr, "Before");
        reverseArray(arr);
        printVec(arr, "After ");
    }

    // --- 2. Rotate Array ---
    cout << "\n--- 2. Rotate Array ---" << endl;
    {
        vector<int> arr = {1, 2, 3, 4, 5, 6, 7};
        printVec(arr, "Original   ");
        rotateRight(arr, 3);
        printVec(arr, "Right by 3 ");

        vector<int> arr2 = {1, 2, 3, 4, 5, 6, 7};
        rotateLeft(arr2, 2);
        printVec(arr2, "Left by 2  ");
    }

    // --- 3. Prefix Sum ---
    cout << "\n--- 3. Prefix Sum + Range Query ---" << endl;
    {
        vector<int> arr = {3, 1, 4, 1, 5, 9, 2, 6};
        auto prefix = buildPrefixSum(arr);
        printVec(arr, "Array");
        cout << "Sum [0,3] = " << rangeSum(prefix, 0, 3) << " (expected 9)" << endl;
        cout << "Sum [2,5] = " << rangeSum(prefix, 2, 5) << " (expected 19)" << endl;
        cout << "Sum [0,7] = " << rangeSum(prefix, 0, 7) << " (expected 31)" << endl;
    }

    // --- 4. Kadane's Algorithm ---
    cout << "\n--- 4. Kadane's Algorithm ---" << endl;
    {
        vector<int> arr = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        auto [maxSum, start, end] = kadane(arr);  // C++17 structured binding
        printVec(arr, "Array");
        cout << "Max subarray sum = " << maxSum
             << " (indices " << start << " to " << end << ")" << endl;

        vector<int> arr2 = {-1, -2, -3, -4};
        auto [maxSum2, s2, e2] = kadane(arr2);
        cout << "All negative: max = " << maxSum2 << endl;
    }

    // --- 5. Dutch National Flag ---
    cout << "\n--- 5. Dutch National Flag ---" << endl;
    {
        vector<int> arr = {2, 0, 1, 2, 1, 0, 0, 2, 1};
        printVec(arr, "Before");
        dutchNationalFlag(arr);
        printVec(arr, "After ");
    }

    // --- 6. Missing Number ---
    cout << "\n--- 6. Missing Number ---" << endl;
    {
        vector<int> nums = {3, 0, 1};  // missing 2
        cout << "Array: [3,0,1] -> Missing (sum): " << missingNumberSum(nums)
             << ", Missing (XOR): " << missingNumberXOR(nums) << endl;

        vector<int> nums2 = {0, 1, 2, 3, 5, 6, 7, 8, 9};  // missing 4
        cout << "Array: [0..9 sans 4] -> Missing (sum): " << missingNumberSum(nums2)
             << ", Missing (XOR): " << missingNumberXOR(nums2) << endl;
    }

    // --- 7. Find Duplicate ---
    cout << "\n--- 7. Find Duplicate (Floyd's) ---" << endl;
    {
        vector<int> nums = {1, 3, 4, 2, 2};
        cout << "Array: [1,3,4,2,2] -> Duplicate = " << findDuplicate(nums) << endl;

        vector<int> nums2 = {3, 1, 3, 4, 2};
        cout << "Array: [3,1,3,4,2] -> Duplicate = " << findDuplicate(nums2) << endl;
    }

    cout << "\n========================================" << endl;
    cout << " All Week 6 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
