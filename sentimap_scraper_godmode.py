"""
SentiMap Reddit Scraper — GOD MODE
====================================
Research: "Geospatial Sentiment Analysis: A Hybrid NLP Approach for
Mapping Traffic Enforcement Grievances in Cebu City"

What makes this God Mode:
- TWO-LAYER filter: keyword match + relevance scoring
- Every post must EARN its place with a minimum relevance score
- Location names CANNOT alone pass a post (fixed the lechon problem)
- Broader scrape surface: r/Cebu + r/Philippines + r/CebuCity + search
- Skips posts already in your existing dataset (no duplicates)
- Saves progress as it goes (crash-safe)
- Auto-scores each post so you know quality of each record

Run:
    pip install requests pandas openpyxl
    python sentimap_scraper_godmode.py
"""

import requests
import pandas as pd
import json
import time
import random
from datetime import datetime, timezone

# ─────────────────────────────────────────────
# SETTINGS
# ─────────────────────────────────────────────
OUTPUT_JSON       = "reddit_godmode.json"
OUTPUT_EXCEL      = "reddit_godmode.xlsx"
PROGRESS_JSON     = "reddit_godmode_progress.json"   # crash-safe checkpoint
TOP_COMMENTS      = 5
REQUEST_DELAY     = 2.5    # polite delay between requests
MIN_SCORE         = 2      # minimum relevance score to keep a post (0-10 scale)
EXISTING_IDS_FILE = "reddit_data_v2.json"  # skip these — already in Supabase

HEADERS = {
    "User-Agent": "SentiMap-Research/2.0 (academic; traffic grievance NLP Cebu City Philippines)"
}

# ─────────────────────────────────────────────
# EXISTING IDS — skip what's already in Supabase
# ─────────────────────────────────────────────
def load_existing_ids() -> set:
    try:
        with open(EXISTING_IDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        ids = {d["id"] for d in data}
        print(f"  Loaded {len(ids)} existing IDs to skip (already in Supabase)")
        return ids
    except FileNotFoundError:
        print("  No existing dataset found — starting fresh")
        return set()


# ─────────────────────────────────────────────
# GOD MODE FILTER — TWO LAYERS
#
# Layer 1: MUST have at least one CORE keyword
#           (actual traffic/enforcement/commute terms)
#           Location names alone CANNOT pass this.
#
# Layer 2: RELEVANCE SCORE
#           Each keyword category adds points.
#           Post must reach MIN_SCORE (default: 2).
#           Higher score = more relevant to research.
# ─────────────────────────────────────────────

# CORE keywords — at least ONE must appear or post is rejected immediately
# These are unambiguous traffic/enforcement/commute signals
CORE_KEYWORDS = [
    # English — enforcement
    "traffic enforcer", "traffic enforcement", "traffic officer",
    "traffic violation", "traffic apprehend", "traffic fine",
    "traffic ticket", "traffic scheme", "traffic law",
    "CITOM", "LTFRB", "LTO", "CCTO", "MMDA",
    "checkpoint", "apprehended", "apprehension",
    "reckless driving", "road rage", "counterflow",
    "illegal parking", "no parking", "towing", "towed",
    "smoke belching", "overloading", "colorum",
    "driver's license", "plate number", "registration",
    "traffic light", "traffic signal", "stoplight",
    "pedestrian lane", "crosswalk", "sidewalk",
    "one way", "one-way scheme", "road scheme",
    "road safety", "road accident", "road incident",
    "BRT", "bus rapid transit",

    # English — transport grievances
    "jeepney", "jeep driver", "jeep conductor",
    "taxi driver", "taxi meter", "overcharging",
    "bus driver", "bus conductor", "fare hike",
    "fare increase", "PUV", "public utility",
    "grab driver", "angkas driver", "move it",
    "habal-habal", "multicab driver",
    "commute", "commuting", "commuters",
    "public transport", "mass transit",

    # Cebuano/Bislish — enforcement
    "trapik enforcer", "pulis sa dalan", "CITOM",
    "naapprehend", "giapprehend", "naaresto",
    "kontra-plaka", "kontra flow",
    "trapik", "trapiko",

    # Cebuano/Bislish — commute/transport
    "sakay jeep", "sakay bus", "nakasakay",
    "pasahero", "konduktor", "driver sa jeep",
    "angkas", "mag-angkas", "nag-angkas",
    "byahe", "mag-byahe", "nag-byahe",
    "plite", "plete", "bayad sa jeep",
    "pag-commute", "mag-commute", "nag-commute",
    "sakyanan", "karsada", "dalan",
]

# BONUS keywords — each adds +1 to relevance score
# Having more of these = more relevant to research
BONUS_KEYWORDS = {
    # Enforcement/authority (high value — core research topic)
    "enforcer":        3,
    "enforcement":     3,
    "apprehend":       3,
    "checkpoint":      3,
    "CITOM":           3,
    "LTFRB":           3,
    "LTO":             2,
    "violation":       2,
    "penalty":         2,
    "fine":            2,
    "ticket":          2,
    "license":         2,

    # Traffic infrastructure (medium value)
    "traffic":         1,
    "road":            1,
    "highway":         1,
    "sidewalk":        1,
    "pedestrian":      1,
    "crosswalk":       1,
    "one way":         2,
    "counterflow":     2,
    "BRT":             2,
    "bus lane":        2,
    "bike lane":       1,

    # Public transport (medium value)
    "jeepney":         2,
    "jeep":            1,
    "taxi":            1,
    "bus":             1,
    "commute":         2,
    "commuter":        2,
    "pasahero":        2,
    "angkas":          2,
    "grab":            1,
    "move it":         1,
    "PUV":             2,
    "fare":            2,
    "plite":           2,
    "plete":           2,

    # Sentiment/frustration (adds Bislish signal value)
    "makalagot":       2,
    "makaguol":        2,
    "hayahay":         3,   # sarcasm marker — high research value
    "yawa":            1,
    "bwisit":          1,
    "kapoy":           1,
    "grabeh":          1,
    "grabe":           1,
    "nasukaon":        2,
    "naratol":         2,

    # Cebuano transport terms
    "byahe":           1,
    "sakay":           1,
    "trapik":          2,
    "karsada":         1,
    "dalan":           1,
    "kotse":           1,
    "motor":           1,
    "motorsiklo":      1,

    # Location + traffic context (only adds if core keyword already present)
    "SRP":             1,
    "Mambaling":       1,
    "Talamban":        1,
    "IT Park":         1,
    "Fuente":          1,
    "Mandaue":         1,
    "Mactan":          1,
    "Talisay":         1,
    "Consolacion":     1,
    "Bulacao":         1,
}

# Hard drop list — these override everything, post is rejected immediately
HARD_DROP = [
    # Off-topic lifestyle
    "lechon", "sinulog", "festival", "concert", "beach",
    "resort", "swimming", "hiking", "camping",
    "recipe", "cooking", "food review", "restaurant review",
    "milk tea", "boba", "coffee shop", "cafe reco",

    # Off-topic personal
    "relationship advice", "break up", "breakup",
    "boyfriend", "girlfriend", "hugot", "crush",
    "valentines", "valentine", "anniversary",
    "wedding", "birthday party",

    # Off-topic business/classifieds
    "for sale", "for rent", "hiring", "job opening",
    "apply now", "apartment", "condo for rent",
    "roommate", "bedspace",

    # Off-topic events/places
    "hotel recommendation", "tourist spot", "itinerary",
    "where to buy", "where to find", "recommendation for",
    "movie", "netflix", "kdrama",
]


def god_mode_filter(title: str, body: str) -> tuple[bool, int, list]:
    """
    Returns (is_relevant, score, matched_keywords)
    
    Two-layer filter:
    1. Hard drop check — immediate rejection
    2. Core keyword check — must have at least one
    3. Bonus scoring — accumulate relevance score
    """
    combined = (title + " " + body).lower()
    matched = []

    # Layer 0: Hard drop — reject immediately
    for kw in HARD_DROP:
        if kw.lower() in combined:
            return False, 0, []

    # Layer 1: Must have at least one CORE keyword
    has_core = False
    for kw in CORE_KEYWORDS:
        if kw.lower() in combined:
            has_core = True
            matched.append(f"CORE:{kw}")
            break

    if not has_core:
        return False, 0, []

    # Layer 2: Accumulate bonus score
    score = 0
    for kw, points in BONUS_KEYWORDS.items():
        if kw.lower() in combined:
            score += points
            matched.append(f"+{points}:{kw}")

    # Minimum score gate
    if score < MIN_SCORE:
        return False, score, matched

    return True, score, matched


# ─────────────────────────────────────────────
# LOCATION EXTRACTOR
# ─────────────────────────────────────────────
CEBU_LOCATIONS = {
    "SRP":              ["srp", "south road properties"],
    "Mambaling":        ["mambaling"],
    "Talamban":         ["talamban"],
    "Lahug":            ["lahug"],
    "IT Park":          ["it park", "itpark", "i.t. park"],
    "Ayala":            ["ayala center", "ayala cebu", "ayala business"],
    "Fuente Osmeña":    ["fuente osmeña", "fuente osmena", "fuente circle", "fuente"],
    "Carbon Market":    ["carbon market"],
    "Colon Street":     ["colon street", "metro colon"],
    "Mandaue":          ["mandaue"],
    "Mactan":           ["mactan"],
    "Consolacion":      ["consolacion"],
    "Talisay":          ["talisay city", "talisay"],
    "Minglanilla":      ["minglanilla"],
    "Bulacao":          ["bulacao"],
    "Banawa":           ["banawa"],
    "Guadalupe":        ["guadalupe"],
    "Basak":            ["basak"],
    "Salinas Drive":    ["salinas drive", "salinas"],
    "N. Bacalso":       ["bacalso", "n. bacalso", "national bacalso"],
    "Osmeña Blvd":      ["osmena blvd", "osmeña blvd", "osmeña boulevard"],
    "Capitol":          ["capitol site", "capitol"],
    "Transcentral":     ["transcentral highway", "transcentral"],
    "Pardo":            ["pardo"],
    "Urgello":          ["urgello"],
    "Ouano":            ["ouano"],
    "Subangdaku":       ["subangdaku"],
    "Hernan Cortes":    ["hernan cortes"],
    "A.S. Fortuna":     ["a.s. fortuna", "as fortuna", "fortuna"],
    "Escario":          ["escario"],
    "Gorordo":          ["gorordo"],
    "Archbishop Reyes": ["archbishop reyes", "reyes ave"],
    "Jones Ave":        ["jones ave", "jones avenue"],
    "Colon":            ["colon"],
    "Cebu City":        ["cebu city"],
}

def extract_locations(title: str, body: str) -> list:
    text = (title + " " + body).lower()
    found = []
    for loc_name, aliases in CEBU_LOCATIONS.items():
        for alias in aliases:
            if alias in text:
                if loc_name not in found:
                    found.append(loc_name)
                break
    if len(found) > 1 and "Cebu City" in found:
        found.remove("Cebu City")
    if len(found) > 1 and "Colon" in found and "Colon Street" in found:
        found.remove("Colon")
    return found if found else ["Unknown"]


# ─────────────────────────────────────────────
# HTTP HELPERS
# ─────────────────────────────────────────────
def fetch_json(url: str) -> dict | None:
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=20)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait = (attempt + 1) * 10
                print(f"    Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            elif resp.status_code == 403:
                print(f"    403 Forbidden — skipping")
                return None
            else:
                print(f"    HTTP {resp.status_code}")
                return None
        except requests.RequestException as e:
            wait = (attempt + 1) * 5
            print(f"    Network error ({e.__class__.__name__}). Waiting {wait}s...")
            time.sleep(wait)
    return None


def fetch_comments(subreddit: str, post_id: str) -> list:
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json?limit=10&sort=top"
    data = fetch_json(url)
    if not data or len(data) < 2:
        return []
    comments = []
    try:
        for child in data[1]["data"]["children"][:TOP_COMMENTS]:
            if child["kind"] != "t1":
                continue
            c = child["data"]
            body = c.get("body", "")
            if body in ("[deleted]", "[removed]", ""):
                continue
            comments.append({
                "body":        body,
                "score":       c.get("score", 0),
                "author":      c.get("author", "[deleted]"),
                "created_utc": datetime.fromtimestamp(
                    c.get("created_utc", 0), tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M:%S UTC"),
            })
    except (KeyError, IndexError, TypeError):
        pass
    return comments


def fetch_listing_page(subreddit: str, sort: str, timeframe: str = "all",
                       after: str = None) -> tuple:
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit=100&t={timeframe}"
    if after:
        url += f"&after={after}"
    data = fetch_json(url)
    if not data:
        return [], None
    try:
        return data["data"]["children"], data["data"].get("after")
    except (KeyError, TypeError):
        return [], None


def fetch_search_page(subreddit: str, query: str, after: str = None) -> tuple:
    """Search within a subreddit for specific terms."""
    url = f"https://www.reddit.com/r/{subreddit}/search.json?q={requests.utils.quote(query)}&restrict_sr=1&sort=relevance&limit=100&t=all"
    if after:
        url += f"&after={after}"
    data = fetch_json(url)
    if not data:
        return [], None
    try:
        return data["data"]["children"], data["data"].get("after")
    except (KeyError, TypeError):
        return [], None


# ─────────────────────────────────────────────
# PROGRESS SAVE — crash safe
# ─────────────────────────────────────────────
def save_progress(results: list):
    with open(PROGRESS_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


def load_progress() -> list:
    try:
        with open(PROGRESS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"  Resumed from checkpoint: {len(data)} posts already collected")
        return data
    except FileNotFoundError:
        return []


# ─────────────────────────────────────────────
# MAIN SCRAPE ENGINE
# ─────────────────────────────────────────────
def build_record(post: dict, subreddit: str, sort: str, score: int,
                 matched: list, comments: list) -> dict:
    title = post.get("title") or ""
    body  = post.get("selftext") or ""
    if body in ("[deleted]", "[removed]"):
        body = ""

    created_dt = datetime.fromtimestamp(
        post.get("created_utc", 0), tz=timezone.utc
    )
    locations = extract_locations(title, body)

    return {
        "id":               post.get("id", ""),
        "title":            title,
        "body":             body,
        "full_text":        (title + " " + body).strip(),
        "has_body":         bool(body.strip()),
        "author":           post.get("author", "[deleted]"),
        "created_utc":      created_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "created_date":     created_dt.strftime("%Y-%m-%d"),
        "created_year":     created_dt.year,
        "created_month":    created_dt.month,
        "upvotes":          post.get("score", 0),
        "upvote_ratio":     round(post.get("upvote_ratio", 0), 2),
        "num_comments":     post.get("num_comments", 0),
        "subreddit":        post.get("subreddit", subreddit),
        "url":              f"https://reddit.com{post.get('permalink', '')}",
        "sort_source":      sort,
        "platform":         "reddit",
        "relevance_score":  score,
        "matched_keywords": ", ".join(matched[:5]),
        "locations":        locations,
        "locations_str":    ", ".join(locations),
        "top_comments":     comments,
        "comments_text":    " | ".join(c["body"] for c in comments),
    }


def process_children(children: list, subreddit: str, sort_label: str,
                     results: list, seen_ids: set, existing_ids: set) -> int:
    """Process a page of posts. Returns number of new posts added."""
    added = 0
    for child in children:
        if child.get("kind") != "t3":
            continue

        post = child["data"]
        pid  = post.get("id", "")

        if not pid or pid in seen_ids or pid in existing_ids:
            continue
        seen_ids.add(pid)

        title = post.get("title") or ""
        body  = post.get("selftext") or ""
        if body in ("[deleted]", "[removed]"):
            body = ""

        # GOD MODE FILTER
        is_relevant, score, matched = god_mode_filter(title, body)
        if not is_relevant:
            continue

        # Fetch comments (separate request — adds delay)
        time.sleep(REQUEST_DELAY)
        comments = fetch_comments(subreddit, pid)

        record = build_record(post, subreddit, sort_label, score, matched, comments)
        results.append(record)
        added += 1

        relevance_bar = "█" * min(score, 10)
        print(f"     [{len(results):>3}] score={score:>2} {relevance_bar:<10} | {title[:60]}")

        # Save progress every 10 posts (crash safe)
        if len(results) % 10 == 0:
            save_progress(results)

        time.sleep(REQUEST_DELAY + random.uniform(0, 1.0))

    return added


def scrape_all(existing_ids: set, resume_results: list) -> list:
    results = resume_results[:]
    seen_ids = {r["id"] for r in results} | existing_ids

    # ── SCRAPE JOBS ──────────────────────────────────────────────
    # Each tuple: (subreddit, sort_mode, timeframe_or_search_query, label)
    # We scrape multiple subreddits and use targeted search queries
    # to maximize coverage of traffic/enforcement content
    # ─────────────────────────────────────────────────────────────

    listing_jobs = [
        # r/Cebu — main source
        ("Cebu", "top",  "all",   "r/Cebu top/all"),
        ("Cebu", "top",  "year",  "r/Cebu top/year"),
        ("Cebu", "top",  "month", "r/Cebu top/month"),
        ("Cebu", "hot",  "all",   "r/Cebu hot"),
        ("Cebu", "new",  "all",   "r/Cebu new"),

        # r/Philippines — national perspective on Cebu traffic
        ("Philippines", "top", "all",  "r/Philippines top/all"),
        ("Philippines", "top", "year", "r/Philippines top/year"),
    ]

    # Targeted search queries within r/Cebu
    # These surface posts that might not appear in top/new/hot
    # but are directly relevant to the research
    search_jobs = [
        ("Cebu", "traffic enforcer cebu",      "search:enforcer"),
        ("Cebu", "CITOM cebu",                 "search:CITOM"),
        ("Cebu", "LTO cebu",                   "search:LTO"),
        ("Cebu", "LTFRB cebu",                 "search:LTFRB"),
        ("Cebu", "jeepney driver cebu",        "search:jeepney"),
        ("Cebu", "commute cebu",               "search:commute"),
        ("Cebu", "taxi cebu overcharge",       "search:taxi"),
        ("Cebu", "angkas cebu",                "search:angkas"),
        ("Cebu", "grab driver cebu",           "search:grab"),
        ("Cebu", "BRT cebu",                   "search:BRT"),
        ("Cebu", "checkpoint cebu",            "search:checkpoint"),
        ("Cebu", "road rage cebu",             "search:road_rage"),
        ("Cebu", "traffic violation cebu",     "search:violation"),
        ("Cebu", "counterflow cebu",           "search:counterflow"),
        ("Cebu", "illegal parking cebu",       "search:parking"),
        ("Cebu", "pedestrian cebu",            "search:pedestrian"),
        ("Cebu", "reckless driving cebu",      "search:reckless"),
        ("Cebu", "fare hike cebu",             "search:fare"),
        ("Cebu", "trapik cebu",                "search:trapik"),
        ("Cebu", "makalagot traffic",          "search:makalagot"),
        ("Cebu", "hayahay traffic",            "search:hayahay_sarcasm"),
        ("Cebu", "SRP traffic",                "search:SRP"),
        ("Cebu", "Mambaling traffic",          "search:Mambaling"),
        ("Cebu", "Mandaue traffic",            "search:Mandaue"),
        ("Cebu", "Move It angkas rider",       "search:rideshare"),
        ("Cebu", "traffic scheme one way",     "search:scheme"),
        ("Cebu", "smoke belching",             "search:smoke"),
        ("Cebu", "overloading bus cebu",       "search:overloading"),
        ("Philippines", "traffic cebu city",   "search:ph_cebu_traffic"),
        ("Philippines", "CITOM Cebu",          "search:ph_CITOM"),
    ]

    # ── RUN LISTING JOBS ─────────────────────────────────────────
    for subreddit, sort, timeframe, label in listing_jobs:
        print(f"\n  → [{label}]")
        after = None
        page  = 0

        while True:
            page += 1
            children, after = fetch_listing_page(subreddit, sort, timeframe, after)
            if not children:
                print(f"     End after {page} page(s).")
                break

            added = process_children(children, subreddit, label,
                                     results, seen_ids, existing_ids)

            if not after:
                print(f"     End after {page} page(s). Added {added} this page.")
                break
            if page >= 10:
                print(f"     Page limit reached.")
                break

            time.sleep(REQUEST_DELAY)

    # ── RUN SEARCH JOBS ──────────────────────────────────────────
    for subreddit, query, label in search_jobs:
        print(f"\n  → [{label}] searching: \"{query}\"")
        after = None
        page  = 0

        while True:
            page += 1
            children, after = fetch_search_page(subreddit, query, after)
            if not children:
                break

            added = process_children(children, subreddit, label,
                                     results, seen_ids, existing_ids)
            print(f"     Page {page}: added {added}")

            if not after or page >= 3:
                break

            time.sleep(REQUEST_DELAY)

    return results


# ─────────────────────────────────────────────
# SAVE OUTPUTS
# ─────────────────────────────────────────────
def save_outputs(results: list):
    if not results:
        print("\nNo results to save.")
        return

    # Full JSON with nested comments
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n  JSON  -> {OUTPUT_JSON}")

    # Flat Excel for Supabase import
    flat = []
    for r in results:
        flat.append({
            "id":               r["id"],
            "title":            r["title"],
            "body":             r["body"],
            "full_text":        r["full_text"],
            "has_body":         r["has_body"],
            "author":           r["author"],
            "created_utc":      r["created_utc"],
            "created_date":     r["created_date"],
            "created_year":     r["created_year"],
            "created_month":    r["created_month"],
            "upvotes":          r["upvotes"],
            "upvote_ratio":     r["upvote_ratio"],
            "num_comments":     r["num_comments"],
            "url":              r["url"],
            "platform":         r["platform"],
            "relevance_score":  r["relevance_score"],
            "matched_keywords": r["matched_keywords"],
            "locations":        r["locations_str"],
            "comments_text":    r["comments_text"],
        })

    df = pd.DataFrame(flat)
    df = df.sort_values("relevance_score", ascending=False)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"  Excel -> {OUTPUT_EXCEL}")

    # Summary
    has_body    = df["has_body"].sum()
    avg_score   = df["relevance_score"].mean()
    high_qual   = (df["relevance_score"] >= 5).sum()

    print(f"""
  +--------------------------------------------------+
  |  GOD MODE DATASET SUMMARY                       |
  +--------------------------------------------------+
  |  Total posts collected : {len(results):<6}                  |
  |  Posts WITH body text  : {has_body:<6} ({100*has_body//max(len(results),1)}%)             |
  |  Avg relevance score   : {avg_score:<6.1f}                  |
  |  High quality (>=5)    : {high_qual:<6}                  |
  |  Date range            : {df['created_date'].min()} to {df['created_date'].max()}  |
  +--------------------------------------------------+
    """)

    # Score distribution
    print("  Relevance score distribution:")
    for threshold in [10, 8, 6, 4, 2]:
        count = (df["relevance_score"] >= threshold).sum()
        bar = "█" * min(count // 2, 30)
        print(f"    score >= {threshold:>2}: {count:>4} posts  {bar}")

    # Location coverage
    from collections import Counter
    locs = []
    for r in results:
        locs.extend(r.get("locations", []))
    loc_counts = Counter(locs).most_common(12)
    print("\n  Top locations:")
    for loc, count in loc_counts:
        bar = "█" * min(count, 20)
        print(f"    {loc:<25} {count:>4}  {bar}")

    print(f"\n  Sorted by relevance_score DESC in Excel.")
    print(f"  Import to Supabase: backend/scripts/import_to_supabase.py")


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  SentiMap Reddit Scraper — GOD MODE")
    print("  Precision filter for traffic enforcement research")
    print("=" * 55)
    print(f"\n  Research: Geospatial Sentiment Analysis")
    print(f"  Target  : r/Cebu + r/Philippines + targeted search")
    print(f"  Filter  : TWO-LAYER (core keyword + relevance score)")
    print(f"  Min score: {MIN_SCORE}/10 to keep a post")
    print(f"  Output  : {OUTPUT_EXCEL} + {OUTPUT_JSON}")
    print(f"\n  This will take 20-40 minutes. Let it run.")
    print(f"  Progress auto-saved every 10 posts.\n")

    existing_ids  = load_existing_ids()
    resume        = load_progress()
    results       = scrape_all(existing_ids, resume)

    save_outputs(results)
    save_progress(results)  # Final save

    print(f"\n  Done! {len(results)} posts collected.")
    print(f"  Next: move {OUTPUT_EXCEL} to backend/data/")
    print(f"  Then: run import_to_supabase.py to push to database")


if __name__ == "__main__":
    main()
