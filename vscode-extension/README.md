# DSA Journey — VS Code Extension

IDE companion for the [my-DSA-journey](../) curriculum. Jump between language
tracks, run the test harness, and open weekly quizzes, challenges, and
patterns from any source file in the repository.

## Features

| Command | What it does |
| --- | --- |
| `DSA Journey: Open Weekly Quiz` | Runs `./scripts/journey quiz <N>` in the integrated terminal, where `<N>` is the week of the active file. |
| `DSA Journey: Open Week Challenges` | Opens `Week N/challenges.md` for the current file's week. |
| `DSA Journey: Open Week Patterns` | Opens `Week N/patterns.md` for the current file's week. |
| `DSA Journey: Open This Topic in All Languages` | Given a topic file in any language, opens the equivalent file in the other four languages, each in its own editor column. |
| `DSA Journey: Run Full Test Harness` | Runs `python tests/harness/harness.py --all` in the integrated terminal. |
| `DSA Journey: Open INDEX.md` | Opens the top-level curriculum index. |

All commands are available via the command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
The cross-language command is also wired into the editor title bar for
`.java`, `.py`, `.cpp`, `.rs`, and `.html` files.

## How week detection works

When you invoke a command, the extension walks up from the active editor's
file path looking for a directory matching `Week N`. The immediately enclosing
directory (e.g. `java`, `python`, `cpp`, `rust`, `web`) is treated as the
language. The file's basename (without extension) is the topic stem used to
find sibling implementations.

So opening `/repo/Week 14/python/avl_tree.py` and running
**Open This Topic in All Languages** will try to open:

- `/repo/Week 14/java/avl_tree.java`
- `/repo/Week 14/cpp/avl_tree.cpp`
- `/repo/Week 14/rust/avl_tree.rs`
- `/repo/Week 14/web/avl_tree.html`

Missing files are skipped silently.

## Installation (sideload)

The extension is not yet published to the VS Code marketplace. To install
locally:

1. `cd vscode-extension`
2. `npm install`
3. `npm run compile`
4. `npm run package` (requires `vsce`; installed as a dev dependency).
5. In VS Code, open the command palette and run `Extensions: Install from VSIX…`
   then pick the generated `dsa-journey-0.1.0.vsix`.

Alternatively, open this `vscode-extension/` folder in VS Code and press
`F5` to launch an Extension Development Host with the extension loaded.

## Development

```sh
cd vscode-extension
npm install
npm run compile     # one-shot TypeScript build into ./out
npm run watch       # rebuild on save
```

Source lives in `src/extension.ts`; the build emits to `out/extension.js`,
which is the entry referenced by `package.json`.

## Packaging

```sh
npm run package
```

This invokes `vsce package` and writes a `.vsix` next to the manifest. Publish
with `vsce publish` once a publisher account is set up.

## Screenshots

_TODO: add screenshots here once the extension has been demoed locally._

- Cross-language split view
- Running the quiz from the terminal
- Test harness output

## Requirements

- VS Code 1.85 or newer.
- The workspace must contain the my-DSA-journey repository (or a checkout with
  the same `Week N/` layout).
- `./scripts/journey` and `python tests/harness/harness.py` must be runnable
  from the repo root.

## License

MIT — see the repository root `LICENSE` file.
