/*
 * WEEK 2 - RUST CONTROL FLOW
 * Topic: If / Else
 * File: 2.if_else.rs
 *
 * CONCEPT:
 *  Rust's `if` is an EXPRESSION (not a statement), so it can return a value.
 *  The condition MUST be a `bool` -- there is no truthy/falsy coercion.
 *
 * KEY POINTS:
 *  - `if cond { ... } else if cond { ... } else { ... }`
 *  - The condition must be bool; `if x { ... }` does NOT compile when x is an int.
 *  - `let m = if a > b { a } else { b };` -- ternary equivalent.
 *  - `match` is the most powerful branching construct (pattern matching).
 *
 * SYNTAX:
 *   let m = if a > b { a } else { b };
 *   match x {
 *       1 => println!("one"),
 *       2 | 3 => println!("two or three"),
 *       _ => println!("other"),
 *   }
 *
 * DRY RUN:
 *   a=10, b=15 -> a>b false -> "b is greater"
 */

fn main() {
    let (a, b) = (10, 15);

    if a > b {
        print!("a ");
    } else {
        print!("b ");
    }
    println!("is greater");

    // if as an expression
    let max = if a > b { a } else { b };
    println!("max = {max}");

    // match -- much richer than Java's switch
    let grade = 'B';
    match grade {
        'A'        => println!("Excellent"),
        'B' | 'C' => println!("Good"),
        _          => println!("Try harder"),
    }

    // Compile-time check: if-cond must be bool
    // let x = 0;
    // if x { ... }   // compile error: expected `bool`, found integer
}

/*
 * NOTES:
 *  - Java/JS/Python allow truthy/falsy; Rust does NOT.
 *  - `if` is an expression in Rust -- assign it to a variable.
 *  - `match` is exhaustive: the compiler ENFORCES that every case is handled.
 *  - There is no `?:` ternary in Rust; use `if/else` expressions instead.
 */
