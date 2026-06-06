# Change Log — hacker-news-monitor

## Session Summaries

### 2026-06-06 | [Feature — Severity-Based Embed Colors]

- **Files**:
  - `src/notifier.py` (updated — added 5-tier keyword→color mapping; embed `color` and `footer` now derived from highest-priority matched tier)
  - `docs/CONTEXT-MAP.md` (updated — notifier responsibility refreshed)
  - `docs/CHANGE-LOG.md` (this entry)
- **Tiers**: Critical (red) > High (orange) > Stack (yellow) > Vendor (blue) > Internal (purple) > General (gray fallback)
- **Validation**: `py_compile src/notifier.py` ✅ | Tier resolver smoke-tested across 6 keyword combos ✅
- **Risk**: Low | **Rollback**: Revert `src/notifier.py` to single-color embed

### 2026-05-09 | [Docs Sync — Post-Live Validation]

- **Routed To**:
  - `docs/CONTEXT-MAP.md` (added `.gitignore` mapping; updated validation status)
  - `docs/ARCHITECTURE.md` (added `python-dateutil` dep; added `.gitignore` + artifact details)
  - `docs/CHANGE-LOG.md` (this entry)
- **Validation**: `workflow_dispatch` confirmed working ✅
- **Risk**: Low

### 2026-05-09 | [Bug Fixes & Live Validation]

- **Files**:
  - `.github/workflows/monitor.yml` (fixed — missing colon on `if: always()` at L50)
  - `src/main.py` (fixed — absolute imports `from src.xxx` for `python -m src.main`)
  - `.gitignore` (added — `__pycache__/`, `*.pyc`, `last_run.txt`, `last_run_artifact/`)
  - `docs/PLAN.md` (updated — Phase 6 first task marked [x])
- **Validation**: `workflow_dispatch` run succeeded ✅
- **Risk**: Low | **Rollback**: Revert commits `98e7292`, `312939a`

### 2026-05-09 | [Full Implementation — Phases 1–5]

- **Files**:
  - `README.md` (rewritten — project overview, setup, structure, keywords)
  - `requirements.txt` (created — feedparser, httpx, python-dateutil)
  - `keywords.csv` (created — 28 keywords across 4 categories)
  - `src/__init__.py` (created — package init)
  - `src/main.py` (created — entry point, orchestration, timestamp management)
  - `src/rss_client.py` (created — RSS fetch/parse, timestamp deduplication)
  - `src/keyword_filter.py` (created — CSV keyword loader, case-insensitive matcher)
  - `src/notifier.py` (created — Discord webhook with embed payload, 3 retries)
  - `.github/workflows/monitor.yml` (created — cron + workflow_dispatch, artifact persistence)
  - `docs/PLAN.md` (updated — Phase 1–5 tasks marked [x])
  - `docs/CONTEXT-MAP.md` (updated — all implemented files mapped)
- **Validation**: `py_compile` all .py files ✅ | Scope/Plan alignment ✅
- **Risk**: Low | **Rollback**: Revert all source files; keep docs/

### 2026-05-09 | [Initialization & Scope Definition]

- **Files**:
  - `docs/SCOPE.md` (created — requirements baseline)
  - `docs/SCOPE.md` (polished — fixed typos, restructured, added technical details)
  - `docs/SCOPE.md` (updated — locked Python 3.11+ as runtime)
  - `AGENTS.md` (created — workflow rules, context loading, token budgets, AI directives)
  - `docs/ARCHITECTURE.md` (created — system topology, tech stack, deployment, data model)
  - `docs/CONTEXT-MAP.md` (created — module mappings, file responsibilities)
  - `docs/CHANGE-LOG.md` (created — this file)
  - `docs/DB-SCHEMA.md` (created — no database for this project)
  - `docs/PLAN.md` (created — phased implementation roadmap)
- **Decisions**:
  - Python 3.11+ selected over Node.js (better fit for GitHub Actions + RSS parsing)
  - No AI/LLM integration needed (keyword matching is sufficient)
  - Filter scope: RSS title + description only (no full URL scraping)
  - No database (stateless execution with artifact-based deduplication)
- **Validation**: docs/ structure ✅ | Scope defined ✅ | Plan aligned ✅
- **Risk**: Low | **Rollback**: Delete all docs/* files except SCOPE.md
