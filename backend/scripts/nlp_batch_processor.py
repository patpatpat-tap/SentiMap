"""
SentiMap NLP Batch Processor v2.0 — God Mode
==============================================
Pre-computes sentiment for all is_clean=true posts using the
updated CebuanoSentimentAnalyzer v2.0.

What's new in v2.0:
- Uses full_text (title + body) — not title only
- Captures sarcasm_triggers for research documentation
- Captures intensifiers_applied for methodology evidence
- Captures negations_applied for methodology evidence
- Detailed per-post logging so you can verify results
- Research summary report at the end
- Can re-run safely (overwrites previous NLP values)

Run from backend/scripts/:
    python nlp_batch_processor.py

Or with test mode to verify analyzer first:
    python nlp_batch_processor.py --test
"""

import os
import sys
import time
import json
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv

# ── PATH SETUP ────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
app_dir    = os.path.join(script_dir, "..", "app")
sys.path.insert(0, app_dir)
sys.path.insert(0, script_dir)

try:
    from sentiment_analyzer import CebuanoSentimentAnalyzer
    from location_extractor import CebuLocationExtractor
    print("  [OK] NLP modules loaded from app/")
except ImportError:
    try:
        from sentiment_analyzer import CebuanoSentimentAnalyzer
        from location_extractor import CebuLocationExtractor
        print("  [OK] NLP modules loaded (local)")
    except ImportError as e:
        print(f"  [ERROR] Could not load NLP modules: {e}")
        sys.exit(1)

for env_path in [
    os.path.join(app_dir, ".env"),
    os.path.join(script_dir, ".env"),
    os.path.join(script_dir, "..", ".env"),
]:
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
        break

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}
REPORT_FILE = "nlp_batch_report.json"


def load_clean_posts() -> list:
    all_posts = []
    offset = 0
    limit  = 200
    print("  Loading clean posts from Supabase...")
    while True:
        url    = f"{SUPABASE_URL}/rest/v1/posts"
        params = {
            "select":   "id,title,body,full_text,comments_text,locations",
            "is_clean": "eq.true",
            "offset":   offset,
            "limit":    limit,
            "order":    "created_date.asc",
        }
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"  [ERROR] {resp.status_code}: {resp.text[:200]}")
            break
        batch = resp.json()
        if not batch:
            break
        all_posts.extend(batch)
        offset += limit
        if len(batch) < limit:
            break
    print(f"  Found {len(all_posts)} clean posts to process")
    return all_posts


def update_post_nlp(post_id: str, updates: dict) -> bool:
    url    = f"{SUPABASE_URL}/rest/v1/posts"
    params = {"id": f"eq.{post_id}"}
    resp   = requests.patch(url, headers=HEADERS, params=params, json=updates, timeout=15)
    return resp.status_code in (200, 204)


def build_nlp_text(post: dict) -> str:
    full_text = (post.get("full_text") or "").strip()
    if full_text:
        return full_text
    title = (post.get("title") or "").strip()
    body  = (post.get("body")  or "").strip()
    return f"{title} {body}".strip()


def process_all(dry_run: bool = False):
    print("=" * 60)
    print("  SentiMap NLP Batch Processor v2.0 — God Mode")
    print("=" * 60)
    if dry_run:
        print("  [DRY RUN] Results will NOT be written to Supabase\n")

    analyzer  = CebuanoSentimentAnalyzer()
    extractor = CebuLocationExtractor()
    posts     = load_clean_posts()

    if not posts:
        print("\n  No clean posts found. Run data_validator.py first.")
        return

    results          = []
    success = errors = sarcasm_count = intensifier_hits = negation_hits = 0
    sarcasm_examples = []
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    score_sum        = 0.0

    print(f"\n  Processing {len(posts)} posts...\n")
    print(f"  {'#':>4}  {'S'}  {'Score':>7}  {'Sarc':>4}  {'Conf':>4}  Title")
    print(f"  {'-'*4}  {'-'}  {'-'*7}  {'-'*4}  {'-'*4}  {'-'*50}")

    for i, post in enumerate(posts):
        pid      = post.get("id", "")
        title    = post.get("title", "") or ""
        nlp_text = build_nlp_text(post)

        if not nlp_text:
            errors += 1
            continue

        try:
            sentiment = analyzer.analyze(nlp_text)
        except Exception as e:
            print(f"  [{i+1:>3}]  E  ERROR: {e}")
            errors += 1
            continue

        try:
            locations     = extractor.extract(nlp_text)
            locations_str = ", ".join(locations) if locations else "Unknown"
        except Exception:
            locations_str = post.get("locations", "Unknown") or "Unknown"

        label      = sentiment["sentiment_label"]
        score      = sentiment["sentiment_score"]
        sarcasm    = sentiment["sarcasm_detected"]
        confidence = sentiment["confidence"]
        triggers   = sentiment.get("sarcasm_triggers", [])
        intensifiers = sentiment.get("intensifiers_applied", [])
        negations    = sentiment.get("negations_applied", [])

        emotions = analyzer.detect_emotions(nlp_text, float(score), sarcasm)

        sentiment_counts[label] = sentiment_counts.get(label, 0) + 1
        score_sum += score
        if sarcasm:
            sarcasm_count += 1
            if len(sarcasm_examples) < 20:
                sarcasm_examples.append({"id": pid, "title": title,
                                          "score": score, "triggers": triggers})
        if intensifiers: intensifier_hits += 1
        if negations:    negation_hits    += 1

        lc = "+" if label == "positive" else ("-" if label == "negative" else ".")
        sf = "YES" if sarcasm else "   "
        print(f"  [{i+1:>3}]  {lc}  {score:>+7.3f}  {sf}  {confidence:.2f}  {title[:50]}")

        results.append({
            "id": pid, "title": title,
            "sentiment_score": round(float(score), 4),
            "sentiment_label": label,
            "sarcasm_detected": sarcasm,
            "sentiment_confidence": round(float(confidence), 4),
            "locations": locations_str,
        })

        if not dry_run:
            ok = update_post_nlp(pid, {
                "sentiment_score":      round(float(score), 4),
                "sentiment_label":      label,
                "sarcasm_detected":     sarcasm,
                "sentiment_confidence": round(float(confidence), 4),
                "locations":            locations_str,
                "platform":             "reddit",
                "emotion_anger":         emotions["anger"],
                "emotion_frustration":   emotions["frustration"],
                "emotion_fear":          emotions["fear"],
                "emotion_disgust":       emotions["disgust"],
                "emotion_sadness":       emotions["sadness"],
                "emotion_resignation":   emotions["resignation"],
                "emotion_trust":         emotions["trust"],
                "emotions_list":         emotions["emotions_list"],
            })
            if ok: success += 1
            else:  errors  += 1
        else:
            success += 1

        time.sleep(0.08)

    total       = len(posts)
    avg_score   = score_sum / max(total, 1)
    sarcasm_pct = round(100 * sarcasm_count / max(total, 1), 1)

    print(f"\n{'='*60}")
    print(f"  NLP BATCH PROCESSING COMPLETE")
    print(f"{'='*60}")
    print(f"  Posts processed    : {total}")
    print(f"  Written to Supabase: {success}")
    print(f"  Errors             : {errors}")
    print(f"\n  SENTIMENT DISTRIBUTION:")
    for lbl, count in sentiment_counts.items():
        pct = round(100 * count / max(total, 1))
        print(f"    {lbl:<10} {count:>4} ({pct:>3}%)  {'█' * (pct // 3)}")
    print(f"\n  Avg sentiment score  : {avg_score:+.4f}")
    print(f"  Sarcasm detected     : {sarcasm_count} posts ({sarcasm_pct}%)")
    print(f"  Intensifiers applied : {intensifier_hits} posts")
    print(f"  Negations flipped    : {negation_hits} posts")
    print(f"\n  Sample sarcastic posts:")
    for ex in sarcasm_examples[:5]:
        print(f"    [{ex['score']:+.3f}] {ex['title'][:55]}")
        print(f"           triggers: {ex['triggers'][:2]}")

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_posts": total, "sentiment_counts": sentiment_counts,
        "avg_sentiment_score": round(avg_score, 4),
        "sarcasm_count": sarcasm_count, "sarcasm_percentage": sarcasm_pct,
        "intensifier_hits": intensifier_hits, "negation_hits": negation_hits,
        "sarcasm_examples": sarcasm_examples, "all_results": results,
    }
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  Report saved: {REPORT_FILE}")
    print(f"\n  THESIS SNIPPET:")
    print(f"  NLP applied to {total} posts. Results: "
          f"{sentiment_counts.get('negative',0)} negative "
          f"({round(100*sentiment_counts.get('negative',0)/max(total,1))}%), "
          f"{sentiment_counts.get('neutral',0)} neutral, "
          f"{sentiment_counts.get('positive',0)} positive. "
          f"Sarcasm detected in {sarcasm_count} posts ({sarcasm_pct}%) "
          f"using 4-layer Cebuano sarcasm detection.")

    if dry_run:
        print(f"\n  [DRY RUN] No data written. Remove --dry-run to save.")
    else:
        print(f"\n  NEXT: Update main.py to read pre-computed columns.")
        print(f"  Dashboard will load in <1 second after that change.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",    action="store_true",
                        help="Run test cases before processing")
    parser.add_argument("--dry-run", action="store_true",
                        help="Process without writing to Supabase")
    args = parser.parse_args()

    if args.test:
        analyzer = CebuanoSentimentAnalyzer()
        passed, failed = analyzer.test_examples()
        if failed > 0:
            ans = input(f"\n  {failed} test(s) failed. Continue anyway? [Y/N]: ")
            if ans.strip().upper() != "Y":
                sys.exit(0)

    process_all(dry_run=args.dry_run)

