> यह अंग्रेज़ी मूल का अनुवाद है। यदि कुछ अस्पष्ट हो, तो [अंग्रेज़ी संस्करण](../../docs/diagnostic.md) देखें।

# Diagnostic — कहाँ से Start करना चाहिए?

Curriculum के अलग-अलग हिस्सों से 15 questions। ईमानदारी से जवाब दीजिए। अंत में हम आपके जवाबों को recommended starting week से map कर देंगे।

**Test देते समय कुछ भी lookup मत कीजिए। Point calibrate करना है, score करना नहीं।** Time budget: ~25 minutes। अगर एक question पर दो minutes से ज़्यादा लग रहे हों, best guess लिखकर आगे बढ़िए।

एक simple answer sheet रखिए: `Q1: C`, `Q2: ...`, आदि। 15 के 15 जवाब देने के बाद ही answer key (नीचे collapsed) reveal कीजिए।

---

## Section 1: Foundations & Complexity (Q1–Q3)

### Q1. इस Python code की time complexity क्या है?

```python
def f(n):
    result = []
    for i in range(n):
        for j in range(i, n):
            result.append(i * j)
    return result
```

- A) O(N)
- B) O(N log N)
- C) O(N²)
- D) O(N³)

### Q2. आपके पास एक algorithm है जो N = 1,000 पर 1 second लेता है। मान लीजिए वह O(N log N) है, तो N = 1,000,000 पर लगभग कितना time लेगा?

- A) लगभग 1,000 seconds (~17 minutes)
- B) लगभग 2,000 seconds (~33 minutes)
- C) लगभग 1,000,000 seconds (~12 days)
- D) लगभग 10 seconds

### Q3. Short answer. एक problem की constraint है `1 ≤ N ≤ 20`। Problem के बारे में और कुछ जाने बिना, इस छोटे N पर कौन सी algorithm class *खुलती है* जो N = 10⁵ पर infeasible होती? एक शब्द या short phrase में जवाब दीजिए।

---

## Section 2: Arrays & Strings (Q4–Q5)

### Q4. आपको distinct integers की एक sorted array और एक target दिए गए हैं। आपको दो indices ढूँढने हैं जिनकी values का sum target हो। सबसे cleanest approach क्या है?

- A) Hash map: हर `x` के लिए, `target - x` lookup। O(N) time, O(N) space।
- B) दोनों ends से two pointers, current sum के आधार पर inward move। O(N) time, O(1) space।
- C) हर element का complement binary search। O(N log N) time, O(1) space।
- D) हर pair check करने वाला nested loop। O(N²) time, O(1) space।

> कई choices *correct* हैं इस मायने में कि "pass हो जाएगा"। उसको चुनिए जो input की structure का **सबसे ज़्यादा** exploit करे।

### Q5. आप characters की एक stream process कर रहे हैं और हर point पर, current character पर ख़त्म होने वाले उस longest substring की length चाहते हैं जिसमें कोई repeated character न हो। कौन सी technique?

- A) Substring sort करके dedupe करें।
- B) Hash set के साथ sliding window: right expand, duplicate window में होने पर left shrink।
- C) Dynamic programming, `dp[i] = dp[i-1] + 1` हमेशा।
- D) Suffix array।

---

## Section 3: Hash Maps & Data Structures (Q6–Q8)

### Q6. Average-case में सही sized hash table में `insert`, `lookup`, और `delete` की time complexity क्या है?

- A) तीनों O(log N)।
- B) तीनों O(1) amortized average।
- C) Insert O(N), lookup O(1), delete O(N)।
- D) Insert O(1), lookup O(N), delete O(N)।

### Q7. आपको एक data structure चाहिए जो `get(key)` और `put(key, value)` O(1) average में करे, AND capacity exceed होने पर least-recently-used key evict करे। कौन सी दो structures compose करते हैं?

- A) दो stacks।
- B) Hash map + balanced BST।
- C) Hash map + doubly linked list।
- D) Min-heap + hash set।

### Q8. Short answer. एक छोटे वाक्य में: strings के एक set को store करने के लिए **trie** को **hash map** के बजाय कब चुनते हैं?

---

## Section 4: Trees, Recursion & Graphs (Q9–Q11)

### Q9. Binary tree का root दिया है, आप लिखते हैं `depth(root) = 1 + max(depth(left), depth(right))` base case `depth(None) = 0` के साथ। यह correct, idiomatic implementation है। इसकी time और space complexity क्या है (space = recursion stack), जहाँ `N` nodes की संख्या और `H` tree height है?

- A) Time O(N log N), space O(N)।
- B) Time O(N), space O(H)।
- C) Time O(H), space O(1)।
- D) Time O(N²), space O(N)।

### Q10. एक **unweighted undirected** graph में node `s` से `t` तक shortest path (edges की संख्या में) चाहिए। कौन सा traversal use करते हैं और क्यों?

- A) DFS, क्योंकि वह पहले deeper explore करता है।
- B) BFS, क्योंकि वह nodes को source से edge-distance के non-decreasing order में visit करता है।
- C) Dijkstra, क्योंकि वह general shortest-path algorithm है।
- D) Topological sort, क्योंकि वह ordering देता है।

### Q11. Short answer. आपको एक **directed** graph में cycle detect करनी है। आप DFS use करने का decide करते हैं। "Visited" set के अलावा कौन सी auxiliary state चाहिए, और क्यों? एक वाक्य।

---

## Section 5: DP & Advanced (Q12–Q15)

### Q12. इनमें से कौन सी problem dynamic programming से *सबसे cleanly* solve होती है (greedy, brute force, या single pass की बजाय)?

- A) Coin denominations और एक amount दिए गए हैं, amount बनाने के लिए coins की **minimum संख्या** return कीजिए। Denominations arbitrary हैं (जैसे `[1, 3, 4]`, amount `6` → `2`, not `3`)।
- B) Intervals की list दी गई है, mutually non-overlapping की maximum संख्या ढूँढिए।
- C) Array का sum return कीजिए।
- D) दो strings anagrams हैं या नहीं check कीजिए।

### Q13. आप देखते हैं "कितने distinct ways" recurrence shape `f(n) = f(n-1) + f(n-2)` जैसी, और constraints `N ≤ 10⁵` तक। Signal क्या है?

- A) Greedy: हर `n` पर locally best step लो।
- B) DP: recurrence memoize करो (या tabulate)। Overlapping subproblems पर ध्यान।
- C) Backtracking: सारे configurations enumerate करो।
- D) देखे गए `n` values का hash map।

### Q14. **Segment tree** कौन सी चीज़ में अच्छा है जो प्लेन prefix-sum array में नहीं है?

- A) "Sum of `a[l..r]`" को O(N) preprocessing के बाद O(1) में answer करना, जब array **static** हो।
- B) Point updates `a[i] = x` और queries interleaved, दोनों O(log N) में, "sum of `a[l..r]`" को answer करना।
- C) Array को O(N log N) में sort करना।
- D) Stream का median ढूँढना।

### Q15. Short answer. एक वाक्य में, explain कीजिए कि **network flow** (max-flow / min-cut) किस तरह की problem model करता है जो plain BFS/DFS नहीं करते। Algorithm names की चिंता मत कीजिए — सिर्फ़ *problem का kind*।

---

## यहाँ रुकिए। 15 जवाब देने के बाद ही score कीजिए।

<details>
<summary><b>Answer key + placement reveal करने के लिए click कीजिए</b></summary>

### Answer key

- **Q1: C** — outer loop N बार चलता है; inner `i` से `n` तक, तो total ops = N + (N-1) + ... + 1 = N(N+1)/2 ≈ N²/2। O(N²)।
- **Q2: B** — N log N scale by `(N₂/N₁) · (log N₂ / log N₁) = 1000 · (20/10) ≈ 2000`। So roughly 2,000 seconds। Choice C O(N³) होगा; choice A O(N²) होगा।
- **Q3** — **Bitmask DP** (या "subset enumeration / 2^N brute force / exponential search")। N ≤ 20 means 2^N ≤ ~10⁶, जो एक second में fit होता है। Week 23 में covered।
- **Q4: B** — Two pointers **sorted** structure को exploit करके O(N) time और O(1) space देता है। A काम करेगा पर O(N) space waste; C log factor waste; D sortedness ignore करता है। Question का point: वह technique चुनो जो input की structure का *सबसे ज़्यादा* use करे।
- **Q5: B** — classical sliding window with hash set / last-seen-index map। C गलत है क्योंकि `dp[i]` हमेशा `dp[i-1] + 1` के बराबर नहीं होता — यह depend करता है कि `s[i]` current window में पहले से है या नहीं।
- **Q6: B** — तीनों O(1) amortized average। Worst case O(N) अगर सारे keys एक bucket में hash हों, पर question average case पूछ रहा है।
- **Q7: C** — O(1) lookup के लिए hash map, हर access पर O(1) reordering के लिए doubly linked list। यही standard **LRU cache** structure है, Weeks 11, 16, और 29 में covered।
- **Q8** — जब **prefix queries** की ज़रूरत हो (जैसे autocomplete, "क्या कोई stored string `pre` से start होती है?"), या जब कई stored strings लंबे common prefixes share करती हों (memory saving)। Hash maps keys को opaque मानते हैं; tries shared prefix structure exploit करते हैं।
- **Q9: B** — हर node एक बार visit → O(N) time। Recursion depth = tree height → O(H) space। Balanced tree के लिए H = O(log N); degenerate (linked-list-like) tree के लिए H = N।
- **Q10: B** — BFS। Level-by-level expansion guarantee करता है कि जब आप किसी node पर पहली बार पहुँचते हैं, तो minimum edges use हुए हैं। Dijkstra भी काम करेगा पर overkill (और unnecessary log factor) है unweighted graphs के लिए।
- **Q11** — "Fully-visited" (black) set के अलावा **"currently on recursion stack" (a.k.a. "gray" or "in-progress")** set चाहिए। Gray node पर back edge cycle है। सिर्फ़ visited set से DAG में cross/forward edge को real back edge से distinguish नहीं कर सकते।
- **Q12: A** — arbitrary denominations वाला coin change canonical DP problem है (greedy fails `[1, 3, 4]` पर amount `6` के लिए — greedy `4 + 1 + 1` चुनता है; DP `3 + 3` ढूँढता है)। B greedy है (interval scheduling)। C और D single-pass।
- **Q13: B** — DP। Overlapping subproblems वाला Fibonacci-shaped recurrence textbook DP signal है। N ≤ 10⁵ पर naive recursion exponential; memoize या tabulate कीजिए।
- **Q14: B** — segment trees **point updates + range queries** दोनों O(log N) में handle करते हैं। Prefix-sum arrays range-sum O(1) में answer करते हैं पर O(N) per update; static array के लिए ही competitive।
- **Q15** — Network flow **capacity-constrained routing** model करता है — हर edge पर `c(u,v)` units तक भेज सकते हैं, source से sink तक maximum total throughput चाहिए। Equivalently (min-cut duality), यह problems solve करता है जैसे "`s` से `t` को disconnect करने वाला smallest edge set कौन सा है?" Plain BFS/DFS सिर्फ़ reachability या shortest path बताते हैं; capacity या aggregate flow के बारे में reason नहीं करते। कई unrelated lagne wali problems (bipartite matching, image segmentation, project selection) max-flow में reduce होती हैं।

### Placement matrix

Count कीजिए कि कितने *fully* right हुए (short-answer के लिए, अगर idea same है तो credit दीजिए even if wording अलग है)।

| Score | Recommended starting point |
|---|---|
| **0–3** | **Week 1** से start कीजिए। Foundations ज़रूरी हैं। Skip मत कीजिए — वे compound interest देते हैं। |
| **4–7** | Weeks 1–5 skim कीजिए (या skip अगर Q1–Q3 easy लगे)। **Week 6** (arrays) या **Week 8** (searching) से serious काम start कीजिए। |
| **8–11** | **Week 11** (linked lists) या **Week 14** (trees) से start कीजिए, इस पर depend करता है कि कहाँ miss किया। Q9–Q11 miss किया तो Week 14। Q6–Q8 miss किया तो Week 16। |
| **12–15** | **Week 17** (graphs) से start कीजिए या advanced topics (**Weeks 21+**) पर jump कीजिए। अगर Q14–Q15 भी सही, तो सीधे Weeks 23–24 (advanced DP & research-level)। |

**Diagnostic anomalies — ये भी पढ़ें:**
- **Sections 4–5 (Q9–Q15) ace किए पर section 1 (Q1–Q3) fail**: unusual। Algorithms लिख सकते हैं पर cost reason नहीं कर सकते। [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) में complexity analysis revisit कीजिए — specifically "Constraints पहचानना" section। फिर Week 8 पर लौटिए।
- **Sections 1–3 ace किए पर sections 4–5 fail**: classic profile। Solid foundations हैं पर algorithmic vocabulary build नहीं हुआ। **8-week interview prep path** पर jump कीजिए [root README](../../README.md#path-2-interview-prep-8-weeks) — Weeks 6, 8, 11, 14, 16, 17, 18, 30।
- **Q3, Q8, Q11, या Q15 fully right**: experienced practitioner की *vocabulary* है। MCQ score mid भी हो तो advanced path lean कीजिए।

### हर section ने क्या test किया

| Section | Tested | Covered in |
|---|---|---|
| 1 (Q1–Q3) | Complexity intuition, big-O scaling, constraint reading | Weeks 1–5, 8; [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) |
| 2 (Q4–Q5) | Array & string idioms — two pointers, sliding window | Weeks 6, 7, 10, 30 |
| 3 (Q6–Q8) | Hash maps, composite data structures, tries | Weeks 11, 16, 21 |
| 4 (Q9–Q11) | Recursion, trees, graph traversal reasoning | Weeks 5, 14, 17 |
| 5 (Q12–Q15) | DP recognition, segment trees, network flow | Weeks 18, 21, 23, 26 |

---

> चाहे जिस week पर land करें, diagnostic score और recommendation को journal की पहली entry के रूप में drop कीजिए। छह महीने बाद, जब आप भूल जाएँगे कि क्या नहीं आता था, यह सबसे ईमानदार snapshot होगा कि कहाँ से start किया।

</details>

---

## आगे क्या?

- Methodology में नए हैं? पहले [**Quickstart**](QUICKSTART.md) try कीजिए — 4 घंटे, 8 problems, पूरा loop।
- Commit करने को तैयार हैं? [**Root README**](../../README.md) पर जाइए और learning path चुनिए।
- Curriculum की philosophy चाहिए? [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) पढ़िए।
