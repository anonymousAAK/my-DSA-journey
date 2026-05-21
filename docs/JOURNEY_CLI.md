# The `journey` CLI — full reference

`./scripts/journey` is the single entry point for the daily learning loop:
onboarding, picking a next session, scaffolding code, verifying it, journaling,
spaced-repetition review, and progress tracking.

```bash
./scripts/journey --help
```

State lives in `~/.journey/`:

| File | Purpose |
|------|---------|
| `config.json` | Your preferences: language, time-per-session, goal, soft-gate flag. |
| `progress.json` | Per-week quiz results, FSRS state, rolling history, miss counts. |
| `dashboard.html` | Self-contained HTML written by `progress --html` / `dashboard`. |

> Set `JOURNEY_NON_INTERACTIVE=1` to make every command auto-pick defaults — the
> CI workflow and smoke tests rely on this.

---

## `start` — onboarding

```bash
./scripts/journey start
```

Walks four short prompts (≈2 minutes total):

1. Primary language? `python` / `java` / `cpp` / `rust` (default `python`)
2. Time per session? `15m` / `30m` / `1h` (default `30m`)
3. Goal? `interview` / `curriculum` / `exploration` (default `curriculum`)
4. Skip the diagnostic? `y/N` — answering "no" surfaces a one-line pointer to
   `docs/diagnostic.md` and prints the current progress table.

Persists answers to `~/.journey/config.json` with `soft_gate_enabled: true`.
With `JOURNEY_NON_INTERACTIVE=1` it accepts every default silently.

---

## `next` — pick ONE concrete next action

```bash
./scripts/journey next                  # 30 min plan
./scripts/journey next --time 15m       # smaller plan (one task)
./scripts/journey next --time 1h        # full session (4 tasks)
./scripts/journey next --time weekend   # capstone-sized
./scripts/journey next --skip           # advance current_week without doing it
./scripts/journey next --skip --force   # override the soft mastery gate
```

Decision logic (priority order):

1. No progress AND no config → recommend `./scripts/journey start`.
2. Current week's mastery < 80% → suggest a mastery-quiz-focused session.
3. Else if there are FSRS-due skills AND time ≥ 15m → suggest `review`.
4. Else suggest the *next* week's first session (concept + drill + implement + verify).

Output is a numbered plan with explicit `Open:` / `Run:` commands so there's
zero ambiguity about what to do.

### Time scaling

| `--time` | Plan size |
|----------|-----------|
| `15m`    | ONE small task (a drill or a concept skim) |
| `30m`    | 3 tasks (concept + drill + quiz verification) |
| `1h`     | 4-5 tasks (concept + drill + implement + verify + quiz) |
| `weekend` | Capstone-scale: multi-step sprint, optionally a capstone milestone |

### Soft mastery gate

If `soft_gate_enabled` is true (the default) and your current week's mastery
quiz is below 80%, `next` will refuse to jump ahead — pass `--force` to
override. This prevents the "always-rush-forward" failure mode.

---

## `quiz` — mastery checkpoints for a week

```bash
./scripts/journey quiz 6              # full Week 6 quiz
./scripts/journey quiz 6 --n 3        # 3 random questions
./scripts/journey quiz 6 --review     # 80% Week 6 + 20% FSRS-due
./scripts/journey quiz all            # 10 random questions across all weeks
```

After each question you can self-rate `again/hard/good/easy` (or press Enter to
auto-rate). Ratings feed the FSRS scheduler that drives `review` and `next`.
See [`MASTERY.md`](MASTERY.md) and [`SPACED_REPETITION.md`](SPACED_REPETITION.md)
for the algorithm.

---

## `review` — only what FSRS says is due

```bash
./scripts/journey review
./scripts/journey review --n 5    # cap to 5 skills
```

Walks every week's `mastery.yml`, picks skills whose `next_review_date` is today
or earlier, orders them most-overdue-first, and runs them as a single mixed
quiz. If nothing is due, the command prints a hint and exits cleanly.

---

## `new-attempt` — scaffold a workbook stub

```bash
./scripts/journey new-attempt kadane             # uses config.language
./scripts/journey new-attempt two_sum --lang java # one-off override
```

- Picks the current week from `progress.json`.
- Creates `workbook/week_NN/attempts/` if needed.
- Writes `workbook/week_NN/attempts/<topic>__YYYY-MM-DD.<ext>` with:
  - a header comment (topic, week, date),
  - the function signature pulled from `tests/cases/<topic>.json`,
  - a `# WRITE YOUR CODE HERE` block, and
  - (Python only) an `if __name__ == "__main__":` block with one sample input.
- If a file with that exact name already exists, the date suffix is bumped
  (`...-2.py`, `...-3.py`, etc.). Existing attempts are never overwritten.

Topic resolution supports aliases — typing `kadane` finds
`tests/cases/kadane_max_subarray.json`. See the full alias table in
`scripts/journey` (`TOPIC_FIXTURE_ALIASES`).

---

## `verify` — run YOUR code against the fixtures

```bash
./scripts/journey verify kadane workbook/week_06/attempts/kadane__2026-05-12.py
```

- Resolves the topic to a `tests/cases/<topic>.json` fixture (with alias support).
- Dynamically imports your file as a Python module.
- For each case, calls `module.<function>(*input)` and compares to `expected`.
- Prints `PASS <case>` / `FAIL <case>` with `input / expected / got` diff.
- Final line: `TOTAL: X/Y passed` and a pointer to `tests/refs/<topic>.py` for
  the canonical implementation diff.
- Exits non-zero if any case fails (handy in shell pipelines).

If the topic doesn't exist, the command lists every available topic so you
know what's testable.

---

## `reflect` — append a journal entry

```bash
./scripts/journey reflect              # uses current_week
./scripts/journey reflect --week 6     # specific week
```

- Creates `workbook/week_NN/journal.md` if missing.
- Appends a dated section with the **Reflection prompts** parsed from that
  week's `Week NN/README.md`. Each prompt is followed by a blank `(your
  thoughts here)` placeholder.
- Prints the path and the appended template so you know where to write.

The journal is yours — no editor is launched. Just write honest two-sentence
answers; over 30 weeks they become a high-leverage retrospective artefact.

---

## `daily` — today's deterministic 25-min drip

```bash
./scripts/journey daily
./scripts/journey daily --markdown      # for piping into emails / issues
```

A deterministic plan (driven by today's ordinal day) that mixes:

1. A pattern-recognition drill from the current week's `patterns.md`.
2. A challenge from a revisit week (N-3 or N-7 per `REVIEW_SCHEDULE.md`).
3. A mastery-quiz topic from `Week N/mastery.yml`.
4. A reflection prompt from a curated rotating list.

Use `next` for an adaptive plan; use `daily` if you want the same plan to
appear regardless of progress state.

---

## `progress` — text table

```bash
./scripts/journey progress
```

One row per week: skills tested, pass rate, last attempt timestamp. Ends with
a "Suggested next" pointer that respects the highest week you've ever quizzed.

```bash
./scripts/journey progress --html        # writes ~/.journey/dashboard.html
./scripts/journey progress --html --open # also opens in default browser
./scripts/journey dashboard              # shortcut for the line above
```

The HTML dashboard is self-contained (no external CSS/JS) — refresh it
whenever you want a visual heat-map, streak counter, top-missed-skills table,
time-to-mastery table, and a recommended next session.

---

## `reset` — forget a week's progress

```bash
./scripts/journey reset 6
```

Removes `progress.json["weeks"]["6"]`. FSRS state (`srs_state`) and rolling
history are preserved — you only zero out the per-week summary.

---

## Default (no subcommand)

```bash
./scripts/journey
```

Prints "Resuming at Week N" and runs `progress` so you can see the table at a
glance. Most users alias this to `j` and run it as the first thing every day.

---

## Configuration schema

`~/.journey/config.json`:

```json
{
  "language": "python",
  "time_per_session": "30m",
  "goal": "curriculum",
  "soft_gate_enabled": true
}
```

| Key | Values | Effect |
|-----|--------|--------|
| `language` | `python` / `java` / `cpp` / `rust` | Default for `new-attempt` stubs. |
| `time_per_session` | `15m` / `30m` / `1h` / `weekend` | Default for `next` plan size. |
| `goal` | `interview` / `curriculum` / `exploration` | Soft hint (currently informational). |
| `soft_gate_enabled` | bool | If true, `next` refuses to advance past current week with <80% mastery (override with `--force`). |

Backwards-compatible with `progress.json`: every command reads both files and
falls back to sensible defaults if either is missing.

---

## Common workflows

**First-time setup:**

```bash
./scripts/journey start
./scripts/journey next
```

**Every morning (5-10 min):**

```bash
./scripts/journey review              # FSRS-due skills, if any
./scripts/journey next --time 15m     # one small task
```

**Weekly deep dive (1 hour):**

```bash
./scripts/journey next --time 1h
# ... do the suggested concept + drill + implement + verify ...
./scripts/journey quiz N              # confirm mastery
./scripts/journey reflect             # write 4 short paragraphs
```

**Weekend capstone:**

```bash
./scripts/journey next --time weekend
```

**Track your progress visually:**

```bash
./scripts/journey dashboard           # opens ~/.journey/dashboard.html
```
