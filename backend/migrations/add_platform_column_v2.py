#!/usr/bin/env python3
"""
Script to add the platform column to Supabase posts table.
Uses direct PostgreSQL connection - requires postgres password from Supabase.
"""

import os
import sys
import getpass
from dotenv import load_dotenv

# Load environment variables
load_dotenv('app/.env')

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

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
    HAS_PSYCOPG2 = True
except ImportError:
    print("[ERROR] psycopg2 not installed")
    print("Install it with: pip install psycopg2-binary")
    sys.exit(1)

# Get PostgreSQL credentials
print("\n[INFO] Enter PostgreSQL credentials from your Supabase project:")
print("       (Go to Project Settings > Database > Connection Info)")
print()

db_password = getpass.getpass("PostgreSQL Password: ")

db_host = 'db.xbdhvpjhhvopatmyeubb.supabase.co'
db_name = 'postgres'
db_user = 'postgres'
db_port = 5432

try:
    print(f"\nStep 1: Connecting to PostgreSQL at {db_host}...")
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
        port=db_port,
        sslmode='require'
    )
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    print(f"[OK] Connected!")
    
    # Step 2: Add platform column if it doesn't exist
    print("\nStep 2: Adding platform column...")
    add_column_sql = """
    ALTER TABLE posts 
    ADD COLUMN IF NOT EXISTS platform TEXT DEFAULT 'reddit';
    """
    cursor.execute(add_column_sql)
    conn.commit()
    print("[OK] Platform column added (or already exists)")
    
    # Step 3: Update all NULL platform values to 'reddit'
    print("\nStep 3: Setting platform = 'reddit' for all posts...")
    cursor.execute("UPDATE posts SET platform = 'reddit' WHERE platform IS NULL;")
    conn.commit()
    affected_rows = cursor.rowcount
    print(f"[OK] Updated {affected_rows} rows with platform='reddit'")
    
    # Step 4: Ensure default for new records
    print("\nStep 4: Verifying schema...")
    cursor.execute("""
    SELECT column_name, data_type, column_default 
    FROM information_schema.columns 
    WHERE table_name = 'posts' AND column_name = 'platform';
    """)
    col_info = cursor.fetchone()
    if col_info:
        print(f"[OK] Platform column exists: {col_info}")
    
    # Step 5: Show summary
    print("\nStep 5: Summary...")
    cursor.execute("""
    SELECT 
        COUNT(*) as total_posts,
        COUNT(platform) as posts_with_platform,
        COUNT(CASE WHEN platform = 'reddit' THEN 1 END) as reddit_posts
    FROM posts;
    """)
    result = cursor.fetchone()
    print(f"[OK] Total posts: {result['total_posts']}")
    print(f"[OK] Posts with platform value: {result['posts_with_platform']}")
    print(f"[OK] Posts with platform='reddit': {result['reddit_posts']}")
    
    # Show samples
    print("\n[INFO] Sample records:")
    cursor.execute("SELECT id, title, platform FROM posts ORDER BY RANDOM() LIMIT 3;")
    samples = cursor.fetchall()
    for row in samples:
        print(f"  - {row['id']}: {row['title'][:50]}... → {row['platform']}")
    
    cursor.close()
    conn.close()
    
    print("\n" + "=" * 60)
    print("[OK] SUCCESS! Platform column has been added and populated.")
    print("     Now restart the backend and check localhost:3000")
    print("=" * 60)
    
except psycopg2.Error as e:
    print(f"\n[ERROR] PostgreSQL Error: {e}")
    print("\n[INFO] Troubleshooting steps:")
    print("  1. Verify you entered the correct password")
    print("  2. Check that PostgreSQL connection is enabled in Supabase project")
    print("  3. Go to Project Settings > Database and verify credentials")
    sys.exit(1)
    
except Exception as e:
    print(f"\n[ERROR] Unexpected error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
