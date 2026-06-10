from __future__ import annotations

import json
import logging
import os
import sys

from src.rss_client import fetch_feed
from src.keyword_filter import load_keywords, filter_posts
from src.notifier import send_notification

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

LAST_RUN_FILE = os.path.join(os.path.dirname(__file__), "..", "last_run.txt")


def load_last_run_timestamp() -> str:
    if not os.path.exists(LAST_RUN_FILE):
        return ""
    with open(LAST_RUN_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def save_last_run_timestamp(timestamp: str) -> None:
    with open(LAST_RUN_FILE, "w", encoding="utf-8") as f:
        f.write(timestamp)


def _load_webhook_urls() -> list[str]:
    urls_json = os.environ.get("DISCORD_WEBHOOK_URLS")
    if urls_json:
        try:
            parsed = json.loads(urls_json)
        except json.JSONDecodeError:
            logger.error("DISCORD_WEBHOOK_URLS is not valid JSON")
            sys.exit(1)
        if not isinstance(parsed, list) or not all(
            isinstance(u, str)
            and u.strip()
            and u.startswith(("http://", "https://"))
            for u in parsed
        ):
            logger.error(
                "DISCORD_WEBHOOK_URLS must be a JSON array of http(s) URLs"
            )
            sys.exit(1)
        deduped = list(dict.fromkeys(u.strip() for u in parsed))
        logger.info(
            "Using DISCORD_WEBHOOK_URLS (%d channel(s))", len(deduped)
        )
        return deduped

    legacy = os.environ.get("DISCORD_WEBHOOK_URL")
    if legacy and legacy.strip():
        logger.info("Falling back to DISCORD_WEBHOOK_URL (1 channel)")
        return [legacy.strip()]

    logger.error(
        "DISCORD_WEBHOOK_URLS or DISCORD_WEBHOOK_URL environment variable "
        "is not set"
    )
    sys.exit(1)


def main() -> None:
    webhook_urls = _load_webhook_urls()

    last_run = load_last_run_timestamp()
    logger.info("Last run timestamp: %s", last_run or "(none)")

    logger.info("Fetching RSS feed...")
    posts = fetch_feed(last_run)
    logger.info("Fetched %d new post(s) since last run", len(posts))

    if not posts:
        logger.info("No new posts found. Exiting.")
        return

    keywords = load_keywords()
    logger.info("Loaded %d keyword(s)", len(keywords))

    newest_published = max(p["published"] for p in posts)

    matched = filter_posts(posts, keywords)
    logger.info("Matched %d post(s)", len(matched))

    if not matched:
        logger.info("No matching posts found. Exiting.")
        save_last_run_timestamp(newest_published)
        logger.info("Updated last run timestamp to: %s", newest_published)
        return

    success_count = 0
    total_attempts = 0
    for post in matched:
        ok, attempts = send_notification(webhook_urls, post)
        success_count += ok
        total_attempts += attempts

    logger.info(
        "Sent %d/%d notification(s) across %d channel(s)",
        success_count,
        total_attempts,
        len(webhook_urls),
    )

    save_last_run_timestamp(newest_published)
    logger.info("Updated last run timestamp to: %s", newest_published)


if __name__ == "__main__":
    main()
