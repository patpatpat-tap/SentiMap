"""
SentiMap Reddit Scraper v2 — No API Key Required
=================================================
Uses Reddit's public .json endpoints (no PRAW, no credentials, no approval).
Gets: title, body text, top comments, real timestamps, upvotes, URL.
Outputs: reddit_data_v2.json + reddit_data_v2.xlsx

Install dependencies:
    pip install requests pandas openpyxl

Run:
    python sentimap_scraper_v2.py
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
SUBREDDIT       = "Cebu"
OUTPUT_JSON     = "reddit_data_v2.json"
OUTPUT_EXCEL    = "reddit_data_v2.xlsx"
TOP_COMMENTS    = 5      # comments to grab per post
REQUEST_DELAY   = 2.0    # seconds between requests (be polite, avoid 429s)

# Reddit requires a non-empty User-Agent or it blocks you
HEADERS = {
    "User-Agent": "SentiMap-Research/1.0 (academic project; traffic sentiment analysis Cebu City)"
}

# ─────────────────────────────────────────────
# KEYWORD FILTER — keep only traffic-related posts
# Mix of English, Cebuano, Bislish
# ─────────────────────────────────────────────
KEEP_KEYWORDS = [
    # Must be actual traffic/enforcement/commute terms
    "traffic", "enforcer", "enforcement", "checkpoint", "apprehend",
    "commute", "commuting", "LTFRB", "LTO", "CITOM", "one way scheme",
    "reckless driving", "reckless driver", "road rage",
    "taxi", "grab driver", "jeepney", "bus driver", "truck",
    "violation", "traffic fine", "traffic ticket", "towed", "towing",
    "illegal parking", "pedestrian lane", "overloading",
    "smoke belching", "driver's license", "plate number",
    "trapik", "traysikol", "motorsiklo", "habal-habal", "angkas",
    "byahe", "sakay", "pasahero", "karsada",
    "makalagot", "makaguol",
    "hayahay kaayo ang traffic",
    "traffic enforcer", "traffic officer",
    "kotse", "motor",
]

DROP_KEYWORDS = [
    "valentines", "valentine", "christmas", "birthday", "food",
    "restaurant", "hiring", "job", "apartment", "condo", "rent",
    "lost and found", "lost dog", "missing", "pet", "cat", "dog",
    "meta", "subreddit update", "mod post", "moderator",
    "happy new year", "merry christmas",
    "lechon", "food", "beach", "sunset", "photo", "picture",
    "relationship", "dating", "hookup", "scam", "election",
    "rally", "festival", "concert", "shopping", "medical",
]

CEBU_LOCATIONS = {
    "SRP":           ["srp", "south road properties", "south road property"],
    "Mambaling":     ["mambaling"],
    "Talamban":      ["talamban"],
    "Lahug":         ["lahug"],
    "IT Park":       ["it park", "itpark", "i.t. park"],
    "Ayala":         ["ayala center", "ayala cebu", "ayala"],
    "Fuente":        ["fuente osmeña", "fuente osmena", "fuente circle", "fuente"],
    "Carbon":        ["carbon market", "carbon"],
    "Colon":         ["colon street", "colon"],
    "Mandaue":       ["mandaue"],
    "Mactan":        ["mactan"],
    "Consolacion":   ["consolacion"],
    "Talisay":       ["talisay"],
    "Minglanilla":   ["minglanilla"],
    "Bulacao":       ["bulacao"],
    "Banawa":        ["banawa"],
    "Guadalupe":     ["guadalupe"],
    "Basak":         ["basak"],
    "Salinas Drive": ["salinas drive", "salinas"],
    "N. Bacalso":    ["bacalso", "national bacalso", "n. bacalso"],
    "Osmeña Blvd":   ["osmena blvd", "osmeña blvd", "osmeña boulevard", "osmena boulevard"],
    "Capitol":       ["capitol site", "capitol"],
    "Transcentral":  ["transcentral highway", "transcentral"],
    "Pardo":         ["pardo"],
    "Cebu City":     ["cebu city", "cebu"],   # Generic fallback — lowest priority
}


def is_relevant(title: str, body: str) -> bool:
    text = (title + " " + body).lower()
    for kw in DROP_KEYWORDS:
        if kw in text:
            return False
    for kw in KEEP_KEYWORDS:
        if kw.lower() in text:
            return True
    return False


def extract_locations(title: str, body: str) -> list:
    text = (title + " " + body).lower()
    found = []
    for loc_name, aliases in CEBU_LOCATIONS.items():
        for alias in aliases:
            if alias in text:
                if loc_name not in found:
                    found.append(loc_name)
                break
    # Deprioritize generic "Cebu City" if specific locations also found
    if len(found) > 1 and "Cebu City" in found:
        found.remove("Cebu City")
    return found if found else ["Unknown"]


def fetch_json(url: str) -> dict | None:
    """Fetch a Reddit .json URL with retry logic."""
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                wait = (attempt + 1) * 5
                print(f"    Rate limited (429). Waiting {wait}s...")
                time.sleep(wait)
            else:
                print(f"    HTTP {resp.status_code} for {url}")
                return None
        except requests.RequestException as e:
            print(f"    Request error: {e}")
            time.sleep(3)
    return None


def fetch_post_comments(post_id: str) -> list:
    """Fetch top-level comments for a specific post."""
    url = f"https://www.reddit.com/r/{SUBREDDIT}/comments/{post_id}.json?limit=10&sort=top"
    data = fetch_json(url)
    if not data or len(data) < 2:
        return []

    comments = []
    try:
        comment_listing = data[1]["data"]["children"]
        for child in comment_listing[:TOP_COMMENTS]:
            if child["kind"] != "t1":
                continue
            c = child["data"]
            body = c.get("body", "")
            if body in ("[deleted]", "[removed]", ""):
                continue
            comments.append({
                "body":   body,
                "score":  c.get("score", 0),
                "author": c.get("author", "[deleted]"),
                "created_utc": datetime.fromtimestamp(
                    c.get("created_utc", 0), tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M:%S UTC"),
            })
    except (KeyError, IndexError, TypeError):
        pass

    return comments


def fetch_subreddit_page(sort: str, timeframe: str = "all", after: str = None) -> tuple:
    """
    Fetch one page (up to 100 posts) from a subreddit listing.
    Returns (posts_list, next_after_token)
    """
    url = f"https://www.reddit.com/r/{SUBREDDIT}/{sort}.json?limit=100&t={timeframe}"
    if after:
        url += f"&after={after}"

    data = fetch_json(url)
    if not data:
        return [], None

    try:
        children = data["data"]["children"]
        after_token = data["data"].get("after")
        return children, after_token
    except (KeyError, TypeError):
        return [], None


def scrape_all_posts() -> list:
    results = []
    seen_ids = set()

    # Scrape across multiple sort modes and timeframes for maximum coverage
    # This gets us recent posts AND historically popular ones
    scrape_jobs = [
        ("top",  "all"),    # All-time top posts — best for finding high-signal grievances
        ("top",  "year"),   # Past year
        ("top",  "month"),  # Past month
        ("new",  "all"),    # Newest posts — catches recent Bislish
        ("hot",  "all"),    # Currently trending
    ]

    for sort, timeframe in scrape_jobs:
        label = f"r/{SUBREDDIT}/{sort}?t={timeframe}"
        print(f"\n  → Fetching {label}...")

        after = None
        page  = 0

        while True:
            page += 1
            children, after = fetch_subreddit_page(sort, timeframe, after)

            if not children:
                break

            for child in children:
                if child["kind"] != "t3":
                    continue

                post = child["data"]
                pid  = post.get("id", "")

                if pid in seen_ids:
                    continue
                seen_ids.add(pid)

                title = post.get("title") or ""
                body  = post.get("selftext") or ""

                # Skip deleted/removed
                if body in ("[deleted]", "[removed]"):
                    body = ""

                # Apply relevance filter
                if not is_relevant(title, body):
                    continue

                # Real timestamp
                created_utc = post.get("created_utc", 0)
                created_dt  = datetime.fromtimestamp(created_utc, tz=timezone.utc)

                # Fetch comments for this post (separate request)
                time.sleep(REQUEST_DELAY)
                comments = fetch_post_comments(pid)

                locations = extract_locations(title, body)

                record = {
                    "id":             pid,
                    "title":          title,
                    "body":           body,
                    "full_text":      (title + " " + body).strip(),
                    "author":         post.get("author", "[deleted]"),
                    "created_utc":    created_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                    "created_date":   created_dt.strftime("%Y-%m-%d"),
                    "created_year":   created_dt.year,
                    "created_month":  created_dt.month,
                    "upvotes":        post.get("score", 0),
                    "upvote_ratio":   round(post.get("upvote_ratio", 0), 2),
                    "num_comments":   post.get("num_comments", 0),
                    "subreddit":      post.get("subreddit", SUBREDDIT),
                    "url":            f"https://reddit.com{post.get('permalink', '')}",
                    "sort_source":    f"{sort}/{timeframe}",
                    "locations":      locations,
                    "locations_str":  ", ".join(locations),
                    "top_comments":   comments,
                    "comments_text":  " | ".join(c["body"] for c in comments),
                    "has_body":       bool(body.strip()),
                }

                results.append(record)
                print(f"     [{len(results):>3}] {title[:70]}")

                time.sleep(REQUEST_DELAY + random.uniform(0, 1))

            # Stop paginating if no more pages
            if not after:
                print(f"     End of {label} after {page} page(s).")
                break

            # Reddit listings cap at ~1000 posts; stop after 10 pages (100 each)
            if page >= 10:
                print(f"     Reached page limit for {label}.")
                break

            time.sleep(REQUEST_DELAY)

    return results


def save_outputs(results: list):
    if not results:
        print("\nNo results to save.")
        return

    # Save full JSON (includes nested comments)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n  JSON  → {OUTPUT_JSON}")

    # Save flat Excel (comments as plain text) — CLEAN SUPABASE SCHEMA ONLY
    flat = []
    for r in results:
        flat.append({
            "id":            r["id"],
            "title":         r["title"],
            "body":          r["body"],
            "full_text":     r["full_text"],
            "created_date":  r["created_date"],
            "upvotes":       r["upvotes"],
            "num_comments":  r["num_comments"],
            "url":           r["url"],
            "locations":     r["locations_str"],
            "comments_text": r["comments_text"],
            "is_relevant":   True,  # All posts passed relevance filter
        })

    df = pd.DataFrame(flat)
    df.to_excel(OUTPUT_EXCEL, index=False)
    print(f"  Excel → {OUTPUT_EXCEL}")

    # Summary stats
    posts_with_body = sum(1 for r in results if r["body"].strip())
    print(f"""
  ┌─────────────────────────────────────────┐
  │  DATASET SUMMARY                        │
  ├─────────────────────────────────────────┤
  │  Total posts scraped  : {len(results):<5}               │
  │  Posts WITH body text : {posts_with_body:<5} ({100*posts_with_body//len(results)}%)          │
  │  Date range           : {df['created_date'].min()} → {df['created_date'].max()} │
  │  Avg upvotes          : {df['upvotes'].mean():>10.1f}           │
  │  Avg comments/post    : {df['num_comments'].mean():>10.1f}           │
  └─────────────────────────────────────────┘
    """)

    top_locs = {}
    for locs in results:
        for l in locs["locations"]:
            top_locs[l] = top_locs.get(l, 0) + 1
    top_locs = sorted(top_locs.items(), key=lambda x: -x[1])[:8]
    print("  Top locations detected:")
    for loc, count in top_locs:
        print(f"    {loc:<20} {count} posts")


def main():
    print("=" * 55)
    print("  SentiMap Reddit Scraper v2")
    print("  No API key required")
    print("=" * 55)
    print(f"\n  Target  : r/{SUBREDDIT}")
    print(f"  Filter  : traffic/enforcement keywords (EN + Cebuano + Bislish)")
    print(f"  Output  : {OUTPUT_EXCEL} + {OUTPUT_JSON}")
    print(f"\n  Note: This will take several minutes due to")
    print(f"  rate limit delays between requests. Let it run.\n")

    results = scrape_all_posts()
    save_outputs(results)

    print("\n  Done!")
    print(f"  ✓ Excel file: {OUTPUT_EXCEL}")
    print(f"  ✓ JSON file:  {OUTPUT_JSON}")
    print(f"\n  SCHEMA (ready for Supabase):")
    print(f"    • id, title, body, full_text (title + body for NLP)")
    print(f"    • created_date, upvotes, num_comments, url")
    print(f"    • locations (extracted Cebu locations)")
    print(f"    • comments_text (top 5 comments per post)")
    print(f"    • is_relevant (boolean flag — all True)")
    print(f"\n  Point your FastAPI backend at: {OUTPUT_EXCEL}")


if __name__ == "__main__":
    main()
