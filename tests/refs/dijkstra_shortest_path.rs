// Reference Rust driver for tests/cases/dijkstra_shortest_path.json.
use std::collections::BinaryHeap;
use std::cmp::Reverse;
use std::io::{self, BufRead};

fn dijkstra(v: usize, edges: &[(i32, i32, i64)], src: usize) -> Vec<i64> {
    let mut adj: Vec<Vec<(usize, i64)>> = vec![Vec::new(); v];
    for &(u, w, ww) in edges {
        adj[u as usize].push((w as usize, ww));
        adj[w as usize].push((u as usize, ww));
    }
    let inf = i64::MAX / 2;
    let mut dist = vec![inf; v];
    dist[src] = 0;
    let mut pq: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    pq.push(Reverse((0, src)));
    while let Some(Reverse((d, u))) = pq.pop() {
        if d > dist[u] { continue; }
        for &(x, ww) in &adj[u] {
            let nd = d + ww;
            if nd < dist[x] { dist[x] = nd; pq.push(Reverse((nd, x))); }
        }
    }
    dist.iter().map(|&d| if d == inf { -1 } else { d }).collect()
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut v_in: usize = 0; let mut src: usize = 0;
    let mut edges: Vec<(i32, i32, i64)> = Vec::new();
    let mut edges_remain: usize = 0; let mut in_edges = false;
    let mut expected: Vec<i64> = Vec::new();
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, v_in: usize, edges: &mut Vec<(i32, i32, i64)>, src: usize, expected: &mut Vec<i64>,
                 hi: &mut bool, he: &mut bool, in_edges: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = dijkstra(v_in, edges, src);
            if got == *expected { println!("PASS dijkstra_shortest_path :: {}", name); *p += 1; }
            else { println!("FAIL dijkstra_shortest_path :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); edges.clear(); expected.clear();
        *hi = false; *he = false; *in_edges = false;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, v_in, &mut edges, src, &mut expected, &mut hi, &mut he, &mut in_edges, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); }
            "V" => { v_in = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); }
            "EDGES" => {
                edges_remain = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                in_edges = true; edges.clear();
                if edges_remain == 0 { in_edges = false; }
            }
            "SRC" => { src = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); hi = true; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                expected.clear();
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { expected.push(v); } } }
                he = true;
            }
            _ => {
                if in_edges {
                    let u: i32 = tag.parse().unwrap_or(0);
                    let w: i32 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                    let ww: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                    edges.push((u, w, ww));
                    edges_remain -= 1;
                    if edges_remain == 0 { in_edges = false; }
                }
            }
        }
    }
    flush(&mut name, v_in, &mut edges, src, &mut expected, &mut hi, &mut he, &mut in_edges, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
