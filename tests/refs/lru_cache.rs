// Reference Rust driver for tests/cases/lru_cache.json.
// Uses HashMap<key, usize-stamp> + max stamp counter to find LRU on eviction.
// O(capacity) on eviction; acceptable for fixture sizes.
use std::collections::HashMap;
use std::io::{self, BufRead};

struct LRU {
    cap: usize,
    map: HashMap<i64, (i64, u64)>, // key -> (value, last_used)
    clock: u64,
}
impl LRU {
    fn new(cap: usize) -> Self { LRU { cap, map: HashMap::new(), clock: 0 } }
    fn touch(&mut self) -> u64 { self.clock += 1; self.clock }
    fn get(&mut self, k: i64) -> i64 {
        let t = self.touch();
        match self.map.get_mut(&k) {
            None => -1,
            Some(v) => { v.1 = t; v.0 }
        }
    }
    fn put(&mut self, k: i64, v: i64) {
        let t = self.touch();
        if let Some(entry) = self.map.get_mut(&k) { entry.0 = v; entry.1 = t; return; }
        if self.map.len() >= self.cap {
            // Find min stamp
            let oldest = self.map.iter().min_by_key(|(_, val)| val.1).map(|(k, _)| *k);
            if let Some(o) = oldest { self.map.remove(&o); }
        }
        self.map.insert(k, (v, t));
    }
}

#[derive(Clone)]
enum Op { Put(i64, i64), Get(i64) }

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut cap: usize = 0;
    let mut ops: Vec<Op> = Vec::new();
    let mut expected: Vec<i64> = Vec::new();
    let mut ops_remain: usize = 0; let mut in_ops = false;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;

    let flush = |name: &mut String, cap: usize, ops: &mut Vec<Op>, expected: &mut Vec<i64>,
                 hi: &mut bool, he: &mut bool, in_ops: &mut bool, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let mut c = LRU::new(cap);
            let mut out: Vec<i64> = Vec::new();
            for op in ops.iter() {
                match op {
                    Op::Put(k, v) => c.put(*k, *v),
                    Op::Get(k) => out.push(c.get(*k)),
                }
            }
            if out == *expected { println!("PASS lru_cache :: {}", name); *p += 1; }
            else { println!("FAIL lru_cache :: {}\n  expected: {:?}\n  got: {:?}", name, expected, out); *f += 1; }
        }
        name.clear(); ops.clear(); expected.clear(); *hi = false; *he = false; *in_ops = false;
    };

    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, cap, &mut ops, &mut expected, &mut hi, &mut he, &mut in_ops, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); ops.clear(); in_ops = false; }
            "CAP" => { cap = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); }
            "OPS" => {
                ops_remain = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                in_ops = true;
                if ops_remain == 0 { hi = true; in_ops = false; }
            }
            "PUT" if in_ops => {
                let k: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                let v: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                ops.push(Op::Put(k, v));
                ops_remain -= 1;
                if ops_remain == 0 { hi = true; in_ops = false; }
            }
            "GET" if in_ops => {
                let k: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                ops.push(Op::Get(k));
                ops_remain -= 1;
                if ops_remain == 0 { hi = true; in_ops = false; }
            }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                expected.clear();
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { expected.push(v); } } }
                he = true;
            }
            _ => {}
        }
    }
    flush(&mut name, cap, &mut ops, &mut expected, &mut hi, &mut he, &mut in_ops, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
