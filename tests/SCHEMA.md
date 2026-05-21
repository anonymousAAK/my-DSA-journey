# `cases.json` schema

Each fixture file under `tests/cases/<topic>.json` is the single source of truth
for that topic's correctness checks across every language harness.

## Top-level object

```json
{
  "topic": "kadane_max_subarray",
  "week": 6,
  "function": "maxSubarraySum",
  "cases": [
    {"name": "basic", "input": [[-2,1,-3,4,-1,2,1,-5,4]], "expected": 6},
    {"name": "all_negative", "input": [[-3,-1,-2]], "expected": -1},
    {"name": "single_element", "input": [[5]], "expected": 5},
    {"name": "empty", "input": [[]], "expected": 0, "edge": true}
  ]
}
```

### Fields

| field      | type      | required | meaning                                                                              |
| ---------- | --------- | -------- | ------------------------------------------------------------------------------------ |
| `topic`    | string    | yes      | snake_case identifier; matches the file stem and the module/class in `tests/refs/`.   |
| `week`     | int       | yes      | Week number where the topic is taught (for tooling / grouping).                       |
| `function` | string    | yes      | Logical operation name. Each language harness maps this to its own identifier table. |
| `cases`    | array     | yes      | Non-empty list of case objects.                                                       |

### Case object

| field         | type    | required | meaning                                                                              |
| ------------- | ------- | -------- | ------------------------------------------------------------------------------------ |
| `name`        | string  | yes      | Unique within the file; appears in PASS / FAIL output.                               |
| `input`       | array   | yes      | **JSON array of positional args**. The harness unpacks this with `f(*input)`.        |
| `expected`    | any     | yes      | The value the harness compares against (deep equality).                              |
| `edge`        | bool    | no       | Marks an edge case (empty / boundary). Informational only.                           |
| `stretch`     | bool    | no       | A larger/stress input.                                                               |
| `adversarial` | bool    | no       | Designed to defeat naive or buggy implementations.                                   |
| `skip`        | bool    | no       | Skip this case (do not run, do not fail). Useful while iterating.                    |

The harness ALWAYS unpacks `input` as positional arguments. If your function
takes a list, wrap that list once more in the `input` array — see the kadane
example above.

## Conventions

* **Determinism**: every case must produce one canonical answer. For algorithms
  whose result is order-dependent (e.g. topological sort, group anagrams), the
  fixture's `expected` is the **canonical sorted form**, and the reference
  function is responsible for normalising its output before returning. Document
  this contract in the reference module.
* **Empty cases**: include at least one when the algorithm has a defined
  behaviour on an empty input. Mark `edge: true`.
* **All-negative / duplicates / already-sorted**: include these for algorithms
  where they historically break naive implementations.
* **Stress case**: include at least one case of size 50-200 (not gigantic;
  these run in CI and need to stay snappy).
* **Sequences of operations** (e.g. LRU cache, stack): represent the operations
  as a list of `[op_name, arg1, arg2, ...]` tuples, and the reference function
  is a "driver" that interprets them and returns a list of results from the
  query ops.

## Per-language harness extension

The reference Python harness lives at `tests/harness/harness.py`. To add a new
language harness, follow these steps:

1. **Identifier mapping**: define a per-language alias table that maps
   `topic` -> concrete identifier (class name, function name, file path).
2. **Case loader**: parse `cases.json` with whatever JSON library the language
   provides. Iterate cases; deserialise `input` and `expected` into native
   values.
3. **Dispatch**: invoke the operation. Some topics need a thin "driver" written
   per-language (e.g. building a linked list from an array) — keep these
   drivers in `tests/refs/<lang>/<topic>.<ext>` to mirror the Python layout.
4. **Compare & report**: print exactly the same `PASS topic :: name` /
   `FAIL topic :: name` format so CI aggregation is uniform.

Skeletons for C++, Java, and Rust harnesses are in place:

* `tests/harness/harness_cpp.sh` — wraps a per-topic C++ binary built from each
  `tests/refs/<topic>.cpp` plus a tiny stdin-driven driver.
* `tests/harness/harness.java` — single Java entry point that reflects into a
  per-topic class.
* `tests/harness/harness_rust.sh` — `rustc`-based runner that mirrors the C++
  harness for each `tests/refs/<topic>.rs` driver.

The C++ and Rust harnesses share a single per-topic JSON->line emitter in
`tests/harness/emit_lines.py`. Each driver reads a deterministic line-based
format from stdin (`CASE`, `ARR`, `INT`, `STR`, etc.) and prints `PASS topic
:: case_name` or `FAIL topic :: case_name`. Both `--all` modes loop through
every `tests/cases/*.json` and dispatch to the matching driver; topics without
a driver print `SKIP topic :: no <lang> driver yet` and don't fail the run.

All 25 topics ship with both C++ and Rust drivers (120/120 cases per
language). The Python orchestrator at `tests/harness/harness.py` accepts
`--lang python|cpp|rust|java|all`, where `all` runs Python first (fast), then
C++, then Rust, then aggregates the per-language exit codes.
