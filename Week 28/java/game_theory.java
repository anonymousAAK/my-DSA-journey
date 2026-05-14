// Week 28: Game Theory & Combinatorics
// Nim O(n), Sprague-Grundy, Pascal's Triangle, Catalan, Matrix Exponentiation

import java.util.*;

public class game_theory {

    // Nim Game - XOR all pile sizes
    static String nimWinner(int[] piles) {
        int xor = 0;
        for (int p : piles) xor ^= p;
        return xor != 0 ? "First" : "Second";
    }

    // Sprague-Grundy - compute Grundy number
    static int grundy(int n, int[] moves) {
        int[] g = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            Set<Integer> reachable = new HashSet<>();
            for (int m : moves)
                if (i >= m) reachable.add(g[i - m]);
            int mex = 0;
            while (reachable.contains(mex)) mex++;
            g[i] = mex;
        }
        return g[n];
    }

    // Pascal's Triangle
    static long[][] buildPascal(int n) {
        long[][] C = new long[n+1][n+1];
        for (int i = 0; i <= n; i++) {
            C[i][0] = 1;
            for (int j = 1; j <= i; j++)
                C[i][j] = C[i-1][j-1] + C[i-1][j];
        }
        return C;
    }

    // Catalan Number using binomial formula
    static long catalan(int n) {
        long result = 1;
        for (int i = 0; i < n; i++)
            result = result * (2 * n - i) / (i + 1);
        return result / (n + 1);
    }

    // Matrix Exponentiation for Fibonacci
    static long MOD = 1_000_000_007;

    static long[][] matMult(long[][] A, long[][] B) {
        int n = A.length;
        long[][] C = new long[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < n; k++)
                    C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD;
        return C;
    }

    static long[][] matPow(long[][] M, long p) {
        int n = M.length;
        long[][] result = new long[n][n];
        for (int i = 0; i < n; i++) result[i][i] = 1;
        while (p > 0) {
            if ((p & 1) == 1) result = matMult(result, M);
            M = matMult(M, M);
            p >>= 1;
        }
        return result;
    }

    static long fibonacci(int n) {
        if (n <= 1) return n;
        long[][] M = {{1, 1}, {1, 0}};
        return matPow(M, n - 1)[0][0];
    }

    public static void main(String[] args) {
        System.out.println("Nim [3,4,5]: " + nimWinner(new int[]{3,4,5}));
        System.out.println("Grundy(10, [1,3,4]): " + grundy(10, new int[]{1,3,4}));
        long[][] C = buildPascal(10);
        System.out.println("C(10,3) = " + C[10][3]);
        System.out.println("Catalan(5) = " + catalan(5));
        System.out.println("Fibonacci(10) = " + fibonacci(10));
    }
}
