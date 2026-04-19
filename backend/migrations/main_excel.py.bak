from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from sentiment_analyzer import CebuanoSentimentAnalyzer
from location_extractor import CebuLocationExtractor
from geospatial import cluster_grievances_by_location, get_severity_color

app = FastAPI(title="SentiMap API")

# Initialize NLP modules
sentiment_analyzer = CebuanoSentimentAnalyzer()
location_extractor = CebuLocationExtractor()

# Allow your Frontend to talk to your Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins for development
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "reddit_data.xlsx")

@app.get("/api/heatmap")
def get_heatmap():
    """
    Get clustered grievance data for heatmap visualization.
    
    Returns heat zones by location with count, average sentiment, and severity.
    """
    try:
        df = pd.read_excel(DATA_PATH)
        df = df.rename(columns={
            "Faceplate-screen-reader-content": "title",
            "Time": "time_ago",
            "Faceplate-number": "upvotes",
            "Faceplate-number.1": "comments"
        })
        df = df[["title", "time_ago", "upvotes", "comments", "URL"]]
        df['upvotes'] = pd.to_numeric(df['upvotes'], errors='coerce').fillna(0).astype(int)
        df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0).astype(int)
        
        # Enrich with NLP
        data_records = []
        for idx, row in df.iterrows():
            record = row.to_dict()
            sentiment = sentiment_analyzer.analyze(record['title'])
            record['sentiment_score'] = sentiment['sentiment_score']
            record['sentiment_label'] = sentiment['sentiment_label']
            record['sarcasm_detected'] = sentiment['sarcasm_detected']
            locations = location_extractor.extract(record['title'])
            record['locations'] = locations
            data_records.append(record)
        
        # Cluster by location and calculate heat zones
        clusters = cluster_grievances_by_location(data_records)
        
        # Format for frontend
        heat_zones = []
        for location, cluster_data in clusters.items():
            heat_zones.append({
                'location': location,
                'coords': cluster_data['coords'],
                'count': cluster_data['count'],
                'avg_sentiment': cluster_data['avg_sentiment'],
                'severity_color': cluster_data['severity_color'],
                'radii': cluster_data['radii'],
                'platforms': cluster_data['platforms'],
                'grievance_count': len(cluster_data['grievance_ids']),
            })
        
        return {
            "status": "success",
            "heatmap": heat_zones,
            "total_clusters": len(heat_zones),
            "center": [10.3157, 123.8854],  # Cebu City center
            "zoom": 12
        }
        
    except Exception as e:
        print(f"ERROR in /api/heatmap: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.get("/api/data")
def get_raw_data():
    try:
        df = pd.read_excel(DATA_PATH)
        
        # Log actual columns for debugging
        print(f"DEBUG: Actual columns in Excel: {df.columns.tolist()}")
        print(f"DEBUG: First row preview: {df.iloc[0].to_dict() if len(df) > 0 else 'Empty'}")
        
        # Rename columns
        df = df.rename(columns={
            "Faceplate-screen-reader-content": "title",
            "Time": "time_ago",
            "Faceplate-number": "upvotes",
            "Faceplate-number.1": "comments"
        })

        # Keep only what we need
        df = df[["title", "time_ago", "upvotes", "comments", "URL"]]
        
        # CLEANUP: Ensure upvotes/comments are numbers (handles '1.2k' or empty)
        df['upvotes'] = pd.to_numeric(df['upvotes'], errors='coerce').fillna(0).astype(int)
        df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0).astype(int)

        # NLP Processing: Sentiment & Location extraction
        data_records = []
        for idx, row in df.iterrows():
            record = row.to_dict()
            
            # Sentiment Analysis on title
            sentiment = sentiment_analyzer.analyze(record['title'])
            record['sentiment_score'] = sentiment['sentiment_score']
            record['sentiment_label'] = sentiment['sentiment_label']
            record['sarcasm_detected'] = sentiment['sarcasm_detected']
            record['sentiment_confidence'] = sentiment['confidence']
            
            # Location Extraction
            locations = location_extractor.extract(record['title'])
            record['locations'] = locations
            
            data_records.append(record)
        
        print(f"DEBUG: Processed {len(data_records)} records with NLP")
        return {"status": "success", "data": data_records}
        
    except FileNotFoundError:
        print(f"ERROR: Excel file not found at {DATA_PATH}")
        return {"status": "error", "message": f"Data file not found at {DATA_PATH}"}
    except KeyError as e:
        print(f"ERROR: Missing expected column: {e}")
        return {"status": "error", "message": f"Missing column in Excel file: {e}. Check column names match the expected schema."}
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)}")
        return {"status": "error", "message": str(e)}


# Additional utility endpoints

@app.get("/api/stats")
def get_statistics():
    """
    Get sentiment and location statistics across all grievances.
    
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
        df = pd.read_excel(DATA_PATH)
        df = df.rename(columns={
            "Faceplate-screen-reader-content": "title",
            "Time": "time_ago",
            "Faceplate-number": "upvotes",
            "Faceplate-number.1": "comments"
        })
        df = df[["title", "time_ago", "upvotes", "comments", "URL"]]
        df['upvotes'] = pd.to_numeric(df['upvotes'], errors='coerce').fillna(0).astype(int)
        df['comments'] = pd.to_numeric(df['comments'], errors='coerce').fillna(0).astype(int)
        
        # Analyze all records
        sentiment_labels_count = {'positive': 0, 'neutral': 0, 'negative': 0}
        sentiment_scores = []
        sarcasm_count = 0
        location_sentiment_map = {}  # {location: [scores]}
        
        for idx, row in df.iterrows():
            sentiment = sentiment_analyzer.analyze(row['title'])
            label = sentiment['sentiment_label']
            score = sentiment['sentiment_score']
            
            sentiment_labels_count[label] += 1
            sentiment_scores.append(score)
            
            if sentiment['sarcasm_detected']:
                sarcasm_count += 1
            
            # Locations with sentiment
            locations = location_extractor.extract(row['title'])
            for loc in locations:
                if loc not in location_sentiment_map:
                    location_sentiment_map[loc] = []
                location_sentiment_map[loc].append(score)
        
        # Calculate location stats
        location_stats = []
        for loc, scores in location_sentiment_map.items():
            location_stats.append({
                'location': loc,
                'count': len(scores),
                'avg_sentiment': round(sum(scores) / len(scores), 2)
            })
        
        location_stats.sort(key=lambda x: x['count'], reverse=True)
        
        avg_sentiment = round(sum(sentiment_scores) / len(sentiment_scores), 2) if sentiment_scores else 0.0
        sarcasm_percentage = round(100 * sarcasm_count / len(df), 1) if len(df) > 0 else 0.0
        
        return {
            "status": "success",
            "total_grievances": len(df),
            "sentiment_breakdown": sentiment_labels_count,
            "avg_sentiment_score": avg_sentiment,
            "locations": location_stats,
            "sarcasm_percentage": sarcasm_percentage,
        }
        
    except Exception as e:
        print(f"ERROR in /api/stats: {str(e)}")
        return {"status": "error", "message": str(e)}


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


@app.get("/api/locations")
def get_all_locations():
    """
    Get list of all known Cebu City locations.
    
    Returns:
        {'status': 'success', 'locations': [str, ...]}
    """
    locations = location_extractor.get_all_locations()
    return {
        "status": "success",
        "locations": locations,
        "total": len(locations)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)