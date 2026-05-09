# AGENTS.md — hacker-news-monitor

## Workflow Rules

- **Target OS**: Windows 11 (PowerShell). Never use Unix-only commands.
- **Language**: Python 3.11+
- **Execution**: GitHub Actions (cron every 4 hours + workflow_dispatch)
- **Validation**: Run `python -m py_compile src/main.py` after changes; run full workflow via `workflow_dispatch` to validate end-to-end
- **Commit Convention**: Conventional Commits (`feat:`, `fix:`, `chore:`, `docs:`)
- **Branch Strategy**: Direct push to `main` for initial development; feature branches once CI is active

## Context Loading Protocol

- At session start, always read `docs/CONTEXT-MAP.md` before exploring code.
- Use it as the primary navigation index. Load only files referenced there.
- Never load full directories or unrelated modules without explicit mapping.
- Load `docs/SCOPE.md` and `docs/PLAN.md` at session initialization for requirement baseline and phased task alignment.
- If combined file size exceeds 5KB, extract only the active phase, pending tasks, and requirement boundaries relevant to the current `docs/CHANGE-LOG.md` objective.
- Validate implementation output against `docs/PLAN.md` checkbox status before marking `- [x]`.
- Flag requirement deviations or scope drift in `docs/CHANGE-LOG.md` immediately; do not auto-modify upstream references.

## Architecture & Token Control

- If `graphify-out/GRAPH_REPORT.md` exists
  - Before reading source files, running grep, or generating code, read `graphify-out/GRAPH_REPORT.md`.
  - Extract only the target modules, god nodes, and cross-dependencies relevant to the task.
  - Retrieve files strictly by path listed in the report. Do not traverse directories recursively.
  - After code changes, execute `graphify update .` before committing.

## Token Budgets

- **Session Limit**: 300K tokens/session
- **Context Map**: Primary navigation index; always load first
- **Architecture Docs**: Load only sections relevant to current task
- **Source Code**: Load via CONTEXT-MAP references only; never bulk-read directories
- **Combined Memory Footprint**: Maintain <50KB across all memory files

## AI Directives

- Respond concisely. English or Traditional Chinese as requested.
- Preserve existing section headers, order, and markdown formatting in all docs.
- Surgical edits only — modify factually outdated or missing entries. Never rewrite prose.
- No source code dumps in docs — use relative paths, line ranges, or config keys.
- All doc entries must be concise bullet points. Zero paragraphs.
- Focus on architectural impact, validation status, and operational risk. Omit implementation trivia.
