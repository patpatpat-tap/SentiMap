"""
Cebuano Sentiment Lexicon v2.0
================================
Domain: Traffic Enforcement Grievances in Cebu City
Research: "Geospatial Sentiment Analysis: A Hybrid NLP Approach for
Mapping Traffic Enforcement Grievances in Cebu City"

Version 2.0 improvements over v1:
- Fixed contradictions (words appearing in both positive and negative)
- Expanded from 40 to 200+ sentiment terms
- Added authentic Bislish expressions from validated post corpus
- Expanded sarcasm detection from 7 to 30+ patterns
- Added Cebuano-specific enforcement and corruption vocabulary
- Added emoji and emoticon sentiment markers
- Added intensifiers that modify sentiment scores
- Separated ambiguous words into context-dependent category

Lexicon construction methodology:
- Core terms sourced from validated post corpus (142 clean posts)
- Supplemented with Cebuano linguistic references
- Sarcasm patterns validated against manually reviewed examples
- All scores validated against human judgment on sample posts
"""

# ─────────────────────────────────────────────────────────────
# NEGATIVE SENTIMENT LEXICON
# Score range: -0.1 (mildly negative) to -1.0 (extremely negative)
# ─────────────────────────────────────────────────────────────
NEGATIVE_LEXICON = {

    # ── CEBUANO FRUSTRATION & EXASPERATION ──────────────────
    "puryagaba":       -0.9,   # strong Cebuano exasperation
    "hangak":          -0.8,   # exhausted/fed up
    "luod":            -0.9,   # disgusted
    "libog":           -0.6,   # confused frustration
    "nasubo":          -0.7,   # disappointed
    "nasukaon":        -0.9,   # fed up/had enough
    "naratol":         -0.8,   # irritated
    "nalagot":         -0.8,   # got annoyed
    "makalagot":       -0.9,   # annoying/infuriating
    "makaguol":        -0.8,   # saddening/frustrating
    "makastress":      -0.8,   # stressful
    "kapoy na":        -0.8,   # so tired of this
    "kapoy kaayo":     -0.9,   # extremely tired/fed up
    "kapoy":           -0.6,   # tired (mild)
    "gi kapoy":        -0.8,   # gotten tired of
    "di na kaya":      -0.9,   # can't take it anymore
    "dili na kaya":    -0.9,   # can't endure anymore
    "di na":           -0.5,   # can't/won't anymore (mild)
    "grabe":           -0.8,   # intense negative (context-dependent)
    "grabi":           -0.8,   # Cebuano variant of grabe
    "grabe kaayo":     -0.9,   # extremely bad
    "grabi kaayo":     -0.9,   # extremely bad (variant)
    "grabeh":          -0.8,   # another variant
    "daotan":          -0.8,   # bad/negative
    "dili maayo":      -0.7,   # not good
    "sayop":           -0.7,   # wrong/mistake
    "supak":           -0.7,   # defiant/improper
    "hilak nalang":    -0.9,   # situation so bad you want to cry
    "naluha":          -0.8,   # cried (from frustration)
    "stress":          -0.7,   # stressed
    "frustrated":      -0.8,   # frustrated
    "frustrating":     -0.8,   # frustrating

    # ── CEBUANO CURSE-ADJACENT (domain-appropriate) ──────────
    "yawa":            -0.8,   # strong Cebuano expletive (devil)
    "piste":           -0.9,   # Cebuano expletive
    "bwisit":          -0.9,   # Tagalog/Cebuano: bad luck/annoying
    "yawaa":           -0.9,   # intensified yawa
    "animal":          -0.8,   # used as insult in context
    "giatay":          -0.9,   # strong Cebuano expletive
    "atay":            -0.7,   # mild Cebuano expletive
    "puta":            -0.9,   # strong expletive
    "gago":            -0.9,   # stupid/idiot
    "bobo":            -0.7,   # stupid
    "buang":           -0.8,   # crazy/stupid (Cebuano)
    "tiguwang nga":    -0.7,   # dismissive insult
    "walay pulos":     -0.9,   # useless/worthless
    "walay silbi":     -0.9,   # no use/worthless

    # ── TRAFFIC-SPECIFIC NEGATIVE ────────────────────────────
    "traffic":         -0.7,   # traffic (almost always negative in context)
    "trapik":          -0.7,   # Cebuano: traffic
    "congestion":      -0.7,   # road congestion
    "gridlock":        -0.9,   # complete gridlock
    "standstill":      -0.8,   # traffic standstill
    "bumper to bumper":-0.8,   # heavy traffic
    "heavy traffic":   -0.8,   # heavy traffic
    "traffic jam":     -0.9,   # traffic jam
    "stuck":           -0.7,   # stuck in traffic
    "late":            -0.6,   # caused to be late
    "delayed":         -0.6,   # delayed
    "nag abang":       -0.5,   # waiting long time
    "dugay":           -0.6,   # takes too long
    "dugay kaayo":     -0.8,   # takes extremely long
    "wa na ko":        -0.8,   # gave up

    # ── ENFORCEMENT ABUSE & CORRUPTION ──────────────────────
    "abuso":           -0.9,   # abuse of authority
    "nag-abuso":       -0.9,   # abusing authority
    "corrupt":         -0.9,   # corrupt
    "corruption":      -0.9,   # corruption
    "kotong":          -0.9,   # bribery/extortion by authority
    "hulidap":         -0.9,   # robbery by authority figures
    "extortion":       -0.9,   # extortion
    "extort":          -0.9,   # to extort
    "bribe":           -0.9,   # bribe
    "lagay":           -0.9,   # bribe (Filipino term)
    "palakasan":       -0.8,   # favoritism system
    "pabor":           -0.7,   # favoritism
    "under the table": -0.9,   # illegal payment
    "quota":           -0.8,   # traffic quota system (negative)
    "unjust":          -0.8,   # unjust
    "injustice":       -0.8,   # injustice
    "unfair":          -0.8,   # unfair
    "biased":          -0.8,   # biased
    "walang silbi":    -0.9,   # useless (Tagalog)
    "walang kwenta":   -0.9,   # worthless
    "peke":            -0.8,   # fake/fraudulent
    "manggilaw":       -0.8,   # taking bribes (Cebuano)

    # ── DRIVER/TRANSPORT NEGATIVE ────────────────────────────
    "bastos":          -0.8,   # rude/disrespectful
    "walang galang":   -0.9,   # disrespectful
    "walay respeto":   -0.9,   # Cebuano: no respect
    "pasaway":         -0.8,   # troublemaker/rule-breaker
    "siga":            -0.7,   # arrogant/showing off
    "suplado":         -0.7,   # snobbish/unfriendly
    "harang":          -0.7,   # blocking
    "counterflow":     -0.7,   # driving against traffic
    "reckless":        -0.8,   # reckless
    "speeding":        -0.7,   # speeding
    "overloading":     -0.7,   # vehicle overloading
    "overcharging":    -0.8,   # fare overcharging
    "dagdag":          -0.7,   # illegal surcharge
    "singit":          -0.7,   # cutting in line
    "dagdag-singko":   -0.8,   # illegal fare addition
    "fast timer":      -0.9,   # tampered taxi meter
    "tampered":        -0.9,   # tampered meter
    "manloloko":       -0.9,   # cheater/deceiver
    "scammer":         -0.9,   # scammer

    # ── INFRASTRUCTURE FAILURE ───────────────────────────────
    "counterproductive":-0.8,  # counterproductive (esp. BRT context)
    "overbudget":      -0.7,   # over budget
    "over budget":     -0.7,   # over budget
    "delay":           -0.6,   # project delay
    "unfinished":      -0.7,   # unfinished project
    "incomplete":      -0.6,   # incomplete
    "worn":            -0.6,   # worn out/deteriorating
    "deteriorating":   -0.7,   # deteriorating
    "pothole":         -0.8,   # road potholes
    "butas ang dalan": -0.8,   # Cebuano: road has holes
    "bato-bato":       -0.6,   # rocky/rough road
    "grabe ang dalan": -0.8,   # road is terrible
    "blacklisted":     -0.9,   # blacklisted contractor
    "anomalya":        -0.9,   # anomaly/corruption (Filipino)

    # ── ENGLISH NEGATIVE (domain-relevant) ──────────────────
    "terrible":        -0.8,
    "horrible":        -0.9,
    "awful":           -0.8,
    "bad":             -0.6,
    "worse":           -0.7,
    "worst":           -0.9,
    "hate":            -0.9,
    "sucks":           -0.8,
    "pathetic":        -0.9,
    "useless":         -0.9,
    "waste":           -0.7,
    "ridiculous":      -0.7,
    "absurd":          -0.8,
    "outrageous":      -0.8,
    "disgusting":      -0.9,
    "appalling":       -0.9,
    "unacceptable":    -0.9,
    "dangerous":       -0.8,
    "unsafe":          -0.8,
    "incompetent":     -0.9,
    "negligent":       -0.8,

    # ── CEBUANO LEGACY (kept from v1 — validated) ────────────
    "hagit":           -0.8,   # harassment
    "linang":          -0.9,   # disgusting
    "pabagal":         -0.7,   # slow (frustration)
    "lisod":           -0.7,   # difficult
    "malupit":         -0.9,   # cruel/harsh
    "basura":          -0.8,   # garbage/junk (metaphorical)
    "ayaw ko":         -0.6,   # I don't like
    "tuyot":           -0.7,   # bad luck/dire situation
    "putok":           -0.9,   # outburst expression
}


# ─────────────────────────────────────────────────────────────
# POSITIVE SENTIMENT LEXICON
# Score range: 0.1 (mildly positive) to 1.0 (extremely positive)
# ─────────────────────────────────────────────────────────────
POSITIVE_LEXICON = {

    # ── CEBUANO POSITIVE EXPRESSIONS ─────────────────────────
    "maayo":           0.8,    # good
    "maayos":          0.8,    # organized/well-done
    "ayos":            0.7,    # all good/okay
    "tarong":          0.7,    # proper/correct
    "husay":           0.8,    # organized
    "klaro":           0.7,    # clear/proper
    "sakto":           0.7,    # just right/correct
    "epektibo":        0.8,    # effective
    "padayon":         0.6,    # keep going (encouragement)
    "puwede":          0.5,    # acceptable/okay
    "okay lang":       0.6,    # fairly okay
    "ayos ra":         0.6,    # it's fine/okay
    "maayo man":       0.7,    # it's actually good
    "dako nga tabang": 0.9,    # big help
    "naayo":           0.8,    # got better
    "nagamay":         0.7,    # improved
    "nagmaayo":        0.8,    # getting better
    "salamat":         0.6,    # thank you
    "gipasalamat":     0.7,    # expressed gratitude
    "angay":           0.7,    # appropriate/deserving
    "tarong na":       0.7,    # now proper/correct
    "dali":            0.7,    # fast/easy
    "dali ra":         0.7,    # easy enough
    "paspas":          0.6,    # fast (positive in commute context)
    "smooth":          0.8,    # smooth flow
    "libre":           0.6,    # free (positive when genuine)
    "serbisyo":        0.5,    # service (neutral-positive)

    # ── ENFORCEMENT PRAISE ───────────────────────────────────
    "fair":            0.8,    # fair enforcement
    "professional":    0.8,    # professional conduct
    "accountable":     0.8,    # accountability
    "accountability":  0.8,    # accountability
    "helpful":         0.8,    # helpful officer
    "courteous":       0.8,    # courteous officer
    "matino":          0.8,    # upright/decent (Cebuano)
    "tapat":           0.8,    # honest/loyal (Cebuano)
    "effective":       0.8,    # effective enforcement
    "strict":          0.6,    # strict (positive in enforcement)
    "implemented":     0.6,    # properly implemented
    "enforced":        0.6,    # properly enforced

    # ── INFRASTRUCTURE PRAISE ────────────────────────────────
    "improvement":     0.8,
    "improved":        0.8,
    "better":          0.7,
    "best":            0.9,
    "efficient":       0.8,
    "solution":        0.7,
    "progress":        0.7,
    "upgrade":         0.7,
    "modernized":      0.8,
    "functional":      0.7,
    "operational":     0.7,
    "opened":          0.6,    # new road/facility opened
    "completed":       0.7,    # project completed

    # ── ENGLISH POSITIVE ─────────────────────────────────────
    "good":            0.7,
    "great":           0.8,    # NOTE: removed from negative — context handles sarcasm
    "excellent":       0.9,
    "awesome":         0.8,
    "nice":            0.6,
    "fast":            0.7,
    "quick":           0.7,
    "easy":            0.7,
    "clear":           0.6,
    "safe":            0.8,
    "safer":           0.8,
    "respect":         0.7,
}


# ─────────────────────────────────────────────────────────────
# SARCASM DETECTION SYSTEM
#
# Sarcasm in Cebuano traffic discourse works in layers:
# 1. Marker words that signal sarcastic intent
# 2. Positive words used in negative context (ironic praise)
# 3. Resignation patterns (laughing at a bad situation)
# 4. Structural patterns ("supposed to X but actually Y")
#
# For a post to be flagged sarcastic, it needs:
# - At least one SARCASM_MARKER, OR
# - A POSITIVE_IN_NEGATIVE_CONTEXT pattern + traffic/enforcement term
# ─────────────────────────────────────────────────────────────
SARCASM_MARKERS = {

    # ── PRIMARY CEBUANO SARCASM MARKERS ──────────────────────
    # These alone are strong signals of sarcasm in traffic context
    "hayahay":              True,   # "comfortable" — classic Cebuano sarcasm
    "hayahay kaayo":        True,   # intensified
    "hayahay man":          True,   # variant
    "hahayz":               True,   # resigned sarcasm (laugh-cry)
    "puryagaba":            True,   # can signal sarcastic exasperation
    "kanus-a pa kaha":      True,   # "when will it ever happen"
    "kanus-a pa":           True,   # shorter variant
    "padayon cebu":         True,   # "keep it up Cebu" — often sarcastic
    "proud cebuano":        True,   # can be sarcastic in complaint context
    "mao nay Cebu":         True,   # "this is Cebu" — resignation
    "mao ni":               True,   # "this is how it is" — resigned

    # ── FILIPINO SARCASM MARKERS ─────────────────────────────
    "sana all":             True,   # sarcastic wish
    "nakaka-proud":         True,   # "makes you proud" — often sarcastic
    "galing":               True,   # "great/skilled" — often sarcastic
    "ang galing":           True,   # intensified sarcastic praise
    "taas ng noo":          True,   # arrogance — sarcastic
    "swabe":                True,   # "smooth" — often sarcastic

    # ── IRONIC PRAISE PATTERNS ───────────────────────────────
    # Positive words used sarcastically in traffic/enforcement context
    "so comfortable":       True,
    "so smooth":            True,
    "so efficient":         True,
    "very efficient":       True,   # likely sarcastic about CITOM/LTO
    "so professional":      True,
    "great job":            True,   # in complaint context
    "well done":            True,   # in complaint context
    "congratulations":      True,   # in complaint context
    "thank you CITOM":      True,   # almost always sarcastic
    "thank you LTO":        True,   # almost always sarcastic
    "thank you traffic":    True,   # sarcastic thanks to traffic
    "salamat CITOM":        True,   # Cebuano sarcastic thanks
    "salamat LTO":          True,   # Cebuano sarcastic thanks
    "naayo ang Cebu":       True,   # "Cebu is fixed now" — sarcastic

    # ── RESIGNED SARCASM PATTERNS ────────────────────────────
    # Laughing at a hopeless situation
    "😂😭":                 True,   # laugh-cry combo = resigned sarcasm
    "hahaha ang traffic":   True,
    "lol traffic":          True,
    "hhaha":                True,   # dismissive laugh about serious issue
    "char":                 True,   # "just kidding" but used sarcastically
    "charot":               True,   # "just kidding" variant

    # ── STRUCTURAL IRONY PATTERNS ────────────────────────────
    # "Supposed to X but actually Y" = ironic framing
    "supposed to decongest": True,
    "supposed to help":      True,
    "supposed to improve":   True,
    "counterproductive":     True,  # especially in BRT/traffic context
    "ironic":                True,
    "ironically":            True,
    "funny how":             True,
    "isn't it funny":        True,
    "dba funny":             True,
}

# Words that are ONLY sarcastic when appearing WITH a traffic/enforcement term
# These cannot be sarcasm triggers on their own
CONTEXT_DEPENDENT_SARCASM = {
    "wow":         ["traffic", "enforcer", "CITOM", "LTO", "jeepney",
                    "trapik", "checkpoint", "commute"],
    "nice":        ["traffic", "dalan", "karsada", "enforcer"],
    "perfect":     ["traffic", "trapik", "commute", "CITOM"],
    "amazing":     ["traffic", "commute", "enforcer"],
    "love it":     ["traffic", "commute", "jeepney"],
    "enjoy":       ["traffic", "commute", "trapik"],
    "unta":        ["maayo", "tarong", "ayos"],  # hopeful = resigned
}


# ─────────────────────────────────────────────────────────────
# INTENSIFIERS — modify the score of adjacent sentiment words
# An intensifier multiplies the score of the next sentiment word
# ─────────────────────────────────────────────────────────────
INTENSIFIERS = {
    # Cebuano intensifiers
    "kaayo":    1.5,    # very/extremely (most common Cebuano intensifier)
    "gyud":     1.3,    # really/truly
    "jud":      1.3,    # variant of gyud
    "gyud kaayo": 1.7,  # really extremely
    "sobra":    1.4,    # excessive/too much
    "sobra kaayo": 1.6, # extremely excessive
    "grabe":    1.4,    # intense (as intensifier)
    "grabi":    1.4,    # variant

    # Filipino intensifiers
    "talaga":   1.3,    # really/truly
    "sobra":    1.4,    # excessive
    "napaka":   1.5,    # very (prefix)
    "naman":    1.2,    # mild emphasis

    # English intensifiers
    "very":     1.3,
    "really":   1.3,
    "so":       1.2,
    "extremely": 1.5,
    "super":    1.4,
    "absolutely": 1.5,
    "completely": 1.4,
    "totally":  1.3,
}

# Negation words — flip the sentiment score when preceding a sentiment word
NEGATIONS = {
    "hindi":    True,   # not (Tagalog)
    "dili":     True,   # not (Cebuano)
    "di":       True,   # not (short form)
    "wala":     True,   # none/not
    "walay":    True,   # none of (Cebuano)
    "not":      True,
    "no":       True,
    "never":    True,
    "without":  True,
    "dili man": True,   # not really
    "wala man": True,   # not really
}


# ─────────────────────────────────────────────────────────────
# CEBU CITY LOCATIONS
# For geospatial extraction — maps text mentions to location names
# Coordinates are in geospatial.py
# ─────────────────────────────────────────────────────────────
CEBU_LOCATIONS = {
    # ── HIGH CONFIDENCE LOCATIONS ─────────────────────────────
    "srp":                  "SRP (South Road Properties)",
    "south road properties":"SRP (South Road Properties)",
    "south road":           "SRP (South Road Properties)",
    "mambaling":            "Mambaling",
    "talamban":             "Talamban",
    "lahug":                "Lahug",
    "it park":              "IT Park",
    "itpark":               "IT Park",
    "i.t. park":            "IT Park",
    "fuente osmeña":        "Fuente Osmeña",
    "fuente osmena":        "Fuente Osmeña",
    "fuente circle":        "Fuente Osmeña",
    "fuente":               "Fuente Osmeña",
    "mandaue":              "Mandaue City",
    "mandawe":              "Mandaue City",
    "mactan":               "Mactan",
    "consolacion":          "Consolacion",
    "talisay":              "Talisay City",
    "liloan":               "Liloan",
    "minglanilla":          "Minglanilla",
    "bulacao":              "Bulacao",
    "banawa":               "Banawa",
    "guadalupe":            "Guadalupe",
    "basak":                "Basak",
    "salinas drive":        "Salinas Drive",
    "salinas":              "Salinas Drive",
    "bacalso":              "N. Bacalso Avenue",
    "n. bacalso":           "N. Bacalso Avenue",
    "national bacalso":     "N. Bacalso Avenue",
    "transcentral":         "Transcentral Highway",
    "transcentral highway": "Transcentral Highway",
    "pardo":                "Pardo",
    "capitol":              "Capitol Site",
    "capitol site":         "Capitol Site",
    "urgello":              "Urgello",
    "subangdaku":           "Subangdaku",
    "hernan cortes":        "Hernan Cortes Street",
    "a.s. fortuna":         "A.S. Fortuna Street",
    "as fortuna":           "A.S. Fortuna Street",
    "fortuna":              "A.S. Fortuna Street",
    "escario":              "Escario Street",
    "gorordo":              "Gorordo Avenue",
    "archbishop reyes":     "Archbishop Reyes Avenue",
    "reyes ave":            "Archbishop Reyes Avenue",
    "jones ave":            "Jones Avenue",
    "jones avenue":         "Jones Avenue",
    "juan luna":            "Juan Luna Street",
    "magallanes":           "Magallanes Street",
    "osmena blvd":          "Osmeña Boulevard",
    "osmena boulevard":     "Osmeña Boulevard",
    "osmeña blvd":          "Osmeña Boulevard",
    "osmeña boulevard":     "Osmeña Boulevard",
    "mango avenue":         "Mango Avenue",
    "mango ave":            "Mango Avenue",
    "national bookstore mango": "Mango Avenue",

    # ── BUSINESS/COMMERCIAL AREAS ─────────────────────────────
    "ayala":                "Ayala (Business District)",
    "ayala center":         "Ayala (Business District)",
    "ayala cebu":           "Ayala (Business District)",
    "ayala mall":           "Ayala Mall",
    "robinsons":            "Robinsons Place",
    "robinsons place":      "Robinsons Place",
    "sm cebu":              "SM City Cebu",
    "sm city cebu":         "SM City Cebu",
    "sm seaside":           "SM Seaside",
    "seaside":              "SM Seaside",
    "carbon":               "Carbon Market",
    "carbon market":        "Carbon Market",
    "colon street":         "Colon Street",
    "metro colon":          "Colon Street",
    "gaisano":              "Gaisano",
    "pier":                 "Pier Area",
    "pier area":            "Pier Area",

    # ── GENERAL AREAS ────────────────────────────────────────
    "mabolo":               "Mabolo",
    "apas":                 "Apas",
    "busay":                "Busay",
    "pungol":               "Pungol",
    "labangon":             "Labangon",
    "tisa":                 "Tisa",
    "carreta":              "Carreta",
    "cogon":                "Cogon",
    "north road":           "North Road",
    "bypass":               "Cebu City Bypass",

    # ── GENERIC FALLBACK (lowest confidence) ─────────────────
    "cebu city":            "Cebu City",
    "cebu":                 "Cebu City",
}


# ─────────────────────────────────────────────────────────────
# TRAFFIC & ENFORCEMENT DOMAIN TERMS
# Used to verify a post is in the traffic domain
# before applying sentiment analysis
# ─────────────────────────────────────────────────────────────
TRAFFIC_TERMS = {
    # Enforcement agencies
    "CITOM": True, "CCTO": True, "LTFRB": True, "LTO": True,
    "traffic enforcer": True, "traffic officer": True,
    "traffic police": True, "pulis": True, "polis": True,

    # Enforcement actions
    "apprehended": True, "apprehend": True,
    "giapprehend": True, "naapprehend": True,
    "checkpoint": True, "checkpoints": True,
    "violation": True, "violators": True,
    "ticket": True, "fine": True,
    "arrested": True, "arrest": True,
    "towed": True, "towing": True,
    "colorum": True, "kotong": True,

    # Violations
    "counterflow": True, "reckless driving": True,
    "illegal parking": True, "smoke belching": True,
    "overloading": True, "speeding": True,
    "no license": True, "no plate": True,

    # Vehicles
    "jeepney": True, "jeep": True, "taxi": True,
    "bus": True, "truck": True, "motorcycle": True,
    "motor": True, "motorsiklo": True,
    "angkas": True, "grab": True, "move it": True,
    "habal-habal": True, "multicab": True,
    "PUV": True, "BRT": True,

    # Infrastructure
    "road": True, "highway": True, "street": True,
    "intersection": True, "lane": True,
    "pedestrian lane": True, "sidewalk": True,
    "traffic light": True, "stoplight": True,

    # Transport experience
    "commute": True, "commuter": True, "commuting": True,
    "pasahero": True, "fare": True, "plite": True,
    "driver": True, "conductor": True,
    "sakay": True, "byahe": True, "trapik": True,
}