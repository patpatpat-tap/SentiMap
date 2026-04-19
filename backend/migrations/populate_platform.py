#!/usr/bin/env python3
"""
Step 2: Populate platform column after it's been created in Supabase dashboard.
This script updates all posts with platform='reddit' via REST API.
"""

import os
import requests
from dotenv import load_dotenv
import json

load_dotenv('app/.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[ERROR] Missing SUPABASE_URL or SUPABASE_KEY in .env")
    exit(1)

headers = {
    'apikey': SUPABASE_KEY,
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {SUPABASE_KEY}'
}

print("=" * 60)
print("POPULATING PLATFORM COLUMN")
print("=" * 60)

# Step 1: Check if platform column now exists
print("\nStep 1: Checking if platform column exists...")
verify_url = f'{SUPABASE_URL}/rest/v1/posts'
verify_response = requests.get(verify_url, headers=headers, params={'select': 'id,platform', 'limit': 1})

if verify_response.status_code == 200:
    data = verify_response.json()
    if data and 'platform' in data[0]:
        print("[OK] Platform column exists!")
        current_value = data[0].get('platform')
        print(f"     Sample post has platform={current_value}")
    else:
        print("[ERROR] Platform column still doesn't exist in the table")
        print("[INFO] Please add it via Supabase dashboard:")
        print("       1. Go to https://app.supabase.com")
        print("       2. Open your SentiMap project")
        print("       3. Navigate to SQL Editor")
        print("       4. Run this command:")
        print()
        print('       ALTER TABLE posts ADD COLUMN platform TEXT DEFAULT \'reddit\';')
        print()
        exit(1)
else:
    print(f"[ERROR] Failed to fetch posts: {verify_response.status_code}")
    print(f"        {verify_response.text}")
    exit(1)

# Step 2: Update all posts to platform = 'reddit'
print("\nStep 2: Updating posts with NULL platform to 'reddit'...")
update_url = f'{SUPABASE_URL}/rest/v1/posts'

# Use PATCH with WHERE clause - only update NULL values
update_data = {'platform': 'reddit'}
update_response = requests.patch(
    update_url,
    headers=headers,
    params={'platform': 'is.null'},  # WHERE platform IS NULL
    json=update_data
)

if update_response.status_code in [200, 204]:
    print(f"[OK] Successfully updated all posts!")
    print(f"     Status code: {update_response.status_code}")
    
    # Verify
    print("\nStep 3: Verifying updates...")
    verify_response = requests.get(
        verify_url, 
        headers=headers, 
        params={'select': 'id,platform', 'limit': 5}
    )
    
    if verify_response.status_code == 200:
        data = verify_response.json()
        reddit_count = sum(1 for post in data if post.get('platform') == 'reddit')
        print(f"[OK] Sample check: {reddit_count}/{len(data)} posts have platform='reddit'")
        
        # Show samples
        print("\n[INFO] Sample records:")
        for post in data[:3]:
            print(f"  - ID: {post['id']}, Platform: {post['platform']}")
else:
    print(f"[ERROR] Failed to update posts: {update_response.status_code}")
    print(f"        {update_response.text}")
    exit(1)

print("\n" + "=" * 60)
print("[OK] SUCCESS! Platform column is now populated with 'reddit'.")
print("\nNext steps:")
print("  1. Restart your backend: python -m uvicorn app.main:app --reload")
print("  2. Refresh localhost:3000 in your browser")
print("  3. The grievance feed should now show data!")
print("=" * 60)
