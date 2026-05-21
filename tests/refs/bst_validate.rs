// Reference Rust driver for tests/cases/bst_validate.json.
use std::collections::VecDeque;
use std::io::{self, BufRead};

struct Node { val: i64, l: Option<Box<Node>>, r: Option<Box<Node>> }

fn build(v: &[Option<i64>]) -> Option<Box<Node>> {
    if v.is_empty() || v[0].is_none() { return None; }
    let mut root = Box::new(Node { val: v[0].unwrap(), l: None, r: None });
    // Use raw pointers via Vec of references for assignment
    let mut queue: VecDeque<*mut Node> = VecDeque::new();
    queue.push_back(&mut *root as *mut Node);
    let mut i = 1usize;
    while let Some(node_ptr) = queue.pop_front() {
        if i >= v.len() { break; }
        if let Some(vl) = v[i] {
            let n = Box::new(Node { val: vl, l: None, r: None });
            unsafe { (*node_ptr).l = Some(n); }
            unsafe { queue.push_back(&mut **(*node_ptr).l.as_mut().unwrap() as *mut Node); }
        }
        i += 1;
        if i >= v.len() { break; }
        if let Some(vr) = v[i] {
            let n = Box::new(Node { val: vr, l: None, r: None });
            unsafe { (*node_ptr).r = Some(n); }
            unsafe { queue.push_back(&mut **(*node_ptr).r.as_mut().unwrap() as *mut Node); }
        }
        i += 1;
    }
    Some(root)
}

fn check(n: &Option<Box<Node>>, lo: Option<i64>, hi: Option<i64>) -> bool {
    match n {
        None => true,
        Some(b) => {
            if let Some(l) = lo { if !(l < b.val) { return false; } }
            if let Some(h) = hi { if !(b.val < h) { return false; } }
            check(&b.l, lo, Some(b.val)) && check(&b.r, Some(b.val), hi)
        }
    }
}

fn is_valid_bst(v: &[Option<i64>]) -> bool {
    let r = build(v);
    check(&r, None, None)
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut vals: Vec<Option<i64>> = Vec::new();
    let mut tree_len: usize = 0; let mut tree_read: usize = 0; let mut in_tree = false;
    let mut expected = 0i32;
    let mut hi = false; let mut he = false;
    let mut p = 0u32; let mut f = 0u32;
    let flush = |name: &mut String, vals: &mut Vec<Option<i64>>, expected: i32,
                 hi: &mut bool, he: &mut bool, in_tree: &mut bool, tree_read: &mut usize,
                 p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hi && *he {
            let got = is_valid_bst(vals);
            if (got as i32) == expected { println!("PASS bst_validate :: {}", name); *p += 1; }
            else { println!("FAIL bst_validate :: {}\n  expected: {}\n  got: {}", name, expected, got); *f += 1; }
        }
        name.clear(); vals.clear(); *hi = false; *he = false; *in_tree = false; *tree_read = 0;
    };
    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() { flush(&mut name, &mut vals, expected, &mut hi, &mut he, &mut in_tree, &mut tree_read, &mut p, &mut f); continue; }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); }
            "TREE" => {
                tree_len = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                vals.clear(); in_tree = true; tree_read = 0;
                if tree_len == 0 { hi = true; in_tree = false; }
            }
            "NULL" if in_tree => {
                vals.push(None); tree_read += 1;
                if tree_read == tree_len { hi = true; in_tree = false; }
            }
            "VAL" if in_tree => {
                let v: i64 = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                vals.push(Some(v)); tree_read += 1;
                if tree_read == tree_len { hi = true; in_tree = false; }
            }
            "BOOL" => { expected = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0); he = true; }
            _ => {}
        }
    }
    flush(&mut name, &mut vals, expected, &mut hi, &mut he, &mut in_tree, &mut tree_read, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
