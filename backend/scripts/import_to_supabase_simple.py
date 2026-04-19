"""
Simple Supabase Import using REST API (no library dependency)
===============================================================
Imports reddit_data_v3_clean.csv into Supabase 'posts' table.

Run:
    python import_to_supabase_simple.py
"""

import csv
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

# Supabase credentials
SUPABASE_URL = "https://xbdhvpjhhvopatmyeubb.supabase.co"
SUPABASE_KEY = "sb_secret_TElydENOMJQOos9yfPSDIg_xd5ioeE6"  # Service role key (bypasses RLS)

# Find CSV file relative to this script
SCRIPT_DIR = Path(__file__).parent.parent
CSV_FILE = SCRIPT_DIR / "data" / "reddit_data_v3_clean.csv"
TABLE_NAME = "posts"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json",
    "Prefer": "return=minimal"  # Don't return row data
}

def load_csv_data():
    """Load data from CSV file."""
    try:
        df = pd.read_csv(CSV_FILE)
        # Drop columns that don't exist in Supabase schema
        columns_to_drop = ['relevance_score', 'source']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        print(f"✓ Loaded {len(df)} records from {CSV_FILE}")
        print(f"  Columns: {', '.join(df.columns)}")
        return df.to_dict('records')
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return []

def insert_posts(posts):
    """Insert posts into Supabase via REST API."""
    if not posts:
        print("No posts to insert")
        return
    
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?on_conflict=id"
    
    # Batch insert (Supabase allows bulk inserts)
    print(f"\n📤 Inserting {len(posts)} posts to Supabase...")
    
    try:
        # Convert NaN/None to null for JSON
        for post in posts:
            for key, value in post.items():
                if pd.isna(value):
                    post[key] = None
                elif isinstance(value, list):
                    post[key] = json.dumps(value)  # Convert lists to JSON strings
        
        # Supabase REST API batch insert with upsert
        headers = {
            "apikey": SUPABASE_KEY,
            "Content-Type": "application/json",
            "Prefer": "return=minimal,resolution=merge-duplicates"
        }
        
        response = requests.post(
            url,
            json=posts[:100],  # Start with first 100
            headers=headers,
            timeout=30
        )
        
        if response.status_code in [200, 201, 206]:
            print(f"  ✓ Batch 1: Inserted {min(100, len(posts))} posts")
        else:
            print(f"  ✗ Error: {response.status_code} - {response.text}")
            return False
        
        # Insert remaining in batches of 100
        for i in range(100, len(posts), 100):
            batch = posts[i:i+100]
            response = requests.post(
                url,
                json=batch,
                headers=headers,
                timeout=30
            )
            
            if response.status_code in [200, 201, 206]:
                print(f"  ✓ Batch {i//100 + 1}: Inserted {len(batch)} posts")
            else:
                print(f"  ✗ Batch error: {response.status_code}")
                return False
        
        print(f"\n✅ ALL {len(posts)} POSTS INSERTED TO SUPABASE!")
        return True
        
    except Exception as e:
        print(f"✗ Error inserting posts: {e}")
        return False

def main():
    print("=" * 70)
    print("SUPABASE DATA IMPORT (v3 - Godmode + v2)")
    print("=" * 70)
    
    # Load CSV
    posts = load_csv_data()
    if not posts:
        print("✗ No data to import")
        return
    
    # Insert to Supabase
    success = insert_posts(posts)
    
    print("\n" + "=" * 70)
    if success:
        print("✅ IMPORT COMPLETE")
        print("   The backend API now serves 736 posts with NLP enrichment")
    else:
        print("❌ IMPORT FAILED")
    print("=" * 70)

if __name__ == "__main__":
    main()
