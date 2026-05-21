# Bug Case Study: Missing React keys turn O(n) diffs into O(n²) DOM churn

**Project**: React reconciler (the original Stack reconciler, and the same hazard in the Fiber reconciler). Approximate reconstruction of a class of bug that every React-using product has hit at least once; called out in React's own docs and in countless GitHub issues across UI libraries.
**Date**: 2014–present (the "key prop" warning predates React 1.0)
**Severity**: performance (and sometimes correctness — input focus, scroll position, animation state)
**DSA principle**: comparing two sequences cheaply requires a stable identity per element — Week 16 (hashing) and Week 18 (DP on sequences)

## What happened

React's reconciler is asked, on every render, to turn an *old* tree of elements into a *new* tree of elements with the smallest possible number of DOM operations. The hard case is a list: you have an old children array and a new children array, and you have to figure out which children are the same, which moved, which were added, and which were removed.

The general "edit distance between two sequences" problem is O(n × m) (Wagner–Fischer / Hunt–McIlroy). React deliberately doesn't pay that cost — its reconciler is a linear-time heuristic that matches children by **position and identity**. Identity is the `key` prop. If you provide stable keys, the reconciler can do an O(n) two-cursor walk: keys that match in both lists are reused, keys missing from the new list are deleted, keys new in the new list are inserted, and keys that moved are repositioned via hash-table lookup.

If you *don't* provide keys, the reconciler falls back to matching by index. Inserting a single element at the *front* of a 10,000-item list makes every subsequent index "mismatch": React tears down and rebuilds every child below the insertion point, because element 0 used to be Alice and is now the new entry, element 1 used to be Bob and is now Alice, and so on. Worse, if your children are stateful (an `<input>` with focus, a `<video>` mid-playback, a list row mid-animation), all that state is destroyed — the bug shows up as "the cursor jumped" or "the video restarted" long before anyone profiles the render time.

The other common variant is `key={index}`. This *silences the warning* but provides no actual identity: it's equivalent to no key, and produces the same teardown-on-insert behavior.

## The naive code

```jsx
// Renders fine the first time, churns the DOM on every reorder/insert.
function TodoList({ items }) {
  return (
    <ul>
      {items.map((item, i) => (
        <li key={i}>                   {/* key={index} == no key */}
          <input defaultValue={item.text} />
        </li>
      ))}
    </ul>
  );
}
```

When `items` changes from `[A, B, C]` to `[X, A, B, C]`, the reconciler matches:
- old index 0 (A) ↔ new index 0 (X) → mutate / re-mount
- old index 1 (B) ↔ new index 1 (A) → mutate / re-mount
- old index 2 (C) ↔ new index 2 (B) → mutate / re-mount
- (none) ↔ new index 3 (C) → create

All four list items churn. Any `<input>` focus is lost. With 10,000 rows, it's O(n) DOM operations for a single-row prepend — and in nested lists, this multiplies.

## The DSA insight

To diff two sequences in O(n) instead of O(n × m), you need a hash from "element identity" to "old position." React keeps a `Map<key, oldFiber>` for exactly this: it walks the new list, looks up each key in the map, and either reuses the existing fiber or creates a new one. The whole operation is O(n) only because hash-table lookup is O(1).

Take the keys away and you've taken the hash table away — the reconciler can't match A in the new list to A in the old list, so it falls back to a structurally weaker comparison (position) that produces a structurally worse diff. The same algorithmic principle shows up in Git's rename detection, `diff -u` line matching, and Myers' diff for editor history. **Cheap sequence diffing requires per-element identity.**

The Week 18 view (LCS, edit distance) is the *expensive* version: O(n × m) DP that finds an optimal diff with no identity. React traded optimality for linearity by demanding the user provide identity. Both are valid; you choose based on what guarantees you can ask of your input.

## The fix

```jsx
function TodoList({ items }) {
  return (
    <ul>
      {items.map(item => (
        <li key={item.id}>            {/* stable, unique, non-positional */}
          <input defaultValue={item.text} />
        </li>
      ))}
    </ul>
  );
}
```

Key requirements: **stable across renders** (don't generate a fresh UUID inside `map`), **unique among siblings** (not necessarily globally), **derived from data identity** (not from list position).

## What you can learn

- Whenever you diff two sequences, ask: do my elements have stable identity? If yes, you can match in O(n) with a hash. If no, you're paying O(n × m) DP or settling for a heuristic.
- A "key" / "id" / "ETag" / "row hash" is the universal trick: Git pack files, React reconciliation, database CDC streams, and `rsync`'s rolling-checksum approach all rely on it.
- Position is *not* identity. Anything keyed on index will silently misbehave under insertion / deletion / reorder.
- The warning "Each child in a list should have a unique key" is the linter telling you "you're about to opt into a quadratic-DOM-churn shape." Don't silence it with `key={index}`.

## Related curriculum
- Week 16 (Hashing) — the lookup that makes the linear-time diff possible
- Week 18 (DP — edit distance and LCS) — the costlier no-identity alternative
- `tests/cases/lcs.json` — implement the DP version and compare runtime against a hash-based diff for two near-identical lists of 10,000 elements
