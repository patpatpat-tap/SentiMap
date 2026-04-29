"""
Geospatial data and utilities for Cebu City

Maps location names to coordinates and provides heat zone calculations.
"""

# Cebu City key locations with coordinates (lat, lng)
CEBU_COORDINATES = {
    "Cebu City": (10.3157, 123.8854),
    "SRP (South Road Properties)": (10.2790, 123.8805),
    "Talamban": (10.3850, 123.9080),
    "Mambaling": (10.3450, 123.8950),
    "Lahug": (10.3220, 123.9120),
    "Apas": (10.3100, 123.8920),
    "Banawa": (10.3380, 123.8850),
    "Coopers": (10.2950, 123.9200),
    "IT Park": (10.3260, 123.9070),
    "Mabolo": (10.3420, 123.9050),
    "Ayala (Business District)": (10.3130, 123.9230),
    "Salinas Drive": (10.3150, 123.8900),
    "Fuente Osmeña": (10.3050, 123.8820),
    "Mandaue City": (10.3230, 123.9220),
    "Talisay City": (10.2447, 123.8496),
    "Liloan": (10.3990, 123.9990),
    "Downtown Cebu": (10.2950, 123.8780),
    "Carbon Market Area": (10.2830, 123.8750),
    "Fort San Pedro Area": (10.2920, 123.8670),
    "Colon Street": (10.2940, 123.8720),
    "A.S. Fortuna Street": (10.3450, 123.9250),
    "Archbishop Reyes Avenue": (10.3200, 123.9060),
    "Ayala Mall": (10.3178, 123.9056),
    "Basak": (10.2928, 123.8687),
    "Bulacao": (10.2820, 123.8540),
    "Busay": (10.3540, 123.8780),
    "Capitol Site": (10.3175, 123.8912),
    "Carbon Market": (10.2917, 123.8986),
    "Carreta": (10.3150, 123.9100),
    "Cebu City Bypass": (10.3300, 123.9200),
    "Cogon": (10.3010, 123.8650),
    "Consolacion": (10.3956, 123.9614),
    "Escario Street": (10.3190, 123.8950),
    "Gaisano": (10.3050, 123.8950),
    "Gorordo Avenue": (10.3170, 123.9000),
    "Guadalupe": (10.3235, 123.8841),
    "Hernan Cortes Street": (10.3380, 123.9310),
    "Jones Avenue": (10.3050, 123.8930),
    "Juan Luna Street": (10.3150, 123.9150),
    "Labangon": (10.3040, 123.8760),
    "Mactan": (10.3090, 123.9820),
    "Magallanes Street": (10.2920, 123.9000),
    "Mango Avenue": (10.3120, 123.8970),
    "Minglanilla": (10.2450, 123.7930),
    "N. Bacalso Avenue": (10.2930, 123.8750),
    "North Road": (10.3500, 123.9350),
    "Osmeña Boulevard": (10.3080, 123.8930),
    "Pardo": (10.2840, 123.8560),
    "Pier Area": (10.2950, 123.9050),
    "Pungol": (10.3700, 123.8500),
    "Robinsons Place": (10.3087, 123.8943),
    "SM City Cebu": (10.3115, 123.9180),
    "SM Seaside": (10.2818, 123.8805),
    "Subangdaku": (10.3340, 123.9210),
    "Tisa": (10.3000, 123.8700),
    "Transcentral Highway": (10.3760, 123.8580),
    "Urgello": (10.3020, 123.8950),
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
            # Skip posts with no extracted location so they don't artificially stack up at the map center
            continue
        
        for location in locations:
            coords = CEBU_COORDINATES.get(location)
            if not coords:
                # Skip unmapped locations to avoid false hotspots at center
                continue
            if location not in clusters:
                clusters[location] = {
                    'coords': coords,
                    'count': 0,
                    'sentiment_scores': [],
                    'grievance_ids': [],
                    'sarcasm_count': 0,
                    'platforms': {},  # Count by platform
                }
            
            clusters[location]['count'] += 1
            clusters[location]['sentiment_scores'].append(grievance.get('sentiment_score', 0))
            clusters[location]['grievance_ids'].append(grievance.get('URL', ''))

            if grievance.get('sarcasm_detected', False):
                clusters[location]['sarcasm_count'] += 1
            
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
            'sarcasm_count': cluster['sarcasm_count'],
            'platforms': cluster['platforms'],
            'severity_color': get_severity_color(avg_sentiment),
            'radii': calculate_heat_zone_radius(cluster['count'], avg_sentiment),
        }
    
    return result
