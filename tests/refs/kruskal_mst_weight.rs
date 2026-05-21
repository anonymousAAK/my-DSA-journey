// Reference Rust driver for tests/cases/kruskal_mst_weight.json.
use std::io::{self, BufRead};

struct DSU { p: Vec<usize>, r: Vec<i32> }
impl DSU {
    fn new(n: usize) -> Self { DSU { p: (0..n).collect(), r: vec![0; n] } }
    fn find(&mut self, mut x: usize) -> usize {
        while self.p[x] != x { self.p[x] = self.p[self.p[x]]; x = self.p[x]; }
        x
    }
    fn unite(&mut self, a: usize, b: usize) -> bool {
        let (mut a, mut b) = (self.find(a), self.find(b));
        if a == b { return false; }
        if self.r[a] < self.r[b] { std::mem::swap(&mut a, &mut b); }
        self.p[b] = a;
        if self.r[a] == self.r[b] { self.r[a] += 1; }
        true
    }
}

fn kruskal(v: usize, mut edges: Vec<(i32, i32, i64)>) -> i64 {
    edges.sort_by_key(|e| e.2);
    let mut d = DSU::new(v);
    let mut total = 0i64; let mut used = 0usize;
    for (u, w, ww) in edges {
        if d.unite(u as usize, w as usize) {
            total += ww;
            used += 1;
            if used == v.saturating_sub(1) { break; }
        }
    }
    total
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut v_in: usize = 0;
    let mut edges: Vec<(i32, i32, i64)> = Vec::new();
    let mut edges_remain: usize = 0; let mut in_edges = false;
    let mut expected: i64 = 0;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, v_in: usize, edges: &mut Vec<(i32, i32, i64)>, expected: i64,
                 hi: &mut bool, he: &mut bool, in_edges: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = kruskal(v_in, edges.clone());
            if got == expected { println!("PASS kruskal_mst_weight :: {}", name); *p += 1; }
            else { println!("FAIL kruskal_mst_weight :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); edges.clear(); *hi = false; *he = false; *in_edges = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, v_in, &mut edges, expected, &mut hi, &mut he, &mut in_edges, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); }
            "V" => { v_in = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); }
            "EDGES" => {
                edges_remain = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                in_edges = true; edges.clear();
                if edges_remain == 0 { hi = true; in_edges = false; }
            }
            "INT" => { expected = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); he = true; }
            _ => {
                if in_edges {
                    let u: i32 = tag.parse().unwrap_or(0);
                    let w: i32 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                    let ww: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                    edges.push((u, w, ww));
                    edges_remain -= 1;
                    if edges_remain == 0 { hi = true; in_edges = false; }
                }
            }
        }
    }
    flush(&mut name, v_in, &mut edges, expected, &mut hi, &mut he, &mut in_edges, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
