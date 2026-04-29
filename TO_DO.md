# My Actual Situation
You have 736 posts in Supabase. Your table is missing sentiment_score, sentiment_label, sarcasm_detected, and relevance_score columns. NLP runs live on every request which is why it takes 3-5 minutes. The God Mode scraper collected 711 posts which were merged with the original 58 into 736 after deduplication.
Thorough vs Fast Approach
Fast approach — 1 day of work. Pre-compute NLP on all 736 posts as-is, store in Supabase, fix the frontend. Dashboard works instantly. But dirty data remains — your numbers (severe, sarcastic, hotspots) are still partially wrong. Acceptable if you need something working quickly.
Thorough approach — 3-4 days of work. Clean the data first, then pre-compute NLP on only verified posts, then fix the frontend. Every number you show in your thesis is defensible. This is what I recommend for a thesis defense since your committee will ask about data validity.
Since you have time, we do the thorough approach. Here's the exact sequence:

# The Complete Plan — Step by Step (DONE THIS ALREADY)
# Step 1 — Add missing columns to Supabase

ALTER TABLE posts ADD COLUMN IF NOT EXISTS sentiment_score float;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS sentiment_label text;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS sarcasm_detected boolean DEFAULT false;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS sentiment_confidence float;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS relevance_score integer DEFAULT 0;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS is_clean boolean DEFAULT false;

# Step 2 — Build a data validation script (automated + manual) 
# I added 'data_validator.py' and 'nlp_batch_processor.py' in backend\scripts\
- data_validator.py for Data validation and cleaning script for SentiMap - auto-scores and flags posts for review
- nlp_batch_processor.py pre-computes sentiment for all clean posts and stores in supabase

Place data_validator.py in backend/scripts/ and run it:
cd D:\PROJECTS\SentiMap
backend\venv\Scripts\activate
python backend\scripts\data_validator.py

What happens: It loads all 736 posts and scores each one across four research dimensions — Enforcement signal, Transport grievance, Sentiment/Bislish value, and Location specificity. It auto-decides KEEP or DISCARD for most posts. Only the borderline ones (probably 80-120 posts) get shown to you for manual review. You just press K, D, or S for each one. Then it writes is_clean and relevance_score back to Supabase. It also saves a validation_report.xlsx so you have a documented record of every decision — which is exactly what your thesis methodology section needs.

Step 3 — Run the NLP Batch Processor
python backend\scripts\nlp_batch_processor.py

This runs NLP on full_text (title + body combined — the critical fix) for every post where is_clean = true, and stores sentiment_score, sentiment_label, sarcasm_detected directly in Supabase. After this runs, your API response time drops from 3-5 minutes to under 1 second because the backend just reads stored values instead of computing them live.
What You End Up With
After both scripts finish, your 736 posts become a validated, scored, NLP-enriched clean dataset. Your thesis numbers become defensible — you can say exactly how many posts you reviewed, what your validation criteria were, and what percentage passed. That's the difference between "we scraped 736 posts" and "we validated 736 posts against four research-relevance dimensions, retaining X posts with relevance scores above 6."

- Yes, it can be largely automated. Here's how it works — the script scores each post on multiple dimensions and auto-classifies it, then flags borderline cases for you to review manually. You only manually review the uncertain ones, not all 736.

# Step 3 — Pre-compute NLP on clean posts only
After cleaning, run NLP on full_text (not title) for every post marked is_clean = true. Store results in Supabase.
# Step 4 — Fix backend to read pre-computed values
# Step 5 — Fix frontend (remove Facebook, fix map, add pagination)


# What I'm Thinking the next Steps Are
Based on everything I know about SentiMap, here's what I believe the right sequence is — but I want your answers before committing to this:
Phase 1 — Data audit (do this first, everything else depends on it)
Build a script that loads all 736 posts from Supabase and runs them through a strict relevance check — stricter than the God Mode filter — and tags each post as relevant, borderline, or irrelevant. This gives you a number you can actually defend in your research paper.
Phase 2 — Clean Supabase
Delete or flag irrelevant posts. You probably end up with 350-500 clean posts. That's still a strong dataset for a research paper — quality matters more than quantity.
Phase 3 — Pre-compute NLP on clean data
Run sentiment analysis, sarcasm detection, and location extraction on full_text (title + body) for every clean post. Store results directly in Supabase columns. This fixes the loading time problem and makes your numbers accurate.
Phase 4 — Fix the map
Filter out the generic "Cebu City" coordinate bucket from the heatmap visualization. Only show posts with specific identified locations as pins. Show a count of unlocated posts separately as a stat.
Phase 5 — Fix the frontend
Remove Facebook filter, fix timeframe filter to use actual dates, add pagination to the feed, fix the header counts to read from pre-computed Supabase columns.