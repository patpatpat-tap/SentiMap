Summary of Last Week's Work
Phase 1: Data Validation (Completed)
Ran data_validator.py to auto-score all 736 posts across 4 dimensions:

D1 = Enforcement keywords (CITOM, LTO, checkpoint, etc.)
D2 = Transport keywords (jeepney, taxi, fare hike, commute, etc.)
D3 = Sentiment/grievance markers (hayahay, grabe, sarcasm, etc.)
D4 = Location specificity (Mambaling, SRP, Bulacao, etc.)
Auto-decision logic:

Keep if score >= 6
Review if score 3-5 (you manually decided these)
Discard if score <= 2 OR fails gating rules
Your manual review: 58 borderline posts

Final result: 142 posts marked clean (up from 111 auto-kept)
594 posts discarded as irrelevant
All results written to Supabase with is_clean flag

The Problem We Discovered
The validation script is too strict with keyword matching. Posts that are clearly about traffic/commute grievances get auto-discarded because:

Example 1: "Puryagaba ning traffic sa Cebu ba!" (Complaining about traffic)

"traffic" ≠ in ENFORCEMENT_KEYWORDS (not official enough)
"traffic" ≠ in TRANSPORT_KEYWORDS (only has jeepney, taxi, etc.)
Result: Auto-discarded despite being a valid grievance
Example 2: "Is it me or Cebu BRT kay counterproductive?"

"BRT" scores 3 pts (D1)
But "counterproductive" ≠ SENTIMENT_KEYWORDS
Result: Might fail gating or final score threshold
Root cause: The keyword lists are incomplete. They don't cover common traffic complaint vocabulary.

Solution Going Forward
Option 1 (Recommended): Expand keyword lists with missing terms:

Add "traffic" to TRANSPORT_KEYWORDS
Add "congestion", "annoying", "counterproductive" to SENTIMENT_KEYWORDS
Add "gridlock", "slow moving" to ENFORCEMENT_KEYWORDS
Then re-run validation to capture previously discarded posts
Option 2: Keep 142 clean posts for now, move to Phase 3 (NLP pre-computation), and refine keyword lists later