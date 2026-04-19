"""
Supabase Client Module for SentiMap Backend
============================================
Handles all Supabase database connections and queries.
"""

import os
from typing import List, Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# For simple REST API calls without the supabase-py library
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

class SupabaseClient:
    """Simple Supabase client for REST operations."""
    
    def __init__(self):
        self.url = SUPABASE_URL
        self.key = SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.key}"
        }
        
        if not self.url or not self.key:
            print("[WARNING] SUPABASE_URL and SUPABASE_KEY not set in .env - using environment variables")
        else:
            print(f"[OK] Supabase client initialized for {self.url}")
    
    def get_all_posts(self) -> List[Dict[str, Any]]:
        """Fetch all posts from Supabase."""
        try:
            url = f"{self.url}/rest/v1/posts"
            params = {"select": "*"}
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                print(f"[OK] Fetched {len(data)} posts from Supabase")
                return data
            else:
                print(f"[ERROR] Error fetching posts: {response.status_code}")
                print(f"  Response: {response.text}")
                return []
        except Exception as e:
            print(f"[ERROR] Exception fetching posts: {e}")
            return []
    
    def get_posts_by_relevance(self, is_relevant: bool = True) -> List[Dict[str, Any]]:
        """Fetch posts filtered by relevance."""
        try:
            url = f"{self.url}/rest/v1/posts"
            params = {
                "select": "*",
                "is_relevant": f"eq.{str(is_relevant).lower()}"
            }
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                print(f"[ERROR] Error filtering posts: {response.status_code}")
                return []
        except Exception as e:
            print(f"[ERROR] Exception filtering posts: {e}")
            return []
    
    def get_posts_by_location(self, location: str) -> List[Dict[str, Any]]:
        """Fetch posts by location (if extracted in NER)."""
        try:
            url = f"{self.url}/rest/v1/posts"
            params = {
                "select": "*",
                "locations": f"ilike.%{location}%"
            }
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                return []
        except Exception as e:
            print(f"[ERROR] Exception filtering by location: {e}")
            return []
    
    def update_locations(self, post_id: str, locations: str) -> bool:
        """Update locations for a post (after NER processing)."""
        try:
            url = f"{self.url}/rest/v1/posts"
            params = {"id": f"eq.{post_id}"}
            data = {"locations": locations}
            
            response = requests.patch(url, headers=self.headers, params=params, json=data)
            
            if response.status_code == 200:
                return True
            else:
                print(f"[ERROR] Error updating locations: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERROR] Exception updating locations: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Calculate statistics from posts."""
        posts = self.get_all_posts()
        
        if not posts:
            return {"error": "No posts found"}
        
        stats = {
            "total_posts": len(posts),
            "avg_upvotes": sum(p.get("upvotes", 0) for p in posts) / len(posts),
            "total_comments": sum(p.get("num_comments", 0) for p in posts),
            "relevant_posts": sum(1 for p in posts if p.get("is_relevant", True)),
            "posts_with_locations": sum(1 for p in posts if p.get("locations")),
        }
        
        return stats

# Initialize client
try:
    supabase_client = SupabaseClient()
except ValueError as e:
    print(f"[WARNING] Warning: {e}")
    supabase_client = None
