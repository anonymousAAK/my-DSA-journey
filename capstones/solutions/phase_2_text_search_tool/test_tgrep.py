"""Tests for tgrep. Run: python test_tgrep.py"""
from __future__ import annotations

import os
import sys
import tempfile

from tgrep import (
    build_index,
    glob_match,
    literal_search,
    prefix_sum,
    search_file,
    walk_files,
)


def test_literal_search() -> None:
    assert literal_search("abcabc", "abc") == [0, 3]
    assert literal_search("aaaa", "aa") == [0, 1, 2]
    assert literal_search("hello", "x") == []
    assert literal_search("", "x") == []
    assert literal_search("abc", "") == []


def test_glob_match() -> None:
    assert glob_match("hello world", "hello")
    assert glob_match("hello world", "h?llo")
    assert glob_match("hello world", "h*o")
    assert glob_match("hello world", "*world")
    assert glob_match("hello world", "hello*")
    assert glob_match("hello world", "*")
    assert not glob_match("hello", "xyz")
    assert not glob_match("hello", "h?xlo")
    assert glob_match("abcXYZdef", "abc*def")
    assert glob_match("abcdef", "abc*def")
    assert not glob_match("abc", "abc*def")


def test_prefix_sum() -> None:
    assert prefix_sum([]) == [0]
    assert prefix_sum([1, 0, 1, 1]) == [0, 1, 1, 2, 3]


def test_index_and_range() -> None:
    sample = (
        "alpha line\n"
        "beta line\n"
        "alpha alpha\n"
        "nothing\n"
        "the end alpha\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "f.txt")
        with open(path, "w") as fh:
            fh.write(sample)
        idx = search_file(path, "alpha", use_glob=False, ignore_case=False)
        assert idx is not None
        # 3 lines contain 'alpha' (lines 1, 3, 5)
        assert idx.prefix[-1] == 3
        assert idx.matches_in_range(1, 5) == 3
        assert idx.matches_in_range(1, 2) == 1
        assert idx.matches_in_range(2, 4) == 1
        assert idx.matches_in_range(3, 5) == 2
        assert idx.matches_in_range(100, 200) == 0


def test_case_insensitive() -> None:
    flags = build_index(["Hello", "HELLO", "world"], "hello", use_glob=False, ignore_case=True)
    assert flags == [1, 1, 0]
    flags = build_index(["Hello", "HELLO", "world"], "hello", use_glob=False, ignore_case=False)
    assert flags == [0, 0, 0]


def test_glob_via_build_index() -> None:
    flags = build_index(["foo.py", "bar.txt", "baz.py"], "*.py", use_glob=True, ignore_case=False)
    assert flags == [1, 0, 1]


def test_recursive_walk() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        os.makedirs(os.path.join(tmp, "sub"))
        for rel in ("a.txt", "sub/b.txt", "sub/c.txt"):
            with open(os.path.join(tmp, rel), "w") as fh:
                fh.write("alpha\n")
        found = sorted(walk_files([tmp], recursive=True))
        assert len(found) == 3
        flat = sorted(walk_files([tmp], recursive=False))
        assert len(flat) == 1  # only a.txt at top level


def main() -> int:
    test_literal_search()
    test_glob_match()
    test_prefix_sum()
    test_index_and_range()
    test_case_insensitive()
    test_glob_via_build_index()
    test_recursive_walk()
    print("tgrep: all tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
