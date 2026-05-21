> यह अंग्रेज़ी मूल का अनुवाद है। यदि कुछ अस्पष्ट हो, तो [अंग्रेज़ी संस्करण](../../PROBLEM_SOLVING.md) देखें।

# Problem-Solving — सोचने का तरीका (Mindset Manifesto)

> 30 हफ़्तों का DSA पाठ्यक्रम आपको सिखा सकता है कि algorithms *क्या* हैं। यह फ़ाइल इस बारे में है कि *कैसे सोचा जाए* जब कोई ऐसी समस्या आपकी स्क्रीन पर आ जाए जिसे आपने पहले कभी नहीं देखा। इसे एक बार पढ़िए। फिर Week 10 के बाद दोबारा पढ़िए। फिर Week 20 के बाद और एक बार।

> **30 हफ़्ते देने से पहले इसे practice में महसूस करना चाहते हैं?** [Quickstart](QUICKSTART.md) पर 4 घंटे लगाइए — आठ चुनी हुई problems जो आपको नीचे दिए गए पूरे loop में ले जाती हैं। या [Diagnostic](diagnostic.md) देकर पता लगाइए कि curriculum में आप वास्तव में कहाँ हैं।

---

## यह क्यों है

यह repository data structures और algorithms सिखाती है। यह problem solving सिखाने जैसा नहीं है।

एक **coder** को syntax आती है, standard library आती है, और एक catalog में रखे हुए algorithms के नाम याद होते हैं। उन्हें सही keyword वाली problem दे दीजिए ("sorted array" → binary search) और वे solution ship कर देते हैं।

एक **problem solver** कुछ और होता है। वह एक नई, अजनबी problem के सामने बैठकर घबराता नहीं। वह उसे तब तक restate करता रहता है जब तक वह फिसलनी न रहे। वह छोटा example हाथ से बनाकर देखता है। वह एक brute-force solution लिखता है जिसके बारे में उसे पता है कि वो बहुत slow है — *जान-बूझकर*, क्योंकि वही solution problem की structure को सामने ले आता है। फिर वह वही एक सवाल पूछता है जो computer science के लगभग हर optimization के पीछे है: *कौन सा काम बेकार हो रहा है?* उसका जवाब ही algorithm है।

आप यहाँ 200 LeetCode patterns रटने नहीं आए हैं। आप यहाँ ऐसा इंसान बनने आए हैं जो किसी ऐसी problem का सामना करके भी आगे बढ़ सके जिसे अब तक किसी ने हल नहीं किया। Patterns scaffolding हैं। Mindset ही असली चीज़ है।

---

## Polya के चार steps

George Polya की *How to Solve It* (1945) आपकी reading list की हर textbook से पुरानी है और उनमें से अधिकतर से ज़्यादा useful है। चार steps:

### 1. समस्या को समझिए (Understand the problem)
इसे दो बार पढ़िए। फिर तीन बार पढ़िए। अपने शब्दों में लिखिए:
- Inputs क्या हैं? (types, ranges, क्या वे sorted हैं, क्या उनमें duplicates हो सकते हैं, क्या वे empty हो सकते हैं)
- Output क्या है? (एक value, एक structure, सारे valid configurations)
- यहाँ "valid" या "best" का क्या मतलब है?
- Problem statement *क्या नहीं* कहती? (अक्सर यह सबसे ज़रूरी सवाल होता है)

**उदाहरण.** "Find the longest substring with at most K distinct characters." कुछ भी करने से पहले: क्या K ≥ 1 guaranteed है? Characters ASCII हैं या Unicode? अगर string empty है, तो answer 0 है या undefined? "Substring" contiguous है (हाँ, convention के अनुसार) या "subsequence" (non-contiguous)? अगर यह step skip कर देंगे, तो आप गलत problem solve करेंगे और बीस मिनट तक आपको पता ही नहीं चलेगा।

### 2. योजना बनाइए (Devise a plan)
एक भी line code लिखने से पहले, approach को English में (या अपनी भाषा में) बोलकर देखिए। "I'll use a sliding window where the right pointer expands until the window has K+1 distinct chars, then the left pointer shrinks until it has K again. I track the max length along the way." अगर आप इसे दो वाक्यों में नहीं कह सकते, तो आपके पास अभी plan है ही नहीं।

यही वो जगह है जहाँ आप नई problem को पुरानी problems से जोड़ते हैं। "यह 'minimum window substring' जैसी लग रही है।" "यह तो बस BFS है implicit graph पर।" Pattern recognition एक planning skill है, memorization skill नहीं।

### 3. योजना को execute कीजिए (Carry out the plan)
अब आप code लिखते हैं। Plan से code तक का translation mechanical होना चाहिए। अगर typing करते-करते आप बड़े decisions ले रहे हैं, तो रुकिए — आपने step 2 skip कर दिया है।

### 4. पीछे मुड़कर देखिए (Look back)
यह step हर कोई skip कर देता है। Solution pass होने के बाद:
- क्या मैं और tight complexity bound निकाल सकता हूँ?
- क्या मैं code simplify कर सकता हूँ? (variables rename करना, special cases हटाना, unused branch निकालना)
- *Key insight* क्या था? एक वाक्य में लिखिए। वही वाक्य अगली problem में transfer होगा।
- यह किस family की problem है? अपने mental index में जोड़िए।

**Worked example — Two Sum.**
1. *Understand.* `nums` और `target` दिए गए हैं, उन दो indices को return करिए जिनका sum `target` हो। ठीक एक solution है। एक ही element दो बार use नहीं कर सकते। Indices चाहिए, values नहीं।
2. *Plan.* Brute force O(n²) pairs। बेहतर: हर `x` के लिए, हमें `target - x` चाहिए। Lookup O(1) है hash से। एक बार walk करते हैं, hash से पूछते हैं कि `target - nums[i]` पहले देखा गया है क्या, नहीं तो `nums[i] → i` store कर देते हैं।
3. *Execute.* दस lines का code।
4. *Look back.* Key insight: *हमें pair खोजने की ज़रूरत नहीं है; हमें यह पूछना है कि complement मौजूद है या नहीं*। यह reframing — "search → existence query" — वही move है जो 3Sum, 4Sum, two-pointers-on-sorted आदि के पीछे है। Technique portable है; code नहीं, move याद रखिए।

---

## अस्पष्ट problems को restate करना

असली problems — work पर, research में, interviews में — vague आती हैं। उन्हें tighten करने की practice कीजिए।

| Vague prompt | Tightened version |
|---|---|
| "Find duplicates in this array." | "उन values का set return कीजिए जो एक से ज़्यादा बार आती हैं। Order matter नहीं करता। Array memory में fit होती है। Values 32-bit integers हैं।" |
| "Schedule the meetings." | "`(start, end)` intervals की list दी गई है, ज़्यादा से ज़्यादा कितने mutually non-overlapping intervals चुने जा सकते हैं? सिर्फ़ endpoint share करने वाले दो intervals overlap नहीं करते।" |
| "Find the shortest path." | "Unweighted undirected graph, 10⁵ nodes तक; `s` से `t` तक के shortest path में edges की संख्या return कीजिए, या `-1` अगर unreachable है।" |
| "Compress this string." | "हर `k ≥ 2` identical characters के run को `c` के बाद decimal में count से replace कीजिए। Length 1 के runs वैसे ही रहते हैं। Output input से छोटा होना चाहिए, वरना input as-is return कीजिए।" |
| "Find the best route." | "*Best* किस metric से — distance, time, fuel, fewest transfers? Edges weighted हैं? Weights negative हो सकते हैं? Graph dense है या sparse?" |

Pattern गौर कीजिए: vague prompts में **implicit constraints** होते हैं जो पूछने वाले के दिमाग में होते हैं और आपके नहीं। जब तक constraints कागज़ पर नहीं हैं, तब तक वह problem नहीं है — एक wish है।

जब अकेले काम कर रहे हों (पूछने वाला कोई नहीं है), तो problem को खुद से restate कीजिए और **constraints lock कीजिए**। उन्हें अपनी scratch file के सबसे ऊपर लिखिए। अब वे spec का हिस्सा हैं।

---

## Constraints पहचानना — हर एक *क्या बताता है*

Constraints problem statement का सबसे कम पढ़ा जाने वाला हिस्सा होते हैं। और साथ ही room में सबसे ज़ोर से बजने वाले hints भी। उन्हें ऐसे पढ़िए जैसे compiler types पढ़ता है।

**Input size N.** यह एक number आपके algorithm class को किसी भी और information से ज़्यादा संकीर्ण कर देता है।

| N up to | Algorithms that fit (~1 sec budget) |
|---|---|
| ~10 | कुछ भी। O(N!) brute force भी चलेगा। Backtracking, permutations. |
| ~20 | O(2^N) bitmask DP, meet-in-the-middle. |
| ~500 | O(N³) ठीक है — Floyd-Warshall, interval DP. |
| ~5,000 | O(N²) ठीक है — quadratic DP, all-pairs scans. |
| ~10⁵ | O(N log N) — sorting, segment trees, Dijkstra with heap. |
| ~10⁶ | O(N) या O(N log log N) — linear scans, sieves, hashing. |
| ~10⁸+ | O(log N) या O(1) per query — preprocessed, math, या आप streaming कर रहे हैं। |

अगर problem कहती है `N ≤ 20` और आप polynomial DP की तरफ बढ़ रहे हैं, तो आप overthinking कर रहे हैं। अगर `N ≤ 10⁶` है और आपका plan O(N²) है, तो आप under-thinking कर रहे हैं।

**Time limit.** "2 seconds" + N मिलकर वही कहानी दूसरी तरफ से बताते हैं। Modern machines roughly 10⁸–10⁹ simple operations प्रति second कर सकती हैं। अपने N को अपने big-O से गुणा कीजिए और देखिए कि product fit होता है या नहीं।

**Memory limit.** 256 MB लगभग 6×10⁷ ints है। अगर problem आपको N=10⁶ देती है और N×N table माँगती है, तो आपको O(N) या O(log N) space चाहिए — यह आपको space-optimized DP, rolling arrays, या in-place algorithms की तरफ़ धकेलता है।

**Ordering / sortedness.** "The array is sorted" एक बड़ा flashing sign है जो कहता है *binary search, two pointers, or merge*। "The values are distinct" duplicate-handling edge cases को हटा देता है। "The input is a permutation of 1..N" cycle decomposition और counting tricks के दरवाज़े खोलता है।

**Mutability.** क्या आप input modify कर सकते हैं? अगर हाँ, तो in-place tricks (negative-marking, swap-to-index) free मिल जाती हैं। अगर नहीं, तो कम से कम O(N) auxiliary space चाहिए।

**Real numbers vs. integers.** Integer-only counting sort, bitmask, modular arithmetic, और exact comparison को खोलता है। Floats आपको precision, epsilon comparisons, और numerically stable formulations के बारे में सोचने पर मजबूर करते हैं।

**Online vs. offline.** Offline का मतलब है आप सारे queries पहले से देख सकते हैं — आप उन्हें reorder कर सकते हैं, batch कर सकते हैं, sweep कर सकते हैं। Online का मतलब है हर query का जवाब अगली देखने से पहले देना होगा — segment trees, balanced BSTs, persistent structures।

**Constraints पहले पढ़िए, फिर problem।** यह typo नहीं है। Constraints अक्सर answer का shape बता देते हैं इससे पहले कि आप पढ़ें कि question क्या है।

---

## Brute → better → optimal की सीढ़ी

इस पूरे document की सबसे ज़रूरी आदत।

**Step 1 — Brute force.** सबसे dumb correct solution लिखिए जो आप लिख सकते हैं। हर pair try कीजिए, हर subset, हर path। यह step skip मत कीजिए। अगर brute force इतना slow है कि type ही नहीं हो सकता, तो उसका *recurrence* कागज़ पर लिखिए।

यह क्यों matter करता है:
- यह pin कर देता है कि "correct" का क्या मतलब है — अब आपके पास एक reference implementation है जिसके against test किया जा सकता है।
- यह **structure** को expose करता है। Brute solution का bottleneck वहीं है जहाँ optimization रहता है।
- यह problem का डर निकाल देता है। आप "मुझे solve करना नहीं आता" से "मेरे पास working O(N³) solution है, मैं इसे fast करना चाहता हूँ" तक पहुँच जाते हैं — ये दो अलग psychological states हैं।

**Step 2 — एक सवाल पूछिए.** *Brute force कौन सा काम बेकार कर रहा है?*

यह सवाल computer science के लगभग हर algorithmic improvement का engine है:

| Wasted work | Optimization it produces |
|---|---|
| एक ही subproblem को बार-बार compute करना | Memoization → DP |
| एक range जो अभी-अभी scan की थी उसे फिर scan करना | Prefix sums, sliding window |
| Sorted data में linearly search करना | Binary search |
| ऐसी value खोजना जिसे हम index कर सकते थे | Hash map |
| Moving window पर बार-बार `min` लेना | Monotonic deque |
| Tree को फिर-फिर traverse करना | Euler tour, DFS reuse |
| ऐसे choices try करना जो clearly dominate हो रहे हैं | Greedy + exchange argument |
| ऐसे edges examine करना जो answer सुधार नहीं सकते | Dijkstra's relaxation |

**Step 3 — Optimal (या काफ़ी अच्छा).** Optimization apply कीजिए। Small inputs पर brute solution से verify कीजिए। *उसके बाद* constants, SIMD, और cache behavior पर सोचिए — और usually ज़रूरत नहीं पड़ती।

Step 1 skip करना intermediate programmers की सबसे common गलती है। वे clever solution की तरफ़ कूदते हैं, एक case miss करते हैं, और अब वे एक clever solution debug कर रहे हैं जिसे वे ख़ुद पूरी तरह नहीं समझते। Brute force first. हमेशा।

---

## कब छोड़ देना है — गलत track पर होने के लक्षण

आप atki जाओगे। Stuck होना ठीक है। Ego की वजह से stuck रहना ठीक नहीं है। Signs कि आपका plan मर चुका है:

- **30+ minutes बिना working code और बिना shrinking problem के.** Bug पर stuck नहीं — approach पर stuck। Fresh page से start कीजिए।
- **आपके edge cases बढ़ते जा रहे हैं.** हर fix दो नए cases लाता है। Data structure गलत है, या invariant गलत है।
- **आपकी complexity analysis close नहीं हो रही.** आप कागज़ पर bound नहीं लगा पा रहे। Plan incoherent है; आपको ख़ुद नहीं पता वह क्या कर रहा है।
- **आप symptoms patch कर रहे हैं.** आपने `if (i == 0)` डाला, फिर `if (n == 1)`, फिर `if (arr[i] < 0)`। हर patch बताता है कि आपकी core logic वो case handle नहीं कर रही जिसे construction से handle करना चाहिए था।
- **आप थके हुए हैं और वही bug बार-बार आ रहा है.** दस minute के लिए दूर हो जाइए। यह आलस नहीं, debugging है।

**Ego के बिना backtrack कैसे करें.** लिखिए — सच में लिखिए — कि आपका current approach क्या assume कर रहा है। सबसे कमज़ोर assumption कौन सा है? उसे drop कीजिए। अक्सर सही algorithm आपके try किए हुए algorithm का sibling होता है, सिर्फ़ एक design choice का फ़र्क़ (BFS vs. DFS, sort by start vs. end, top-down vs. bottom-up)।

जल्दी bail out करना एक skill है। Minute 15 पर approach बदलने की cost कम है। Minute 90 पर catastrophic है।

---

## आम cognitive जाल

ये बार-बार दिखने वाले failure modes हैं। इन्हें name दीजिए ताकि अपने अंदर पहचान सकें।

- **Premature optimization.** Prefix sum करेगा कि नहीं यह check करने से पहले segment tree उठा लेना। Correctness से पहले constant-factor tweaks। Discipline: *correct, then clear, then fast*।
- **पहले idea पर anchor हो जाना.** आपका पहला plan आपको *the* plan लगता है क्योंकि वह आपने सोचा। ख़ुद को मजबूर कीजिए कि कम से कम तीन approaches generate करें फिर एक चुनें। Compare करना ही insight produce करता है।
- **Brute force लिखने से इनकार.** "यह मेरे level से नीचे है।" "वैसे भी slow है।" फिर भी लिखिए। यह reference implementation, test oracle, और thinking aid है। चार minute लगते हैं।
- **Recursion से डर.** Recursion notation है, magic नहीं। अगर recurrence लिख सकते हैं, function लिख सकते हैं। अगर recursion बहुत deep है, stack में convert कीजिए — यह mechanical transformation है, creative leap नहीं।
- **कलम-कागज़ skip करना.** हर problem एक index card पर fit हो जाती है। Array draw करना, tree sketch करना, पहले तीन iterations हाथ से walk करना — ये किसी भी debugger से fast bugs पकड़ते हैं। Keyboard typing के लिए है, सोचने के लिए नहीं।
- **Solution बहुत जल्दी पढ़ लेना.** बीस minute productive struggle दो घंटे की reading से ज़्यादा सिखाती है। अगर peek करना है तो *idea* peek कीजिए (एक sentence) और tab बंद कर दीजिए।
- **एक example से generalize कर लेना.** आपका code `[1,2,3]` पर चल रहा है। `[]`, `[5]`, `[5,5]`, `[5,4,3,2,1]`, `[-1,-2]`, और सबसे बड़ा input try कीजिए। Edge cases optional नहीं हैं।
- **Complexity गलत पढ़ना.** "It's O(N log N) because I sorted." पर inner loop O(N) है, तो overall O(N² log N)। संदेह हो तो recompute कीजिए।

---

## 7 problem archetypes

ज़्यादातर coding-interview और competitive problems इन्हीं में से एक का भेस होती हैं। हर एक का एक "smell" है — surface feature जो underlying shape का hint देती है।

| Archetype | Smell | इस repo में कहाँ |
|---|---|---|
| **Search & sort** | "Sorted array", "find the K-th", "smallest such that…" | Weeks 8–9 |
| **Two pointers** | "Sorted array में property X वाला pair", "in-place rearrange" | Week 30 |
| **Sliding window** | "Property X वाला longest/shortest contiguous subarray" | Weeks 6, 13, 30 |
| **BFS / DFS** | "Reachable", "connected", "unweighted graph में shortest", "सब explore करो" | Week 17 |
| **Dynamic programming** | "कितने तरीक़े", "choices पर min/max", "overlapping subproblems के साथ optimal substructure" | Weeks 18, 23 |
| **Greedy** | "Schedule", "X की कम से कम संख्या", "local choice safe साबित कर सकते हैं" | Week 19 |
| **Divide & conquer** | "Halves पर recurse", "results merge", "O(N log N) plausible है" | Week 9 (merge/quick sort), Week 27 (closest pair) |

ये overlap होते हैं। Sliding window two pointers का specialization है। DP अक्सर memoization के साथ divide & conquer से निकलता है। Greedy DP है जब आप साबित कर सकें कि सिर्फ़ एक choice ever matter करती है। Boundaries धुंधली हैं — labels scaffolding हैं, truth की categories नहीं।

जब नई problem आए, quick triage करें: सात smells में से कौन से दिख रहे हैं? अगर दो हैं, तो answer probably उनको combine करता है।

---

## Closing reading list

- **Polya, *How to Solve It* (1945).** छोटा। पुराना। फिर भी इस topic पर सबसे अच्छी किताब। साल में एक बार पढ़िए।
- **Skiena, *The Algorithm Design Manual*, 3rd ed.** Chapters 1–3 problem-solving philosophy के लिए; "war stories" gold हैं। दूसरे half का catalog working programmer's reference है।
- **CLRS (Cormen, Leiserson, Rivest, Stein), *Introduction to Algorithms*, 4th ed.**
  - Chapter 1 — The role of algorithms.
  - Chapter 2 — Getting started (insertion sort as a worked Polya example).
  - Chapter 4 — Divide and conquer (recurrences, master theorem).
  - Chapter 15 — Dynamic programming (rod-cutting derivation canonical brute → better → optimal walkthrough है)।
  - Chapter 16 — Greedy algorithms (और correctness कैसे prove करते हैं)।
- **Bentley, *Programming Pearls*.** Column 2 ("Aha! Algorithms") और Column 8 ("Algorithm Design Techniques") इस mindset के लिए सबसे useful हैं।
- **Kleinberg & Tardos, *Algorithm Design*.** Chapter 1 का gale-shapley walkthrough vague problem को precise बनाने का masterclass है।

इन्हें curriculum के साथ-साथ पढ़िए, बाद में नहीं। Point इन्हें finish करना नहीं है — point यह है कि जब stuck हों, ये खुली हों।

---

> इस repo के algorithms tools हैं। *Problem solving* workshop है। Toolbox से ज़्यादा time workshop में बिताइए।
