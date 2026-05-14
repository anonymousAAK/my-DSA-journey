/*
 * WEEK 29 - C++ ADVANCED TOPICS
 * Topic: Message Queues - FIFO, Priority, Delayed, Pub/Sub
 * File: message_queues.cpp
 *
 * CONCEPT:
 *   Decouple producers and consumers. Four flavours:
 *     - FIFO:    ordered consumption (std::deque).
 *     - PRIORITY: high priority first (std::priority_queue).
 *     - DELAYED:  messages become visible at a future time (heap of pairs).
 *     - PUB/SUB:  one publish, many subscribers receive.
 *
 * KEY POINTS:
 *   - At-least-once semantics need acks + redelivery (not shown).
 *   - Visibility timeout hides in-flight messages.
 *
 * ALGORITHM / APPROACH:
 *   PRIORITY: push (priority, tie, msg); pop highest priority.
 *   DELAYED:  push (deliver_at, tie, msg); poll() pops only if ready.
 *   PUBSUB:   broker -> topic -> list of callbacks; iterate and invoke.
 *
 * C++-SPECIFIC NOTES:
 *   - std::priority_queue is a max-heap by default — negate priority or
 *     use std::greater<> with a min-heap.
 *   - std::function captures subscriber callbacks.
 *
 * DRY RUN / EXAMPLE:
 *   Priority {(0,'low'),(1,'med'),(2,'high')}: pop -> high, med, low.
 *   Delayed put('A', 50 ms); poll now -> empty; sleep; poll -> 'A'.
 *
 * COMPLEXITY:
 *   FIFO O(1); Priority/Delayed O(log n); Pub/Sub O(subscribers/publish).
 */

#include <iostream>
#include <queue>
#include <vector>
#include <string>
#include <chrono>
#include <thread>
#include <functional>
#include <unordered_map>
#include <utility>
#include <deque>

using namespace std;
using namespace std::chrono;

class FIFOQueue {
    deque<string> q;
public:
    void put(const string& m) { q.push_back(m); }
    bool get(string& out) {
        if (q.empty()) return false;
        out = q.front(); q.pop_front(); return true;
    }
    size_t size() const { return q.size(); }
};

class PriorityQueueMQ {
    long long tie = 0;
    using Entry = tuple<int, long long, string>;
    // higher priority first: use max-heap; tuple ordering uses priority then tie
    priority_queue<Entry, vector<Entry>, less<Entry>> pq;
public:
    void put(const string& m, int priority) { pq.emplace(priority, ++tie, m); }
    bool get(string& out) {
        if (pq.empty()) return false;
        out = std::get<2>(pq.top()); pq.pop(); return true;
    }
};

class DelayedQueue {
    long long tie = 0;
    using TP = steady_clock::time_point;
    using Entry = tuple<TP, long long, string>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> pq;
public:
    void put(const string& m, double deliver_in_seconds) {
        pq.emplace(steady_clock::now() + duration_cast<steady_clock::duration>(
            duration<double>(deliver_in_seconds)), ++tie, m);
    }
    bool poll(string& out) {
        if (pq.empty()) return false;
        if (std::get<0>(pq.top()) > steady_clock::now()) return false;
        out = std::get<2>(pq.top()); pq.pop(); return true;
    }
};

class PubSubBroker {
    unordered_map<string, vector<function<void(const string&)>>> topics;
public:
    void subscribe(const string& topic, function<void(const string&)> cb) {
        topics[topic].push_back(move(cb));
    }
    void publish(const string& topic, const string& msg) {
        auto it = topics.find(topic);
        if (it == topics.end()) return;
        for (auto& cb : it->second) cb(msg);
    }
};

int main() {
    FIFOQueue fifo;
    for (auto m : {"a","b","c"}) fifo.put(m);
    string out;
    cout << "FIFO drain:";
    while (fifo.get(out)) cout << " " << out;
    cout << "\n";

    PriorityQueueMQ pq;
    pq.put("low", 0); pq.put("med", 1); pq.put("high", 2);
    cout << "Priority drain:";
    while (pq.get(out)) cout << " " << out;
    cout << "\n";

    DelayedQueue dq;
    dq.put("future-A", 0.05);
    cout << "Delayed poll now: " << (dq.poll(out) ? out : "EMPTY") << "\n";
    this_thread::sleep_for(milliseconds(60));
    cout << "Delayed poll later: " << (dq.poll(out) ? out : "EMPTY") << "\n";

    PubSubBroker broker;
    vector<string> output;
    broker.subscribe("orders", [&](const string& m) { output.push_back("sub1<-" + m); });
    broker.subscribe("orders", [&](const string& m) { output.push_back("sub2<-" + m); });
    broker.publish("orders", "ORD#42");
    cout << "Pub/Sub delivered:";
    for (auto& s : output) cout << " " << s;
    cout << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Java's system_design.java covers different topics; we add four queue
 *     flavours for spec completeness.
 *   - std::priority_queue is a max-heap; for the delayed queue we use
 *     greater<> to get min-heap on time.
 *   - std::function captures subscribers heap-allocated; for hot paths
 *     consider a custom function-list of fixed callback type.
 */
