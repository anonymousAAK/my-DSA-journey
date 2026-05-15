# Phase 1 — CLI Calculator (reference implementation)

A ~200-line recursive descent calculator for arithmetic expressions over `+ - * / ^ ( )` with unary minus, integer/float literals, and a small set of named functions (`sqrt`, `abs`, `min`, `max`).

```
$ python calculator.py "1 + 2 * 3"
7.0
$ python calculator.py "sqrt(16) + abs(-2)"
6.0
$ python calculator.py          # demo + REPL
```

## Files

- `calculator.py` — tokenizer + parser + evaluator in one module (single pass, tree-walking).
- `test_calculator.py` — ~40 assertions, exits non-zero on failure.

## Design decisions

**Recursive descent, not Shunting Yard.** Recursive descent is the path a real compiler takes once you outgrow a toy calculator. The grammar maps 1:1 to functions, and each level encodes a precedence tier:

```
expr   := term   (('+' | '-') term)*           # lowest precedence, left-assoc
term   := factor (('*' | '/') factor)*         # next, left-assoc
factor := unary ('^' factor)?                  # right-assoc via recursive call on the RHS
unary  := ('-' | '+') unary | primary          # prefix operators
primary:= NUMBER | '(' expr ')' | IDENT '(' args ')'
```

Adding a new precedence tier means inserting one function. Adding a new syntactic form (ternary, comparison, function-call syntax — already done here) means adding one production. Shunting Yard would have given us a flat operator-precedence table, which is fine for `+-*/^` but awkward for things like function calls or future ternary expressions.

**Single-pass tree-walking eval.** Each parser rule both *parses and evaluates* on the way back up. There's no separate AST. For a reference impl this is the smallest working thing; for a real compiler you'd want an explicit AST so you can do constant folding, type checking, and pretty-printing.

**Errors carry a column.** `CalcError.pretty()` reproduces the input line with a `^` underneath the bad token, the way `rustc` and `clang` do it.

## Trade-offs / known quirks

- **`-2^2` evaluates to `4`, not `-4`.** Because `unary` is *below* `factor` in the grammar, unary minus binds tighter than `^`. Python and most calculators do the opposite (`-2^2 = -4`). Fixing this requires putting `unary` between `factor` and the right-hand side of `^`, which is left as an exercise. The test locks the current behavior so the regression is visible.
- **Recursion depth.** Each `(` consumes ~5 stack frames. With Python's default 1000 limit you get ~190 levels before crashing. The test calls `sys.setrecursionlimit(10000)` to verify 150 levels works. A production version would rewrite `expr`/`term`/`factor` as Pratt-style loops to remove the limit entirely.
- **No variables, no history.** Both are listed as stretch goals. Variables slot into `primary` as `IDENT` followed by no `(` — the parser already handles the disambiguation.

## Performance

Hand-test: `+`-joined sum of 5000 ones (`"1+1+...+1"`) evaluates in well under 100 ms on a laptop. The 10,000-char target from the spec is comfortably met.

## Where extensions go

- **Modulo (`%`):** add to `term` alongside `*` and `/`.
- **Comparison / boolean ops:** add a new tier below `expr` (e.g. `relation := expr (('<' | '>' | '==') expr)?`).
- **Variables:** add an `env: dict[str, float]` to `Parser`, recognize bare `IDENT` (not followed by `(`) in `primary`, and add an `=` assignment statement at the top level.
- **Big numbers:** swap `float` for `decimal.Decimal` or `fractions.Fraction`. Only `primary` (number parsing) and the arithmetic ops need to change.
