# Capstone — Phase 1: CLI Calculator with Operator Precedence

**Time estimate**: 8-12 hours over 1-2 weekends.
**Prerequisite weeks**: 1-5 (arrays, strings, stacks, recursion, basic complexity).
**Skill checked**: You can take a real-world parsing problem, choose between two well-known algorithms (Shunting Yard vs. recursive descent), implement it cleanly, and defend your choice in a commit message.

## The Goal
Build a command-line calculator that reads an arithmetic expression from stdin or argv and prints the numeric result. It must respect operator precedence (`*` and `/` bind tighter than `+` and `-`), associativity (left for the four basics, right for `^`), parentheses, unary minus, and ideally a small set of named functions (`sqrt`, `abs`, `min`, `max`). This is the canonical "first compiler-ish thing you build" — every language has one, every senior engineer has written one, and it's the cleanest way to lock in stacks and recursion.

## Functional Requirements
- Must support `+ - * / ^` with correct precedence and associativity.
- Must support parenthesized sub-expressions, arbitrarily nested.
- Must support unary minus (e.g. `-3 * (-4 + 5)`).
- Must support integer and floating-point literals (`3`, `3.14`, `.5`, `2.`).
- Must produce a *helpful* error message (with column position) on malformed input — not a Python traceback.
- Should support at least the named functions `sqrt`, `abs`, `min(a,b)`, `max(a,b)`.
- Should reject division by zero and other domain errors with a clean message.

## Non-functional Requirements
- Performance: parse + evaluate a 10,000-character expression in well under one second. (Trivial — but you must measure it and report the number in the README.)
- Memory: no recursion-depth crashes on a 1000-level nested expression. If you use recursive descent, document the depth limit; if Shunting Yard, you have no such issue.
- Code quality: each function ≤ 30 lines; the tokenizer, parser, and evaluator are three distinct modules/files.
- Tests: at least 30 test cases covering precedence, associativity, parentheses, unary minus, errors.

## Architecture Sketch

```
+-----------+     tokens     +----------+    AST or RPN     +-----------+
| Tokenizer | -------------> |  Parser  | ----------------> | Evaluator |
+-----------+                +----------+                   +-----------+
       ^                          ^                              |
       |                          |                              v
   input string             error reporter                    number
```

If you go Shunting Yard, the "AST or RPN" channel is an RPN list, and the evaluator is a stack machine. If you go recursive descent, it's an AST and the evaluator is a tree walk.

## Implementation Roadmap

1. **Day 1 (3-4h) — Tokenizer.**
   Hand-write the tokenizer. No regex shortcuts. Token types: NUMBER, IDENT, LPAREN, RPAREN, COMMA, PLUS, MINUS, STAR, SLASH, CARET, EOF. Each token carries its source column for later error reporting. Write the tokenizer's tests first (TDD here pays off because tokenizer bugs are silent).

2. **Day 2 (3-4h) — Parser.**
   Pick *one* approach and write a 100-200 word decision note in your commit message explaining why.
   - **Shunting Yard**: easier to extend with new operators, harder to extend with new syntactic forms (e.g. ternary). Produces RPN.
   - **Recursive descent**: easier to read, easier to add new productions (function calls, ternary, comparison), the path most production compilers take. Produces an AST.

   Whichever you pick, the parser must handle unary minus and parentheses and at least one named function. Write tests for "expression with all operator precedences in one line" — these are where you'll find the bugs.

3. **Day 3 (2-3h) — Evaluator + CLI + errors.**
   Walk the RPN or AST. Implement domain checks (division by zero, negative sqrt, etc.). Wire up the CLI with `argparse` or your language's equivalent: read from argv if provided, otherwise REPL on stdin. Errors should print:
   ```
   error at column 7: unexpected token ')'
       3 + 4 )
              ^
   ```

4. **Polish (1-2h)** — README with a usage section, a one-paragraph "design choices" section (your Shunting Yard vs. recursive descent justification, copied from your commit), and the performance number.

## Stretch Goals
- Variables: `x = 3; x * 4` returns 12.
- A `history` command that recalls past expressions.
- Implicit multiplication: `2(3+4)` evaluates as `2*(3+4)`. (Beware: this interacts badly with named functions — `sqrt(4)` must still parse as a call, not multiplication.)
- A debug flag that prints the token stream and (for recursive descent) the AST.
- Big-number arithmetic via your language's bignum library, opt-in by flag.

## Reference Implementation

A working Python reference lives at `capstones/solutions/phase_1_cli_calculator/`. **Don't peek before you attempt this yourself** — copying it defeats the entire point of a capstone.

When you're done (or genuinely stuck after 4+ hours of honest effort), open the reference and:

1. Read its `README.md` for the design decisions and tradeoffs the author made.
2. Diff your architecture against theirs. What's different? Whose choices were better, and why?
3. Run its `test_*.py` against your implementation (you may need a thin adapter).
4. Write a journal entry comparing the two implementations.

The reference is *a* solution, not *the* solution. Yours might be cleaner. Yours might be slower. Either is a learning outcome.

## Self-grading rubric
| Criterion | Points | What you're checking |
|-----------|--------|----------------------|
| Correctness on basic inputs | 30 | All 4 operators, parens, floats, named functions produce right answers |
| Handles edge cases | 20 | Unary minus, deeply nested parens, division by zero, malformed input |
| Algorithm choice is justified (commit message or README) | 15 | You can articulate Shunting Yard vs. recursive descent tradeoff |
| Code is readable (function size, naming) | 15 | Three clear modules; functions ≤ 30 lines; no mystery names |
| Tests pass (≥80% coverage on core logic) | 10 | Run a coverage tool and screenshot the result |
| Stretch goal implemented | 10 | At least one of the stretch goals, with its own tests |

## When you're done
- Push to a separate repo (or branch) and link it from your portfolio.
- Write a reflection essay in your `SOLUTION_JOURNAL.md`: which bugs surprised you, where did the algorithm choice cost or save you time, what would you do differently?
- Compare your final architecture to a real product that does the same thing (see `case_studies/real_world/`). For this one, look at how Python's `ast` module or `bc(1)` are structured — they're not so different from yours, just bigger.
