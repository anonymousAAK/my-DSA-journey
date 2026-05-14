// Week 28: Game Theory & Combinatorics
#include <iostream>
#include <vector>
#include <set>
using namespace std;

// Nim Game
string nimWinner(vector<int>& piles) {
    int x = 0;
    for (int p : piles) x ^= p;
    return x ? "First" : "Second";
}

// Sprague-Grundy
int grundy(int n, vector<int>& moves) {
    vector<int> g(n+1, 0);
    for (int i = 1; i <= n; i++) {
        set<int> reach;
        for (int m : moves)
            if (i >= m) reach.insert(g[i-m]);
        int mex = 0;
        while (reach.count(mex)) mex++;
        g[i] = mex;
    }
    return g[n];
}

// Pascal's Triangle
vector<vector<long long>> buildPascal(int n) {
    vector<vector<long long>> C(n+1, vector<long long>(n+1, 0));
    for (int i = 0; i <= n; i++) {
        C[i][0] = 1;
        for (int j = 1; j <= i; j++)
            C[i][j] = C[i-1][j-1] + C[i-1][j];
    }
    return C;
}

// Catalan Number
long long catalan(int n) {
    long long result = 1;
    for (int i = 0; i < n; i++)
        result = result * (2*n - i) / (i + 1);
    return result / (n + 1);
}

// Matrix Exponentiation
const long long MOD = 1e9 + 7;
typedef vector<vector<long long>> Matrix;

Matrix matMult(Matrix& A, Matrix& B) {
    int n = A.size();
    Matrix C(n, vector<long long>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            for (int k = 0; k < n; k++)
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
    return C;
}

long long fibonacci(int n) {
    if (n <= 1) return n;
    Matrix M = {{1,1},{1,0}};
    Matrix result = {{1,0},{0,1}};
    int p = n - 1;
    while (p > 0) {
        if (p & 1) result = matMult(result, M);
        M = matMult(M, M);
        p >>= 1;
    }
    return result[0][0];
}

int main() {
    vector<int> piles = {3,4,5};
    cout << "Nim [3,4,5]: " << nimWinner(piles) << endl;
    vector<int> moves = {1,3,4};
    cout << "Grundy(10): " << grundy(10, moves) << endl;
    auto C = buildPascal(10);
    cout << "C(10,3) = " << C[10][3] << endl;
    cout << "Catalan(5) = " << catalan(5) << endl;
    cout << "Fibonacci(10) = " << fibonacci(10) << endl;
}
