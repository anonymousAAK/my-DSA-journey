# Correctness Tests

This directory houses the cross-language **correctness-check** layer that
sits on top of the per-language compile checks in `.github/workflows/build.yml`.

The layout is:

```
tests/
├── SCHEMA.md            # cases.json format and conventions
├── README.md            # this file
├── cases/               # canonical fixtures, one JSON file per topic
│   ├── kadane_max_subarray.json
│   ├── linear_search.json
│   └── ... (25 total)
├── refs/                # reference implementations consumed by harnesses
│   ├── kadane_max_subarray.py
│   ├── kadane_max_subarray.cpp
│   ├── kadane_max_subarray.rs
│   ├── KadaneMaxSubarray.java    # pilot: Java reference for kadane
│   └── ... (25 Python refs + 25 C++ + 25 Rust drivers; Java still pilot-only)
└── harness/
    ├── harness.py        # Python orchestrator — also shells out to cpp/rust/java
    ├── emit_lines.py     # shared JSON->line-format emitter (cpp + rust)
    ├── harness_cpp.sh    # C++ harness — all 25 topics
    ├── Harness.java      # Java harness — pilot: kadane only
    └── harness_rust.sh   # Rust harness — all 25 topics
```

## What problem does this solve?

Before this layer the CI guarantees were "every file compiles". That catches
syntax errors but not algorithm bugs. The fixtures here drive the same input
(JSON) into every language's implementation and compare against the same
expected output, giving four-way agreement as a much stronger signal.

## Running

### Python (the full 25 topics)

```bash
# Run a specific topic
python tests/harness/harness.py tests/cases/kadane_max_subarray.json

# Run every fixture
python tests/harness/harness.py --all

# Show PASS lines too (default: only FAILs)
python tests/harness/harness.py --all -v
```

CI runs `python tests/harness/harness.py --all --lang python` after the
Python compile job succeeds, plus parallel `tests-cpp` / `tests-rust` /
`tests-java` jobs. See `.github/workflows/build.yml`.

### C++ and Rust (all 25 topics)

```bash
# One topic
bash tests/harness/harness_cpp.sh tests/cases/<topic>.json
bash tests/harness/harness_rust.sh tests/cases/<topic>.json

# All 25 topics
bash tests/harness/harness_cpp.sh --all
bash tests/harness/harness_rust.sh --all

# Via the Python orchestrator (same args, picks the wrapper)
python tests/harness/harness.py --all --lang cpp
python tests/harness/harness.py --all --lang rust

# Run python first, then cpp, then rust, then aggregate
python tests/harness/harness.py --all --lang all
```

### Java (kadane pilot only)

```bash
javac -d /tmp/java-out tests/harness/Harness.java tests/refs/KadaneMaxSubarray.java
java -cp /tmp/java-out Harness tests/cases/kadane_max_subarray.json
```

Each non-Python harness prints `SKIP <topic> :: no <lang> driver yet` for
fixtures whose driver hasn't been written (still the case for Java).

## Adding a new fixture

1. Create `tests/cases/<topic>.json` per `SCHEMA.md`.
2. Create `tests/refs/<topic>.py` exposing the canonical function. The
   `function` field in the JSON file must match the function name in the
   Python module.
3. Run `python tests/harness/harness.py tests/cases/<topic>.json` until it
   passes; tweak `expected` if your reference is the source of truth.
4. Commit both files. CI picks them up automatically (the harness globs
   `tests/cases/*.json`).

## Extending the C++ / Java / Rust harnesses

The pilot already establishes the pattern. Adding a new topic follows three
mechanical steps:

### C++

1. Copy `tests/refs/kadane_max_subarray.cpp` to
   `tests/refs/<new_topic>.cpp`.
2. Replace `maxSubarraySum` with your function under test. Keep the
   stdin-driven CASE/INPUT/EXPECTED parser — only swap the body of the
   per-line decoding if your inputs aren't a flat list of ints.
3. In `tests/harness/harness_cpp.sh`:
   * append `<new_topic>` to `SUPPORTED_TOPICS`,
   * add an `emit_<new_topic>` translator (mirror `emit_kadane`),
   * add a `case` branch in `run_one` that calls it.

### Java

1. Add `tests/refs/<NewTopicCamelCase>.java` with the static method to test.
2. In `tests/harness/Harness.java` add an entry to `TOPIC_CLASSES`:
   `TOPIC_CLASSES.put("<snake_case_topic>", new String[]{"<ClassName>", "<methodName>"});`
3. If the input shape differs from `long[]` (i.e. anything except a flat
   array of integers), branch in `main()` on `topic` to build the right
   reflection call and decode the JSON.

### Rust

1. Copy `tests/refs/kadane_max_subarray.rs` to `tests/refs/<new_topic>.rs`.
2. Replace `max_subarray_sum` with your function; keep the same stdin
   protocol unless your input shape differs.
3. In `tests/harness/harness_rust.sh`: add the topic to `SUPPORTED_TOPICS`,
   add an `emit_<new_topic>` translator, and a `case` branch.

The shell harnesses use Python (`python3 - <<PY ... PY`) for JSON parsing on
the host side, then hand the line-format protocol to the compiled binary.
This lets the per-topic Rust / C++ sources stay free of any JSON dependency
while reusing the canonical fixtures.

## Architecture notes

* **Single source of truth**: every language harness reads the same
  `tests/cases/<topic>.json` files. If you change a fixture, all languages
  see the change next run.
* **Reference modules contain ONLY pure functions** — no `print`, no
  `input()`, no module-level side effects. They are extracted from the
  Week N teaching files (the originals stay untouched to preserve the
  learning narrative including their demo `main()` blocks).
* **Determinism**: algorithms whose result is not unique (topological sort,
  group anagrams, etc.) use a deterministic tie-break in the reference.
  Document this contract in the reference docstring so the corresponding
  C++/Java/Rust drivers can mirror it when you extend them.
* **Failure reporting**: when a case fails the harness prints a 4-line block
  with topic, case name, input, expected, and got values. Suitable for
  copy-pasting into bug reports.

## Future work

The list of fixtures is currently 25 topics, all passing under Python.
Extending the non-Python harnesses to all 25 is mechanical (see the recipes
above). Stretch goals:

* Wrap every Week N (`/cpp`, `/java`, `/rust`) implementation rather than
  re-creating the algorithm in `tests/refs/`. This requires per-language
  parsing of those files' module-level code, or refactoring those files to
  separate `main` from the function. Today we sidestep this for Python by
  duplicating the pure function into `tests/refs/`; the same pattern
  generalises.
* Add a `--diff` mode showing the first difference between expected and got
  for list outputs.
* Add a benchmark mode that runs each case repeatedly and reports wall time
  by language — useful for the "Python vs Java" learning notes in the
  README files.
