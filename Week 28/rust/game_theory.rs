// Week 28: Game Theory & Combinatorics
use std::collections::HashSet;

const MOD: u64 = 1_000_000_007;

// Nim Game
fn nim_winner(piles: &[u32]) -> &str {
    let xor: u32 = piles.iter().fold(0, |acc, &x| acc ^ x);
    if xor != 0 { "First" } else { "Second" }
}

// Sprague-Grundy
fn grundy(n: usize, moves: &[usize]) -> usize {
    let mut g = vec![0usize; n + 1];
    for i in 1..=n {
        let reach: HashSet<usize> = moves.iter()
            .filter(|&&m| i >= m)
            .map(|&m| g[i - m])
            .collect();
        let mut mex = 0;
        while reach.contains(&mex) { mex += 1; }
        g[i] = mex;
    }
    g[n]
}

// Pascal's Triangle
fn build_pascal(n: usize) -> Vec<Vec<u64>> {
    let mut c = vec![vec![0u64; n+1]; n+1];
    for i in 0..=n {
        c[i][0] = 1;
        for j in 1..=i { c[i][j] = c[i-1][j-1] + c[i-1][j]; }
    }
    c
}

// Catalan Number
fn catalan(n: u64) -> u64 {
    let mut result: u64 = 1;
    for i in 0..n {
        result = result * (2 * n - i) / (i + 1);
    }
    result / (n + 1)
}

// Matrix Exponentiation for Fibonacci
fn mat_mult(a: &Vec<Vec<u64>>, b: &Vec<Vec<u64>>) -> Vec<Vec<u64>> {
    let n = a.len();
    let mut c = vec![vec![0u64; n]; n];
    for i in 0..n {
        for j in 0..n {
            for k in 0..n {
                c[i][j] = (c[i][j] + a[i][k] * b[k][j]) % MOD;
            }
        }
    }
    c
}

fn fibonacci(n: u64) -> u64 {
    if n <= 1 { return n; }
    let mut m = vec![vec![1u64, 1], vec![1, 0]];
    let mut result = vec![vec![1u64, 0], vec![0, 1]];
    let mut p = n - 1;
    while p > 0 {
        if p & 1 == 1 { result = mat_mult(&result, &m); }
        m = mat_mult(&m, &m);
        p >>= 1;
    }
    result[0][0]
}

fn main() {
    println!("Nim [3,4,5]: {}", nim_winner(&[3,4,5]));
    println!("Grundy(10, [1,3,4]): {}", grundy(10, &[1,3,4]));
    let c = build_pascal(10);
    println!("C(10,3) = {}", c[10][3]);
    println!("Catalan(5) = {}", catalan(5));
    println!("Fibonacci(10) = {}", fibonacci(10));
}
