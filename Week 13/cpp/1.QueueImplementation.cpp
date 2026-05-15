/*
 * WEEK 13 - C++ DSA
 * Topic: Queue Implementations + Sliding Window Maximum
 * File: 1.QueueImplementation.cpp
 *
 * CONCEPT:
 *   FIFO container. Enqueue at the back, dequeue from the front. Variants:
 *   circular queue (ring buffer), queue from two stacks, deque (used for
 *   monotonic-deque sliding window maximum).
 *
 * KEY POINTS:
 *   - std::queue<T> is the STL adapter; backed by std::deque by default.
 *   - std::deque<T> is the canonical double-ended queue.
 *   - Sliding window max uses a monotonic deque storing indices.
 *
 * ALGORITHM / APPROACH:
 *   See Week 13 Java file. Same algorithms.
 *
 * C++-SPECIFIC NOTES:
 *   - Templates for the circular queue.
 *   - Use std::deque<int> for the SWM monotonic deque.
 *   - We avoid undefined behavior with explicit empty() checks before front
 *     / back access.
 *
 * DRY RUN:
 *   Same as Java/Python files.
 *
 * COMPLEXITY:
 *   CircularQueue ops: O(1)
 *   QueueUsingStacks ops: amortized O(1)
 *   slidingWindowMax: O(n) total
 */

#include <iostream>
#include <stack>
#include <deque>
#include <stdexcept>
#include <vector>
#include <sstream>

template <typename T>
class CircularQueue {
public:
    explicit CircularQueue(std::size_t capacity)
        : cap(capacity), data(capacity), front(0), rear(0), sz(0) {}

    bool enqueue(const T& x) {
        if (sz == cap) return false;
        data[rear] = x;
        rear = (rear + 1) % cap;
        ++sz;
        return true;
    }

    T dequeue() {
        if (sz == 0) throw std::runtime_error("Queue empty");
        T x = data[front];
        front = (front + 1) % cap;
        --sz;
        return x;
    }

    const T& peek() const {
        if (sz == 0) throw std::runtime_error("Queue empty");
        return data[front];
    }

    bool empty() const { return sz == 0; }
    bool full() const  { return sz == cap; }
    std::size_t size() const { return sz; }

private:
    std::size_t cap;
    std::vector<T> data;
    std::size_t front, rear, sz;
};

class QueueUsingStacks {
public:
    void enqueue(int x) { inbox.push(x); }

    int dequeue() {
        shift();
        if (outbox.empty()) throw std::runtime_error("Queue empty");
        int v = outbox.top();
        outbox.pop();
        return v;
    }

    int peek() {
        shift();
        if (outbox.empty()) throw std::runtime_error("Queue empty");
        return outbox.top();
    }

    bool empty() const { return inbox.empty() && outbox.empty(); }

private:
    std::stack<int> inbox, outbox;
    void shift() {
        if (!outbox.empty()) return;
        while (!inbox.empty()) { outbox.push(inbox.top()); inbox.pop(); }
    }
};

std::vector<int> slidingWindowMax(const std::vector<int>& arr, int k) {
    int n = static_cast<int>(arr.size());
    if (n == 0 || k == 0) return {};
    std::vector<int> result;
    result.reserve(n - k + 1);
    std::deque<int> dq; // indices, arr[dq] strictly decreasing
    for (int i = 0; i < n; ++i) {
        while (!dq.empty() && dq.front() < i - k + 1) dq.pop_front();
        while (!dq.empty() && arr[dq.back()] < arr[i]) dq.pop_back();
        dq.push_back(i);
        if (i >= k - 1) result.push_back(arr[dq.front()]);
    }
    return result;
}

template<typename T>
std::string vec_str(const std::vector<T>& v) {
    std::ostringstream os; os << "[";
    for (std::size_t i = 0; i < v.size(); ++i) { if (i) os << ", "; os << v[i]; }
    os << "]"; return os.str();
}

int main() {
    std::cout << "=== Circular Queue ===\n";
    CircularQueue<int> cq(4);
    cq.enqueue(1); cq.enqueue(2); cq.enqueue(3); cq.enqueue(4);
    std::cout << "Full: " << std::boolalpha << cq.full() << "\n";
    std::cout << "Dequeue: " << cq.dequeue() << "\n";
    cq.enqueue(5);
    std::cout << "Peek: " << cq.peek() << "\n";

    std::cout << "\n=== Queue using Two Stacks ===\n";
    QueueUsingStacks q;
    q.enqueue(1); q.enqueue(2); q.enqueue(3);
    std::cout << "dequeue: " << q.dequeue() << "\n";
    std::cout << "dequeue: " << q.dequeue() << "\n";
    q.enqueue(4);
    std::cout << "peek: " << q.peek() << "\n";
    std::cout << "dequeue: " << q.dequeue() << "\n";
    std::cout << "dequeue: " << q.dequeue() << "\n";

    std::cout << "\n=== std::deque as Queue ===\n";
    std::deque<int> jd;
    jd.push_back(10); jd.push_back(20); jd.push_back(30);
    std::cout << "peek: " << jd.front() << "\n";
    std::cout << "poll: " << jd.front() << "\n"; jd.pop_front();
    std::cout << "poll: " << jd.front() << "\n"; jd.pop_front();

    std::cout << "\n=== Sliding Window Maximum ===\n";
    std::vector<int> arr = {1, 3, -1, -3, 5, 3, 6, 7};
    int k = 3;
    std::cout << "Array: " << vec_str(arr) << " k=" << k << "\n";
    std::cout << "Max in each window: " << vec_str(slidingWindowMax(arr, k)) << "\n";

    std::vector<int> arr2 = {9, 11};
    std::cout << "\nArray: " << vec_str(arr2) << " k=2\n";
    std::cout << "Max: " << vec_str(slidingWindowMax(arr2, 2)) << "\n";

    return 0;
}

/*
 * NOTES (vs. Java):
 * - std::queue is the STL queue adapter; std::deque is the workhorse for
 *   anything more interesting. Java's ArrayDeque corresponds.
 * - The two-stacks approach is identical conceptually.
 * - C++ throws std::runtime_error on misuse; Java throws RuntimeException.
 */
