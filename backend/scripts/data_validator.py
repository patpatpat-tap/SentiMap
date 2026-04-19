"""
SentiMap Data Validator & Cleaner
===================================
Purpose: Audit all 736 posts in Supabase and determine which are
genuinely relevant to the research:
"Geospatial Sentiment Analysis: A Hybrid NLP Approach for
Mapping Traffic Enforcement Grievances in Cebu City"

What this script does:
1. Loads all posts from Supabase
2. Scores each post on multiple research-relevance dimensions
3. Auto-classifies: KEEP / REVIEW / DISCARD
4. Lets you manually review only the BORDERLINE cases (~50-100 posts)
5. Writes final is_clean + relevance_score back to Supabase
6. Outputs a report showing your clean dataset stats

Run:
    python data_validator.py

Requirements:
    pip install requests pandas openpyxl python-dotenv
"""

import os
import json
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "app", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

REPORT_FILE  = "validation_report.json"
EXCEL_REPORT = "validation_report.xlsx"

# ─────────────────────────────────────────────────────────────
# RESEARCH RELEVANCE SCORING SYSTEM
#
# A post earns points across 4 dimensions:
#   D1 - Enforcement signal   (max 10 pts) ← most important
#   D2 - Public transport     (max 6 pts)
#   D3 - Sentiment/grievance  (max 4 pts)  ← Bislish value
#   D4 - Location specificity (max 3 pts)
#
# Total max: 23 pts
# AUTO-KEEP:    score >= 6
# MANUAL REVIEW: score 3-5
# AUTO-DISCARD: score <= 2
# ─────────────────────────────────────────────────────────────

# D1 — Traffic Enforcement (highest weight — core of research)
ENFORCEMENT_KEYWORDS = {
    # Agencies — strongest signal
    "CITOM":               5,
    "CCTO":                5,
    "LTFRB":               5,
    "LTO":                 4,
    "traffic enforcer":    5,
    "traffic enforcement": 5,
    "traffic officer":     4,
    "traffic law":         3,
    # Actions
    "apprehended":         4,
    "apprehend":           4,
    "giapprehend":         4,
    "naapprehend":         4,
    "checkpoint":          4,
    "colorum":             4,
    "counterflow":         4,
    "conterflow":          3,
    "road rage":           3,
    "reckless driving":    4,
    "reckless driver":     4,
    # Violations
    "traffic violation":   4,
    "traffic fine":        3,
    "traffic ticket":      3,
    "illegal parking":     3,
    "no parking":          2,
    "towing":              3,
    "towed":               3,
    "smoke belching":      3,
    "overloading":         3,
    "license":             2,
    "plate number":        2,
    # Schemes/policy
    "one way scheme":      3,
    "one-way scheme":      3,
    "traffic scheme":      3,
    "road scheme":         3,
    "BRT":                 3,
    "bus rapid transit":   3,
    "CCLEX":               2,
    # Safety
    "pedestrian lane":     3,
    "crosswalk":           2,
    "road safety":         2,
    "traffic light":       2,
    "traffic signal":      2,
    "stoplight":           2,
}

# D2 — Public Transport Grievances
TRANSPORT_KEYWORDS = {
    "jeepney":             3,
    "jeep driver":         3,
    "jeep conductor":      2,
    "bus driver":          2,
    "bus conductor":       2,
    "taxi driver":         3,
    "taxi meter":          4,
    "overcharging":        3,
    "fare hike":           3,
    "fare increase":       3,
    "PUV":                 2,
    "public utility":      2,
    "angkas":              2,
    "grab driver":         2,
    "habal-habal":         2,
    "move it":             2,
    "commute":             2,
    "commuting":           2,
    "commuter":            2,
    "pasahero":            2,
    "plite":               2,
    "plete":               2,
    "byahe":               1,
    "sakay":               1,
    "sakyanan":            1,
    "trapik":              2,
    "karsada":             1,
}

# D3 — Sentiment/Grievance signal (Bislish value for NLP research)
SENTIMENT_KEYWORDS = {
    # Sarcasm markers — highest research value
    "hayahay":             4,
    "hayahay kaayo":       4,
    "so comfortable":      3,
    "smooth ra":           3,
    # Strong negative
    "makalagot":           2,
    "makaguol":            2,
    "nasukaon":            2,
    "naratol":             2,
    "kapoy na":            2,
    "kapoy kaayo":         2,
    "yawa":                1,
    "bwisit":              1,
    "piste":               1,
    "grabe":               1,
    "grabeh":              1,
    # Complaint framing
    "reklamo":             2,
    "sumbong":             2,
    "report":              1,
    "complain":            1,
    "asa ko mu-report":    3,
    "asa ta maka-reklamo": 3,
}

# D4 — Specific Cebu location (adds precision to geospatial claim)
LOCATION_KEYWORDS = {
    "SRP":              2,
    "south road":       2,
    "Mambaling":        2,
    "Talamban":         2,
    "Lahug":            2,
    "IT Park":          2,
    "Fuente":           2,
    "Fuente Osmena":    2,
    "Fuente Osmeña":    2,
    "Mandaue":          2,
    "Mactan":           2,
    "Consolacion":      2,
    "Talisay":          2,
    "Bulacao":          2,
    "Banawa":           2,
    "Guadalupe":        2,
    "Basak":            2,
    "Salinas":          2,
    "Bacalso":          2,
    "Transcentral":     2,
    "Pardo":            2,
    "Capitol":          2,
    "Colon":            1,
    "Ayala":            1,
    "Carbon":           1,
    "Gorordo":          2,
    "Archbishop Reyes": 2,
    "Jones Ave":        2,
    "Escario":          2,
    "Urgello":          2,
    "Subangdaku":       2,
    "Hernan Cortes":    2,
    "A.S. Fortuna":     2,
    "Cebu City":        1,   # generic — low weight
}

# HARD DISQUALIFIERS — these override everything
# If any of these appear in title, auto-discard regardless of score
DISQUALIFIERS = [
    # Food
    "lechon", "sinulog", "carcar lechon", "chicharon",
    "restaurant", "milk tea", "boba", "coffee shop",
    "cafe reco", "food review", "where to eat", "best food",
    # Shopping/retail
    "for sale", "for rent", "rent", "bedspace", "roommate",
    "ukay", "thrift", "ref", "appliance", "gadget",
    # Entertainment
    "concert", "festival", "sinulog festival",
    "movie", "kdrama", "netflix", "anime",
    # Personal/relationship
    "relationship", "breakup", "break up", "boyfriend",
    "girlfriend", "crush", "hugot", "valentines",
    "wedding", "birthday party", "anniversary",
    # Jobs/classifieds
    "hiring", "job opening", "job vacancy", "apply now",
    "work from home", "WFH",
    # Tourism
    "tourist spot", "beach resort", "hotel recommendation",
    "travel itinerary", "where to stay",
    # Medical (unless related to road accident)
    "hospital recommendation", "doctor reco",
    # Gaming
    "nintendo", "playstation", "gaming",
    # Weather (unless causes traffic)
    "earthquake", "typhoon",
    # Crime (unrelated to traffic)
    "murder", "rape", "robbery", "scam",
    # General chit-chat
    "hugot", "love life", "kilig",
]

# TITLE-ONLY DISQUALIFIERS
# These in the TITLE alone (not body) are enough to discard
TITLE_DISQUALIFIERS = [
    "where to buy", "where to find", "recommendation for",
    "best place", "good place", "looking for",
    "asa makapalit", "asa makita", "asa maka",
    "photo", "picture", "pic", "OC", "[OC]",
    "appreciation post", "shoutout",
]


def score_post(title: str, body: str, full_text: str) -> dict:
    """
    Score a post across all 4 research relevance dimensions.
    Returns detailed breakdown so you can see WHY a post scored what it did.
    """
    text_lower = full_text.lower()
    title_lower = title.lower()

    result = {
        "d1_enforcement": 0,
        "d2_transport":   0,
        "d3_sentiment":   0,
        "d4_location":    0,
        "total":          0,
        "matched":        [],
        "disqualified":   False,
        "disqualify_reason": "",
        "verdict":        "",
    }

    # Check hard disqualifiers on title first (fast path)
    for kw in TITLE_DISQUALIFIERS:
        if kw.lower() in title_lower:
            result["disqualified"] = True
            result["disqualify_reason"] = f"title_disqualifier: '{kw}'"
            result["verdict"] = "DISCARD"
            return result

    # Check all disqualifiers on full text
    for kw in DISQUALIFIERS:
        if kw.lower() in text_lower:
            result["disqualified"] = True
            result["disqualify_reason"] = f"disqualifier: '{kw}'"
            result["verdict"] = "DISCARD"
            return result

    # D1 — Enforcement scoring (capped at 10)
    for kw, pts in ENFORCEMENT_KEYWORDS.items():
        if kw.lower() in text_lower:
            result["d1_enforcement"] = min(result["d1_enforcement"] + pts, 10)
            result["matched"].append(f"D1+{pts}:{kw}")

    # D2 — Transport scoring (capped at 6)
    for kw, pts in TRANSPORT_KEYWORDS.items():
        if kw.lower() in text_lower:
            result["d2_transport"] = min(result["d2_transport"] + pts, 6)
            result["matched"].append(f"D2+{pts}:{kw}")

    # D3 — Sentiment scoring (capped at 4)
    for kw, pts in SENTIMENT_KEYWORDS.items():
        if kw.lower() in text_lower:
            result["d3_sentiment"] = min(result["d3_sentiment"] + pts, 4)
            result["matched"].append(f"D3+{pts}:{kw}")

    # D4 — Location scoring (capped at 3)
    for kw, pts in LOCATION_KEYWORDS.items():
        if kw.lower() in text_lower:
            result["d4_location"] = min(result["d4_location"] + pts, 3)
            result["matched"].append(f"D4+{pts}:{kw}")

    # Must have at least D1 OR (D2 + D3) to be relevant
    # A post about commuting with frustration counts even without CITOM
    has_enforcement = result["d1_enforcement"] >= 3
    has_transport_grievance = result["d2_transport"] >= 2 and result["d3_sentiment"] >= 1

    if not has_enforcement and not has_transport_grievance:
        result["disqualified"] = True
        result["disqualify_reason"] = "no enforcement or transport+grievance signal"
        result["verdict"] = "DISCARD"
        result["total"] = result["d1_enforcement"] + result["d2_transport"]
        return result

    total = (result["d1_enforcement"] +
             result["d2_transport"] +
             result["d3_sentiment"] +
             result["d4_location"])
    result["total"] = total

    if total >= 6:
        result["verdict"] = "KEEP"
    elif total >= 3:
        result["verdict"] = "REVIEW"
    else:
        result["verdict"] = "DISCARD"

    return result


def load_all_posts() -> list:
    """Load all posts from Supabase with pagination."""
    all_posts = []
    offset = 0
    limit  = 200

    print("  Loading posts from Supabase...")
    while True:
        url = f"{SUPABASE_URL}/rest/v1/posts"
        params = {
            "select": "id,title,body,full_text,locations,url,upvotes,num_comments,created_date",
            "offset": offset,
            "limit":  limit,
            "order":  "created_date.desc",
        }
        resp = requests.get(url, headers=HEADERS, params=params)
        if resp.status_code != 200:
            print(f"  ERROR loading posts: {resp.status_code} {resp.text}")
            break
        batch = resp.json()
        if not batch:
            break
        all_posts.extend(batch)
        offset += limit
        if len(batch) < limit:
            break

    print(f"  Loaded {len(all_posts)} posts from Supabase")
    return all_posts


def update_post_in_supabase(post_id: str, updates: dict) -> bool:
    """Write validation results back to a single post."""
    url = f"{SUPABASE_URL}/rest/v1/posts"
    params = {"id": f"eq.{post_id}"}
    resp = requests.patch(url, headers=HEADERS, params=params, json=updates)
    return resp.status_code in (200, 204)


def manual_review_session(borderline: list) -> dict:
    """
    Interactive terminal session for reviewing borderline posts.
    Shows title + body excerpt + score breakdown.
    User presses K (keep), D (discard), or S (skip).
    Returns {post_id: decision}
    """
    decisions = {}
    total = len(borderline)

    print(f"\n{'='*60}")
    print(f"  MANUAL REVIEW — {total} borderline posts")
    print(f"  Commands: K=Keep  D=Discard  S=Skip (decide later)")
    print(f"  Tip: Keep if it's about traffic/commute frustration in Cebu")
    print(f"{'='*60}\n")

    for i, item in enumerate(borderline):
        post  = item["post"]
        score = item["score"]
        pid   = post.get("id", "")
        title = post.get("title", "")
        body  = (post.get("body") or post.get("full_text") or "")[:300]

        print(f"\n[{i+1}/{total}] Score: {score['total']}/23  "
              f"D1={score['d1_enforcement']} D2={score['d2_transport']} "
              f"D3={score['d3_sentiment']} D4={score['d4_location']}")
        print(f"  TITLE : {title}")
        print(f"  BODY  : {body[:200]}{'...' if len(body) > 200 else ''}")
        print(f"  MATCHED: {', '.join(score['matched'][:6])}")
        print(f"  URL   : {post.get('url', '')}")

        while True:
            choice = input("  Decision [K/D/S]: ").strip().upper()
            if choice in ("K", "D", "S"):
                break
            print("  Please enter K, D, or S")

        if choice == "K":
            decisions[pid] = "KEEP"
            print("  -> KEEP")
        elif choice == "D":
            decisions[pid] = "DISCARD"
            print("  -> DISCARD")
        else:
            decisions[pid] = "SKIP"
            print("  -> SKIPPED (will review later)")

    return decisions


def run_validation():
    print("=" * 60)
    print("  SentiMap Data Validator")
    print("  Research: Traffic Enforcement Grievances in Cebu City")
    print("=" * 60)

    # ── LOAD ───────────────────────────────────────────────────
    posts = load_all_posts()
    if not posts:
        print("No posts found. Check your .env credentials.")
        return

    # ── SCORE ALL POSTS ────────────────────────────────────────
    print(f"\n  Scoring {len(posts)} posts across 4 research dimensions...")

    auto_keep    = []
    borderline   = []
    auto_discard = []

    for post in posts:
        title     = post.get("title", "") or ""
        body      = post.get("body", "") or ""
        full_text = post.get("full_text", "") or (title + " " + body)

        score = score_post(title, body, full_text)

        entry = {"post": post, "score": score}

        if score["verdict"] == "KEEP":
            auto_keep.append(entry)
        elif score["verdict"] == "REVIEW":
            borderline.append(entry)
        else:
            auto_discard.append(entry)

    print(f"\n  AUTO-KEEP    : {len(auto_keep)} posts (score >= 6)")
    print(f"  NEED REVIEW  : {len(borderline)} posts (score 3-5)")
    print(f"  AUTO-DISCARD : {len(auto_discard)} posts (score <= 2 or disqualified)")
    print(f"\n  Sample AUTO-KEEP titles:")
    for e in auto_keep[:5]:
        print(f"    [{e['score']['total']:>2}] {e['post']['title'][:70]}")
    print(f"\n  Sample AUTO-DISCARD titles:")
    for e in auto_discard[:5]:
        t = e['post']['title'][:60]
        r = e['score']['disqualify_reason'][:40]
        print(f"    [{e['score']['total']:>2}] {t} | reason: {r}")

    # ── MANUAL REVIEW ──────────────────────────────────────────
    manual_decisions = {}
    if borderline:
        print(f"\n  {len(borderline)} posts need your manual review.")
        ans = input("  Start manual review now? [Y/N]: ").strip().upper()
        if ans == "Y":
            manual_decisions = manual_review_session(borderline)
        else:
            print("  Skipping manual review. Borderline posts will be marked SKIP.")

    # ── COMPILE FINAL DECISIONS ────────────────────────────────
    final = []
    for e in auto_keep:
        final.append({
            "id":              e["post"]["id"],
            "title":           e["post"]["title"],
            "url":             e["post"].get("url", ""),
            "verdict":         "KEEP",
            "relevance_score": e["score"]["total"],
            "matched":         ", ".join(e["score"]["matched"][:8]),
            "is_clean":        True,
        })

    for e in borderline:
        pid = e["post"]["id"]
        decision = manual_decisions.get(pid, "SKIP")
        final.append({
            "id":              pid,
            "title":           e["post"]["title"],
            "url":             e["post"].get("url", ""),
            "verdict":         decision,
            "relevance_score": e["score"]["total"],
            "matched":         ", ".join(e["score"]["matched"][:8]),
            "is_clean":        decision == "KEEP",
        })

    for e in auto_discard:
        final.append({
            "id":              e["post"]["id"],
            "title":           e["post"]["title"],
            "url":             e["post"].get("url", ""),
            "verdict":         "DISCARD",
            "relevance_score": e["score"]["total"],
            "matched":         e["score"]["disqualify_reason"],
            "is_clean":        False,
        })

    keep_count    = sum(1 for f in final if f["verdict"] == "KEEP")
    discard_count = sum(1 for f in final if f["verdict"] == "DISCARD")
    skip_count    = sum(1 for f in final if f["verdict"] == "SKIP")

    print(f"\n{'='*60}")
    print(f"  VALIDATION SUMMARY")
    print(f"{'='*60}")
    print(f"  Total posts    : {len(final)}")
    print(f"  KEEP           : {keep_count}")
    print(f"  DISCARD        : {discard_count}")
    print(f"  SKIP (review)  : {skip_count}")
    print(f"  Clean dataset  : {keep_count} posts")
    print(f"{'='*60}")

    # ── SAVE EXCEL REPORT ─────────────────────────────────────
    df = pd.DataFrame(final)
    df = df.sort_values("relevance_score", ascending=False)
    df.to_excel(EXCEL_REPORT, index=False)
    print(f"\n  Report saved to: {EXCEL_REPORT}")
    print(f"  Open this to review/change decisions before writing to Supabase.")

    # ── WRITE TO SUPABASE ─────────────────────────────────────
    ans = input("\n  Write results to Supabase now? [Y/N]: ").strip().upper()
    if ans != "Y":
        print("  Skipped. Run again and choose Y when ready.")
        return

    print(f"\n  Writing to Supabase...")
    success = 0
    errors  = 0
    for i, f in enumerate(final):
        updates = {
            "is_clean":        f["is_clean"],
            "relevance_score": f["relevance_score"],
        }
        ok = update_post_in_supabase(f["id"], updates)
        if ok:
            success += 1
        else:
            errors += 1
        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(final)} updated...")
        time.sleep(0.05)  # avoid rate limiting

    print(f"\n  Done. {success} updated, {errors} errors.")
    print(f"\n  NEXT STEPS:")
    print(f"  1. Review {EXCEL_REPORT} — change any wrong verdicts")
    print(f"  2. Run nlp_batch_processor.py to pre-compute sentiment")
    print(f"     on all is_clean=true posts")
    print(f"  3. Update main.py to read pre-computed values from DB")


if __name__ == "__main__":
    run_validation()
