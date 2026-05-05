# SentiMap Objective (Current)

Last updated: May 3, 2026
Status: Active development, validated snapshot mode (not live streaming)

## 1) Project Goal
SentiMap transforms Cebu traffic grievance posts into actionable geospatial intelligence for authorities.

Primary questions:
- Where are grievance hotspots?
- How severe are complaints?
- How often are posts sarcastic or emotionally charged?

## 2) Current Process
1. Collect and merge Reddit data into a master dataset.
2. Validate/clean posts and mark relevant entries via is_clean.
3. Precompute NLP fields and store results in Supabase.
4. Serve precomputed analytics through FastAPI.
5. Visualize in Next.js using map + feed + analytics views.

## 3) Data and NLP State
- Total dataset in Supabase: 736 posts.
- Current validated clean subset used for dashboard analytics: 180 posts.
- NLP fields in use:
  - sentiment_score, sentiment_label (positive/neutral/negative)
  - sarcasm_detected, sentiment_confidence
  - location extraction with confidence filtering
  - emotion flags: anger, frustration, fear, disgust, sadness, resignation, trust

Latest batch outcome (clean posts):
- Negative: 140 (78%)
- Neutral: 16 (9%)
- Positive: 24 (13%)
- Sarcasm detected: 42 (23.3%)

## 4) Backend (Implemented)
Framework: FastAPI + Supabase

Active endpoints:
- /api/data: cleaned posts with precomputed NLP + emotion fields
- /api/heatmap: clustered map zones with counts, sarcasm_count, and radii
- /api/stats: sentiment summary + location ranking + emotion_counts
- /api/analyze: ad hoc single-text sentiment/location check
- /api/locations: known location list
- /health: service check

Key logic currently implemented:
- Snapshot mode (not live ingestion).
- Generic-location suppression for mapping quality.
- Location confidence thresholding and mapped-location filtering.

## 5) Frontend (Implemented)
Framework: Next.js (App Router) + React + Leaflet + Recharts

Current UI snapshot (based on latest dashboard/analytics screens):
- Left fixed navigation: Dashboard and Analytics tabs, with in-page Analytics section links.
- Dashboard view:
  - Interactive Cebu heatmap with three-layer zones, visible core markers, and bottom-left intensity legend (High/Moderate/Low).
  - Top-right map KPI card (total reports, negative count/percentage, sarcastic count/percentage).
  - Right grievance feed with sentiment filter chips (All/Negative/Neutral/Positive), location tags, quote preview, intensity score, engagement metrics, and source link.
- Analytics view:
  - KPI cards (Total Reports, Negative, Sarcastic, Active Hotspots).
  - Emotion Distribution (8-emotion horizontal bar chart).
  - Severity Mix donut and Sarcasm vs Direct donut.
  - Dominant Emotions ranking panel.
  - Emotion by Hotspot stacked bar chart.
  - Grievance Category Breakdown chart.
  - Methodology/Transparency card documenting rule-based emotion derivation.

## 6) What Has Been Achieved
- End-to-end pipeline from scraping to dashboard is functional.
- Supabase integration replaced local-file-only workflow.
- Precomputed NLP reduced dependence on expensive on-request full analysis.
- Cebuano/Bislish sentiment + sarcasm handling is operational in production code.
- Geospatial clustering and hotspot visualization are stable and interactive.
- Dashboard + Analytics dual-view UI is operational with navigation, filters, and chart-driven summaries.
- Multi-emotion analytics have been introduced and exposed in UI and API.

## 7) Current UI/UX Design State (Brief)
- Two-mode experience: Dashboard (map + feed) and Analytics (emotion transparency), with a minimal icon rail for switching.
- Glassmorphism system in use: translucent panels, hairline borders, and softened glow to separate layers without heavy chrome.
- Map-first hierarchy: 70/30 split for spatial context vs. narrative evidence; KPI tiles live above the feed.
- Grievance cards are layered for 5-second scanning (severity accent, tags, location, headline, quote, intensity bar, engagement footer).
- Analytics focuses on explainability: distribution, donuts, rankings, hotspot mix, category breakdown, and a methodology block.
- Color and typography are consistent across views to make emotion and severity readable at a glance.

## 8) Current Product Position
SentiMap is currently a validated analysis snapshot system, suitable for:
- thesis demonstration,
- policy exploration,
- hotspot trend interpretation.

It is not yet a fully live ingestion platform.

## 9) Next Milestones
1. Improve location and sentiment accuracy further (precision/recall checks).
2. Finalize warm civic UI consistency across all dashboard sections.
3. Add production cache/pagination hardening where needed.
4. Introduce scheduled ingestion for near-live operation only after quality thresholds are met.
