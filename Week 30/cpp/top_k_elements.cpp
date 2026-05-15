/*
 * WEEK 30 - C++ ADVANCED TOPICS
 * Topic: Top-K Elements Pattern
 * File: top_k_elements.cpp
 *
 * CONCEPT:
 *   "Find the K largest / smallest / most-frequent" boils down to:
 *     - Min-heap of size K (keeps largest): O(n log K).
 *     - Bucket sort by frequency: O(n) when frequencies are bounded.
 *     - Quickselect: O(n) expected.
 *
 * KEY POINTS:
 *   - std::priority_queue is a max-heap; for the min-heap variant pass
 *     greater<int> as the comparator.
 *   - For top-K frequent integer elements, bucket sort is asymptotically
 *     optimal.
 *
 * ALGORITHM / APPROACH:
 *   KTH LARGEST (heap): push, if size > K pop. Top of min-heap is answer.
 *   TOP K FREQ (heap):  same trick on (count, value).
 *   TOP K FREQ (bucket): freq -> bucket[freq].push(value); collect from
 *                        highest bucket downward.
 *   QUICKSELECT:        Hoare partition; recurse into the side containing K.
 *
 * C++-SPECIFIC NOTES:
 *   - priority_queue<int, vector<int>, greater<int>> is a min-heap.
 *
 * DRY RUN / EXAMPLE:
 *   findKthLargest [3,2,1,5,6,4], k=2 -> 5.
 *   topKFrequent  [1,1,1,2,2,3], k=2 -> {1, 2}.
 *
 * COMPLEXITY:
 *   Heap O(n log K); Bucket O(n); Quickselect O(n) expected.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
#include <random>
#include <functional>

using namespace std;

int findKthLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> heap;
    for (int x : nums) {
        heap.push(x);
        if ((int)heap.size() > k) heap.pop();
    }
    return heap.top();
}

vector<int> topKFrequent(vector<int>& nums, int k) {
    unordered_map<int,int> freq;
    for (int x : nums) ++freq[x];
    using P = pair<int,int>; // (count, value)
    priority_queue<P, vector<P>, greater<P>> heap;
    for (auto& kv : freq) {
        heap.emplace(kv.second, kv.first);
        if ((int)heap.size() > k) heap.pop();
    }
    vector<int> out;
    while (!heap.empty()) { out.push_back(heap.top().second); heap.pop(); }
    return out;
}

vector<int> topKFrequentBucket(vector<int>& nums, int k) {
    unordered_map<int,int> freq;
    for (int x : nums) ++freq[x];
    vector<vector<int>> buckets((int)nums.size() + 1);
    for (auto& kv : freq) buckets[kv.second].push_back(kv.first);
    vector<int> out;
    for (int i = (int)buckets.size() - 1; i >= 0 && (int)out.size() < k; --i)
        for (int v : buckets[i]) {
            out.push_back(v);
            if ((int)out.size() == k) break;
        }
    return out;
}

int quickselectKthLargest(vector<int> nums, int k) {
    int target = (int)nums.size() - k;
    static mt19937 rng(42);
    function<int(int,int)> partition = [&](int lo, int hi) {
        int pivot = nums[lo + rng() % (hi - lo + 1)];
        int i = lo, j = hi;
        while (i <= j) {
            while (nums[i] < pivot) ++i;
            while (nums[j] > pivot) --j;
            if (i <= j) { swap(nums[i], nums[j]); ++i; --j; }
        }
        return i;
    };
    int lo = 0, hi = (int)nums.size() - 1;
    while (lo < hi) {
        int idx = partition(lo, hi);
        if (idx <= target) lo = idx; else hi = idx - 1;
    }
    return nums[target];
}

int main() {
    vector<int> a = {3,2,1,5,6,4};
    cout << "Kth largest k=2: " << findKthLargest(a, 2) << "\n";

    vector<int> b = {1,1,1,2,2,3};
    cout << "Top 2 frequent (heap):  ";
    for (int x : topKFrequent(b, 2)) cout << x << " ";
    cout << "\nTop 2 frequent (bucket):";
    for (int x : topKFrequentBucket(b, 2)) cout << " " << x;
    cout << "\n";

    cout << "Quickselect kth=2: " << quickselectKthLargest({3,2,1,5,6,4}, 2) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - priority_queue with greater<> for a min-heap.
 *   - Adds quickselect as a third top-K technique (Java had heap + bucket).
 */
