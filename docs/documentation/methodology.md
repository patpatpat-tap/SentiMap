# Methodology Answers (SentiMap)

This file consolidates methodology-related answers for documentation and thesis defense. Items marked "TBD" need your confirmation or numbers.

## 1. Data Collection and Validation
- Exact date range of scraped Reddit posts: December 6, 2015 to April 13, 2026.
- Total posts scraped before validation: 736 posts.
- Validation approach: semi-automated human-in-the-loop pipeline. Two-layer automated relevance scoring runs first; the principal researcher verifies edge cases flagged by the algorithm.
- Reviewers and inter-rater reliability: single-researcher review; bias mitigated by automated scoring before manual verification.
- Scraping method: custom Python scrapers using Reddit public .json endpoints (no API key), via requests (`sentimap_scraper_v2.py` and `sentimap_scraper_godmode.py`).

## 2. NLP Pipeline Details  
- Baseline comparison (VADER/TextBlob/etc.): no baseline comparison performed. Existing literature shows these tools underperform on Cebuano/Bislish; the custom hybrid lexicon is the primary methodological contribution.
- Location extraction method: deterministic keyword matching with strict word boundaries and confidence weighting (no NER or fuzzy matching).
- Location extraction accuracy: quantitative sample-based accuracy not measured. Spatial ambiguity is mitigated through UI verification (live coordinate badge and center crosshair for manual checks).
- Cebuano lexicon validation: validated functionally through the HITL pipeline where automated scoring triaged data and manual review handled edge cases.

## 3. Sarcasm Detection
- Sarcasm detection approach: custom 5-layer rules and markers.
- Confirmed detections: 42 sarcastic posts flagged within the final validated dataset.

## 4. Geospatial Mapping
- Unique hotspot locations: 27 extracted from the 180 validated posts.
- Handling unknown locations: posts without exact coordinates (about 137) are excluded from the heatmap to prevent spatial inaccuracies; they remain in the textual feed for context.
- Spatial ambiguity: mitigated via the live coordinate badge and crosshair overlay for manual verification.

## 5. Dataset Composition
- Topic breakdown: multi-label classification. In the 180 clean subset, the dominant category is Transport service (135 posts). Other high-frequency categories include Policy frustration, Infrastructure failure, Enforcement abuse, and Road safety. A specific enforcement query flagged 101 enforcement-related posts.
- Upvote distribution range: lowest = 0, highest = 11830, average = 197.
- Date distribution across years: strongly right-skewed and clustered in recent years (2015:1, 2017:2, 2018:10, 2019:8, 2020:4, 2021:5, 2022:10, 2023:80, 2024:218, 2025:261, 2026:137).

## 6. Sentiment Distribution
- Exact counts (n=180): 140 negative, 24 positive, 16 neutral.
- Sarcasm overlap: 42 posts flagged as sarcastic; in the current dataset, these map to the negative category.
- Threshold logic: `sentiment_label` is threshold-based in code. Negative if `sentiment_score < -0.15`, positive if `sentiment_score > 0.15`, otherwise neutral.

## 7. Emotion Analysis Results
- Emotion set: anger, frustration, fear, disgust, sadness, resignation, trust, sarcasm.
- Distribution across 180 posts (multi-label counts): Anger (72), Frustration (62), Sadness (59), Sarcasm (42), Fear (38), Trust (21), Disgust (9), Resignation (2).
- Mutually exclusive thresholds: anger and frustration have zero overlap by design. Frustration applies for -0.75 < score <= -0.3; anger applies for score <= -0.75.

## 8. Location and Hotspot Data
- Top locations (documented 105-post snapshot): Cebu City (38 mentions, avg sentiment -0.53), SRP (4 mentions, avg sentiment -0.62), Talamban (3 mentions, avg sentiment -0.8). A full top-5 list for the 180-post clean subset was not published.
- Hotspot cutoff definition: any mapped location with at least one extracted grievance; radii and severity scale by count and average sentiment.

## 9. Validation Methodology
- Borderline posts manually reviewed: 61.
- Acceptance criteria: D1 enforcement keywords, D2 transport keywords, D3 sentiment/grievance markers, D4 location specificity; auto-keep threshold, manual review band, and auto-discard rules in the v4 validator.
- Systematic errors found: not formally cataloged; hard-drop lists were used to reduce off-topic false positives.

## 10. System Performance
- Validator v4 performance: precision/recall not computed (no ground-truth labels).
- Location extraction accuracy: not formally measured; keyword matching with confidence weighting is used.

## 11. Research Claims
- "First linguistically accurate visualization tool" claim: should be phrased as "appears to be" unless a direct comparison study is completed.
- Novelty: hybrid Cebuano/Bislish lexicon, five-layer sarcasm detection, and geospatial hotspot mapping with precomputed NLP fields.

## 12. Limitations
- Reddit-only dataset.
- Snapshot system (not live ingestion).
- Small clean subset (180 posts).
- Lexicon and sarcasm rules may be domain- and author-specific.
- Keyword-based location extraction (no fuzzy or NER).
- Quantitative ground-truth validation not finalized.

## 13. Validation Quality
- Unanimous KEEP vs judgment calls: single-reviewer workflow; counts not tracked.
- Reviewer disagreements and resolution: not applicable (single reviewer).

## 14. Target Audience
- Target audience: thesis committee (academic) and local traffic policy stakeholders (practical deployment).

## 15. Quantitative Validation Numbers
- Accuracy/precision/recall/F1 for sentiment: not computed (no labeled ground-truth set).
- Accuracy for location extraction: not computed.
- Statement: "This study does not include quantitative validation against ground truth beyond the sarcasm verification on the clean subset."
