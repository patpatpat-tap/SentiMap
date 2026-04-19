"""
Merge Script: Combine reddit_data_v2.json (existing) + reddit_godmode.json (new)
===============================================================================
Takes the existing 58 posts from v2 and merges with godmode's new posts.
Deduplicates by post ID.
Preserves quality_score from godmode for filtering.

Output: reddit_data_v3_clean.csv (ready for Supabase import)

Run:
    python merge_godmode_data.py
"""

import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# ─────────────────────────────────────────────
# FILE PATHS
# ─────────────────────────────────────────────
DATA_DIR = Path("../data")
SCRIPTS_DIR = Path(".")

EXISTING_JSON = DATA_DIR / "reddit_data_v2.json"
GODMODE_JSON = Path("../../reddit_godmode.json")  # Godmode outputs at project root
OUTPUT_CSV = DATA_DIR / "reddit_data_v3_clean.csv"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
def load_json(filepath):
    """Load JSON safely with error handling."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else [data]
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error in {filepath}: {e}")
        return []


def normalize_post(post, source="v2"):
    """
    Normalize post structure to common format.
    Godmode and v2 may have different field names.
    """
    return {
        "id": post.get("id") or post.get("post_id"),
        "title": post.get("title", ""),
        "body": post.get("body", post.get("selftext", "")),
        "full_text": post.get("full_text", ""),
        "created_date": post.get("created_date", post.get("created_at", "")),
        "upvotes": post.get("upvotes", post.get("score", 0)),
        "num_comments": post.get("num_comments") or post.get("comments", 0),
        "url": post.get("url", ""),
        "locations": post.get("locations", []),
        "comments_text": post.get("comments_text", ""),
        "is_relevant": post.get("is_relevant", True),
        "relevance_score": post.get("relevance_score", 0),  # Godmode field
        "source": source,  # Track which scraper provided this post
    }


def merge_datasets():
    """Main merge logic."""
    print("=" * 70)
    print("MERGE SCRIPT: reddit_data_v2.json + reddit_godmode.json")
    print("=" * 70)

    # Load existing data
    print(f"\n📂 Loading existing posts from {EXISTING_JSON}...")
    existing_posts = load_json(EXISTING_JSON)
    print(f"  ✓ Loaded {len(existing_posts)} existing posts")

    # Load godmode data
    print(f"\n📂 Loading new posts from {GODMODE_JSON}...")
    godmode_posts = load_json(GODMODE_JSON)
    print(f"  ✓ Loaded {len(godmode_posts)} new posts from godmode")

    # Normalize all posts
    print(f"\n🔄 Normalizing post structures...")
    existing_normalized = [normalize_post(p, source="v2") for p in existing_posts]
    godmode_normalized = [normalize_post(p, source="godmode") for p in godmode_posts]

    # Deduplicate by post ID
    print(f"\n🧹 Deduplicating by post ID...")
    seen_ids = set()
    merged = []

    for post in existing_normalized:
        post_id = post.get("id")
        if post_id and post_id not in seen_ids:
            merged.append(post)
            seen_ids.add(post_id)

    for post in godmode_normalized:
        post_id = post.get("id")
        if post_id and post_id not in seen_ids:
            merged.append(post)
            seen_ids.add(post_id)

    duplicates_found = len(existing_posts) + len(godmode_posts) - len(merged)
    print(f"  ✓ Merged {len(merged)} unique posts")
    if duplicates_found > 0:
        print(f"  ℹ️ Found and removed {duplicates_found} duplicates")

    # Convert to DataFrame
    print(f"\n📊 Converting to DataFrame...")
    df = pd.DataFrame(merged)

    # Data quality checks
    print(f"\n✅ Quality Checks:")
    print(f"   - Total posts: {len(df)}")
    print(f"   - Posts from v2 (existing): {(df['source'] == 'v2').sum()}")
    print(f"   - Posts from godmode (new): {(df['source'] == 'godmode').sum()}")
    print(f"   - Posts with relevance_score: {(df['relevance_score'] > 0).sum()}")
    print(f"   - Avg relevance_score (godmode): {df[df['source'] == 'godmode']['relevance_score'].mean():.2f}")

    # Filter: Keep only relevant posts (godmode scoring >= 2, or all v2 posts)
    print(f"\n🎯 Filtering by relevance (godmode posts must have score >= 2)...")
    before_filter = len(df)
    df_filtered = df[
        (df['source'] == 'v2') |  # Keep all v2 posts as-is
        (df['relevance_score'] >= 2)  # Keep godmode posts with score >= 2
    ].copy()
    after_filter = len(df_filtered)
    removed = before_filter - after_filter
    print(f"  ✓ Kept {after_filter} posts (removed {removed} low-relevance godmode posts)")

    # Reorder columns for clarity
    column_order = [
        "id", "title", "body", "full_text", "created_date",
        "upvotes", "num_comments", "url", "locations", "comments_text",
        "is_relevant", "relevance_score", "source"
    ]
    df_filtered = df_filtered[[col for col in column_order if col in df_filtered.columns]]

    # Export to CSV
    print(f"\n💾 Exporting to {OUTPUT_CSV}...")
    df_filtered.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"  ✓ Saved {len(df_filtered)} posts to CSV")

    # Summary report
    print(f"\n" + "=" * 70)
    print(f"MERGE COMPLETE")
    print(f"=" * 70)
    print(f"✅ Output file: {OUTPUT_CSV}")
    print(f"   Columns: {', '.join(df_filtered.columns)}")
    print(f"   Ready for Supabase import!")
    print(f"\nNext step:")
    print(f"   python import_to_supabase.py")
    print(f"=" * 70)

    return df_filtered


if __name__ == "__main__":
    try:
        df_result = merge_datasets()
    except Exception as e:
        print(f"\n❌ Error during merge: {e}")
        import traceback
        traceback.print_exc()
