/*
 * WEEK 8 - C++ DSA
 * Topic: Binary Search on the Answer
 * File: 2.binary_search_on_answer.cpp
 *
 * CONCEPT:
 *     Binary search applied over an answer range rather than an array.
 *     Works whenever a monotonic predicate is available.
 *
 * KEY POINTS:
 *     - Template: lo..hi over plausible answers; while lo<hi: mid=...,
 *       if predicate(mid) hi=mid else lo=mid+1; return lo.
 *     - Examples here: integer sqrt, Koko bananas, ship-packages-in-D-days.
 *
 * ALGORITHM / APPROACH:
 *     See per-problem code; identical template each time.
 *
 * C++-SPECIFIC NOTES:
 *     - Use long long when intermediate products can exceed 2^31.
 *     - std::ranges::max / std::ranges::reduce (C++20+) shorten bounds.
 *     - We rely on <numeric> std::accumulate for the sum bound.
 *
 * DRY RUN:
 *     sqrt(17): converges to 4 (since 4*4=16<=17<25=5*5).
 *     Koko piles=[3,6,7,11] H=8 -> speed 4.
 *     Ship weights 1..10 D=5 -> capacity 15.
 *
 * COMPLEXITY:
 *     O(log(range) * predicate cost).
 */

#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>

int sqrtInt(int n) {
    if (n < 2) return n;
    int lo = 1, hi = n / 2;
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;
        long long sq = static_cast<long long>(mid) * mid;
        if (sq <= n) lo = mid;
        else         hi = mid - 1;
    }
    return lo;
}

bool canFinish(const std::vector<int>& piles, int h, int speed) {
    long long hours = 0;
    for (int p : piles) hours += (p + speed - 1) / speed;
    return hours <= h;
}

int minEatingSpeed(const std::vector<int>& piles, int h) {
    int lo = 1;
    int hi = *std::max_element(piles.begin(), piles.end());
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (canFinish(piles, h, mid)) hi = mid;
        else                          lo = mid + 1;
    }
    return lo;
}

bool canShip(const std::vector<int>& weights, int days, int capacity) {
    int currentLoad = 0, daysNeeded = 1;
    for (int w : weights) {
        if (w > capacity) return false;
        if (currentLoad + w > capacity) {
            ++daysNeeded;
            currentLoad = 0;
        }
        currentLoad += w;
    }
    return daysNeeded <= days;
}

int minShipCapacity(const std::vector<int>& weights, int days) {
    int lo = *std::max_element(weights.begin(), weights.end());
    int hi = std::accumulate(weights.begin(), weights.end(), 0);
    while (lo < hi) {
        int mid = lo + (hi - lo) / 2;
        if (canShip(weights, days, mid)) hi = mid;
        else                              lo = mid + 1;
    }
    return lo;
}

int main() {
    std::cout << "=== Integer Square Root ===\n";
    for (int n : {0, 1, 4, 8, 9, 16, 17, 100}) {
        std::cout << "sqrt(" << n << ") = " << sqrtInt(n) << "\n";
    }

    std::cout << "\n=== Koko Eating Bananas ===\n";
    std::vector<int> piles = {3, 6, 7, 11};
    std::cout << "Piles: [3,6,7,11]\n";
    std::cout << "Min speed for H=8: " << minEatingSpeed(piles, 8) << "\n";  // 4

    std::vector<int> piles2 = {30, 11, 23, 4, 20};
    std::cout << "Piles: [30,11,23,4,20]\n";
    std::cout << "Min speed for H=5: " << minEatingSpeed(piles2, 5) << "\n"; // 30
    std::cout << "Min speed for H=6: " << minEatingSpeed(piles2, 6) << "\n"; // 23

    std::cout << "\n=== Ship Packages ===\n";
    std::vector<int> weights = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    std::cout << "Weights: [1..10]\n";
    std::cout << "Min capacity for D=5 days:  " << minShipCapacity(weights, 5) << "\n";  // 15
    std::cout << "Min capacity for D=10 days: " << minShipCapacity(weights, 10) << "\n"; // 10

    return 0;
}

/*
 * NOTES — C++ vs Java:
 *     - std::max_element returns an iterator; deref with *.
 *     - long long defends against integer overflow in mid*mid.
 *     - std::accumulate is the STL sum.
 */
