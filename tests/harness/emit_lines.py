"""Per-topic JSON-fixture -> line-format emitter shared by harness_cpp.sh
and harness_rust.sh.

Reads tests/cases/<topic>.json and prints a deterministic, simple line-based
representation that the per-topic C++/Rust drivers parse on stdin. Keeping a
single emitter ensures both language drivers consume an identical format.

Usage:
    python3 tests/harness/emit_lines.py <topic> <fixture.json>
"""

from __future__ import annotations
import json
import sys


def emit_arr(arr):
    if not arr:
        print(f"ARR {len(arr)}")
    else:
        print(f"ARR {len(arr)} " + " ".join(str(x) for x in arr))


def emit_str(s):
    print(f"STR {len(s)} {s}")


def emit_int(v):
    print(f"INT {v}")


def emit_bool(b):
    print(f"BOOL {1 if b else 0}")


def emit_arr_opt(arr):
    """Level-order tree encoding with NULL sentinels."""
    print(f"TREE {len(arr)}")
    for v in arr:
        if v is None:
            print("NULL")
        else:
            print(f"VAL {v}")


def main():
    topic = sys.argv[1]
    fixture = sys.argv[2]
    data = json.load(open(fixture))

    for c in data["cases"]:
        if c.get("skip"):
            continue
        print(f"CASE {c['name']}")
        inp = c["input"]
        exp = c["expected"]

        if topic == "kadane_max_subarray":
            emit_arr(inp[0]); emit_int(exp)
        elif topic == "linear_search":
            arr = inp[0]; target = inp[1]
            print(f"INPUT {len(arr)}" + ("" if not arr else " " + " ".join(str(x) for x in arr)) + f" {target}")
            emit_int(exp)
        elif topic == "dutch_national_flag":
            emit_arr(inp[0]); emit_arr(exp)
        elif topic == "palindrome_check":
            emit_str(inp[0]); emit_bool(exp)
        elif topic == "valid_anagram":
            emit_str(inp[0]); emit_str(inp[1]); emit_bool(exp)
        elif topic == "kmp_search":
            emit_str(inp[0]); emit_str(inp[1]); emit_arr(exp)
        elif topic == "rabin_karp_search":
            emit_str(inp[0]); emit_str(inp[1]); emit_arr(exp)
        elif topic == "binary_search":
            emit_arr(inp[0]); emit_int(inp[1]); emit_int(exp)
        elif topic == "binary_search_on_answer":
            emit_arr(inp[0]); emit_int(inp[1]); emit_int(exp)
        elif topic == "merge_sort":
            emit_arr(inp[0]); emit_arr(exp)
        elif topic == "quick_sort":
            emit_arr(inp[0]); emit_arr(exp)
        elif topic == "spiral_traversal":
            mat = inp[0]
            rows = len(mat); cols = len(mat[0]) if rows else 0
            print(f"MAT {rows} {cols}")
            for row in mat:
                print(" ".join(str(x) for x in row))
            emit_arr(exp)
        elif topic == "reverse_linked_list":
            emit_arr(inp[0]); emit_arr(exp)
        elif topic == "lru_cache":
            cap = inp[0]; ops = inp[1]
            print(f"CAP {cap}")
            print(f"OPS {len(ops)}")
            for op in ops:
                if op[0] == "put":
                    print(f"PUT {op[1]} {op[2]}")
                elif op[0] == "get":
                    print(f"GET {op[1]}")
            emit_arr(exp)
        elif topic == "balanced_parens":
            emit_str(inp[0]); emit_bool(exp)
        elif topic == "sliding_window_max":
            emit_arr(inp[0]); emit_int(inp[1]); emit_arr(exp)
        elif topic == "bst_validate":
            emit_arr_opt(inp[0]); emit_bool(exp)
        elif topic == "kth_largest":
            emit_arr(inp[0]); emit_int(inp[1]); emit_int(exp)
        elif topic == "two_sum":
            emit_arr(inp[0]); emit_int(inp[1]); emit_arr(exp)
        elif topic == "topological_sort":
            V = inp[0]; edges = inp[1]
            print(f"V {V}")
            print(f"EDGES {len(edges)}")
            for e in edges:
                print(f"{e[0]} {e[1]}")
            if exp is None:
                print("EXPECTED_NONE")
            else:
                emit_arr(exp)
        elif topic == "coin_change":
            emit_arr(inp[0]); emit_int(inp[1]); emit_int(exp)
        elif topic == "n_queens_count":
            emit_int(inp[0]); emit_int(exp)
        elif topic == "dijkstra_shortest_path":
            V = inp[0]; edges = inp[1]; src = inp[2]
            print(f"V {V}")
            print(f"EDGES {len(edges)}")
            for e in edges:
                print(f"{e[0]} {e[1]} {e[2]}")
            print(f"SRC {src}")
            emit_arr(exp)
        elif topic == "kruskal_mst_weight":
            V = inp[0]; edges = inp[1]
            print(f"V {V}")
            print(f"EDGES {len(edges)}")
            for e in edges:
                print(f"{e[0]} {e[1]} {e[2]}")
            emit_int(exp)
        elif topic == "sliding_window_longest_substr":
            emit_str(inp[0]); emit_int(exp)
        else:
            # Unknown topic — emit nothing; driver prints no PASS/FAIL.
            pass
        print()


if __name__ == "__main__":
    main()
