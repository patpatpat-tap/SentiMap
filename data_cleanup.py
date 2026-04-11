"""
Data Inspection & Cleanup for SentiMap Reddit Scraper
======================================================
Validates reddit_data_v2.json and normalizes for Supabase migration.
"""

import json
import pandas as pd
from datetime import datetime, timezone
import os

# Paths
INPUT_JSON = "reddit_data_v2.json"
OUTPUT_CSV = "reddit_data_v2_clean.csv"
REPORT_FILE = "data_cleanup_report.txt"

def parse_json():
    """Load and parse the JSON file."""
    try:
        with open(INPUT_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(data)} records from {INPUT_JSON}")
        return data
    except Exception as e:
        print(f"✗ Error loading JSON: {e}")
        return []

def validate_records(records):
    """Check for missing/inconsistent fields."""
    report = []
    report.append("=" * 60)
    report.append("DATA VALIDATION REPORT")
    report.append("=" * 60)
    report.append(f"\nTotal records: {len(records)}\n")
    
    issues = {
        "missing_id": 0,
        "missing_title": 0,
        "missing_body": 0,
        "missing_full_text": 0,
        "missing_created_date": 0,
        "missing_upvotes": 0,
        "missing_url": 0,
        "blank_body": 0,
        "duplicate_ids": set(),
    }
    
    seen_ids = set()
    
    for i, rec in enumerate(records):
        # Check for missing fields
        if not rec.get("id"):
            issues["missing_id"] += 1
        else:
            if rec["id"] in seen_ids:
                issues["duplicate_ids"].add(rec["id"])
            seen_ids.add(rec["id"])
        
        if not rec.get("title"):
            issues["missing_title"] += 1
        if not rec.get("body"):
            issues["missing_body"] += 1
        if not rec.get("full_text"):
            issues["missing_full_text"] += 1
        if not rec.get("created_date"):
            issues["missing_created_date"] += 1
        if rec.get("upvotes") is None:
            issues["missing_upvotes"] += 1
        if not rec.get("url"):
            issues["missing_url"] += 1
        
        # Check for blank body text
        if rec.get("body", "").strip() == "":
            issues["blank_body"] += 1
    
    # Report issues
    report.append("MISSING FIELDS:")
    report.append(f"  • ID:          {issues['missing_id']}")
    report.append(f"  • Title:       {issues['missing_title']}")
    report.append(f"  • Body:        {issues['missing_body']}")
    report.append(f"  • Full text:   {issues['missing_full_text']}")
    report.append(f"  • Created date:{issues['missing_created_date']}")
    report.append(f"  • Upvotes:     {issues['missing_upvotes']}")
    report.append(f"  • URL:         {issues['missing_url']}")
    report.append(f"\nBLANK BODY TEXT: {issues['blank_body']}")
    report.append(f"DUPLICATE IDs: {len(issues['duplicate_ids'])}")
    if issues['duplicate_ids']:
        report.append(f"  → {issues['duplicate_ids']}")
    
    total_issues = sum([
        issues['missing_id'], issues['missing_title'], issues['missing_body'],
        issues['missing_full_text'], issues['missing_created_date'],
        issues['missing_upvotes'], issues['missing_url'], issues['blank_body'],
        len(issues['duplicate_ids'])
    ])
    report.append(f"\nTOTAL ISSUES: {total_issues}")
    
    return "\n".join(report), total_issues

def clean_records(records):
    """Clean and normalize records for Supabase."""
    cleaned = []
    
    for rec in records:
        # Skip if missing critical fields
        if not rec.get("id") or not rec.get("title"):
            continue
        
        # Combine title + body for full_text
        title = rec.get("title", "").strip()
        body = rec.get("body", "").strip()
        full_text = (title + " " + body).strip()
        
        # Normalize date to ISO format (YYYY-MM-DD)
        created_date = rec.get("created_date", "")
        if created_date and "-" in str(created_date):
            # Already in YYYY-MM-DD format
            date_normalized = str(created_date)
        else:
            # Try to parse from various formats
            try:
                dt = datetime.fromisoformat(str(created_date).replace(" UTC", ""))
                date_normalized = dt.strftime("%Y-%m-%d")
            except:
                date_normalized = ""  # Placeholder
        
        cleaned_record = {
            "id": rec.get("id", ""),
            "title": title,
            "body": body,
            "full_text": full_text,
            "created_date": date_normalized,
            "upvotes": int(rec.get("upvotes", 0)),
            "num_comments": int(rec.get("num_comments", 0)),
            "url": rec.get("url", ""),
            "locations": "",  # Placeholder - will be filled via spaCy NER
            "comments_text": "",  # Placeholder - will extract from top_comments later
            "is_relevant": True,  # All posts passed relevance filter
        }
        
        cleaned.append(cleaned_record)
    
    return cleaned

def extract_comments_text(records_original, cleaned_records):
    """Extract top 5 comments and concatenate."""
    for i, original in enumerate(records_original):
        if i < len(cleaned_records):
            comments = original.get("top_comments", [])
            if isinstance(comments, list):
                comments_text = " | ".join([
                    c.get("body", "")[:200]  # First 200 chars per comment
                    for c in comments if c.get("body")
                ])
                cleaned_records[i]["comments_text"] = comments_text[:1000]  # Max 1000 chars
    
    return cleaned_records

def save_csv(records):
    """Save cleaned records to CSV."""
    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"\n✓ Cleaned data saved to {OUTPUT_CSV}")
    print(f"  Columns: {', '.join(df.columns.tolist())}")
    print(f"  Rows: {len(df)}")
    
    # Data preview
    print(f"\n  Sample record (ID: {df.iloc[0]['id']}):")
    print(f"    Title: {df.iloc[0]['title'][:50]}...")
    print(f"    Date: {df.iloc[0]['created_date']}")
    print(f"    Upvotes: {df.iloc[0]['upvotes']}")
    print(f"    URL: {df.iloc[0]['url']}")

def main():
    print("\n" + "=" * 60)
    print("SENTIMAP DATA CLEANUP & VALIDATION")
    print("=" * 60 + "\n")
    
    # Step 1: Parse JSON
    print("→ Parsing JSON...")
    records = parse_json()
    if not records:
        print("✗ No records found. Exiting.")
        return
    
    # Step 2: Validate
    print("→ Validating records...")
    report, issues = validate_records(records)
    print(report)
    
    # Step 3: Clean
    print("\n→ Cleaning records...")
    cleaned = clean_records(records)
    print(f"✓ Cleaned {len(cleaned)} records (removed {len(records) - len(cleaned)} invalid)")
    
    # Step 4: Extract comments
    print("→ Extracting comments...")
    cleaned = extract_comments_text(records, cleaned)
    
    # Step 5: Save
    print("→ Saving cleaned data...")
    save_csv(cleaned)
    
    # Step 6: Save report
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ Report saved to {REPORT_FILE}")
    
    print("\n" + "=" * 60)
    print("✓ CLEANUP COMPLETE - Ready for Supabase import!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
