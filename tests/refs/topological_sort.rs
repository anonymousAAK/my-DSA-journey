// Reference Rust driver for tests/cases/topological_sort.json.
use std::collections::BinaryHeap;
use std::cmp::Reverse;
use std::io::{self, BufRead};

fn topo_sort(v: usize, edges: &[(i32, i32)]) -> Option<Vec<i32>> {
    let mut adj: Vec<Vec<i32>> = vec![Vec::new(); v];
    let mut indeg: Vec<i32> = vec![0; v];
    for &(u, w) in edges { adj[u as usize].push(w); indeg[w as usize] += 1; }
    let mut pq: BinaryHeap<Reverse<i32>> = BinaryHeap::new();
    for i in 0..v as i32 { if indeg[i as usize] == 0 { pq.push(Reverse(i)); } }
    let mut out: Vec<i32> = Vec::new();
    while let Some(Reverse(u)) = pq.pop() {
        out.push(u);
        for &x in &adj[u as usize] {
            indeg[x as usize] -= 1;
            if indeg[x as usize] == 0 { pq.push(Reverse(x)); }
        }
    }
    if out.len() == v { Some(out) } else { None }
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut v_in: usize = 0;
    let mut edges: Vec<(i32, i32)> = Vec::new();
    let mut edges_remain: usize = 0; let mut in_edges = false;
    let mut expected: Vec<i32> = Vec::new();
    let mut expected_none = false;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;

    let flush = |name: &mut String, v_in: usize, edges: &mut Vec<(i32, i32)>, expected: &mut Vec<i32>,
                 expected_none: &mut bool, hi: &mut bool, he: &mut bool, in_edges: &mut bool,
                 p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = topo_sort(v_in, edges);
            let pass = if *expected_none { got.is_none() } else { got.as_ref() == Some(expected) };
            if pass { println!("PASS topological_sort :: {}", name); *p += 1; }
            else { println!("FAIL topological_sort :: {}\n  expected: {:?}\n  got: {:?}", name,
                if *expected_none { "None".to_string() } else { format!("{:?}", expected) }, got); *f += 1; }
        }
        name.clear(); edges.clear(); expected.clear();
        *expected_none = false; *hi = false; *he = false; *in_edges = false;
    };

    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, v_in, &mut edges, &mut expected, &mut expected_none, &mut hi, &mut he, &mut in_edges, &mut p, &mut f); continue; }
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
            "EXPECTED_NONE" => { expected_none = true; he = true; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                expected.clear();
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i32>() { expected.push(v); } } }
                he = true;
            }
            _ => {
                if in_edges {
                    let u: i32 = tag.parse().unwrap_or(0);
                    let w: i32 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                    edges.push((u, w));
                    edges_remain -= 1;
                    if edges_remain == 0 { hi = true; in_edges = false; }
                }
            }
        }
    }
    flush(&mut name, v_in, &mut edges, &mut expected, &mut expected_none, &mut hi, &mut he, &mut in_edges, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
