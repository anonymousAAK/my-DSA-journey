# Mock Interview: Meeting Rooms II (Intervals)

**Setup**: Engineering manager at a fictional scheduling startup, Calenday. Candidate has 2 years experience, mostly backend.

**Difficulty**: Medium
**Topic**: Weeks 6-8 (sorting, greedy, heaps).

---

## Transcript

**Interviewer**: Given a list of meeting time intervals, return the minimum number of conference rooms required.

> 🔍 **What's happening here**: This is a famously two-approachable problem (heap vs. sweep line / chronological-ordering of start and end events). The interviewer is watching whether you commit to the first idea or survey the option space.

**Candidate**: Quick clarifications. Are intervals `[start, end)` half-open or `[start, end]` closed? Specifically, if meeting A ends at 10:00 and meeting B starts at 10:00, do they conflict?

**Interviewer**: Half-open. End-of-A at 10 means the room is free for B at 10.

> 🔍 **What's happening here**: This single clarifier rewrites the comparison logic later. Asking it up front saves you from a 5-minute debate about a `<` vs `<=` in the middle of coding.

**Candidate**: Are timestamps integers? Sorted in any way?

**Interviewer**: Integer minutes since midnight. Unsorted.

**Candidate**: Any input size hints? Could there be 10^6 intervals?

**Interviewer**: Up to about 10^5.

**Candidate**: Okay. The brute force is: for every minute on the timeline, count how many intervals cover it; the answer is the max. That's O(T × N) where T is the timeline length — bad if intervals span days.

> 🔍 **What's happening here**: Even though brute force here is silly, naming it serves a purpose: it sets up the *insight* — we don't need every minute, only the minutes where the count changes, i.e. starts and ends.

**Candidate**: That motivates a sweep line. Make 2N events: each interval contributes a +1 at start and a -1 at end. Sort by time, with ties broken so that ends come before starts (because of the half-open convention). Then walk and track the running max.

**Interviewer**: Could you also do it with a heap?

> 🔍 **What's happening here**: The interviewer is *not* saying the sweep line is wrong — they want to know if you understand both, and if so, which you'd reach for and why. This is the trap many candidates fall into: they hear "could you also do it with X" and immediately abandon their plan, panicking. Hold your ground while engaging.

**Candidate**: Yes. Sort intervals by start time. Use a min-heap of end times of currently-active meetings. For each interval in order: while the heap's top end is `<=` the current start, pop (that room is free now); push the current end. The answer is the max heap size seen.

**Interviewer**: Which would you implement and why?

**Candidate**: Both are O(N log N) and O(N) space. I'd lean toward the sweep line: simpler primitives, one sort, one linear pass, no priority-queue edge cases, easier to test. The heap version is more natural if the interviewer follows up with "now assign a specific room number to each meeting" — then you want a free-room queue.

> 🔍 **What's happening here**: The candidate gave a *decision* with a *reason*, while also previewing how the choice connects to plausible follow-ups. This is signaling judgment, not just knowledge.

**Interviewer**: Go with sweep line.

**Candidate**:

```python
def min_meeting_rooms(intervals: list[tuple[int, int]]) -> int:
    events = []
    for s, e in intervals:
        events.append((s, +1))
        events.append((e, -1))
    # half-open: ends come before starts at the same timestamp
    events.sort(key=lambda x: (x[0], x[1]))  # -1 sorts before +1, correct
    rooms = peak = 0
    for _, delta in events:
        rooms += delta
        peak = max(peak, rooms)
    return peak
```

**Candidate**: Quick dry run on `[(0,30),(5,10),(15,20)]`. Events sorted: (0,+1),(5,+1),(10,-1),(15,+1),(20,-1),(30,-1). Running: 1,2,1,2,1,0. Peak 2. Correct.

> 🔍 **What's happening here**: The candidate ran the sample after writing the code, and they explicitly invoked the half-open rule by pointing out that -1 sorts before +1 — proving the clarification at the top wasn't wasted.

**Interviewer**: What if I told you intervals stream in one at a time and you need to maintain the answer online?

**Candidate**: That changes the data structure. I'd want an order-statistic tree or a balanced BST of events, or in practice a sorted container — insert each (time, delta), and maintain a Fenwick tree on a coordinate-compressed time axis so I can query the running prefix sum maximum. Without coordinate compression, a segment tree over the time range works if the range is bounded.

> 🔍 **What's happening here**: The candidate translated the offline batch algorithm into an online one by *naming the missing structure* (BIT/segtree for prefix maximum) without trying to code it. In a 45-minute interview you sketch online follow-ups; you don't fully implement them unless asked.

**Interviewer**: Last one. If two events have the same timestamp but one is a start and one is an end of a *different* meeting, who wins?

**Candidate**: End first, given our half-open convention. Because if room frees at 10:00 and another meeting starts at 10:00, they don't conflict — the freeing must be processed before the demand. If it were the closed convention they'd conflict and start should win.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill*.

---

## What was tested
- Clarifying questions: ✅ the half-open question was load-bearing
- Brute force first: ✅ used as a *bridge* to the insight, not a token gesture
- Complexity-driven optimization: ✅ both approaches sized up
- Edge cases without prompting: ✅ tie-break at equal timestamps
- Communication while coding: ⚠️ could have narrated the sort-key tuple more
- Handling interviewer hints: ✅ stayed on sweep line when nudged toward heap, then committed when told to

## Reflection prompts for the learner
- The interviewer asked "could you also do it with a heap?" — was that a hint that sweep line was wrong, or just probing? How can you tell? (Heuristic: hints that say "you might want to reconsider X" are corrective; hints that say "could you also" are exploratory.)
- Replay the moment when the candidate justified sweep line over heap. Write down a problem where you'd reverse that choice.
- The closed-interval variant (where `[1,5]` and `[5,9]` *do* conflict) is one tie-break flip away. Modify the code to handle it. Did you change `(x[0], x[1])` or `(x[0], -x[1])`? Why?
