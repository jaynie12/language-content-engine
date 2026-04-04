"""
Claude API service for French language analysis.
Handles CEFR level detection, vocabulary extraction, and topic tagging.
"""

import json
import logging
from typing import Optional, Dict, List
from anthropic import Anthropic
from config import settings

logger = logging.getLogger(__name__)

# Initialize Anthropic client
client = Anthropic()

# System prompt for CEFR analysis
CEFR_SYSTEM_PROMPT = """You are a French language expert specializing in CEFR (Common European Framework of Reference) level assessment.

Given a French transcript, determine its overall difficulty level and provide a confidence score.

Rules:
- CEFR levels: A1 (absolute beginner), A2 (elementary), B1 (intermediate), B2 (upper intermediate), C1 (advanced), C2 (mastery)
- Confidence: 0.0-1.0 (how sure you are of this level)
- Consider: vocabulary complexity, grammar structures, sentence length, idiomatic expressions
- Be conservative: if unclear between two levels, pick the higher one

Return ONLY valid JSON, no markdown or extra text."""

# System prompt for vocabulary extraction
VOCABULARY_SYSTEM_PROMPT = """You are a French language teacher extracting key vocabulary for learners.

Given a French transcript, extract exactly 20 key words that appear in the text and are most useful for a learner.

Rules:
- Must actually appear in the provided transcript
- Prioritize words that appear multiple times or are semantically important
- Include word frequency information based on the transcript
- CEFR level should be A1-C2 (be realistic based on word complexity)
- Example sentence must be from the actual transcript

For each word, return:
- word: French word exactly as it appears
- translation: English translation
- cefr_level: A1, A2, B1, B2, C1, or C2
- frequency: "very common" (appears 5+ times), "common" (2-4 times), "once" (appears once but important)
- example_sentence: Exact sentence from the transcript containing this word

Return ONLY valid JSON array, no markdown or extra text."""

# System prompt for topic extraction
TOPICS_SYSTEM_PROMPT = """You are an expert at extracting main topics from French texts.

Given a French transcript, identify 3-5 main topics or themes discussed.

Rules:
- Topics should be general (e.g., "cooking", "travel", "science") not specific details
- Base on content, not length
- Return as simple array of strings

Return ONLY valid JSON array of strings, no markdown or extra text."""


async def analyze_cefr_level(transcript: str) -> Dict[str, any]:
    """
    Analyze CEFR level of a French transcript.
    
    Returns:
        {
            'cefr_level': str (A1-C2),
            'confidence': float (0.0-1.0),
            'tokens_used': int
        }
    """
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            system=CEFR_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze this French transcript and determine CEFR level:\n\n{transcript[:8000]}"
                }
            ]
        )
        
        result_text = response.content[0].text.strip()
        result = json.loads(result_text)
        
        # Track tokens if enabled
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        if settings.log_cost_per_request:
            logger.info(f"CEFR analysis: {tokens_used} tokens")
        
        return {
            'cefr_level': result.get('cefr_level'),
            'confidence': result.get('confidence', 0.5),
            'tokens_used': tokens_used
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse CEFR response: {e}")
        raise
    except Exception as e:
        logger.error(f"Error analyzing CEFR level: {e}")
        raise


async def extract_vocabulary(transcript: str) -> Dict[str, any]:
    """
    Extract 20 key vocabulary words from transcript.
    
    Returns:
        {
            'vocabulary': List[VocabItem],
            'tokens_used': int
        }
    """
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=VOCABULARY_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Extract 20 key vocabulary words from this French transcript:\n\n{transcript[:12000]}"
                }
            ]
        )
        
        result_text = response.content[0].text.strip()
        vocabulary = json.loads(result_text)
        
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        if settings.log_cost_per_request:
            logger.info(f"Vocabulary extraction: {tokens_used} tokens")
        
        # Validate structure
        if not isinstance(vocabulary, list):
            vocabulary = [vocabulary]
        
        # Ensure exactly 20 items (or less if that's all that's available)
        vocabulary = vocabulary[:20]
        
        return {
            'vocabulary': vocabulary,
            'tokens_used': tokens_used
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse vocabulary response: {e}")
        raise
    except Exception as e:
        logger.error(f"Error extracting vocabulary: {e}")
        raise


async def extract_topics(transcript: str) -> Dict[str, any]:
    """
    Extract main topics from transcript.
    
    Returns:
        {
            'topics': List[str],
            'tokens_used': int
        }
    """
    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            system=TOPICS_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Extract main topics from this French transcript:\n\n{transcript[:6000]}"
                }
            ]
        )
        
        result_text = response.content[0].text.strip()
        topics = json.loads(result_text)
        
        tokens_used = response.usage.input_tokens + response.usage.output_tokens
        if settings.log_cost_per_request:
            logger.info(f"Topics extraction: {tokens_used} tokens")
        
        return {
            'topics': topics if isinstance(topics, list) else [topics],
            'tokens_used': tokens_used
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse topics response: {e}")
        raise
    except Exception as e:
        logger.error(f"Error extracting topics: {e}")
        raise


async def analyze_video(transcript: str, youtube_title: str = "Unknown") -> Dict[str, any]:
    """
    Full analysis pipeline: CEFR + vocabulary + topics.
    
    Returns all analysis results in one call.
    """
    try:
        logger.info(f"Starting full analysis for: {youtube_title}")
        
        # Run all three analyses (could be parallelized)
        cefr_result = await analyze_cefr_level(transcript)
        vocab_result = await extract_vocabulary(transcript)
        topics_result = await extract_topics(transcript)
        
        total_tokens = cefr_result['tokens_used'] + vocab_result['tokens_used'] + topics_result['tokens_used']
        
        logger.info(f"Analysis complete. Total tokens: {total_tokens}")
        
        return {
            'cefr_level': cefr_result['cefr_level'],
            'confidence': cefr_result['confidence'],
            'vocabulary': vocab_result['vocabulary'],
            'topics': topics_result['topics'],
            'total_tokens_used': total_tokens
        }
        
    except Exception as e:
        logger.error(f"Error in full analysis: {e}")
        raise
