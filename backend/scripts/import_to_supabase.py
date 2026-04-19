"""
Supabase Data Import Script
============================
Imports reddit_data_v2_clean.csv into Supabase 'posts' table.

Usage:
    python import_to_supabase.py
"""

import os
import csv
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# Supabase credentials
SUPABASE_URL = "https://xbdhvpjhhvopatmyeubb.supabase.co"
SUPABASE_KEY = "sb_publishable_7exwi-Ym62ER0i6hqtaDbw_juD2aU02"
CSV_FILE = "reddit_data_v3_clean.csv"
TABLE_NAME = "posts"

def create_supabase_client() -> Client:
    """Initialize Supabase client."""
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print(f"✓ Connected to Supabase")
        return client
    except Exception as e:
        print(f"✗ Failed to connect to Supabase: {e}")
        return None

def create_posts_table(client: Client):
    """Create posts table if it doesn't exist."""
    try:
        # Check if table exists by querying it
        client.table(TABLE_NAME).select('id').limit(1).execute()
        print(f"✓ Table '{TABLE_NAME}' already exists")
        return True
    except Exception as e:
        print(f"⚠ Table may not exist, attempting to create...")
        # If table doesn't exist, we'll handle it in the insert phase
        return False

def load_csv_data() -> list:
    """Load data from CSV file."""
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✓ Loaded {len(df)} records from {CSV_FILE}")
        return df.to_dict('records')
    except Exception as e:
        print(f"✗ Error loading CSV: {e}")
        return []

def import_records(client: Client, records: list) -> dict:
    """Import records into Supabase."""
    stats = {
        "total": len(records),
        "success": 0,
        "failed": 0,
        "errors": []
    }
    
    print(f"\n→ Importing {len(records)} records into '{TABLE_NAME}' table...\n")
    
    for idx, record in enumerate(records, 1):
        try:
            # Clean the record for insertion
            clean_record = {
                "id": str(record.get("id", "")).strip(),
                "title": str(record.get("title", "")).strip(),
                "body": str(record.get("body", "")).strip(),
                "full_text": str(record.get("full_text", "")).strip(),
                "created_date": str(record.get("created_date", "")).strip(),
                "upvotes": int(record.get("upvotes", 0)),
                "num_comments": int(record.get("num_comments", 0)),
                "url": str(record.get("url", "")).strip(),
                "locations": str(record.get("locations", "")).strip(),
                "comments_text": str(record.get("comments_text", "")).strip(),
                "is_relevant": bool(record.get("is_relevant", True))
            }
            
            # Insert record
            response = client.table(TABLE_NAME).insert(clean_record).execute()
            stats["success"] += 1
            
            # Progress indicator
            if idx % 10 == 0:
                print(f"  ✓ Imported {idx}/{len(records)} records")
        
        except Exception as e:
            stats["failed"] += 1
            error_msg = f"Record {idx} (ID: {record.get('id')}): {str(e)}"
            stats["errors"].append(error_msg)
            print(f"  ✗ Failed: {error_msg}")
    
    return stats

def print_report(stats: dict):
    """Print import report."""
    print(f"\n" + "=" * 60)
    print("IMPORT REPORT")
    print("=" * 60)
    print(f"\nTable: {TABLE_NAME}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n  Total Records:   {stats['total']}")
    print(f"  Successful:      {stats['success']} ✓")
    print(f"  Failed:          {stats['failed']} ✗")
    print(f"  Success Rate:    {100 * stats['success'] // stats['total']}%")
    
    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for error in stats['errors'][:5]:  # Show first 5 errors
            print(f"  • {error}")
        if len(stats['errors']) > 5:
            print(f"  ... and {len(stats['errors']) - 5} more")
    
    print("\n" + "=" * 60)
    if stats['failed'] == 0:
        print("✓ IMPORT COMPLETE - ALL RECORDS IMPORTED SUCCESSFULLY!")
    else:
        print(f"⚠ IMPORT COMPLETE - {stats['failed']} records failed")
    print("=" * 60 + "\n")

def main():
    print("\n" + "=" * 60)
    print("SENTIMAP → SUPABASE DATA IMPORT")
    print("=" * 60 + "\n")
    
    # Step 1: Connect to Supabase
    print("→ Connecting to Supabase...")
    client = create_supabase_client()
    if not client:
        print("✗ Cannot proceed without Supabase connection")
        return
    
    # Step 2: Check table exists
    print("→ Checking posts table...")
    create_posts_table(client)
    
    # Step 3: Load CSV
    print("→ Loading CSV data...")
    records = load_csv_data()
    if not records:
        print("✗ No records to import")
        return
    
    # Step 4: Import records
    print("→ Importing records...")
    stats = import_records(client, records)
    
    # Step 5: Print report
    print_report(stats)

if __name__ == "__main__":
    main()
