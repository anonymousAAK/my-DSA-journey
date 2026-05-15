// Reference Rust implementation for tests/cases/kadane_max_subarray.json.
//
// The companion shell (tests/harness/harness_rust.sh) compiles this file
// directly with rustc — no Cargo, no serde, no third-party deps. The harness
// preprocesses cases.json into a simple line-based format on stdin:
//
//     CASE <case_name>
//     INPUT <space-separated ints>
//     EXPECTED <int>
//     <blank line>
//
// To add a new topic, copy this file, swap the function under test, and add
// an entry in the topic dispatch table in tests/harness/harness_rust.sh.

use std::io::{self, BufRead};

fn max_subarray_sum(arr: &[i64]) -> i64 {
    if arr.is_empty() {
        return 0;
    }
    let mut best = arr[0];
    let mut current = arr[0];
    for &x in &arr[1..] {
        current = std::cmp::max(x, current + x);
        best = std::cmp::max(best, current);
    }
    best
}

fn main() {
    let stdin = io::stdin();
    let mut case_name = String::new();
    let mut input: Vec<i64> = Vec::new();
    let mut expected: i64 = 0;
    let mut have_input = false;
    let mut have_expected = false;

    let mut passed = 0u32;
    let mut failed = 0u32;

    let mut run_case = |name: &mut String,
                        input: &mut Vec<i64>,
                        expected: &mut i64,
                        have_input: &mut bool,
                        have_expected: &mut bool,
                        passed: &mut u32,
                        failed: &mut u32| {
        if !name.is_empty() && *have_input && *have_expected {
            let got = max_subarray_sum(input);
            if got == *expected {
                println!("PASS kadane_max_subarray :: {}", name);
                *passed += 1;
            } else {
                println!("FAIL kadane_max_subarray :: {}", name);
                println!("  expected: {}", *expected);
                println!("  got: {}", got);
                *failed += 1;
            }
        }
        name.clear();
        input.clear();
        *have_input = false;
        *have_expected = false;
    };

    for line in stdin.lock().lines() {
        let line = line.unwrap_or_default();
        if line.is_empty() {
            run_case(&mut case_name, &mut input, &mut expected,
                     &mut have_input, &mut have_expected, &mut passed, &mut failed);
            continue;
        }
        let mut parts = line.split_whitespace();
        let tag = parts.next().unwrap_or("");
        match tag {
            "CASE" => {
                if let Some(n) = parts.next() {
                    case_name = n.to_string();
                }
            }
            "INPUT" => {
                input.clear();
                for tok in parts {
                    if let Ok(v) = tok.parse::<i64>() {
                        input.push(v);
                    }
                }
                have_input = true;
            }
            "EXPECTED" => {
                if let Some(tok) = parts.next() {
                    if let Ok(v) = tok.parse::<i64>() {
                        expected = v;
                        have_expected = true;
                    }
                }
            }
            _ => {}
        }
    }
    run_case(&mut case_name, &mut input, &mut expected,
             &mut have_input, &mut have_expected, &mut passed, &mut failed);

    println!("TOTAL: {} passed, {} failed", passed, failed);
    std::process::exit(if failed == 0 { 0 } else { 1 });
}

// TODO: add more topics with a parallel structure: one Rust source per topic
// under tests/refs/, each consuming the same CASE/INPUT/EXPECTED line format.
// See tests/README.md for the full extension recipe.
