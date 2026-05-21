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
files we only require a `<!-- WEEK N` comment near the top, OR a
`<title>Week N - ...</title>` element — the rest of the structure varies
too much.

**Why**: this is the shared narrative scaffolding of every topic file. If
a file is missing `COMPLEXITY`, you cannot grep the repo for asymptotic
analysis. If it is missing `NOTES`, you cannot find the cross-language
sidebar.

#### Tutorial / fundamentals exception (COMPLEXITY)

For files in **Weeks 1-5**, OR for any file whose topic name matches a
tutorial keyword (`hello_world`, `installation`, `data_types`, `typecasting`,
`operators`, `if_else`, `while_loop`, `for_loop`, `break`, `continue`,
`scope_of_variable`, `bitwise_operator`, `infinite_loop`, `taking_input`,
`multiple_input`, `integer_and_string`, `how_integer_is_stored`,
`how_other_datatype`, `arithmetic_operation`, `increment_decrement`,
`precedence_associativity`, `add_two_numbers`, `better_hello`,
`find_character_case`, `for_loop_variations`), the `COMPLEXITY` token is
not required. These files are teaching language syntax (declaring a
variable, the shape of an `if` statement); asymptotic analysis is not the
pedagogical point.

The full set of required tokens still applies — only `COMPLEXITY` is
relaxed.

#### Pedagogical-fragment exception (Java only)

Files listed in **`.ci-skip-java`** (which the CI java-compile job also
skips because they intentionally don't compile — pseudocode fragments,
syntax demos outside any class) are exempt from the header check
entirely.

#### Known-drift exception (`.ci-known-drift.yml`)

Files listed in **`.ci-known-drift.yml`** (at the repo root) are exempt
from the header check, with a human-readable reason recorded next to
each path. Format:

```yaml
# Comments start with '#'.
Week 6/java/1.ReturnArraySum.java: multi-topic survey file; uses sectioned in-file headers, not per-topic schema
Week 1/java/2.hello_world.java: fundamentals-week tutorial; abbreviated header schema (syntax demo)
```

Two categories of legitimate drift live here today:

- **Fundamentals-week tutorials (Weeks 1-5)** that intentionally use an
  abbreviated header schema. Many of these files are demonstrating a
  single language feature (e.g. how `break` works); a worked example
  block and a cross-language NOTES block do not add pedagogical value.
- **Multi-topic survey files (Weeks 6-25 java/web)** that bundle several
  related algorithms into one source file (e.g.
  `BubbleSelectionInsertion.java` covers three sorts). They use
  sectioned in-file headers (`===== BUBBLE SORT =====`,
  `===== SELECTION SORT =====`, ...) rather than the top-of-file per-topic
  token schema. The pedagogical content is present; it is just not
  parseable by the literal `CONCEPT:`/`KEY POINTS:`/etc. check.

**Adding to `.ci-known-drift.yml` is a conscious decision**, not an
ignore-list reflex. It means *this file legitimately does not follow the
schema and that's OK because <reason>*. For new code, the right answer is
to write the file with the full header schema — the drift list was
captured at the point CI flipped from report-only to gating, and new
contributions should not extend it without a documented reason.

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

#### Survey-file exception

Java files whose normalised stem is in the `SURVEY_TOPIC_STEMS` set
(`network_flow`, `geometry`, `game_theory`, `system_design`,
`interview_patterns`, `fundamentals`, `arrays`, `strings`, `searching`,
`sorting`, `matrix`, `linked_lists`, `stacks`, `queues`, `trees`,
`heaps`, `hashing`, `graphs`, `dp`, `greedy`, `backtracking`,
`recursion`, `control_flow`, `string_algorithms`) are treated as
**weekly overviews / cross-cutting surveys**, not per-topic
implementations. They are exempt from the counterpart check because
they exist to give a single-file recap of the week, not to be mirrored
1:1 across all five language tracks.

Files listed in `.ci-skip-java` and `.ci-known-drift.yml` are also
exempt from the counterpart check (they're not standalone topic
implementations).

**Why**: each topic should be implementable in every language; missing
counterparts mean a topic isn't truly cross-language yet. Survey files
are explicitly *not* per-topic and so the rule should not apply.

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

`quality_check.py` is deliberately simple. There are exactly two
exemption mechanisms, both file-based and both readable by humans:

- **`.ci-skip-java`** — pedagogical Java fragments that intentionally
  don't compile (pseudocode, syntax-outside-a-class). Also consumed by
  the CI java-compile job.
- **`.ci-known-drift.yml`** — per-file header-check exemptions, with a
  human-readable reason recorded next to each path. See
  [Known-drift exception](#known-drift-exception-ci-known-driftyml).

For ad-hoc filtering during development:

- Run a single check: `python scripts/quality_check.py --check headers`
- Edit the constants at the top of `quality_check.py` (e.g. extend
  `TUTORIAL_TOPIC_PATTERNS`, `SURVEY_TOPIC_STEMS`, or
  `REQUIRED_DOCS`).

For one-off exemptions, the right answer is almost always to fix the
file, not to ignore it. The whole point is that drift is cheap to fix
early. The two file-based exemption lists exist for *structural* drift
— files whose layout is intentionally different (legacy survey files,
language tutorials with no asymptotic story) — not for "I don't feel
like adding a NOTES block today".

## CI integration

The repo's `.github/workflows/build.yml` runs `quality_check.py --quiet`
in a dedicated `quality` job on every push and pull request. **The job
gates the merge**: a non-zero exit fails the workflow. There is no
`continue-on-error` fallback; quality drift on a PR will block it.

## Runbook — how to fix a quality failure

When a CI run on your PR fails on the `quality` job, the log will end
with one or more lines like:

```
HEADER_MISSING tokens=[COMPLEXITY, NOTES] file=Week 11/python/3.merge_sorted_lists.py
COUNTERPART_MISSING java topic 'lru_cache' has no rust counterpart file=Week 11/java/4.LRUCache.java
LEETCODE_MALFORMED url=https://leetcode.com/problems/Two_Sum/ reasons=[malformed slug ...]
```

Reproduce locally:

```bash
python scripts/quality_check.py            # full output with per-check summary
python scripts/quality_check.py --check headers   # focus on one check
python scripts/quality_check.py --json | jq .     # machine-readable
```

Then, based on the issue code:

| Code | Meaning | Fix |
|---|---|---|
| `HEADER_MISSING tokens=[...]` | A required header token is missing from a numbered topic file. | Add the missing block(s) to the file's header comment. For a one-line `COMPLEXITY:` fix, an O(...) note suffices. See "How to fix" below. |
| `HEADER_UNREADABLE` | The script could not read the file (permissions / encoding). | Fix the file's encoding to UTF-8. |
| `PATTERNS_MISSING` / `PATTERNS_SCHEMA` | A `Week N/patterns.md` is missing or has fewer than 10 drills / Pattern: / Why: lines. | Add the missing drill block(s). |
| `CHALLENGES_MISSING` / `CHALLENGES_SCHEMA` | A `Week N/challenges.md` lacks `**Spec**`, `**Constraints**`, `**Test inputs**`, or a test-input table. | Add the missing block(s) to that challenge section. |
| `README_MISSING` / `README_SECTIONS` | A `Week N/README.md` is missing or lacks a required section / topic-index table. | Add the section. |
| `COUNTERPART_MISSING ... has no <lang> counterpart` | A Java topic has no equivalent file in another language. | Create the missing per-topic file in `python/`, `cpp/`, `rust/`, or `web/`. |
| `LEETCODE_MALFORMED ... reasons=[...]` | A LeetCode URL in `problems.md` has a malformed slug. | Open the URL; copy the correct slug from the LeetCode problem page; replace the link. |
| `SMART_QUOTE chars=[L30:’] count=1` | The file contains U+2018/U+2019/U+201C/U+201D. | Replace the curly quotes with ASCII `'` and `"`. |
| `DOC_MISSING` | A required top-level doc is absent. | Restore the file, or update `REQUIRED_DOCS` in `quality_check.py` if the rename was intentional. |

### When the failure is a *category*, not a file

If you genuinely believe the lint is wrong about a class of file (you
have, say, a new "weekly capstone" file type that should never need
DRY RUN), the right fix is to update `quality_check.py` itself — extend
`TUTORIAL_TOPIC_PATTERNS`, add a new heuristic, etc. Then this doc
should be updated to describe the new exception.

If the file is **structurally drift** (legacy layout, can't be cleanly
fixed without rewriting), add it to `.ci-known-drift.yml` with a
one-line reason. PR reviewers should push back on additions to the
drift list that are not clearly structural.
