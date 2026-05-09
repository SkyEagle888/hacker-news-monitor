# Architecture — hacker-news-monitor

## System Topology

- **Platform**: GitHub Actions (GitHub-hosted `ubuntu-latest` runner)
- **Trigger**: Cron schedule (`0 */4 * * *`) + `workflow_dispatch`
- **Runtime**: Python 3.11+ (pre-installed on runner)
- **Data Flow**: RSS Feed → Parser → Keyword Filter → Discord Webhook

```
[The Hacker News RSS]
        │
        ▼
  [GitHub Actions Cron]
        │
        ▼
  [Python Script]
   ├─ fetch RSS feed
   ├─ filter by keywords (CSV)
   ├─ deduplicate (last run timestamp)
   └─ notify via Discord webhook
        │
        ▼
  [Discord Channel]
```

## Tech Stack & Dependencies

- **Language**: Python 3.11+
- **RSS Parsing**: `feedparser`
- **HTTP Client**: `httpx` (sync, with retry logic)
- **Date Parsing**: `python-dateutil` (fallback for non-standard RSS date formats)
- **Keyword Storage**: CSV file (built-in `csv` module)
- **State Persistence**: GitHub Actions artifact (last run timestamp)
- **Notification**: Discord Webhook via HTTP POST

## Deployment & Infra

- **CI/CD**: GitHub Actions workflow (`.github/workflows/monitor.yml`)
- **Secrets**: `DISCORD_WEBHOOK_URL` stored as GitHub Actions secret
- **Scheduling**: Cron `0 */4 * * *` (every 4 hours)
- **Artifacts**: Persist `last_run.txt` as workflow artifact (`last-run-timestamp`) for deduplication; 90-day retention
- **Ignored Paths**: `__pycache__/`, `*.pyc`, `last_run.txt`, `last_run_artifact/` (via `.gitignore`)

## Data Model & Schema

- **No database** — stateless execution model
- **RSS Entry Fields Consumed**: `title`, `link`, `summary`, `published` / `published_parsed`
- **Keyword CSV Format**: Single-column or multi-column CSV with keyword strings
- **Discord Payload**: JSON `{ embeds: [{ title, url, description, fields: [matched_keywords, published_date] }] }`
