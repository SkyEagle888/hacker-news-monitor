from __future__ import annotations

import csv
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

KEYWORDS_FILE = os.path.join(os.path.dirname(__file__), "..", "keywords.csv")


def load_keywords(filepath: str = KEYWORDS_FILE) -> list[str]:
    keywords: list[str] = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row.get("keyword", "").strip()
                if keyword:
                    keywords.append(keyword)
    except FileNotFoundError:
        logger.error("Keywords file not found: %s", filepath)
        return []
    except Exception:
        logger.exception("Failed to read keywords file: %s", filepath)
        return []

    if not keywords:
        logger.warning("No keywords loaded from %s", filepath)

    return keywords


def filter_posts(
    posts: list[dict[str, Any]],
    keywords: list[str],
) -> list[dict[str, Any]]:
    if not keywords:
        return []

    keywords_lower = [k.lower() for k in keywords]
    matched: list[dict[str, Any]] = []

    for post in posts:
        title = post.get("title", "").lower()
        summary = post.get("summary", "").lower()
        searchable = f"{title} {summary}"

        post_keywords: list[str] = [
            keywords[i]
            for i, kw in enumerate(keywords_lower)
            if kw in searchable
        ]

        if post_keywords:
            matched.append({**post, "matched_keywords": post_keywords})

    return matched
