from __future__ import annotations

import json
import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

DISCORD_WEBHOOK_MAX_RETRIES = 3
DISCORD_WEBHOOK_TIMEOUT = 10
DISCORD_DESCRIPTION_MAX_WORDS = 60
TRUNCATION_ELLIPSIS = "…"

TIER_CRITICAL = "Critical"
TIER_HIGH = "High"
TIER_STACK = "Stack"
TIER_VENDOR = "Vendor"
TIER_INTERNAL = "Internal"
TIER_DEFAULT = "General"

TIER_COLORS: dict[str, int] = {
    TIER_CRITICAL: 15158332,
    TIER_HIGH: 15105570,
    TIER_STACK: 15844367,
    TIER_VENDOR: 3447003,
    TIER_INTERNAL: 10181046,
    TIER_DEFAULT: 9807270,
}

TIER_PRIORITY: list[str] = [
    TIER_CRITICAL,
    TIER_HIGH,
    TIER_STACK,
    TIER_VENDOR,
    TIER_INTERNAL,
]

KEYWORD_TIERS: dict[str, str] = {
    "zero-day": TIER_CRITICAL,
    "exploit": TIER_CRITICAL,
    "breach": TIER_CRITICAL,
    "cyberattack": TIER_CRITICAL,
    "malware": TIER_CRITICAL,
    "vulnerability": TIER_HIGH,
    "leak": TIER_HIGH,
    "phishing": TIER_HIGH,
    "ddos": TIER_HIGH,
    "nginx": TIER_STACK,
    "mysql": TIER_STACK,
    "apache": TIER_STACK,
    "wordpress": TIER_STACK,
    "magento": TIER_STACK,
    "openssl": TIER_STACK,
    "docker": TIER_STACK,
    "microsoft": TIER_VENDOR,
    "apple": TIER_VENDOR,
    "google": TIER_VENDOR,
    "amazon web services (aws)": TIER_VENDOR,
    "microsoft azure": TIER_VENDOR,
    "google cloud platform (gcp)": TIER_VENDOR,
    "cloudflare": TIER_VENDOR,
    "n8n": TIER_INTERNAL,
    "openclaw": TIER_INTERNAL,
    "hermes agent": TIER_INTERNAL,
}


def _truncate_words(text: str, max_words: int) -> str:
    if not text:
        return ""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]) + TRUNCATION_ELLIPSIS


def _resolve_tier(matched_keywords: list[str]) -> str:
    tiers = {
        KEYWORD_TIERS[k.lower()]
        for k in matched_keywords
        if k.lower() in KEYWORD_TIERS
    }
    for tier in TIER_PRIORITY:
        if tier in tiers:
            return tier
    return TIER_DEFAULT


def _build_embed(post: dict[str, Any]) -> dict[str, Any]:
    matched_keywords = post.get("matched_keywords", [])
    keywords_str = ", ".join(matched_keywords)
    tier = _resolve_tier(matched_keywords)
    color = TIER_COLORS[tier]

    embed: dict[str, Any] = {
        "title": post.get("title", "Untitled"),
        "url": post.get("link", ""),
        "description": _truncate_words(
            post.get("summary", ""), DISCORD_DESCRIPTION_MAX_WORDS
        ),
        "color": color,
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
        "footer": {"text": f"Hacker News Monitor • {tier}"},
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
