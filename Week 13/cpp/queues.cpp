/*
 * =============================================================================
 * Week 13 - Queues (C++ Edition)
 * =============================================================================
 *
 * Topics Covered:
 *   1. Queue implementation using vector/array (for understanding)
 *   2. Circular Queue (fixed-size ring buffer)
 *   3. Queue using two stacks
 *   4. Sliding Window Maximum (using deque — monotonic deque)
 *
 * Complexity Analysis provided for every function.
 * Uses modern C++17 features where appropriate.
 * =============================================================================
 */

#include <bits/stdc++.h>
using namespace std;

// =============================================================================
// 1. SIMPLE QUEUE (using std::deque internally for illustration)
// =============================================================================
// All operations: O(1)
// This demonstrates the interface. In practice, use std::queue<T>.
template <typename T>
class SimpleQueue {
    deque<T> data_;

public:
    // Enqueue — O(1) amortized
    void enqueue(const T& val) {
        data_.push_back(val);
    }

    // Dequeue — O(1)
    T dequeue() {
        if (data_.empty()) throw runtime_error("Queue underflow");
        T val = data_.front();
        data_.pop_front();
        return val;
    }

    // Peek front — O(1)
    T front() const {
        if (data_.empty()) throw runtime_error("Queue is empty");
        return data_.front();
    }

    bool empty() const { return data_.empty(); }
    size_t size() const { return data_.size(); }
};

// =============================================================================
// 2. CIRCULAR QUEUE (Fixed-Size Ring Buffer)
// =============================================================================
// All operations: O(1)
// Space: O(k) where k = capacity
class CircularQueue {
    vector<int> buffer_;
    int head_;      // index of front element
    int tail_;      // index of next insertion point
    int size_;      // current number of elements
    int capacity_;

public:
    CircularQueue(int k) : buffer_(k), head_(0), tail_(0), size_(0), capacity_(k) {}

    // Enqueue — O(1)
    bool enqueue(int val) {
        if (isFull()) return false;
        buffer_[tail_] = val;
        tail_ = (tail_ + 1) % capacity_;
        ++size_;
        return true;
    }

    // Dequeue — O(1)
    bool dequeue() {
        if (isEmpty()) return false;
        head_ = (head_ + 1) % capacity_;
        --size_;
        return true;
    }

    // Front — O(1)
    int front() const {
        if (isEmpty()) return -1;
        return buffer_[head_];
    }

    // Rear — O(1)
    int rear() const {
        if (isEmpty()) return -1;
        return buffer_[(tail_ - 1 + capacity_) % capacity_];
    }

    bool isEmpty() const { return size_ == 0; }
    bool isFull() const { return size_ == capacity_; }
    int getSize() const { return size_; }

    void printState() const {
        cout << "  [";
        for (int i = 0; i < size_; ++i) {
            int idx = (head_ + i) % capacity_;
            cout << buffer_[idx] << (i + 1 < size_ ? ", " : "");
        }
        cout << "] (size=" << size_ << ", capacity=" << capacity_ << ")" << endl;
    }
};

// =============================================================================
// 3. QUEUE USING TWO STACKS
// =============================================================================
// Amortized O(1) for enqueue and dequeue.
//
// Strategy: push stack for enqueue, pop stack for dequeue.
// Transfer from push to pop stack only when pop stack is empty.
// Each element is moved at most twice (once to pushStack, once to popStack),
// so amortized O(1) per operation.
class QueueTwoStacks {
    stack<int> pushStack_;  // for enqueue
    stack<int> popStack_;   // for dequeue

    void transfer() {
        while (!pushStack_.empty()) {
            popStack_.push(pushStack_.top());
            pushStack_.pop();
        }
    }

public:
    // Enqueue — O(1)
    void enqueue(int val) {
        pushStack_.push(val);
    }

    // Dequeue — O(1) amortized
    int dequeue() {
        if (popStack_.empty()) transfer();
        if (popStack_.empty()) throw runtime_error("Queue underflow");
        int val = popStack_.top();
        popStack_.pop();
        return val;
    }

    // Peek — O(1) amortized
    int front() {
        if (popStack_.empty()) transfer();
        if (popStack_.empty()) throw runtime_error("Queue is empty");
        return popStack_.top();
    }

    bool empty() const { return pushStack_.empty() && popStack_.empty(); }
    size_t size() const { return pushStack_.size() + popStack_.size(); }
};

// =============================================================================
// 4. SLIDING WINDOW MAXIMUM (Monotonic Deque)
// =============================================================================
// For each window of size k, find the maximum element.
//
// Time: O(n) — each element is added and removed from deque at most once
// Space: O(k) for the deque
//
// Key insight: maintain a monotonically decreasing deque of indices.
// The front of the deque is always the index of the maximum in the current window.
vector<int> slidingWindowMax(const vector<int>& nums, int k) {
    vector<int> result;
    deque<int> dq;  // stores indices; values at these indices are in decreasing order

    for (int i = 0; i < static_cast<int>(nums.size()); ++i) {
        // Remove elements outside the current window
        while (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }

        // Remove elements smaller than current (they can never be the max)
        while (!dq.empty() && nums[dq.back()] <= nums[i]) {
            dq.pop_back();
        }

        dq.push_back(i);

        // Window is fully formed once i >= k - 1
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }
    return result;
}

// Brute-force sliding window max for comparison
// Time: O(n * k)   Space: O(1) extra
vector<int> slidingWindowMaxBrute(const vector<int>& nums, int k) {
    vector<int> result;
    for (int i = 0; i <= static_cast<int>(nums.size()) - k; ++i) {
        int maxVal = nums[i];
        for (int j = i + 1; j < i + k; ++j) {
            maxVal = max(maxVal, nums[j]);
        }
        result.push_back(maxVal);
    }
    return result;
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
    cout << " Week 13: Queues (C++)" << endl;
    cout << "========================================" << endl;

    // --- 1. Simple Queue ---
    cout << "\n--- 1. Simple Queue ---" << endl;
    {
        SimpleQueue<int> q;
        for (int x : {10, 20, 30, 40, 50}) q.enqueue(x);
        cout << "Front: " << q.front() << " (expected 10)" << endl;
        cout << "Size: " << q.size() << " (expected 5)" << endl;
        cout << "Dequeue: " << q.dequeue() << endl;
        cout << "Dequeue: " << q.dequeue() << endl;
        cout << "Front after 2 dequeues: " << q.front() << " (expected 30)" << endl;
    }

    // --- 2. Circular Queue ---
    cout << "\n--- 2. Circular Queue ---" << endl;
    {
        CircularQueue cq(5);
        cout << "Enqueue 10,20,30,40,50:" << endl;
        for (int x : {10, 20, 30, 40, 50}) cq.enqueue(x);
        cq.printState();

        cout << "Is full: " << (cq.isFull() ? "yes" : "no") << endl;
        cout << "Enqueue 60 (should fail): " << (cq.enqueue(60) ? "ok" : "failed") << endl;

        cout << "Front: " << cq.front() << ", Rear: " << cq.rear() << endl;

        cq.dequeue();
        cq.dequeue();
        cout << "After 2 dequeues:";
        cq.printState();

        cq.enqueue(60);
        cq.enqueue(70);
        cout << "After enqueue 60, 70 (wraps around):";
        cq.printState();
        cout << "Front: " << cq.front() << ", Rear: " << cq.rear() << endl;
    }

    // --- 3. Queue Using Two Stacks ---
    cout << "\n--- 3. Queue Using Two Stacks ---" << endl;
    {
        QueueTwoStacks q;
        cout << "Enqueue: 1, 2, 3" << endl;
        q.enqueue(1);
        q.enqueue(2);
        q.enqueue(3);

        cout << "Dequeue: " << q.dequeue() << " (expected 1)" << endl;
        cout << "Dequeue: " << q.dequeue() << " (expected 2)" << endl;

        q.enqueue(4);
        q.enqueue(5);

        cout << "Dequeue: " << q.dequeue() << " (expected 3)" << endl;
        cout << "Dequeue: " << q.dequeue() << " (expected 4)" << endl;
        cout << "Front:   " << q.front() << " (expected 5)" << endl;
        cout << "Size:    " << q.size() << " (expected 1)" << endl;
    }

    // --- 4. Sliding Window Maximum ---
    cout << "\n--- 4. Sliding Window Maximum ---" << endl;
    {
        vector<int> nums1 = {1, 3, -1, -3, 5, 3, 6, 7};
        int k1 = 3;
        printVec(nums1, "Array");
        cout << "k = " << k1 << endl;
        printVec(slidingWindowMax(nums1, k1), "Deque result ");
        printVec(slidingWindowMaxBrute(nums1, k1), "Brute result ");
        // Expected: [3, 3, 5, 5, 6, 7]

        vector<int> nums2 = {1, -1};
        int k2 = 1;
        printVec(nums2, "\nArray");
        cout << "k = " << k2 << endl;
        printVec(slidingWindowMax(nums2, k2), "Result");
        // Expected: [1, -1]

        vector<int> nums3 = {9, 11};
        int k3 = 2;
        printVec(nums3, "\nArray");
        cout << "k = " << k3 << endl;
        printVec(slidingWindowMax(nums3, k3), "Result");
        // Expected: [11]

        // Larger test
        vector<int> nums4 = {4, 3, 5, 4, 3, 3, 6, 7};
        int k4 = 3;
        printVec(nums4, "\nArray");
        cout << "k = " << k4 << endl;
        printVec(slidingWindowMax(nums4, k4), "Result");
        // Expected: [5, 5, 5, 4, 6, 7]
    }

    cout << "\n========================================" << endl;
    cout << " All Week 13 tests complete!" << endl;
    cout << "========================================" << endl;
    return 0;
}
