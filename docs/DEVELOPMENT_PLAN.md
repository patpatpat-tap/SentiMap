# SentiMap Development Plan

## Phase 1: NLP Engine Foundation ✅ COMPLETE
- ✅ Create Cebuano Sentiment Lexicon (custom dictionary for slang, sarcasm)
- ✅ Build Sentiment Analyzer module (lexicon-based + sarcasm detection)
- ✅ Build Location Extractor module (Cebu City locations)
- ✅ Integrate into FastAPI `/api/data` endpoint

## Phase 2: Backend Enhancement ✅ COMPLETE
- ✅ Extend API response schema to include:
  - `sentiment_score`: float (-1 to 1)
  - `sentiment_label`: "negative" | "positive" | "neutral"
  - `locations`: array of extracted Cebu City locations
  - `sarcasm_detected`: boolean
- ✅ Add `/api/stats` endpoint for aggregated statistics
- ✅ Add `/api/analyze` endpoint for text testing
- ✅ Add `/api/locations` endpoint for location reference

## Phase 3: Frontend Enhancement ✅ COMPLETE
- ✅ Update SentiMap Dashboard component to display:
  - Sentiment badges on Grievance Cards
  - Location tags
  - Sarcasm indicators
- ✅ Add filtering by sentiment/location
- ✅ Add statistics panel (totals, sentiment breakdown, sarcasm %)
- ✅ Responsive grid layout with emoji indicators

## Phase 4: Visualization & Polish 🔄 IN PROGRESS
- [ ] Integrate map visualization (Cebu City boundaries)
- [ ] Build heatmap layer showing grievance density by location
- [ ] Add interactive location filtering
- [ ] Performance optimization

---

## Current Status ✅ FULLY FUNCTIONAL

### Backend Capabilities:
- **NLP Pipeline**: Sentiment analysis + location extraction on all grievances
- **REST API**: 5 endpoints fully operational
  - GET `/api/data` - All grievances with NLP enrichment
  - GET `/api/stats` - Aggregated statistics  
  - GET `/api/analyze` - Test NLP on custom text
  - GET `/api/locations` - All known Cebu locations

### Data Insights (from 105 Reddit grievances):
- Total Grievances: 105
- Sentiment Breakdown: 66 negative (63%), 36 neutral (34%), 3 positive (3%)
- Avg Sentiment Score: -0.49 (mostly negative)
- Sarcasm Detection: 0% (currently tuned for explicit sarcasm)
- Top Locations: Cebu City (38), SRP (4), Talamban (3)

### Frontend Capabilities:
- Sentiment filtering (All/Negative/Neutral/Positive)
- Location display on cards
- Sarcasm badges
- Statistics dashboard
- Responsive design (mobile-first)
