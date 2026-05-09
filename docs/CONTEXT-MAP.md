# Context Map — hacker-news-monitor

## Module Mappings

| Path | Responsibility | Last Modified | Validation |
| --- | --- | --- | --- |
| `docs/SCOPE.md` | Requirements baseline; immutable source of truth | 2026-05-09 | ✅ |
| `docs/PLAN.md` | Implementation roadmap derived from SCOPE.md | 2026-05-09 | ✅ |
| `docs/ARCHITECTURE.md` | System topology, tech stack, deployment, data model | 2026-05-09 | ✅ |
| `docs/CONTEXT-MAP.md` | Primary navigation index for AI sessions (this file) | 2026-05-09 | ✅ |
| `docs/CHANGE-LOG.md` | Session summaries, diffs, risks, rollbacks | 2026-05-09 | ✅ |
| `docs/DB-SCHEMA.md` | Database definitions (N/A for this project) | 2026-05-09 | ✅ |
| `AGENTS.md` | Workflow rules, token budgets, AI directives | 2026-05-09 | ✅ |
| `README.md` | Project description and setup instructions | 2026-05-09 | ✅ |
| `src/__init__.py` | Package init | 2026-05-09 | ✅ |
| `src/main.py` | Entry point: orchestrate fetch → filter → notify | 2026-05-09 | ✅ |
| `src/rss_client.py` | RSS feed fetching and parsing via feedparser | 2026-05-09 | ✅ |
| `src/keyword_filter.py` | Keyword loading from CSV and case-insensitive matching | 2026-05-09 | ✅ |
| `src/notifier.py` | Discord webhook notification with retry logic | 2026-05-09 | ✅ |
| `keywords.csv` | Configurable keyword list (28 keywords) | 2026-05-09 | ✅ |
| `requirements.txt` | Python dependencies (feedparser, httpx, python-dateutil) | 2026-05-09 | ✅ |
| `.github/workflows/monitor.yml` | GitHub Actions workflow (cron + workflow_dispatch) | 2026-05-09 | ✅ |
| `.gitignore` | Excludes `__pycache__/`, `*.pyc`, `last_run.txt`, `last_run_artifact/` | 2026-05-09 | ✅ |

## File Responsibilities

- `src/main.py` — Loads last run timestamp, orchestrates RSS fetch → keyword filter → Discord notify, saves new timestamp
- `src/rss_client.py` — Fetches feed via `feedparser.parse()`, deduplicates by timestamp, returns list of post dicts
- `src/keyword_filter.py` — Reads `keywords.csv` via `csv.DictReader`, matches against title+summary (lowercased)
- `src/notifier.py` — Builds Discord embed payload, POSTs via `httpx` with 3 retries and 10s timeout
- `keywords.csv` — Single-column CSV with header `keyword`; edit to add/remove keywords
- `.github/workflows/monitor.yml` — Cron `0 */4 * * *`, `workflow_dispatch`, artifact-based timestamp persistence

## Validation Status

- **Phase**: Phase 6 in progress — `workflow_dispatch` validated ✅; cron/dedup pending natural validation
- **Compilation**: `py_compile` passed for all `.py` files ✅
- **Live Test**: `workflow_dispatch` run succeeded ✅ (commit `312939a`)
- **Blocking Issues**: None
- **Scope/Plan Alignment**: ✅ Phase 1–5 complete; Phase 6 task 1/5 checked
