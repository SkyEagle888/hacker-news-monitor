# Change Log — hacker-news-monitor

## Session Summaries

### 2026-06-18 | [Bug Fix — Suppress Empty-Body Notifications]

- **Files**:
  - `src/notifier.py` (added — `should_notify(post) -> bool` returns False when `post["summary"]` is missing, `None`, empty, or whitespace-only)
  - `src/main.py` (updated — imports `should_notify`; after `filter_posts`, drops posts with empty summary and logs `Suppressed %d post(s) with empty summary`; exit path unified for both no-match and all-suppressed cases)
  - `docs/CONTEXT-MAP.md` (updated — notifier + main rows reflect new helper and filter step)
  - `docs/CHANGE-LOG.md` (this entry)
- **Trigger**: observed Discord webhook delivery with title/url/color/footer present but blank description body when an RSS entry lacked `<description>`.
- **Behavior**:
  - Posts whose RSS summary is empty no longer generate Discord embeds.
  - `last_run.txt` still advances to `newest_published` when all matches are suppressed, preserving dedup against the upstream window.
  - Test notification unaffected (synthetic summary is non-empty).
- **Validation**: `py_compile src/main.py src/notifier.py` ✅
- **Risk**: Low | **Rollback**: revert `src/notifier.py` (drop `should_notify`) and `src/main.py` (drop filter block + import); behavior reverts to sending all matches.

### 2026-06-10 | [Feature — Manual Test Notification] 

- **Files**:
  - `.github/workflows/monitor.yml` (updated — `workflow_dispatch` now exposes `send_test` boolean input, default `false`; passed to run step as `SEND_TEST` env)
  - `src/main.py` (updated — new `_send_test_notification(webhook_urls)` helper; `main()` short-circuits when `SEND_TEST` is truthy (`true|1|yes`) to fan out a synthetic "Test Notification" embed to all configured channels and exit before RSS fetch)
  - `README.md` (updated — `Run Manually` section documents the new `send_test` input)
  - `docs/CONTEXT-MAP.md` (updated — main row reflects `SEND_TEST` short-circuit)
  - `docs/PLAN.md` (updated — Phase 6 test-notification task added and checked)
  - `docs/CHANGE-LOG.md` (this entry)
- **Behavior**:
  - Test embed uses the real `_build_embed()` path (same color/footer/fields as a real post); tier resolves to `General` (gray) since `"(test)"` is not a tiered keyword.
  - Per-channel retry/failure isolation inherited from `send_notification`; any channel failure exits 1.
  - No RSS fetch, no `last_run.txt` write — purely a webhook reachability check.
- **Validation**: `py_compile src/main.py` ✅; smoke test covers truthy variants + exit-on-partial-failure ✅
- **Risk**: Low | **Rollback**: revert `monitor.yml` and `src/main.py`; cron and back-compat behavior unchanged.

### 2026-06-10 | [Feature — Multi-Channel Discord Delivery]

- **Scope Drift**: SCOPE.md [05] updated from single-channel to one-or-more channels via `DISCORD_WEBHOOK_URLS` (JSON array) with `DISCORD_WEBHOOK_URL` legacy fallback.
- **Files**:
  - `src/notifier.py` (refactored — extracted `_post_to_webhook(url, post) -> bool`; `send_notification(urls: list[str], post) -> tuple[int, int]` fans out with per-URL 3-retry loop; URLs deduped preserving order)
  - `src/main.py` (updated — new `_load_webhook_urls()` helper: parses JSON, validates http(s) array, falls back to `DISCORD_WEBHOOK_URL` when URLS unset, dedupes, exits 1 on malformed/missing; final log line reports `(successes, total_attempts, channel_count)`)
  - `.github/workflows/monitor.yml` (updated — exposes both `DISCORD_WEBHOOK_URL` and `DISCORD_WEBHOOK_URLS` env vars to the `Run monitor` step)
  - `docs/SCOPE.md` (updated — [05] now specifies one-or-more channels and new secret precedence; scope drift flagged here)
  - `docs/ARCHITECTURE.md` (updated — topology diagram shows 1..N channels; secrets section lists both)
  - `docs/CONTEXT-MAP.md` (updated — notifier + main rows reflect multi-webhook contract)
  - `docs/PLAN.md` (updated — Phase 6 multi-webhook task added and marked complete)
  - `README.md` (updated — `How It Works` and `Setup` reflect new secret)
- **Failure isolation**: per-URL retry loop; one channel's 5xx/timeout does not block siblings.
- **Dedupe**: `list(dict.fromkeys(urls))` preserves order; prevents accidental duplicate embeds.
- **Validation**: `py_compile src/main.py src/notifier.py` ✅; `_load_webhook_urls` branch smoke-tests pass (JSON happy path, fallback to legacy, malformed JSON exits 1, non-array exits 1, non-http URL exits 1, dedupe works) ✅
- **Risk**: Low | **Rollback**: revert `src/notifier.py`, `src/main.py`, `.github/workflows/monitor.yml`, and doc lines; behavior reverts to single-webhook.

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
