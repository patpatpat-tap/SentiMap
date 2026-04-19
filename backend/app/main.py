"""
SentiMap FastAPI Backend - Supabase Edition
============================================
Connects to Supabase for data layer instead of local Excel files.
All endpoints now query from Supabase posts table.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .sentiment_analyzer import CebuanoSentimentAnalyzer
from .location_extractor import CebuLocationExtractor
from .geospatial import cluster_grievances_by_location, get_severity_color
from .supabase_client import supabase_client

# Load environment variables
load_dotenv()

app = FastAPI(title="SentiMap API - Supabase")

# Initialize NLP modules
sentiment_analyzer = CebuanoSentimentAnalyzer()
location_extractor = CebuLocationExtractor()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HEATMAP ENDPOINT
# ============================================================================
@app.get("/api/heatmap")
def get_heatmap():
    """
    Get clustered grievance data for heatmap visualization.
    Queries from Supabase posts table.
    
    Returns heat zones by location with count, average sentiment, and severity.
    """
    try:
        if not supabase_client:
            return {"status": "error", "message": "Supabase client not initialized"}
        
        # Fetch all posts from Supabase
        posts = supabase_client.get_all_posts()
        
        if not posts:
            return {
                "status": "success",
                "heatmap": [],
                "total_clusters": 0,
                "center": [10.3157, 123.8854],
                "zoom": 12
            }
        
        # Enrich with NLP if not already done
        data_records = []
        for post in posts:
            record = {
                "title": post.get("title", ""),
                "upvotes": post.get("upvotes", 0),
                "comments": post.get("num_comments", 0),
                "locations": post.get("locations", "").split(",") if post.get("locations") else []
            }
            
            # If locations not yet extracted, extract them now
            if not record["locations"]:
                text = post.get("full_text", post.get("title", ""))
                record["locations"] = location_extractor.extract(text)
            
            # Analyze sentiment
            sentiment = sentiment_analyzer.analyze(post.get("full_text", post.get("title", "")))
            record["sentiment_score"] = sentiment["sentiment_score"]
            record["sentiment_label"] = sentiment["sentiment_label"]
            record["sarcasm_detected"] = sentiment["sarcasm_detected"]
            
            data_records.append(record)
        
        # Cluster by location and calculate heat zones
        clusters = cluster_grievances_by_location(data_records)
        
        # Format for frontend
        heat_zones = []
        for location, cluster_data in clusters.items():
            heat_zones.append({
                "location": location,
                "coords": cluster_data["coords"],
                "count": cluster_data["count"],
                "avg_sentiment": cluster_data["avg_sentiment"],
                "severity_color": cluster_data["severity_color"],
                "radii": cluster_data["radii"],
                "platforms": cluster_data["platforms"],
                "grievance_count": len(cluster_data["grievance_ids"]),
            })
        
        return {
            "status": "success",
            "heatmap": heat_zones,
            "total_clusters": len(heat_zones),
            "center": [10.3157, 123.8854],
            "zoom": 12
        }
        
    except Exception as e:
        print(f"ERROR in /api/heatmap: {str(e)}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# DATA ENDPOINT
# ============================================================================
@app.get("/api/data")
def get_raw_data():
    """
    Get all posts from Supabase with NLP analysis.
    
    Returns enriched post data with sentiment, sarcasm, and locations.
    """
    try:
        if not supabase_client:
            return {"status": "error", "message": "Supabase client not initialized"}
        
        # Fetch all posts from Supabase
        posts = supabase_client.get_all_posts()
        
        if not posts:
            print("⚠ No posts found in Supabase")
            return {"status": "success", "data": []}
        
        # Enrich with NLP processing
        data_records = []
        for post in posts:
            record = {
                "id": post.get("id"),
                "title": post.get("title", ""),
                "body": post.get("body", ""),
                "full_text": post.get("full_text", ""),
                "created_date": post.get("created_date"),
                "upvotes": post.get("upvotes", 0),
                "num_comments": post.get("num_comments", 0),
                "url": post.get("url", ""),
                "comments_text": post.get("comments_text", ""),
                "is_relevant": post.get("is_relevant", True),
            }
            
            # Sentiment Analysis
            sentiment = sentiment_analyzer.analyze(record["full_text"])
            record["sentiment_score"] = sentiment["sentiment_score"]
            record["sentiment_label"] = sentiment["sentiment_label"]
            record["sarcasm_detected"] = sentiment["sarcasm_detected"]
            record["sentiment_confidence"] = sentiment["confidence"]
            
            # Location Extraction
            locations = location_extractor.extract(record["full_text"])
            record["locations"] = locations
            
            data_records.append(record)
        
        print(f"✓ Processed {len(data_records)} records from Supabase with NLP")
        return {"status": "success", "data": data_records}
        
    except Exception as e:
        print(f"ERROR in /api/data: {str(e)}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# STATISTICS ENDPOINT
# ============================================================================
@app.get("/api/stats")
def get_statistics():
    """
    Get sentiment and location statistics from Supabase.
    
    Returns:
        {
            'total_grievances': int,
            'sentiment_breakdown': {'positive': int, 'neutral': int, 'negative': int},
            'avg_sentiment_score': float,
            'locations': [{'location': str, 'count': int, 'avg_sentiment': float}],
            'sarcasm_percentage': float,
        }
    """
    try:
        if not supabase_client:
            return {"status": "error", "message": "Supabase client not initialized"}
        
        posts = supabase_client.get_all_posts()
        
        if not posts:
            return {
                "status": "success",
                "total_grievances": 0,
                "sentiment_breakdown": {"positive": 0, "neutral": 0, "negative": 0},
                "avg_sentiment_score": 0.0,
                "locations": [],
                "sarcasm_percentage": 0.0,
            }
        
        # Analyze all records
        sentiment_labels_count = {"positive": 0, "neutral": 0, "negative": 0}
        sentiment_scores = []
        sarcasm_count = 0
        location_sentiment_map = {}
        
        for post in posts:
            text = post.get("full_text", post.get("title", ""))
            try:
                sentiment = sentiment_analyzer.analyze(text)
                label = sentiment["sentiment_label"]
                score = sentiment["sentiment_score"]
                
                sentiment_labels_count[label] += 1
                sentiment_scores.append(score)
                
                if sentiment["sarcasm_detected"]:
                    sarcasm_count += 1
                
                # Locations with sentiment
                locations = location_extractor.extract(text)
                for loc in locations:
                    if loc not in location_sentiment_map:
                        location_sentiment_map[loc] = []
                    location_sentiment_map[loc].append(score)
            except Exception as e:
                print(f"[WARNING] Error processing post {post.get('id')}: {e}")
                continue
        
        # Calculate location stats
        location_stats = []
        for loc, scores in location_sentiment_map.items():
            location_stats.append({
                "location": loc,
                "count": len(scores),
                "avg_sentiment": round(sum(scores) / len(scores), 2)
            })
        
        location_stats.sort(key=lambda x: x["count"], reverse=True)
        
        avg_sentiment = round(sum(sentiment_scores) / len(sentiment_scores), 2) if sentiment_scores else 0.0
        sarcasm_percentage = round(100 * sarcasm_count / len(posts), 1) if len(posts) > 0 else 0.0
        
        return {
            "status": "success",
            "total_grievances": len(posts),
            "sentiment_breakdown": sentiment_labels_count,
            "avg_sentiment_score": avg_sentiment,
            "locations": location_stats,
            "sarcasm_percentage": sarcasm_percentage,
        }
        
    except Exception as e:
        print(f"ERROR in /api/stats: {str(e)}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# ANALYZE ENDPOINT
# ============================================================================
@app.get("/api/analyze")
def analyze_text(text: str):
    """
    Analyze a given text for sentiment and locations.
    
    Query parameter: ?text=your%20text%20here
    
    Returns sentiment score, label, sarcasm detection, and extracted locations.
    """
    if not text:
        return {"status": "error", "message": "Text parameter is required"}
    
    sentiment = sentiment_analyzer.analyze(text)
    locations = location_extractor.extract(text)
    
    return {
        "status": "success",
        "text": text,
        "sentiment": sentiment,
        "locations": locations,
    }


# ============================================================================
# LOCATIONS ENDPOINT
# ============================================================================
@app.get("/api/locations")
def get_all_locations():
    """
    Get list of all known Cebu City locations from location extractor.
    """
    try:
        locations = list(location_extractor.cebu_locations.keys())
        return {
            "status": "success",
            "locations": locations,
            "count": len(locations)
        }
    except Exception as e:
        print(f"ERROR in /api/locations: {str(e)}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================
@app.get("/health")
def health_check():
    """
    Health check endpoint for deployment monitoring.
    """
    return {
        "status": "healthy",
        "service": "SentiMap Backend",
        "database": "Supabase",
        "version": "2.0"
    }


# ============================================================================
# ROOT ENDPOINT
# ============================================================================
@app.get("/")
def root():
    """
    SentiMap API Documentation
    """
    return {
        "name": "SentiMap API",
        "version": "2.0",
        "database": "Supabase",
        "endpoints": {
            "/api/data": "GET - All posts with NLP analysis",
            "/api/heatmap": "GET - Heat zones for Leaflet map",
            "/api/stats": "GET - Statistics and sentiment breakdown",
            "/api/analyze": "GET - Analyze custom text (?text=...)",
            "/api/locations": "GET - All Cebu locations",
            "/health": "GET - Health check"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run with: uvicorn main:app --reload
    uvicorn.run(app, host="127.0.0.1", port=8000)
