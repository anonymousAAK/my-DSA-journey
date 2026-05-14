/*
 * WEEK 12 - RUST DSA
 * Topic: Stack Implementation + Classic Problems
 * File: 1.StackImplementation.rs
 *
 * CONCEPT:
 *   LIFO container. Vec<T> in Rust is a growable array; push and pop are
 *   amortized O(1) — exactly the stack interface.
 *
 * KEY POINTS:
 *   - ArrayStack<T>: capped wrapper around Vec<T>.
 *   - MinStack: parallel Vec<i32> tracking running minimums.
 *   - Classic problems: balanced parens, next-greater, postfix.
 *
 * ALGORITHM / APPROACH:
 *   Same algorithms as Java/Python/C++. Differences are syntactic.
 *
 * RUST-SPECIFIC NOTES:
 *   - Vec<T>::push / Vec<T>::pop are the canonical stack operations.
 *   - pop returns Option<T> (None on empty) — no exceptions.
 *   - We use generics (`<T: Copy>` to keep `peek` simple).
 *   - For balanced-paren we use a Vec<char>; .chars() yields Unicode scalar
 *     values (i.e. proper code points, not bytes).
 *   - Postfix uses i32 and Rust's normal integer division (truncates toward
 *     zero, like Java/C++).
 *
 * DRY RUN:
 *   Same examples as Java file (omitted for brevity but identical).
 *
 * COMPLEXITY:
 *   push/pop/peek O(1); next-greater & postfix O(n).
 */

use std::collections::VecDeque;

// ---------- Generic capacity-bounded stack ----------

pub struct ArrayStack<T: Copy> {
    cap: usize,
    data: Vec<T>,
}

impl<T: Copy> ArrayStack<T> {
    pub fn new(capacity: usize) -> Self { Self { cap: capacity, data: Vec::with_capacity(capacity) } }

    pub fn push(&mut self, x: T) -> Result<(), &'static str> {
        if self.data.len() == self.cap { return Err("Stack overflow"); }
        self.data.push(x);
        Ok(())
    }

    pub fn pop(&mut self) -> Result<T, &'static str> {
        self.data.pop().ok_or("Stack underflow")
    }

    pub fn peek(&self) -> Result<T, &'static str> {
        self.data.last().copied().ok_or("Stack is empty")
    }

    pub fn is_empty(&self) -> bool { self.data.is_empty() }
    pub fn len(&self) -> usize { self.data.len() }
}

// ---------- MinStack ----------

pub struct MinStack {
    s: Vec<i32>,
    m: Vec<i32>,  // running minimums
}

impl MinStack {
    pub fn new() -> Self { Self { s: Vec::new(), m: Vec::new() } }

    pub fn push(&mut self, x: i32) {
        self.s.push(x);
        let new_min = match self.m.last() {
            Some(&cur) => cur.min(x),
            None => x,
        };
        self.m.push(new_min);
    }

    pub fn pop(&mut self) -> Option<i32> { self.m.pop(); self.s.pop() }
    pub fn peek(&self) -> Option<i32> { self.s.last().copied() }
    pub fn get_min(&self) -> Option<i32> { self.m.last().copied() }
}

// ---------- Classic problems ----------

pub fn is_balanced(s: &str) -> bool {
    let mut st: Vec<char> = Vec::new();
    for c in s.chars() {
        match c {
            '(' | '[' | '{' => st.push(c),
            ')' | ']' | '}' => {
                let want = match c { ')' => '(', ']' => '[', _ => '{' };
                match st.pop() {
                    Some(top) if top == want => {}
                    _ => return false,
                }
            }
            _ => {}  // ignore other chars
        }
    }
    st.is_empty()
}

pub fn next_greater_element(arr: &[i32]) -> Vec<i32> {
    let n = arr.len();
    let mut result = vec![-1; n];
    let mut st: VecDeque<usize> = VecDeque::new();  // indices, strictly decreasing
    for i in 0..n {
        while let Some(&top) = st.back() {
            if arr[i] > arr[top] {
                result[top] = arr[i];
                st.pop_back();
            } else { break; }
        }
        st.push_back(i);
    }
    result
}

pub fn eval_postfix(expr: &str) -> i32 {
    let mut st: Vec<i32> = Vec::new();
    for tok in expr.split_whitespace() {
        match tok {
            "+" | "-" | "*" | "/" => {
                let b = st.pop().unwrap();
                let a = st.pop().unwrap();
                st.push(match tok {
                    "+" => a + b,
                    "-" => a - b,
                    "*" => a * b,
                    _   => a / b,  // truncate toward zero
                });
            }
            _ => st.push(tok.parse().unwrap()),
        }
    }
    st.pop().unwrap()
}

fn main() {
    println!("=== Array Stack ===");
    let mut as_: ArrayStack<i32> = ArrayStack::new(10);
    as_.push(1).unwrap(); as_.push(2).unwrap(); as_.push(3).unwrap();
    println!("peek: {:?}", as_.peek().unwrap());
    println!("pop:  {:?}", as_.pop().unwrap());
    println!("pop:  {:?}", as_.pop().unwrap());
    println!("size: {}", as_.len());

    println!("\n=== Min Stack ===");
    let mut ms = MinStack::new();
    for v in [5, 3, 7, 2] { ms.push(v); }
    println!("peek: {:?}, min: {:?}", ms.peek(), ms.get_min());
    ms.pop();
    println!("After pop -- peek: {:?}, min: {:?}", ms.peek(), ms.get_min());

    println!("\n=== Balanced Parentheses ===");
    for t in ["([]{})", "(])", "((()))", "{[}]", ""] {
        println!("{:?}: {}", t, is_balanced(t));
    }

    println!("\n=== Next Greater Element ===");
    let arr = [4, 5, 2, 10, 8];
    println!("Array: {:?}", arr);
    println!("NGE:   {:?}", next_greater_element(&arr));

    println!("\n=== Postfix Evaluation ===");
    println!("\"3 4 +\" = {}", eval_postfix("3 4 +"));
    println!("\"3 4 + 2 *\" = {}", eval_postfix("3 4 + 2 *"));
    println!("\"15 7 1 1 + - / 3 * 2 1 1 + + -\" = {}",
        eval_postfix("15 7 1 1 + - / 3 * 2 1 1 + + -"));
}

/*
 * NOTES (vs. Java):
 * - Java's ArrayDeque is the recommended Stack. In Rust we use Vec or
 *   VecDeque. Both are growable arrays; VecDeque is ring-buffered.
 * - Java throws on underflow; Rust returns Result/Option so the caller is
 *   forced to handle the failure case.
 * - Generics in Rust are monomorphized like C++ templates (no runtime
 *   erasure as in Java).
 */
