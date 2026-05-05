"""
SentiMap Sentiment Analyzer v3.0 — Final
=============================================
Analyzes sentiment in Cebuano/Bislish traffic discourse.

v3.0 improvements:
- Fully synced with Cebuano Sentiment Lexicon v3.0
- 5-Layer Sarcasm Detection System (incorporating BRT-specific resignation)
- Structural irony redundancy removed (promoted to primary lexicon)
- Expanded emoji context triggers (BRT, CCTO)
- Phrase-first matching with \b word boundaries
- Improved score normalization (evidence accumulation, not averaging)
- Exports debug info for research documentation
"""

import re
from typing import Dict, List, Tuple
try:
    from cebuano_lexicon import (
        NEGATIVE_LEXICON,
        POSITIVE_LEXICON,
        SARCASM_MARKERS,
        CONTEXT_DEPENDENT_SARCASM,
        INTENSIFIERS,
        NEGATIONS,
        TRAFFIC_TERMS,
    )
except ImportError:
    from .cebuano_lexicon import (
        NEGATIVE_LEXICON,
        POSITIVE_LEXICON,
        SARCASM_MARKERS,
        CONTEXT_DEPENDENT_SARCASM,
        INTENSIFIERS,
        NEGATIONS,
        TRAFFIC_TERMS,
    )


class CebuanoSentimentAnalyzer:
    """
    Analyzes sentiment in Cebuano/Bislish traffic discourse.

    Handles:
    - Phrase-first lexicon matching (multi-word entries)
    - Intensifier multiplication (kaayo, gyud, sobra)
    - Negation flipping (dili, hindi, wala)
    - Sarcasm detection (35+ Cebuano/Filipino patterns)
    - Context-dependent sarcasm (wow/nice/perfect in traffic context)
    - Emoji sentiment signals
    - Code-switching (Cebuano + English + Tagalog)
    """

    # Emoji sentiment map — common in Filipino social media
    EMOJI_SENTIMENT = {
        "😡": -0.9, "🤬": -0.9, "😤": -0.8, "😠": -0.8,
        "😒": -0.7, "🙄": -0.6, "😑": -0.5, "😔": -0.6,
        "😢": -0.7, "😭": -0.7, "😩": -0.8, "😫": -0.8,
        "🤦": -0.7, "🤦‍♂️": -0.7, "🤦‍♀️": -0.7,
        "💀": -0.6,  # "I'm dead" from frustration
        "😂": 0.3,   # Positive but ALSO sarcasm signal — handled separately
        "😂😭": -0.4, # Laugh-cry = sarcastic resignation (negative net)
        "😅": -0.3,  # Nervous laugh — mild negative
        "🙏": 0.5,   # Grateful/hopeful
        "👍": 0.7,   # Positive
        "❤️": 0.8,   # Love/positive
        "✅": 0.6,   # Good/approved
        "❌": -0.7,  # Bad/rejected
        "⚠️": -0.4,  # Warning
    }

    def __init__(self):
        self.negative_lexicon = NEGATIVE_LEXICON
        self.positive_lexicon = POSITIVE_LEXICON
        self.sarcasm_markers  = SARCASM_MARKERS
        self.context_sarcasm  = CONTEXT_DEPENDENT_SARCASM
        self.intensifiers     = INTENSIFIERS
        self.negations        = NEGATIONS

        # Pre-sort multi-word phrases longest first
        # Critical: match "grabe kaayo" before "grabe"
        self.neg_phrases = sorted(
            self.negative_lexicon.keys(),
            key=len, reverse=True
        )
        self.pos_phrases = sorted(
            self.positive_lexicon.keys(),
            key=len, reverse=True
        )
        self.intensifier_phrases = sorted(
            self.intensifiers.keys(),
            key=len, reverse=True
        )
        self.negation_phrases = sorted(
            self.negations.keys(),
            key=len, reverse=True
        )
        self.sarcasm_phrases = sorted(
            [k for k, v in self.sarcasm_markers.items() if v is True],
            key=len, reverse=True
        )

    def analyze(self, text: str) -> Dict:
        """
        Analyze sentiment of a given text.

        Returns:
            {
                'sentiment_score':      float (-1.0 to 1.0),
                'sentiment_label':      str ('negative'|'neutral'|'positive'),
                'sarcasm_detected':     bool,
                'confidence':           float (0.0 to 1.0),
                'words_found':          list of (word, score) tuples,
                'sarcasm_triggers':     list of matched sarcasm patterns,
                'intensifiers_applied': list of applied intensifiers,
                'negations_applied':    list of applied negations,
            }
        """
        if not text or not isinstance(text, str):
            return self._neutral_response()

        # Preserve original for emoji detection
        text_original = text.strip()
        text_lower    = text_original.lower()
        text_clean    = self._clean_text(text_lower)

        if not text_clean.strip():
            return self._neutral_response()

        # ── STEP 1: Sarcasm detection (before sentiment scoring) ──
        sarcasm_detected, sarcasm_triggers = self._detect_sarcasm(
            text_clean, text_original
        )

        # ── STEP 2: Emoji sentiment ───────────────────────────────
        emoji_score, emoji_hits = self._score_emojis(text_original)

        # ── STEP 3: Phrase-aware sentiment scoring ────────────────
        (raw_score,
         words_found,
         intensifiers_applied,
         negations_applied) = self._score_sentiment_phrases(text_clean)

        # ── STEP 4: Combine scores ────────────────────────────────
        # Emoji score adds to raw score (not averaged — it's additive evidence)
        combined_score = raw_score + (emoji_score * 0.3)  # emoji weighted at 30%

        # ── STEP 5: Apply sarcasm polarity flip ──────────────────
        if sarcasm_detected:
            if combined_score > 0.15:
                # Positive text that's sarcastic → flip to negative
                combined_score = -abs(combined_score) * 0.85
            elif combined_score >= -0.1:
                # Neutral text with sarcasm → mildly negative
                combined_score = -0.4

        # ── STEP 6: Clamp and label ───────────────────────────────
        sentiment_score = max(-1.0, min(1.0, combined_score))

        if sentiment_score > 0.15:
            sentiment_label = "positive"
        elif sentiment_score < -0.15:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        # ── STEP 7: Confidence calculation ───────────────────────
        # Based on: number of matched words, sarcasm certainty, emoji presence
        evidence_count = len(words_found) + len(sarcasm_triggers) + len(emoji_hits)
        confidence = min(1.0, evidence_count * 0.15)
        if sarcasm_detected:
            confidence = min(1.0, confidence + 0.2)

        return {
            "sentiment_score":      round(sentiment_score, 4),
            "sentiment_label":      sentiment_label,
            "sarcasm_detected":     sarcasm_detected,
            "confidence":           round(confidence, 4),
            "words_found":          words_found[:10],
            "sarcasm_triggers":     sarcasm_triggers,
            "intensifiers_applied": intensifiers_applied,
            "negations_applied":    negations_applied,
        }

    # ─────────────────────────────────────────────────────────────
    # SARCASM DETECTION
    # ─────────────────────────────────────────────────────────────
    def _detect_sarcasm(self, text_clean: str,
                        text_original: str) -> Tuple[bool, List[str]]:
        """
        Multi-layer sarcasm detection (5-Layer System).

        Layer 1: Primary Cebuano/Filipino markers & Ironic praise & Resignation & BRT patterns (SARCASM_MARKERS)
        Layer 2: Context-dependent sarcasm (CONTEXT_DEPENDENT_SARCASM)
        Layer 3: Emoji-based sarcasm (😂😭 combination)
        Layer 4: Advanced Structural irony ("para ma... pero")
        Layer 5: Handled in SARCASM_MARKERS (BRT-specific resignation patterns)
        """
        triggers = []

        # Layer 1 — Direct sarcasm phrase matches
        for phrase in self.sarcasm_phrases:
            if phrase.lower() in text_clean:
                triggers.append(f"marker:{phrase}")

        # Layer 2 — Context-dependent sarcasm
        # These words are only sarcastic when near traffic/enforcement terms
        for word, required_context in self.context_sarcasm.items():
            if word.lower() in text_clean:
                for ctx_word in required_context:
                    if ctx_word.lower() in text_clean:
                        triggers.append(f"context:{word}+{ctx_word}")
                        break

        # Layer 3 — Emoji sarcasm combinations
        # 😂😭 together = resigned sarcasm (laughing at hopeless situation)
        if "😂" in text_original and "😭" in text_original:
            triggers.append("emoji:laugh-cry=resigned_sarcasm")
        # 😂 in context of traffic complaint = sarcasm
        if "😂" in text_original and any(
            t in text_clean for t in ["traffic", "trapik", "commute",
                                      "enforcer", "citom", "lto", "ccto", "brt"]
        ):
            triggers.append("emoji:😂+traffic_context")

        # Layer 4 — Advanced Structural irony patterns
        structural_patterns = [
            ("para ma", "pero"),      # "para ma-X pero" = irony
            ("para mabawasan", "pero"),
        ]
        for pattern_a, pattern_b in structural_patterns:
            if pattern_a in text_clean and pattern_b in text_clean:
                triggers.append(f"structural:{pattern_a}")

        return len(triggers) > 0, triggers

    # ─────────────────────────────────────────────────────────────
    # PHRASE-AWARE SENTIMENT SCORING
    # ─────────────────────────────────────────────────────────────
    def _score_sentiment_phrases(
        self, text: str
    ) -> Tuple[float, List, List, List]:
        """
        Score sentiment using phrase-first matching with
        intensifier multiplication and negation flipping.

        Returns:
            (score, words_found, intensifiers_applied, negations_applied)
        """
        scored_spans = []  # (start, end, score, word)
        matched_ranges = set()  # character positions already matched

        def add_match(start: int, end: int, score: float, word: str):
            """Add a match if it doesn't overlap with existing matches."""
            positions = set(range(start, end))
            if not positions & matched_ranges:
                matched_ranges.update(positions)
                scored_spans.append((start, score, word))

        # ── Phrase matching (longest first — critical for correctness) ──
        for phrase in self.neg_phrases:
            idx = 0
            while True:
                pos = text.find(phrase, idx)
                if pos == -1:
                    break
                # Verify word boundaries (avoid partial matches)
                before_ok = (pos == 0 or not text[pos-1].isalpha())
                after_ok  = (pos + len(phrase) >= len(text) or
                             not text[pos + len(phrase)].isalpha())
                if before_ok and after_ok:
                    add_match(pos, pos + len(phrase),
                              self.negative_lexicon[phrase], phrase)
                idx = pos + 1

        for phrase in self.pos_phrases:
            idx = 0
            while True:
                pos = text.find(phrase, idx)
                if pos == -1:
                    break
                before_ok = (pos == 0 or not text[pos-1].isalpha())
                after_ok  = (pos + len(phrase) >= len(text) or
                             not text[pos + len(phrase)].isalpha())
                if before_ok and after_ok:
                    add_match(pos, pos + len(phrase),
                              self.positive_lexicon[phrase], phrase)
                idx = pos + 1

        if not scored_spans:
            return 0.0, [], [], []

        # ── Intensifier detection ──────────────────────────────
        intensifiers_applied = []
        for phrase in self.intensifier_phrases:
            pos = text.find(phrase)
            if pos == -1:
                continue
            multiplier = self.intensifiers[phrase]
            # Look for a sentiment word within 40 characters after intensifier
            search_end = pos + len(phrase) + 40
            for i, (span_pos, score, word) in enumerate(scored_spans):
                if pos < span_pos < search_end:
                    new_score = score * multiplier
                    scored_spans[i] = (span_pos, new_score, word)
                    intensifiers_applied.append(
                        f"{phrase}x{multiplier}->{word}"
                    )
                    break

        # ── Negation detection ────────────────────────────────
        negations_applied = []
        for neg_phrase in self.negation_phrases:
            pos = text.find(neg_phrase)
            if pos == -1:
                continue
            # Look for a sentiment word within 35 characters after negation
            search_end = pos + len(neg_phrase) + 35
            for i, (span_pos, score, word) in enumerate(scored_spans):
                if pos < span_pos < search_end:
                    new_score = -score * 0.8  # flip and slightly reduce
                    scored_spans[i] = (span_pos, new_score, word)
                    negations_applied.append(f"{neg_phrase}->flipped:{word}")
                    break

        # ── Calculate final score ──────────────────────────────
        # Use evidence accumulation approach:
        # Sum scores but dampen successive same-direction evidence
        # (the 3rd negative word adds less than the 1st)
        scores = [s for _, s, _ in sorted(scored_spans)]
        words_found = [(w, round(s, 3))
                       for _, s, w in sorted(scored_spans, key=lambda x: abs(x[1]), reverse=True)]

        if not scores:
            return 0.0, [], [], []

        # Primary score from strongest evidence
        primary = scores[0] if scores else 0.0

        # Additional evidence adds diminishing contribution
        additional = sum(
            s * (0.5 ** i) for i, s in enumerate(scores[1:], 1)
        )

        final_score = primary + additional

        # Soft normalization — keeps scale but prevents extreme outliers
        final_score = final_score / (1 + abs(final_score) * 0.3)

        return final_score, words_found, intensifiers_applied, negations_applied

    # ─────────────────────────────────────────────────────────────
    # EMOJI SCORING
    # ─────────────────────────────────────────────────────────────
    def _score_emojis(self, text: str) -> Tuple[float, List[str]]:
        """Score sentiment from emoji usage."""
        total = 0.0
        hits  = []
        for emoji, score in self.EMOJI_SENTIMENT.items():
            if emoji in text:
                total += score
                hits.append(f"{emoji}:{score}")
        return total, hits

    # ─────────────────────────────────────────────────────────────
    # TEXT CLEANING
    # ─────────────────────────────────────────────────────────────
    def _clean_text(self, text: str) -> str:
        """Clean text while preserving sentiment-relevant content."""
        text = re.sub(r"http[s]?://\S+", " ", text)
        text = re.sub(r"\S+@\S+", " ", text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    # ─────────────────────────────────────────────────────────────
    # NEUTRAL RESPONSE
    # ─────────────────────────────────────────────────────────────
    def _neutral_response(self) -> Dict:
        return {
            "sentiment_score":      0.0,
            "sentiment_label":      "neutral",
            "sarcasm_detected":     False,
            "confidence":           0.0,
            "words_found":          [],
            "sarcasm_triggers":     [],
            "intensifiers_applied": [],
            "negations_applied":    [],
        }

    # ─────────────────────────────────────────────────────────────
    # EMOTION DETECTION
    # ─────────────────────────────────────────────────────────────
    def detect_emotions(self, text: str, 
                        sentiment_score: float,
                        sarcasm_detected: bool) -> dict:
        """
        Multi-label emotion detection.
        A single post can express multiple emotions simultaneously.
        Based on sentiment score + keyword patterns.
        """
        text_lower = text.lower()
        emotions = {}

        # Anger — very strong negative sentiment
        emotions["anger"] = sentiment_score <= -0.75

        # Frustration — moderate negative (default for negative posts)
        emotions["frustration"] = -0.75 < sentiment_score <= -0.3

        # Sarcasm — already computed by sarcasm detector
        emotions["sarcasm"] = sarcasm_detected

        # Fear — safety/danger keywords
        fear_keywords = [
            "danger", "unsafe", "accident", "bangga", "disgrasya",
            "nahadlok", "hadlok", "mahadlok", "crash", "patay",
            "namatay", "nasakitan", "injured", "dangerous",
            "risk", "risky", "baka", "mapuros",
        ]
        emotions["fear"] = any(kw in text_lower for kw in fear_keywords)

        # Disgust — corruption/abuse keywords  
        disgust_keywords = [
            "corrupt", "corruption", "abuso", "kotong", "hulidap",
            "palpak", "incompetent", "peke", "malicious", "anomalya",
            "disgusting", "manggilaw", "lagay", "bribe", "extort",
        ]
        emotions["disgust"] = any(kw in text_lower for kw in disgust_keywords)

        # Sadness — hopelessness/resignation keywords
        sadness_keywords = [
            "kapoy", "hopeless", "wala nay", "di na",
            "nasubo", "sad", "lungkot", "hilak",
            "naluha", "kinda sad", "dili na kaya",
        ]
        emotions["sadness"] = any(kw in text_lower for kw in sadness_keywords)

        # Resignation — "normal na" patterns
        resignation_keywords = [
            "normal na", "wala nay mahimo", "sanay na",
            "ganon talaga", "mao nay cebu", "mao na ni",
            "what do you expect", "expected na",
            "kanus-a pa kaha", "hahayz",
        ]
        emotions["resignation"] = any(kw in text_lower for kw in resignation_keywords)

        # Trust/Approval — positive posts about enforcement working
        emotions["trust"] = sentiment_score >= 0.35 and not sarcasm_detected

        # Build summary list
        active = [k for k, v in emotions.items() if v]
        emotions["emotions_list"] = ", ".join(active) if active else "neutral"

        return emotions

    # ─────────────────────────────────────────────────────────────
    # BATCH ANALYSIS (convenience method for batch processor)
    # ─────────────────────────────────────────────────────────────
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts and return list of results."""
        return [self.analyze(t) for t in texts]

    # ─────────────────────────────────────────────────────────────
    # TEST METHOD — for verifying lexicon coverage
    # ─────────────────────────────────────────────────────────────
    def test_examples(self):
        """
        Run test cases to verify the analyzer works correctly.
        Call this after updating the lexicon to sanity-check results.
        """
        test_cases = [
            # (text, expected_label, expected_sarcasm, description)
            ("Hayahay kaayo ang traffic sa Fuente karon!",
             "negative", True,
             "Classic hayahay sarcasm"),

            ("Grabe kaayo ang traffic sa SRP, dili na kaya!",
             "negative", False,
             "Intensifier + strong negative"),

            ("Gi kapoy na kaayo ko sa commute. Yawa.",
             "negative", False,
             "Frustration + expletive"),

            ("Puryagaba ning traffic sa Cebu ba!",
             "negative", True,
             "Authentic Cebuano frustration (now classified as sarcasm)"),

            ("CITOM naapprehend akong motor. Counterflow daw.",
             "negative", False,
             "Enforcement incident"),

            ("World Bank warns PH officials over slow BRT. Hahayz. 😂😭",
             "negative", True,
             "Resigned sarcasm with emoji"),

            ("Dili maayo ang traffic scheme sa one way.",
             "negative", False,
             "Negation flipping"),

            ("Naayo na ang dalan sa Mambaling, maayo kaayo!",
             "positive", False,
             "Positive road improvement"),

            ("Ang BRT counterproductive kaayo sa traffic.",
             "negative", True,
             "Counterproductive = sarcasm marker"),

            ("Supposed to decongest traffic ang groundbreaking pero nag-traffic pa more.",
             "negative", True,
             "Structural irony"),
        ]

        print("\n" + "="*65)
        print("  SENTIMENT ANALYZER TEST CASES")
        print("="*65)

        passed = 0
        failed = 0

        for text, exp_label, exp_sarcasm, desc in test_cases:
            result = self.analyze(text)
            label_ok   = result["sentiment_label"]  == exp_label
            sarcasm_ok = result["sarcasm_detected"] == exp_sarcasm
            ok = label_ok and sarcasm_ok

            status = "PASS" if ok else "FAIL"
            if ok:
                passed += 1
            else:
                failed += 1

            print(f"\n  [{status}] {desc}")
            safe_text = text[:70].encode('ascii', 'replace').decode('ascii')
            print(f"  Text    : {safe_text}")
            print(f"  Label   : {result['sentiment_label']:>8} "
                  f"(expected: {exp_label}) {'OK' if label_ok else 'WRONG'}")
            print(f"  Sarcasm : {str(result['sarcasm_detected']):>5} "
                  f"(expected: {exp_sarcasm}) {'OK' if sarcasm_ok else 'WRONG'}")
            print(f"  Score   : {result['sentiment_score']:>6.3f}  "
                  f"Confidence: {result['confidence']:.3f}")
            if result["sarcasm_triggers"]:
                safe_triggers = str(result["sarcasm_triggers"]).encode('ascii', 'replace').decode('ascii')
                print(f"  Sarcasm triggers : {safe_triggers}")
            if result["intensifiers_applied"]:
                print(f"  Intensifiers     : {result['intensifiers_applied']}")
            if result["negations_applied"]:
                print(f"  Negations        : {result['negations_applied']}")
            if result["words_found"]:
                print(f"  Words found      : {result['words_found'][:5]}")

        print(f"\n  Results: {passed} passed, {failed} failed "
              f"out of {len(test_cases)} tests")
        print("="*65 + "\n")
        return passed, failed