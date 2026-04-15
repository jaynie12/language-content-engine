"""
YouTube transcript extraction service.
Handles fetching transcripts from YouTube URLs.
"""

import logging
import re
from typing import Any, Optional
import asyncio


import httpx
from youtube_transcript_api import YouTubeTranscriptApi

logger = logging.getLogger(__name__)


def extract_youtube_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.

    Supports:
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ
    - https://youtu.be/dQw4w9WgXcQ
    - dQw4w9WgXcQ
    """
    patterns = [
        r"(?:youtube\.com\/watch\?v=|youtu\.be\/)([0-9A-Za-z_-]{11})",
        r"^([0-9A-Za-z_-]{11})$",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError(f"Invalid YouTube URL: {url}")


def merge_raw_transcript_text(raw_data: list[dict[str, Any]]) -> str:
    """
    Merge transcript dicts from FetchedTranscript.to_raw_data() into one string.

    Only the "text" field is kept so the merged string is minimal for downstream AI use
    (no per-snippet start/duration metadata).
    """
    parts = [str(part.get("text", "")).strip() for part in raw_data]
    return " ".join(p for p in parts if p)


def get_transcript(video_id: str) -> str:
    """
    Fetch transcript for a YouTube video.

    Uses fetch().to_raw_data(), then merge_raw_transcript_text for a single string.
    Tries French first, falls back to English.
    """
    ytt = YouTubeTranscriptApi()
    try:
        try:
            raw = ytt.fetch(video_id, languages=["fr"]).to_raw_data()
            logger.info("Fetched French transcript for %s (%s snippets)", video_id, len(raw))
        except Exception as e:
            logger.warning("French transcript not available, trying English: %s", e)
            raw = ytt.fetch(video_id, languages=["en"]).to_raw_data()
            logger.info("Fetched English transcript for %s (%s snippets)", video_id, len(raw))

        text = merge_raw_transcript_text(raw)
        if not text:
            raise ValueError(f"No transcript text extracted for {video_id}")
        return text
    except Exception as e:
        logger.error("Failed to fetch transcript for %s: %s", video_id, e)
        raise


def get_video_title(video_id: str) -> Optional[str]:
    """
    Fetch video title from YouTube.
    Uses open API (no key needed for public videos).
    """
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = httpx.get(url, timeout=5.0)
        response.raise_for_status()
        data = response.json()
        return data.get("title")
    except Exception as e:
        logger.warning("Failed to fetch title for %s: %s", video_id, e)
        return None


async def fetch_and_validate_transcript(url: str) -> dict:
    """
    Full pipeline: validate URL, extract ID, fetch transcript, get title.

    Returns:
        {
            'youtube_id': str,
            'title': str or None,
            'transcript': str,
            'token_count': int (approximate)
        }
    """
    try:
        video_id = extract_youtube_id(url)
        logger.info("Extracted YouTube ID: %s", video_id)

        transcript = get_transcript(video_id)
        if not transcript or len(transcript) < 50:
            raise ValueError("Transcript is too short or empty")

        title = get_video_title(video_id)
        token_estimate = len(transcript) // 4

        logger.info("Successfully fetched transcript: ~%s tokens (approx)", token_estimate)

        return {
            "youtube_id": video_id,
            "title": title or "Unknown",
            "transcript": transcript,
            "token_count": token_estimate,
        }

    except Exception as e:
        logger.error("Error fetching transcript for %s: %s", url, e)
        raise


if __name__ == "__main__":
    test_url = "https://www.youtube.com/watch?v=0E95x66B6cE"
    result = asyncio.run(fetch_and_validate_transcript((test_url)))
    print(result)
