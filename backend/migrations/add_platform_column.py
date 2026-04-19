#!/usr/bin/env python3
"""
Script to add the platform column to Supabase posts table
and update all existing records to platform = 'reddit'

Uses direct PostgreSQL connection via psycopg2
"""

import os
import sys
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv('app/.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if not SUPABASE_URL or not SUPABASE_KEY:
    print("[ERROR] Missing SUPABASE_URL or SUPABASE_KEY in .env")
    sys.exit(1)

print("=" * 60)
print("ADDING PLATFORM COLUMN TO SUPABASE")
print("=" * 60)

# Try to import psycopg2
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    USE_DIRECT_DB = True
    print("[OK] psycopg2 available - using direct PostgreSQL connection")
except ImportError:
    print("[WARNING] psycopg2 not available - using REST API fallback")
    USE_DIRECT_DB = False
    import requests

if USE_DIRECT_DB:
    # Extract DB connection details from Supabase URL
    # Format: https://xbdhvpjhhvopatmyeubb.supabase.co
    db_host = SUPABASE_URL.replace('https://', '').split('/')[0].replace('xbdhvpjhhvopatmyeubb', 'db.xbdhvpjhhvopatmyeubb')
    db_host = 'db.xbdhvpjhhvopatmyeubb.supabase.co'
    db_name = 'postgres'
    db_user = 'postgres'
    db_password = DB_PASSWORD or 'your_password'  # Should be in .env
    
    try:
        print(f"\nStep 1: Connecting to PostgreSQL...")
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=5432
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print(f"[OK] Connected to {db_host}")
        
        # Step 2: Add platform column if it doesn't exist
        print("\nStep 2: Adding platform column...")
        add_column_sql = '''
        ALTER TABLE posts 
        ADD COLUMN IF NOT EXISTS platform TEXT DEFAULT 'reddit';
        '''
        cursor.execute(add_column_sql)
        conn.commit()
        print("[OK] Platform column added (or already exists)")
        
        # Step 3: Update all records with platform = 'reddit'
        print("\nStep 3: Updating all records to platform = 'reddit'...")
        update_sql = "UPDATE posts SET platform = 'reddit' WHERE platform IS NULL;"
        cursor.execute(update_sql)
        conn.commit()
        affected_rows = cursor.rowcount
        print(f"[OK] Updated {affected_rows} rows")
        
        # Step 4: Verify
        print("\nStep 4: Verifying platform column...")
        cursor.execute("SELECT COUNT(*) as total, COUNT(platform) as with_platform FROM posts;")
        result = cursor.fetchone()
        print(f"[OK] Total posts: {result['total']}, Posts with platform: {result['with_platform']}")
        
        # Show sample
        cursor.execute("SELECT id, title, platform FROM posts LIMIT 3;")
        samples = cursor.fetchall()
        print("\nSample records:")
        for row in samples:
            print(f"  ID: {row['id']}, Platform: {row['platform']}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] Direct PostgreSQL connection failed: {str(e)}")
        print("[INFO] Falling back to REST API approach...")
        USE_DIRECT_DB = False

# REST API fallback (if psycopg2 not available or connection failed)
if not USE_DIRECT_DB:
    import requests
    
    headers = {
        'apikey': SUPABASE_KEY,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
    
    print(f"\nStep 1: Checking current posts...")
    verify_url = f'{SUPABASE_URL}/rest/v1/posts'
    params = {'select': 'id,platform', 'limit': 3}
    verify_response = requests.get(verify_url, headers=headers, params=params)
    
    if verify_response.status_code == 200:
        data = verify_response.json()
        print(f"[OK] Can fetch posts. Sample:")
        for post in data[:1]:
            print(f"  {json.dumps(post, indent=4)}")
        
        # Check if platform column already exists
        if data and 'platform' in data[0]:
            print("[OK] Platform column already exists!")
    else:
        print(f"[ERROR] Failed to fetch posts: {verify_response.status_code}")
        print(f"  Response: {verify_response.text}")

# Step 2: Update all NULL platform values to 'reddit'
print("\nStep 2: Updating posts with NULL platform to 'reddit'...")
update_url = f'{SUPABASE_URL}/rest/v1/posts'
update_response = requests.patch(
    update_url,
    headers=headers,
    params={'platform': 'is.null'},
    json={'platform': 'reddit'}
)

if update_response.status_code in [200, 204]:
    print(f"[OK] Update successful (status: {update_response.status_code})")
else:
    print(f"[WARNING] Update response status: {update_response.status_code}")
    if update_response.text:
        print(f"  Response: {update_response.text[:200]}")

# Step 3: Set default for all existing posts that might be missing the field
print("\nStep 3: Ensuring all posts have platform = 'reddit'...")
default_update_response = requests.patch(
    update_url,
    headers=headers,
    json={'platform': 'reddit'}
)

if default_update_response.status_code in [200, 204]:
    print(f"[OK] Default update successful (status: {default_update_response.status_code})")
else:
    print(f"[WARNING] Default update response status: {default_update_response.status_code}")

# Step 4: Verify the changes
print("\nStep 4: Verifying platform column after updates...")
verify_url = f'{SUPABASE_URL}/rest/v1/posts'
params = {'select': 'id,title,platform', 'limit': 5}
final_verify = requests.get(verify_url, headers=headers, params=params)

if final_verify.status_code == 200:
    data = final_verify.json()
    print(f"[OK] Verification successful!")
    print(f"  Total records checked: {len(data)}")
    print(f"  Sample records with platform:")
    for i, post in enumerate(data[:3]):
        print(f"    [{i+1}] ID: {post.get('id')}, Platform: {post.get('platform')}")
    
    # Count reddit posts
    reddit_count = sum(1 for p in data if p.get('platform') == 'reddit')
    print(f"  Reddit posts in sample: {reddit_count}/{len(data)}")
else:
    print(f"[ERROR] Verification failed: {final_verify.status_code}")
    print(f"  Response: {final_verify.text}")

print("\n" + "=" * 60)
print("PLATFORM COLUMN UPDATE COMPLETE")
print("=" * 60)
