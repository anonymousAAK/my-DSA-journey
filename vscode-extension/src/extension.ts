// DSA Journey — VS Code extension entry point.
//
// All commands derive context from the currently active editor's file path,
// which is expected to live somewhere under a `Week N/` directory in the
// workspace. The extension then constructs sibling paths for the other
// language tracks, the per-week markdown files, and shell commands.

import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

/**
 * Known per-week language directories. Order matters for the
 * "open across languages" multi-pane layout.
 */
const LANGUAGE_DIRS = ['java', 'python', 'cpp', 'rust', 'web'] as const;
type LanguageDir = typeof LANGUAGE_DIRS[number];

const LANGUAGE_EXTENSIONS: Record<LanguageDir, string> = {
    java: '.java',
    python: '.py',
    cpp: '.cpp',
    rust: '.rs',
    web: '.html',
};

interface WeekContext {
    /** Absolute path to the workspace root that contains the `Week N` dir. */
    repoRoot: string;
    /** Absolute path to the matched `Week N` directory. */
    weekDir: string;
    /** Numeric week (1..30) parsed from the directory name. */
    weekNumber: number;
    /** The language directory containing the active file, if any. */
    language?: LanguageDir;
    /** The topic stem (filename without extension), if applicable. */
    topicStem?: string;
}

/**
 * Walk upward from `startPath` looking for a `Week N` directory.
 * Returns the parsed context or undefined if not found.
 */
function detectWeekContext(startPath: string): WeekContext | undefined {
    let current = startPath;
    let language: LanguageDir | undefined;
    let topicStem: string | undefined;

    // The file's own basename gives us topicStem candidate.
    if (fs.existsSync(current) && fs.statSync(current).isFile()) {
        topicStem = path.basename(current, path.extname(current));
        current = path.dirname(current);
    }

    // The immediate parent directory may be a language folder.
    const immediateName = path.basename(current);
    if ((LANGUAGE_DIRS as readonly string[]).includes(immediateName)) {
        language = immediateName as LanguageDir;
        current = path.dirname(current);
    }

    // Walk up until we find `Week N` or hit the filesystem root.
    while (current && current !== path.dirname(current)) {
        const name = path.basename(current);
        const match = /^Week\s+(\d+)$/i.exec(name);
        if (match) {
            return {
                repoRoot: path.dirname(current),
                weekDir: current,
                weekNumber: parseInt(match[1], 10),
                language,
                topicStem,
            };
        }
        current = path.dirname(current);
    }
    return undefined;
}

/**
 * Returns the active editor's WeekContext or surfaces a VS Code error
 * with a hint about what's expected.
 */
function requireWeekContext(): WeekContext | undefined {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage(
            'DSA Journey: open a file inside a "Week N" directory first.'
        );
        return undefined;
    }
    const ctx = detectWeekContext(editor.document.uri.fsPath);
    if (!ctx) {
        vscode.window.showErrorMessage(
            'DSA Journey: could not detect a "Week N" parent for the active file.'
        );
        return undefined;
    }
    return ctx;
}

/**
 * Open a markdown file in a preview pane if it exists; warn otherwise.
 */
async function openMarkdown(absPath: string): Promise<void> {
    if (!fs.existsSync(absPath)) {
        vscode.window.showWarningMessage(`DSA Journey: ${absPath} not found.`);
        return;
    }
    const doc = await vscode.workspace.openTextDocument(absPath);
    await vscode.window.showTextDocument(doc, { preview: false });
}

/**
 * Run a shell command in the integrated terminal, rooted at the repo.
 */
function runInTerminal(name: string, command: string, cwd: string): void {
    const terminal = vscode.window.createTerminal({ name, cwd });
    terminal.show(true);
    terminal.sendText(command, true);
}

export function activate(context: vscode.ExtensionContext): void {
    // ---- openQuiz -------------------------------------------------------
    context.subscriptions.push(
        vscode.commands.registerCommand('dsa-journey.openQuiz', () => {
            const ctx = requireWeekContext();
            if (!ctx) {
                return;
            }
            runInTerminal(
                `DSA Quiz Week ${ctx.weekNumber}`,
                `./scripts/journey quiz ${ctx.weekNumber}`,
                ctx.repoRoot
            );
        })
    );

    // ---- openChallenges -------------------------------------------------
    context.subscriptions.push(
        vscode.commands.registerCommand('dsa-journey.openChallenges', async () => {
            const ctx = requireWeekContext();
            if (!ctx) {
                return;
            }
            await openMarkdown(path.join(ctx.weekDir, 'challenges.md'));
        })
    );

    // ---- openPatterns ---------------------------------------------------
    context.subscriptions.push(
        vscode.commands.registerCommand('dsa-journey.openPatterns', async () => {
            const ctx = requireWeekContext();
            if (!ctx) {
                return;
            }
            await openMarkdown(path.join(ctx.weekDir, 'patterns.md'));
        })
    );

    // ---- openTopicAcrossLanguages --------------------------------------
    context.subscriptions.push(
        vscode.commands.registerCommand(
            'dsa-journey.openTopicAcrossLanguages',
            async () => {
                const ctx = requireWeekContext();
                if (!ctx || !ctx.topicStem) {
                    vscode.window.showErrorMessage(
                        'DSA Journey: active file must be a topic file inside a language directory.'
                    );
                    return;
                }
                // Each language gets its own column (split pane). VS Code
                // accepts ViewColumn numbers up to ~9 in practice.
                let column = 1;
                for (const lang of LANGUAGE_DIRS) {
                    if (lang === ctx.language) {
                        column += 1;
                        continue;
                    }
                    const ext = LANGUAGE_EXTENSIONS[lang];
                    const candidate = path.join(
                        ctx.weekDir,
                        lang,
                        ctx.topicStem + ext
                    );
                    if (!fs.existsSync(candidate)) {
                        // The web track sometimes uses index.html-style names;
                        // try a couple of fallbacks before giving up silently.
                        const fallbacks = [
                            path.join(ctx.weekDir, lang, `${ctx.topicStem}.md`),
                            path.join(
                                ctx.weekDir,
                                lang,
                                ctx.topicStem,
                                `index${ext}`
                            ),
                        ];
                        const found = fallbacks.find((p) => fs.existsSync(p));
                        if (!found) {
                            continue;
                        }
                        const doc = await vscode.workspace.openTextDocument(found);
                        await vscode.window.showTextDocument(doc, {
                            viewColumn: column,
                            preview: false,
                        });
                    } else {
                        const doc = await vscode.workspace.openTextDocument(
                            candidate
                        );
                        await vscode.window.showTextDocument(doc, {
                            viewColumn: column,
                            preview: false,
                        });
                    }
                    column += 1;
                }
            }
        )
    );

    // ---- runTests -------------------------------------------------------
    context.subscriptions.push(
        vscode.commands.registerCommand('dsa-journey.runTests', () => {
            const editor = vscode.window.activeTextEditor;
            const startPath =
                editor?.document.uri.fsPath ??
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (!startPath) {
                vscode.window.showErrorMessage(
                    'DSA Journey: no workspace folder is open.'
                );
                return;
            }
            const ctx = detectWeekContext(startPath);
            const repoRoot =
                ctx?.repoRoot ??
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ??
                process.cwd();
            runInTerminal(
                'DSA Test Harness',
                'python tests/harness/harness.py --all',
                repoRoot
            );
        })
    );

    // ---- openIndex ------------------------------------------------------
    context.subscriptions.push(
        vscode.commands.registerCommand('dsa-journey.openIndex', async () => {
            const root =
                vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
            await openMarkdown(path.join(root, 'INDEX.md'));
        })
    );
}

export function deactivate(): void {
    // No persistent resources to release.
}
