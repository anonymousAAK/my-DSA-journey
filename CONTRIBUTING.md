# Contributing to `my-DSA-journey`

Thank you for wanting to make this repo better. The 30-week curriculum lives or dies by consistency: five language tracks, hundreds of files, and a quality lint that fails the build the moment a corner drifts. This document is the contract between you and the repo so your contribution lands cleanly the first time.

If you only read one section, read **Code conventions** and **Quality lint** below — together they cover roughly 90% of why a PR is bounced.

---

## How to contribute

There are three shapes of contribution. Pick the one that matches what you're doing — the workflow differs.

### 1. Reporting a bug in code

A bug is anything that compiles wrong, prints the wrong output, or breaks when you run it as documented. Specifically:

- A file fails to compile or run.
- A function returns the wrong answer for a stated input.
- A smart quote (`'`, `'`, `"`, `"`) has leaked into a `.java`/`.py`/`.cpp`/`.rs` file (the Java compiler rejects these outright).
- A header section that the quality lint requires is missing.
- A test in `tests/` fails on `main`.

**Action**: open an issue using the [bug template](.github/ISSUE_TEMPLATE/bug.yml). Don't open a PR first — we want to triage the bug into the right week / language track before code is written, because the same logical bug often hides in three sibling files and a one-line fix turns into a four-file fix.

### 2. Suggesting a new topic file

Adding a *new* topic to an existing week (or proposing a new sub-section) is a meaningful change to the curriculum and needs a quick scope conversation before you write code.

**Action**: open a [topic-request issue](.github/ISSUE_TEMPLATE/topic_request.yml) describing the proposed topic, which week it belongs in, and why it earns a numbered slot rather than living as a supplementary note. Wait for a thumbs-up before opening a PR — this saves you from writing five language implementations of something that turns out to belong in a different week.

### 3. Submitting a correction

A correction is a small, isolated fix where the right answer is unambiguous:

- A typo or grammar error.
- A broken external link.
- A factual error (a wrong complexity, a misnamed algorithm, a citation that's been refuted).
- A clarification (one or two sentences, not a rewrite).

**Action**: open a [correction issue](.github/ISSUE_TEMPLATE/correction.yml). For trivial typos you may open the PR at the same time and link them.

---

## Code conventions

### Header block

Every numbered topic file in `Week 1` through `Week 24` (and the topic files in `Weeks 25-30`) must include the following sections in its header comment block. The quality lint (`scripts/quality_check.py`) checks for at least one token from each group, case-insensitive, in the first 200 and last 40 lines of the file.

**Required sections:**

- `CONCEPT` — one paragraph stating what the topic is.
- `KEY POINTS` — bulleted essential ideas.
- `SYNTAX` *or* `ALGORITHM` (alias: `APPROACH`) — the language-level skeleton or the algorithmic pseudocode.
- `DRY RUN` *or* `EXAMPLE` — a worked walkthrough on a small input.
- `COMPLEXITY` — time and space.
- `NOTES` (alias: `NOTE:`) — the cross-language sidebar. What's idiomatic in *this* language that differs from Java?

For `.html` files we only require a `<!-- WEEK N` comment near the top — the embedded JS varies too much to schematize.

If you're new to the repo, copy the header from a neighbouring file rather than inventing the structure from scratch.

### File naming conventions

**Weeks 1-24** use a numeric prefix that establishes a 1:1 mapping across the five language tracks:

```
Week N/java/<n>.<TopicName>.java       # CamelCase for Java
Week N/python/<n>.<snake_case>.py
Week N/cpp/<n>.<snake_case>.cpp
Week N/rust/sNN_<snake_case>.rs        # Rust uses sNN_ instead of N. because rustc rejects leading-digit module names
Week N/web/<n>.<snake_case>.html
```

Java's `<n>.<TopicName>.java` filename collides with the requirement that the public class match the filename, so **Java files in Weeks 1-24 use package-private (no `public`) classes** and the topic name without the numeric prefix becomes the class name. This is a deliberate, repo-wide convention — don't "fix" it by removing the prefix.

**Weeks 25-30** drop the numeric prefix entirely and use `<topic_name>.<ext>` (e.g. `aho_corasick.py`, `network_flow.cpp`). The cross-language consistency check matches by stem alone in this range.

For everything: `snake_case` for non-Java, `CamelCase` for Java types, lowercase-and-hyphenated for LeetCode URLs in `problems.md`.

### Build-everything-before-pushing

Run from the repo root:

```bash
./scripts/build_all.sh all
```

This compiles every Java, C++, and Rust file in every week, and syntax-checks every Python file. **Every file must compile.** Failing to compile is the single most common reason a PR is bounced — local laziness becomes CI noise.

### Quality lint

Run from the repo root:

```bash
python scripts/quality_check.py
```

Must exit `0`. If you've added drift the lint will say so. See **Quality lint** below for what each check does and how to fix the common failure modes.

### Adding a fixture and reference (for topic files)

If your new file implements an algorithm that has a `tests/cases/<topic>.json` fixture, the test harness will pick it up automatically. If you're adding a brand-new topic that *deserves* a fixture (most algorithmic ones do):

1. Add `tests/cases/<topic>.json` following `tests/SCHEMA.md`.
2. Add a Python reference at `tests/refs/<topic>.py` exporting the canonical function.
3. Run `python tests/harness/harness.py --all` — must pass.

The cross-language harnesses (Java, C++, Rust) read the same fixture; extending them is mechanical once Python passes. See `tests/README.md`.

---

## Testing

### How the harness works

`tests/harness/harness.py` is the reference test runner. For each topic that has a `tests/cases/<topic>.json` fixture *and* a `tests/refs/<topic>.py` reference, it:

1. Loads the JSON, which is a list of cases, each with `input` (a JSON array of positional args) and `expected` (the value the function must return, compared by deep equality).
2. Imports `tests/refs/<topic>.py` and calls the function whose name is given by the `function` field.
3. Prints `PASS topic :: case` or `FAIL topic :: case (got X, expected Y)`.

The C++, Rust, and Java harnesses (`harness_cpp.sh`, `harness_rust.sh`, `Harness.java`) consume the same fixture JSON so a single test definition exercises all four languages.

### Adding a fixture

See `tests/SCHEMA.md` for the full schema. The minimum:

```json
{
  "topic": "kadane_max_subarray",
  "week": 6,
  "function": "maxSubarraySum",
  "cases": [
    {"name": "basic", "input": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6},
    {"name": "empty", "input": [[]], "expected": 0, "edge": true}
  ]
}
```

Conventions worth internalising:

- `input` is **always** a JSON array of positional args. If your function takes a single list, wrap it once more in `input` (as above).
- Include at least one `edge` case (empty input, single element, boundary).
- For algorithms whose output is order-dependent (topological sort, group anagrams), the reference function must normalise its output (sort, canonicalise) before returning so `expected` can be canonical too.

---

## Quality lint

`scripts/quality_check.py` runs eight checks. Each is cheap, each fires fast, and each catches a specific failure mode the repo has historically suffered.

1. **`headers`** — every numbered topic file has `CONCEPT`, `KEY POINTS`, `SYNTAX`/`ALGORITHM`, `DRY RUN`/`EXAMPLE`, `COMPLEXITY`, `NOTES`/`NOTE:`. Without these tokens you cannot grep the repo for asymptotic analysis or the cross-language sidebar.
2. **`patterns`** — each `Week N/patterns.md` has at least 10 numbered drills, an `## Answer Key` (or `<details>`), and at least 10 `Pattern:` and 10 `Why:` blanks for the learner to fill in.
3. **`challenges`** — each `Week N/challenges.md` has at least 3 `## Challenge N:` headers, each with `**Spec**`, `**Constraints**`, `**Test inputs**`, and at least one markdown table.
4. **`readme`** — each `Week N/README.md` has `## Tradeoff Matrix`, `## Anti-patterns to avoid`, `## Reflection prompts`, and a topic-index table mentioning at least three languages in its header row.
5. **`consistency`** — every Java topic in `Week N/java/` has an equivalently named counterpart in `python/`, `cpp/`, `rust/`, *and* `web/`. CamelCase ↔ snake_case differences and Rust's `sNN_` prefix are tolerated.
6. **`leetcode`** — every `https://leetcode.com/problems/<slug>/` URL in `problems.md` has a lowercase, hyphenated, single-segment slug (no network call — slug format only).
7. **`smart_quotes`** — no U+2018/U+2019/U+201C/U+201D in any `.java`/`.py`/`.cpp`/`.rs` file. These cause silent Java compile failures and sneak in through copy-paste.
8. **`docs`** — required top-level docs (`PROBLEM_SOLVING.md`, `LICENSE`, `README.md`, `docs/SOLUTION_JOURNAL.md`, `docs/estimation.md`, `docs/REVIEW_SCHEDULE.md`, `.github/workflows/build.yml`, `scripts/build_all.sh`) exist.

### Debugging a header-missing failure

The most common lint failure looks like:

```
HEADER_MISSING tokens=[COMPLEXITY] file=Week 6/python/3.kadane.py
```

Open the file. Search for `COMPLEXITY` — if it isn't there, add one of:

```python
# COMPLEXITY: O(n) time, O(1) space
```

or, in a docstring:

```python
"""
...
COMPLEXITY:
    time:  O(n)
    space: O(1)
"""
```

The token can be anywhere in the first 200 lines or the last 40 lines. Likewise for missing `NOTES:`, add a short cross-language remark at the bottom of the file (one or two bullets is fine — what's idiomatic in this language that the Java version doesn't have?).

If you genuinely think a *category* of file should be exempt (e.g. a new file type), don't add a per-file ignore — instead open an issue or PR adjusting `REQUIRED_TOKENS_GROUPS` in `quality_check.py`. The script is living code and the conventions evolve with the curriculum.

Full details: `scripts/QUALITY_CHECK.md`.

---

## Per-week structure

Every week folder must contain:

```
Week N/
├── README.md         # Includes Tradeoff Matrix, Anti-patterns, Reflection prompts, topic-index table
├── problems.md       # LeetCode-style problems with valid slugs
├── patterns.md       # 10+ drills with Pattern: / Why: blanks and an Answer Key
├── challenges.md     # 3+ challenges with Spec / Constraints / Test inputs and a table
├── mastery.yml       # YAML rubric of mastery checkpoints for the week
├── java/             # Java implementations, numbered (Weeks 1-24) or named (Weeks 25-30)
├── python/           # 1:1 counterpart of every Java topic
├── cpp/              # 1:1 counterpart of every Java topic
├── rust/             # 1:1 counterpart of every Java topic
├── web/              # 1:1 counterpart of every Java topic + index.html overview
```

The five language folders each contain one file per topic, with names that satisfy the consistency check.

When adding a topic file, you must add it in **all five languages at once** (java, python, cpp, rust, web). The consistency check will fail otherwise. There is no "I'll add the C++ later" path — it always becomes never.

---

## Mock interview / case study / capstone contributions

The `mock_interviews/`, `case_studies/`, and `capstones/` folders are lower-priority but very welcome contributions. Each has its own established format — read two or three existing files in the same folder before writing yours and match the structure. In particular:

- **Mock interviews** follow the transcript-and-debrief format. The debrief is more valuable than the transcript.
- **Case studies** in `case_studies/real_world/` are systems built by real companies; in `case_studies/` they are illustrative pedagogical examples. Don't mix the two.
- **Capstones** in `capstones/` have a spec file + a reference solution under `capstones/solutions/phase_N_<name>/`. If you propose a new capstone, both pieces are required.

---

## Pull request flow

### Branch naming

- `claude/<short-topic>` — automated Claude-Code contributions
- `codex/<short-topic>` — automated Codex contributions
- `contrib/<github-username>/<short-topic>` — human contributors

Branch names that don't match one of these prefixes pass CI but are easier for maintainers to triage when they do.

### Required CI checks

Every PR must pass these jobs in `.github/workflows/build.yml`:

- `python` — Python files import-check / smoke-run.
- `cpp` — every C++ file compiles under `g++ -std=c++17`.
- `rust` — every Rust file compiles under `rustc`.
- `java` — every Java file compiles under `javac`.
- `tests-python` (and the per-language harness jobs) — fixture-driven tests pass.
- `quality` — `python scripts/quality_check.py --quiet` exits 0.

If any one of these is red, the PR will not be merged.

### PR template

The repo has a pull-request template at `.github/PULL_REQUEST_TEMPLATE.md` that will populate automatically. Fill it out completely — especially the checklist. The single most common failure mode is "I ran the build, I just forgot to run the lint."

---

## Translations

The repo's foundational mindset docs are available in Hindi, Spanish, and Mandarin under `translations/<lang>/`. To add a new language:

1. Create `translations/<iso-code>/` (e.g. `translations/fr/` for French).
2. Translate at minimum: `PROBLEM_SOLVING.md`, `QUICKSTART.md`, `docs/diagnostic.md`, and a partial `README.md` (focus on Start Here + Learning Paths sections).
3. At the top of each translated file, add a one-line note:
   > This is a translation of the English original. If unclear, refer to [the English version](../../FILE.md).
4. Preserve code blocks unchanged — code stays English.
5. Preserve markdown structure (headings, tables, lists).
6. Update the root `README.md` "🌍 Languages" line to include your locale.
7. Open a PR. Native-speaker review welcome — most current translations are AI-assisted and would benefit from refinement.

Avoid word-for-word translation of technical terms; use what speakers in the target language actually use (e.g. "binary search" in Hindi is often left transliterated in English mid-sentence).

## Community

Code contributions aren't the only way to make this repo better. There's a lot of value in being a present, helpful voice in the community around it.

- **GitHub Discussions** is the home for questions, study-buddy pairing, capstone show-and-tell, and big-picture career chat. See [`docs/DISCUSSIONS.md`](docs/DISCUSSIONS.md) for the full category map. Two categories worth highlighting:
  - **Stuck on a problem?** — Q&A format. Ask once, search forever. Helping here is one of the highest-leverage things you can do.
  - **Can't see the pattern?** — for the upstream skill of *classifying* a problem before you solve it.
- **Showcase** — finished a capstone? [Submit it to the public showcase](showcase/README.md). Other learners use these as inspiration for what's possible.
- **Weekly digest** — for low-bandwidth contact with the repo, subscribe to the [weekly RSS feed](docs/NEWSLETTER.md). One case study, one drill, one challenge per week.
- **Daily-practice issues** — if you'd like a daily nudge, watch the `daily-practice` label. The bot opens one issue every weekday with a 25-minute practice plan. See [`docs/DAILY_PRACTICE.md`](docs/DAILY_PRACTICE.md).

When you participate in discussions, the rule of thumb mirrors the code conventions: be the kind of contributor that the learner reading this thread three years from now will be glad existed.

---

## Code of Conduct

This project follows the spirit of the [Contributor Covenant](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). There is no separate `CODE_OF_CONDUCT.md` file yet; until there is, treat the Covenant text as authoritative: be respectful, assume good faith, criticise code not people, and remember that a learner reading this repo three years from now is the audience you're writing for.

If you encounter behaviour that violates the Covenant, open an issue tagged `conduct` or contact the maintainers directly.

---

Thank you for contributing. Every fixed typo, every new topic file, every clarified complexity comment is one less moment of confusion for the next learner who picks this up.
