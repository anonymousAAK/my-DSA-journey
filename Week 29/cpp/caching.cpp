/*
 * WEEK 29 - C++ ADVANCED TOPICS
 * Topic: Caching - LRU, LFU and TTL
 * File: caching.cpp
 *
 * CONCEPT:
 *   Caches accelerate access to frequently used items by storing them in
 *   limited fast storage. Eviction policy decides what to drop:
 *     - LRU: drop the least recently used (HashMap + doubly-linked list).
 *     - LFU: drop the least frequently used (HashMap + freq buckets).
 *     - TTL: each entry expires after a fixed time.
 *
 * KEY POINTS:
 *   - LRU: O(1) get/put with std::list + std::unordered_map<key, iterator>.
 *   - LFU: O(1) get/put using freq -> list<key>, key -> (value, freq, iter).
 *   - TTL: store deadline; lazily evict on access.
 *
 * ALGORITHM / APPROACH:
 *   LRU: on get/put, move node to list head; if size > cap, drop tail.
 *   LFU: bump freq, move key from bucket f to bucket f+1; evict from
 *        minFreq bucket's tail when full.
 *   TTL: compare std::chrono::steady_clock::now() against entry's expiry.
 *
 * C++-SPECIFIC NOTES:
 *   - std::list::iterator stays valid on insert/erase elsewhere.
 *   - std::chrono::steady_clock for monotonic time.
 *
 * DRY RUN / EXAMPLE:
 *   LRU cap=2: put(1,1); put(2,2); get(1)=1; put(3,3) evicts 2; get(2)=-1.
 *   LFU cap=2: put(1); put(2); get(1) twice -> evict 2 on put(3).
 *
 * COMPLEXITY:
 *   LRU/LFU: O(1) per op.
 *   TTL:     O(1) per op.
 */

#include <iostream>
#include <list>
#include <unordered_map>
#include <chrono>
#include <thread>
#include <string>

using namespace std;

// ---------------------------------------------------------------------------
// LRU Cache
// ---------------------------------------------------------------------------
class LRUCache {
    int cap;
    list<pair<int,int>> lst; // (key, value); front = most recent
    unordered_map<int, list<pair<int,int>>::iterator> mp;
public:
    explicit LRUCache(int c) : cap(c) {}

    int get(int key) {
        auto it = mp.find(key);
        if (it == mp.end()) return -1;
        lst.splice(lst.begin(), lst, it->second);
        return it->second->second;
    }

    void put(int key, int val) {
        auto it = mp.find(key);
        if (it != mp.end()) {
            it->second->second = val;
            lst.splice(lst.begin(), lst, it->second);
            return;
        }
        if ((int)lst.size() == cap) {
            mp.erase(lst.back().first);
            lst.pop_back();
        }
        lst.emplace_front(key, val);
        mp[key] = lst.begin();
    }
};

// ---------------------------------------------------------------------------
// LFU Cache (O(1) with freq buckets)
// ---------------------------------------------------------------------------
class LFUCache {
    int cap, minFreq;
    unordered_map<int, pair<int,int>> kv;             // key -> (value, freq)
    unordered_map<int, list<int>> fl;                 // freq -> list of keys (LRU within)
    unordered_map<int, list<int>::iterator> kit;      // key -> iterator in fl[freq]

    void bump(int key) {
        auto& [val, freq] = kv[key];
        fl[freq].erase(kit[key]);
        if (fl[freq].empty()) {
            fl.erase(freq);
            if (minFreq == freq) ++minFreq;
        }
        ++freq;
        fl[freq].push_front(key);
        kit[key] = fl[freq].begin();
    }
public:
    explicit LFUCache(int c) : cap(c), minFreq(0) {}

    int get(int key) {
        if (!kv.count(key)) return -1;
        bump(key);
        return kv[key].first;
    }

    void put(int key, int val) {
        if (cap <= 0) return;
        if (kv.count(key)) {
            kv[key].first = val;
            bump(key);
            return;
        }
        if ((int)kv.size() >= cap) {
            int evict = fl[minFreq].back();
            fl[minFreq].pop_back();
            if (fl[minFreq].empty()) fl.erase(minFreq);
            kv.erase(evict);
            kit.erase(evict);
        }
        kv[key] = {val, 1};
        fl[1].push_front(key);
        kit[key] = fl[1].begin();
        minFreq = 1;
    }
};

// ---------------------------------------------------------------------------
// TTL Cache
// ---------------------------------------------------------------------------
class TTLCache {
    using Clock = chrono::steady_clock;
    chrono::milliseconds defTtl;
    unordered_map<string, pair<string, Clock::time_point>> store;
public:
    explicit TTLCache(int defaultTtlMs) : defTtl(defaultTtlMs) {}
    void put(const string& k, const string& v) {
        store[k] = {v, Clock::now() + defTtl};
    }
    bool get(const string& k, string& out) {
        auto it = store.find(k);
        if (it == store.end()) return false;
        if (it->second.second < Clock::now()) { store.erase(it); return false; }
        out = it->second.first;
        return true;
    }
};

int main() {
    LRUCache lru(2);
    lru.put(1, 1); lru.put(2, 2);
    cout << "LRU get(1) = " << lru.get(1) << "\n";
    lru.put(3, 3);
    cout << "LRU get(2) = " << lru.get(2) << "  (expected -1)\n";

    LFUCache lfu(2);
    lfu.put(1, 1); lfu.put(2, 2);
    lfu.get(1); lfu.get(1);
    lfu.put(3, 3);
    cout << "LFU get(2) = " << lfu.get(2) << "  (expected -1)\n";
    cout << "LFU get(1) = " << lfu.get(1) << "  (expected 1)\n";
    cout << "LFU get(3) = " << lfu.get(3) << "  (expected 3)\n";

    TTLCache ttl(50);
    ttl.put("alpha", "value");
    string out;
    cout << "TTL get(alpha) imm.: " << (ttl.get("alpha", out) ? out : "MISS") << "\n";
    this_thread::sleep_for(chrono::milliseconds(60));
    cout << "TTL get(alpha) later: " << (ttl.get("alpha", out) ? out : "MISS") << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - C++ uses std::list + iterator stability instead of a hand-rolled
 *     doubly-linked list.
 *   - LFU here is O(1); Java's system_design.java demoes only LRU.
 *   - std::chrono::steady_clock is the C++ monotonic clock.
 */
