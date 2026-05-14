# Week 28: Game Theory & Combinatorics
# Nim, Sprague-Grundy, Pascal's Triangle, Catalan, Matrix Exponentiation

# === Nim Game ===
# Time: O(n), Space: O(1)
def nim_winner(piles):
    xor = 0
    for p in piles:
        xor ^= p
    return "First" if xor != 0 else "Second"

# === Sprague-Grundy ===
# Time: O(n * |moves|), Space: O(n)
def grundy(n, moves):
    g = [0] * (n + 1)
    for i in range(1, n + 1):
        reachable = set()
        for m in moves:
            if i >= m:
                reachable.add(g[i - m])
        mex = 0
        while mex in reachable:
            mex += 1
        g[i] = mex
    return g[n]

# === Pascal's Triangle / nCr ===
# Time: O(n^2), Space: O(n^2)
def build_pascal(n):
    C = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i-1][j-1] + C[i-1][j]
    return C

# === Catalan Numbers ===
# Time: O(n), Space: O(1) using binomial formula
def catalan(n):
    if n <= 1:
        return 1
    result = 1
    for i in range(n):
        result = result * (2 * n - i) // (i + 1)
    return result // (n + 1)

# === Matrix Exponentiation for Fibonacci ===
# Time: O(k^3 * log n), Space: O(k^2)
def mat_mult(A, B, mod=10**9+7):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def mat_pow(M, p, mod=10**9+7):
    n = len(M)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    while p > 0:
        if p & 1:
            result = mat_mult(result, M, mod)
        M = mat_mult(M, M, mod)
        p >>= 1
    return result

def fibonacci(n, mod=10**9+7):
    if n <= 1:
        return n
    M = [[1, 1], [1, 0]]
    result = mat_pow(M, n - 1, mod)
    return result[0][0]

if __name__ == "__main__":
    print(f"Nim [3,4,5]: {nim_winner([3,4,5])}")
    print(f"Grundy(10, moves=[1,3,4]): {grundy(10, [1,3,4])}")
    C = build_pascal(10)
    print(f"C(10,3) = {C[10][3]}")
    print(f"Catalan(5) = {catalan(5)}")
    print(f"Fibonacci(10) = {fibonacci(10)}")
