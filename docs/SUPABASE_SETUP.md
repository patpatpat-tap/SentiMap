# SentiMap Backend → Supabase Setup Guide

## What Was Created

1. **`.env`** - Environment variables with your Supabase credentials
2. **`supabase_client.py`** - Reusable Supabase client module
3. **`main_supabase.py`** - Updated FastAPI backend using Supabase

## Installation & Setup

### Step 1: Install python-dotenv

```powershell
cd d:\PROJECTS\SentiMap\backend\venv
.\Scripts\python.exe -m pip install python-dotenv
```

### Step 2: Verify .env File

Check that `d:\PROJECTS\SentiMap\backend\venv\.env` contains:

```
SUPABASE_URL=https://xbdhvpjhhvopatmyeubb.supabase.co
SUPABASE_KEY=sb_publishable_7exwi-Ym62ER0i6hqtaDbw_juD2aU02
ENVIRONMENT=development
```

### Step 3: Switch to Supabase-Enabled Backend

**Option A: Replace main.py (recommended)**
```powershell
cd d:\PROJECTS\SentiMap\backend\venv

# Backup old main.py
Copy-Item main.py main_excel.py.bak

# Use the new Supabase version
Copy-Item main_supabase.py main.py
```

**Option B: Keep Both (test first)**
- Run `main_supabase.py` to test
- If working, then replace `main.py`

### Step 4: Run the Backend

```powershell
cd d:\PROJECTS\SentiMap\backend\venv
.\Scripts\python.exe -m uvicorn main:app --reload
```

You should see:
```
✓ Supabase client initialized for https://xbdhvpjhhvopatmyeubb.supabase.co
INFO:     Application startup complete
Uvicorn running on http://127.0.0.1:8000
```

---

## Testing the Endpoints

### 1. Health Check
```
http://127.0.0.1:8000/health
```

### 2. Get All Data
```
http://127.0.0.1:8000/api/data
```
Should return 58 posts from Supabase with NLP analysis.

### 3. Get Heatmap
```
http://127.0.0.1:8000/api/heatmap
```
Should return heat zones for Leaflet map.

### 4. Get Statistics
```
http://127.0.0.1:8000/api/stats
```
Should return sentiment breakdown and location stats.

---

## How It Works

**Before (Excel):**
```
Frontend → FastAPI → read_excel() → /data response
```

**After (Supabase):**
```
Frontend → FastAPI → supabase_client.get_all_posts() → /data response
         ↑                                    ↑
      Port 3000                      Port 5432 (PostgreSQL)
```

**All endpoints now:**
- Query from Supabase `posts` table (58 records)
- Enrich with NLP analysis (sentiment, sarcasm, locations)
- Return same JSON format to frontend (no frontend changes needed!)

---

## Next Steps

### 1. Extract NER Locations (Optional)
After the backend is running, populate the `locations` column in Supabase:

```python
# Create a script to run NER on all posts and update locations
# Use: location_extractor.extract() on each full_text
# Then: supabase_client.update_locations(id, locations_str)
```

### 2. Verify Frontend Still Works
- Run: `npm run dev` in `frontend/`
- Frontend should automatically query the new Supabase backend
- No code changes needed (same API contract!)

### 3. Production Deployment
- Use environment variables on your hosting platform
- Never commit `.env` to GitHub (already in .gitignore)
- Use `SERVICE_ROLE_KEY` for backend operations (more secure)

---

## Troubleshooting

**Error: "Supabase client not initialized"**
- Check `.env` file exists and has correct credentials
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are not empty

**Error: "No posts found in Supabase"**
- Verify data was imported successfully in Supabase dashboard
- Check that `posts` table has 58 rows

**Error: Connection timeout**
- Check your internet connection
- Verify Supabase service is running (check supabase.com status)

---

## Files Used

- ✅ `d:\PROJECTS\SentiMap\backend\venv\.env` - Credentials
- ✅ `d:\PROJECTS\SentiMap\backend\venv\supabase_client.py` - Client module
- ✅ `d:\PROJECTS\SentiMap\backend\venv\main_supabase.py` - New backend
- ⚠️ `d:\PROJECTS\SentiMap\backend\venv\main.py` - Keep as backup

---

## Architecture 

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                        │
│              Running on localhost:3000                       │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP Requests (CORS enabled)
                     ↓
┌─────────────────────────────────────────────────────────────┐
│            FastAPI Backend (main.py)                         │
│         Running on localhost:8000                            │
│                                                              │
│  • /api/data → Queries Supabase posts                        │
│  • /api/heatmap → Enriches with NLP, clusters              │
│  • /api/stats → Calculates sentiment stats                  │
│  • /health → Status check                                   │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API (REST v1)
                     ↓
┌─────────────────────────────────────────────────────────────┐
│               Supabase (PostgreSQL)                          │
│         https://xbdhvpjhhvopatmyeubb.supabase.co           │
│                                                              │
│   posts table (58 rows):                                     │
│   ├─ id, title, body, full_text                            │
│   ├─ created_date, upvotes, num_comments                   │
│   ├─ url, locations, comments_text                         │
│   └─ is_relevant                                            │
└─────────────────────────────────────────────────────────────┘


   NLP Processing Layers:
   ┌─────────────────────┐
   │ Sentiment Analyzer  │  (Cebuano + Bislish + Sarcasm)
   │ Location Extractor  │  (Cebu City locations)
   │ Geospatial Cluster  │  (Heat zones for heatmap)
   └─────────────────────┘
```

---

**Ready to go!** 🚀 Run the backend and it will connect to your Supabase database automatically.
