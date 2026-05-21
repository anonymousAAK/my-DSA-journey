// Reference C++ driver for tests/cases/balanced_parens.json.
#include <iostream>
#include <stack>
#include <string>

bool isBalanced(const std::string& s) {
    std::stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else {
            if (st.empty()) return false;
            char t = st.top(); st.pop();
            if ((c == ')' && t != '(') || (c == ']' && t != '[') || (c == '}' && t != '{')) return false;
        }
    }
    return st.empty();
}

static std::string parseStr(const std::string& line) {
    std::size_t sp = line.find(' ', 4);
    if (sp == std::string::npos) return std::string();
    int len = std::stoi(line.substr(4, sp - 4));
    std::string s = line.substr(sp + 1);
    if ((int)s.size() < len) s += std::string(len - s.size(), ' ');
    else if ((int)s.size() > len) s = s.substr(0, len);
    return s;
}

int main() {
    std::string line, name, s; int expected = 0;
    bool hi = false, he = false; int p = 0, f = 0;
    auto run = [&]() {
        if (name.empty() || !hi || !he) return;
        bool got = isBalanced(s);
        if ((int)got == expected) { std::cout << "PASS balanced_parens :: " << name << "\n"; ++p; }
        else { std::cout << "FAIL balanced_parens :: " << name << "\n  expected: " << expected << "\n  got: " << got << "\n"; ++f; }
        name.clear(); s.clear(); hi = he = false;
    };
    while (std::getline(std::cin, line)) {
        if (line.empty()) { run(); continue; }
        if (line.rfind("CASE ", 0) == 0) name = line.substr(5);
        else if (line.rfind("STR ", 0) == 0) { s = parseStr(line); hi = true; }
        else if (line.rfind("BOOL ", 0) == 0) { expected = std::stoi(line.substr(5)); he = true; }
    }
    run();
    std::cout << "TOTAL: " << p << " passed, " << f << " failed\n";
    return f == 0 ? 0 : 1;
}
