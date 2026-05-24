"""
SentiMap Data Validator v4.0 — Final God Mode
===============================================
Research: "Geospatial Sentiment Analysis: A Hybrid NLP Approach for
Mapping Traffic Enforcement Grievances in Cebu City"

HOW THIS VALIDATOR CAME TO BE — METHODOLOGY DOCUMENTATION
==========================================================
This validator was developed through iterative refinement across
four versions, each informed by manual review of borderline posts.

Version 1 (baseline): Simple keyword scoring, 142 clean posts
  Problem: 81% discard rate, many valid posts auto-discarded

Version 2: Added 4-layer scoring, manual review of 61 posts
  Problem: BRT posts scoring 3 → REVIEW; LTO admin questions scoring 6 → KEEP
  Problem: "animal", "plete", "baha", "counterflow" false positives
  Problem: Same posts appearing in manual review repeatedly

Version 3: 7 false-positive patterns fixed, 32 manual reviews
  Problem: BRT/CITOM posts still landed in REVIEW (score 3)
  Problem: Checkpoint admin questions scoring 4 → REVIEW every time
  Problem: Transport grievance posts (taxi/traffic) scoring 5 → REVIEW
  Problem: Duplicate body posts passing GUARANTEED_KEEP via BRT keyword

Version 4 (this file): Complete pipeline redesign
  FIX 1: GUARANTEED_KEEP list — unambiguous Cebu traffic terms auto-keep
  FIX 2: ADMINISTRATIVE_PATTERNS check BEFORE GUARANTEED_KEEP
  FIX 3: Correct pipeline ORDER — duplicates killed before GUARANTEED_KEEP
  FIX 4: STRONG_TRANSPORT_ANCHOR auto-keep for D2≥2+D3≥1+anchor
  FIX 5: LTO grievance bonus — confirmed LTO grievances get +2 D1 bonus
  FIX 6: "uso ba", "mangutana" added to administrative pattern killers
  FIX 7: Historical inquiry patterns added to title disqualifiers
  FIX 8: "what happened to", "history of" title disqualifiers
  FIX 9: National politics expanded disqualifiers
  FIX 10: "reklamo" context-check (only scores with transport context)

PIPELINE ORDER (critical — order determines correctness):
  Step 1:  Duplicate/empty body check          → DISCARD
  Step 2:  Administrative pattern check        → DISCARD
  Step 3:  Title disqualifiers                 → DISCARD
  Step 4:  Body/full-text disqualifiers        → DISCARD
  Step 5:  Subreddit gate (r/Philippines)      → DISCARD
  Step 6:  GUARANTEED_KEEP check               → AUTO-KEEP
  Step 7:  Normal D1/D2/D3/D4 scoring
  Step 8:  LTO grievance gate + bonus          → score adjustment
  Step 9:  Pattern E: D3 neutering             → score adjustment
  Step 10: Strong transport anchor check       → AUTO-KEEP if qualified
  Step 11: Final threshold verdict
"""

import os
import re
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ── ENV LOADING ───────────────────────────────────────────────
for env_path in [
    os.path.join(os.path.dirname(__file__), "..", "app", ".env"),
    os.path.join(os.path.dirname(__file__), ".env"),
    os.path.join(os.path.dirname(__file__), "..", ".env"),
]:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        break

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
HEADERS = {
    "apikey":        SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type":  "application/json",
}
EXCEL_REPORT = "validation_report_v4.xlsx"
HTTP_TIMEOUT = (5, 45)
HTTP_RETRIES = 5
HTTP_BACKOFF_SECONDS = 1.5
# If non-empty, only these post IDs will be written to Supabase.
# Clear the list ([]) for a full update.
RETRY_ONLY_IDS = []

def request_with_retry(method: str, url: str, **kwargs):
    """Basic retry wrapper to handle transient Supabase timeouts."""
    timeout = kwargs.pop("timeout", HTTP_TIMEOUT)
    last_exc = None
    for attempt in range(1, HTTP_RETRIES + 1):
        try:
            return requests.request(method, url, timeout=timeout, **kwargs)
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < HTTP_RETRIES:
                time.sleep(HTTP_BACKOFF_SECONDS * attempt)
    raise last_exc


# ═════════════════════════════════════════════════════════════
# SCORING DICTIONARIES
# D1 - Enforcement signal   (max 10) ← most important
# D2 - Public transport     (max 6)
# D3 - Sentiment/grievance  (max 4)
# D4 - Location specificity (max 3)
# AUTO-KEEP threshold:    total >= 6
# MANUAL REVIEW:          total 3-5
# AUTO-DISCARD:           total <= 2
# ═════════════════════════════════════════════════════════════

ENFORCEMENT_KEYWORDS = {
    # Agencies
    "CITOM":               5,
    "CCTO":                5,
    "LTFRB":               5,
    "LTO":                 2,    # Low — needs grievance signal to compound
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
    "counterflow":         4,    # word boundary enforced
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
    "license":             2,    # word boundary enforced
    "plate number":        2,
    # Policy/schemes
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
    # Infrastructure/accidents
    "roadwork":            3,
    "accident":            3,
    "disgrasya":           3,
    "bangga":              3,
}

TRANSPORT_KEYWORDS = {
    "jeepney":          3,
    "jeep driver":      3,
    "jeep conductor":   2,
    "bus driver":       2,
    "bus conductor":    2,
    "taxi driver":      3,
    "taxi meter":       4,
    "overcharging":     3,
    "fare hike":        3,
    "fare increase":    3,
    "PUV":              2,
    "public utility":   2,
    "angkas":           2,
    "grab driver":      2,
    "habal-habal":      2,
    "move it":          2,
    "commute":          2,    # word boundary enforced
    "commuting":        2,    # word boundary enforced
    "commuter":         2,    # word boundary enforced
    "commuters":        2,    # word boundary enforced
    "pasahero":         2,
    "plite":            2,    # word boundary enforced — NOT inside "complete"
    "byahe":            1,
    "sakay":            1,
    "sakyanan":         1,
    "trapik":           2,
    "karsada":          1,
    "traffic":          3,
    "heavy traffic":    4,
    "bumper to bumper": 4,
    "congestion":       3,
    "gridlock":         4,
    "slow moving":      3,
}

SENTIMENT_KEYWORDS = {
    # Sarcasm markers — highest research value
    "hayahay":             4,
    "hayahay kaayo":       4,
    "so comfortable":      3,
    "smooth ra":           3,
    "kanus-a pa kaha":     3,
    "hahayz":              3,
    "counterproductive":   3,
    # Strong Cebuano negative — from validated post corpus
    "makalagot":           2,
    "makaguol":            2,
    "nasukaon":            2,
    "naratol":             2,
    "kapoy na":            2,
    "kapoy kaayo":         2,
    "puryagaba":           3,    # added from manual review — Cebu Safari incident
    "hangak":              2,
    "luod":                2,    # appeared in "aircon bus" post
    "di na kaya":          2,
    "dili na kaya":        2,
    "yawa":                1,
    "bwisit":              1,
    "piste":               1,
    "grabe":               1,
    "grabeh":              1,
    "grabi":               1,
    "samok":               2,
    "dugay kaayo":         2,
    "alimuot":             2,
    "trapik kaayo":        3,
    "walay klaro":         3,
    "piskot":              2,
    "atay":                2,
    "buang":               2,
    "hasol":               2,
    "giatay":              2,
    "maungot":             2,    # appeared in "wala nay traffic gabii" post
    "gikapoy":             2,    # appeared in "carpool south" post
    "gi kapoy":            2,    # variant
    # English grievance terms
    "annoying":            2,
    "frustrating":         2,
    "ridiculous":          2,
    "terrible":            2,
    "worst":               2,
    "unacceptable":        2,
    "incompetent":         2,
    # Complaint/accountability framing
    "sumbong":             2,
    "complain":            1,
    "asa ko mu-report":    3,
    "asa ta maka-reklamo": 3,
    # NOTE: "animal" REMOVED — fires on Cebu Safari, literal animals
    # NOTE: "report" REMOVED — fires on news reports
    # NOTE: "reklamo" REMOVED from here — context-checked separately below
}

LOCATION_KEYWORDS = {
    "SRP":              2, "south road":       2,
    "Mambaling":        2, "Talamban":         2,
    "Lahug":            2, "IT Park":          2,
    "Fuente":           2, "Fuente Osmena":    2,
    "Fuente Osmeña":    2, "Mandaue":          2,
    "Mactan":           2, "Consolacion":      2,
    "Talisay":          2, "Bulacao":          2,
    "Banawa":           2, "Guadalupe":        2,
    "Basak":            2, "Salinas":          2,
    "Bacalso":          2, "Transcentral":     2,
    "Pardo":            2, "Capitol":          2,
    "Gorordo":          2, "Archbishop Reyes": 2,
    "Jones Ave":        2, "Escario":          2,
    "Urgello":          2, "Subangdaku":       2,
    "Hernan Cortes":    2, "A.S. Fortuna":     2,
    "Osmeña Blvd":      2, "Osmeña Boulevard": 2,
    "Mango Avenue":     2, "Mango Ave":        2,
    "Colon":            1, "Ayala":            1,
    "Carbon":           1, "Cebu City":        1,
}

# ═════════════════════════════════════════════════════════════
# STEP 6: GUARANTEED_KEEP
# Keywords so domain-specific to Cebu traffic enforcement that
# their presence ALONE means AUTO-KEEP — no scoring needed.
# These have ZERO off-topic use in Cebu Reddit context.
# Applied AFTER Steps 1-5 (so duplicates/admin questions die first).
# ═════════════════════════════════════════════════════════════
GUARANTEED_KEEP_KEYWORDS = [
    # Cebu-specific enforcement agencies
    "CITOM", "CCTO",
    # Cebu-specific transport project — every BRT post is research-relevant
    "BRT", "bus rapid transit", "CBRT",
    # Unambiguous enforcement actions
    "traffic enforcer", "traffic enforcement",
    "naapprehend", "giapprehend",
    "colorum", "smoke belching",
    "reckless driving", "reckless driver",
    "counterflow",
    # Unambiguous violations/policy
    "one way scheme", "one-way scheme",
    "road rage",
    # Specific Cebu transport terms with no off-topic use
    "habal-habal",
    "paasa",       # empty promise — often about BRT
    # Taxi franchise/policy (EV taxi approvals)
    "ev taxi",
    "taxi franchise",
    "provisional authority",
    # Ride-hailing driver safety complaints
    "grab car",
    "grab driver",
    # Specific violations/complaint phrases that should override title filters
    "fast timer",
    "fast timers",
    "taxi meter",
    "timer niya kusog",
    "kusog ang timer",
    "daghan na taxi",
    "nag-report",
    "nagsumbong",
    "asa mu-report",
    "asa ko mu-reklamo",
    # Road safety incidents
    "motorcycle accident",
]

# ═════════════════════════════════════════════════════════════
# STEP 2: ADMINISTRATIVE PATTERNS
# Checked BEFORE GUARANTEED_KEEP — kills informational questions
# even when they contain guaranteed keywords.
# Example: "Is CITOM open on Sunday?" → killed here before CITOM
#          triggers GUARANTEED_KEEP.
# ═════════════════════════════════════════════════════════════
ADMINISTRATIVE_PATTERNS = [
    # Cebuano question openers
    "uso ba", "uso ba ang",          # "is it common/practiced?" — asking
    "open ba", "bukas ba",           # is it open?
    "mangutana", "mu-ask", "mag-ask", # asking/inquiry
    "asking if", "asking for",
    "inquiry on", "question about",
    # Process/procedure questions
    "how to get", "tips on getting", "tips on how",
    "what are the requirements", "unsa ang requirements",
    "how do i", "how do you",
    "puwede ba", "pwede ba",         # "is it possible/allowed?"
    "kaya ba", "mahimo ba",          # "can I?" — permission questions
    "appointment online",
    "slots occupied",
    "online renewal",
    "mag set ug appointment",
    "mag-set ng appointment",
    "naa bay slot",
    "naa bay dakop",
    "mu ask lang unta",
    "do i still need",
    "still need to",
    # Contact/location questions
    "phone number", "contact number", "landline", "hotline",
    "where is the", "asa ang", "asa na ang",
    "nearest branch", "branch sa",
    "where to report lost", "where to report found",
    "where to find",
    # Historical inquiry (not current grievance)
    "what happened to",
    "history of",
    "before ww2", "before world war",
    "right-of-way",                  # historical/technical
    "old maps",
    # Scheduling/availability
    "anong oras", "unsa oras", "what time",
    "ilang oras", "may appointment",
    "schedule ba",
    # Career/personal advice (not traffic)
    "mangayo rakog honest opinion",
    "honest opinion",
    "need advice", "need help with",
    "ano ang advice",
]


# ═════════════════════════════════════════════════════════════
# STEP 3: TITLE-ONLY DISQUALIFIERS
# Post discarded if title contains ANY of these.
# (Events like sinulog moved here — body mentions are allowed)
# ═════════════════════════════════════════════════════════════
TITLE_DISQUALIFIERS = [
    # LTO administrative — all variants seen in manual review
    "asa na lto", "lto branch", "lto office",
    "lto nonpro", "lto dl", "lto or/cr",
    "or/cr", "mag pa-lto", "mag register ng",
    "driver's license renewal", "dl renewal",
    "applying for a", "applying for driver",
    "for registration license",
    "adding driver", "driver's license restriction",
    "plastic license", "plastic driver",
    "naa na ba lto", "na ana bay nakakuha",
    "lto branch walkin", "walkin sp to dl",
    "nonpro license question",
    # Direction/navigation questions
    "how to commute to", "how to commute from",
    "directions to", "where to buy", "where to find",
    "asa makapalit", "asa makita",
    # Looking for something
    "recommendation for", "looking for",
    "best place", "good place",
    "cafe reco", "cafe recos",
    "food reco", "food recos",
    "restaurant reco",
    # Events (title only — body mentions of sinulog are okay)
    "sinulog", "sinulog festival",
    "festival", "concert", "music scene",
    "christmas party", "new year party",
    # Classifieds/jobs
    "for sale", "for rent",
    "hiring", "job opening", "apply now",
    # Appreciation/meta
    "appreciation post", "shoutout",
    # Safari/tourism inquiry
    "cebu safari",
    # Medical inquiry
    "inquiry on ct scan", "ct scan prices",
    "animal bite center",
]


# ═════════════════════════════════════════════════════════════
# STEP 4: BODY DISQUALIFIERS
# Checked against full text — things NEVER relevant in any context
# ═════════════════════════════════════════════════════════════
DISQUALIFIERS = [
    # Food
    "lechon", "carcar lechon", "chicharon",
    "milk tea", "boba", "food review", "where to eat",
    "cafe reco", "cafe recos", "coffee shop",
    # Shopping
    "for sale", "bedspace", "roommate", "ukay", "thrift",
    # Entertainment
    "movie", "kdrama", "netflix", "anime",
    # Personal/relationship
    "breakup", "break up", "boyfriend", "girlfriend",
    "crush", "hugot", "valentines", "love life", "kilig",
    "wedding", "birthday party", "anniversary",
    # Jobs
    "job opening", "job vacancy", "work from home",
    # Medical (non-accident)
    "anti-rabies", "kidney stone",
    "hospital recommendation", "doctor reco",
    # Gaming
    "nintendo", "playstation",
    # National politics
    "impeach", "impeachment",
    "sara duterte", "vice president sara",
    "senate bill", "house bill",
    # Image-only posts (Pattern C)
    "preview.redd.it",
    "i.redd.it",
    # Tourism
    "tourist spot", "beach resort", "hotel recommendation",
    "travel itinerary", "where to stay",
    # Crime unrelated to traffic
    "murder", "rape", "robbery",
    # Music events
    "singer-songwriter", "live performance",
    # Wrong geography — Manila-specific
    "metro manila", "edsa", "mmda", "lrt ", "mrt ",
    "makati", "quezon city", "pasig", "taguig",
]


# ═════════════════════════════════════════════════════════════
# GRIEVANCE SIGNALS
# Used for LTO gate: LTO posts need at least one of these
# to be considered a grievance (not informational)
# ═════════════════════════════════════════════════════════════
GRIEVANCE_SIGNALS = [
    "grabe", "grabi", "grabeh", "yawa", "bwisit", "piste",
    "makalagot", "makaguol", "nasukaon", "kapoy",
    "puryagaba", "annoying", "frustrating", "unfair",
    "unjust", "corrupt", "abuso", "maungot",
    "apprehended", "giapprehend", "naapprehend",
    "kotong", "hulidap", "extort", "bribe", "lagay",
    "delayed", "dugay kaayo", "grabe ang delay",
    "counterproductive", "inefficient", "incompetent",
    "walay klaro", "walay sense", "ngano wala", "ngano dili",
    "dili na kaya", "di na kaya",
]


# ═════════════════════════════════════════════════════════════
# LTO ENFORCEMENT-SPECIFIC SIGNALS
# Only these count as true enforcement grievances for LTO posts.
# Prevents admin questions from passing on generic frustration.
# ═════════════════════════════════════════════════════════════
LTO_ENFORCEMENT_SIGNALS = [
    "apprehend", "giapprehend", "naapprehend",
    "kotong", "hulidap", "extort", "bribe", "lagay",
    "abuso", "corrupt", "corruption",
    "no plate no travel", "delayed ang plaka",
    "grabe ang delay", "sobra delayed",
    "counterproductive", "unfair", "unjust",
    "nakulit", "gi-kulit", "nabayran",
]


# ═════════════════════════════════════════════════════════════
# STRONG TRANSPORT ANCHORS
# For Step 10: D2≥2 + D3≥1 + one of these = AUTO-KEEP
# These are specific transport service/vehicle terms that
# confirm the post is genuinely about transport, not generic.
# Excludes generic words like "sakay", "byahe" that appear
# in tourism/food contexts too.
# ═════════════════════════════════════════════════════════════
STRONG_TRANSPORT_ANCHORS = {
    "jeepney", "jeep driver", "jeep conductor",
    "taxi driver", "taxi meter",
    "bus driver", "bus conductor",
    "bus", "ceres", "ceres bus",
    "angkas", "grab driver", "move it", "habal-habal",
    "commute", "commuting", "commuter", "commuters",
    "pasahero", "trapik", "traffic",
    "PUV", "public utility vehicle",
    "overcharging", "fare hike", "fare increase",
    "plite",                    # word boundary checked
}

# Subreddit references for r/Philippines gate
CEBU_REFERENCES = [
    "cebu", "sugbo", "cebuana", "cebuano",
    "bisaya", "bislish", "cebu city",
]
TRAFFIC_REFERENCES = [
    "traffic", "trapik", "commute", "enforcer",
    "BRT", "CITOM", "LTO", "LTFRB",
    "jeepney", "angkas", "grab", "taxi",
    "bus", "checkpoint",
]


# ═════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═════════════════════════════════════════════════════════════

def has_word(text: str, word: str) -> bool:
    """Word boundary check — prevents 'plete' matching inside 'complete'."""
    pattern = r'(?<![a-zA-Z])' + re.escape(word) + r'(?![a-zA-Z])'
    return bool(re.search(pattern, text, re.IGNORECASE))


# Keywords requiring word boundary matching
BOUNDARY_REQUIRED = {
    "plite", "plete", "counterflow", "license",
    "baha", "flood", "construction",
    "commute", "commuter", "commuting", "commuters",
    "traffic",   # prevents matching inside "trafficking"
}


def is_duplicate_or_empty(title: str, body: str) -> tuple:
    """Step 1: Detect empty, duplicate, or image-only posts."""
    title_clean = title.strip().lower()
    body_clean  = body.strip().lower()

    # Both title and body too short — no content
    if not body_clean or len(body_clean) < 20:
        if len(title_clean) < 30:
            return True, "empty: title+body both too short"

    # Body is verbatim copy of title
    if body_clean and title_clean:
        t = re.sub(r'\s+', ' ', title_clean)
        b = re.sub(r'\s+', ' ', body_clean[:len(t) + 10])
        if t == b or (len(t) > 15 and t in b[:len(t) + 5]):
            return True, "duplicate: body repeats title verbatim"

    # Body is only URLs (image-only post)
    body_no_urls = re.sub(r'http\S+', '', body_clean).strip()
    body_no_urls = re.sub(r'&amp;\S*', '', body_no_urls).strip()
    body_no_urls = re.sub(r'\s+', ' ', body_no_urls).strip()
    if body and len(body_no_urls) < 15:
        return True, "image_only: body contains only URLs"

    return False, ""


def has_administrative_pattern(title: str, body: str) -> tuple:
    """
    Step 2: Check for administrative/informational question patterns.
    Checks title first (stronger signal), then first 150 chars of body.
    Returns (is_admin, matched_pattern)
    """
    title_lower = title.lower()
    # Short body prefix — admin questions reveal themselves early
    body_prefix = body[:150].lower()

    for pattern in ADMINISTRATIVE_PATTERNS:
        if pattern.lower() in title_lower:
            return True, f"title_admin: '{pattern}'"
        if pattern.lower() in body_prefix:
            return True, f"body_admin: '{pattern}'"
    return False, ""


def passes_subreddit_gate(post: dict) -> tuple:
    """
    Step 5: r/Philippines posts need Cebu + traffic context.
    r/Cebu posts always pass.
    """
    url       = post.get("url", "").lower()
    subreddit = post.get("subreddit", "").lower()

    is_ph = "r/philippines" in url or subreddit == "philippines"
    if not is_ph:
        return True, ""

    full_text   = (post.get("full_text") or "").lower()
    has_cebu    = any(r in full_text for r in CEBU_REFERENCES)
    has_traffic = any(r.lower() in full_text for r in TRAFFIC_REFERENCES)

    if has_cebu and has_traffic:
        return True, ""
    return False, "r/Philippines post lacks Cebu+traffic context"


def check_guaranteed_keep(full_text: str) -> tuple:
    """
    Step 6: Check if post contains a GUARANTEED_KEEP keyword.
    These are unambiguous Cebu traffic terms — no off-topic use.
    Returns (is_guaranteed, matched_keyword)
    """
    text_lower = full_text.lower()
    for kw in GUARANTEED_KEEP_KEYWORDS:
        # Use word boundary for short/ambiguous terms
        if len(kw) <= 4:
            if has_word(text_lower, kw):
                return True, kw
        else:
            if kw.lower() in text_lower:
                return True, kw
    return False, ""


def lto_has_grievance(text: str) -> bool:
    """
    Step 8: LTO posts need enforcement-specific grievance signals.
    Prevents admin/informational LTO posts from passing on generic sentiment.
    """
    text_lower = text.lower()
    return any(s.lower() in text_lower for s in LTO_ENFORCEMENT_SIGNALS)


def has_strong_transport_anchor(text: str) -> bool:
    """
    Step 10: Check for specific transport vehicle/service terms.
    These confirm D2 matches are about actual transport, not generic.
    """
    text_lower = text.lower()
    for anchor in STRONG_TRANSPORT_ANCHORS:
        if anchor in BOUNDARY_REQUIRED:
            if has_word(text_lower, anchor):
                return True
        else:
            if anchor.lower() in text_lower:
                return True
    return False


def check_reklamo_context(text: str) -> bool:
    """
    "Reklamo" only scores if transport/enforcement context present.
    Prevents "reklamo sa trabaho" from scoring D3.
    """
    text_lower = text.lower()
    transport_context = [
        "traffic", "trapik", "commute", "jeepney", "taxi",
        "bus", "angkas", "grab", "enforcer", "CITOM", "LTO",
        "LTFRB", "CCTO", "dalan", "karsada", "byahe",
    ]
    return any(ctx.lower() in text_lower for ctx in transport_context)


# ═════════════════════════════════════════════════════════════
# MAIN SCORER — 11-step pipeline
# ═════════════════════════════════════════════════════════════
def score_post(title: str, body: str, full_text: str,
               post: dict = None) -> dict:

    text_lower  = full_text.lower()
    title_lower = title.lower()

    result = {
        "d1_enforcement": 0, "d2_transport": 0,
        "d3_sentiment":   0, "d4_location":  0,
        "total":          0, "matched":      [],
        "disqualified":   False,
        "disqualify_reason": "",
        "verdict":        "",
        "guaranteed":     False,
    }

    # ── STEP 1: Duplicate/empty check ────────────────────────
    is_dup, dup_reason = is_duplicate_or_empty(title, body)
    if is_dup:
        result.update({"disqualified": True,
                       "disqualify_reason": dup_reason,
                       "verdict": "DISCARD"})
        return result

    # ── STEP 2: Administrative pattern check ─────────────────
    # MUST run before GUARANTEED_KEEP
    # "Is CITOM open on Sunday?" must die here before step 6
    is_admin, admin_reason = has_administrative_pattern(title, body)
    if is_admin:
        result.update({"disqualified": True,
                       "disqualify_reason": admin_reason,
                       "verdict": "DISCARD"})
        return result

    # ── STEP 3: Title disqualifiers ──────────────────────────
    for kw in TITLE_DISQUALIFIERS:
        if kw.lower() in title_lower:
            result.update({"disqualified": True,
                           "disqualify_reason": f"title_disqualifier: '{kw}'",
                           "verdict": "DISCARD"})
            return result

    # ── STEP 4: Body/full-text disqualifiers ─────────────────
    for kw in DISQUALIFIERS:
        if kw in ("preview.redd.it", "i.redd.it"):
            if kw in text_lower:
                result.update({"disqualified": True,
                               "disqualify_reason": f"image_only: '{kw}'",
                               "verdict": "DISCARD"})
                return result
        else:
            if kw.lower() in text_lower:
                result.update({"disqualified": True,
                               "disqualify_reason": f"disqualifier: '{kw}'",
                               "verdict": "DISCARD"})
                return result

    # ── STEP 5: Subreddit gate ───────────────────────────────
    if post:
        passes, gate_reason = passes_subreddit_gate(post)
        if not passes:
            result.update({"disqualified": True,
                           "disqualify_reason": gate_reason,
                           "verdict": "DISCARD"})
            return result

    # ── STEP 6: GUARANTEED_KEEP ──────────────────────────────
    # Only reached if steps 1-5 all passed
    is_guaranteed, guaranteed_kw = check_guaranteed_keep(full_text)
    if is_guaranteed:
        result.update({
            "verdict": "KEEP",
            "guaranteed": True,
            "total": 10,   # high score for reporting clarity
            "matched": [f"GUARANTEED:{guaranteed_kw}"],
        })
        return result

    # ── STEP 7: Normal D1/D2/D3/D4 scoring ──────────────────

    # D1 Enforcement
    for kw, pts in ENFORCEMENT_KEYWORDS.items():
        if kw in BOUNDARY_REQUIRED:
            matched = has_word(text_lower, kw)
        else:
            matched = kw.lower() in text_lower
        if matched:
            result["d1_enforcement"] = min(
                result["d1_enforcement"] + pts, 10
            )
            result["matched"].append(f"D1+{pts}:{kw}")

    # D2 Transport
    for kw, pts in TRANSPORT_KEYWORDS.items():
        if kw in BOUNDARY_REQUIRED:
            matched = has_word(text_lower, kw)
        else:
            matched = kw.lower() in text_lower
        if matched:
            result["d2_transport"] = min(
                result["d2_transport"] + pts, 6
            )
            result["matched"].append(f"D2+{pts}:{kw}")

    # D3 Sentiment
    for kw, pts in SENTIMENT_KEYWORDS.items():
        if kw.lower() in text_lower:
            result["d3_sentiment"] = min(
                result["d3_sentiment"] + pts, 4
            )
            result["matched"].append(f"D3+{pts}:{kw}")

    # D3 special: "reklamo" — only if transport context present
    if "reklamo" in text_lower and check_reklamo_context(full_text):
        result["d3_sentiment"] = min(result["d3_sentiment"] + 2, 4)
        result["matched"].append("D3+2:reklamo(context)")

    # D4 Location
    for kw, pts in LOCATION_KEYWORDS.items():
        if kw.lower() in text_lower:
            result["d4_location"] = min(
                result["d4_location"] + pts, 3
            )
            result["matched"].append(f"D4+{pts}:{kw}")

    # ── STEP 8: LTO grievance gate + bonus ───────────────────
    lto_in_match = any("LTO" in m for m in result["matched"])
    if lto_in_match:
        if lto_has_grievance(full_text):
            # Confirmed LTO grievance — give bonus to push over threshold
            result["d1_enforcement"] = min(
                result["d1_enforcement"] + 2, 10
            )
            result["matched"].append("NOTE:LTO_grievance_confirmed+2")
        else:
            # Administrative LTO mention — neuter the score
            result["d1_enforcement"] = max(
                result["d1_enforcement"] - 2, 0
            )
            result["matched"].append("NOTE:LTO_admin_neutered-2")

    # ── STEP 9: Pattern E — D3 neutering ─────────────────────
    # Frustration must co-occur with transport/enforcement
    # Prevents "naratol sa ubang pasahero" scoring D3
    if (result["d3_sentiment"] > 0 and
            result["d1_enforcement"] == 0 and
            result["d2_transport"] == 0):
        result["d3_sentiment"] = 0
        result["matched"].append("NOTE:D3_neutered_no_domain")

    # ── STEP 10: Strong transport anchor AUTO-KEEP ───────────
    # D2≥2 + D3≥1 + specific transport anchor = confirmed grievance
    if (result["d2_transport"] >= 2 and
            result["d3_sentiment"] >= 1 and
            has_strong_transport_anchor(full_text)):
        result.update({
            "verdict": "KEEP",
            "total": result["d1_enforcement"] + result["d2_transport"] +
                     result["d3_sentiment"] + result["d4_location"],
            "matched": result["matched"] + ["AUTO-KEEP:transport_anchor"],
        })
        return result

    # ── STEP 11: Final threshold verdict ─────────────────────
    has_enforcement = result["d1_enforcement"] >= 3
    has_transport_grievance = (result["d2_transport"] >= 2 and
                               result["d3_sentiment"] >= 1)

    if not has_enforcement and not has_transport_grievance:
        result.update({
            "disqualified": True,
            "disqualify_reason": "no enforcement or transport+grievance",
            "verdict": "DISCARD",
            "total": result["d1_enforcement"] + result["d2_transport"],
        })
        return result

    total = (result["d1_enforcement"] + result["d2_transport"] +
             result["d3_sentiment"]   + result["d4_location"])
    result["total"] = total
    result["verdict"] = ("KEEP"   if total >= 6 else
                         "REVIEW" if total >= 3 else "DISCARD")
    return result


# ═════════════════════════════════════════════════════════════
# SUPABASE OPERATIONS
# ═════════════════════════════════════════════════════════════
def load_all_posts() -> list:
    all_posts = []
    offset    = 0
    limit     = 200
    print("  Loading posts from Supabase...")
    while True:
        url    = f"{SUPABASE_URL}/rest/v1/posts"
        params = {
            "select": ("id,title,body,full_text,locations,url,"
                       "upvotes,num_comments,created_date,subreddit"),
            "offset": offset, "limit": limit,
            "order":  "created_date.desc",
        }
        try:
            resp = request_with_retry("GET", url, headers=HEADERS, params=params)
        except requests.exceptions.RequestException as exc:
            print(f"  ERROR loading posts: {exc}")
            break
        if resp.status_code != 200:
            print(f"  ERROR: {resp.status_code} — {resp.text[:200]}")
            break
        batch = resp.json()
        if not batch:
            break
        all_posts.extend(batch)
        offset += limit
        if len(batch) < limit:
            break
    print(f"  Loaded {len(all_posts)} posts")
    return all_posts


def update_post(post_id: str, updates: dict) -> bool:
    url    = f"{SUPABASE_URL}/rest/v1/posts"
    params = {"id": f"eq.{post_id}"}
    try:
        resp = request_with_retry(
            "PATCH",
            url,
            headers=HEADERS,
            params=params,
            json=updates,
        )
        return resp.status_code in (200, 204)
    except requests.exceptions.RequestException as exc:
        print(f"  ERROR updating {post_id}: {exc}")
        return False


# ═════════════════════════════════════════════════════════════
# MANUAL REVIEW SESSION
# ═════════════════════════════════════════════════════════════
def manual_review_session(borderline: list) -> dict:
    decisions = {}
    total     = len(borderline)
    print(f"\n{'='*60}")
    print(f"  MANUAL REVIEW — {total} borderline posts")
    print(f"  K=Keep  D=Discard  S=Skip  Q=Quit")
    print(f"  KEEP if: traffic/commute GRIEVANCE in Cebu")
    print(f"  DISCARD if: just asking, wrong topic, wrong geography")
    print(f"{'='*60}\n")

    for i, item in enumerate(borderline):
        post  = item["post"]
        score = item["score"]
        pid   = post.get("id", "")
        title = post.get("title", "")
        body  = (post.get("body") or post.get("full_text") or "")

        print(f"\n[{i+1}/{total}] Score:{score['total']}/23  "
              f"D1={score['d1_enforcement']} "
              f"D2={score['d2_transport']} "
              f"D3={score['d3_sentiment']} "
              f"D4={score['d4_location']}")
        print(f"  TITLE  : {title}")
        print(f"  BODY   : {body[:220]}"
              f"{'...' if len(body) > 220 else ''}")
        print(f"  MATCHED: {', '.join(score['matched'][:6])}")
        print(f"  URL    : {post.get('url', '')}")

        while True:
            choice = input("  [K/D/S/Q]: ").strip().upper()
            if choice in ("K", "D", "S", "Q"):
                break
        if choice == "Q":
            print("  Quit — remaining posts marked SKIP.")
            break
        decisions[pid] = {"K": "KEEP", "D": "DISCARD", "S": "SKIP"}[choice]
        print(f"  → {decisions[pid]}")

    return decisions


# ═════════════════════════════════════════════════════════════
# MAIN VALIDATION RUNNER
# ═════════════════════════════════════════════════════════════
def run_validation():
    print("=" * 60)
    print("  SentiMap Data Validator v4.0 — Final God Mode")
    print("  11-step pipeline | all manual review lessons applied")
    print("=" * 60)

    posts = load_all_posts()
    if not posts:
        print("  No posts found. Check .env credentials.")
        return

    print(f"\n  Scoring {len(posts)} posts through 11-step pipeline...")

    auto_keep    = []
    borderline   = []
    auto_discard = []
    guaranteed_count = 0

    for post in posts:
        title     = post.get("title", "") or ""
        body      = post.get("body",  "") or ""
        full_text = post.get("full_text", "") or (title + " " + body)
        score     = score_post(title, body, full_text, post)
        entry     = {"post": post, "score": score}

        if score["verdict"] == "KEEP":
            auto_keep.append(entry)
            if score.get("guaranteed"):
                guaranteed_count += 1
        elif score["verdict"] == "REVIEW":
            borderline.append(entry)
        else:
            auto_discard.append(entry)

    print(f"\n  AUTO-KEEP    : {len(auto_keep)} posts")
    print(f"    (of which {guaranteed_count} via GUARANTEED_KEEP)")
    print(f"  NEED REVIEW  : {len(borderline)} posts (score 3-5)")
    print(f"  AUTO-DISCARD : {len(auto_discard)} posts")

    print(f"\n  Sample AUTO-KEEP:")
    for e in auto_keep[:10]:
        g = " [G]" if e["score"].get("guaranteed") else ""
        print(f"    [{e['score']['total']:>2}]{g} "
              f"{e['post']['title'][:60]}")

    print(f"\n  Sample AUTO-DISCARD:")
    for e in auto_discard[:8]:
        print(f"    [{e['score']['total']:>2}] "
              f"{e['post']['title'][:45]} | "
              f"{e['score']['disqualify_reason'][:30]}")

    # Manual review
    manual_decisions = {}
    if borderline:
        print(f"\n  {len(borderline)} posts need manual review.")
        ans = input("  Start now? [Y/N]: ").strip().upper()
        if ans == "Y":
            manual_decisions = manual_review_session(borderline)

    # Compile results
    final = []
    for e in auto_keep:
        final.append({
            "id":              e["post"]["id"],
            "title":           e["post"]["title"],
            "url":             e["post"].get("url", ""),
            "verdict":         "KEEP",
            "relevance_score": e["score"]["total"],
            "matched":         ", ".join(e["score"]["matched"][:8]),
            "guaranteed":      e["score"].get("guaranteed", False),
            "is_clean":        True,
        })
    for e in borderline:
        pid      = e["post"]["id"]
        decision = manual_decisions.get(pid, "SKIP")
        final.append({
            "id":              pid,
            "title":           e["post"]["title"],
            "url":             e["post"].get("url", ""),
            "verdict":         decision,
            "relevance_score": e["score"]["total"],
            "matched":         ", ".join(e["score"]["matched"][:8]),
            "guaranteed":      False,
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
            "guaranteed":      False,
            "is_clean":        False,
        })

    keep_count    = sum(1 for f in final if f["verdict"] == "KEEP")
    discard_count = sum(1 for f in final if f["verdict"] == "DISCARD")
    skip_count    = sum(1 for f in final if f["verdict"] == "SKIP")

    print(f"\n{'='*60}")
    print(f"  VALIDATION SUMMARY v4.0")
    print(f"{'='*60}")
    print(f"  Total posts    : {len(final)}")
    print(f"  KEEP           : {keep_count}")
    print(f"    Guaranteed   : {guaranteed_count}")
    print(f"    Transport    : {keep_count - guaranteed_count}")
    print(f"  DISCARD        : {discard_count}")
    print(f"  SKIP (review)  : {skip_count}")
    print(f"  Clean dataset  : {keep_count} posts")
    print(f"{'='*60}")
    print(f"\n  THESIS DOCUMENTATION:")
    print(f"  'Data validation used an 11-step pipeline with")
    print(f"  GUARANTEED_KEEP for unambiguous Cebu enforcement terms,")
    print(f"  strong transport anchor auto-keep, and administrative")
    print(f"  pattern elimination. {keep_count} posts retained from")
    print(f"  {len(final)} total ({round(100*keep_count/max(len(final),1))}% retention rate).'")

    # Save Excel report
    df = pd.DataFrame(final).sort_values(
        "relevance_score", ascending=False
    )
    df.to_excel(EXCEL_REPORT, index=False)
    print(f"\n  Report saved: {EXCEL_REPORT}")

    # Write to Supabase
    ans = input("\n  Write to Supabase now? [Y/N]: ").strip().upper()
    if ans != "Y":
        print("  Skipped.")
        return

    if RETRY_ONLY_IDS:
        final = [f for f in final if f["id"] in RETRY_ONLY_IDS]
        print(f"\n  Retrying only {len(final)} specified IDs...")

    print("\n  Writing to Supabase...")
    success = errors = 0
    for i, f in enumerate(final):
        ok = update_post(f["id"], {
            "is_clean":        f["is_clean"],
            "relevance_score": f["relevance_score"],
        })
        if ok: success += 1
        else:  errors  += 1
        if (i + 1) % 50 == 0:
            print(f"  {i+1}/{len(final)} updated...")
        time.sleep(0.05)

    print(f"\n  Done. {success} updated, {errors} errors.")
    print(f"\n  NEXT STEPS:")
    print(f"  1. Review {EXCEL_REPORT} — check sample of AUTO-KEEP")
    print(f"  2. Run nlp_batch_processor.py on is_clean=true posts")
    print(f"  3. Update main.py to read pre-computed NLP columns")
    print(f"  4. Restart backend — dashboard loads in <1 second")

if __name__ == "__main__":
    run_validation()