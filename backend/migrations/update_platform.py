#!/usr/bin/env python
"""Update platform field in Supabase to 'reddit' for all posts"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

headers = {
    "apikey": SUPABASE_KEY,
    "Content-Type": "application/json",
    "Authorization": f"Bearer {SUPABASE_KEY}"
}

print("[*] Updating platform field in Supabase...")

# Step 1: Update all NULL or 'unknown' platform values to 'reddit'
update_url = f"{SUPABASE_URL}/rest/v1/posts"
update_data = {"platform": "reddit"}

# Update where platform is NULL
response1 = requests.patch(
    update_url, 
    headers=headers,
    json=update_data,
    params={"platform": "is.null"}
)

print(f"[*] Updated NULL platform values: {response1.status_code}")

# Update where platform is 'unknown'
response2 = requests.patch(
    update_url, 
    headers=headers,
    json=update_data,
    params={"platform": "eq.unknown"}
)

print(f"[*] Updated 'unknown' platform values: {response2.status_code}")

# Step 2: Verify the update
verify_url = f"{SUPABASE_URL}/rest/v1/posts?select=id,platform&limit=10"
verify_response = requests.get(verify_url, headers=headers)

if verify_response.status_code == 200:
    data = verify_response.json()
    print(f"\n[OK] Verified: {len(data)} records fetched:")
    
    platform_counts = {}
    for record in data:
        platform = record.get('platform', 'N/A')
        platform_counts[platform] = platform_counts.get(platform, 0) + 1
    
    print(f"[OK] Platform distribution:")
    for platform, count in platform_counts.items():
        print(f"  {platform}: {count}")
    
    # Check if all are 'reddit' now
    all_reddit = all(r.get('platform') == 'reddit' for r in data)
    if all_reddit:
        print(f"\n[SUCCESS] All visible records have platform='reddit'")
    else:
        print(f"\n[WARNING] Some records still have non-'reddit' platform")
else:
    print(f"[ERROR] Failed to verify: {verify_response.status_code}")
    print(f"Response: {verify_response.text}")

print("\n[OK] Platform field update complete!")
