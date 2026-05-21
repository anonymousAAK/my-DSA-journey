"""Python correctness-check harness for the DSA repository.

Loads a `cases.json` fixture, imports the matching reference module from
`tests/refs/<topic>.py`, and runs every case through the function named in the
fixture. Reports PASS/FAIL counts and exits non-zero on any failure.

Usage:
    python tests/harness/harness.py cases/kadane_max_subarray.json --lang python
    python tests/harness/harness.py --all
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path
from typing import Any

HARNESS_DIR = Path(__file__).resolve().parent
TESTS_DIR = HARNESS_DIR.parent
REFS_DIR = TESTS_DIR / "refs"
CASES_DIR = TESTS_DIR / "cases"


def _load_ref_module(topic: str):
    """Dynamically import tests/refs/<topic>.py."""
    path = REFS_DIR / f"{topic}.py"
    if not path.exists():
        raise FileNotFoundError(f"reference module not found: {path}")
    mod_name = f"refs_{topic}"
    spec = importlib.util.spec_from_file_location(mod_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = module  # needed for @dataclass and friends
    spec.loader.exec_module(module)
    return module


def _normalise(value: Any) -> Any:
    """Make tuple/list comparison forgiving (JSON has no tuple)."""
    if isinstance(value, tuple):
        return [_normalise(v) for v in value]
    if isinstance(value, list):
        return [_normalise(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalise(v) for k, v in value.items()}
    return value


def _format_failure(topic: str, case_name: str, inputs: Any, expected: Any, got: Any) -> str:
    return (
        f"FAIL {topic} :: {case_name}\n"
        f"  input: {inputs!r}\n"
        f"  expected: {expected!r}\n"
        f"  got: {got!r}"
    )


def run_fixture(fixture_path: Path, verbose: bool = False) -> tuple[int, int, list[str]]:
    """Run all cases in a fixture. Returns (passed, failed, failure_messages)."""
    with fixture_path.open() as fh:
        fixture = json.load(fh)

    topic = fixture["topic"]
    fn_name = fixture["function"]
    cases = fixture["cases"]

    try:
        module = _load_ref_module(topic)
    except FileNotFoundError as exc:
        msg = f"SKIP {topic} :: missing reference module ({exc})"
        print(msg)
        return 0, 0, [msg]

    if not hasattr(module, fn_name):
        msg = f"FAIL {topic} :: reference module has no attribute {fn_name!r}"
        print(msg)
        return 0, len(cases), [msg]

    fn = getattr(module, fn_name)

    passed = 0
    failed = 0
    failures: list[str] = []

    for case in cases:
        if case.get("skip"):
            if verbose:
                print(f"SKIP {topic} :: {case['name']}")
            continue
        name = case["name"]
        inputs = case["input"]
        expected = _normalise(case["expected"])
        try:
            got = fn(*inputs)
        except Exception:
            msg = (
                f"FAIL {topic} :: {name}\n"
                f"  input: {inputs!r}\n"
                f"  exception:\n"
                + "".join("    " + line for line in traceback.format_exc().splitlines(keepends=True))
            )
            print(msg)
            failures.append(msg)
            failed += 1
            continue
        got_norm = _normalise(got)
        if got_norm == expected:
            passed += 1
            if verbose:
                print(f"PASS {topic} :: {name}")
        else:
            msg = _format_failure(topic, name, inputs, expected, got_norm)
            print(msg)
            failures.append(msg)
            failed += 1

    return passed, failed, failures


def run_all(verbose: bool = False) -> int:
    fixtures = sorted(CASES_DIR.glob("*.json"))
    if not fixtures:
        print(f"No fixtures found in {CASES_DIR}", file=sys.stderr)
        return 1

    total_passed = 0
    total_failed = 0
    topic_summary: list[tuple[str, int, int]] = []

    for fixture in fixtures:
        passed, failed, _ = run_fixture(fixture, verbose=verbose)
        total_passed += passed
        total_failed += failed
        topic_summary.append((fixture.stem, passed, failed))

    print()
    print("=" * 60)
    print("Per-topic summary:")
    for topic, p, f in topic_summary:
        flag = "OK" if f == 0 and p > 0 else ("FAIL" if f else "SKIP")
        print(f"  [{flag:4}] {topic:35s} {p:3d} passed, {f:3d} failed")
    print("=" * 60)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed "
          f"across {len(fixtures)} fixtures")

    return 0 if total_failed == 0 else 1


def _run_java(fixture: str | None, run_all_flag: bool) -> int:
    """Compile the Java harness + refs and shell out to it."""
    build_dir = Path(tempfile.gettempdir()) / "jbuild"
    build_dir.mkdir(parents=True, exist_ok=True)
    sources = [str(HARNESS_DIR / "Harness.java"), *sorted(str(p) for p in REFS_DIR.glob("*.java"))]
    rc = subprocess.call(["javac", "-d", str(build_dir), *sources])
    if rc != 0:
        print("javac failed", file=sys.stderr)
        return rc
    if run_all_flag:
        return subprocess.call(["java", "-cp", str(build_dir), "Harness", "--all"])
    if not fixture:
        print("supply a fixture path or --all", file=sys.stderr)
        return 2
    return subprocess.call(["java", "-cp", str(build_dir), "Harness", fixture])


def _run_shell_harness(script: str, fixture: str | None, run_all_flag: bool) -> int:
    """Shell out to harness_cpp.sh or harness_rust.sh."""
    cmd = ["bash", str(HARNESS_DIR / script)]
    if run_all_flag:
        cmd.append("--all")
    elif fixture:
        cmd.append(fixture)
    else:
        print("supply a fixture path or --all", file=sys.stderr)
        return 2
    return subprocess.call(cmd)


def _run_all_langs(fixture: str | None, run_all_flag: bool, verbose: bool) -> int:
    """Run python first (fast), then C++, then Rust. Aggregate exit code."""
    results: list[tuple[str, int]] = []

    print("\n========== python ==========")
    if run_all_flag:
        rc_py = run_all(verbose=verbose)
    else:
        if not fixture:
            print("supply a fixture path or --all", file=sys.stderr)
            return 2
        passed, failed, _ = run_fixture(Path(fixture), verbose=verbose)
        rc_py = 0 if failed == 0 else 1
    results.append(("python", rc_py))

    print("\n========== cpp ==========")
    rc_cpp = _run_shell_harness("harness_cpp.sh", fixture, run_all_flag)
    results.append(("cpp", rc_cpp))

    print("\n========== rust ==========")
    rc_rs = _run_shell_harness("harness_rust.sh", fixture, run_all_flag)
    results.append(("rust", rc_rs))

    print("\n========== summary ==========")
    fail = 0
    for name, rc in results:
        flag = "OK" if rc == 0 else "FAIL"
        print(f"  [{flag:4}] {name}")
        if rc != 0:
            fail = rc
    return fail


def main() -> int:
    parser = argparse.ArgumentParser(description="DSA correctness harness")
    parser.add_argument("fixture", nargs="?", help="Path to a cases.json fixture")
    parser.add_argument("--lang", default="python",
                        choices=["python", "java", "cpp", "rust", "all"],
                        help="Reference-language harness to run "
                             "('all' runs python, then C++, then Rust)")
    parser.add_argument("--all", action="store_true",
                        help="Run every fixture under tests/cases/")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print PASS lines too (default: only FAILs)")
    args = parser.parse_args()

    if args.lang == "java":
        return _run_java(args.fixture, args.all)
    if args.lang == "cpp":
        return _run_shell_harness("harness_cpp.sh", args.fixture, args.all)
    if args.lang == "rust":
        return _run_shell_harness("harness_rust.sh", args.fixture, args.all)
    if args.lang == "all":
        return _run_all_langs(args.fixture, args.all, args.verbose)

    if args.all:
        return run_all(verbose=args.verbose)

    if not args.fixture:
        parser.error("supply a fixture path or --all")

    fixture_path = Path(args.fixture)
    if not fixture_path.is_absolute() and not fixture_path.exists():
        # try relative to tests/
        candidate = TESTS_DIR / args.fixture
        if candidate.exists():
            fixture_path = candidate

    if not fixture_path.exists():
        print(f"fixture not found: {args.fixture}", file=sys.stderr)
        return 2

    passed, failed, _ = run_fixture(fixture_path, verbose=args.verbose)
    print()
    print(f"{fixture_path.name}: {passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
