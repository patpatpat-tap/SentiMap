# SentiMap Master Summary (All Docs Consolidated)

Last updated: 2026-05-11
Status: Snapshot system (not live streaming)

## 1. Project Overview
SentiMap is a hybrid NLP and geospatial dashboard that transforms Cebu traffic enforcement grievances into actionable hotspot intelligence. It ingests Reddit posts, validates relevance, precomputes Cebuano/Bislish-aware NLP fields (sentiment, sarcasm, emotions, locations), and visualizes the results as a heatmap with a grievance feed and analytics panels.

Core research focus:
- Address the language-context gap in Cebuano/Bislish discourse.
- Detect sarcasm that flips literal positivity into real-world negativity.
- Map grievances to specific Cebu City locations for spatial analysis.

Primary questions answered:
- Where are grievance hotspots?
- How severe are complaints?
- How often are posts sarcastic or emotionally charged?

## 2. Research Context and Motivation
Public grievance data on social platforms is unstructured and usually ignored by authorities. Cebuano and Bislish expressions, sarcasm, and slang cause English-trained sentiment tools to fail on real Cebu traffic complaints. SentiMap uses a Cebuano lexicon, sarcasm detection, and location extraction to produce a location-aware heatmap of public grievances.

## 3. End-to-End Pipeline (Start to Finish)
1) Scrape Reddit posts (godmode scraper).
2) Merge v2 and godmode datasets with deduplication.
3) Validate and clean posts; mark is_clean for analytics eligibility.
4) Import into Supabase posts table.
5) Run NLP batch processing to precompute sentiment, sarcasm, emotions, and locations.
6) Serve precomputed results via FastAPI endpoints.
7) Visualize in Next.js with map, feed, and analytics views.

## 4. Data Collection and Godmode Scraping
Godmode scraper features:
- Two-layer filtering: CORE traffic keywords required; relevance score threshold enforced.
- Targeted searches (29 queries) beyond hot/top/new listings.
- Crash recovery with progress checkpoints.
- Explicit hard-drop list to avoid off-topic posts.

Outputs:
- reddit_godmode.json (raw posts)
- reddit_godmode.xlsx (excel export)
- reddit_godmode_progress.json (checkpoint)

Merged dataset:
- Total posts: 736 (58 v2 + 678 godmode after dedupe)
- Merged output: backend/data/reddit_data_v3_clean.csv

## 5. Validation and Data Quality
Validation logic (v4 pipeline):
- D1 enforcement keywords (CITOM, LTO, checkpoint, etc.)
- D2 transport keywords (jeepney, taxi, commute, fare, etc.)
- D3 sentiment/grievance markers (sarcasm, frustration, complaints)
- D4 location specificity (SRP, Mambaling, Talamban, etc.)
- Auto-keep threshold, manual review band, auto-discard rules

Key outcome (documented):
- Clean subset used for analytics: 180 posts

## 6. Dataset Snapshot (Latest Documented)
- Total dataset in Supabase: 736 posts
- Clean subset (is_clean): 180 posts
- Sentiment breakdown (clean subset): 140 negative, 16 neutral, 24 positive
- Sarcasm detected: 42 posts (23.3 percent of clean subset)

## 7. System Architecture
Frontend (Next.js) -> FastAPI -> Supabase (PostgreSQL)
	- Next.js App Router UI with map, feed, and analytics views
	- FastAPI endpoints serve precomputed NLP and heatmap clusters
	- Supabase stores posts and NLP fields

## 8. Backend Capabilities (FastAPI)
Endpoints:
- /api/data: clean posts with precomputed NLP and emotions
- /api/heatmap: clustered map zones (counts, sarcasm_count, radii)
- /api/stats: sentiment summary, location ranking, emotion_counts
- /api/analyze: ad hoc text analysis
- /api/locations: known Cebu locations
- /health: service check

Key logic:
- Snapshot mode only (not live)
- Generic-location suppression for mapping quality
- Confidence filtering for locations

## 9. Supabase Migration and Schema
Supabase migration is complete and operational. The posts table stores both raw and NLP-enriched fields. Supabase REST API is used by the backend client.

Core columns:
- id, title, body, full_text, created_date, upvotes, num_comments, url
- locations, comments_text, is_relevant, is_clean

NLP enrichment columns:
- sentiment_score, sentiment_label, sentiment_confidence
- sarcasm_detected
- emotion_anger, emotion_frustration, emotion_fear, emotion_disgust
- emotion_sadness, emotion_resignation, emotion_trust
- emotions_list
- platform

## 10. NLP Engine (Hybrid Cebuano/Bislish)
Modules:
- Cebuano sentiment lexicon with phrase-first matching
- Sarcasm detection (five-layer system)
- Intensifiers and negation handling
- Emoji sentiment weighting
- Multi-label emotion detection

Emotion set:
- Anger, Frustration, Fear, Disgust, Sadness, Resignation, Trust, Sarcasm

Outputs stored per post:
- sentiment_score, sentiment_label, sentiment_confidence
- sarcasm_detected
- emotion flags and emotions_list
- extracted locations

## 11. Geospatial Clustering and Heatmap
Clustering behavior:
- Group by extracted location
- Compute count, avg sentiment, sarcasm_count, and platform distribution
- Compute three-layer radii (outer, mid, core)
- Map severity color by negative polarity

Legend and controls:
- Bottom-left intensity legend with critical/moderate/low
- Custom zoom controls
- Location pill for Cebu coordinates

## 12. Frontend UI (Dashboard and Analytics)
Dashboard:
- 70/30 split: map (left) and right sidebar (KPI panel + feed)
- Grievance feed with pinned group, sentiment pills, emotion tags
- Intensity bar with signed polarity
- Engagement metrics (upvotes, comments)

Analytics:
- Emotion distribution (multi-label bar chart)
- Severity mix donut
- Sarcasm vs direct donut
- Dominant emotions list
- Emotion by hotspot stacked bars
- Category breakdown chart (documented as placeholder, target is computed)

Design system:
- Glassmorphism panels with dark mission-control palette
- Typography hierarchy for glanceability
- Bidirectional map-feed highlighting

## 13. Design Implementation (Rationale)
Design intent:
- 5-second glanceability for traffic authorities
- Map-first hierarchy with clear visual separation
- Subtle gradients and translucent borders to reduce noise
- Severity color system (red/orange/yellow) reserved for risk

Interaction principles:
- Hover linking between map and feed
- Fly-to animation for location focus
- Progressive disclosure on cards

## 14. QA and System Analysis Notes
Confirmed requirements:
- All data is Reddit-only (no Facebook filters)
- System is a snapshot, not live
- Sentiment is positive/neutral/negative with sarcasm
- Multi-label emotions are supported in NLP pipeline

Recommended removals:
- Remove any platform filter or LIVE indicator if present
- Remove filters that do not map to actual dataset constraints

Recommended additions:
- Data quality indicator (counts, date range, clean subset size)
- Computed category breakdown from dataset

## 15. Operational Runbook (Local)
Backend:
- Start FastAPI with uvicorn on 127.0.0.1:8000
Frontend:
- Run Next.js on localhost:3000

Data pipeline commands:
- Scrape: sentimap_scraper_godmode.py
- Merge: backend/scripts/merge_godmode_data.py
- Import: backend/scripts/import_to_supabase_simple.py
- NLP batch: backend/scripts/nlp_batch_processor.py

## 16. Known Limitations and Risks
- Snapshot only (no live ingestion)
- Location extraction is keyword-based (no fuzzy matching)
- Sarcasm detection misses subtle cases if full_text is sparse
- Category breakdown may be static unless computed from data

## 17. Roadmap and Next Milestones
- Improve location and sentiment accuracy (precision/recall checks)
- Finalize warm civic UI consistency
- Add caching or pagination if needed
- Automate ingestion for near-live updates only after accuracy is stable

## 18. Document Sources Covered
This summary consolidates and updates all content from:
- DESIGN_IMPLEMENTATION.md
- DEVELOPMENT_PLAN.md
- GODMODE_IMPLEMENTATION.md
- IMPLEMENTATION_COMPLETE.md
- IMPLEMENTATION_SUMMARY.md
- OBJECTIVE.md
- sentimap_supabase_migration_complete.md
- sentiment_prompt.md
- SUMMARY.md (previous version)
- system.md