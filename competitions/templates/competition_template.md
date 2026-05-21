# Weekly Competition — <ISO Week, e.g. 2026-W22>

> Replace this placeholder block with one paragraph framing the problem:
> what's the real-world setting, what's the algorithmic core, and roughly
> which curriculum week's material it draws on.

## Problem statement

Implement a function with signature:

```
<language-agnostic signature, e.g.>
top_k(stream: Iterable[int], k: int) -> List[int]
```

Constraints:

- `1 <= k <= 10^4`
- The stream may be larger than memory; you must process it in a single pass
  using O(k) auxiliary space.
- Ties may be broken in any consistent order.

## Sample IO

### Example 1

```
Input:  stream = [4, 1, 7, 3, 8, 2, 9, 5], k = 3
Output: [9, 8, 7]
```

### Example 2

```
Input:  stream = [1, 1, 1, 1], k = 2
Output: [1, 1]
```

## Hidden test plan

Describe the categories of hidden tests so participants can self-check
without seeing the actual data:

- Stream length 1 (edge case).
- `k` equal to stream length.
- All elements equal (tie-breaking).
- Stream length 10^6 with `k = 100` (performance — must finish in
  `timeout_seconds`).
- Negative integers and zeros.

Place the actual test data in
`competitions/judges/<iso_week>.json`:

```json
{
  "tests": [
    {"input": "8 3\n4 1 7 3 8 2 9 5", "expected": "9 8 7"}
  ],
  "timeout_seconds": 5
}
```

## Scoring rubric

| Criterion | Weight |
| --- | --- |
| Correctness on hidden tests | 70% |
| Asymptotic complexity (state and justify) | 15% |
| Code clarity (naming, comments where non-obvious) | 10% |
| Wall-clock runtime on the 10^6 case (tie-breaker) | 5% |

## Submission format

Post as a comment on the pinned competition issue:

1. Language tag (`java`, `python`, `cpp`, `rust`, or `web`).
2. Code block with your solution.
3. One sentence stating your claimed time and space complexity.
4. Output for both sample inputs above.

## Notes for the author

- Keep the problem solvable in 60–120 minutes for a learner at the relevant
  week's level.
- Avoid problems that require external libraries; stdlib of each language
  only.
- If the problem is open-ended (system design, API shape), use peer-voted
  judging instead of hidden tests, and write that clearly in the spec.
