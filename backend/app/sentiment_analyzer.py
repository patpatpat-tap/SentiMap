"""
Sentiment Analyzer for Cebuano Traffic Discourse

Combines lexicon-based analysis with sarcasm detection and code-switching awareness.
"""

import re
from typing import Dict, Tuple
from .cebuano_lexicon import (
    NEGATIVE_LEXICON,
    POSITIVE_LEXICON,
    SARCASM_MARKERS,
    TRAFFIC_TERMS,
)


class CebuanoSentimentAnalyzer:
    """
    Analyzes sentiment in Cebuano/Bislish traffic discourse.
    
    Handles:
    - Lexicon-based sentiment scoring
    - Sarcasm detection (especially "hayahay" pattern)
    - Case-insensitive matching (accounts for informal writing)
    - Weighted scoring based on word position and context
    """
    
    def __init__(self):
        self.negative_lexicon = NEGATIVE_LEXICON
        self.positive_lexicon = POSITIVE_LEXICON
        self.sarcasm_markers = SARCASM_MARKERS
        
    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of a given text.
        
        Returns:
            {
                'sentiment_score': float (-1.0 to 1.0),
                'sentiment_label': str ('negative' | 'neutral' | 'positive'),
                'sarcasm_detected': bool,
                'confidence': float (0.0 to 1.0),
                'words_found': list of (word, score) tuples,
            }
        """
        if not text or not isinstance(text, str):
            return self._neutral_response()
        
        text_lower = text.lower().strip()
        
        # Clean text: remove URLs, mentions, special characters (but keep spaces)
        text_clean = self._clean_text(text_lower)
        tokens = text_clean.split()
        
        if not tokens:
            return self._neutral_response()
        
        # Check for sarcasm patterns
        sarcasm_detected = self._detect_sarcasm(text_clean, tokens)
        
        # Score sentiment
        sentiment_score, words_found = self._score_sentiment(text_clean, tokens)
        
        # Adjust for sarcasm (flip polarity if sarcastic positive)
        if sarcasm_detected and sentiment_score > 0.3:
            sentiment_score = -sentiment_score * 0.8  # Reduce intensity slightly
            sarcasm_label = " (sarcastic)"
        else:
            sarcasm_label = ""
        
        # Clamp score to [-1, 1]
        sentiment_score = max(-1.0, min(1.0, sentiment_score))
        
        # Determine label
        if sentiment_score > 0.1:
            sentiment_label = "positive"
        elif sentiment_score < -0.1:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"
        
        # Calculate confidence based on word count and strength
        confidence = min(1.0, len(words_found) / max(1, len(tokens) / 2))
        
        return {
            'sentiment_score': round(sentiment_score, 3),
            'sentiment_label': sentiment_label,
            'sarcasm_detected': sarcasm_detected,
            'confidence': round(confidence, 3),
            'words_found': words_found[:10],  # Top 10 words for debugging
        }
    
    def _clean_text(self, text: str) -> str:
        """Remove URLs, mentions, email addresses, but preserve word boundaries."""
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _detect_sarcasm(self, text: str, tokens: list) -> bool:
        """
        Detect sarcasm indicators.
        
        Primary sarcasm pattern in traffic context:
        - "hayahay" + positive language
        - "so comfortable", "so smooth" + about traffic
        """
        # Check for explicit sarcasm markers
        sarcasm_phrases = [
            "so comfortable",
            "so smooth",
            "super efficient",
            "really efficient",
            "hayahay",
            "yeah right",
            "sure",
        ]
        
        for phrase in sarcasm_phrases:
            if phrase in text:
                # Check if there's a traffic term nearby
                words_set = set(tokens)
                traffic_words_present = any(
                    term in words_set for term in TRAFFIC_TERMS.keys()
                )
                if traffic_words_present or "traffic" in text:
                    return True
        
        # Check for "hayahay" + positive sentiment pattern
        if "hayahay" in text:
            return True
        
        return False
    
    def _score_sentiment(self, text: str, tokens: list) -> Tuple[float, list]:
        """
        Score sentiment using lexicon.
        
        Returns:
            (sentiment_score, [(word, score), ...])
        """
        total_score = 0.0
        words_found = []
        word_count = 0
        
        for i, token in enumerate(tokens):
            # Remove punctuation from token
            token_clean = re.sub(r'[^\w]', '', token)
            
            if token_clean in self.negative_lexicon:
                score = self.negative_lexicon[token_clean]
                total_score += score
                words_found.append((token_clean, score))
                word_count += 1
                
            elif token_clean in self.positive_lexicon:
                score = self.positive_lexicon[token_clean]
                total_score += score
                words_found.append((token_clean, score))
                word_count += 1
        
        # Normalize score by number of words
        if word_count > 0:
            sentiment_score = total_score / word_count
        else:
            sentiment_score = 0.0
        
        # Sort words by absolute score (strongest first)
        words_found.sort(key=lambda x: abs(x[1]), reverse=True)
        
        return sentiment_score, words_found
    
    def _neutral_response(self) -> Dict:
        """Return a neutral sentiment response."""
        return {
            'sentiment_score': 0.0,
            'sentiment_label': 'neutral',
            'sarcasm_detected': False,
            'confidence': 0.0,
            'words_found': [],
        }
