/*
 * =============================================================================
 * Week 15 — Heaps & Priority Queues  (C++17)
 * =============================================================================
 *
 * Topics covered
 * --------------
 *   1. MaxHeap class  (insert, extract_max, heapify/sift_down, build_heap)
 *   2. Heap sort (in-place)
 *   3. Kth largest element using a min-heap of size k
 *   4. Merge k sorted arrays using priority_queue
 *   5. MedianFinder  (two-heap technique: max-heap + min-heap)
 *
 * Complexity cheat-sheet
 * ----------------------
 *   MaxHeap::insert         O(log n)
 *   MaxHeap::extract_max    O(log n)
 *   MaxHeap::build_heap     O(n)          — bottom-up heapify
 *   heap_sort               O(n log n)    — in-place, not stable
 *   kth_largest             O(n log k)    — maintains min-heap of size k
 *   merge_k_sorted          O(N log k)    — N = total elements, k = arrays
 *   MedianFinder::add       O(log n)
 *   MedianFinder::median    O(1)
 *
 * Build & run
 *   g++ -std=c++17 -O2 -o heaps heaps.cpp && ./heaps
 * =============================================================================
 */

#include <iostream>
#include <vector>
#include <queue>
#include <functional>
#include <algorithm>
#include <cassert>
#include <optional>
#include <numeric>
#include <sstream>

// ---------------------------------------------------------------------------
// 1. MaxHeap class — manual implementation backed by std::vector
// ---------------------------------------------------------------------------
class MaxHeap {
public:
    MaxHeap() = default;

    // Build a heap from an arbitrary vector in O(n).
    explicit MaxHeap(std::vector<int> data) : heap_(std::move(data)) {
        build_heap();
    }

    // Insert a value — O(log n).
    void insert(int val) {
        heap_.push_back(val);
        sift_up(static_cast<int>(heap_.size()) - 1);
    }

    // Remove and return the maximum — O(log n).
    // Returns std::nullopt when empty.
    [[nodiscard]] std::optional<int> extract_max() {
        if (heap_.empty()) return std::nullopt;
        int max_val = heap_.front();
        heap_.front() = heap_.back();
        heap_.pop_back();
        if (!heap_.empty()) sift_down(0);
        return max_val;
    }

    // Peek at the maximum — O(1).
    [[nodiscard]] std::optional<int> peek() const {
        if (heap_.empty()) return std::nullopt;
        return heap_.front();
    }

    [[nodiscard]] std::size_t size() const { return heap_.size(); }
    [[nodiscard]] bool empty() const { return heap_.empty(); }

    // Expose internal array (useful for heap-sort).
    [[nodiscard]] const std::vector<int>& data() const { return heap_; }

private:
    std::vector<int> heap_;

    static int parent(int i)      { return (i - 1) / 2; }
    static int left_child(int i)  { return 2 * i + 1; }
    static int right_child(int i) { return 2 * i + 2; }

    // Sift an element UP to restore heap property — used after insert.
    void sift_up(int i) {
        while (i > 0 && heap_[parent(i)] < heap_[i]) {
            std::swap(heap_[parent(i)], heap_[i]);
            i = parent(i);
        }
    }

    // Sift an element DOWN (a.k.a. heapify) — used after extract_max.
    void sift_down(int i) {
        int n = static_cast<int>(heap_.size());
        while (true) {
            int largest = i;
            int l = left_child(i), r = right_child(i);
            if (l < n && heap_[l] > heap_[largest]) largest = l;
            if (r < n && heap_[r] > heap_[largest]) largest = r;
            if (largest == i) break;
            std::swap(heap_[i], heap_[largest]);
            i = largest;
        }
    }

    // Build heap from unordered array — O(n) bottom-up.
    void build_heap() {
        for (int i = static_cast<int>(heap_.size()) / 2 - 1; i >= 0; --i) {
            sift_down(i);
        }
    }
};

// ---------------------------------------------------------------------------
// 2. Heap Sort — in-place, O(n log n) time, O(1) extra space
// ---------------------------------------------------------------------------
// Complexity:  Time  O(n log n)   |   Space O(1)   |   Not stable
void heap_sort(std::vector<int>& arr) {
    int n = static_cast<int>(arr.size());

    // Build a max-heap (bottom-up).
    auto sift_down = [&](int i, int size) {
        while (true) {
            int largest = i;
            int l = 2 * i + 1, r = 2 * i + 2;
            if (l < size && arr[l] > arr[largest]) largest = l;
            if (r < size && arr[r] > arr[largest]) largest = r;
            if (largest == i) break;
            std::swap(arr[i], arr[largest]);
            i = largest;
        }
    };

    for (int i = n / 2 - 1; i >= 0; --i) sift_down(i, n);

    // Repeatedly extract max and place at end.
    for (int i = n - 1; i > 0; --i) {
        std::swap(arr[0], arr[i]);
        sift_down(0, i);
    }
}

// ---------------------------------------------------------------------------
// 3. Kth Largest Element — min-heap of size k
// ---------------------------------------------------------------------------
// Complexity:  Time  O(n log k)   |   Space O(k)
int kth_largest(const std::vector<int>& nums, int k) {
    // Min-heap: the top is always the kth-largest seen so far.
    std::priority_queue<int, std::vector<int>, std::greater<>> min_heap;

    for (int num : nums) {
        min_heap.push(num);
        if (static_cast<int>(min_heap.size()) > k) {
            min_heap.pop();          // evict the smallest — keep k largest
        }
    }
    return min_heap.top();           // smallest among the k largest = kth largest
}

// ---------------------------------------------------------------------------
// 4. Merge k Sorted Arrays — priority_queue with (value, array_idx, elem_idx)
// ---------------------------------------------------------------------------
// Complexity:  Time  O(N log k)   |   Space O(N + k)
//              N = total number of elements across all arrays
std::vector<int> merge_k_sorted(const std::vector<std::vector<int>>& arrays) {
    struct Entry {
        int val;
        int arr_idx;
        int elem_idx;
        bool operator>(const Entry& o) const { return val > o.val; }
    };

    std::priority_queue<Entry, std::vector<Entry>, std::greater<>> pq;

    // Seed with the first element of each non-empty array.
    for (int i = 0; i < static_cast<int>(arrays.size()); ++i) {
        if (!arrays[i].empty()) {
            pq.push({arrays[i][0], i, 0});
        }
    }

    std::vector<int> result;
    while (!pq.empty()) {
        auto [val, ai, ei] = pq.top();
        pq.pop();
        result.push_back(val);
        if (ei + 1 < static_cast<int>(arrays[ai].size())) {
            pq.push({arrays[ai][ei + 1], ai, ei + 1});
        }
    }
    return result;
}

// ---------------------------------------------------------------------------
// 5. MedianFinder — two-heap technique
// ---------------------------------------------------------------------------
// Invariant:  max_heap holds the smaller half, min_heap holds the larger half.
//             |max_heap.size() - min_heap.size()| <= 1
// Complexity: add O(log n)   |   median O(1)
class MedianFinder {
public:
    void add(int num) {
        // Always push to max_heap first, then balance.
        lo_.push(num);

        // Ensure every element in lo_ <= every element in hi_.
        hi_.push(lo_.top());
        lo_.pop();

        // Keep sizes balanced: lo_ may have at most one extra element.
        if (hi_.size() > lo_.size()) {
            lo_.push(hi_.top());
            hi_.pop();
        }
    }

    [[nodiscard]] double median() const {
        if (lo_.size() > hi_.size()) {
            return static_cast<double>(lo_.top());
        }
        return (lo_.top() + hi_.top()) / 2.0;
    }

private:
    std::priority_queue<int>                                   lo_;  // max-heap (smaller half)
    std::priority_queue<int, std::vector<int>, std::greater<>> hi_;  // min-heap (larger half)
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
template <typename T>
std::string vec_to_string(const std::vector<T>& v) {
    std::ostringstream oss;
    oss << "[";
    for (std::size_t i = 0; i < v.size(); ++i) {
        if (i) oss << ", ";
        oss << v[i];
    }
    oss << "]";
    return oss.str();
}

// ---------------------------------------------------------------------------
// main — test cases
// ---------------------------------------------------------------------------
int main() {
    std::cout << "=== Week 15: Heaps & Priority Queues ===\n\n";

    // ---- 1. MaxHeap ----
    {
        std::cout << "-- MaxHeap --\n";
        MaxHeap h;
        for (int x : {3, 1, 6, 5, 2, 4}) h.insert(x);
        assert(h.peek() == 6);
        std::cout << "  peek after inserting {3,1,6,5,2,4}: " << *h.peek() << "\n";

        auto m = h.extract_max();
        assert(m == 6);
        std::cout << "  extract_max: " << *m << "  new peek: " << *h.peek() << "\n";

        // Build heap from vector.
        MaxHeap h2({10, 20, 5, 7, 15});
        assert(h2.peek() == 20);
        std::cout << "  build_heap({10,20,5,7,15}) peek: " << *h2.peek() << "\n\n";
    }

    // ---- 2. Heap Sort ----
    {
        std::cout << "-- Heap Sort --\n";
        std::vector<int> arr = {12, 11, 13, 5, 6, 7};
        std::cout << "  before: " << vec_to_string(arr) << "\n";
        heap_sort(arr);
        std::cout << "  after:  " << vec_to_string(arr) << "\n";
        assert(std::is_sorted(arr.begin(), arr.end()));
        std::cout << "  (sorted correctly)\n\n";
    }

    // ---- 3. Kth Largest ----
    {
        std::cout << "-- Kth Largest --\n";
        std::vector<int> nums = {3, 2, 1, 5, 6, 4};
        int k = 2;
        int ans = kth_largest(nums, k);
        assert(ans == 5);
        std::cout << "  nums=" << vec_to_string(nums) << "  k=" << k << "  => " << ans << "\n\n";
    }

    // ---- 4. Merge k Sorted Arrays ----
    {
        std::cout << "-- Merge k Sorted Arrays --\n";
        std::vector<std::vector<int>> arrays = {
            {1, 4, 7},
            {2, 5, 8},
            {3, 6, 9}
        };
        auto merged = merge_k_sorted(arrays);
        std::cout << "  merged: " << vec_to_string(merged) << "\n";
        assert(std::is_sorted(merged.begin(), merged.end()));
        assert(merged.size() == 9);
        std::cout << "  (correct)\n\n";
    }

    // ---- 5. MedianFinder ----
    {
        std::cout << "-- MedianFinder --\n";
        MedianFinder mf;
        mf.add(1);
        std::cout << "  add(1)  median=" << mf.median() << "\n";
        assert(mf.median() == 1.0);

        mf.add(2);
        std::cout << "  add(2)  median=" << mf.median() << "\n";
        assert(mf.median() == 1.5);

        mf.add(3);
        std::cout << "  add(3)  median=" << mf.median() << "\n";
        assert(mf.median() == 2.0);

        mf.add(4);
        std::cout << "  add(4)  median=" << mf.median() << "\n";
        assert(mf.median() == 2.5);

        mf.add(5);
        std::cout << "  add(5)  median=" << mf.median() << "\n";
        assert(mf.median() == 3.0);
    }

    std::cout << "\nAll Week 15 tests passed.\n";
    return 0;
}
