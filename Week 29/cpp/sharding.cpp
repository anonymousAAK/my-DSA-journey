/*
 * WEEK 29 - C++ ADVANCED TOPICS
 * Topic: Sharding Strategies
 * File: sharding.cpp
 *
 * CONCEPT:
 *   Partition data across N nodes. Three classical strategies:
 *     - Range: lex-ordered key ranges per shard.
 *     - Hash:  shard = hash(key) mod N.
 *     - Directory: explicit per-key mapping in metadata.
 *
 * KEY POINTS:
 *   - Range queries vs. uniform load is the central trade-off.
 *   - Hash gives near-uniform distribution but rebalancing on N change is
 *     costly without consistent hashing.
 *
 * ALGORITHM / APPROACH:
 *   RANGE:  std::upper_bound on sorted boundaries.
 *   HASH:   std::hash<string> + modulo (use a stable hash in real systems).
 *   DIR:    std::unordered_map<string, int>.
 *
 * C++-SPECIFIC NOTES:
 *   - std::hash<string> is OK for demos but is not stable across
 *     processes / binaries. Use SHA-256 in production.
 *
 * DRY RUN / EXAMPLE:
 *   range boundaries {"c","m","t"}: 'apple'->0, 'cat'->1, 'mango'->2,
 *   'tiger'->3.
 *
 * COMPLEXITY:
 *   Range: O(log shards); Hash: O(L); Dir: O(1).
 */

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <functional>

using namespace std;

class RangeShardRouter {
    vector<string> b;
public:
    explicit RangeShardRouter(vector<string> boundaries) : b(move(boundaries)) {
        sort(b.begin(), b.end());
    }
    int route(const string& key) const {
        return (int)(upper_bound(b.begin(), b.end(), key) - b.begin());
    }
};

class HashShardRouter {
    int n;
public:
    explicit HashShardRouter(int n) : n(n) {}
    int route(const string& key) const {
        return (int)(hash<string>{}(key) % (size_t)n);
    }
};

class DirectoryShardRouter {
    unordered_map<string, int> map;
public:
    void assign(const string& key, int shard) { map[key] = shard; }
    int route(const string& key) const {
        auto it = map.find(key);
        return it == map.end() ? -1 : it->second;
    }
};

int main() {
    RangeShardRouter rng({"c", "m", "t"});
    for (auto& k : {"apple","banana","cat","mango","tiger"})
        cout << "range " << k << " -> shard " << rng.route(k) << "\n";

    HashShardRouter hsh(4);
    for (auto& k : {"user:42","user:43","order:99","session:xyz"})
        cout << "hash  " << k << " -> shard " << hsh.route(k) << "\n";

    DirectoryShardRouter dr;
    dr.assign("hot-customer:Acme", 0);
    dr.assign("hot-customer:Globex", 1);
    cout << "dir   hot-customer:Acme -> shard "
         << dr.route("hot-customer:Acme") << "\n";
    return 0;
}

/*
 * NOTES
 * -----
 * Differences from Java:
 *   - Java's system_design.java does not include sharding; we add it.
 *   - std::upper_bound + iterator subtraction is the C++ binary-search idiom.
 *   - std::hash<string> for demo; use SHA-256 if cross-process stability is
 *     required.
 */
