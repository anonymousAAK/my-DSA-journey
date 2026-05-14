/*
 * WEEK 6 - C++ DSA
 * Topic: Dutch National Flag + Missing / Duplicate
 * File: 5.dutch_national_flag_and_missing.cpp
 *
 * CONCEPT:
 *     A) Dutch National Flag — sort {0,1,2} array in O(n), single pass.
 *     B) Missing number in [0..n] — using sum formula or XOR.
 *     C) Find the duplicate in a [1..n] array of size n+1 — Floyd's
 *        cycle detection on the array-as-functional-graph.
 *
 * KEY POINTS:
 *     - Dutch flag uses three pointers (low, mid, high) and is in-place.
 *     - Sum/XOR for missing both run in O(n) with O(1) extra space.
 *     - Floyd's (tortoise & hare) needs no extra memory — perfect when
 *       modifying the input is forbidden.
 *
 * ALGORITHM / APPROACH:
 *     Dutch flag — see code: classify arr[mid] as 0 / 1 / 2.
 *     Missing (sum) : expected = n*(n+1)/2; return expected - sum(arr).
 *     Missing (XOR) : XOR all of [0..n] with all values; survivors cancel.
 *     Duplicate     : two-phase Floyd as in linked-list cycle detection.
 *
 * C++-SPECIFIC NOTES:
 *     - std::swap for in-place swaps.
 *     - Use long long when summing large arrays to dodge overflow.
 *     - std::accumulate sums a range in one call.
 *
 * DRY RUN:
 *     Dutch on [2,0,2,1,1,0]:
 *         lo=0 mid=0 hi=5
 *         arr[0]=2 -> swap(0,5), hi=4: [0,0,2,1,1,2]
 *         arr[0]=0 -> swap(0,0), lo=1 mid=1
 *         arr[1]=0 -> swap(1,1), lo=2 mid=2
 *         arr[2]=2 -> swap(2,4), hi=3: [0,0,1,1,2,2]
 *         arr[2]=1 -> mid=3
 *         arr[3]=1 -> mid=4 stop
 *
 *     Missing on [3,0,1] (n=3): 6 - 4 = 2.
 *
 *     Duplicate on [1,3,4,2,2]: Floyd converges on 2.
 *
 * COMPLEXITY:
 *     All operations: O(n) time, O(1) extra space.
 */

#include <iostream>
#include <vector>
#include <numeric>
#include <utility>

void dutchFlag(std::vector<int>& arr) {
    int low = 0, mid = 0, high = static_cast<int>(arr.size()) - 1;
    while (mid <= high) {
        if (arr[mid] == 0) {
            std::swap(arr[low], arr[mid]);
            ++low; ++mid;
        } else if (arr[mid] == 1) {
            ++mid;
        } else { // 2
            std::swap(arr[mid], arr[high]);
            --high;
        }
    }
}

int missingNumberSum(const std::vector<int>& arr) {
    long long n = static_cast<long long>(arr.size());
    long long expected = n * (n + 1) / 2;
    long long actual = std::accumulate(arr.begin(), arr.end(), 0LL);
    return static_cast<int>(expected - actual);
}

int missingNumberXOR(const std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());
    int x = 0;
    for (int i = 0; i <= n; ++i) x ^= i;
    for (int v : arr) x ^= v;
    return x;
}

int findDuplicate(const std::vector<int>& arr) {
    // Phase 1: find an intersection inside the cycle.
    int slow = arr[0];
    int fast = arr[0];
    do {
        slow = arr[slow];
        fast = arr[arr[fast]];
    } while (slow != fast);
    // Phase 2: find the cycle entry — that is the duplicate.
    slow = arr[0];
    while (slow != fast) {
        slow = arr[slow];
        fast = arr[fast];
    }
    return slow;
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i)
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    std::cout << "]";
}

int main() {
    std::vector<int> colors = {2, 0, 2, 1, 1, 0};
    std::cout << "Before: "; print(colors); std::cout << "\n";
    dutchFlag(colors);
    std::cout << "After:  "; print(colors); std::cout << "\n";

    std::vector<int> colors2 = {2, 2, 2, 0, 0, 1};
    dutchFlag(colors2);
    std::cout << "Sorted: "; print(colors2); std::cout << "\n";

    std::vector<int> arr1 = {3, 0, 1};
    std::cout << "\narr = "; print(arr1); std::cout << "\n";
    std::cout << "Missing (sum): " << missingNumberSum(arr1) << "\n";
    std::cout << "Missing (XOR): " << missingNumberXOR(arr1) << "\n";

    std::vector<int> arr2 = {9, 6, 4, 2, 3, 5, 7, 0, 1};
    std::cout << "\narr = "; print(arr2); std::cout << "\n";
    std::cout << "Missing (sum): " << missingNumberSum(arr2) << "\n";
    std::cout << "Missing (XOR): " << missingNumberXOR(arr2) << "\n";

    std::vector<int> dup = {1, 3, 4, 2, 2};
    std::cout << "\narr = "; print(dup); std::cout << "\n";
    std::cout << "Duplicate: " << findDuplicate(dup) << "\n";

    std::vector<int> dup2 = {3, 1, 3, 4, 2};
    std::cout << "arr = "; print(dup2); std::cout << "\n";
    std::cout << "Duplicate: " << findDuplicate(dup2) << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::swap and std::accumulate replace explicit temp-variable code.
 *     - Use long long when summing large arrays to be overflow-safe.
 *     - Floyd's algorithm reads the input but never mutates it, so it is
 *       suited for read-only inputs.
 */
