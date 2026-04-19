# SentiMap Godmode — Quick Implementation Summary

**Status**: ✅ FULLY OPERATIONAL  
**Data**: 736 Posts (58 v2 + 711 godmode)  
**Backend**: http://127.0.0.1:8000  
**Frontend**: http://localhost:3000

---

## The Problem & Solution

**Old Scraper (v2):** Only 58 posts, many false positives (lechon recipes, vacation photos)

**New Scraper (Godmode):** 711 posts using 2-layer intelligent filtering:
- **Layer 1:** Post must contain actual traffic keywords (CITOM, checkpoint, etc.)
- **Layer 2:** Post scored on relevance (must reach 2+ points)

**Result:** 736 total high-quality posts, ~95% relevant

---

## Quick Start

### Backend
```powershell
cd D:\PROJECTS\SentiMap\backend
..\backend\venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Frontend
```powershell
cd D:\PROJECTS\SentiMap\frontend
npm run dev
```

**Access:** http://localhost:3000

---

## Data Pipeline

```
1. Scrape Reddit (30-40 min)
   → sentimap_scraper_godmode.py
   → Output: reddit_godmode.json (711 posts)

2. Merge Datasets
   → merge_godmode_data.py
   → Combines v2 + godmode, removes 33 dupes
   → Output: reddit_data_v3_clean.csv (736 posts)

3. Import to Database
   → import_to_supabase_simple.py
   → Uses service role key to bypass RLS
   → Output: 736 posts in Supabase

4. Serve via API
   → FastAPI backend
   → 5 endpoints: /api/data, /api/stats, /api/heatmap, /api/analyze, /api/locations

5. Display on Dashboard
   → Next.js frontend
   → Shows posts with sentiment badges, locations, interactive map
```

---

## Commands Reference

**Install dependencies:**
```powershell
pip install requests pandas openpyxl supabase python-dotenv
```

**Run scraper:**
```powershell
cd D:\PROJECTS\SentiMap
python sentimap_scraper_godmode.py
```

**Merge data:**
```powershell
cd D:\PROJECTS\SentiMap\backend\scripts
python merge_godmode_data.py
```

**Import to Supabase:**
```powershell
cd D:\PROJECTS\SentiMap
python backend\scripts\import_to_supabase_simple.py
```

---

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/api/data` | All posts with sentiment analysis |
| `/api/stats` | Sentiment breakdown, top locations |
| `/api/heatmap` | Geospatial data for map |
| `/api/analyze?text=...` | Analyze custom text |
| `/api/locations` | List all 37 Cebu neighborhoods |

---

## Key Features

- **2-Layer Filtering:** CORE keywords (mandatory) + Relevance scoring
- **29 Targeted Searches:** Not just top/hot/new
- **Crash Recovery:** Auto-saves progress every 10 posts
- **NLP Enrichment:** Sentiment analysis + sarcasm detection + location extraction
- **Geospatial Mapping:** Interactive Leaflet map with heatmaps

---

## CORE Keywords (Layer 1)

**Enforcement:** CITOM, LTO, LTFRB, checkpoint, traffic enforcer  
**Transport:** jeepney, taxi, commute, angkas, overcharging  
**Violations:** reckless driving, counterflow, smoke belching, illegal parking  
**Cebuano:** sakay jeep, drayber salot, traffic enforcer na salot

---

## File Structure

```
sentimap_scraper_godmode.py          → Scraper (711 posts)
reddit_godmode.json                  → Scraper output
reddit_godmode_progress.json         → Crash checkpoint
│
backend/
├── app/main.py                      → API server
├── app/sentiment_analyzer.py        → NLP engine
├── app/location_extractor.py        → Geolocation module
├── scripts/merge_godmode_data.py    → Merge script
├── scripts/import_to_supabase_simple.py → Import script
└── data/reddit_data_v3_clean.csv    → Final 736 posts
│
frontend/
├── app/page.tsx                     → Dashboard
└── app/components/                  → React components
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | `pip install requests pandas openpyxl` |
| Backend won't start | Make sure you're in `backend/` directory |
| RLS policy error | Use service role key (sb_secret_*) |
| Frontend won't start | Run `npm install` then `npm run dev` |
| Scraper too slow | Normal — 2.5s delays between requests |

---

## Performance

| Metric | Value |
|--------|-------|
| Total posts | 736 |
| Scraper runtime | 30-40 minutes |
| Import time | ~2 minutes |
| Backend startup | <5 seconds |
| API response | <500ms |
| Avg relevance score | 4.68/21 |

---

## What's Different: Old vs New

| Feature | v2 | Godmode |
|---------|----|---------| 
| Posts | 58 | 711 |
| Filtering | Location only | 2-layer keywords + score |
| Searches | Top/hot/new | 29 targeted queries |
| Quality | ~30% | ~95% |
| Crash recovery | None | Every 10 posts |

---

## Next Steps

1. Backend running → API serves 736 posts with NLP enrichment
2. Frontend running → Dashboard displays everything
3. To update data → Run scraper → merge → import → done

**GitHub:** https://github.com/patpatpat-tap/SentiMap

---

**Last Updated: April 19, 2026**
