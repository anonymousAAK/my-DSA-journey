# Master Index

Every doc in this repo, grouped by purpose. Skim it once to know what exists; come back when you need something specific.

> New here? Start with [QUICKSTART.md](QUICKSTART.md). Already convinced? Jump to [Week 1](Week%201/).

---

## 🚀 Start here

- [`QUICKSTART.md`](QUICKSTART.md) — 4-hour curriculum to see if this works for you.
- [`docs/diagnostic.md`](docs/diagnostic.md) — 15-question placement test that maps your score to a starting week.

---

## 🧠 Mindset & methodology

- [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) — How to think like a problem solver.
- [`docs/SOLUTION_JOURNAL.md`](docs/SOLUTION_JOURNAL.md) — Template for journaling every problem you solve.
- [`docs/estimation.md`](docs/estimation.md) — 25 drills for complexity / hardware-budget intuition.
- [`docs/REVIEW_SCHEDULE.md`](docs/REVIEW_SCHEDULE.md) — Spaced-repetition + interleaving plan (hand-curated revisit table).
- [`docs/SPACED_REPETITION.md`](docs/SPACED_REPETITION.md) — FSRS-driven adaptive scheduler powering `journey review`.
- [`docs/MASTERY.md`](docs/MASTERY.md) — Why mastery quizzes matter and how the CLI works.

---

## 📚 Curriculum

[`Week 1/`](Week%201/) through [`Week 30/`](Week%2030/) — Each week contains:

- `java/`, `python/`, `cpp/`, `rust/`, `web/` — 1:1 per-topic implementations across all four languages plus interactive HTML.
- `README.md` — week overview, topic index, tradeoff matrix, anti-patterns, reflection prompts.
- `problems.md` — curated LeetCode problems for this week.
- `patterns.md` — pattern-recognition drills with hidden answer keys.
- `challenges.md` — "implement without peeking" hard-mode challenges.
- `mastery.yml` — skill-check fixtures driven by `./scripts/journey quiz N`.

---

## 🛣️ Real-world & interview prep

- [`case_studies/`](case_studies/) — 6 phase walkthroughs from messy problems to algorithms.
- [`case_studies/real_world/`](case_studies/real_world/) — 15 essays mapping algorithms to real products.
- [`case_studies/real_bugs/`](case_studies/real_bugs/) — 15 short case studies of real OSS bugs whose root cause was a DSA principle from this curriculum.
- [`mock_interviews/`](mock_interviews/) — 8 annotated interview transcripts, including one bombed interview as a negative example.

---

## 🎯 Capstones

- [`capstones/`](capstones/) — 6 multi-weekend project specs (one per curriculum phase).
- [`capstones/solutions/`](capstones/solutions/) — working Python reference implementations + tests + design READMEs.

---

## ✅ Testing & quality

- [`tests/SCHEMA.md`](tests/SCHEMA.md) — `cases.json` fixture schema.
- [`tests/cases/`](tests/cases/) — 25 per-topic correctness fixtures.
- [`tests/refs/`](tests/refs/) — pure reference functions.
- [`tests/harness/`](tests/harness/) — multi-language test runner.
- [`tests/COVERAGE.md`](tests/COVERAGE.md) — current per-week coverage % (auto-generated).
- [`scripts/quality_check.py`](scripts/quality_check.py) — 8-category schema/consistency lint.
- [`scripts/QUALITY_CHECK.md`](scripts/QUALITY_CHECK.md) — what each check tests and how to fix failures.

---

## 🛠️ Tools

- [`scripts/build_all.sh`](scripts/build_all.sh) — local equivalent of CI smoke test.
- [`scripts/journey`](scripts/journey) — mastery quiz CLI; `progress` shows dashboard; `progress --html` opens visual dashboard.
- [`scripts/coverage_report.py`](scripts/coverage_report.py) — regenerates `tests/COVERAGE.md`.
- [`scripts/ask`](scripts/ask) — AI tutor CLI; ask natural-language questions, get answers retrieved from this repo (offline by default, optional `--llm` mode). See [`docs/AI_TUTOR.md`](docs/AI_TUTOR.md).

---

## 🎨 Visualizations

- [`viz/index.html`](viz/index.html) — interactive algorithm visualizations (sorting, binary search, BFS/DFS, Dijkstra, segment tree, recursion tree, DP table). Vanilla JS, no build step — open in any browser.

---

## 🤝 Contributing

- [`CONTRIBUTING.md`](CONTRIBUTING.md) — conventions, header schema, PR flow.
- [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/) — bug, topic request, correction.
- [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md) — PR template.
- [`LICENSE`](LICENSE) — MIT.
