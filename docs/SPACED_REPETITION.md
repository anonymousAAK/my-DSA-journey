# Spaced repetition with FSRS

> The hand-curated revisit table in `REVIEW_SCHEDULE.md` is what you should do *if* you have a fully-formed plan and the discipline to follow it. This document is what to do when you don't — a scheduler that decides for you which skills to surface, when, based on how well you've remembered them so far.

This system uses **FSRS** (the Free Spaced Repetition Scheduler) as the brain behind `./scripts/journey review`. It plugs into the existing mastery-check infrastructure: every time you answer a question in `./scripts/journey quiz N`, the scheduler updates a per-skill memory model and recomputes when to surface that skill again. Skills you remembered get pushed weeks or months into the future; skills you flubbed come back tomorrow.

---

## Why spaced repetition matters

Hermann Ebbinghaus's 1885 self-experiments produced what's now called the **forgetting curve**: a sharp exponential drop in recall immediately after learning, leveling off into a long tail. After 24 hours without revisiting fresh material, you've typically lost 50-80% of it. After a week, almost all of it.

The clean implication is brutal: **studying without spaced review is studying-as-pouring-water-into-sand**. The 4 hours you spent on Week 6 last Tuesday are mostly gone by next Tuesday — unless you review them. Conversely, even tiny review touches (5 minutes a few days apart) flatten the forgetting curve dramatically, because each *successful retrieval* under cognitive load strengthens the memory trace much more than rereading does (the "testing effect" — Roediger and Karpicke, 2006).

The hard question isn't "should I review?" — it's "*when?*" Too soon: you waste time on material you still remember. Too late: you've forgotten it and you're effectively relearning, not reviewing. The right interval is "just before you would have forgotten" — long enough to be a genuine retrieval, short enough that the retrieval still succeeds. That sweet spot is what an SRS scheduler tries to predict.

---

## How FSRS chooses intervals

FSRS (Piotr Wozniak's SuperMemo line and the more modern derivatives from the open-spaced-repetition team) models each skill's memory with two latent variables:

- **Stability (S)** — measured in days. Roughly: "how long until your retrievability drops to 90%?" Stability grows when you successfully retrieve under load; it shrinks (often dramatically) when you fail.
- **Difficulty (D)** — on a 1–10 scale. Roughly: "how stubbornly does this card refuse to grow stable?" Cards that you keep flubbing accumulate difficulty, which damps stability growth on future successes.

A scheduler with stability `S` picks the next interval `t` so that **retrievability at time t** (`R(t) = (1 + t/(9S))^-w`) hits a target retention rate — typically 90%. Plug in S = 2.4 days, R = 0.9: next review in ~1 day. Plug in S = 60 days, R = 0.9: next review in ~7 weeks.

Each time you answer, you (explicitly or implicitly) provide a **rating**:

| Rating | Meaning | Effect on schedule |
|-------:|---------|--------------------|
| 1 / "again" | Forgot — could not retrieve | Big drop in stability; tomorrow or sooner |
| 2 / "hard" | Got it but barely | Small stability growth; short interval |
| 3 / "good" | Got it cleanly | Standard stability growth; default interval |
| 4 / "easy" | Got it without thought | Larger stability growth; longer interval |

The `journey` CLI auto-derives a rating from correctness — pass = good (3), fail = again (1). In interactive mode you can override with a self-rating after each question.

Reference: <https://github.com/open-spaced-repetition/fsrs4anki>. We use the published v4 default weights (17 parameters) so the scheduler is sensible out of the box; learning the weights to individual learner data is supported by upstream but not implemented here.

---

## Using the new commands

### `./scripts/journey review`

Quiz only the skills that are due *now*, across every week, in priority order (most overdue first). Stops once all due skills have been answered, or when you cap with `--n N`.

```bash
./scripts/journey review              # all due skills
./scripts/journey review --n 10       # cap at 10 to keep the session short
```

If nothing is due, the command tells you so and exits. Use this as your daily 5-minute warm-up: run it first thing, answer whatever it surfaces, then move on to current-week material.

### `./scripts/journey quiz N --review`

Run a normal week-N quiz but interleave **20% due-skill reviews** with **80% current-week skills**. This is the "I'm studying Week N but I want to keep last month's material from rotting" mode.

```bash
./scripts/journey quiz 12 --n 10 --review   # 8 Week-12 questions + 2 review picks
```

If no skills are currently due, it falls back to a plain Week-N quiz.

### `./scripts/journey quiz N` (unchanged)

Still works exactly as before. The only difference: each answer now updates the SRS state for that skill behind the scenes, so the *next* `review` or `quiz --review` run has data to schedule on. Existing progress.json keys (`weeks`, `history`, `current_week`, `skill_miss_counts`) are untouched — the SRS state lives in a new `srs_state` block, so the dashboard and existing tools keep working.

---

## Schema changes to `~/.journey/progress.json`

A new top-level key, **backwards-compatible** with everything else:

```json
{
  "current_week": 6,
  "weeks": { ... },
  "history": [ ... ],
  "skill_miss_counts": { ... },
  "srs_state": {
    "6:kadane_basic": {
      "difficulty": 4.93,
      "stability": 30.02,
      "last_review_date": "2026-05-15",
      "next_review_date": "2026-06-14",
      "reps": 3,
      "lapses": 0,
      "history": [
        {"date": "2026-05-01", "rating": 3},
        {"date": "2026-05-08", "rating": 3},
        {"date": "2026-05-15", "rating": 3}
      ]
    }
  }
}
```

The key is `"<week>:<skill_id>"` matching the existing `skill_miss_counts` convention. `history` is capped at the last 50 ratings per skill to avoid unbounded growth.

If you want a fresh start, delete the `srs_state` block and re-run a quiz; everything else (history, miss counts, dashboard) survives.

---

## Practical rhythm

A workable daily loop:

1. **Run `./scripts/journey review`** first. 5 minutes, maybe nothing is due, maybe 8 things are.
2. **Run `./scripts/journey quiz N`** for your current week. Or `quiz N --review` if you want the interleaving without thinking about it.
3. **Trust the schedule.** If FSRS doesn't surface a skill for 60 days, it's because the model thinks you remember it. If it surfaces something three days in a row, take the hint — that skill needs more than the schedule alone.

The hidden value of FSRS over a fixed table (like `REVIEW_SCHEDULE.md`'s N-3 / N-7 cadence) is that it *adapts to you*. The fixed table assumes every skill has the same forgetting curve; FSRS measures yours and personalizes. The fixed table is great when you're starting; the scheduler takes over when you've built up a few weeks of data.

---

## Caveats and known limitations

- **The first review interval is short** (~1 day) regardless of how confident you are, because S starts at the rating-specific initial value (2.4 for "good"). That's intentional — FSRS doesn't know how stable a *new* memory is, so it tests early to find out.
- **Auto-rating is binary** (good or again). The richer 4-way rating only kicks in if you self-rate interactively. For most learners the auto-derived rating is fine; if you find FSRS too forgiving or too harsh, switch to interactive ratings on a few sessions to retrain it.
- **Defaults are population averages.** FSRS upstream supports learning per-user weights from your own review history; we don't. If you want personalization, dump your `srs_state` and feed it to `fsrs4anki_optimizer` — but in practice the defaults are within ~10% of optimal for most learners.
- **No "leech" detection yet.** Anki's UX flags cards you've failed too many times so you can rewrite or suspend them. The CLI's `skill_miss_counts` block already records this; the next iteration could surface "Week 6, kadane_basic — failed 7 times; consider editing the prompt or studying it differently."

---

## Credits

- **FSRS** algorithm: <https://github.com/open-spaced-repetition/fsrs4anki> (not added as a dependency; the algorithm is reimplemented here with the published default weights).
- **Ebbinghaus forgetting curve**: Ebbinghaus, "Über das Gedächtnis" (1885).
- **Testing effect**: Roediger and Karpicke, "Test-enhanced learning" (2006).
- **The "spacing > cramming" effect** has been replicated so many times across cognitive psychology that you can pick essentially any review article from the last 40 years; Cepeda et al. (2008) is a good meta-analysis.
