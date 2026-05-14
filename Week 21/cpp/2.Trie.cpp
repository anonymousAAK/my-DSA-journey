/*
 * WEEK 21 - C++ ADVANCED DSA
 * Topic: Trie (Prefix Tree) + Binary Trie for Maximum XOR
 * File: 2.Trie.cpp
 *
 * CONCEPT:
 *   A trie is a multi-way tree where each edge corresponds to a character.
 *   Words sharing a prefix share an initial path. Operations are O(m) for
 *   word length m. A binary trie stores integer bit patterns and computes
 *   the maximum XOR between any pair in O(n * B), B = bit width.
 *
 * KEY POINTS:
 *   - Each node has up to 26 children (lowercase) and an `is_end` flag.
 *   - `word_count` enables fast count-with-prefix queries.
 *   - Delete must clear `is_end` and prune unused branches.
 *   - Binary trie greedy walk: at each bit, prefer the opposite bit
 *     to maximise XOR.
 *
 * ALGORITHM / APPROACH:
 *   insert(word):     walk/extend; mark terminal; bump word_count along path
 *   search(word):     walk; check terminal flag
 *   startsWith(p):    walk only; success if reachable
 *   autocomplete(p):  walk to prefix node; DFS collect all leaves
 *   delete(word):     recursive prune; clear terminal; drop empty children
 *   maxXOR(nums):     build binary trie; for each x, greedily XOR with
 *                     opposite bit when present.
 *
 * C++-SPECIFIC NOTES vs JAVA:
 *   - Use raw owning pointers + manual delete OR std::unique_ptr; here we
 *     keep nodes leaked (program-lifetime) for brevity, mirroring Java.
 *   - `std::array<TrieNode*, 26>` is the C++ analogue of TrieNode[26].
 *   - For binary trie, a flat `std::vector<std::array<int,2>>` avoids
 *     pointer chasing — faster than per-node objects.
 *
 * DRY RUN:
 *   Insert "apple" then "app": both walk a->p->p; "app" terminates at the
 *   second p, "apple" continues l->e and terminates at e.
 *   search("app") -> True (is_end set). search("ap") -> False.
 *   autocomplete("ap") returns every word with "ap" prefix.
 *
 *   maxXOR([3,10,5,25,2,8]):
 *     5-bit numbers (max=25=11001), best pair 5 ^ 25 = 28.
 *
 * COMPLEXITY:
 *   Trie operations: O(m).
 *   maxXOR:          O(n * B), B = bit length of max element.
 */

#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <array>
#include <string>

struct TrieNode {
    std::array<TrieNode*, 26> children{};
    bool is_end = false;
    int word_count = 0;
    TrieNode() { children.fill(nullptr); }
};

struct Trie {
    TrieNode* root = new TrieNode();

    static int idx(char c) { return c - 'a'; }

    void insert(const std::string& word) {
        TrieNode* cur = root;
        for (char c : word) {
            int i = idx(c);
            if (!cur->children[i]) cur->children[i] = new TrieNode();
            cur = cur->children[i];
            cur->word_count++;
        }
        cur->is_end = true;
    }

    bool search(const std::string& word) const {
        TrieNode* cur = root;
        for (char c : word) {
            int i = idx(c);
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return cur->is_end;
    }

    bool starts_with(const std::string& prefix) const {
        TrieNode* cur = root;
        for (char c : prefix) {
            int i = idx(c);
            if (!cur->children[i]) return false;
            cur = cur->children[i];
        }
        return true;
    }

    int count_with_prefix(const std::string& prefix) const {
        TrieNode* cur = root;
        for (char c : prefix) {
            int i = idx(c);
            if (!cur->children[i]) return 0;
            cur = cur->children[i];
        }
        return cur->word_count;
    }

    std::vector<std::string> autocomplete(const std::string& prefix) const {
        std::vector<std::string> out;
        TrieNode* cur = root;
        for (char c : prefix) {
            int i = idx(c);
            if (!cur->children[i]) return out;
            cur = cur->children[i];
        }
        std::string buf = prefix;
        dfs_collect(cur, buf, out);
        return out;
    }

    void dfs_collect(TrieNode* node, std::string& buf, std::vector<std::string>& out) const {
        if (node->is_end) out.push_back(buf);
        for (int i = 0; i < 26; ++i) {
            if (node->children[i]) {
                buf.push_back(char('a' + i));
                dfs_collect(node->children[i], buf, out);
                buf.pop_back();
            }
        }
    }

    bool del(const std::string& word) { return del_helper(root, word, 0); }

    bool del_helper(TrieNode* node, const std::string& word, int i) {
        if (i == (int)word.size()) {
            if (!node->is_end) return false;
            node->is_end = false;
            return true;
        }
        int k = idx(word[i]);
        if (!node->children[k]) return false;
        bool deleted = del_helper(node->children[k], word, i + 1);
        if (deleted) {
            node->children[k]->word_count--;
            bool any_child = false;
            for (auto* c : node->children[k]->children) if (c) { any_child = true; break; }
            if (!any_child && node->children[k]->word_count == 0) {
                delete node->children[k];
                node->children[k] = nullptr;
            }
        }
        return deleted;
    }
};

int max_xor(const std::vector<int>& nums) {
    int mx = 0;
    for (int x : nums) mx = std::max(mx, x);
    int bits = 0; while ((1 << bits) <= mx) bits++;
    if (bits == 0) bits = 1;

    std::vector<std::array<int, 2>> trie(1, {0, 0});
    for (int x : nums) {
        int node = 0;
        for (int b = bits - 1; b >= 0; --b) {
            int bit = (x >> b) & 1;
            if (trie[node][bit] == 0) {
                trie.push_back({0, 0});
                trie[node][bit] = (int)trie.size() - 1;
            }
            node = trie[node][bit];
        }
    }

    int best = 0;
    for (int x : nums) {
        int node = 0, cur = 0;
        for (int b = bits - 1; b >= 0; --b) {
            int bit = (x >> b) & 1;
            int want = 1 - bit;
            if (trie[node][want] != 0) { cur |= (1 << b); node = trie[node][want]; }
            else node = trie[node][bit];
        }
        best = std::max(best, cur);
    }
    return best;
}

int main() {
    Trie trie;
    for (auto& w : std::vector<std::string>{"apple","app","application","apply","apt","banana","band"})
        trie.insert(w);

    std::cout << std::boolalpha;
    std::cout << "=== Trie ===\n";
    std::cout << "search('apple')     : " << trie.search("apple") << "\n";
    std::cout << "search('app')       : " << trie.search("app") << "\n";
    std::cout << "search('ap')        : " << trie.search("ap") << "\n";
    std::cout << "starts_with('app')  : " << trie.starts_with("app") << "\n";
    std::cout << "starts_with('xyz')  : " << trie.starts_with("xyz") << "\n";

    std::cout << "\nautocomplete('app'): ";
    for (auto& w : trie.autocomplete("app")) std::cout << w << " ";
    std::cout << "\nautocomplete('ban'): ";
    for (auto& w : trie.autocomplete("ban")) std::cout << w << " ";
    std::cout << "\nautocomplete('z')  : ";
    for (auto& w : trie.autocomplete("z")) std::cout << w << " ";
    std::cout << "\n";

    trie.del("app");
    std::cout << "\nAfter deleting 'app':\n";
    std::cout << "search('app')   : " << trie.search("app")   << "\n";
    std::cout << "search('apple') : " << trie.search("apple") << "\n";

    std::cout << "\n=== Maximum XOR ===\n";
    std::cout << "max_xor([3,10,5,25,2,8]) = " << max_xor({3,10,5,25,2,8}) << "\n"; // 28
    std::cout << "max_xor([0,1,2])         = " << max_xor({0,1,2})         << "\n"; // 3
    return 0;
}
