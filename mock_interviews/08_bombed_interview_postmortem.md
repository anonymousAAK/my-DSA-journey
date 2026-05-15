# Mock Interview: The Bombed Interview (Postmortem)

**Setup**: Senior engineer at a fictional ride-share company, Wendigo. Candidate has 2 years of experience and rushed prep the night before.

**Difficulty**: Medium (problem) / Catastrophic (performance)
**Topic**: Weeks 6-10 (arrays, two pointers) — but really, every meta-skill from every week.

**Important**: This transcript shows the candidate consistently doing the *wrong* thing. The annotations call out each mistake. Use this as a checklist of habits to *not* develop.

---

## Transcript

**Interviewer**: Given an array, find the contiguous subarray with the largest sum. Return the sum.

**Candidate**: Kadane's algorithm. I've done this one.

> 🔍 **Mistake #1: Skipped clarification.** Pattern-matching on a problem name is one of the worst interview habits. The interviewer hasn't told you whether the array can be empty, whether all-negative arrays should return 0 or the max single element, whether the input is small enough for naive solutions, or whether they want the subarray itself in addition to the sum. The candidate just dove in. Even if Kadane's IS the answer, asking clarifies (a) you're not pattern-matching blindly and (b) you understand the variants.

**Candidate**: ```
def max_subarray(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    return best
```

> 🔍 **Mistake #2: Coded before stating an approach.** The interviewer doesn't know whether the candidate is about to write Kadane's, brute force, or divide-and-conquer. By coding silently, the candidate has eliminated their chance to get a course correction in 15 seconds and is instead going to discover any misunderstanding at the dry-run stage in 5 minutes.

**Interviewer**: Walk me through it.

**Candidate**: It's standard Kadane's. `cur` is the best subarray ending here. We extend or restart. `best` tracks the global max.

> 🔍 **Mistake #3: "It's standard."** Never say this. Even if it is standard, *the interviewer wants to hear you derive it*. "Standard" tells them "I memorized this", which is exactly the opposite signal you want. The right framing is: "At each index, the best subarray ending here either extends the previous one or starts fresh. Whichever is larger wins. Keep a running global max."

**Interviewer**: What if the array is empty?

**Candidate**: ...I guess it crashes on `nums[0]`. Should I handle it?

> 🔍 **Mistake #4: Asked instead of decided.** "Should I handle it?" hands the steering wheel to the interviewer. The right move is to *propose*: "I'd raise a ValueError on empty input, or return 0 if the spec treats empty as a no-op subarray with sum 0 — which would you prefer?" That shows judgment and offers a choice rather than a request.

**Interviewer**: Up to you.

**Candidate**: I'll return 0.

**Interviewer**: What if all elements are negative?

**Candidate**: It should return... uh, the max element, I think. Let me check. `nums = [-3, -1, -2]`. cur starts -3, best -3. x=-1, cur = max(-1, -4) = -1, best = -1. x=-2, cur = max(-2, -3) = -2, best stays -1. Returns -1. Okay that works.

> 🔍 **Mistake #5: Dry-run after the interviewer asked, not before.** The candidate should have dry-run *unprompted*, especially on the trickiest case (all-negative) which is exactly where Kadane's-with-initial-zero variants are buggy. Now the dry-run looks defensive rather than diligent.

**Interviewer**: What's the complexity?

**Candidate**: O(N) time. O(1) space.

**Interviewer**: Can you also return the subarray itself, not just the sum?

**Candidate**: Sure, just track the indices. Um. Let me think. `start` updates when we... when `x > cur + x`, so when we restart. `end` is the current index when we update `best`.

```
def max_subarray(nums):
    cur = best = nums[0]
    start = end = best_start = best_end = 0
    for i in range(1, len(nums)):
        x = nums[i]
        if x > cur + x:
            cur = x
            start = i
        else:
            cur = cur + x
        if cur > best:
            best = cur
            best_start = start
            best_end = i
    return best, nums[best_start:best_end+1]
```

> 🔍 **Mistake #6: Refactored under pressure without dry-running.** The candidate added two pairs of indices, mutated the loop structure, and never re-ran the original example mentally. This is where bugs nest — particularly with the `>` vs `>=` on `if x > cur + x` (what about equal? does start move or not?). Confidently moving forward without verifying is the most common bombing pattern.

**Interviewer**: Run it on `[5, -2, 3, -1, 2]`.

**Candidate**: cur=5, best=5, all indices 0. i=1, x=-2. -2 > 5-2=3? No. cur=3. cur > best=5? No. i=2, x=3. 3 > 3+3=6? No. cur=6. cur > best? Yes, best=6, best_end=2. i=3, x=-1. -1 > 6-1=5? No. cur=5. i=4, x=2. 2 > 5+2=7? No. cur=7. best=7, best_end=4. Returns (7, [5,-2,3,-1,2]).

**Interviewer**: Good. What about `[-1, 2, 3, -10, 4, 5]`?

**Candidate**: cur=-1, best=-1, indices 0. i=1, x=2. 2 > -1+2=1? Yes. cur=2, start=1. best=2, best_start=1, best_end=1. i=2, x=3. 3 > 2+3=5? No. cur=5. best=5, best_end=2. i=3, x=-10. -10 > -5? No. cur=-5. i=4, x=4. 4 > -5+4=-1? Yes. cur=4, start=4. best 5 > 4. i=5, x=5. 5 > 4+5=9? No. cur=9. best=9, best_start=4, best_end=5.

Wait, did best_start update? Let me re-check. At i=5, cur=9 > best=5, so we update best, best_start=start=4, best_end=5. Yes. Returns (9, [4,5]).

**Interviewer**: Correct. Now: can you do it for a 2D matrix — find the rectangle with the max sum?

**Candidate**: Oh. Um. I haven't seen that one. Brute force is all rectangles, O(M²N²) for picking corners times O(MN) to sum, so O(M³N³)... no wait, with prefix sums it's O(M²N²) total. Is that good enough?

> 🔍 **Mistake #7: Conflating "I haven't seen this" with "I can't reason about it".** The candidate has the building blocks — they know prefix sums and 1D Kadane's — but freezes because they don't recognize the problem. A confident candidate would say: "I haven't seen the exact problem. Let me think out loud. The 1D version uses Kadane's. For 2D, I want to reduce to 1D. Idea: fix the top and bottom rows; collapse the rows into a single 1D array of column sums; run Kadane's on it. That's O(M²N) for M rows and N columns. Want me to walk through the reduction?"

**Interviewer**: It's a step up. Can you reduce 2D to 1D?

**Candidate**: ...Maybe with prefix sums on rows? So I precompute row prefix sums and then... I'm not sure. Can you give me a hint?

> 🔍 **Mistake #8: Asked for a hint without first proposing.** The right structure is: "Here's my best guess: <something>. I'm not sure about the details — does this direction seem right?" That gives the interviewer a target to correct. "Give me a hint" gives them nothing to grade.

**Interviewer**: Try fixing two row boundaries.

**Candidate**: Oh. So for each pair (top, bottom), I get a 1D array where element j is the column sum from row top to row bottom in column j. Then 1D Kadane's gives the best rectangle with those rows. Loop over pairs: O(M²) pairs × O(N) Kadane's = O(M²N). With column prefix sums, computing each pair's array is O(N), so total O(M²N).

**Interviewer**: Right. Code it.

**Candidate**: We're running short on time. Can I sketch instead?

> 🔍 **Mistake #9: Surrendered on time.** Running short on time is the candidate's fault — they spent 10 minutes on Kadane's because of all the back-and-forth. A confident candidate either (a) writes the code anyway, fast, because they understand it, or (b) writes pseudocode with a sentence explaining what they'd refine. "Can I sketch instead" without offering pseudocode reads as "I don't actually know how to write it".

**Interviewer**: Sure, sketch it.

**Candidate**: For each top row, initialize an array of N zeros. For each bottom from top to M-1, add row[bottom] elementwise. Run Kadane's on the array. Track global best.

**Interviewer**: Complexity?

**Candidate**: O(M²N) time, O(N) space.

**Interviewer**: Okay. Let's stop here. Do you have any questions for me?

**Candidate**: Um. What's the team like?

> 🔍 **Mistake #10: A reflexive, low-effort closing question.** "What's the team like" tells the interviewer the candidate has not prepared *for them specifically*. Strong closers are problem-shaped: "What's a hard engineering decision the team made in the last six months that you'd reconsider?" or "What part of your system would you most want to rewrite, and why hasn't it been rewritten?"

---

## What happened, in aggregate

The candidate *technically solved* both problems. They wrote correct 1D Kadane's, derived the 2D reduction with one nudge, and gave a correct complexity. By the answers alone, they'd pass an automated grader.

But the interviewer's notes look like this:

- *Did not clarify before coding.*
- *Pattern-matched the problem name; gave canned answer.*
- *Did not dry-run unprompted.*
- *Refactored under pressure without re-verifying.*
- *Asked for hints without proposing.*
- *Surrendered on time; sketched when code was expected.*
- *Closing question was generic.*

When the hiring committee meets, the bar is "would I want this person in a 1-on-1 design meeting at 4pm on a Wednesday?" The transcript says: this person knows the algorithms but won't drive the conversation, will need babysitting on novel problems, and won't show curiosity for our specific work. **No hire.**

---

## Annotation legend

Each 🔍 callout labels a specific *mistake* and what the candidate should have done instead.

---

## What was tested
- Clarifying questions: ❌
- Brute force first: ❌ (skipped to memorized solution)
- Complexity-driven optimization: ⚠️ (correct numbers, no reasoning)
- Edge cases without prompting: ❌ (had to be prompted twice)
- Communication while coding: ❌ (silent)
- Handling interviewer hints: ❌ (asked for hints, then accepted them without proposing)

## Reflection prompts for the learner
- For each of the 10 mistakes, write down a one-line *rewrite* of what the candidate should have said. Tape it to your monitor before your next mock.
- Re-read transcript 01 (Two Sum). Where does the strong candidate do the *opposite* of each mistake here? Make a side-by-side table.
- "Standard" is a tell. Make a list of other words that signal memorization to interviewers (start: "obviously", "the trick is", "as everyone knows", "it's just Kadane's"). Banish them from your interview vocabulary.
- The candidate technically solved both problems and still got "no hire". This is the central lesson: in mid-level and above interviews, the *dialogue* is graded more heavily than the *code*. Internalize that asymmetry.
