# Phase 1: Foundations — Build a Calculator That Respects Operator Precedence

## The Word Problem

> Hey, quick one. We're building an in-app "formula bar" for our finance dashboard so analysts can type something like `1200 + 35 * (8 - 3) / 2 - 7` and see the result. Right now the engineer who started it just used `eval()` and security flagged it. Can you build a tiny safe expression evaluator? It should handle `+ - * /`, parentheses, and decimals. Don't worry about variables yet. Oh — and someone's already typing `3++4` into the staging build, so it has to fail gracefully when the input is junk. Need it by Friday-ish.

This is a one-paragraph message from a PM, but inside it are at least five hidden questions. Let's pull them apart.

## Step 1: Restate the problem precisely

- **Input**: a string, e.g. `"1200 + 35 * (8 - 3) / 2 - 7"`.
- **Output**: a number — the value of the expression — OR a clear error if the input is malformed.
- **Operators**: `+`, `-`, `*`, `/`. Standard precedence (`*` and `/` bind tighter than `+` and `-`). Parentheses override precedence.
- **Numbers**: integers and decimals. Probably non-negative literals (negation is a separate concern: is `-3` a unary minus or a parse error?).
- **Hidden requirement**: must be safe — no `eval`. So we are writing a *parser*.

The fact that the PM said "respects operator precedence" tells us the obvious left-to-right scan is wrong. `1 + 2 * 3` must give `7`, not `9`.

## Step 2: Identify constraints

- Input size: a formula bar — probably under 200 characters. Performance is not the constraint here; **correctness and safety** are.
- Time budget: human-interactive, so under a few milliseconds.
- Memory: trivial.
- Edge cases I can already think of:
  - Empty string
  - Just whitespace
  - Mismatched parens: `(1 + 2`, `1 + 2)`
  - Division by zero: `1 / 0`
  - Junk tokens: `3++4`, `1 + + 2`, `1 2 3`
  - Leading/trailing operators: `+ 3`, `3 *`
  - Decimals like `.5`, `5.`, `5.5.5`
  - Very deep nesting `(((((1)))))`
  - Unicode digits, fullwidth `＋`, smart minus `−` (decide: reject)
  - Floating-point quirks: `0.1 + 0.2 != 0.3`

## Step 3: Brute force first (don't skip this)

The naivest correct-feeling approach: scan left to right, build up a result. This *works* for `1 + 2 + 3` but breaks immediately for `1 + 2 * 3` because by the time we see `*`, we've already committed to adding.

A slightly less naive approach: do two passes. First pass evaluates all `*` and `/`, collapsing the expression. Second pass evaluates all `+` and `-`. This is essentially what a calculator from the 70s did, and it actually works for flat expressions. But it falls apart with parentheses — now you need to recursively evaluate the inside first.

So the "brute force" version is really: **find the innermost parenthesis pair, evaluate that flat expression with two passes, replace with its value, repeat**. Complexity: O(n²) in the worst case (deeply nested parens, each pass rescanning). For a 200-char input that's fine, but it's clumsy and the bookkeeping is error-prone.

## Step 4: Identify wasted work

The re-scanning is the wasted work. Every time we resolve a parenthesis, we re-walk the same string. More importantly, the brute force conflates two jobs: **figuring out the structure** of the expression, and **computing its value**. Those should be separated.

The structural insight: an arithmetic expression has a natural *grammar*:

```
expr   := term   (('+' | '-') term)*
term   := factor (('*' | '/') factor)*
factor := number | '(' expr ')'
```

Once you see this, the algorithm writes itself. `expr` calls `term`, `term` calls `factor`, `factor` either returns a number or recurses into `expr`. **Operator precedence falls out of the call hierarchy** — `*` is at the `term` level (deeper in the call stack), so it gets computed before `+` returns.

This is the classic **recursive descent parser**, and it's the right Week 4-5 tool for this job.

## Step 5: Optimize

Two-stage cleanup:

1. **Tokenize first.** Walk the string once, producing a list of tokens: `NUM(1200)`, `PLUS`, `NUM(35)`, `STAR`, `LPAREN`, …. This isolates "is this a valid character" from "is this a valid expression". A lot of edge cases (smart minus, fullwidth digits, stray letters) die at tokenization.

2. **Recursive descent.** Three mutually-recursive functions matching the grammar above. Each consumes from the token stream. We carry an index `i` (or pop from a deque). At the top level we assert `i == len(tokens)` — anything left over means a syntax error.

The whole thing is O(n) time, O(d) stack depth where d is paren-nesting depth.

```python
def parse_expr(tokens, i):
    val, i = parse_term(tokens, i)
    while i < len(tokens) and tokens[i] in ('+', '-'):
        op = tokens[i]
        rhs, i = parse_term(tokens, i + 1)
        val = val + rhs if op == '+' else val - rhs
    return val, i
```

`parse_term` and `parse_factor` follow the same shape. **Each level handles exactly the operators at its precedence**, and recursion handles the rest.

## Step 6: Implementation gotchas

- **Division**: integer or float? Pick float for a calculator (`5 / 2 == 2.5`). Document it.
- **Division by zero**: don't crash; return a structured error.
- **Decimals**: parse `.5` and `5.` consistently or reject both — don't be inconsistent.
- **Float comparison**: never use `==` in tests; use `abs(a-b) < 1e-9`.
- **Off-by-one**: when advancing `i` past an operator, make sure the recursive call sees the *operand*, not the operator.
- **Unary minus**: easiest fix is to allow a leading `-` in `factor`: `factor := '-' factor | number | '(' expr ')'`. Be deliberate.
- **Whitespace**: strip it in the tokenizer, not in the parser. Mixing concerns is how you get bugs.
- **Stack depth**: Python's default recursion limit is 1000. `(((((...)))))` 600 deep is fine. 5000 deep crashes. Document the limit or switch to an iterative shunting-yard if you care.

## Step 7: Verification

Test plan:

- Trivial: `"1"` → 1, `"1 + 1"` → 2.
- Precedence: `"1 + 2 * 3"` → 7, `"2 * 3 + 1"` → 7, `"2 + 2 * 2"` → 6.
- Parens: `"(1 + 2) * 3"` → 9, `"((1))"` → 1.
- Nesting: `"1 + (2 * (3 + 4))"` → 15.
- Errors: `""`, `"1 +"`, `"+ 1"`, `"(1 + 2"`, `"1 + 2)"`, `"3++4"`, `"abc"` → all should raise a structured `ParseError` with a position.
- Float: `"0.1 + 0.2"` → close to 0.3.
- Stress test: random expression generator that builds trees, evaluates with the parser AND with Python's own arithmetic, and compares. Run 10,000 random cases.

## Step 8: Reflection

What made this hard: it *looks* trivial. A calculator is the canonical "I can do that in 10 minutes" problem. But operator precedence is exactly the trap that catches people who don't realize they're writing a parser.

The pattern is **recursive descent**, and once you see it you start to spot it everywhere:

- JSON parsers (Week 5).
- The `cron` expression parser at your day job.
- Markdown → HTML.
- SQL `WHERE` clauses.
- The regex engine that powers your text editor's find-and-replace.

The deeper pattern is **separation of concerns**: tokenize, then parse, then evaluate. When you find yourself doing all three in one loop, you're going to have a bad time.

Curriculum tie-in: this exercises Week 4 (recursion) and Week 5 (basic parsing) in tight integration. If you've done those weeks, you've already built every piece — this just assembles them around a real-world prompt.
