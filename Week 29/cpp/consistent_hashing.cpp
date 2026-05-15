/*
 * WEEK 29 - C++ ADVANCED TOPICS
 * Topic: Consistent Hashing with Virtual Nodes
 * File: consistent_hashing.cpp
 *
 * CONCEPT:
 *   Map nodes and keys onto a hash ring (0..UINT64_MAX). Each key belongs
 *   to the next node clockwise. Each physical node receives V virtual
 *   nodes (different hash positions) to balance load and smooth
 *   rebalancing. Adding/removing a node only displaces ~1/N of keys.
 *
 * KEY POINTS:
 *   - O(log(N*V)) lookup via std::map::lower_bound / upper_bound.
 *   - Used by: DynamoDB, Cassandra, memcached clients, Akka.
 *   - Virtual nodes per physical node (V) typically 100-200.
 *
 * ALGORITHM / APPROACH:
 *   add: insert hash(node + "#VN" + i) for i in [0, V) into the map.
 *   remove: erase those keys.
 *   get_node: upper_bound(hash(key)); wrap to begin() if at end.
 *
 * C++-SPECIFIC NOTES:
 *   - std::map<uint64_t, string> is a balanced BST.
 *   - For demos use std::hash<string>; real systems use SHA-256.
 *
 * DRY RUN / EXAMPLE:
 *   Add A, B, C with V=150 -> 450 entries. Query several keys before and
 *   after removing B to see the locality of remapped keys.
 *
 * COMPLEXITY:
 *   Time add/remove O(V log(NV)); get O(log(NV)).
 *   Space O(NV).
 */

#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <functional>
#include <cstdint>

using namespace std;

class ConsistentHashRing {
    int v;
    map<uint64_t, string> ring;

    static uint64_t hashKey(const string& s) {
        // demo only; not stable across processes
        return (uint64_t)hash<string>{}(s);
    }
public:
    explicit ConsistentHashRing(int vnodes) : v(vnodes) {}

    void addNode(const string& name) {
        for (int i = 0; i < v; ++i)
            ring[hashKey(name + "#VN" + to_string(i))] = name;
    }
    void removeNode(const string& name) {
        for (int i = 0; i < v; ++i)
            ring.erase(hashKey(name + "#VN" + to_string(i)));
    }
    string getNode(const string& key) const {
        if (ring.empty()) return "";
        auto it = ring.lower_bound(hashKey(key));
        if (it == ring.end()) it = ring.begin();
        return it->second;
    }
};

int main() {
    ConsistentHashRing ring(150);
    for (auto& n : {"server-A", "server-B", "server-C"}) ring.addNode(n);
    for (auto& k : {"user:1001", "session:xyz", "order:42"})
        cout << "  " << k << " -> " << ring.getNode(k) << "\n";

    cout << "\nAfter removing server-B:\n";
    ring.removeNode("server-B");
    for (auto& k : {"user:1001", "session:xyz", "order:42"})
        cout << "  " << k << " -> " << ring.getNode(k) << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - std::map::lower_bound replaces TreeMap.ceilingEntry.
 *   - We use std::hash<string> for the demo; Java demo used SHA-256.
 *     For real cross-process stability switch to a SHA-256 hash.
 */
