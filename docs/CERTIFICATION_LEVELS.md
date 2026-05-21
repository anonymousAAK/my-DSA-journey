# DSA Journey — Certification levels

Three tiers.  Each tier is a strict superset of the one below it:
every requirement of Foundation is also a requirement of
Practitioner, and so on.  The verifier
(`scripts/verify_certification.py`) always issues the **highest** tier
you actually qualify for, regardless of which you claim.

The pass bar throughout is `>=80%` on a week's **mastery quiz**, as
recorded in `~/.journey/progress.json` under `weeks[<n>].rate`.  See
`scripts/journey quiz <week>` for how those scores are generated.

---

## Foundation

> You've built the muscle for the basics.

| Requirement              | Bar                                          |
|--------------------------|----------------------------------------------|
| Mastery quizzes          | `>=80%` on Weeks **1 through 10**            |
| Capstones                | **1** of the six capstones, submitted via PR |
| Showcase entry           | Not required                                 |

What "Foundation" means in practice: arrays, strings, hashmaps, the
two-pointer and sliding-window patterns, basic sorting, intro to
recursion and trees — the core that an interviewer would expect from
a junior engineer.

---

## Practitioner

> You can pick the right pattern and reason about its cost.

| Requirement              | Bar                                          |
|--------------------------|----------------------------------------------|
| Mastery quizzes          | `>=80%` on Weeks **1 through 20**            |
| Capstones                | **2** of the six capstones                   |
| Showcase entry           | Not required                                 |

What "Practitioner" adds over Foundation: trees and BSTs, heaps,
graphs (BFS / DFS / shortest paths), greedy, basic DP, and the
intuition to spot the right approach quickly.  Roughly: comfortable
in a real interview loop.

---

## Master

> You can carry a system from algorithm to design.

| Requirement              | Bar                                                                     |
|--------------------------|-------------------------------------------------------------------------|
| Mastery quizzes          | `>=80%` on Weeks **1 through 30** (all of them)                         |
| Capstones                | **All three phase 1-3 capstones**, OR any **4** capstones in total      |
| Showcase entry           | **Required** — a directory under `showcase/` with a write-up and demo   |

What "Master" adds: advanced DP, segment / Fenwick / DSU, advanced
graph (SCC, max-flow, MST), string algorithms (KMP, Aho-Corasick,
suffix structures), and a system-design / architecture flavor on top.
The bar is "could mentor someone else through the whole journey".

---

## How the verifier picks a level

`scripts/verify_certification.py` evaluates the levels in order
**Master -> Practitioner -> Foundation**.  The first level whose
requirements are fully satisfied is what gets issued.  If none are
satisfied, the verifier exits non-zero and lists exactly what's
missing per level — so you know what to work on next.

A worked example:

```text
$ python3 scripts/verify_certification.py \
    --progress progress.json --user octocat \
    --capstone https://github.com/octocat/dsa/pull/12 \
    --capstone https://github.com/octocat/dsa/pull/15

Verification FAILED — no certification level reached.
  - Master: missing weeks [22, 23, 24, 25, 26, 27, 28, 29, 30] and 2 capstone(s)
  - Practitioner: missing weeks [21]
  - Foundation: need 1 capstones, got 0 ... wait that doesn't apply, you have 2.
```

(Concretely: in that scenario the learner is one week — Week 21 —
away from Practitioner.  Pass it and rerun.)

---

## Capstone shorthand

| #   | Title                                                |
|-----|------------------------------------------------------|
| P1  | `phase_1_cli_calculator`                             |
| P2  | `phase_2_text_search_tool`                           |
| P3  | `phase_3_visualizer_for_trees_and_heaps`             |
| P4  | `phase_4_maze_solver`                                |
| P5  | `phase_5_leaderboard_service`                        |
| P6  | `phase_6_tinyurl_with_consistent_hashing`            |

"All phase 1-3 capstones" in the Master row means P1 **and** P2
**and** P3.  Any four out of `{P1..P6}` is the alternate path.
