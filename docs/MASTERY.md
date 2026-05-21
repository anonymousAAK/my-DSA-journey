# Mastery Checkpoints

> Compile-checks confirm your code parses. Mastery checks confirm you understand.

This repo already has a smoke-test pipeline (`scripts/build_all.sh`) that compiles every Java / C++ / Rust file and runs Python through `py_compile`. That pipeline tells you "the code is syntactically valid." It says nothing about whether the *person who wrote the code* still remembers why Kadane resets to zero, or what happens to Dijkstra under negative weights, or how a min-heap of size k finds the K-th largest element.

The **mastery checkpoint** layer fills that gap. Each `Week N/mastery.yml` defines 5–8 small "can-you-do-this-in-five-minutes-without-looking?" checks of five flavours:

1. **Numeric / computational** — apply the algorithm by hand to a tiny input.
2. **Complexity** — what's the time/space cost of approach X?
3. **Pattern recognition** — which technique fits this problem description?
4. **Concept / failure mode** — explain why approach Y breaks on input Z.
5. **Applied judgement** — at scale N = 10⁹, which approach survives?

The questions are intentionally short. The goal is **recall under time pressure**, not extensive practice — that's what `problems.md` and `challenges.md` are for. Think of mastery checks as a daily 5-minute warm-up.

---

## Philosophy

- **Recognition over recall.** If you can solve the LeetCode problem when told "use Dijkstra," but you can't recognise that a vague road-network question *is* a Dijkstra problem, you haven't mastered Dijkstra — you've mastered "Dijkstra problems labelled Dijkstra." Mastery checks deliberately drop the label.
- **Spacing > cramming.** A 5-minute check three days after learning a topic beats a 30-minute re-read on day 1 *plus* never thinking about the topic again. The CLI tracks dates so you can see what's gone stale.
- **Interleaving.** `journey quiz all` picks random questions across weeks. Performance feels worse than blocked practice — that's the recognition muscle being worked. (See `REVIEW_SCHEDULE.md` for the science.)
- **Cheap to fail.** Each question is fast enough that getting one wrong costs you 30 seconds. Failing fast = failing often = learning often.

---

## File format (`Week N/mastery.yml`)

```yaml
week: 6
title: Arrays
skills:
  - id: kadane_basic
    prompt: "Given [-2,1,-3,4,-1,2,1,-5,4], return the maximum subarray sum."
    answer: 6
    type: numeric
    explanation: "Kadane: running sum, reset to 0 when negative, track max."
```

Each skill has:

| Field | Meaning |
|-------|---------|
| `id` | Stable, short snake_case identifier — used in progress tracking. |
| `prompt` | Short question. Should be answerable in ≤5 min by mental work. |
| `answer` | The expected answer (shape depends on `type`). |
| `type` | One of `numeric`, `string`, `list`, `multiple_choice`, `open`. |
| `explanation` | One- to two-sentence "why" — printed after the question. |
| `choices` | (For `multiple_choice` only.) The list of options shown to the learner. |

### Answer-matching semantics

- `numeric` — exact numeric comparison (floats allowed).
- `string` — exact string match, whitespace-collapsed and case-insensitive.
- `list` — the learner is asked for one bullet at a time. Each bullet is matched substring-wise against the expected list; you pass if you get ≥60% of the expected bullets.
- `multiple_choice` — learner answers with the index or the option text. `answer` may be the index (int) or the option string.
- `open` — `answer` is an array of acceptable substrings. If any matches, you pass. Otherwise the CLI shows the canonical answer hints and asks you to self-grade.

---

## CLI

```bash
./scripts/journey quiz 6            # Quiz on Week 6
./scripts/journey quiz 6 --n 3      # Only 3 random questions
./scripts/journey quiz 6 --review   # 80% Week 6 + 20% due-skill review (FSRS)
./scripts/journey quiz all          # Cross-week mix (default 10 questions)
./scripts/journey review            # Only skills FSRS says are due, across all weeks
./scripts/journey progress          # Print the progress table
./scripts/journey reset 6           # Forget Week 6 progress
./scripts/journey                   # Resume from current week
```

The `review` subcommand and `--review` flag use an adaptive scheduler (FSRS) that
surfaces skills "just before you would have forgotten them." See
[`docs/SPACED_REPETITION.md`](SPACED_REPETITION.md) for how it picks intervals,
the new `srs_state` block in `progress.json`, and how to use it as a daily warm-up.

Results persist to `~/.journey/progress.json`. Pass `JOURNEY_NON_INTERACTIVE=1` to auto-fill correct answers (useful for CI / smoke tests; this is what the workflow uses to verify every `mastery.yml` parses cleanly).

### `~/.journey/progress.json` schema

```json
{
  "current_week": 6,
  "weeks": {
    "6": {
      "week": 6,
      "passed": ["kadane_basic", "dutch_flag_idea", "prefix_sum_use"],
      "missed": ["kadane_all_negative"],
      "total": 4,
      "rate": 75.0,
      "timestamp": "2026-05-15"
    }
  }
}
```

- `current_week` — highest week the learner has run a quiz against. Used as the "Suggested next" pointer.
- `weeks[N]` — most recent quiz result for week N. Older results are overwritten; if you need history, copy `progress.json` aside before re-running.
- `rate` — pass percentage (0–100). The CLI uses ≥80% as the threshold for "you've passed this week" and suggests revisits of Week N-3 and Week N-7 (see `REVIEW_SCHEDULE.md`).

---

## Spaced repetition

When you score ≥80% on a week, the CLI prints a one-line suggestion like:

```
Great work — for retention, revisit Week 3 and Week — (see docs/REVIEW_SCHEDULE.md).
```

`REVIEW_SCHEDULE.md` already documents the philosophy and a hand-curated revisit table; mastery checkpoints are the mechanical implementation of that schedule.

---

## How to add a new skill

1. Open the relevant `Week N/mastery.yml`.
2. Add an entry with a unique `id`, a short `prompt`, the correct `answer` (matching the `type`'s shape), and a one-line `explanation`.
3. (Optional) Run `./scripts/journey progress` — it parses every `mastery.yml`, so YAML errors will surface immediately.
4. (Optional) Run `JOURNEY_NON_INTERACTIVE=1 ./scripts/journey quiz N` to confirm the new skill doesn't crash the engine.
