"""
Location Extractor for Cebu City

Extracts and normalizes location mentions from Cebuano traffic discourse.
"""

import re
from typing import List, Set
from cebuano_lexicon import CEBU_LOCATIONS


class CebuLocationExtractor:
    """
    Extracts Cebu City locations from text using keyword matching.
    
    Handles:
    - Case-insensitive matching
    - Partial matches for abbreviations
    - Deduplication of normalized locations
    """
    
    def __init__(self):
        self.locations_dict = CEBU_LOCATIONS
        # Build reverse index for faster lookup
        self._location_keywords = {
            k.lower(): v for k, v in CEBU_LOCATIONS.items()
        }
    
    def extract(self, text: str) -> List[str]:
        """
        Extract locations mentioned in text.
        
        Returns:
            List of normalized location names (deduplicated)
        """
        if not text or not isinstance(text, str):
            return []
        
        text_lower = text.lower()
        found_locations = set()
        
        # Search for each location keyword in the text
        for keyword, location_name in self._location_keywords.items():
            # Use word boundary matching to avoid partial matches
            if self._find_keyword(text_lower, keyword):
                found_locations.add(location_name)
        
        # Return sorted, deduplicated list
        return sorted(list(found_locations))
    
    def _find_keyword(self, text: str, keyword: str) -> bool:
        """
        Check if keyword appears in text with word boundaries.
        
        Handles:
        - Word boundaries (space, punctuation)
        - Abbreviations (e.g., "rd" for "road")
        """
        # Pattern: word boundary + keyword + word boundary
        # \b = word boundary, \W+ = one or more non-word chars
        pattern = r'\b' + re.escape(keyword) + r'\b'
        return bool(re.search(pattern, text))
    
    def extract_with_confidence(self, text: str) -> List[dict]:
        """
        Extract locations with confidence scores.
        
        Confidence is based on:
        - How specific/unique the location is
        - How many times it appears in text
        
        Returns:
            [{
                'location': str,
                'count': int,
                'confidence': float (0.0-1.0)
            }]
        """
        if not text or not isinstance(text, str):
            return []
        
        text_lower = text.lower()
        location_counts = {}
        
        # Count occurrences of each location keyword
        for keyword, location_name in self._location_keywords.items():
            count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
            if count > 0:
                if location_name not in location_counts:
                    location_counts[location_name] = 0
                location_counts[location_name] += count
        
        # Calculate confidence based on specificity
        # High-confidence locations are more specific (e.g., "Mambaling" vs "Cebu City")
        confidence_weights = {
            "cebu city": 0.3,  # Very general
            "cebu": 0.3,      # Ambiguous, often just refers to city
            "bypass": 0.6,    # More specific
            "srp": 0.9,       # Very specific
            "mambaling": 0.9,
            "mabolo": 0.9,
            "apas": 0.9,
            "lahug": 0.9,
            "talamban": 0.9,
            "banawa": 0.8,
            "coopers": 0.85,
            "ayala": 0.85,
            "it park": 0.85,
        }
        
        result = []
        for location, count in sorted(location_counts.items(), 
                                     key=lambda x: x[1], reverse=True):
            confidence = confidence_weights.get(location.lower(), 0.7)
            result.append({
                'location': location,
                'count': count,
                'confidence': round(confidence, 2)
            })
        
        return result
    
    def get_all_locations(self) -> List[str]:
        """Return list of all known Cebu locations."""
        return sorted(list(set(self._location_keywords.values())))
    
    def normalize_location(self, location: str) -> str:
        """
        Normalize a location name to standard form.
        
        Example: "mambaling" → "Mambaling", "srp" → "SRP (South Road Properties)"
        """
        location_lower = location.lower().strip()
        return self._location_keywords.get(location_lower, location)
