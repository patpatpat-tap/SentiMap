"""
Geospatial data and utilities for Cebu City

Maps location names to coordinates and provides heat zone calculations.
"""

# Cebu City key locations with coordinates (lat, lng)
CEBU_COORDINATES = {
    "Cebu City": (10.3157, 123.8854),
    "SRP (South Road Properties)": (10.2786, 123.9149),
    "Talamban": (10.3850, 123.9080),
    "Mambaling": (10.3450, 123.8950),
    "Lahug": (10.3220, 123.9120),
    "Apas": (10.3100, 123.8920),
    "Banawa": (10.3380, 123.8850),
    "Coopers": (10.2950, 123.9200),
    "IT Park": (10.3180, 123.9750),
    "Mabolo": (10.3420, 123.9050),
    "Ayala (Business District)": (10.3130, 123.9230),
    "Salinas Drive": (10.3150, 123.8900),
    "Fuente Osmeña": (10.3050, 123.8820),
    "Mandaue City": (10.3660, 123.9750),
    "Talisay City": (10.2480, 123.9300),
    "Liloan": (10.2150, 123.9850),
    "Downtown Cebu": (10.2950, 123.8780),
    "Carbon Market Area": (10.2830, 123.8750),
    "Fort San Pedro Area": (10.2920, 123.8670),
    "Colon Street": (10.2940, 123.8720),
}


def get_location_center(location_name: str) -> tuple:
    """
    Get latitude and longitude for a location.
    
    Returns:
        (lat, lng) tuple, or None if not found
    """
    return CEBU_COORDINATES.get(location_name)


def calculate_heat_zone_radius(count: int, polarity: float) -> dict:
    """
    Calculate three-layer heat zone radii based on complaint count and severity.
    
    Args:
        count: Number of complaints at this location
        polarity: Average sentiment (-1.0 to 1.0), converted to severity (0.0 to 1.0)
    
    Returns:
        {
            'outer': radius in meters (largest, ~5% opacity),
            'mid': radius in meters (~12% opacity),
            'core': radius in meters (interactive, 80-95% opacity)
        }
    """
    # Convert polarity (-1 to 1) to severity (0 to 1)
    # Negative polarity = high severity
    severity = max(0, -polarity)
    
    return {
        'outer': 200 + count * 80 + severity * 150,
        'mid': 100 + count * 50 + severity * 80,
        'core': 50 + count * 30 + severity * 40,
    }


def get_severity_color(polarity: float) -> str:
    """
    Get severity color based on sentiment polarity.
    
    Args:
        polarity: Sentiment score (-1.0 to 1.0)
    
    Returns:
        Hex color code: Red (critical) → Orange (moderate) → Yellow (low)
    """
    severity = max(0, -polarity)  # Convert negative sentiment to severity
    
    if severity > 0.66:  # Critical (high negative sentiment)
        return "#ef4444"  # Red
    elif severity > 0.33:  # Moderate
        return "#f97316"  # Orange
    else:  # Low
        return "#eab308"  # Yellow


def cluster_grievances_by_location(grievances: list) -> dict:
    """
    Cluster grievances by extracted location.
    
    Args:
        grievances: List of grievance records with 'locations' and 'sentiment_score' fields
    
    Returns:
        {
            'location_name': {
                'coords': (lat, lng),
                'count': int,
                'avg_sentiment': float,
                'grievances': [grievance_ids],
                'severity_color': str,
                'radii': {outer, mid, core}
            }
        }
    """
    clusters = {}
    
    for grievance in grievances:
        locations = grievance.get('locations', [])
        
        if not locations:
            # Default to Cebu City if no location extracted
            locations = ['Cebu City']
        
        for location in locations:
            if location not in clusters:
                coords = CEBU_COORDINATES.get(location, (10.3157, 123.8854))
                clusters[location] = {
                    'coords': coords,
                    'count': 0,
                    'sentiment_scores': [],
                    'grievance_ids': [],
                    'platforms': {},  # Count by platform
                }
            
            clusters[location]['count'] += 1
            clusters[location]['sentiment_scores'].append(grievance.get('sentiment_score', 0))
            clusters[location]['grievance_ids'].append(grievance.get('URL', ''))
            
            # Track platform counts
            platform = grievance.get('platform', 'unknown')
            clusters[location]['platforms'][platform] = clusters[location]['platforms'].get(platform, 0) + 1
    
    # Calculate aggregates and add styling
    result = {}
    for location, cluster in clusters.items():
        avg_sentiment = sum(cluster['sentiment_scores']) / len(cluster['sentiment_scores']) if cluster['sentiment_scores'] else 0
        
        result[location] = {
            'coords': cluster['coords'],
            'count': cluster['count'],
            'avg_sentiment': round(avg_sentiment, 2),
            'grievance_ids': cluster['grievance_ids'],
            'platforms': cluster['platforms'],
            'severity_color': get_severity_color(avg_sentiment),
            'radii': calculate_heat_zone_radius(cluster['count'], avg_sentiment),
        }
    
    return result
