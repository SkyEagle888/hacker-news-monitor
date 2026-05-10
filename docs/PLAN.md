# Implementation Plan — hacker-news-monitor

> Derived from `docs/SCOPE.md`. All tasks trace to functional requirements [01]–[05].

## Phase 1: Project Skeleton

- [x] Initialize Python project structure (`src/`, `requirements.txt`)
- [x] Create `keywords.csv` with default keyword list per SCOPE.md §[04]
- [x] Create `.github/workflows/monitor.yml` with cron schedule (`0 */4 * * *`) and `workflow_dispatch` trigger → **[01]** **[02]**

## Phase 2: RSS Feed Client

- [x] Implement `src/rss_client.py` — fetch and parse The Hacker News RSS feed → **[03]**
- [x] Extract `title`, `link`, `summary`, `published` fields from each entry
- [x] Implement deduplication: compare entry `published` against last run timestamp artifact → **[03]**
- [x] Handle network errors and malformed XML gracefully → Non-Functional

## Phase 3: Keyword Filter

- [x] Implement `src/keyword_filter.py` — load keywords from `keywords.csv` → **[04]**
- [x] Match keywords against post title + description (case-insensitive) → **[04]**
- [x] Return matched posts with their matched keywords attached → **[04]**

## Phase 4: Discord Notifier

- [x] Implement `src/notifier.py` — send Discord webhook notification → **[05]**
- [x] Read webhook URL from `DISCORD_WEBHOOK_URL` environment variable → **[05]**
- [x] Format embed payload: title, URL, matched keywords, publication date → **[05]**
- [x] Handle webhook failures gracefully (retry or log) → Non-Functional

## Phase 5: Orchestration & Integration

- [x] Implement `src/main.py` — wire RSS client → filter → notifier
- [x] Log number of posts fetched, matched, and notifications sent → Non-Functional
- [x] Save current run timestamp as GitHub Actions artifact for next run deduplication → **[03]**

## Phase 6: Validation & Hardening

- [x] Test full workflow via `workflow_dispatch` trigger
- [ ] Verify Discord notification format and content
- [ ] Verify deduplication works across consecutive runs
- [ ] Confirm cron schedule fires correctly
- [ ] Final `docs/` review — mark all PLAN tasks as `[x]`
