/*
 * WEEK 6 - C++ DSA
 * Topic: Return Array Sum
 * File: 1.return_array_sum.cpp
 *
 * CONCEPT:
 *     Compute the sum of all elements in an int vector.
 *
 * KEY POINTS:
 *     - Use std::vector<int> instead of raw int[] for safety/length.
 *     - The STL provides std::accumulate (header <numeric>) for the
 *       same job.
 *     - Recursive variant illustrates call-stack cost.
 *
 * ALGORITHM / APPROACH:
 *     Iterative:
 *         long long total = 0;
 *         for (int v : arr) total += v;
 *         return total;
 *
 * C++-SPECIFIC NOTES:
 *     - Range-based for ('for (int v : arr)') is the modern idiom.
 *     - Accumulate into long long to avoid overflow on huge inputs.
 *     - std::accumulate(arr.begin(), arr.end(), 0LL) is the STL form.
 *
 * DRY RUN:
 *     arr = {1,2,3,4,5}    -> 1,3,6,10,15
 *     arr = {-1,0,5,-3,10} -> -1,-1,4,1,11
 *     arr = {}             -> 0
 *
 * COMPLEXITY:
 *     Iterative : O(n) time, O(1) extra space
 *     Recursive : O(n) time, O(n) stack
 */

#include <iostream>
#include <vector>
#include <numeric>

long long sumArray(const std::vector<int>& arr) {
    long long total = 0;
    for (int v : arr) total += v;
    return total;
}

long long sumArrayRecursive(const std::vector<int>& arr, std::size_t i = 0) {
    if (i == arr.size()) return 0;
    return static_cast<long long>(arr[i]) + sumArrayRecursive(arr, i + 1);
}

void print(const std::vector<int>& arr) {
    std::cout << "[";
    for (std::size_t i = 0; i < arr.size(); ++i) {
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    }
    std::cout << "]";
}

int main() {
    std::vector<int> test1 = {1, 2, 3, 4, 5};
    std::cout << "Array: "; print(test1); std::cout << "\n";
    std::cout << "Sum (iterative): " << sumArray(test1) << "\n";
    std::cout << "Sum (recursive): " << sumArrayRecursive(test1) << "\n";
    std::cout << "Sum (STL):       "
              << std::accumulate(test1.begin(), test1.end(), 0LL) << "\n";

    std::vector<int> test2 = {-1, 0, 5, -3, 10};
    std::cout << "\nArray: "; print(test2); std::cout << "\n";
    std::cout << "Sum: " << sumArray(test2) << "\n";

    std::vector<int> test3;
    std::cout << "\nEmpty array sum: " << sumArray(test3) << "\n";

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::vector replaces the heap-allocated int[]; size lives with the data.
 *     - std::accumulate (header <numeric>) is the STL one-liner.
 *     - Use 'long long' or an explicit accumulator type to dodge overflow.
 *     - Pass containers by const reference to avoid copies.
 */
