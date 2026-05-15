# Quality Check

`scripts/quality_check.py` is a stdlib-only Python script that validates
schema and consistency across the DSA learning repo. It runs eight checks
and exits non-zero when any of them fail.

## Philosophy

This project lives or dies by consistency. Five language tracks, thirty
weeks, hundreds of files. The instant one corner drifts — a header section
missing here, a smart-quote pasted from a chat there, a Java topic with no
Python counterpart — the cross-language story stops working and the build
silently degrades.

`quality_check.py` is the canary. It runs locally in seconds and on every
push in CI. It does **not** auto-fix anything; auto-fixers paper over the
drift instead of teaching us where it came from. The script tells you what
looks wrong, and you decide whether to fix the file or to update the
checker because the convention has legitimately changed.

The cost of catching drift here is cheap. The cost of catching it after it
lands in main and propagates across a week's worth of new topic files is
not.

## Usage

```bash
python scripts/quality_check.py                # full check
python scripts/quality_check.py --check headers # one check only
python scripts/quality_check.py --json          # machine-readable output
python scripts/quality_check.py --quiet         # only print failures
```

Valid `--check` values: `headers`, `patterns`, `challenges`, `readme`,
`consistency`, `leetcode`, `smart_quotes`, `docs`.

Exit code is `1` if any check found at least one issue; `0` otherwise.

## What each check looks for

### 1. Code file headers (`headers`)

For every numbered topic file (`Week N/<lang>/<num>.<name>.<ext>` or Rust's
`sNN_name.rs`), the header must include — case-insensitive — at least one
token from each of these groups:

- `CONCEPT`
- `KEY POINTS`
- `DRY RUN` *or* `EXAMPLE`
- `COMPLEXITY`
- `NOTES` *or* `NOTE:`

The scan covers the first 200 lines plus the last 40 lines so that
`NOTES:` blocks at the bottom of a Python file still count. For `.html`
files we only require a `<!-- WEEK N` comment near the top — the rest of
the structure varies too much.

**Why**: this is the shared narrative scaffolding of every topic file. If
a file is missing `COMPLEXITY`, you cannot grep the repo for asymptotic
analysis. If it is missing `NOTES`, you cannot find the cross-language
sidebar.

### 2. `patterns.md` schema (`patterns`)

Each `Week N/patterns.md` must have:

- At least 10 numbered drills (`### 1.` … `### 10.`)
- A `## Answer Key` section or a `<details>` block
- At least 10 `Pattern:` lines and at least 10 `Why:` lines

**Why**: the drill format teaches pattern recognition by repetition. Missing
`Pattern:` / `Why:` blanks means there is nothing for the learner to fill in.

### 3. `challenges.md` schema (`challenges`)

Each `Week N/challenges.md` must have:

- At least 3 `## Challenge N:` headers
- Each challenge must contain `**Spec**`, `**Constraints**`, `**Test inputs**`
- Each challenge must contain at least one markdown table with a header
  row, separator row, and at least one data row (the test-input table)

**Why**: the challenge format is uniform on purpose. The learner is
supposed to be able to predict where the spec / constraints / test inputs
live before reading them.

### 4. Per-week README sections (`readme`)

Each `Week N/README.md` must contain:

- `## Tradeoff Matrix`
- `## Anti-patterns to avoid`
- `## Reflection prompts`
- A topic-index table (markdown table whose header row mentions at least
  three of: java, python, c++, cpp, rust, web)

**Why**: these sections are how a week's README becomes pedagogically
useful instead of a glorified directory listing.

### 5. Cross-file consistency (`consistency`)

For each Java topic in `Week N/java/<num>.<name>.java`, verify that an
equivalently named file exists in `python/`, `cpp/`, `rust/`, and `web/`.
Naming differences are tolerated:

- Case + snake_case differences (`Hello_World` ↔ `hello_world`)
- Rust's `sNN_name.rs` convention
- CamelCase split into snake_case (`BubbleSelectionInsertion` ↔
  `bubble_selection_insertion`)
- Spaces collapsed to underscores
- Weeks 26-30 are matched by stem (no numeric prefix)

Extension-less stub files in `java/` (e.g. `1.Java Installation`) are
ignored — they are tutorial scaffolds, not source files.

**Why**: each topic should be implementable in every language; missing
counterparts mean a topic isn't truly cross-language yet.

### 6. LeetCode link health (`leetcode`)

Extract every `https://leetcode.com/problems/<slug>/` URL from
`Week N/problems.md`. Validate the slug format only — no network calls.

A slug is valid if it is lowercase, hyphenated, with no double slashes,
no embedded whitespace, no trailing punctuation, and no uppercase chars.

**Why**: malformed slugs are silent 404s. Catching them at PR time is
much cheaper than catching them on review night.

### 7. Smart-quote detection (`smart_quotes`)

Scan every `.java`, `.py`, `.cpp`, `.rs` file for U+2018, U+2019, U+201C,
U+201D. These cause Java compile failures (we've already fixed three) and
sneak in through copy-paste from chat windows and word processors.

**Why**: hard to spot visually; easy to detect mechanically.

### 8. Required top-level docs (`docs`)

Verify these files exist:

- `PROBLEM_SOLVING.md`
- `LICENSE`
- `README.md`
- `docs/SOLUTION_JOURNAL.md`
- `docs/estimation.md`
- `docs/REVIEW_SCHEDULE.md`
- `.github/workflows/build.yml`
- `scripts/build_all.sh`

**Why**: anything imported by the README must continue to exist.

## How to fix common failures

### `HEADER_MISSING tokens=[COMPLEXITY] file=...`

Open the file and add a `COMPLEXITY:` line (or `COMPLEXITY: O(...)` inside
the existing docstring/comment block). For most fundamentals-style topics
the answer is `COMPLEXITY: O(1)` for a single statement, `O(n)` for a
loop, etc.

### `HEADER_MISSING tokens=[NOTES] file=...`

Add a `NOTES:` section, typically at the bottom of the file, summarising
the cross-language idiom this file teaches. One or two bullets is fine.

### `CHALLENGES_SCHEMA Challenge N missing: test-input table row`

Make sure the challenge has a markdown table with the standard
three-line shape:

```
| Input | Expected output |
|-------|-----------------|
| 4 6   | 5               |
```

### `COUNTERPART_MISSING java topic 'foo' has no python counterpart`

Either create the missing `python/foo.py` (preferred) or rename the Java
file to match the topic name used in the other languages. Cross-language
consistency is the goal.

### `LEETCODE_MALFORMED url=... reasons=[...]`

Open the URL in a browser. If it 404s, find the correct slug from the
LeetCode problem page and replace the link in `problems.md`. If it works,
the slug probably has a typo (uppercase letter, underscore, trailing
period) that the script flagged.

### `SMART_QUOTE chars=[L30:’] count=1 file=...`

Open the file at the reported line. Replace `’ ‘ “ ”` with their ASCII
equivalents `' '` and `"`. In Java this is mandatory — the compiler will
reject smart quotes.

### `DOC_MISSING ...`

The script expects a file that no longer exists. Either restore the file
or — if it has been intentionally renamed — update the `REQUIRED_DOCS`
list at the top of `quality_check.py`.

## Suppressing / configuring individual checks

`quality_check.py` is deliberately simple: there is no `.qualitycheckrc`
or per-file ignore file. To suppress a check:

- Run only the checks you care about: `python scripts/quality_check.py --check headers`
- Edit the constants at the top of `quality_check.py` (e.g. add a token
  to `REQUIRED_TOKENS_GROUPS`, change `REQUIRED_DOCS`, broaden
  `EXPECTED_EXT_BY_LANG`).
- For one-off exemptions, the right answer is to fix the file, not to
  ignore it. The whole point is that drift is cheap to fix early.

If you have a *category* of false positive (a legitimate file pattern
that the script flags incorrectly), open an issue or PR adjusting the
relevant heuristic in the script. Treating the checker as living code
that evolves with the conventions is healthier than building an
ignore-list culture.

## CI integration

The repo's `.github/workflows/build.yml` runs `quality_check.py --quiet`
in a dedicated `quality` job on every push and pull request. The job
fails iff any check finds an issue.
