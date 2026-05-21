> यह अंग्रेज़ी मूल का अनुवाद है। यदि कुछ अस्पष्ट हो, तो [अंग्रेज़ी संस्करण](../../QUICKSTART.md) देखें।

# Quickstart — 4 घंटे में देखिए कि यह Repo आपके लिए काम करता है या नहीं

अगर 30 हफ़्ते डराने वाले लगते हैं: वहाँ से start मत कीजिए। इस curated path पर 4 focused घंटे लगाइए। अंत तक आपने 5 difficulty levels की 8 representative problems पर पूरी methodology practice कर ली होगी। अगर loop आपके लिए काम करता है, तो long path बस उसी loop के और reps हैं।

Loop वही है जो [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) में सिखाया गया है:

> Understand → Plan (brute → better → optimal) → Execute → Look back (journal)।

आप आज वह loop आठ बार करेंगे।

---

## शुरू करने से पहले (10 min)

1. [`PROBLEM_SOLVING.md`](PROBLEM_SOLVING.md) पढ़िए — कम से कम **"Polya के चार steps"** और **"Brute → better → optimal की सीढ़ी"** sections skim कीजिए।
2. [`docs/SOLUTION_JOURNAL.md`](../../docs/SOLUTION_JOURNAL.md) को अपनी working directory में `my_journal.md` के नाम से copy कीजिए (commit मत कीजिए)। हर problem के लिए एक entry append करेंगे।
3. 4-घंटे का timer लगाइए। अगर किसी problem के budget से 5 minutes से ज़्यादा निकल जाएँ, तो रुकिए, reference file peek कीजिए, और आगे बढ़ जाइए। आज का point *loop का coverage* है, perfect solutions नहीं।
4. Scratch editor में दो panes खोलिए: बाईं तरफ़ problem, दाहिनी तरफ़ journal।

> **एक rule, non-negotiable.** हर problem को reference file खोलने से *पहले* attempt कीजिए। पहले answer पढ़ लेना training को entertainment में बदल देता है।

---

## Hour 1 — Foundations (pattern पहचानना)

लक्ष्य: brute force और "right tool" का फ़र्क़ feel कीजिए। दो छोटी problems, फिर एक pattern drill।

### Problem 1: Two Sum (15 min, Easy)
- **Reference (attempt के बाद ही peek करें)**: [`Week 16/java/1.HashingAndHashMap.java`](../../Week%2016/java/1.HashingAndHashMap.java) — सिर्फ़ `twoSum` function skim कीजिए (line 43 के आसपास)।
- **Spec**: `nums` और `target` दिए गए, उन दो indices को return कीजिए जिनकी values sum होकर `target` बनती हैं। ठीक एक solution मानिए।
- **Task**: बिना देखे, अपनी पसंदीदा language में solve कीजिए। पहले brute-force `O(N²)` लिखिए, फिर hash-map `O(N)` version।
- **Journal (2 min)**: कौन सा pattern use किया? Brute-force `O(N²)` क्यों था? *Key insight* एक वाक्य में लिखिए — वही transfer होगा।

### Problem 2: Maximum Subarray / Kadane (15 min, Easy)
- **Reference**: [`Week 6/python/4.prefix_sum_and_kadane.py`](../../Week%206/python/4.prefix_sum_and_kadane.py) — Part B, Kadane's algorithm.
- **Spec**: integer array दी गई (values negative भी हो सकती हैं), उस contiguous subarray को ढूँढिए जिसका sum maximum है। Sum return कीजिए।
- **Task**: पहले brute-force (हर `(i, j)` pair, O(N²) या O(N³)), फिर Kadane का `O(N)` running-best recurrence derive कीजिए। दोनों लिखे बिना peek मत कीजिए।
- **Journal (2 min)**: Brute force ने कौन सा काम waste किया? Kadane हर step पर कौन सा invariant maintain करता है?

### Problem 3: Pattern Recognition Drill (10 min)
- [`Week 6/patterns.md`](../../Week%206/patterns.md) खोलिए। **Drills 1–5** cold कीजिए (बाक़ी file या solutions peek मत कीजिए)।
- हर एक के लिए एक line लिखिए: कौन सा pattern (two pointers / sliding window / prefix sum / Kadane / Dutch flag / hash) और एक-वाक्य justification।
- फिर file के नीचे answer key से ख़ुद को check कीजिए।

### Hour 1 wrap (5 min)
Journal में 3 sentences में जवाब दीजिए:
1. आपको सबसे मुश्किल क्या लगा — problem restate करना, pattern चुनना, या code करना?
2. कौन सी problem "hindsight में obvious" लगी? पहले obvious क्यों नहीं थी?
3. क्या आपने Problem 2 पर सच में पहले brute force लिखा, या सीधे Kadane पर कूद गए?

---

## Hour 2 — Structures (सही tool बनाना)

लक्ष्य: देखिए कि *data structure चुनना* अक्सर *algorithm है*।

### Problem 4: दो Sorted Linked Lists Merge करना (25 min, Medium)
- **Reference**: [`Week 11/python/2.MergeSortedListsAndLRU.py`](../../Week%2011/python/2.MergeSortedListsAndLRU.py) — सिर्फ़ merge function। LRU section अभी मत पढ़िए।
- **Spec**: दो sorted singly linked lists दी गई हैं, एक merged sorted list return कीजिए। Nodes reuse कीजिए (copy मत कीजिए)।
- **Task**: पहले कागज़ पर sketch कीजिए। दो lists, दो pointers draw कीजिए, और trace कीजिए कि अगला कौन सा node splice करना है। फिर code कीजिए। एक dummy/sentinel head use कीजिए — यह "first node is special" case हटा देता है।
- **Journal (3 min)**: Dummy head code छोटा क्यों करता है? Time और space complexity क्या है, और space कहाँ जाता है?

### Problem 5: Binary Tree — Maximum Depth (15 min, Easy–Medium)
- **Reference**: [`Week 14/python/1.BinaryTree.py`](../../Week%2014/python/1.BinaryTree.py) — depth / height function ढूँढिए।
- **Spec**: binary tree का root दिया गया, उसकी depth return कीजिए (longest root-to-leaf path पर nodes की संख्या)।
- **Task**: recursively तीन lines में लिखिए। फिर iterative version queue से (level-order, levels count) लिखिए।
- **Journal (2 min)**: एक line में recurrence: `depth(root) = ...`। यह DP recurrence का same shape है; यह आपको फिर मिलेगा।

### Hour 2 wrap (5 min)
- आपको कौन सी structure ने surprise किया — linked list या tree?
- क्या आप Problem 5 को [`Week 5/python/3.recursion_basics.py`](../../Week%205/python/3.recursion_basics.py) वाली recursion habit से solve कर सकते थे? उसे संक्षेप में खोलकर confirm कीजिए — recursion ही through-line है।

---

## Hour 3 — Algorithms (सही approach चुनना)

लक्ष्य: "data structure क्या है?" से बढ़कर "*technique* क्या है?" तक पहुँचना।

### Problem 6: K Distinct Characters वाला Longest Substring (25 min, Medium)
- **Reference**: [`Week 30/python/sliding_window.py`](../../Week%2030/python/sliding_window.py) — variable-size window template।
- **Spec**: string `s` और integer `k` दिए, उस longest substring की length return कीजिए जिसमें ज़्यादा से ज़्यादा `k` distinct characters हों।
- **Task**: पहले brute force (हर substring, distinct count → `O(N²)` या `O(N³)`)। फिर sliding window derive कीजिए: right expand, left तब तक shrink जब distinct count `k` से ज़्यादा हो, max length track कीजिए। `O(N)`।
- **Journal (3 min)**: Window कौन सा invariant maintain करता है? हर character ज़्यादा से ज़्यादा दो बार क्यों visit होता है (एक `right` से, एक `left` से)?

### Problem 7a (warm-up before the open challenge): BFS reasoning (15 min, Medium)
- **Reference**: [`Week 17/python/1.GraphRepresentations.py`](../../Week%2017/python/1.GraphRepresentations.py) — BFS function।
- **Spec**: unweighted undirected graph adjacency list के रूप में दिया, और दो nodes `s` और `t`, shortest path में edges की संख्या return कीजिए, या `-1` अगर unreachable है।
- **Task**: BFS scratch से लिखिए। Queue और visited set use कीजिए। Depth track कीजिए — या तो `(node, depth)` tuples store करके, या queue एक level at a time process करके।
- **Journal (2 min)**: BFS unweighted graph में shortest path क्यों देता है पर weighted में नहीं? (अगर नहीं पता, तो यह आपका Week 22 की तरफ़ signpost है।)

### Hour 3 wrap (5 min)
Sliding window और BFS दोनों "frontier carefully expand करना" हैं। Journal में note कीजिए: ये क्या share करते हैं, और क्या उन्हें अलग बनाता है (एक 1-D array पर चलता है, दूसरा arbitrary graph पर)।

---

## Hour 4 — Synthesis (simulated pressure में end-to-end करना)

लक्ष्य: loop को end-to-end एक ऐसी problem पर combine कीजिए जिस पर आपको spoon-feed नहीं किया गया।

### Problem 8: Open-ended challenge (40 min, Hard)
[`Week 8/challenges.md`](../../Week%208/challenges.md) से **एक** challenge चुनिए — recommended: **Challenge 1 (Closest Element in a Rotated Sorted Array)** अगर binary search देखा है, वरना उसी file का **Challenge 2**।

Rules:
1. Journal entry के top पर spec अपने शब्दों में restate कीजिए। Constraints लिखिए।
2. Code लिखने *से पहले* approach को 2 sentences में English (या अपनी भाषा) में sketch कीजिए।
3. Implement कीजिए। `Week 8/python/`, `Week 8/java/` आदि की किसी file को peek मत कीजिए।
4. Challenge file में दिए inputs पर test कीजिए।
5. यह काम करने के बाद (या 40 min के बाद, जो भी पहले हो) ही canonical solution से अपना diff कीजिए। क्या अलग किया?

### Problem 9: Mock interview self-review (15 min)
[`mock_interviews/01_two_sum_warm_up.md`](../../mock_interviews/01_two_sum_warm_up.md) पढ़िए — Hour 1 की पहली problem का annotated transcript।

- अपनी Hour-1 thought process को transcript के annotated good habits (callouts) से compare कीजिए।
- *आपने* क्या किया जिसे transcript ने "good" कहा है? (जैसे duplicates पूछना, problem restate करना, tradeoffs बोलकर बताना।)
- क्या skip किया? (जैसे complexity announce की? Brute force mention किया solve करने से पहले?)

### Hour 4 wrap (5 min)
Journal में लिखिए:
- आपका Hour-4 challenge solution brute force के क़रीब था, "better" था, या optimal? क्यों?
- आज Polya के चार steps में से कौन सा सबसे ज़्यादा skip किया? (ज़्यादातर learners step 4 "Look back" skip करते हैं।)
- अगली बार क्या अलग करोगे?

---

## अब क्या?

आपने अभी पूरे curriculum का microcosm कर लिया है। आठ problems, पाँच difficulty levels, loop की हर layer। अगर value आई:

- **Diagnostic लीजिए** ([`docs/diagnostic.md`](../../docs/diagnostic.md)) — असली starting point पता करिए। जो हफ़्ते master हैं, skip कीजिए।
- **8 हफ़्तों का focused interview prep**: root README में [Learning Path 2 (Interview Prep)](../../README.md#path-2-interview-prep-8-weeks) follow कीजिए — Weeks 6, 8, 11, 14, 16, 17, 18, 30।
- **पूरा 30 हफ़्ते**: Week 1 से start कीजिए और हर problem पर journal लिखिए। ज़्यादातर लोग जो finish करते हैं इसी तरह करते हैं।
- **Competitive programming**: [Path 3](../../README.md#path-3-competitive-programming-10-weeks) follow कीजिए।

अगर value नहीं आई, तो bounce करने से पहले ईमानदारी से check कीजिए:

- क्या आपने सच में हर problem attempt की peek करने से पहले?
- क्या journal किया, या सिर्फ़ पढ़ा?
- क्या Problems 2, 6, और 7a पर brute force *पहले* लिखा — या सीधे clever solution पर?
- क्या Problem 8 पर canonical version से अपना code compare किया?

ज़्यादातर "मेरे लिए काम नहीं किया" outcomes एक specific skip तक trace होते हैं: journaling step। Journal वो जगह है जहाँ methodology actually रहती है। Code byproduct है।

---

> एक बार आप loop आठ बार कर लो, तो आपने आठ बार किया। यह कुछ नहीं नहीं है। आदत ऐसे ही start होती है।
