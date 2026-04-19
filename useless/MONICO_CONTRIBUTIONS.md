# SentiMap Research Contributions — Monico (The Backend)

**Role:** Backend Architect, Database Designer, Geolocation Module Developer, API Developer

---

## PART 2 — MAJOR CONTRIBUTION

**What did I contribute?**

I designed and built the entire backend infrastructure that powers the SentiMap system. This includes three major components:

1. **Database Architecture** — Designed the Supabase database schema to store posts with all metadata (content, timestamps, scores, etc.). Implemented proper data relationships, indexing for fast queries, and Row-Level Security (RLS) policies to protect data integrity.

2. **Geolocation Module** — Developed a custom module that automatically extracts geographic locations from raw post text. When a post mentions "traffic at Escario near the IT Park," the system parses it and extracts ["Escario", "IT Park", "Cebu City"]. This geographic data powers the interactive map visualization.

3. **API Layer** — Built 5 production-ready REST API endpoints:
   - `/api/data` — Returns posts with enriched analysis
   - `/api/stats` — Returns aggregated statistics and summaries
   - `/api/heatmap` — Returns geospatial visualization data
   - `/api/analyze` — Processes custom text input
   - `/api/locations` — Lists identified geographic areas

These endpoints serve as the communication bridge between the database and frontend.

**Why was this important?**

Data infrastructure is the invisible backbone of any application. Without it:
- Data would have nowhere to be stored reliably
- There would be no way to retrieve or query information
- Geographic extraction wouldn't work (map would be empty)
- Frontend would have no API endpoints to call
- Users would see a broken, non-functional application
- System wouldn't scale beyond manual, one-off data access

The backend transforms raw data into an accessible, queryable, usable system.

**What would happen if this contribution was missing?**

Without the backend:
- Database structure would be disorganized, leading to slow queries and data loss
- Geolocation extraction wouldn't happen (locations wouldn't be tagged)
- No APIs means no way for the frontend to access any data
- Frontend application would be completely non-functional
- Interactive map couldn't render without geospatial data
- Statistics couldn't be calculated without aggregation endpoints
- The entire project would be just files, not a working application

---

## PART 3 — PROBLEM SOLVING

**Problem encountered:**

Posts contain location information written in natural language with variations, typos, informal references, and context dependencies. How do you automatically extract geographic locations from unstructured text reliably? Example: A post might say "traffic at the intersection near Ayala, close to the bridge near Cebu Business Park" — the system needs to recognize this mentions multiple specific locations and extract them accurately for geospatial mapping.

**What did I try first?**

Simple exact string matching: Keep a list of 37 Cebu neighborhoods and search for exact matches in each post. If "Talisay" appears in the text, extract "Talisay."

**What did not work?**

Exact matching failed because:
- Users misspell locations ("Osmena" instead of "Osmeña")
- Users use informal names ("the mall" instead of "SM City Cebu")
- Same location has multiple names ("Cebu Business Park," "CBD")
- Context matters ("near the corner" — near what corner?)
- Multiple locations in one sentence weren't properly separated

**Final solution:**

I built a geolocation extraction module that:
- Uses fuzzy string matching to handle typos and spelling variations
- Maintains a mapping of alternate names for locations ("CBD" → "Cebu Business Park")
- Extracts locations contextually using window-based parsing
- Normalizes variations to canonical location names
- Links each extracted location to latitude/longitude coordinates for mapping

Result: Posts are automatically tagged with accurate geographic locations that can be plotted on the interactive map with high accuracy.

---

## PART 4 — TIME CONTRIBUTION

| Activity | Hours Spent |
|----------|-------------|
| Database schema design and architecture | 1.5 hours |
| Geolocation module development and testing | 2 hours |
| API endpoint design and implementation | 1.5 hours |
| Testing API performance and reliability | 1 hour |
| Database indexing and optimization | 0.75 hours |
| Error handling and edge cases | 0.5 hours |
| API documentation | 0.5 hours |
| Integration testing and deployment | 0.75 hours |
| **Total Hours:** | **~9 hours** |

---

## PART 5 — DECISION PARTICIPATION

**Decision Topic:**

What database platform and backend architecture should support the application? Should we use traditional SQL with custom deployment, managed services, or a hybrid approach?

**My Recommendation:**

Use a managed database service (Supabase, which is PostgreSQL) combined with a FastAPI backend. Store data in managed Supabase, build custom Python logic in FastAPI for geolocation extraction and data processing, expose everything through REST APIs.

**Reason for my recommendation:**

Managed services reduce infrastructure complexity (no server management), provide built-in authentication and data protection features, scale automatically, and allow focus on business logic instead of DevOps. Hybrid approach separates database concerns (Supabase) from application logic concerns (FastAPI).

**Outcome of decision:**

This architecture proved reliable and performant. API response times <500ms, database handles queries efficiently, and the geolocation module integrates cleanly. System can scale without architectural changes.

---

## PART 6 — TEAM CONTRIBUTION AWARENESS

**Team Structure:**

The project consists of distinct technical layers, each requiring expertise:

1. **Research & Data Layer** — Responsibility for data collection, validation, and quality assurance
2. **Backend & Infrastructure Layer** — My responsibility: database design, API development, geolocation extraction
3. **Frontend & UI Layer** — Responsibility for user interface, visualization, user experience

Each layer is independent but interconnected. The backend receives inputs from the research layer and outputs to the frontend layer.

---

## PART 7 — CONTRIBUTION PERCENTAGE

| Contributor | Contribution % |
|------------|-----------------|
| Research & Data Layer | 50% |
| Backend & Infrastructure (Monico) | 35% |
| Frontend & UI Layer | 15% |
| **Total** | **100%** |

Backend infrastructure represents the core technical complexity. Database design, API architecture, and geolocation extraction are critical to system functionality.

---

## PART 8 — MEETING PARTICIPATION

**Meetings:** Technical architecture reviews, database design meetings, API performance reviews, integration testing sessions

**Most recent contribution in a meeting:**

Presented the backend architecture, explained the geolocation extraction approach, and demonstrated API response times. Discussed how the database is structured to support efficient queries.

**Action item assigned:**

Ensure the backend infrastructure scales properly as data volume increases. Monitor API response times and optimize database queries as needed.

---

## PART 9 — SELF REFLECTION

**What part of the project depended most on me?**

Data accessibility and scalability. The system needs to reliably store large datasets, extract geographic information, and serve that data to users through APIs. Without solid backend architecture, the application wouldn't function.

**What did I learn from this project?**

- Database schema design decisions impact every downstream query performance
- Geolocation extraction requires both rule-based and fuzzy matching approaches
- REST API design should prioritize response time and data efficiency
- Managed services reduce infrastructure complexity but require understanding their constraints
- Small optimizations in database indexing can reduce API response time by 5-10x
- Proper error handling in APIs prevents cascading failures

**What should I have contributed more?**

Caching layer for frequently requested data. Without caching, every API request recalculates results. Adding Redis or similar would reduce response times significantly and lower database load. Also should have implemented more comprehensive monitoring to catch performance issues earlier.

---

**Project Status:** ✅ Backend fully functional. Database architecture solid. All APIs operational. Geolocation extraction working reliably. System ready for production use.
