//! # Week 12: Stacks
//!
//! This module covers stack data structures and classic stack-based algorithms in Rust.
//! Topics include:
//! - Stack implementation using `Vec<i32>`
//! - Balanced parentheses check
//! - Next greater element (monotonic stack)
//! - MinStack (stack with O(1) minimum query)
//! - Postfix expression evaluation
//!
//! ## Rust-Specific Notes for DSA Learners
//! - `Vec<T>` is the natural stack in Rust: `push()` and `pop()` are O(1) amortized.
//! - `pop()` returns `Option<T>` — Rust forces you to handle the empty-stack case.
//!   No null pointer exceptions or silent undefined behavior.
//! - `last()` / `peek()` returns `Option<&T>` — a borrowed reference, not a copy.
//!   This means the stack still owns the element.

use std::collections::HashMap;

// ===========================================================================
// Stack Implementation
// ===========================================================================

/// A simple stack backed by a `Vec<i32>`.
///
/// In practice, you'd use `Vec<T>` directly — this wrapper exists to demonstrate
/// the stack interface explicitly.
struct Stack {
    data: Vec<i32>,
}

impl Stack {
    fn new() -> Self {
        Stack { data: Vec::new() }
    }

    /// Pushes a value onto the top of the stack.
    /// # Complexity: O(1) amortized
    fn push(&mut self, value: i32) {
        self.data.push(value);
    }

    /// Removes and returns the top element, or `None` if empty.
    /// # Complexity: O(1)
    fn pop(&mut self) -> Option<i32> {
        self.data.pop()
    }

    /// Returns a reference to the top element without removing it.
    /// # Complexity: O(1)
    fn peek(&self) -> Option<&i32> {
        self.data.last()
    }

    /// Returns true if the stack is empty.
    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    /// Returns the number of elements.
    fn len(&self) -> usize {
        self.data.len()
    }
}

// ===========================================================================
// Balanced Parentheses
// ===========================================================================

/// Checks if a string of brackets is balanced.
///
/// Supports `()`, `[]`, `{}`. Uses a stack: push opening brackets, pop and
/// compare when we see a closing bracket.
///
/// # Complexity
/// - Time:  O(n)
/// - Space: O(n) worst case (all opening brackets)
fn is_balanced(s: &str) -> bool {
    let mut stack: Vec<char> = Vec::new();

    // Map closing brackets to their matching opening bracket.
    let matches: HashMap<char, char> = [(')', '('), (']', '['), ('}', '{')]
        .iter()
        .cloned()
        .collect();

    for ch in s.chars() {
        match ch {
            '(' | '[' | '{' => stack.push(ch),
            ')' | ']' | '}' => {
                // `matches.get(&ch)` returns Option<&char>.
                // We check that the top of the stack matches.
                match (stack.pop(), matches.get(&ch)) {
                    (Some(top), Some(&expected)) if top == expected => {}
                    _ => return false,
                }
            }
            _ => {} // Ignore non-bracket characters.
        }
    }

    stack.is_empty() // Must be empty — all brackets matched.
}

// ===========================================================================
// Next Greater Element (Monotonic Stack)
// ===========================================================================

/// For each element in the array, finds the next greater element to its right.
///
/// Uses a **monotonic decreasing stack**: we maintain a stack of indices whose
/// values haven't found their "next greater" yet. When we encounter a larger
/// element, we pop and assign.
///
/// Returns a `Vec<Option<i32>>`: `Some(value)` if a greater element exists,
/// `None` if not (Rust's `Option` is perfect for this).
///
/// # Complexity
/// - Time:  O(n) — each element is pushed and popped at most once
/// - Space: O(n)
fn next_greater_element(arr: &[i32]) -> Vec<Option<i32>> {
    let n = arr.len();
    let mut result: Vec<Option<i32>> = vec![None; n];
    let mut stack: Vec<usize> = Vec::new(); // Stack of indices

    for i in 0..n {
        // Pop all elements that are smaller than arr[i].
        while let Some(&top_idx) = stack.last() {
            if arr[top_idx] < arr[i] {
                stack.pop();
                result[top_idx] = Some(arr[i]);
            } else {
                break;
            }
        }
        stack.push(i);
    }
    // Elements remaining in the stack have no next greater element (already None).

    result
}

// ===========================================================================
// MinStack
// ===========================================================================

/// A stack that supports push, pop, top, and retrieving the minimum element
/// in O(1) time.
///
/// ## Strategy
/// We maintain two stacks in parallel:
/// - `data`: the actual elements.
/// - `mins`: tracks the minimum at each level. `mins[i]` is the minimum of
///   all elements from the bottom up to position `i`.
///
/// This uses O(n) extra space but guarantees O(1) `get_min()`.
///
/// # Complexity (all operations)
/// - Time:  O(1)
/// - Space: O(n) total
struct MinStack {
    data: Vec<i32>,
    mins: Vec<i32>,
}

impl MinStack {
    fn new() -> Self {
        MinStack {
            data: Vec::new(),
            mins: Vec::new(),
        }
    }

    /// Pushes a value and updates the running minimum.
    fn push(&mut self, value: i32) {
        self.data.push(value);
        // The new minimum is min(value, current_min).
        let new_min = match self.mins.last() {
            Some(&current_min) => value.min(current_min),
            None => value,
        };
        self.mins.push(new_min);
    }

    /// Pops the top element (also pops from the mins stack).
    fn pop(&mut self) -> Option<i32> {
        self.mins.pop();
        self.data.pop()
    }

    /// Returns the top element.
    fn top(&self) -> Option<&i32> {
        self.data.last()
    }

    /// Returns the current minimum in O(1).
    fn get_min(&self) -> Option<&i32> {
        self.mins.last()
    }

    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }
}

// ===========================================================================
// Evaluate Postfix Expression
// ===========================================================================

/// Evaluates a postfix (Reverse Polish Notation) expression.
///
/// Tokens are space-separated. Operands are pushed onto a stack; operators pop
/// two operands, compute the result, and push it back.
///
/// Supported operators: `+`, `-`, `*`, `/` (integer division, truncates toward zero).
///
/// Returns `Some(result)` on success, `None` on invalid expression.
///
/// # Complexity
/// - Time:  O(n) where n = number of tokens
/// - Space: O(n) for the stack
fn eval_postfix(expression: &str) -> Option<i32> {
    let mut stack: Vec<i32> = Vec::new();

    for token in expression.split_whitespace() {
        match token {
            "+" | "-" | "*" | "/" => {
                // Need at least two operands.
                let b = stack.pop()?;
                let a = stack.pop()?;
                let result = match token {
                    "+" => a + b,
                    "-" => a - b,
                    "*" => a * b,
                    "/" => {
                        if b == 0 {
                            return None; // Division by zero.
                        }
                        a / b // Integer division (truncates toward zero in Rust).
                    }
                    _ => unreachable!(),
                };
                stack.push(result);
            }
            _ => {
                // Try to parse as integer.
                let num: i32 = token.parse().ok()?;
                stack.push(num);
            }
        }
    }

    // Valid postfix expression leaves exactly one value on the stack.
    if stack.len() == 1 {
        stack.pop()
    } else {
        None
    }
}

// ===========================================================================
// Main — demonstrations and test assertions
// ===========================================================================

fn main() {
    println!("=== Week 12: Stacks ===\n");

    // --- Stack Implementation ---
    println!("--- Stack (Vec-backed) ---");
    let mut stack = Stack::new();
    assert!(stack.is_empty());

    stack.push(10);
    stack.push(20);
    stack.push(30);
    assert_eq!(stack.len(), 3);
    assert_eq!(stack.peek(), Some(&30));
    println!("Stack after push(10, 20, 30): top = {:?}", stack.peek());

    assert_eq!(stack.pop(), Some(30));
    assert_eq!(stack.pop(), Some(20));
    assert_eq!(stack.peek(), Some(&10));
    println!("After two pops: top = {:?}", stack.peek());

    assert_eq!(stack.pop(), Some(10));
    assert_eq!(stack.pop(), None); // Empty!
    println!("Pop from empty stack: {:?}", stack.pop());

    // --- Balanced Parentheses ---
    println!("\n--- Balanced Parentheses ---");
    assert!(is_balanced("()"));
    assert!(is_balanced("()[]{}"));
    assert!(is_balanced("{[()]}"));
    assert!(is_balanced(""));
    assert!(!is_balanced("(]"));
    assert!(!is_balanced("([)]"));
    assert!(!is_balanced("(("));
    assert!(!is_balanced(")"));
    assert!(is_balanced("(a + b) * [c - {d / e}]")); // Non-bracket chars ignored
    println!("is_balanced(\"{{[()]}}\") = {}", is_balanced("{[()]}"));
    println!("is_balanced(\"([)]\")    = {}", is_balanced("([)]"));

    // --- Next Greater Element ---
    println!("\n--- Next Greater Element (Monotonic Stack) ---");
    let arr = vec![4, 5, 2, 10, 8];
    let nge = next_greater_element(&arr);
    assert_eq!(nge, vec![Some(5), Some(10), Some(10), None, None]);
    println!("arr = {:?}", arr);
    println!("NGE = {:?}", nge);

    let arr2 = vec![3, 2, 1];
    let nge2 = next_greater_element(&arr2);
    assert_eq!(nge2, vec![None, None, None]);
    println!("arr = {:?}, NGE = {:?}", arr2, nge2);

    let arr3 = vec![1, 2, 3];
    let nge3 = next_greater_element(&arr3);
    assert_eq!(nge3, vec![Some(2), Some(3), None]);
    println!("arr = {:?}, NGE = {:?}", arr3, nge3);

    // --- MinStack ---
    println!("\n--- MinStack ---");
    let mut ms = MinStack::new();
    ms.push(5);
    ms.push(3);
    ms.push(7);
    ms.push(2);
    ms.push(8);
    assert_eq!(ms.get_min(), Some(&2));
    assert_eq!(ms.top(), Some(&8));
    println!("Stack: [5, 3, 7, 2, 8], min = {:?}, top = {:?}", ms.get_min(), ms.top());

    ms.pop(); // Remove 8
    assert_eq!(ms.get_min(), Some(&2));
    println!("After pop(8): min = {:?}", ms.get_min());

    ms.pop(); // Remove 2
    assert_eq!(ms.get_min(), Some(&3));
    println!("After pop(2): min = {:?}", ms.get_min());

    ms.pop(); // Remove 7
    assert_eq!(ms.get_min(), Some(&3));
    println!("After pop(7): min = {:?}", ms.get_min());

    ms.pop(); // Remove 3
    assert_eq!(ms.get_min(), Some(&5));
    println!("After pop(3): min = {:?}", ms.get_min());

    // --- Evaluate Postfix ---
    println!("\n--- Evaluate Postfix Expression ---");
    // "3 4 + 2 * 7 /" = ((3 + 4) * 2) / 7 = 14 / 7 = 2
    assert_eq!(eval_postfix("3 4 + 2 * 7 /"), Some(2));
    println!("\"3 4 + 2 * 7 /\" = {:?}", eval_postfix("3 4 + 2 * 7 /"));

    // "5 1 2 + 4 * + 3 -" = 5 + ((1 + 2) * 4) - 3 = 5 + 12 - 3 = 14
    assert_eq!(eval_postfix("5 1 2 + 4 * + 3 -"), Some(14));
    println!("\"5 1 2 + 4 * + 3 -\" = {:?}", eval_postfix("5 1 2 + 4 * + 3 -"));

    // Simple: "2 3 +"
    assert_eq!(eval_postfix("2 3 +"), Some(5));

    // Division truncates: "7 2 /"
    assert_eq!(eval_postfix("7 2 /"), Some(3));

    // Invalid expression
    assert_eq!(eval_postfix("1 2 3 +"), None); // Two values left on stack
    assert_eq!(eval_postfix("+"), None);         // Not enough operands

    // Negative numbers
    assert_eq!(eval_postfix("-3 4 +"), Some(1));
    println!("\"-3 4 +\" = {:?}", eval_postfix("-3 4 +"));

    println!("\nAll assertions passed!");
}
