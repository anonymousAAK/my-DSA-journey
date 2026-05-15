# Mock Interview: Two Sum (Warm-Up)

**Setup**: Senior engineer interviewer at a fictional fintech called Ledgerly. Candidate has a CS background, 2 years experience writing CRUD services in Go.

**Difficulty**: Easy
**Topic**: Weeks 1-3 (arrays, hash maps, complexity reasoning).

---

## Transcript

**Interviewer**: Hey, good to meet you. Let's start with something gentle to warm up. Given a list of integers and a target, return the indices of the two numbers that add up to the target.

> 🔍 **What's happening here**: The interviewer is deliberately vague. They didn't say "integer array", "exactly one solution", "may have duplicates", or what to return if there's no answer. Easy problems are easy *if* you treat the interview as a conversation; they become traps if you race to code.

**Candidate**: Sure. Before I jump in — can the input contain duplicates? And is it guaranteed that exactly one pair exists?

**Interviewer**: There can be duplicates. Assume exactly one valid pair exists per input.

> 🔍 **What's happening here**: One clarifying question at a time. The candidate did not fire off "duplicates? negatives? sorted? in-place? what if no answer? what language?" all at once. Asking serially lets each answer shape the next question, and it sounds like a conversation rather than a checklist.

**Candidate**: Got it. And the return — indices or values?

**Interviewer**: Indices, zero-based.

**Candidate**: Can the same element be used twice? E.g. for target=6 and input=[3], obviously not, but for target=6 and input=[3,3] I should return [0,1]?

**Interviewer**: Right. Each element used at most once. [0,1] is correct there.

> 🔍 **What's happening here**: The "can I use the same element twice" question looks pedantic but catches a real off-by-one bug in many naive hash-map solutions where the candidate stores everything up front and then looks up `target - x`, accidentally matching `x` against itself.

**Candidate**: Cool. Let me think out loud. The brute force is two nested loops: for every `i`, scan `j > i` checking `nums[i] + nums[j] == target`. That's O(N²). If N is say 10^5, that's 10^10 operations — too slow for a one-second budget. So I want to do better.

> 🔍 **What's happening here**: The candidate verbalized brute force *and then justified moving past it with a concrete complexity-vs-constraint argument*. They didn't dismiss brute force ("obviously O(N²) is bad") — they made the case. Interviewers love this because it shows you'd make the same call alone at 2am.

**Interviewer**: Assume N up to 10^5. What's your better idea?

**Candidate**: Trade space for time with a hash map. As I iterate, for each `x = nums[i]`, I check if `target - x` is already in the map. If yes, I have my pair: the stored index and `i`. If not, I store `x -> i` and continue. One pass, O(N) time, O(N) space.

**Interviewer**: Walk me through `nums = [2, 7, 11, 15], target = 9`.

**Candidate**: i=0, x=2, need 7, map is empty, store {2:0}. i=1, x=7, need 2, found at index 0, return [0,1]. Done.

> 🔍 **What's happening here**: The candidate ran the algorithm on the example BEFORE writing code. This catches design bugs while they're cheap. Coding first, debugging on the example after, is one of the most common time-sinks in interviews.

**Candidate**: Let me code it.

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}
    for i, x in enumerate(nums):
        complement = target - x
        if complement in seen:
            return [seen[complement], i]
        seen[x] = i
    return []  # contract says unreachable, but explicit beats implicit
```

**Interviewer**: Why store after the check rather than before?

**Candidate**: So an element can't pair with itself. If I stored first, `nums=[3], target=6` would falsely return when `x=3` and `complement=3` is found at the same index. Storing after guarantees the lookup only sees prior indices.

> 🔍 **What's happening here**: The interviewer probed an invariant. The candidate didn't just say "that's how it's done" — they articulated *why*. Knowing the invariant is the difference between memorized solutions and understood ones.

**Interviewer**: Edge cases?

**Candidate**: Negative numbers — works fine, hashing handles them. Duplicates that aren't the answer — fine, we just overwrite, but since we return as soon as we find a match, overwriting is harmless. Empty array or single element — the loop just exits and we return `[]`. Very large or very small ints — Python is unbounded, but in Java/Go I'd worry about `target - x` overflow.

**Interviewer**: Good. Suppose now the array is sorted and you must use O(1) extra space.

> 🔍 **What's happening here**: The follow-up isn't a gotcha — it's the interviewer checking whether your solution is the only tool in your belt or one of several. Always expect a "now change one constraint" follow-up on warm-up problems.

**Candidate**: Two pointers. `l=0, r=N-1`. If `nums[l]+nums[r] < target`, move `l` right; if greater, move `r` left; if equal, return. O(N) time, O(1) space. Correctness comes from monotonicity: at each step, the value on one side can only be moved in the direction that gets us closer.

**Interviewer**: Perfect. Last question: how would this scale if the array doesn't fit in memory?

**Candidate**: That's a different problem — external two sum. I'd external-sort the array, then either two-pointer through the sorted file with two file handles seeking inward, or hash-partition by `x mod K` into K shards and search each shard's complement shard `(target - x) mod K` together. Pick based on whether disk seeks or hash collisions dominate.

> 🔍 **What's happening here**: The candidate didn't pretend to design a full distributed system in 30 seconds. They named two plausible approaches, gave one sentence on the tradeoff, and stopped. Knowing when to stop is a skill.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill* — not the algorithm, the *dialogue*.

---

## What was tested
- Clarifying questions: ✅ asked serially, each informed by the prior answer
- Brute force first: ✅ stated, complexity-checked against constraint, then improved
- Complexity-driven optimization: ✅ "10^10 ops in 1 sec is too slow"
- Edge cases without prompting: ✅ negatives, duplicates, empty, overflow
- Communication while coding: ✅ narrated the invariant
- Handling interviewer hints: ✅ adapted to "now sorted, O(1) space"

## Reflection prompts for the learner
- Which clarifying question would YOU have skipped? Why? (Hint: in this transcript none were truly skippable for the Two Sum class, but in a tighter slot you might collapse "duplicates?" and "same element twice?" into one.)
- At what point in the transcript could the candidate have gone faster? At what point should they have gone *slower*? (Try: faster on the code; slower on stating the invariant about storing-after-checking.)
- The candidate gave a one-sentence answer to the out-of-memory follow-up. Was that the right length? When does brevity become bluffing?
