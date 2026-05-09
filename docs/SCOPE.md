# Hacker News Monitor — Project Scope

## Overview

**hacker-news-monitor** is an automated monitoring tool that runs on GitHub Actions to track The Hacker News RSS feed (<https://feeds.feedburner.com/TheHackersNews>) for new posts matching predefined keywords. When a match is found, a notification is sent to a designated Discord channel.

## Functional Requirements

### [01] Execution Platform

- The tool **must** run as a GitHub Actions workflow within this repository.

### [02] Schedule

- The workflow **must** execute every **4 hours** using a cron-based schedule (`0 */4 * * *`).
- The workflow **should** also support manual triggering via `workflow_dispatch` for testing and on-demand runs.

### [03] RSS Feed Retrieval

- The tool **must** fetch and parse the latest posts from The Hacker News RSS feed.
- Only posts published **since the last successful run** should be considered, to avoid duplicate notifications.

### [04] Keyword Filtering

- The tool **must** filter retrieved posts against a configurable keyword list stored in a CSV file.
- A post matches if its **title** or **summary/content** contains **any** of the keywords (case-insensitive).
- The keyword CSV file **should** support easy additions and removals without code changes.

#### Default Keywords

| Category | Keywords |
| --- | --- |
| Threat Types | `vulnerability`, `exploit`, `breach`, `leak`, `ransomware`, `malware`, `phishing`, `DDoS`, `zero-day`, `cyberattack` |
| Infrastructure | `Nginx`, `MySQL`, `Apache`, `WordPress`, `Magento`, `OpenSSL`, `Docker`, `Cloudflare` |
| Vendors / Platforms | `Microsoft`, `Apple`, `Google`, `Amazon Web Services (AWS)`, `Microsoft Azure`, `Google Cloud Platform (GCP)` |
| Workflow / Tools | `n8n`, `OpenClaw`, `Hermes Agent` |

### [05] Discord Notification

- When one or more posts match the keyword filter, the tool **must** send a notification to a Discord channel via a **Discord Webhook URL**.
- The webhook URL **must** be stored as a GitHub Actions secret (e.g. `DISCORD_WEBHOOK_URL`) — never hard-coded.
- Each notification **should** include:
  - Post title
  - Post URL/link
  - Matched keyword(s)
  - Publication date

## Non-Functional Requirements

- **Language/Runtime**: **Python 3.11+** — pre-installed on GitHub-hosted runners; ideal for this fetch-filter-notify pattern.
- **Dependencies**: Keep external dependencies minimal. Use `feedparser` for RSS parsing and `httpx` (or `urllib`) for HTTP requests. Use the built-in `csv` module for keyword loading.
- **Logging**: The workflow **should** log the number of posts fetched, matched, and notifications sent for observability.
- **Error Handling**: The tool **must** handle RSS feed failures (network errors, malformed XML) gracefully and not crash silently.

## Out of Scope

- Monitoring feeds other than The Hacker News RSS feed.
- Sending notifications to platforms other than Discord.
- Storing or persisting matched posts to a database.
