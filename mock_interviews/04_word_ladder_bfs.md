# Mock Interview: Word Ladder (BFS with a twist)

**Setup**: Senior engineer at a fictional crossword-puzzle startup, Anagrammr. Candidate has 2 years of experience and is comfortable with graph basics.

**Difficulty**: Medium
**Topic**: Weeks 11-12 (graphs, BFS, implicit graphs).

---

## Transcript

**Interviewer**: Given a `beginWord`, an `endWord`, and a dictionary `wordList`, return the length of the shortest transformation sequence from `beginWord` to `endWord`, where each adjacent pair differs by exactly one letter and every intermediate word must be in `wordList`. Return 0 if no such sequence exists.

**Candidate**: A few questions. Are all words the same length?

**Interviewer**: Yes, all lowercase English, same length.

**Candidate**: Is `beginWord` guaranteed to be in the list? And does `endWord` have to be?

**Interviewer**: `beginWord` may or may not be in the list. `endWord` must be in the list, otherwise return 0.

> 🔍 **What's happening here**: This second clarifier matters: it lets the candidate return 0 immediately as a guard, and it lets them include `beginWord` in the visited set without worrying about removing it from the dictionary.

**Candidate**: What's the length count — number of words (so begin → end counts as 2 if they differ by one letter) or number of transformations (so that case is 1)?

**Interviewer**: Number of words in the sequence, inclusive.

**Candidate**: Constraints?

**Interviewer**: Word length up to 10. Word list up to about 5000 words.

**Candidate**: Okay. The natural model is an implicit graph: nodes are words, edges connect words that differ by exactly one letter. Shortest path on an unweighted graph means BFS.

> 🔍 **What's happening here**: "Implicit graph" is the keyword. The candidate signaled that they recognize the graph isn't given to them — they have to build it (or build neighbors on the fly).

**Interviewer**: How do you find neighbors?

**Candidate**: Two strategies. First, the naive: for each pair of words in the list check Hamming distance — O(N² · L) preprocessing. That's 5000² · 10 = 2.5×10^8, borderline.

The second, much better: for each word, for each position, replace the letter at that position with `*` to form a *pattern*. Build a map `pattern -> list of words matching it`. Neighbors of a word are all the words sharing any of its L patterns (excluding itself). That's O(N · L · 26) at worst per BFS expansion, or O(N · L) preprocessing plus O(N · L) BFS work.

> 🔍 **What's happening here**: The "wildcard pattern" trick is the canonical insight for this problem. The candidate explicitly compared to the brute force so the interviewer sees the asymptotic reasoning — they're not just reciting a memorized hack.

**Interviewer**: Go with the pattern map.

**Candidate**:

```python
from collections import defaultdict, deque

def ladder_length(begin: str, end: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end not in words:
        return 0
    L = len(begin)

    # build pattern -> [words]
    pattern_map: dict[str, list[str]] = defaultdict(list)
    for w in words | {begin}:
        for i in range(L):
            pattern_map[w[:i] + "*" + w[i+1:]].append(w)

    visited = {begin}
    q = deque([(begin, 1)])
    while q:
        word, dist = q.popleft()
        if word == end:
            return dist
        for i in range(L):
            pat = word[:i] + "*" + word[i+1:]
            for nbr in pattern_map[pat]:
                if nbr in visited:
                    continue
                visited.add(nbr)
                q.append((nbr, dist + 1))
    return 0
```

**Candidate**: Dry run on `begin="hit", end="cog", list=["hot","dot","dog","lot","log","cog"]`. Patterns include `*ot: [hot,dot,lot]`, `h*t: [hit,hot]`, `do*: [dot,dog]`, `*og: [dog,log,cog]`, etc. BFS from hit dist 1, neighbors `hot` dist 2, then `dot lot` dist 3, then `dog log` dist 4, then `cog` dist 5. Return 5. Matches the expected answer.

> 🔍 **What's happening here**: Dry-running on the *standard* example reassures the interviewer that the candidate's mental model lines up with the problem. Don't invent a new example here — use the one most likely to be in the interviewer's head.

**Interviewer**: Now the twist. Can you make this faster?

**Candidate**: Bidirectional BFS. Search simultaneously from `begin` and `end`; expand the smaller frontier each step; when an expansion produces a word in the other frontier, we've found the shortest path. The intuition is that BFS explores a ball of radius `r` around the start; two balls of radius `r/2` together have far fewer nodes than one ball of radius `r` when the branching factor `b > 1`. Roughly O(b^(d/2)) vs O(b^d).

> 🔍 **What's happening here**: The candidate justified the speedup *quantitatively*. "It's faster because we search from both sides" is the kind of half-answer that interviewers note negatively. "b^(d/2) vs b^d" is what they want to hear.

**Interviewer**: Code it.

**Candidate**:

```python
def ladder_length_bidi(begin: str, end: str, word_list: list[str]) -> int:
    words = set(word_list)
    if end not in words:
        return 0
    L = len(begin)

    front, back = {begin}, {end}
    visited = {begin, end}
    dist = 1
    while front and back:
        # always expand the smaller frontier
        if len(front) > len(back):
            front, back = back, front
        nxt = set()
        for word in front:
            for i in range(L):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c == word[i]:
                        continue
                    cand = word[:i] + c + word[i+1:]
                    if cand in back:
                        return dist + 1
                    if cand in words and cand not in visited:
                        visited.add(cand)
                        nxt.add(cand)
        front = nxt
        dist += 1
    return 0
```

**Candidate**: I switched to the 25-letter-substitution enumeration instead of the pattern map here because bidirectional BFS benefits more from cheap neighbor generation than from the pattern map's preprocessing, and the pattern map's bookkeeping gets fiddly with two frontiers. For small alphabets this is a wash; for L=10 it's still ~250 lookups per word, well within budget.

> 🔍 **What's happening here**: The candidate *justified abandoning the previous data structure* rather than awkwardly reusing it. Interviewers respect a clean break with a reason more than a half-converted Frankenstein.

**Interviewer**: Edge cases?

**Candidate**: `begin == end` — depends on spec; usually return 0 or 1. `endWord` not in list — handled. List contains `beginWord` — fine, visited covers it. Disconnected components — BFS just terminates and returns 0.

**Interviewer**: Last one. If the dictionary is 10 million words and you can preprocess it once, what changes?

**Candidate**: Two changes. First, I'd persist the pattern map to disk (e.g. a sorted file or a key-value store) and load it on startup. Second, BFS visited-set memory becomes the bottleneck — 10M booleans is fine but storing the BFS layer's words isn't. I'd switch to integer IDs and a bitset for `visited`, and store layers as ID arrays. Bidirectional BFS still wins.

---

## Annotation legend

Each 🔍 callout teaches a specific *interview meta-skill*.

---

## What was tested
- Clarifying questions: ✅ "same length", "endWord in list", "length count semantics"
- Brute force first: ✅ named, sized, dismissed
- Complexity-driven optimization: ✅ pattern map, then bidirectional BFS with b^(d/2) argument
- Edge cases without prompting: ✅ begin==end, disconnected
- Communication while coding: ✅ justified the data-structure swap
- Handling interviewer hints: ✅ "make it faster" → bidirectional, not panic

## Reflection prompts for the learner
- The candidate switched from the pattern map to the 25-substitution scan when moving to bidirectional BFS. Was that necessary? Try to keep the pattern map in the bidirectional version. What goes wrong, and is the resulting code clearer or worse?
- For what kind of word list would the brute-force Hamming-distance comparison actually be faster? (Hint: tiny N.)
- The candidate said "begin==end usually returns 0 or 1". Pick one and defend it.
