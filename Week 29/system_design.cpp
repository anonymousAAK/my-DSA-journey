// Week 29: System Design - Consistent Hashing, LRU Cache, Rate Limiter, Trie, Merkle Tree
// Compile: g++ -std=c++17 -O2 -o system_design system_design.cpp

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <list>
#include <queue>
#include <algorithm>
#include <chrono>
#include <sstream>
#include <iomanip>
using namespace std;

// FNV-1a hash (portable, non-cryptographic). Use SHA-256 in production.
static uint64_t fnv_hash(const string& s) {
    uint64_t h = 14695981039346656037ULL;
    for (unsigned char c : s) { h ^= c; h *= 1099511628211ULL; }
    return h;
}
static string hash_hex(const string& s) {
    uint64_t h1 = fnv_hash(s), h2 = fnv_hash(s + "\x01");
    ostringstream oss;
    oss << hex << setfill('0') << setw(16) << h1 << setw(16) << h2;
    return oss.str();
}

// === Consistent Hashing with Virtual Nodes ===
// Used by: DynamoDB, Cassandra, load balancers
// Lookup: O(log(N*V)) via std::map   Space: O(N*V)
class ConsistentHashRing {
    map<uint64_t, string> ring_;
    int vnodes_;
public:
    ConsistentHashRing(int vnodes = 150) : vnodes_(vnodes) {}

    void add_node(const string& node) {  // O(V * log(N*V))
        for (int i = 0; i < vnodes_; ++i)
            ring_[fnv_hash(node + "#VN" + to_string(i))] = node;
    }
    void remove_node(const string& node) {  // O(V * log(N*V))
        for (int i = 0; i < vnodes_; ++i)
            ring_.erase(fnv_hash(node + "#VN" + to_string(i)));
    }
    string get_node(const string& key) const {  // O(log(N*V))
        if (ring_.empty()) return "";
        auto it = ring_.lower_bound(fnv_hash(key));
        if (it == ring_.end()) it = ring_.begin();
        return it->second;
    }
    size_t ring_size() const { return ring_.size(); }
};

// === LRU Cache (HashMap + Doubly Linked List) ===
// O(1) get/put via unordered_map + std::list splice. Space: O(capacity)
class LRUCache {
    int capacity;
    list<pair<int,int>> dll;
    unordered_map<int, list<pair<int,int>>::iterator> cache;
public:
    LRUCache(int cap) : capacity(cap) {}
    int get(int key) {  // O(1)
        auto it = cache.find(key);
        if (it == cache.end()) return -1;
        dll.splice(dll.begin(), dll, it->second);
        return it->second->second;
    }
    void put(int key, int value) {  // O(1)
        auto it = cache.find(key);
        if (it != cache.end()) { it->second->second = value; dll.splice(dll.begin(), dll, it->second); return; }
        if ((int)cache.size() == capacity) { cache.erase(dll.back().first); dll.pop_back(); }
        dll.emplace_front(key, value);
        cache[key] = dll.begin();
    }
};

// === Token Bucket Rate Limiter ===
// Allows bursts up to capacity, enforces average rate.
// O(1) per request, O(1) space. Used by: API gateways, nginx
class TokenBucket {
    int max_tokens_;
    double refill_rate_, tokens_;
    chrono::steady_clock::time_point last_;
public:
    TokenBucket(int max_tok, double rate)
        : max_tokens_(max_tok), refill_rate_(rate), tokens_((double)max_tok),
          last_(chrono::steady_clock::now()) {}

    bool allow_request() {  // O(1)
        auto now = chrono::steady_clock::now();
        double elapsed = chrono::duration<double>(now - last_).count();
        tokens_ = min((double)max_tokens_, tokens_ + elapsed * refill_rate_);
        last_ = now;
        if (tokens_ >= 1.0) { tokens_ -= 1.0; return true; }
        return false;  // 429 Too Many Requests
    }
};

// === Trie Autocomplete with Frequency Ranking ===
// Insert: O(L)   Search: O(L + M + K log K)   Space: O(N*L)
// Used by: search engines, IDE completion, phone keyboards
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool is_end = false;
    int freq = 0;
    string word;
    ~TrieNode() { for (auto& [_, c] : children) delete c; }
};

class AutoComplete {
    TrieNode* root = new TrieNode();
    using Entry = pair<int, string>;
    void dfs(TrieNode* n, priority_queue<Entry, vector<Entry>, greater<>>& heap, int k) {
        if (n->is_end) {
            if ((int)heap.size() < k) heap.emplace(n->freq, n->word);
            else if (n->freq > heap.top().first) { heap.pop(); heap.emplace(n->freq, n->word); }
        }
        for (auto& [_, child] : n->children) dfs(child, heap, k);
    }
public:
    ~AutoComplete() { delete root; }

    void insert(const string& word, int freq = 1) {  // O(L)
        TrieNode* n = root;
        for (char c : word) { if (!n->children.count(c)) n->children[c] = new TrieNode(); n = n->children[c]; }
        n->is_end = true; n->freq += freq; n->word = word;
    }

    vector<string> suggest(const string& prefix, int k = 5) {  // O(L + M + K log K)
        TrieNode* n = root;
        for (char c : prefix) { if (!n->children.count(c)) return {}; n = n->children[c]; }
        priority_queue<Entry, vector<Entry>, greater<>> heap;
        dfs(n, heap, k);
        vector<string> res;
        while (!heap.empty()) { res.push_back(heap.top().second); heap.pop(); }
        reverse(res.begin(), res.end());
        return res;
    }
};

// === Merkle Tree with Proof Verification ===
// Build: O(N)   Proof/Verify: O(log N)   Space: O(N)
// Used by: Bitcoin, Git, IPFS, DynamoDB anti-entropy
class MerkleTree {
    vector<vector<string>> tree_;  // [0]=leaves, [last]=[root]
public:
    MerkleTree(const vector<string>& data) {
        vector<string> leaves;
        for (auto& d : data) leaves.push_back(hash_hex(d));
        if (leaves.size() % 2) leaves.push_back(leaves.back());

        tree_.push_back(leaves);
        auto cur = leaves;
        while (cur.size() > 1) {
            vector<string> next;
            for (size_t i = 0; i < cur.size(); i += 2) {
                auto& r = (i + 1 < cur.size()) ? cur[i + 1] : cur[i];
                next.push_back(hash_hex(cur[i] + r));
            }
            tree_.push_back(next); cur = next;
        }
    }

    string root() const { return tree_.back()[0]; }

    // Proof: list of (sibling_hash, sibling_is_left) — O(log N)
    vector<pair<string, bool>> get_proof(int idx) const {
        vector<pair<string, bool>> proof;
        for (size_t lvl = 0; lvl < tree_.size() - 1; ++lvl) {
            auto& layer = tree_[lvl];
            if (idx % 2 == 0) {
                auto& sib = (idx + 1 < (int)layer.size()) ? layer[idx + 1] : layer[idx];
                proof.emplace_back(sib, false);
            } else {
                proof.emplace_back(layer[idx - 1], true);
            }
            idx /= 2;
        }
        return proof;
    }

    // Recompute hash path and compare to root — O(log N)
    static bool verify_proof(const string& data, const vector<pair<string, bool>>& proof, const string& root) {
        string cur = hash_hex(data);
        for (auto& [sib, is_left] : proof)
            cur = is_left ? hash_hex(sib + cur) : hash_hex(cur + sib);
        return cur == root;
    }
};

int main() {
    cout << "=== WEEK 29: System Design for Engineers (C++) ===\n\n";

    // 1. Consistent Hashing
    cout << "--- Consistent Hashing ---\n";
    ConsistentHashRing ring(150);
    ring.add_node("server-A"); ring.add_node("server-B"); ring.add_node("server-C");
    cout << "Ring size: " << ring.ring_size() << "\n";
    for (auto& k : {"user:1001", "session:xyz", "order:42"})
        cout << "  " << k << " -> " << ring.get_node(k) << "\n";
    ring.remove_node("server-B");
    cout << "After removing server-B:\n";
    for (auto& k : {"user:1001", "session:xyz", "order:42"})
        cout << "  " << k << " -> " << ring.get_node(k) << "\n";

    // 2. LRU Cache
    cout << "\n--- LRU Cache ---\n";
    LRUCache cache(2);
    cache.put(1, 1); cache.put(2, 2);
    cout << "get(1): " << cache.get(1) << endl;
    cache.put(3, 3);
    cout << "get(2): " << cache.get(2) << endl; // -1 (evicted)

    // 3. Rate Limiter
    cout << "\n--- Token Bucket Rate Limiter ---\n";
    TokenBucket tb(5, 2.0);
    for (int i = 1; i <= 7; ++i)
        cout << "  Request " << i << ": " << (tb.allow_request() ? "ALLOWED" : "REJECTED") << "\n";

    // 4. Trie Autocomplete
    cout << "\n--- Trie Autocomplete ---\n";
    AutoComplete ac;
    ac.insert("system design", 50); ac.insert("system call", 30);
    ac.insert("systematic", 20); ac.insert("syntax", 10);
    auto sugg = ac.suggest("sys", 3);
    cout << "Top 3 for 'sys': [";
    for (size_t i = 0; i < sugg.size(); ++i) { if (i) cout << ", "; cout << "\"" << sugg[i] << "\""; }
    cout << "]\n";

    // 5. Merkle Tree
    cout << "\n--- Merkle Tree ---\n";
    MerkleTree mt({"tx1:A->B:50", "tx2:B->C:30", "tx3:C->D:20", "tx4:D->E:10"});
    cout << "Root: " << mt.root().substr(0, 16) << "...\n";
    auto proof = mt.get_proof(2);
    cout << "Proof valid: " << (MerkleTree::verify_proof("tx3:C->D:20", proof, mt.root()) ? "true" : "false") << "\n";
    cout << "Tampered:    " << (MerkleTree::verify_proof("tx3:C->D:99", proof, mt.root()) ? "true" : "false") << "\n";

    return 0;
}
