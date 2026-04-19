# SentiMap — Full Context & Fix Prompt
## Ready to paste into a new Claude conversation

---

## WHO I AM & WHAT THIS PROJECT IS

I am a student researcher developing **SentiMap** — a research system titled:
> *"Geospatial Sentiment Analysis: A Hybrid NLP Approach for Mapping Traffic Enforcement Grievances in Cebu City"*

SentiMap harvests Reddit posts from r/Cebu, runs Cebuano/Bislish-aware NLP (sentiment analysis, sarcasm detection, location extraction), and visualizes results as a geospatial heatmap dashboard. The goal is to show traffic enforcement hotspots in Cebu City using citizen-driven social media data.

---

## CURRENT TECH STACK

| Layer | Technology |
|---|---|
| Frontend | Next.js (App Router), React, Tailwind CSS |
| Backend | Python 3.14, FastAPI, Uvicorn |
| Database | Supabase (PostgreSQL) |
| NLP | Custom Python modules (lexicon-based, no ML classifier yet) |
| Map | Leaflet.js + OpenStreetMap tiles |
| Data Source | Reddit r/Cebu (public .json endpoints, no API key) |

**Local URLs:**
- Frontend: `http://localhost:3000`
- Backend: `http://127.0.0.1:8000`

---

## PROJECT FOLDER STRUCTURE

```
D:\PROJECTS\SentiMap\
├── backend\
│   ├── app\
│   │   ├── main.py                  ← FastAPI app (Supabase-enabled)
│   │   ├── supabase_client.py       ← Supabase REST queries
│   │   ├── sentiment_analyzer.py    ← Cebuano NLP
│   │   ├── location_extractor.py    ← Location NER
│   │   ├── geospatial.py            ← Coordinate mapping + clustering
│   │   ├── cebuano_lexicon.py       ← Custom sentiment lexicon
│   │   └── .env                     ← SUPABASE_URL, SUPABASE_KEY
│   └── venv\
│       ├── data\                    ← Excel backup files
│       └── Scripts\activate
├── frontend\
│   └── app\                         ← Next.js pages and components
└── sentimap_scraper_v2.py           ← Reddit scraper (no API key needed)
```

---

## CURRENT SYSTEM STATUS

### What is WORKING:
- ✅ FastAPI backend running, all 5 endpoints operational
- ✅ Supabase connected with 58 posts in `posts` table
- ✅ `/api/data` returns 58 posts with NLP enrichment (sentiment, locations, sarcasm)
- ✅ `/api/heatmap` returns 12 location clusters with coordinates
- ✅ `/api/stats` returns sentiment breakdown
- ✅ Frontend map renders (Leaflet + OpenStreetMap Cebu tiles)
- ✅ NLP pipeline runs end-to-end on post titles

### What is BROKEN / NOT WORKING:
- ❌ Dashboard header shows `0 REPORTS, 0 SEVERE, 0 SARCASTIC, 0 HOTSPOTS` despite data existing
- ❌ Right panel shows "No grievances match the selected filters" — no posts render
- ❌ No map pins or heatmap circles appear on the map
- ❌ Sarcasm detection is at 0% (NLP only runs on titles, not post body)
- ❌ Platform field is `"unknown"` for all 58 posts (causing frontend filter to return nothing)

---

## ROOT CAUSES IDENTIFIED

### Problem 1 — Platform field is "unknown" (CRITICAL — causes zero display)
All 58 posts in Supabase have `platform: "unknown"` or NULL. The frontend has a PLATFORM filter (`ALL` / `FACEBOOK` / `REDDIT`) that tries to match on this field. Since no post has `platform: "reddit"`, the filter returns zero results — which is why the dashboard shows all zeros despite data existing.

**Fix needed:**
```sql
-- Run in Supabase SQL Editor
UPDATE posts SET platform = 'reddit' WHERE platform IS NULL OR platform = 'unknown';
```
Then remove the FACEBOOK button from the frontend entirely (all data is Reddit-only — Facebook data is not free/accessible).

### Problem 2 — Wrong/fallback coordinates in heatmap (causes empty map)
From `/api/heatmap` response, multiple distinct locations all return the same coordinates `[10.3157, 123.8854]` (generic Cebu City center):
- "Robinsons Place" → `[10.3157, 123.8854]` ← WRONG
- "Pier Area" → `[10.3157, 123.8854]` ← WRONG
- "Ayala Mall" → `[10.3157, 123.8854]` ← WRONG

These locations are not in `geospatial.py`'s coordinate lookup dictionary, so they fall back to center. All pins stack invisibly on one point.

**Fix needed:** Add missing coordinates to `geospatial.py`:
```python
"Robinsons Place":    [10.3173, 123.9024],
"Pier Area":          [10.2942, 123.9017],
"Ayala Mall":         [10.3133, 123.9190],
"Ayala":              [10.3133, 123.9190],
"Fuente Osmeña":      [10.3050, 123.8820],
"IT Park":            [10.3310, 123.9050],
"Colon Street":       [10.2940, 123.8970],
"Talamban":           [10.3850, 123.9080],
"Talisay City":       [10.2480, 123.8430],
"Mandaue":            [10.3236, 123.9223],
"Mactan":             [10.2954, 123.9783],
"Carbon":             [10.2947, 123.8973],
"Mambaling":          [10.2820, 123.8780],
"Lahug":              [10.3280, 123.8990],
"Banawa":             [10.3370, 123.8850],
"Guadalupe":          [10.3050, 123.9120],
"Bulacao":            [10.2760, 123.8710],
"Consolacion":        [10.3762, 123.9573],
"Minglanilla":        [10.2415, 123.8002],
"Talisay":            [10.2480, 123.8430],
"Liloan":             [10.3997, 123.9971],
"Pardo":              [10.2760, 123.8620],
"Capitol":            [10.3170, 123.8910],
"Basak":              [10.3050, 123.9310],
"Salinas Drive":      [10.3230, 123.9020],
"N. Bacalso":         [10.2700, 123.8620],
"Osmeña Blvd":        [10.3000, 123.8870],
"Transcentral":       [10.3500, 123.8500],
```

### Problem 3 — Frontend field mapping mismatch (causes zero stats)
The dashboard header counts (REPORTS, SEVERE, SARCASTIC, HOTSPOTS) are all 0 despite the API returning real data. This means the frontend JavaScript is reading field names that don't match what the backend returns. Needs the frontend component that renders stats to be audited against the actual API response schema.

### Problem 4 — NLP runs on titles only (causes 0% sarcasm, weak sentiment)
In `main.py`, every NLP call is:
```python
sentiment = sentiment_analyzer.analyze(record['title'])
locations = location_extractor.extract(record['title'])
```
Post bodies (`body` field) and comments (`comments_text`) exist in Supabase but are never used. This is why sarcasm detection is 0% — titles are too short (avg 8 words) to trigger sarcasm patterns. The body text is where Bislish, sarcasm, and specific location mentions actually live.

**Fix needed — update all NLP calls to use full_text:**
```python
nlp_text = record.get('full_text') or record.get('body') or record.get('title', '')
sentiment = sentiment_analyzer.analyze(nlp_text)
locations = location_extractor.extract(nlp_text)
```

### Problem 5 — Only 58 posts (thin dataset for research)
The scraper ran but collected only 58 posts. The Reddit scraper (`sentimap_scraper_v2.py`) uses public `.json` endpoints (no API key needed — Reddit's Responsible Builder Policy killed self-service API keys in November 2025). The scraper had connection timeouts during runs. Need a successful full scrape run to get 200-400 relevant posts.

**Scraper runs with:**
```bash
cd D:\PROJECTS\SentiMap
backend\venv\Scripts\activate
python sentimap_scraper_v2.py
```
Outputs `reddit_data_v2.xlsx` + `reddit_data_v2.json` then migrates to Supabase.

---

## SUPABASE DATABASE SCHEMA

**Table: `posts`**
```
id              text (primary key — Reddit post ID)
title           text
body            text (post body — currently underused by NLP)
full_text       text (title + body combined — what NLP SHOULD run on)
created_date    date
upvotes         integer
num_comments    integer
url             text
locations       text (extracted Cebu location names, comma-separated)
comments_text   text (top 5 comments concatenated — rich Bislish source)
is_relevant     boolean
platform        text ← currently "unknown" for all, should be "reddit"
```

**Supabase connection:**
```python
SUPABASE_URL = "https://xbdhvpjhhvopatmyeubb.supabase.co"
# Key stored in backend/app/.env
```

---

## BACKEND API ENDPOINTS

| Endpoint | Status | Returns |
|---|---|---|
| `GET /health` | ✅ Working | Service health check |
| `GET /api/data` | ✅ Working | 58 posts with NLP enrichment |
| `GET /api/heatmap` | ✅ Working | 12 location clusters (coords partly wrong) |
| `GET /api/stats` | ✅ Working | Sentiment breakdown |
| `GET /api/locations` | ✅ Working | 20 known Cebu locations |
| `GET /api/analyze?text=` | ✅ Working | Test NLP on custom text |

---

## NLP MODULES

**`cebuano_lexicon.py`** (320+ lines)
- 50+ Cebuano/Bislish sentiment terms
- Sarcasm markers: "hayahay", "maayo jud", "perfect gyud"
- Traffic-specific terms: enforcers, checkpoints, violations

**`sentiment_analyzer.py`**
- Lexicon-based scoring (-1.0 to 1.0)
- Sarcasm detection (pattern matching)
- Confidence scoring

**`location_extractor.py`**
- Keyword-based NER for Cebu locations
- Word boundary matching
- Returns list of location names

**Known NLP limitations:**
- No ML classifier yet (pure lexicon/rule-based)
- Sarcasm detection 0% on real data (needs body text, not just titles)
- Location coords incomplete in geospatial.py

---

## WHAT TO DO IN THIS SESSION — PRIORITY ORDER

### IMMEDIATE FIXES (get the dashboard working today):

**Step 1 — Fix platform field in Supabase**
Run in Supabase SQL Editor:
```sql
UPDATE posts SET platform = 'reddit' WHERE platform IS NULL OR platform = 'unknown';
```

**Step 2 — Remove Facebook from frontend**
- Remove `FACEBOOK` button from the platform filter UI
- Remove any Facebook-related logic from frontend components
- Keep only: `ALL` | `REDDIT` (or just remove the filter entirely since everything is Reddit)
- Update backend to not reference platform filtering

**Step 3 — Fix geospatial.py coordinate dictionary**
Add all missing Cebu location coordinates listed above so pins appear correctly on the map instead of stacking at center.

**Step 4 — Fix frontend stats (0 counts)**
Audit the frontend component that renders REPORTS/SEVERE/SARCASTIC/HOTSPOTS against the actual `/api/data` and `/api/stats` response schemas. Fix field name mismatches.

**Step 5 — Switch NLP to use full_text**
In `main.py`, change all three endpoints (`/api/data`, `/api/stats`, `/api/heatmap`) from `record['title']` to `record.get('full_text') or record.get('title', '')`.

### AFTER FIXES (improve the system):

**Step 6 — Re-run scraper for more data**
Run `sentimap_scraper_v2.py` on stable internet to get 200-400 posts. Upload new data to Supabase. The `full_text` column will then give NLP real paragraph-length Bislish text to work with.

**Step 7 — Tighten keyword filter in scraper**
Remove standalone location names from `KEEP_KEYWORDS` — they cause off-topic posts (lechon, beach photos, relationship posts) to pass the filter. Only keep actual traffic/enforcement terms.

---

## SUGGESTIONS TO MAKE THE SYSTEM BETTER

These are architectural improvements that would significantly strengthen SentiMap both as a research tool and as a demo:

**1. Add `sentiment_score` and `sentiment_label` columns to Supabase**
Currently NLP runs on every API request (slow, inefficient). Pre-compute sentiment scores and store them in the database. Then `/api/stats` is just a SQL query instead of re-running NLP on every load.

**2. Add a `run_nlp_batch.py` script**
A one-time script that processes all posts in Supabase, computes sentiment + locations, and writes results back to the database. Run it once after each scrape. This makes your API fast and your research results reproducible.

**3. Fix the heatmap radius logic**
Currently "Cebu City" has 50 posts and a radius of 4213 meters — that's huge and covers the entire city. Specific locations like IT Park (4 posts) have radius 580m. The generic "Cebu City" bucket is polluting the heatmap. Consider capping its radius or filtering it out of the visualization entirely, since it's a fallback not a real location.

**4. Add post body to Supabase properly**
Many posts currently have empty `body` fields in Supabase because the original scraper only grabbed titles. After re-scraping with `sentimap_scraper_v2.py`, make sure `body` and `comments_text` columns are populated. These are the richest sources of Bislish text.

**5. Rename dashboard header metrics to be accurate**
- `REPORTS` → total posts count (fine)
- `SEVERE` → posts with `sentiment_label = "negative"` (make sure this matches)
- `SARCASTIC` → posts with `sarcasm_detected = true` (will be 0 until NLP uses full_text)
- `HOTSPOTS` → count of unique locations with 2+ posts (not total clusters)

**6. Remove or fix the TIMEFRAME filter (1H / 6H / 24H)**
Your data is historical Reddit posts, not a live feed. The 1H/6H/24H filters make no sense for this dataset — everything is months or years old. Either remove these filters, or relabel them as date range filters (e.g., "Past Month" / "Past Year" / "All Time") that filter by `created_date`.

**7. Add a data quality indicator to the dashboard**
Show researchers something like: "58 posts | 2021-2026 | 12 locations detected". This is important for your research paper's methodology section and makes the system more credible.

**8. Consider removing the "LIVE" indicator**
The top-right shows "● LIVE" which implies real-time data ingestion. Your system is not live — it's a batch-processed dataset. This is misleading for a research context. Replace with "● LOADED" or "● 58 POSTS" or just remove it.

---

## FILES TO SHARE AT START OF SESSION

To help the AI give you exact code fixes, share these files:
1. `frontend/app/page.tsx` (or whatever renders the main dashboard)
2. `backend/app/geospatial.py`
3. `backend/app/main.py` (already shared but share again for context)

---

## RESEARCH PAPER CONTEXT

- **Title:** Geospatial Sentiment Analysis: A Hybrid NLP Approach for Mapping Traffic Enforcement Grievances in Cebu City
- **Core contribution:** First system to handle Bislish (Cebuano-English code-switching) + sarcasm in geospatial traffic analysis
- **Key challenge addressed:** "Language-Context Gap" — standard tools (VADER, TextBlob) fail on informal Cebuano
- **Example sarcasm case:** "Hayahay kaayo ang traffic!" (literally positive, contextually negative)
- **Data source:** r/Cebu subreddit (public Reddit posts)
- **Target users:** Cebu City traffic authorities, urban planners

---

*Generated April 13, 2026 — SentiMap session handoff*