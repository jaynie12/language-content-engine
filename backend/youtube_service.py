"""
YouTube transcript extraction service.
Handles fetching transcripts from YouTube URLs.
"""

import re
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)


def extract_youtube_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.
    
    Supports:
    - https://www.youtube.com/watch?v=dQw4w9WgXcQ
    - https://youtu.be/dQw4w9WgXcQ
    - dQw4w9WgXcQ
    """
    # Try common patterns
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([0-9A-Za-z_-]{11})',  # Full URLs
        r'^([0-9A-Za-z_-]{11})$',  # Just the ID
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError(f"Invalid YouTube URL: {url}")


def get_transcript(video_id: str) -> str:
    """
    Fetch transcript for a YouTube video.
    
    Returns the full transcript as a single string.
    Tries French first, falls back to English if available.
    """
    try:
        # Try to get French transcript first
        try:
           transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["fr"]).to_raw_data()
           logger.info(f"Fetched French transcript for {video_id}")
           logger.info(f"Transcript parts: {len(transcript_list)}")

        except Exception as e:
            logger.warning(f"French transcript not available, trying English: {e}")
            # Fall back to 
            transcript_list =YouTubeTranscriptApi().fetch(
            video_id, languages=["en"])
            logger.info(f"Fetched English transcript for {video_id}")
        
        # Combine all transcript parts into single string
        #transcript = ' '.join([item['text'] for item in transcript_list])
        #return transcript
        
    except Exception as e:
        logger.error(f"Failed to fetch transcript for {video_id}: {e}")
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
        return data.get('title')
    except Exception as e:
        logger.warning(f"Failed to fetch title for {video_id}: {e}")
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
        # Extract and validate ID
        video_id = extract_youtube_id(url)
        logger.info(f"Extracted YouTube ID: {video_id}")
        
        # Get transcript
        transcript = get_transcript(video_id)
        if not transcript or len(transcript) < 50:
            raise ValueError("Transcript is too short or empty")
        
        # Get title
        title = get_video_title(video_id)
        
        # Rough token estimate (1 token ≈ 4 chars)
        token_estimate = len(transcript) // 4
        
        logger.info(f"Successfully fetched transcript: {token_estimate} tokens (approx)")
        
        return {
            'youtube_id': video_id,
            'title': title or 'Unknown',
            'transcript': transcript,
            'token_count': token_estimate,
        }
        
    except Exception as e:
        logger.error(f"Error fetching transcript for {url}: {e}")
        raise

if __name__ == "__main__":
    # Simple test
    test_url = "https://www.youtube.com/watch?v=0E95x66B6cE"
    #result = asyncio.run(fetch_and_validate_transcript(test_url))
    result = get_transcript(extract_youtube_id(test_url))
    print(result)