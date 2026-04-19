#!/usr/bin/env python3
"""Test script to verify SentiMap system is operational"""

import urllib.request
import json

print("=" * 60)
print("SENTIMAP - HYBRID NLP SYSTEM VERIFICATION")
print("=" * 60)

try:
    # Test 1: Get stats
    print("\n[1/3] Testing /api/stats endpoint...")
    r = urllib.request.urlopen('http://127.0.0.1:8000/api/stats')
    stats = json.loads(r.read())
    
    print(f"  ✅ Total Grievances: {stats['total_grievances']}")
    print(f"  ✅ Sentiment Breakdown: Negative={stats['sentiment_breakdown']['negative']}, "
          f"Neutral={stats['sentiment_breakdown']['neutral']}, "
          f"Positive={stats['sentiment_breakdown']['positive']}")
    print(f"  ✅ Avg Sentiment Score: {stats['avg_sentiment_score']}")
    print(f"  ✅ Sarcasm Detection Rate: {stats['sarcasm_percentage']}%")
    print(f"  ✅ Locations Extracted: {len(stats['locations'])} unique locations")
    print(f"     Top: {stats['locations'][0]['location']} ({stats['locations'][0]['count']} mentions)")
    
    # Test 2: Get enriched data sample
    print("\n[2/3] Testing /api/data endpoint (NLP enrichment)...")
    r2 = urllib.request.urlopen('http://127.0.0.1:8000/api/data')
    data = json.loads(r2.read())
    sample = data['data'][0]
    
    print(f"  ✅ Total Records: {len(data['data'])}")
    print(f"  ✅ Sample Record:")
    print(f"     Title: '{sample['title'][:50]}...'")
    print(f"     Sentiment: {sample['sentiment_label']} ({sample['sentiment_score']*100:.1f}%)")
    print(f"     Locations: {sample['locations'] if sample['locations'] else 'None detected'}")
    print(f"     Sarcasm: {sample['sarcasm_detected']}")
    
    # Test 3: Location reference
    print("\n[3/3] Testing /api/locations endpoint...")
    r3 = urllib.request.urlopen('http://127.0.0.1:8000/api/locations')
    locs = json.loads(r3.read())
    
    print(f"  ✅ Known Locations: {locs['total']}")
    print(f"     Sample: {', '.join(locs['locations'][:5])}")
    
    print("\n" + "=" * 60)
    print("✅ ALL SYSTEMS OPERATIONAL")
    print("=" * 60)
    print("\nFrontend URL: http://localhost:3000")
    print("API URL: http://127.0.0.1:8000")
    print("Backend Status: Running on port 8000")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nEnsure backend is running:")
    print("  d:\\PROJECTS\\SentiMap\\backend\\venv\\Scripts\\python.exe")
    print("  d:\\PROJECTS\\SentiMap\\backend\\venv\\main.py")
