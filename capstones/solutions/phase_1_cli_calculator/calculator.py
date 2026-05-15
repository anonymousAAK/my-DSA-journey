"""Recursive descent calculator: + - * / ^ ( ) and unary minus.

Grammar:
    expr   := term   (('+' | '-') term)*
    term   := factor (('*' | '/') factor)*
    factor := unary ('^' factor)?          # right-associative
    unary  := '-' unary | primary
    primary:= NUMBER | '(' expr ')' | IDENT '(' args ')'
    args   := expr (',' expr)*

Run: ``python calculator.py`` for a demo, or ``python calculator.py "1+2*3"``.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from typing import Callable


class CalcError(Exception):
    """User-facing calculator error with a source column."""

    def __init__(self, msg: str, col: int, src: str = "") -> None:
        super().__init__(msg)
        self.msg = msg
        self.col = col
        self.src = src

    def pretty(self) -> str:
        pointer = " " * self.col + "^"
        return f"error at column {self.col + 1}: {self.msg}\n    {self.src}\n    {pointer}"


# --- Tokenizer ---------------------------------------------------------------

@dataclass
class Token:
    kind: str  # NUMBER, IDENT, +, -, *, /, ^, (, ), ',', EOF
    value: str
    col: int


def tokenize(src: str) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    while i < len(src):
        c = src[i]
        if c.isspace():
            i += 1
            continue
        if c.isdigit() or (c == "." and i + 1 < len(src) and src[i + 1].isdigit()):
            start = i
            saw_dot = False
            while i < len(src) and (src[i].isdigit() or src[i] == "."):
                if src[i] == ".":
                    if saw_dot:
                        raise CalcError("malformed number (two dots)", i, src)
                    saw_dot = True
                i += 1
            tokens.append(Token("NUMBER", src[start:i], start))
            continue
        if c.isalpha() or c == "_":
            start = i
            while i < len(src) and (src[i].isalnum() or src[i] == "_"):
                i += 1
            tokens.append(Token("IDENT", src[start:i], start))
            continue
        if c in "+-*/^(),":
            tokens.append(Token(c, c, i))
            i += 1
            continue
        raise CalcError(f"unexpected character {c!r}", i, src)
    tokens.append(Token("EOF", "", len(src)))
    return tokens


# --- Parser + Evaluator (tree-walking in one pass) ---------------------------

FUNCS: dict[str, tuple[int, Callable[..., float]]] = {
    "sqrt": (1, lambda x: math.sqrt(x)),
    "abs": (1, lambda x: abs(x)),
    "min": (2, lambda a, b: min(a, b)),
    "max": (2, lambda a, b: max(a, b)),
}


class Parser:
    def __init__(self, tokens: list[Token], src: str) -> None:
        self.tokens = tokens
        self.src = src
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def eat(self, kind: str) -> Token:
        t = self.peek()
        if t.kind != kind:
            raise CalcError(f"expected {kind!r} but got {t.kind!r}", t.col, self.src)
        self.pos += 1
        return t

    def parse(self) -> float:
        value = self.expr()
        if self.peek().kind != "EOF":
            t = self.peek()
            raise CalcError(f"unexpected token {t.value!r}", t.col, self.src)
        return value

    def expr(self) -> float:
        lhs = self.term()
        while self.peek().kind in ("+", "-"):
            op = self.eat(self.peek().kind).kind
            rhs = self.term()
            lhs = lhs + rhs if op == "+" else lhs - rhs
        return lhs

    def term(self) -> float:
        lhs = self.factor()
        while self.peek().kind in ("*", "/"):
            tok = self.eat(self.peek().kind)
            rhs = self.factor()
            if tok.kind == "*":
                lhs = lhs * rhs
            else:
                if rhs == 0:
                    raise CalcError("division by zero", tok.col, self.src)
                lhs = lhs / rhs
        return lhs

    def factor(self) -> float:
        lhs = self.unary()
        if self.peek().kind == "^":
            self.eat("^")
            rhs = self.factor()  # right-associative
            return lhs ** rhs
        return lhs

    def unary(self) -> float:
        if self.peek().kind == "-":
            self.eat("-")
            return -self.unary()
        if self.peek().kind == "+":
            self.eat("+")
            return self.unary()
        return self.primary()

    def primary(self) -> float:
        t = self.peek()
        if t.kind == "NUMBER":
            self.eat("NUMBER")
            return float(t.value) if "." in t.value else float(int(t.value))
        if t.kind == "(":
            self.eat("(")
            v = self.expr()
            if self.peek().kind != ")":
                raise CalcError("missing ')'", self.peek().col, self.src)
            self.eat(")")
            return v
        if t.kind == "IDENT":
            self.eat("IDENT")
            if t.value not in FUNCS:
                raise CalcError(f"unknown function {t.value!r}", t.col, self.src)
            arity, fn = FUNCS[t.value]
            self.eat("(")
            args = [self.expr()]
            while self.peek().kind == ",":
                self.eat(",")
                args.append(self.expr())
            self.eat(")")
            if len(args) != arity:
                raise CalcError(
                    f"{t.value} expects {arity} arg(s), got {len(args)}", t.col, self.src
                )
            try:
                return float(fn(*args))
            except ValueError as e:
                raise CalcError(f"{t.value}: {e}", t.col, self.src) from None
        raise CalcError(f"unexpected token {t.value!r}", t.col, self.src)


def evaluate(src: str) -> float:
    tokens = tokenize(src)
    return Parser(tokens, src).parse()


def main(argv: list[str]) -> int:
    if len(argv) > 1:
        expr = " ".join(argv[1:])
        try:
            print(evaluate(expr))
        except CalcError as e:
            print(e.pretty(), file=sys.stderr)
            return 1
        return 0

    # Demo + REPL
    print("calculator demo (Ctrl-D / Ctrl-C to quit)")
    samples = [
        "1 + 2 * 3",
        "(1 + 2) * 3",
        "-3 * (-4 + 5)",
        "2 ^ 3 ^ 2",  # right-assoc => 512
        "sqrt(16) + abs(-2)",
        "max(1, min(9, 5))",
    ]
    for s in samples:
        print(f"  {s} = {evaluate(s)}")

    try:
        while True:
            line = input("> ").strip()
            if not line:
                continue
            try:
                print(evaluate(line))
            except CalcError as e:
                print(e.pretty())
    except (EOFError, KeyboardInterrupt):
        print()
        return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
