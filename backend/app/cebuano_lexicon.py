"""
Cebuano Sentiment Lexicon - Domain-specific dictionary for Cebuano traffic discourse

This lexicon handles:
- Slang and colloquialisms specific to Cebuano
- Sarcasm indicators common in Cebuano culture
- Bislish (Cebuano-English code-switching) terms
- Traffic/enforcement domain-specific terms
"""

# Negative sentiment words (contextually negative traffic experience)
NEGATIVE_LEXICON = {
    # Traffic frustration
    "traffic": -0.8,
    "gridlock": -0.9,
    "hagit": -0.8,  # "harassment" in Cebuano
    "abuso": -0.9,  # "abuse"
    "injustice": -0.8,
    "corrupt": -0.9,
    "corrupted": -0.9,
    "corruption": -0.9,
    
    # Cebuano-specific negative expressions
    "linang": -0.9,  # "disgusting"
    "pabagal": -0.8,  # "slow" (frustration)
    "lisod": -0.8,  # "difficult"
    "malupit": -0.9,  # "cruel/harsh"
    "piston": -0.9,  # "favoritism/corruption" (Cebuano slang)
    "abot kaha": -0.8,  # "can't reach" (complaint)
    "walang saysay": -0.7,  # "meaningless"
    "basura": -0.9,  # "garbage/junk"
    "matay": -0.8,  # "dead" (as in bad service)
    "gasa": -0.8,  # "acting important" (negative)
    
    # English complements
    "terrible": -0.8,
    "horrible": -0.9,
    "awful": -0.8,
    "bad": -0.7,
    "worse": -0.8,
    "worst": -0.9,
    "hate": -0.9,
    "sucks": -0.8,
    "suck": -0.8,
    "crazy": -0.7,  # context-dependent
    "insane": -0.7,
    "ridiculous": -0.8,
    "pathetic": -0.9,
    "useless": -0.9,
    "waste": -0.8,
    "unfair": -0.8,
    "biased": -0.8,
    "delayed": -0.7,
    "slow": -0.6,
    "stuck": -0.7,
    "jam": -0.7,
    "congestion": -0.7,
    
    # Cebuano curse-adjacent (domain-appropriate)
    "putok": -0.9,  # outburst expression
    "ayaw ko": -0.7,  # "I don't like"
    "ayaw": -0.6,  # "don't like"
    "tuyot": -0.8,  # "bad luck/dire"
    
    # Sarcasm markers with negative intent (often appear with positive words in sarcasm)
    "comfort": -0.3,  # Often used sarcastically: "so comfortable!"
    "beautiful": -0.3,  # Often used sarcastically
    "wonderful": -0.3,  # Often used sarcastically
    "great": -0.3,  # Can be sarcastic
    "perfect": -0.3,  # Often sarcastic
    "amazing": -0.3,  # Often sarcastic
}

# Positive sentiment words (good traffic experience / praise)
POSITIVE_LEXICON = {
    # Traffic improvement
    "smooth": 0.8,
    "fast": 0.7,
    "quick": 0.7,
    "easy": 0.7,
    "efficient": 0.8,
    "clear": 0.7,
    "improve": 0.8,
    "improvement": 0.8,
    "better": 0.8,
    "best": 0.9,
    "good": 0.7,
    "great": 0.8,
    "excellent": 0.9,
    "awesome": 0.8,
    "nice": 0.7,
    
    # Cebuano-specific positive
    "ayos": 0.8,  # "all good/ok"
    "maayos": 0.8,  # "organized/good"
    "salamat": 0.7,  # "thank you"
    "thank you": 0.7,
    "maganda": 0.8,  # "beautiful" (genuine context)
    "okay": 0.6,
    "okay lang": 0.7,  # "fairly okay"
    "sapat": 0.6,  # "sufficient"
    "napakaganda": 0.9,  # "very beautiful" (genuine)
    "napakahusay": 0.9,  # "very excellent"
    
    # Fair/just/professional enforcement (positive context)
    "fair": 0.8,
    "professional": 0.8,
    "respect": 0.7,
    "accountability": 0.8,
    
    # Service improvements
    "helpful": 0.8,
    "helpful officer": 0.9,
    "police": 0.5,  # neutral baseline
    "enforce": 0.5,  # neutral in enforcement context
    "solution": 0.8,
}

# Sarcasm indicators - words/phrases that often precede sarcasm
SARCASM_MARKERS = {
    "hayahay": True,  # "comfortable" - classic sarcasm marker
    "kaya": True,  # "that's why" - often sarcastic
    "sure": True,  # "sure"
    "yeah right": True,
    "great job": False,  # Context-dependent: can be genuine
    "nice work": False,  # Context-dependent
    "so comfortable": True,  # Definitely sarcastic in traffic context
    "so smooth": True,  # Sarcastic about traffic
    "super efficient": True,  # Likely sarcastic about traffic
}

# Cebu City locations - Keywords for geolocation extraction
CEBU_LOCATIONS = {
    # Major roads/highways
    "srp": "SRP (South Road Properties)",
    "north road": "North Road",
    "north rd": "North Road",
    "bypas": "Bypass (Cebu City Bypass)",
    "bypass": "Bypass (Cebu City Bypass)",
    "mabolo": "Mabolo",
    "mambaling": "Mambaling",
    "apas": "Apas",
    "lahug": "Lahug",
    "busay": "Busay",
    "banawa": "Banawa",
    "talamban": "Talamban",
    "coopers": "Coopers",
    "cooper": "Coopers",
    "mandaue": "Mandaue City",
    "mandawe": "Mandaue City",
    "talisay": "Talisay City",
    "liloan": "Liloan",
    
    # Business districts
    "ayala": "Ayala (Business District)",
    "it park": "IT Park",
    "cebu business park": "Cebu Business Park",
    "cbp": "Cebu Business Park",
    "erf": "Erf (East Road)",
    "east road": "East Road",
    
    # Landmarks/Districts
    "downtown": "Downtown Cebu",
    "carbon": "Carbon Market Area",
    "colon": "Colon Street",
    "fort san pedro": "Fort San Pedro Area",
    "santo niño": "Santo Niño Area",
    "basilica": "Basilica Area",
    "pier": "Pier Area",
    "waterfront": "Waterfront Area",
    
    # Schools/Institutions
    "usc": "University of San Carlos",
    "cit": "Cebu Institute of Technology",
    "cebu doc": "Cebu Doctors' Hospital Area",
    
    # Intersections/Specific roads
    "gorordo": "Gorordo Avenue",
    "manalili": "Manalili",
    "salinas": "Salinas Drive",
    "fuente": "Fuente Osmeña",
    "juan luna": "Juan Luna Street",
    "magallanes": "Magallanes Street",
    "maria cristina": "Maria Cristina Street",
    "sarao": "Sarao Street",
    "f cabahug": "F. Cabahug Street",
    
    # Shopping areas
    "sm cebu": "SM Cebu",
    "ayala mall": "Ayala Mall",
    "robinsons": "Robinsons Place",
    "gaisano": "Gaisano",
    
    # General city reference
    "cebu city": "Cebu City",
    "cebu": "Cebu City",  # Ambiguous but often means Cebu City
}

# Domain-specific traffic terms
TRAFFIC_TERMS = {
    "enforcers": True,
    "enforcer": True,
    "cops": True,
    "police": True,
    "solong": True,  # "SOLONG" - traffic enforcement unit
    "traffic": True,
    "checkpoints": True,
    "checkpoint": True,
    "apprehended": True,
    "apprehend": True,
    "violation": True,
    "violators": True,
    "ticket": True,
    "arrested": True,
    "arrest": True,
    "driving": True,
    "license": True,
    "vehicle": True,
    "motorcycle": True,
    "motorbike": True,
    "car": True,
    "bike": True,
    "driveway": True,
    "road": True,
    "street": True,
    "intersection": True,
    "lane": True,
    "commute": True,
    "commuter": True,
    "petty": True,  # "petty" enforcement
    "bribes": True,
    "bribe": True,
    "extort": True,
    "extortion": True,
    "quota": True,
    "malicious": True,
}
