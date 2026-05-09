from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

import feedparser
from dateutil import parser as dateutil_parser

logger = logging.getLogger(__name__)

FEED_URL = "https://feeds.feedburner.com/TheHackersNews"


@dataclass
class Post:
    title: str
    link: str
    summary: str
    published: str

    def to_dict(self) -> dict[str, str]:
        return {
            "title": self.title,
            "link": self.link,
            "summary": self.summary,
            "published": self.published,
        }


def _parse_published(entry: Any) -> str:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        import time

        return time.strftime("%Y-%m-%dT%H:%M:%SZ", entry.published_parsed)
    if hasattr(entry, "published") and entry.published:
        try:
            return dateutil_parser.parse(entry.published).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        except (ValueError, TypeError):
            return ""
    return ""


def fetch_feed(last_run_timestamp: str = "") -> list[dict[str, str]]:
    try:
        feed = feedparser.parse(FEED_URL)
    except Exception:
        logger.exception("Failed to fetch RSS feed from %s", FEED_URL)
        return []

    if feed.bozo and not feed.entries:
        logger.error("Malformed RSS feed: %s", feed.bozo_exception)
        return []

    posts: list[dict[str, str]] = []
    for entry in feed.entries:
        published = _parse_published(entry)
        if last_run_timestamp and published <= last_run_timestamp:
            continue

        posts.append(
            {
                "title": getattr(entry, "title", ""),
                "link": getattr(entry, "link", ""),
                "summary": getattr(entry, "summary", ""),
                "published": published,
            }
        )

    logger.info(
        "Parsed %d total entries, %d newer than last run",
        len(feed.entries),
        len(posts),
    )
    return posts
