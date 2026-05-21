// Reference Rust driver for tests/cases/reverse_linked_list.json.
// Uses a safe, owned Box-based singly linked list. Reverses iteratively.
use std::io::{self, BufRead};

struct Node { val: i64, next: Option<Box<Node>> }

fn build(arr: &[i64]) -> Option<Box<Node>> {
    let mut head: Option<Box<Node>> = None;
    for &v in arr.iter().rev() { head = Some(Box::new(Node { val: v, next: head })); }
    head
}
fn to_vec(mut head: Option<Box<Node>>) -> Vec<i64> {
    let mut out = Vec::new();
    while let Some(n) = head { out.push(n.val); head = n.next; }
    out
}
fn reverse(mut head: Option<Box<Node>>) -> Option<Box<Node>> {
    let mut prev: Option<Box<Node>> = None;
    while let Some(mut node) = head {
        head = node.next.take();
        node.next = prev;
        prev = Some(node);
    }
    prev
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut arr: Vec<i64> = Vec::new(); let mut expected: Vec<i64> = Vec::new();
    let mut hi = false; let mut he = false; let mut phase = 0;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, arr: &mut Vec<i64>, expected: &mut Vec<i64>,
                 hi: &mut bool, he: &mut bool, phase: &mut i32, p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = to_vec(reverse(build(arr)));
            if got == *expected { println!("PASS reverse_linked_list :: {}", name); *p += 1; }
            else { println!("FAIL reverse_linked_list :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); arr.clear(); expected.clear(); *hi = false; *he = false; *phase = 0;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut arr, &mut expected, &mut hi, &mut he, &mut phase, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); phase = 0; }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                let mut tmp: Vec<i64> = Vec::with_capacity(n);
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { tmp.push(v); } } }
                if phase == 0 { arr = tmp; hi = true; phase = 1; } else { expected = tmp; he = true; }
            }
            _ => {}
        }
    }
    flush(&mut name, &mut arr, &mut expected, &mut hi, &mut he, &mut phase, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
