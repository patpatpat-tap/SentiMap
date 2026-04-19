# SentiMap Project Objective & System Architecture

**Last Updated:** April 19, 2026  
**Status:** ✅ FULLY OPERATIONAL  
**GitHub:** https://github.com/patpatpat-tap/SentiMap

---

## PROJECT OBJECTIVE

**Goal:** Analyze Reddit sentiment about traffic enforcement in Cebu City to identify community grievances, geographic hotspots, and sentiment trends that can inform policy decisions.

**Research Question:** What is the sentiment of Cebu residents toward traffic enforcement, and where are the geographic clusters of complaints?

**Target Audience:** City government (CITOM, LTO, LTFRB), policy makers, traffic enforcement agencies, academic researchers

**Output:** Production-ready dashboard with 736 validated posts, sentiment analysis, geospatial heatmaps, and statistical summaries

---

## SYSTEM ARCHITECTURE

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Collection** | Python + PRAW (Reddit API) | Scrape Reddit posts |
| **Data Processing** | Python + Pandas | Clean, merge, deduplicate |
| **Database** | Supabase (PostgreSQL) | Store 736 posts + metadata |
| **Backend API** | FastAPI + Uvicorn | Serve NLP-enriched data |
| **NLP Engine** | Custom lexicon-based | Sentiment, sarcasm, location extraction |
| **Frontend** | Next.js 16 + React | Interactive dashboard |
| **Visualization** | Leaflet.js | Geospatial mapping |

### Data Flow Pipeline

```
PHASE 1: COLLECTION (30-40 minutes)
├─ sentimap_scraper_godmode.py
├─ Targets: r/Cebu, r/Philippines, r/CebuCity
├─ Method: 29 targeted searches (not just hot/top/new)
├─ Output: reddit_godmode.json (711 posts)
└─ Filtering: 2-layer (CORE keywords + relevance_score >= 2)

PHASE 2: INTEGRATION (5 minutes)
├─ merge_godmode_data.py
├─ Input: 58 v2 posts + 711 godmode posts
├─ Process: Normalize fields → Deduplicate (33 removed) → Validate
├─ Output: reddit_data_v3_clean.csv (736 posts)
└─ Quality: 95% relevance, avg score 4.68/21

PHASE 3: DATABASE (2 minutes)
├─ import_to_supabase_simple.py
├─ Method: Supabase REST API (8 batches × 100)
├─ Auth: Service role key (sb_secret_*)
├─ Output: 736 posts in Supabase.posts table
└─ Schema: id, title, body, locations, url, created_date, etc.

PHASE 4: API SERVER (Real-time)
├─ backend/app/main.py (FastAPI)
├─ Endpoints: /api/data, /api/stats, /api/heatmap, /api/analyze, /api/locations
├─ Processing: NLP enrichment per request
├─ Performance: <500ms response time
└─ Modules: sentiment_analyzer.py, location_extractor.py

PHASE 5: VISUALIZATION (Browser)
├─ frontend/app/page.tsx (Next.js)
├─ Components: GrievanceFeed, SentiMapMap (Leaflet), StatsBar
├─ Proxy: next.config.ts rewrites /api/* to backend
└─ Output: Interactive dashboard at http://localhost:3000
```

---

## CORE INNOVATION: 2-LAYER FILTERING

### Why It Matters

**Problem:** Original v2 scraper accepted posts based solely on location name mentions (e.g., "Talisay" in lechon recipes). Result: 58 noisy posts, ~30% relevant.

**Solution:** Implemented intelligent 2-layer filtering to separate signal from noise.

### Layer 1: CORE Keywords (Mandatory Gate)

Post MUST contain at least ONE of these unambiguous traffic enforcement terms:

**Agencies:** CITOM, LTO, LTFRB, CCTO, MMDA

**Traffic Enforcement:** checkpoint, traffic enforcer, traffic enforcement, apprehended, citation, violation

**Specific Violations:** reckless driving, counterflow, cornering violations, smoke belching, illegal parking

**Transport Grievances:** jeepney, taxi driver, taxi meter, overcharging, commute, public transport, grab driver, angkas driver

**Cebuano/Bislish:** sakay jeep, drayber na bastos, bouncer salot, traffic enforcer na salot, colorum

### Layer 2: Relevance Scoring (0-21 Points)

Posts passing Layer 1 get scored based on keyword density and importance:

| Keyword | Weight | Category |
|---------|--------|----------|
| hayahay | +3 | Sarcasm marker (high research value) |
| salot | +3 | Cebuano criticism term |
| namatay ko | +2 | Extreme complaint expression |
| CITOM | +2 | Specific enforcement agency |
| checkpoint | +2 | Enforcement action |
| traffic | +1 | Generic traffic mention |
| commute | +1 | Transport term |

**Minimum threshold:** Score must be ≥ 2 to be kept in dataset

**Result:** 711 new posts, 95% relevant (vs 30% in old scraper)

---

## TEAM ROLES & CONTRIBUTIONS

### Patrick (The Brains: 60%)
- **Role:** Project Leader, Research Director, NLP Architect
- **Contributions:**
  - Designed 2-layer filtering strategy
  - Built custom Cebuano Sentiment Lexicon
  - Architected data scraping strategy (29 targeted queries)
  - Created hybrid NLP engine
  - Led research methodology decisions
- **Deliverables:** 
  - sentimap_scraper_godmode.py (711 posts)
  - merge_godmode_data.py (736 posts deduplicated)
  - 2-layer filtering logic
  - Lexicon definitions
  - Research documentation

### Monico (The Backend: 40%)
- **Role:** Backend Architect, Database Designer, API Developer
- **Contributions:**
  - Designed Supabase database schema
  - Built geolocation extraction module
  - Created 5 REST API endpoints
  - Implemented data access layer
  - Handled authentication/RLS
- **Deliverables:**
  - backend/app/main.py (FastAPI server)
  - Geolocation parser (extracts locations from text)
  - 5 production API endpoints
  - Database architecture

---

## CURRENT STATUS

### ✅ COMPLETED

- [x] Godmode scraper with 2-layer filtering (711 posts)
- [x] Dataset merge & deduplication (736 posts final)
- [x] Supabase database import (all 736 posts)
- [x] FastAPI backend with 5 endpoints
- [x] NLP enrichment (sentiment + sarcasm + location)
- [x] Next.js frontend dashboard
- [x] Interactive Leaflet map with heatmaps
- [x] Complete documentation (700+ lines)
- [x] GitHub deployment
- [x] Research Q&A documentation (3 formats)
- [x] Team contribution documentation

### 📊 DATA METRICS

| Metric | Value |
|--------|-------|
| Total posts | 736 |
| From v2 scraper | 58 |
| From godmode scraper | 711 |
| Duplicates removed | 33 |
| Avg relevance score | 4.68/21 |
| Unique Cebu locations | 37 |
| Sentiment positive | 27% (196 posts) |
| Sentiment neutral | 49% (363 posts) |
| Sentiment negative | 24% (177 posts) |
| Sarcasm detected | 6% (42 posts) |

---

## API ENDPOINTS

### 1. `/api/data` - All Posts with NLP
```
GET http://127.0.0.1:8000/api/data
Response: Array of 736 posts with sentiment, sarcasm, locations
Time: 3-5 minutes (processes NLP for all posts)
```

### 2. `/api/stats` - Statistics Summary
```
GET http://127.0.0.1:8000/api/stats
Response: Sentiment breakdown, top locations, sarcasm %, avg sentiment
Time: <500ms
```

### 3. `/api/heatmap` - Geospatial Data
```
GET http://127.0.0.1:8000/api/heatmap
Response: Location coordinates, sentiment clusters, severity markers
Time: <500ms
```

### 4. `/api/analyze` - Analyze Custom Text
```
GET http://127.0.0.1:8000/api/analyze?text=<text>
Response: Sentiment score, sarcasm flag, locations, keywords matched
Time: <1 second
```

### 5. `/api/locations` - Location List
```
GET http://127.0.0.1:8000/api/locations
Response: All 37 Cebu neighborhoods identified
Time: <100ms
```

---

## CRITICAL DECISION POINTS

### Decision 1: Keep v2 Data or Start Fresh?
**Choice:** Keep all 58 v2 posts + add 711 new godmode posts → 736 total

**Reasoning:** Preserves existing data, avoids data loss, larger sample size for research

**Result:** Better statistical power while maintaining original dataset

### Decision 2: How to Filter for Quality?
**Choice:** Implement 2-layer filtering (mandatory keywords + relevance scoring)

**Reasoning:** Location-only filtering creates noise; keyword + scoring removes false positives

**Result:** Increased data quality from 30% to 95% relevant

### Decision 3: Database + Backend Architecture?
**Choice:** Use Supabase (managed) + FastAPI (custom logic)

**Reasoning:** Reduced DevOps overhead, clear separation of concerns, scalable

**Result:** Reliable API performance (<500ms), easy to maintain

### Decision 4: NLP Approach?
**Choice:** Custom lexicon-based (not ML models)

**Reasoning:** Cebuano/Bislish text requires domain knowledge; lexicon is interpretable for research

**Result:** Transparent methodology, academic reviewable, works without large training data

---

## HOW TO CONTINUE / COMPLETE PROJECT

### If Adding More Data:
1. Run scraper again (auto-skips existing posts)
2. Merge new + existing
3. Import to Supabase
4. Backend auto-serves new data

### If Improving NLP:
1. Add more keywords to `CORE_KEYWORDS` and `BONUS_KEYWORDS` in scraper
2. Adjust scoring weights
3. Re-run scraper and merge
4. Backend will use updated lexicon

### If Deploying to Production:
1. Move `.env` credentials to environment variables
2. Use production Supabase project
3. Deploy FastAPI to cloud (Heroku, Railway, Render)
4. Deploy Next.js to Vercel
5. Add caching layer (Redis) for performance

### If Publishing Research:
1. Use RESEARCH_QUESTIONS_SUMMARIZED.md for methodology
2. Include: data collection strategy, filtering logic, sample size (736)
3. Cite: 2-layer approach, keyword list, relevance scoring
4. Data available: reddit_data_v3_clean.csv in GitHub

---

## IMPORTANT INFORMATION FOR AI/IDE ASSISTANCE

### Code Organization
- **Root scripts:** sentimap_scraper_godmode.py (main scraper)
- **Backend:** `backend/app/` contains all API logic
- **NLP:** `backend/app/sentiment_analyzer.py` + `backend/app/location_extractor.py`
- **Frontend:** `frontend/app/` contains Next.js pages/components
- **Data:** `backend/data/` contains all CSV/JSON files
- **Scripts:** `backend/scripts/` contains utilities (merge, import)

### Key Files to Reference
- `GODMODE_IMPLEMENTATION.md` - Complete technical documentation (700+ lines)
- `IMPLEMENTATION_SUMMARY.md` - Quick reference version
- `RESEARCH_QUESTIONS_SUMMARIZED.md` - Research methodology explanation
- `PATRICK_CONTRIBUTIONS_V2.md` - Patrick's role & contributions
- `MONICO_CONTRIBUTIONS.md` - Monico's role & contributions

### Known Limitations
- `/api/data` endpoint is slow (3-5 min) because it processes NLP on all 736 posts per request
  - **Solution:** Implement caching or pre-compute NLP during import
- Geolocation extraction uses simple fuzzy matching, not ML
  - **Accuracy:** ~90% for common location names
- Sentiment lexicon is domain-specific to Cebu traffic
  - **Reuse:** Not applicable to other regions without adaptation

### Database Schema (Supabase)
```sql
posts (
  id TEXT PRIMARY KEY,
  title TEXT,
  body TEXT,
  full_text TEXT,
  created_date TIMESTAMP,
  upvotes INTEGER,
  num_comments INTEGER,
  url TEXT,
  locations TEXT[] (array of neighborhood names),
  comments_text TEXT,
  is_relevant BOOLEAN
)
```

### Environment Variables Needed
```
SUPABASE_URL=https://xbdhvpjhhvopatmyeubb.supabase.co
SUPABASE_KEY=sb_secret_TElydENOMJQOos9yfPSDIg_xd5ioeE6
```

---

## QUICK START FOR NEW CONTRIBUTORS

### Setup
```powershell
# Clone repo
git clone https://github.com/patpatpat-tap/SentiMap.git
cd SentiMap

# Backend setup
cd backend
python -m venv venv
..\backend\venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
```

### Run System
```powershell
# Terminal 1: Backend
cd backend
..\backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Access
- Dashboard: http://localhost:3000
- API: http://127.0.0.1:8000/api/stats

---

## SUCCESS CRITERIA (All Met ✅)

- [x] Collect 500+ high-quality posts about Cebu traffic (736 collected)
- [x] Implement intelligent filtering to remove noise (2-layer system)
- [x] Build database to store posts (Supabase with 736 posts)
- [x] Create API to serve data (5 endpoints, all working)
- [x] Build interactive dashboard (Next.js with map + stats)
- [x] Document methodology (3 documentation files + GitHub)
- [x] Deploy to GitHub (all code + data public)
- [x] Make system reproducible (can rerun scraper anytime)

---

## NEXT PHASE OPPORTUNITIES

### Phase 2: Enhancement
- [ ] Implement caching for `/api/data` (3-5 min → <1 sec)
- [ ] Add pagination (load 50 posts at a time)
- [ ] Scheduled scraping (weekly automated updates)
- [ ] Export to PDF/Excel reports
- [ ] Real-time sentiment trends

### Phase 3: Research Impact
- [ ] Publish academic paper (methodology + findings)
- [ ] Present to Cebu City government
- [ ] Policy recommendations based on data
- [ ] Expand to other Philippine cities
- [ ] Compare enforcement sentiment across regions

### Phase 4: ML Enhancement
- [ ] Train ML sentiment model vs lexicon baseline
- [ ] Fine-tune on Cebuano-specific data
- [ ] Implement Cebuano NER (Named Entity Recognition)
- [ ] Multi-label classification (multiple grievance types)

**For any questions about the system, refer to this document first. For detailed implementation steps, see IMPLEMENTATION_SUMMARY.md or GODMODE_IMPLEMENTATION.md.**
