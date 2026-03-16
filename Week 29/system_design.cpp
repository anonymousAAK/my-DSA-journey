// Week 29: System Design - LRU Cache, Trie Autocomplete
#include <iostream>
#include <unordered_map>
#include <list>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

// === LRU Cache ===
class LRUCache {
    int capacity;
    list<pair<int,int>> dll;
    unordered_map<int, list<pair<int,int>>::iterator> cache;
public:
    LRUCache(int cap) : capacity(cap) {}
    int get(int key) {
        auto it = cache.find(key);
        if (it == cache.end()) return -1;
        dll.splice(dll.begin(), dll, it->second);
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = cache.find(key);
        if (it != cache.end()) { it->second->second = value; dll.splice(dll.begin(), dll, it->second); return; }
        if ((int)cache.size() == capacity) { cache.erase(dll.back().first); dll.pop_back(); }
        dll.emplace_front(key, value);
        cache[key] = dll.begin();
    }
};

// === Trie Autocomplete ===
struct TrieNode {
    unordered_map<char, TrieNode*> children;
    bool is_end = false;
    int freq = 0;
};

class AutoComplete {
    TrieNode* root = new TrieNode();
    void dfs(TrieNode* n, string& path, vector<pair<int,string>>& results) {
        if (n->is_end) results.push_back({n->freq, path});
        for (auto& [ch, child] : n->children) { path.push_back(ch); dfs(child, path, results); path.pop_back(); }
    }
public:
    void insert(const string& word) {
        TrieNode* n = root;
        for (char c : word) { if (!n->children.count(c)) n->children[c] = new TrieNode(); n = n->children[c]; }
        n->is_end = true; n->freq++;
    }
    vector<string> suggest(const string& prefix, int k = 5) {
        TrieNode* n = root;
        for (char c : prefix) { if (!n->children.count(c)) return {}; n = n->children[c]; }
        vector<pair<int,string>> results;
        string path = prefix;
        dfs(n, path, results);
        sort(results.begin(), results.end(), [](auto& a, auto& b) { return a.first > b.first; });
        vector<string> out;
        for (int i = 0; i < min(k, (int)results.size()); i++) out.push_back(results[i].second);
        return out;
    }
};

int main() {
    LRUCache cache(2);
    cache.put(1, 1); cache.put(2, 2);
    cout << "LRU get(1): " << cache.get(1) << endl;
    cache.put(3, 3);
    cout << "LRU get(2): " << cache.get(2) << endl;

    AutoComplete ac;
    for (auto w : {"cat","car","card","care"}) ac.insert(w);
    auto suggestions = ac.suggest("car", 3);
    cout << "Autocomplete 'car': ";
    for (auto& s : suggestions) cout << s << " ";
    cout << endl;
}
