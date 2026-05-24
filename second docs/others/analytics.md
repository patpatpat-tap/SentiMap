# SentiMap Analytics Page Architecture

This document summarizes the architecture, data flow, and visualization components of the SentiMap Analytics Page, based on an analysis of the codebase (`AnalyticsPage.tsx` and the FastAPI backend).

## Overview
The Analytics Page is a React component (`AnalyticsPage.tsx`) built for the SentiMap Next.js frontend. It provides a deeper dive into the emotional and thematic trends of the grievances collected, moving beyond simple geospatial heatmaps to offer academic-grade, multi-label emotion analysis.

## Visualizations & Metrics
The page utilizes the `recharts` library to render the following visualizations:

1. **Emotion Distribution (Horizontal Bar Chart)**: Displays the frequency of each detected emotion (Anger, Frustration, Sarcasm, Resignation, Fear, Disgust, Sadness, Trust) across all reports.
2. **Severity Mix (Donut Chart)**: Buckets negative grievances into Severe, Moderate, and Low based on sentiment polarity scores.
3. **Sarcasm vs Direct (Donut Chart)**: Compares the volume of sarcastic posts versus direct complaints.
4. **Dominant Emotions (Ranked List)**: Highlights the top 3 emotions by signal count.
5. **Emotion by Hotspot (Stacked Bar Chart)**: Analyzes the top 8 locations, showing the breakdown of specific emotions driving the grievances in those areas.
6. **Grievance Category Breakdown (Horizontal Bar Chart)**: Displays manually coded categories like "Enforcement abuse", "Transport service", "Infrastructure failure", etc., mapped against post counts.

## Data Flow & Backend Integration
The Analytics page relies on data provided by the `SentiMapDashboard` (parent page), which aggregates data from several backend endpoints. 

### `GET /api/stats`
The primary endpoint powering the analytics is `/api/stats` in `backend/app/main.py`. This endpoint:
- Fetches all validated (`is_clean=True`) posts from Supabase.
- Computes aggregated metrics: total grievances, sentiment breakdowns, average sentiment scores, and sarcasm percentages.
- **Emotion Counts**: Aggregates boolean emotion flags pre-computed by the NLP pipeline (`emotion_anger`, `emotion_frustration`, etc.) into global counts.

### Multi-label Emotion Pipeline
The frontend relies heavily on the backend's heuristic-based NLP processor. The methodology is transparently documented in the UI and defined as:
- **Anger**: polarity ≥ 0.75
- **Frustration**: polarity 0.50–0.75
- **Sarcasm**: flagged by the custom classifier
- **Resignation**: matched keywords (e.g., "normal na", "wala nay")
- **Fear**: matched keywords (e.g., danger, unsafe, crash)
- **Disgust**: matched keywords (e.g., corrupt, abuse, incompetent)
- **Sadness**: matched keywords (e.g., hopeless, kapoy)
- **Trust**: polarity < 0.35

Because these emotions are multi-label, a single grievance can trigger multiple emotion flags simultaneously, meaning total emotion signals often exceed the total report count.

## Location Context
The analytics view responds dynamically to location selections made on the Dashboard's map. If a `selectedLocation` is passed down, the dataset is instantly filtered to show analytics *only* for that specific hotspot, allowing granular area-level analysis.
