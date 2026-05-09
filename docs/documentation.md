# SentiMap Comprehensive Documentation

Last updated: 2026-05-10
Version: 1.0
Status: Snapshot system (not live streaming)

## 1. Executive Summary
SentiMap is a hybrid NLP and geospatial analytics system that transforms Cebu City traffic enforcement grievances into actionable intelligence. It ingests Reddit posts, filters and validates relevance, precomputes NLP fields (sentiment, sarcasm, emotions, and locations), and exposes the results via a FastAPI backend for a Next.js dashboard with a heatmap and analytics views.

Key objectives:
- Identify where grievances cluster (hotspots).
- Quantify severity and sarcasm in complaints.
- Provide explainable sentiment and emotion signals.

## 2. Research Context and Motivation
Cebuano and Bislish traffic discourse contains slang, sarcasm, and code-switching that general-purpose sentiment models often misinterpret. SentiMap addresses this by combining a Cebuano sentiment lexicon, sarcasm detection, and location extraction to produce a location-aware complaint heatmap.

## 3. System Goals and Scope
In-scope:
- Snapshot analysis of a curated Reddit dataset.
- Precomputed NLP fields stored in Supabase.
- FastAPI endpoints for data, heatmap, statistics, and text analysis.
- Dashboard and analytics interface with a map, feed, and charts.

Out-of-scope (current):
- Live streaming ingestion.
- ML model training pipeline.
- Real-time alerts and long-term trend forecasting.

## 4. System Architecture
High-level architecture:

Frontend (Next.js) -> FastAPI -> Supabase (PostgreSQL)
                    |           |
                    |           +- posts table
                    |
                    +- NLP modules (sentiment, sarcasm, emotions, locations)

Primary components:
- Scrapers for Reddit collection.
- Validation and cleanup scripts.
- NLP batch processor for enrichment.
- Supabase for persistent storage.
- FastAPI service for serving data and analytics.
- Next.js UI for dashboard and analytics views.

## 5. Data Sources and Collection
Primary source:
- Reddit posts from Cebu-focused subreddits and targeted searches.

Scrapers:
- Godmode scraper (two-layer filtering): [sentimap_scraper_godmode.py](../sentimap_scraper_godmode.py)
- Legacy v2 scraper: [sentimap_scraper_v2.py](../sentimap_scraper_v2.py)

Godmode filtering strategy:
- Layer 1: Mandatory core traffic and enforcement keywords.
- Layer 2: Relevance scoring. Posts must reach minimum score to be kept.
- Hard drop list for off-topic categories.

Outputs:
- reddit_godmode.json
- reddit_godmode.xlsx
- reddit_godmode_progress.json

## 6. Data Cleaning, Validation, and Merging
Cleaning and validation:
- Data cleanup: [backend/scripts/data_cleanup.py](../backend/scripts/data_cleanup.py)
- Validator pipeline (v4.0): [backend/scripts/data_validator.py](../backend/scripts/data_validator.py)

Merging v2 and godmode:
- Merge script: [backend/scripts/merge_godmode_data.py](../backend/scripts/merge_godmode_data.py)
- Output: backend/data/reddit_data_v3_clean.csv
- Deduplication by post ID
- Relevance-based filtering for godmode posts

## 7. Database (Supabase) Schema
Base schema creation:
- SQL: [backend/data/supabase_setup.sql](../backend/data/supabase_setup.sql)

Core columns:
- id (primary key)
- title, body, full_text
- created_date
- upvotes, num_comments
- url
- locations
- comments_text
- is_relevant
- created_at, updated_at

NLP enrichment fields (populated by batch processor):
- sentiment_score (float)
- sentiment_label (positive, neutral, negative)
- sarcasm_detected (boolean)
- sentiment_confidence (float)
- emotion_anger, emotion_frustration, emotion_fear, emotion_disgust
- emotion_sadness, emotion_resignation, emotion_trust
- emotions_list (string)
- platform (string)
- is_clean (boolean)

Note: NLP fields are updated by batch processing and used directly by the backend.

SQL migration (add NLP columns):
```sql
ALTER TABLE posts
  ADD COLUMN IF NOT EXISTS sentiment_score DOUBLE PRECISION,
  ADD COLUMN IF NOT EXISTS sentiment_label TEXT,
  ADD COLUMN IF NOT EXISTS sarcasm_detected BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS sentiment_confidence DOUBLE PRECISION,
  ADD COLUMN IF NOT EXISTS emotion_anger BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotion_frustration BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotion_fear BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotion_disgust BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotion_sadness BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotion_resignation BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotion_trust BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS emotions_list TEXT,
  ADD COLUMN IF NOT EXISTS platform TEXT,
  ADD COLUMN IF NOT EXISTS is_clean BOOLEAN DEFAULT FALSE;
```

## 8. NLP Engine
Primary modules:
- Lexicon: [backend/app/cebuano_lexicon.py](../backend/app/cebuano_lexicon.py)
- Analyzer: [backend/app/sentiment_analyzer.py](../backend/app/sentiment_analyzer.py)

Key features:
- Phrase-first matching (longest phrases matched before shorter ones).
- Cebuano lexicon with traffic-specific vocabulary and expletives.
- Sarcasm detection (five-layer system).
- Intensifiers and negation handling.
- Emoji sentiment scoring.
- Multi-label emotion detection.

Sentiment scoring highlights:
- Scores are accumulated with diminishing weights.
- Sarcasm can flip positive polarity to negative.
- Confidence is derived from evidence count.

Emotion detection (multi-label):
- Anger: strong negative sentiment.
- Frustration: moderate negative sentiment.
- Fear: safety-related keywords.
- Disgust: corruption/abuse keywords.
- Sadness: hopelessness keywords.
- Resignation: normalizing or defeated language.
- Trust: strong positive sentiment without sarcasm.

## 9. Location Extraction
Module:
- [backend/app/location_extractor.py](../backend/app/location_extractor.py)

Behavior:
- Keyword-based, case-insensitive matching.
- Word boundary checks to reduce false positives.
- Confidence weighting for specific vs. generic locations.
- Generic location suppression for heatmap accuracy (example: Cebu City).

## 10. Geospatial Clustering and Heatmap
Module:
- [backend/app/geospatial.py](../backend/app/geospatial.py)

Clustering strategy:
- Posts are grouped by extracted locations.
- Each cluster computes:
  - count
  - average sentiment
  - sarcasm count
  - platform distribution
  - radii (outer, mid, core)

Severity color:
- Derived from negative polarity.
- Red (critical), orange (moderate), yellow (low).

Radii formula:
- Outer = 200 + count*80 + severity*150
- Mid = 100 + count*50 + severity*80
- Core = 50 + count*30 + severity*40

## 11. Backend Service (FastAPI)
Entry point:
- [backend/app/main.py](../backend/app/main.py)

Configuration:
- Environment variables loaded via .env
- Supabase credentials used by [backend/app/supabase_client.py](../backend/app/supabase_client.py)

API endpoints:
- GET /api/data
  - Returns all clean posts with precomputed NLP fields
- GET /api/heatmap
  - Returns clustered heatmap zones with severity, radii, and counts
- GET /api/stats
  - Returns aggregated sentiment counts, location stats, sarcasm rate, emotion counts
- GET /api/analyze
  - Analyzes custom text for sentiment and locations
- GET /api/locations
  - Returns known Cebu locations
- GET /health
  - Health check

Filtering:
- Only is_clean posts are used for analysis and visualization.

## 12. Supabase Client
Module:
- [backend/app/supabase_client.py](../backend/app/supabase_client.py)

Behavior:
- Simple REST API client (no supabase-py dependency).
- Fetches all posts and filtered sets.
- Updates location and NLP fields as needed.

## 13. NLP Batch Processing
Script:
- [backend/scripts/nlp_batch_processor.py](../backend/scripts/nlp_batch_processor.py)

Purpose:
- Precompute NLP fields for all is_clean posts.
- Writes sentiment, sarcasm, emotions, and locations to Supabase.
- Produces a JSON report (nlp_batch_report.json).

## 14. Frontend (Next.js)
Configuration:
- API rewrite proxy: [frontend/next.config.ts](../frontend/next.config.ts)
- Backend URL controlled by BACKEND_URL environment variable.

Main entry:
- Dashboard page: [frontend/app/page.tsx](../frontend/app/page.tsx)

Components:
- Sidebar navigation: [frontend/app/components/Sidebar.tsx](../frontend/app/components/Sidebar.tsx)
- Map wrapper: [frontend/app/components/SentiMapMap.tsx](../frontend/app/components/SentiMapMap.tsx)
- Leaflet map: [frontend/app/components/MapComponentInner.tsx](../frontend/app/components/MapComponentInner.tsx)
- Feed: [frontend/app/components/GrievanceFeed.tsx](../frontend/app/components/GrievanceFeed.tsx)
- Analytics: [frontend/app/components/AnalyticsPage.tsx](../frontend/app/components/AnalyticsPage.tsx)

Layout:
- 70 percent map and 30 percent right sidebar on dashboard.
- Right sidebar is split into KPI cards (30 percent) and grievance feed (70 percent).
- Analytics view uses a multi-panel grid of charts and summary cards.

Styling:
- Global styles: [frontend/app/globals.css](../frontend/app/globals.css)
- Glassmorphism panels with dark palette.
- Leaflet controls and legend restyled for map clarity.

## 15. Analytics Views and Metrics
Analytics panels include:
- Emotion distribution (multi-label bar chart).
- Severity mix (donut chart).
- Sarcasm vs direct (donut chart).
- Dominant emotions list.
- Emotion by hotspot (stacked bar chart).
- Category breakdown (computed from dataset).

Data sources:
- stats.emotion_counts from /api/stats (fallback computed in frontend).
- grievances array for hotspot and severity calculations.

Category breakdown computation (target behavior):
- Replace the static category list with rule-based classification on each grievance.
- Use title, body, and emotions_list for keyword matching.
- Example categories and signals:
  - Enforcement abuse: CITOM, LTO, LTFRB, apprehend, kotong, abuso
  - Transport service: jeepney, taxi, fare, overcharging, driver
  - Infrastructure failure: BRT, roadwork, pothole, delay, unfinished
  - Policy frustration: scheme, one-way, road policy, ordinance
  - Road safety: accident, disgrasya, reckless, counterflow
- Aggregate counts by category and feed the chart directly from the computed totals.

## 16. Operational Runbook (Local)
Prerequisites:
- Node.js
- Python environment with required packages
- Supabase credentials in .env

Start backend:
- Run FastAPI with uvicorn from backend directory.

Start frontend:
- Use npm run dev from frontend directory.

Environment variables:
- BACKEND_URL for frontend proxy
- SUPABASE_URL and SUPABASE_KEY for backend

Note: Use service role keys only for trusted server-side scripts. Do not commit or share secret keys.

## 17. Verification and Health Checks
Verification script:
- [backend/scripts/verify_system.py](../backend/scripts/verify_system.py)

Checks:
- /api/stats
- /api/data
- /api/locations

Health endpoint:
- /health

## 18. Known Limitations
- Snapshot system only, no live ingestion.
- Location extraction is keyword-based (no fuzzy matching).
- Category breakdown uses static data (not computed from database).
- Sarcasm detection focuses on explicit markers and may miss subtle cases.

## 19. Security and Ethics
- Data source is public Reddit content.
- Avoid storing sensitive identifiers beyond post IDs and URLs.
- Use Supabase Row Level Security policies for public reads.
- Service role keys must be protected and stored only in secure env files.

## 20. Future Enhancements
- Scheduled or near-real-time ingestion pipeline.
- ML-based sentiment and sarcasm classification.
- Fuzzy matching for locations and spelling variants.
- Live trend alerts for emerging hotspots.
- Admin console for dataset curation and QA.

## 21. Glossary
- NLP: Natural Language Processing.
- Sarcasm detection: identification of ironic or sarcastic language patterns.
- Heatmap: geospatial visualization using intensity based on counts and severity.
- Hotspot: location with clustered grievances and elevated severity.

## Appendix A. Defense-Ready Summary

### A1. Architecture Diagram
```
Frontend (Next.js)
  |  /api/* (proxy)
  v
FastAPI (app/main.py)
  |  Supabase REST
  v
Supabase (posts table)
  |  NLP batch processor writes NLP fields
  v
NLP modules (lexicon, sarcasm, emotions, locations)
```

### A2. Data Pipeline Diagram
```
Scrape (godmode) -> Merge -> Clean/Validate -> Supabase
                                      |
                                      v
                               NLP batch process
```

### A3. NLP Flow Diagram
```
Raw text
  -> clean text
  -> sarcasm detection
  -> emoji scoring
  -> phrase-first sentiment scoring
  -> intensifier/negation adjustment
  -> multi-label emotions
  -> output fields written to Supabase
```

### A4. Dataset Snapshot (latest documented)
Data source: Reddit dataset in Supabase (total 736 posts).
Clean subset used for dashboards: 180 posts.
Sentiment breakdown (clean posts): 140 negative, 16 neutral, 24 positive.
Sarcasm detected: 42 posts (23.3 percent of clean subset).

### A5. Key Metrics (from API)
- total_grievances: count of clean posts served by /api/stats
- sentiment_breakdown: positive, neutral, negative
- avg_sentiment_score: average polarity score across clean posts
- sarcasm_percentage: sarcastic posts divided by total clean posts
- locations: ranked by grievance count and average sentiment
- emotion_counts: anger, frustration, fear, disgust, sadness, resignation, trust, sarcasm
