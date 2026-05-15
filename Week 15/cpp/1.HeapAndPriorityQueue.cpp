/*
 * WEEK 15 - C++ DSA
 * Topic: Heap, Heap Sort, Priority Queue Applications
 * File: 1.HeapAndPriorityQueue.cpp
 *
 * CONCEPT:
 *   A heap is a complete binary tree stored as an array with the heap
 *   property (max-heap: parent >= children).
 *
 * KEY POINTS:
 *   - parent(i) = (i-1)/2; left = 2i+1; right = 2i+2.
 *   - insert: append + sift up. O(log n).
 *   - extract: swap root with last, shrink, sift down. O(log n).
 *   - buildHeap: O(n) — sift down from last non-leaf.
 *   - heap sort: O(n log n), in-place.
 *
 * ALGORITHM / APPROACH:
 *   Same as Java/Python files. C++ STL provides:
 *     - std::priority_queue<T> (max-heap by default).
 *     - std::make_heap, std::push_heap, std::pop_heap on iterators (closer
 *       to hand-rolled).
 *
 * C++-SPECIFIC NOTES:
 *   - To get a min-heap from std::priority_queue, specify the comparator:
 *       std::priority_queue<int, std::vector<int>, std::greater<int>>
 *   - std::make_heap is O(n); equivalent to our buildHeap.
 *
 * DRY RUN:
 *   Build max-heap on [5,3,7,1,9,2,8]: extract order 9 8 7 5 3 2 1.
 *   heapSort([12,11,13,5,6,7]) -> [5,6,7,11,12,13].
 *   kthLargest([3,2,1,5,6,4], k=2) -> 5.
 *
 * COMPLEXITY:
 *   insert/extract O(log n); buildHeap O(n); heapSort O(n log n);
 *   kthLargest O(n log k); medianFromStream O(log n) per add.
 */

#include <algorithm>
#include <functional>
#include <iostream>
#include <queue>
#include <sstream>
#include <vector>

class MaxHeap {
public:
    void insert(int x) {
        data.push_back(x);
        siftUp(static_cast<int>(data.size()) - 1);
    }

    int extractMax() {
        int top = data.front();
        data.front() = data.back();
        data.pop_back();
        if (!data.empty()) siftDown(0);
        return top;
    }

    int peekMax() const { return data.front(); }
    bool empty() const { return data.empty(); }

private:
    std::vector<int> data;

    static int parent(int i) { return (i - 1) / 2; }
    static int left(int i)   { return 2 * i + 1; }
    static int right(int i)  { return 2 * i + 2; }

    void siftUp(int i) {
        while (i > 0 && data[parent(i)] < data[i]) {
            std::swap(data[i], data[parent(i)]);
            i = parent(i);
        }
    }

    void siftDown(int i) {
        int n = static_cast<int>(data.size());
        for (;;) {
            int l = left(i), r = right(i), largest = i;
            if (l < n && data[l] > data[largest]) largest = l;
            if (r < n && data[r] > data[largest]) largest = r;
            if (largest == i) return;
            std::swap(data[i], data[largest]);
            i = largest;
        }
    }
};

static void siftDownArr(std::vector<int>& a, int n, int i) {
    for (;;) {
        int l = 2*i+1, r = 2*i+2, largest = i;
        if (l < n && a[l] > a[largest]) largest = l;
        if (r < n && a[r] > a[largest]) largest = r;
        if (largest == i) return;
        std::swap(a[i], a[largest]);
        i = largest;
    }
}

void heapSort(std::vector<int>& a) {
    int n = static_cast<int>(a.size());
    for (int i = n/2 - 1; i >= 0; --i) siftDownArr(a, n, i);
    for (int i = n - 1; i > 0; --i) {
        std::swap(a[0], a[i]);
        siftDownArr(a, i, 0);
    }
}

int kthLargest(const std::vector<int>& arr, int k) {
    // min-heap of size k; root is the kth largest
    std::priority_queue<int, std::vector<int>, std::greater<int>> mh;
    for (int x : arr) {
        mh.push(x);
        if (static_cast<int>(mh.size()) > k) mh.pop();
    }
    return mh.top();
}

class MedianFinder {
public:
    void addNum(int x) {
        // lower is max-heap; upper is min-heap
        lower.push(x);
        upper.push(lower.top()); lower.pop();
        if (upper.size() > lower.size()) {
            lower.push(upper.top()); upper.pop();
        }
    }
    double findMedian() const {
        if (lower.size() > upper.size()) return static_cast<double>(lower.top());
        return (static_cast<double>(lower.top()) + upper.top()) / 2.0;
    }

private:
    std::priority_queue<int> lower; // max-heap
    std::priority_queue<int, std::vector<int>, std::greater<int>> upper; // min-heap
};

template<typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream os; os << "[";
    for (std::size_t i = 0; i < v.size(); ++i) { if (i) os << ", "; os << v[i]; }
    os << "]"; return os.str();
}

int main() {
    // Max-Heap
    std::cout << "=== Max-Heap ===\n";
    MaxHeap heap;
    for (int x : {5, 3, 7, 1, 9, 2, 8}) heap.insert(x);
    std::cout << "Extract in order: ";
    while (!heap.empty()) std::cout << heap.extractMax() << " ";
    std::cout << "\n";

    // Heap Sort
    std::cout << "\n=== Heap Sort ===\n";
    std::vector<int> arr = {12, 11, 13, 5, 6, 7};
    std::cout << "Before: " << vec_str(arr) << "\n";
    heapSort(arr);
    std::cout << "After:  " << vec_str(arr) << "\n";

    // Kth Largest
    std::cout << "\n=== Kth Largest ===\n";
    std::vector<int> arr2 = {3, 2, 1, 5, 6, 4};
    for (int k = 1; k <= static_cast<int>(arr2.size()); ++k)
        std::cout << "k=" << k << " -> " << kthLargest(arr2, k) << "\n";

    // STL priority_queue demo (min-heap)
    std::cout << "\n=== std::priority_queue (min-heap) ===\n";
    std::priority_queue<int, std::vector<int>, std::greater<int>> pq;
    for (int x : {5, 1, 3, 2, 4}) pq.push(x);
    std::cout << "Pop order: ";
    while (!pq.empty()) { std::cout << pq.top() << " "; pq.pop(); }
    std::cout << "\n";

    // Median from stream
    std::cout << "\n=== Median from Stream ===\n";
    MedianFinder mf;
    for (int x : {5, 15, 1, 3, 2, 8, 7, 9, 10, 6, 11, 4}) {
        mf.addNum(x);
        std::cout << "Added " << x << " -> median = " << mf.findMedian() << "\n";
    }
    return 0;
}

/*
 * NOTES (vs. Java):
 * - std::priority_queue is the STL equivalent of Java's PriorityQueue.
 * - C++ default is MAX-heap (opposite of Java/Python defaults).
 * - For min-heap, supply std::greater<T> as the comparator.
 * - std::make_heap / std::push_heap / std::pop_heap operate on raw
 *   iterators if you want full control over the storage.
 */
