from __future__ import annotations

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


def main() -> None:
    webhook_url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        logger.error("DISCORD_WEBHOOK_URL environment variable is not set")
        sys.exit(1)

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

    matched = filter_posts(posts, keywords)
    logger.info("Matched %d post(s)", len(matched))

    if not matched:
        logger.info("No matching posts found. Exiting.")
        save_last_run_timestamp(posts[0]["published"])
        return

    success_count = 0
    for post in matched:
        if send_notification(webhook_url, post):
            success_count += 1

    logger.info(
        "Sent %d/%d notification(s)", success_count, len(matched)
    )

    newest_published = max(p["published"] for p in matched)
    save_last_run_timestamp(newest_published)
    logger.info("Updated last run timestamp to: %s", newest_published)


if __name__ == "__main__":
    main()
