// Reference Rust driver for tests/cases/spiral_traversal.json.
use std::io::{self, BufRead};

fn spiral_order(m: &[Vec<i64>]) -> Vec<i64> {
    let mut out = Vec::new();
    if m.is_empty() || m[0].is_empty() { return out; }
    let (mut top, mut bot) = (0i32, m.len() as i32 - 1);
    let (mut lo, mut hi) = (0i32, m[0].len() as i32 - 1);
    while top <= bot && lo <= hi {
        for c in lo..=hi { out.push(m[top as usize][c as usize]); } top += 1;
        for r in top..=bot { out.push(m[r as usize][hi as usize]); } hi -= 1;
        if top <= bot { for c in (lo..=hi).rev() { out.push(m[bot as usize][c as usize]); } bot -= 1; }
        if lo <= hi { for r in (top..=bot).rev() { out.push(m[r as usize][lo as usize]); } lo += 1; }
    }
    out
}

fn main() {
    let stdin = io::stdin();
    let mut name = String::new();
    let mut mat: Vec<Vec<i64>> = Vec::new();
    let mut expected: Vec<i64> = Vec::new();
    let mut hm = false; let mut he = false; let mut in_mat = false;
    let mut rows: usize = 0; let mut _cols: usize = 0; let mut rows_read: usize = 0;
    let mut p = 0u32; let mut f = 0u32;

    let mut buf: Vec<String> = Vec::new();
    for line in stdin.lock().lines() { buf.push(line.unwrap_or_default()); }

    let mut flush = |name: &mut String, mat: &mut Vec<Vec<i64>>, expected: &mut Vec<i64>,
                     hm: &mut bool, he: &mut bool, in_mat: &mut bool, rows_read: &mut usize,
                     p: &mut u32, f: &mut u32| {
        if !name.is_empty() && *hm && *he {
            let got = spiral_order(mat);
            if got == *expected { println!("PASS spiral_traversal :: {}", name); *p += 1; }
            else { println!("FAIL spiral_traversal :: {}\n  expected: {:?}\n  got: {:?}", name, expected, got); *f += 1; }
        }
        name.clear(); mat.clear(); expected.clear();
        *hm = false; *he = false; *in_mat = false; *rows_read = 0;
    };

    for line in buf {
        if line.is_empty() {
            flush(&mut name, &mut mat, &mut expected, &mut hm, &mut he, &mut in_mat, &mut rows_read, &mut p, &mut f);
            continue;
        }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => { name = parts.next().unwrap_or("").to_string(); }
            "MAT" => {
                rows = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                _cols = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                mat.clear(); in_mat = true; rows_read = 0;
                if rows == 0 { hm = true; in_mat = false; }
            }
            "ARR" => {
                let n: usize = parts.next().and_then(|s| s.parse().ok()).unwrap_or(0);
                expected.clear();
                for _ in 0..n { if let Some(t) = parts.next() { if let Ok(v) = t.parse::<i64>() { expected.push(v); } } }
                he = true;
            }
            _ => {
                if in_mat {
                    let mut row: Vec<i64> = Vec::new();
                    row.push(tag.parse().unwrap_or(0));
                    for t in parts { row.push(t.parse().unwrap_or(0)); }
                    mat.push(row);
                    rows_read += 1;
                    if rows_read == rows { hm = true; in_mat = false; }
                }
            }
        }
    }
    flush(&mut name, &mut mat, &mut expected, &mut hm, &mut he, &mut in_mat, &mut rows_read, &mut p, &mut f);
    println!("TOTAL: {} passed, {} failed", p, f);
    std::process::exit(if f == 0 { 0 } else { 1 });
}
