// Reference C++ driver for tests/cases/coin_change.json.
#include <climits>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

int coinChange(const std::vector<long long>& coins, long long amount) {
    const long long INF = LLONG_MAX / 2;
    std::vector<long long> dp(amount + 1, INF);
    dp[0] = 0;
    for (long long a = 1; a <= amount; ++a)
        for (long long c : coins)
            if (c <= a && dp[a - c] + 1 < dp[a]) dp[a] = dp[a - c] + 1;
    return dp[amount] == INF ? -1 : (int)dp[amount];
}

int main() {
    std::string line, name; std::vector<long long> coins;
    long long amount = 0, expected = 0;
    int phase = 0; bool he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || phase < 2 || !he) return;
        long long got = coinChange(coins, amount);
        if (got == expected) { std::cout << "PASS coin_change :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL coin_change :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); coins.clear(); phase = 0; he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        std::istringstream iss(line); std::string tag; iss >> tag;
        if (tag == "CASE") { iss >> name; phase = 0; }
        else if (tag == "ARR") {
            coins.clear(); std::size_t n; iss >> n;
            for (std::size_t i = 0; i < n; ++i) { long long v; iss >> v; coins.push_back(v); }
            phase = 1;
        } else if (tag == "INT") {
            long long v; iss >> v;
            if (phase == 1) { amount = v; phase = 2; } else { expected = v; he = true; }
        }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
