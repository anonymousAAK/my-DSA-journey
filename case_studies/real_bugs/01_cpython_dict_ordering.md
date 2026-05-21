# Bug Case Study: Test suites broken by Python 3.6's dict-ordering change

**Project**: CPython (PEP 468 / PEP 520 era — dict insertion-ordering became a language guarantee in 3.7). Approximate reconstruction of a class of bug seen across hundreds of OSS Python projects when they moved to 3.6+.
**Date**: 2016–2017 (3.6 made dicts ordered as an implementation detail; 3.7 made it a guarantee)
**Severity**: correctness (mostly tests; occasionally production output)
**DSA principle**: hash tables don't have an inherent order — Week 16

## What happened

For ~25 years, CPython's `dict` was an open-addressed hash table whose iteration order depended on the hash of each key and the current table size. Two `dict`s with the same keys could iterate in different orders on different runs (and after PEP 456 hash randomization was enabled by default in 3.3, two runs of the *same program* would iterate differently).

A huge amount of Python code in the wild quietly relied on a *specific* iteration order anyway. The most common smell was tests that asserted `list(d.keys()) == ["a", "b", "c"]` or that compared two `repr(d)` strings. These tests passed on a single developer's laptop and then broke under tox / CI / pytest-randomly. When 3.6's compact-dict implementation made insertion order incidentally stable, a *second* wave of bugs emerged: code that started silently depending on insertion order in 3.6 broke when ported back to 3.5, or when a `dict()` call was replaced by a `**kwargs` construction in pre-3.7.

Django, Flask, requests, SQLAlchemy and many smaller projects all had at least one issue in their tracker that boiled down to "we relied on dict order, which is not a property of dicts."

## The naive code

```python
# A test that "passes" — until hash randomization or a Python upgrade kicks in.
def test_serialize_user():
    user = {"name": "Ada", "role": "admin", "id": 1}
    assert json.dumps(user) == '{"name": "Ada", "role": "admin", "id": 1}'

# Production code that happened to work on the dev laptop:
def first_field(d):
    return next(iter(d))   # which field? whichever the hash table decided.
```

## The DSA insight

A hash table is, by definition, an *unordered* associative container. The iteration order is an artefact of `hash(key) % table_size`, the open-addressing probe sequence, and how full the table is. Nothing in the hash-table contract promises stability across:

- different keys,
- different insertion orders,
- different Python versions,
- different runs (with PYTHONHASHSEED randomisation),
- different table sizes (a single insert can trigger a resize and reshuffle every key).

If you need *order*, you need a data structure that carries order as part of its contract — a `list`, a sorted container, or an `OrderedDict` (which is a doubly-linked list grafted onto a hash table specifically to maintain insertion order). Confusing "happens to be ordered in this build" with "ordered" is the root cause.

See Week 16's notes on hash-table fundamentals and the `Week 16/python/hashmap_anatomy.py` walkthrough for why iteration order is incidental.

## The fix

```python
# 1. Compare against the data, not against a serialization order:
def test_serialize_user():
    user = {"name": "Ada", "role": "admin", "id": 1}
    decoded = json.loads(json.dumps(user))
    assert decoded == {"name": "Ada", "role": "admin", "id": 1}

# 2. If you need a stable serialization, ask for one:
json.dumps(user, sort_keys=True)

# 3. If you need a "first" element, define what first means:
def first_field(d):
    return min(d)            # alphabetical
    # or: return next(iter(OrderedDict(items_in_known_order)))
```

## What you can learn

- Hash tables are unordered — treat any observed order as coincidence, not a contract.
- A test that pins an unstable property turns from a safety net into a source of flakes the moment something underneath changes.
- "It works on my machine" is a *symptom of relying on an implementation detail*; the fix is to remove the dependency, not to pin the implementation.
- Even when a language eventually formalises an implementation detail (Python 3.7 did), the years of code written before then expose the same lesson.

## Related curriculum
- Week 16 (Hashing and hash maps)
- `tests/cases/hashmap_anatomy.json` — try the canonical version and see if you can write a fixture that fails when `PYTHONHASHSEED` is varied.
