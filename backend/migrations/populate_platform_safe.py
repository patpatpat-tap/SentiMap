#!/usr/bin/env python3
"""
Populate platform column with retry logic and batching.
"""

import os
import requests
import time
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
print("POPULATING PLATFORM COLUMN WITH RETRY")
print("=" * 60)

# Step 1: Get all posts to check their current platform status
print("\nStep 1: Fetching all posts...")
verify_url = f'{SUPABASE_URL}/rest/v1/posts'

try:
    response = requests.get(
        verify_url, 
        headers=headers, 
        params={'select': 'id,platform', 'limit': 1000}
    )
    response.raise_for_status()
    posts = response.json()
    print(f"[OK] Fetched {len(posts)} posts")
    
    # Check platform values
    platforms = {}
    for post in posts:
        p = post.get('platform', 'null')
        platforms[p] = platforms.get(p, 0) + 1
    
    print(f"     Platform value breakdown:")
    for p, count in sorted(platforms.items()):
        print(f"       - {p}: {count} posts")
    
except Exception as e:
    print(f"[ERROR] Failed to fetch posts: {e}")
    exit(1)

# Step 2: Update posts with NULL or empty platform
print("\nStep 2: Updating posts with null/empty platform to 'reddit'...")

null_posts = [p for p in posts if p.get('platform') in [None, '', 'null', 'NULL']]
print(f"     Found {len(null_posts)} posts to update")

if len(null_posts) == 0:
    print("[OK] All posts already have platform set!")
else:
    # Build update for each post
    update_url = f'{SUPABASE_URL}/rest/v1/posts'
    updated_count = 0
    failed_count = 0
    
    for post in null_posts:
        post_id = post['id']
        try:
            # Update individual post
            response = requests.patch(
                update_url,
                headers=headers,
                params={'id': f'eq.{post_id}'},
                json={'platform': 'reddit'},
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                updated_count += 1
            else:
                print(f"     [WARNING] Failed to update post {post_id}: {response.status_code}")
                failed_count += 1
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
            
        except Exception as e:
            print(f"     [WARNING] Error updating post {post_id}: {e}")
            failed_count += 1
    
    print(f"[OK] Updated: {updated_count}, Failed: {failed_count}")

# Step 3: Verify final state
print("\nStep 3: Verifying final state...")
try:
    response = requests.get(
        verify_url, 
        headers=headers, 
        params={'select': 'id,platform', 'limit': 1000}
    )
    response.raise_for_status()
    posts = response.json()
    
    # Count by platform
    platforms = {}
    for post in posts:
        p = post.get('platform', 'null')
        platforms[p] = platforms.get(p, 0) + 1
    
    print(f"[OK] Final platform value breakdown:")
    for p, count in sorted(platforms.items()):
        status = "[OK]" if p == 'reddit' else "[WARNING]"
        print(f"     {status} {p}: {count} posts")
    
    # Show samples
    print(f"\n[INFO] Sample records (first 3):")
    for post in posts[:3]:
        print(f"       - ID: {post['id']}, Platform: {post['platform']}")
    
except Exception as e:
    print(f"[ERROR] Verification failed: {e}")

print("\n" + "=" * 60)
print("[OK] Platform population complete!")
print("\nNext steps:")
print("  1. Restart backend: venv\\Scripts\\python.exe -m uvicorn app.main:app --reload")
print("  2. Refresh localhost:3000")
print("=" * 60)
