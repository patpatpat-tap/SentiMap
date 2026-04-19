#!/usr/bin/env python3
"""Test backend /api/data endpoint."""

import requests
import json

try:
    response = requests.get("http://127.0.0.1:8000/api/data", timeout=5)
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {response.headers}")
    data = response.json()
    print(f"\nResponse:")
    print(json.dumps(data, indent=2)[:500])
    
    if "data" in data and data["data"]:
        print(f"\n✓ SUCCESS: Received {len(data['data'])} posts")
        print(f"First post keys: {data['data'][0].keys()}")
    else:
        print(f"\n⚠ WARNING: No data in response")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
