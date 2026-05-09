from __future__ import annotations

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_MAX_RETRIES = 3
DISCORD_WEBHOOK_TIMEOUT = 10


def _build_embed(post: dict[str, Any]) -> dict[str, Any]:
    matched_keywords = post.get("matched_keywords", [])
    keywords_str = ", ".join(matched_keywords)

    embed: dict[str, Any] = {
        "title": post.get("title", "Untitled"),
        "url": post.get("link", ""),
        "description": post.get("summary", "")[:500],
        "color": 16711680,
        "fields": [
            {
                "name": "Matched Keywords",
                "value": keywords_str or "N/A",
                "inline": False,
            },
            {
                "name": "Published",
                "value": post.get("published", "Unknown"),
                "inline": True,
            },
        ],
        "footer": {"text": "Hacker News Monitor"},
    }
    return embed


def send_notification(
    webhook_url: str,
    post: dict[str, Any],
) -> bool:
    embed = _build_embed(post)
    payload = {"embeds": [embed]}

    for attempt in range(1, DISCORD_WEBHOOK_MAX_RETRIES + 1):
        try:
            with httpx.Client(timeout=DISCORD_WEBHOOK_TIMEOUT) as client:
                response = client.post(webhook_url, json=payload)

            if response.status_code == 204:
                logger.info(
                    "Notification sent: %s", post.get("title", "Untitled")
                )
                return True

            logger.warning(
                "Webhook returned status %d (attempt %d/%d): %s",
                response.status_code,
                attempt,
                DISCORD_WEBHOOK_MAX_RETRIES,
                response.text,
            )
        except httpx.RequestError:
            logger.warning(
                "Request error (attempt %d/%d)",
                attempt,
                DISCORD_WEBHOOK_MAX_RETRIES,
                exc_info=True,
            )

    logger.error(
        "Failed to send notification after %d attempts: %s",
        DISCORD_WEBHOOK_MAX_RETRIES,
        post.get("title", "Untitled"),
    )
    return False
