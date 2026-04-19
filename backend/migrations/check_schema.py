#!/usr/bin/env python
"""Add platform column to posts table in Supabase and populate it"""

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

print("[*] Checking posts table structure...")

# First, fetch one record to see what columns exist
check_url = f"{SUPABASE_URL}/rest/v1/posts?select=*&limit=1"
check_response = requests.get(check_url, headers=headers)

if check_response.status_code == 200:
    data = check_response.json()
    if data:
        columns = list(data[0].keys())
        print(f"[OK] Current columns in posts table:")
        for col in sorted(columns):
            print(f"  - {col}")
        
        if 'platform' in columns:
            print(f"\n[OK] Platform column already exists!")
        else:
            print(f"\n[WARNING] Platform column does not exist. It needs to be added in Supabase UI.")
            print(f"\nTo add it manually:")
            print(f"1. Go to https://supabase.com/dashboard/project/xbdhvpjhhvopatmyeubb")
            print(f"2. Navigate to Database → Tables → posts")
            print(f"3. Click 'Add column'")
            print(f"4. Name: platform")
            print(f"5. Type: text")
            print(f"6. Default value: 'reddit'")
            print(f"7. Save")
else:
    print(f"[ERROR] Failed to check table: {check_response.status_code}")
    print(f"Response: {check_response.text}")

print("\n[OK] Check complete!")
