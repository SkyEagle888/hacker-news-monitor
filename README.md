# Hacker News Monitor

Automated monitoring tool that tracks [The Hacker News RSS feed](https://feeds.feedburner.com/TheHackersNews) for new posts matching predefined cybersecurity keywords. Matches are forwarded as Discord notifications via webhook.

## How It Works

1. **GitHub Actions** triggers every 4 hours (cron) or on-demand (`workflow_dispatch`)
2. **Python script** fetches and parses the RSS feed
3. **Keyword filter** matches posts by title and summary against a configurable CSV list
4. **Discord notifier** sends an embed per matched post to a webhook channel
5. **Deduplication** ensures only posts published since the last successful run are processed

## Project Structure

```
.github/workflows/monitor.yml   # GitHub Actions workflow
src/
  main.py                       # Entry point — orchestration
  rss_client.py                 # RSS feed fetching and parsing
  keyword_filter.py             # CSV keyword loading and matching
  notifier.py                   # Discord webhook notification
keywords.csv                    # Configurable keyword list
requirements.txt                # Python dependencies
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/hacker-news-monitor.git
cd hacker-news-monitor
```

### 2. Add Discord Webhook Secret

Go to **Settings → Secrets and variables → Actions → New repository secret**:

- **Name**: `DISCORD_WEBHOOK_URL`
- **Value**: Your Discord channel webhook URL

### 3. Customize Keywords (Optional)

Edit `keywords.csv` to add or remove keywords. One keyword per row:

```csv
keyword
vulnerability
exploit
breach
...
```

### 4. Run Manually

Go to **Actions → Monitor Hacker News → Run workflow** to trigger an on-demand run.

## Default Keywords

| Category | Keywords |
| --- | --- |
| Threat Types | vulnerability, exploit, breach, leak, ransomware, malware, phishing, DDoS, zero-day, cyberattack |
| Infrastructure | Nginx, MySQL, Apache, WordPress, Magento, OpenSSL, Docker, Cloudflare |
| Vendors / Platforms | Microsoft, Apple, Google, Amazon Web Services (AWS), Microsoft Azure, Google Cloud Platform (GCP) |
| Workflow / Tools | n8n, OpenClaw, Hermes Agent |

## Tech Stack

- **Python 3.11+**
- **feedparser** — RSS/Atom feed parsing
- **httpx** — HTTP client for Discord webhooks
- **GitHub Actions** — Scheduling and execution

## License

MIT
