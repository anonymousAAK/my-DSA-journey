# Daily Practice — 25 minutes a day

Most learners stall not because they can't do the work, but because they can't *start* the work. The daily-practice drip exists to solve the cold-start problem: every weekday morning, a 25-minute plan lands in your inbox. You can do it on a coffee break.

---

## How it works

### Local

```bash
./scripts/journey daily              # plain-text plan for today
./scripts/journey daily --markdown   # Markdown (pipe into email, paste into issue, ...)
```

The plan has four items:

1. **Pattern drill** — one prompt from the current week's `patterns.md`. Name the pattern in one word, justify in one sentence.
2. **Challenge** — one challenge from `Week (N-3)/challenges.md` (revisit) if N ≥ 4, else from the current week. Read the spec, sketch an approach. You don't have to finish it before tomorrow's drip.
3. **Mastery quiz topic** — one skill from the current week's `mastery.yml`. The command line includes the exact `./scripts/journey quiz N --n 1` to drill it.
4. **Reflection prompt** — one open-ended question to write 2-3 sentences on.

Total time: 25 minutes. If you have more time, do tomorrow's now; the rotation is deterministic, so reading ahead doesn't break anything.

### As a daily GitHub Issue

The workflow at [`.github/workflows/daily_practice.yml`](../.github/workflows/daily_practice.yml) runs every weekday at **08:00 UTC** and:

1. Runs `./scripts/journey daily --markdown` on the repo's `main` branch.
2. Opens a new issue titled `Daily Practice — YYYY-MM-DD` with the markdown as the body.
3. Tags it with the labels `daily-practice` and `auto-generated`.
4. Closes any open `daily-practice` issue older than 7 days.

The repo's `current_week` for the workflow comes from whatever the runner reconstructs on its fresh checkout — see "Caveat" below.

### Subscribing to notifications

Watch the `daily-practice` label and you'll be notified each morning:

1. Go to the repo on GitHub.
2. Click "Watch" → "Custom" → check **Issues**.
3. Or, more surgically, use the [GitHub notifications](https://github.com/notifications) page to subscribe to the `daily-practice` label.

If you'd rather not get a notification every weekday, just bookmark the [issues filtered by label](https://github.com/anonymousAAK/my-DSA-journey/issues?q=is%3Aissue+label%3Adaily-practice) and visit at your own cadence — the issues stay around for 7 days before auto-close, so you'll see the last week of plans at a glance.

---

## Selection rules

The picks are **deterministic on the date**, so two runs on the same day produce the same plan. Specifically:

- `day_idx = date.toordinal()`
- **Pattern drill**: `drills[(day_idx + current_week) % len(drills)]` from the current week's `patterns.md`.
- **Challenge**: from `Week (current_week - 3)/challenges.md` if `current_week >= 4`, else `Week (current_week - 7)` if `current_week >= 8`, else the current week. Picked with `challenges[day_idx % len(challenges)]`.
- **Mastery skill**: `skills[day_idx % len(skills)]` from the current week's `mastery.yml`.
- **Reflection**: cycled from a baked-in pool of 14 prompts inside `scripts/journey`.

Revisit logic mirrors [`docs/REVIEW_SCHEDULE.md`](REVIEW_SCHEDULE.md): the daily challenge defaults to a week you studied 3 weeks ago, which is the highest-leverage spaced-repetition window.

---

## Caveat: workflow's `current_week`

`current_week` lives in `~/.journey/progress.json`, which is created when you take a quiz. On the GitHub Actions runner there is no progress file — so the workflow falls back to `current_week = 1`. That's fine for the first week of the curriculum, but later it will under-deliver.

**Fix**: commit a stub `progress.json` to the repo (or set an env var the CLI checks), or run the workflow only locally via `act` / a self-hosted runner that has your real progress mounted. The simple-but-good-enough fix is to manually `workflow_dispatch` the workflow with an input override; left to a follow-up.

For the issue-opening flow you can also bypass the script entirely by setting `JOURNEY_CURRENT_WEEK` once you wire it into `scripts/journey` — left as a TODO.

---

## Customization

- **Skip weekends**: the workflow's cron is `0 8 * * 1-5`, Monday–Friday only.
- **Different time**: change the cron in `.github/workflows/daily_practice.yml`. Note all GitHub Actions cron times are UTC.
- **Different schedule**: swap to `*/4 * * * 1-5` for an every-4-hours drip, etc. Don't go faster than every couple of hours or you'll generate spam.
- **More reflection prompts**: append to `_REFLECTION_PROMPTS` near the bottom of `scripts/journey`.
