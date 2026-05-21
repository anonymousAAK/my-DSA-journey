// Reference C++ driver for tests/cases/lru_cache.json.
// Uses std::list + unordered_map for O(1) ops.
#include <iostream>
#include <list>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

class LRU {
    int cap;
    std::list<std::pair<long long, long long>> lst; // front = most recent
    std::unordered_map<long long, std::list<std::pair<long long, long long>>::iterator> map;
public:
    LRU(int c) : cap(c) {}
    long long get(long long k) {
        auto it = map.find(k);
        if (it == map.end()) return -1;
        lst.splice(lst.begin(), lst, it->second);
        return it->second->second;
    }
    void put(long long k, long long v) {
        auto it = map.find(k);
        if (it != map.end()) { it->second->second = v; lst.splice(lst.begin(), lst, it->second); return; }
        lst.push_front({k, v});
        map[k] = lst.begin();
        if ((int)lst.size() > cap) { map.erase(lst.back().first); lst.pop_back(); }
    }
};

int main() {
    std::string line, name;
    int cap = 0;
    int opsRemain = 0; bool inOps = false;
    std::vector<std::tuple<int, long long, long long>> ops; // 0=put 1=get
    std::vector<long long> expected;
    bool hi = false, he = false; int p = 0, f = 0;

    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        LRU c(cap);
        std::vector<long long> out;
        for (auto& [kind, a, b] : ops) {
            if (kind == 0) c.put(a, b);
            else out.push_back(c.get(a));
        }
        if (out == expected) { std::cout << "PASS lru_cache :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL lru_cache :: " << name << "\n"; ++f; }
        name.clear(); ops.clear(); expected.clear(); hi = he = false; inOps = false;
    };

    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; ops.clear(); inOps = false; }
        else if (tag == "CAP") { iss >> cap; }
        else if (tag == "OPS") { iss >> opsRemain; inOps = true; if (opsRemain == 0) { hi = true; inOps = false; } }
        else if (tag == "PUT" && inOps) {
            long long k, v; iss >> k >> v; ops.push_back({0, k, v});
            if (--opsRemain == 0) { hi = true; inOps = false; }
        }
        else if (tag == "GET" && inOps) {
            long long k; iss >> k; ops.push_back({1, k, 0});
            if (--opsRemain == 0) { hi = true; inOps = false; }
        }
        else if (tag == "ARR") {
            std::size_t n; iss >> n;
            expected.clear();
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; expected.push_back(v); }
            he = true;
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
