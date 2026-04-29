"""
Cebuano Sentiment Lexicon v3.0 — Final
========================================
Domain: Traffic Enforcement Grievances in Cebu City
Research: "Geospatial Sentiment Analysis: A Hybrid NLP Approach for
Mapping Traffic Enforcement Grievances in Cebu City"

Construction methodology (thesis-documentable):
- v1.0: Original 40-word lexicon (baseline)
- v2.0: Expanded to 200+ terms, sarcasm system, fixed contradictions
- v3.0: Grounded in manual review of 736 Reddit posts across 2 sessions
  - Words added from ACTUAL validated posts (not guesswork)
  - False positives removed: "animal" (fired on Cebu Safari), "report"
  - New Cebuano terms from real corpus: maungot, gilahos, paasa,
    makapangyawa, jusko, pisteng yawa, gitulis, tulis
  - New sarcasm patterns from real posts: "EXCUSE ra", "balik balik",
    "paasa na pod", "another paasa", "supposed to decongest"
  - Infrastructure vocabulary from BRT post cluster
  - Sarcasm layer 5 added: structural irony patterns
"""

# ─────────────────────────────────────────────────────────────
# NEGATIVE SENTIMENT LEXICON
# Score: -0.1 (mild) to -1.0 (extreme)
# ─────────────────────────────────────────────────────────────
NEGATIVE_LEXICON = {

    # ── CEBUANO FRUSTRATION & EXASPERATION ──────────────────
    "puryagaba":        -0.9,
    "hangak":           -0.8,
    "luod":             -0.9,
    "libog":            -0.6,
    "nasubo":           -0.7,
    "nasukaon":         -0.9,
    "naratol":          -0.8,
    "nalagot":          -0.8,
    "makalagot":        -0.9,
    "makaguol":         -0.8,
    "makastress":       -0.8,
    "makabuang":        -0.9,
    "makaboang":        -0.9,
    "makapangyawa":     -0.9,  # makes you curse — from commute post
    "kapoy na":         -0.8,
    "kapoy kaayo":      -0.9,
    "kapoy":            -0.6,
    "gi kapoy":         -0.8,
    "gikapoy":          -0.8,
    "di na kaya":       -0.9,
    "dili na kaya":     -0.9,
    "di na":            -0.5,
    "grabe":            -0.8,
    "grabi":            -0.8,
    "grabe kaayo":      -0.9,
    "grabi kaayo":      -0.9,
    "grabeh":           -0.8,
    "grabe naman":      -0.9,  # "this is too much"
    "daotan":           -0.8,
    "dili maayo":       -0.7,
    "sayop":            -0.7,
    "supak":            -0.7,
    "hilak nalang":     -0.9,
    "naluha":           -0.8,
    "stress":           -0.7,
    "stressed":         -0.7,
    "frustrated":       -0.8,
    "frustrating":      -0.8,
    "samok":            -0.8,
    "hasol":            -0.8,
    "hasola":           -0.9,
    "alimuot":          -0.8,
    "walay klaro":      -0.8,
    "piskot":           -0.8,
    "ahak":             -0.8,
    "trapik kaayo":     -0.9,
    "maungot":          -0.8,  # suffocating — from "2am traffic" post
    "naungot":          -0.8,
    "yangungu":         -0.6,  # insistent repeated requests; mildly negative

    # ── INFRASTRUCTURE FAILURE (from BRT post cluster) ───────
    "gilahos":          -0.8,  # rushed/botched — "gilahos man gani ag BRT"
    "paasa":            -0.8,  # false hope/empty promise
    "excuse ra":        -0.8,  # "just an excuse" — from BRT subway post
    "overbudget":       -0.7,
    "over budget":      -0.7,
    "unfinished":       -0.7,
    "incomplete":       -0.6,
    "worn":             -0.6,  # from BRT stations "already look worn"
    "deteriorating":    -0.7,
    "counterproductive":-0.8,  # from BRT context
    "blacklisted":      -0.9,  # from BRT contractor post
    "anomalya":         -0.9,
    "delay":            -0.6,
    "delayed":          -0.6,
    "long overdue":     -0.7,
    "pothole":          -0.8,
    "butas ang dalan":  -0.8,
    "bato-bato":        -0.6,
    "grabe ang dalan":  -0.8,
    "road narrowing":   -0.7,  # from Osmeña Blvd narrowing post
    "performative":     -0.7,  # performative enforcement (LTFRB viral)
    "acting lang":      -0.8,

    # ── CEBUANO EXPLETIVES ───────────────────────────────────
    "yawa":             -0.8,
    "piste":            -0.9,
    "pisteng yawa":     -1.0,  # combined — strongest Cebuano expletive
    "bwisit":           -0.9,
    "yawaa":            -0.9,
    "giatay":           -0.9,
    "atay":             -0.7,
    "puta":             -0.9,
    "gago":             -0.9,
    "bobo":             -0.7,
    "buang":            -0.8,
    "walay pulos":      -0.9,
    "walay silbi":      -0.9,
    "jusko":            -0.7,  # exasperation — from commute posts
    # NOTE: "animal" REMOVED v2.0 — false positive on literal animals

    # ── TRAFFIC-SPECIFIC ─────────────────────────────────────
    "traffic":          -0.7,
    "trapik":           -0.7,
    "congestion":       -0.7,
    "gridlock":         -0.9,
    "standstill":       -0.8,
    "bumper to bumper": -0.8,
    "heavy traffic":    -0.8,
    "traffic jam":      -0.9,
    "stuck":            -0.7,
    "late":             -0.6,
    "dugay":            -0.6,
    "dugay kaayo":      -0.8,
    "nag abang":        -0.5,
    "wa na ko":         -0.8,

    # ── ENFORCEMENT ABUSE & CORRUPTION ──────────────────────
    "abuso":            -0.9,
    "nag-abuso":        -0.9,
    "corrupt":          -0.9,
    "corruption":       -0.9,
    "kotong":           -0.9,
    "hulidap":          -0.9,
    "extortion":        -0.9,
    "extort":           -0.9,
    "bribe":            -0.9,
    "lagay":            -0.9,
    "palakasan":        -0.8,
    "pabor":            -0.7,
    "under the table":  -0.9,
    "quota":            -0.8,
    "unjust":           -0.8,
    "injustice":        -0.8,
    "unfair":           -0.8,
    "biased":           -0.8,
    "walang silbi":     -0.9,
    "walang kwenta":    -0.9,
    "peke":             -0.8,
    "manggilaw":        -0.8,

    # ── DRIVER/TRANSPORT NEGATIVE ────────────────────────────
    "bastos":           -0.8,
    "walang galang":    -0.9,
    "walay respeto":    -0.9,
    "pasaway":          -0.8,
    "siga":             -0.7,
    "suplado":          -0.7,
    "harang":           -0.7,
    "counterflow":      -0.7,
    "reckless":         -0.8,
    "speeding":         -0.7,
    "overloading":      -0.7,
    "overcharging":     -0.8,
    "dagdag":           -0.7,
    "singit":           -0.7,
    "dagdag-singko":    -0.8,
    "fast timer":       -0.9,
    "tampered":         -0.9,
    "manloloko":        -0.9,
    "scammer":          -0.9,
    "tulis":            -0.9,  # robbery — from taxi robbery post
    "gitulis":          -0.9,  # was robbed (Cebuano past tense)

    # ── ENGLISH NEGATIVE ─────────────────────────────────────
    "terrible":         -0.8,
    "horrible":         -0.9,
    "awful":            -0.8,
    "bad":              -0.6,
    "worse":            -0.7,
    "worst":            -0.9,
    "hate":             -0.9,
    "sucks":            -0.8,
    "pathetic":         -0.9,
    "useless":          -0.9,
    "waste":            -0.7,
    "ridiculous":       -0.7,
    "absurd":           -0.8,
    "outrageous":       -0.8,
    "disgusting":       -0.9,
    "unacceptable":     -0.9,
    "dangerous":        -0.8,
    "unsafe":           -0.8,
    "incompetent":      -0.9,
    "negligent":        -0.8,
    "sad":              -0.6,
    "kinda sad":        -0.7,  # from motorcycle accidents post
    "norm":             -0.5,  # "become the norm" (negative normalization)

    # ── LEGACY v1 ────────────────────────────────────────────
    "hagit":            -0.8,
    "linang":           -0.9,
    "pabagal":          -0.7,
    "lisod":            -0.7,
    "malupit":          -0.9,
    "basura":           -0.8,
    "ayaw ko":          -0.6,
    "tuyot":            -0.7,
    "putok":            -0.9,
}


# ─────────────────────────────────────────────────────────────
# POSITIVE SENTIMENT LEXICON
# ─────────────────────────────────────────────────────────────
POSITIVE_LEXICON = {
    "maayo":            0.8,
    "maayos":           0.8,
    "ayos":             0.7,
    "tarong":           0.7,
    "husay":            0.8,
    "klaro":            0.7,
    "sakto":            0.7,
    "epektibo":         0.8,
    "padayon":          0.6,
    "puwede":           0.5,
    "okay lang":        0.6,
    "ayos ra":          0.6,
    "maayo man":        0.7,
    "dako nga tabang":  0.9,
    "naayo":            0.8,
    "nagamay":          0.7,
    "nagmaayo":         0.8,
    "salamat":          0.6,
    "gipasalamat":      0.7,
    "angay":            0.7,
    "tarong na":        0.7,
    "dali":             0.7,
    "dali ra":          0.7,
    "paspas":           0.6,
    "smooth":           0.8,
    "libre":            0.6,
    "serbisyo":         0.5,
    "fair":             0.8,
    "professional":     0.8,
    "accountable":      0.8,
    "accountability":   0.8,
    "helpful":          0.8,
    "courteous":        0.8,
    "matino":           0.8,
    "tapat":            0.8,
    "effective":        0.8,
    "strict":           0.6,
    "implemented":      0.6,
    "enforced":         0.6,
    "improvement":      0.8,
    "improved":         0.8,
    "better":           0.7,
    "best":             0.9,
    "efficient":        0.8,
    "solution":         0.7,
    "progress":         0.7,
    "upgrade":          0.7,
    "modernized":       0.8,
    "functional":       0.7,
    "operational":      0.7,
    "opened":           0.6,
    "completed":        0.7,
    "good":             0.7,
    "great":            0.8,
    "excellent":        0.9,
    "awesome":          0.8,
    "nice":             0.6,
    "fast":             0.7,
    "quick":            0.7,
    "easy":             0.7,
    "clear":            0.6,
    "safe":             0.8,
    "safer":            0.8,
    "respect":          0.7,
}


# ─────────────────────────────────────────────────────────────
# SARCASM DETECTION — 5-Layer System
# ─────────────────────────────────────────────────────────────
SARCASM_MARKERS = {
    # Layer 1: Primary Cebuano/Filipino markers
    "hayahay":               True,
    "hayahay kaayo":         True,
    "hayahay man":           True,
    "hahayz":                True,
    "kanus-a pa kaha":       True,
    "kanus-a pa":            True,
    "padayon cebu":          True,
    "proud cebuano":         True,
    "mao nay Cebu":          True,
    "mao ni":                True,
    "puryagaba":             True,
    "sana all":              True,
    "nakaka-proud":          True,
    "galing":                True,
    "ang galing":            True,
    "swabe":                 True,
    "hay nako":              True,

    # Layer 2: Ironic praise
    "so comfortable":        True,
    "so smooth":             True,
    "so efficient":          True,
    "very efficient":        True,
    "so professional":       True,
    "great job":             True,
    "well done":             True,
    "congratulations":       True,
    "thank you CITOM":       True,
    "thank you LTO":         True,
    "thank you traffic":     True,
    "salamat CITOM":         True,
    "salamat LTO":           True,
    "naayo ang Cebu":        True,
    "solving na":            True,

    # Layer 3: Resigned sarcasm
    "😂😭":                  True,
    "hahaha ang traffic":    True,
    "lol traffic":           True,
    "char":                  True,
    "charot":                True,

    # Layer 4: Structural irony
    "supposed to decongest": True,
    "supposed to help":      True,
    "supposed to improve":   True,
    "counterproductive":     True,
    "ironic":                True,
    "ironically":            True,
    "funny how":             True,
    "isn't it funny":        True,
    "dba funny":             True,

    # Layer 5: BRT-specific resignation patterns (from real posts)
    "EXCUSE ra":             True,  # "EXCUSE ra'y nakadaghan"
    "excuse lang":           True,
    "paasa na pod":          True,  # "another false hope"
    "another paasa":         True,
    "balik balik":           True,  # "same promises over and over"
    "bla bla bla":           True,  # dismissive of empty promises
}

CONTEXT_DEPENDENT_SARCASM = {
    "wow":    ["traffic", "enforcer", "CITOM", "LTO", "jeepney",
               "trapik", "checkpoint", "commute"],
    "nice":   ["traffic", "dalan", "karsada", "enforcer"],
    "perfect":["traffic", "trapik", "commute", "CITOM"],
    "amazing":["traffic", "commute", "enforcer"],
    "love it":["traffic", "commute", "jeepney"],
    "enjoy":  ["traffic", "commute", "trapik"],
    "unta":   ["maayo", "tarong", "ayos"],
    "di ba":  ["traffic", "commute", "enforcer", "BRT"],
    "dba":    ["traffic", "commute", "enforcer", "BRT"],
}


# ─────────────────────────────────────────────────────────────
# INTENSIFIERS & NEGATIONS
# ─────────────────────────────────────────────────────────────
INTENSIFIERS = {
    "kaayo":        1.5,
    "gyud":         1.3,
    "jud":          1.3,
    "gyud kaayo":   1.7,
    "sobra":        1.4,
    "sobra kaayo":  1.6,
    "grabe":        1.4,
    "grabi":        1.4,
    "super":        1.4,
    "super kaayo":  1.6,
    "talaga":       1.3,
    "napaka":       1.5,
    "naman":        1.2,
    "very":         1.3,
    "really":       1.3,
    "so":           1.2,
    "extremely":    1.5,
    "absolutely":   1.5,
    "completely":   1.4,
    "totally":      1.3,
}

NEGATIONS = {
    "hindi":     True,
    "dili":      True,
    "di":        True,
    "wala":      True,
    "walay":     True,
    "not":       True,
    "no":        True,
    "never":     True,
    "without":   True,
    "dili man":  True,
    "wala man":  True,
    "dili gyud": True,
}


# ─────────────────────────────────────────────────────────────
# CEBU CITY LOCATIONS
# ─────────────────────────────────────────────────────────────
CEBU_LOCATIONS = {
    "srp":                    "SRP (South Road Properties)",
    "south road properties":  "SRP (South Road Properties)",
    "south road":             "SRP (South Road Properties)",
    "mambaling":              "Mambaling",
    "talamban":               "Talamban",
    "lahug":                  "Lahug",
    "it park":                "IT Park",
    "itpark":                 "IT Park",
    "i.t. park":              "IT Park",
    "fuente osmeña":          "Fuente Osmeña",
    "fuente osmena":          "Fuente Osmeña",
    "fuente circle":          "Fuente Osmeña",
    "fuente":                 "Fuente Osmeña",
    "mandaue":                "Mandaue City",
    "mandawe":                "Mandaue City",
    "mactan":                 "Mactan",
    "consolacion":            "Consolacion",
    "talisay":                "Talisay City",
    "liloan":                 "Liloan",
    "minglanilla":            "Minglanilla",
    "bulacao":                "Bulacao",
    "banawa":                 "Banawa",
    "guadalupe":              "Guadalupe",
    "basak":                  "Basak",
    "mabolo":                 "Mabolo",
    "apas":                   "Apas",
    "busay":                  "Busay",
    "pungol":                 "Pungol",
    "labangon":               "Labangon",
    "tisa":                   "Tisa",
    "carreta":                "Carreta",
    "cogon":                  "Cogon",
    "pardo":                  "Pardo",
    "capitol site":           "Capitol Site",
    "capitol":                "Capitol Site",
    "salinas drive":          "Salinas Drive",
    "salinas":                "Salinas Drive",
    "bacalso":                "N. Bacalso Avenue",
    "n. bacalso":             "N. Bacalso Avenue",
    "national bacalso":       "N. Bacalso Avenue",
    "transcentral highway":   "Transcentral Highway",
    "transcentral":           "Transcentral Highway",
    "urgello":                "Urgello",
    "subangdaku":             "Subangdaku",
    "hernan cortes":          "Hernan Cortes Street",
    "a.s. fortuna":           "A.S. Fortuna Street",
    "as fortuna":             "A.S. Fortuna Street",
    "fortuna":                "A.S. Fortuna Street",
    "escario":                "Escario Street",
    "gorordo":                "Gorordo Avenue",
    "archbishop reyes":       "Archbishop Reyes Avenue",
    "reyes ave":              "Archbishop Reyes Avenue",
    "jones ave":              "Jones Avenue",
    "jones avenue":           "Jones Avenue",
    "juan luna":              "Juan Luna Street",
    "magallanes":             "Magallanes Street",
    "osmena blvd":            "Osmeña Boulevard",
    "osmena boulevard":       "Osmeña Boulevard",
    "osmeña blvd":            "Osmeña Boulevard",
    "osmeña boulevard":       "Osmeña Boulevard",
    "mango avenue":           "Mango Avenue",
    "mango ave":              "Mango Avenue",
    "north road":             "North Road",
    "bypass":                 "Cebu City Bypass",
    "ayala center":           "Ayala (Business District)",
    "ayala cebu":             "Ayala (Business District)",
    "ayala mall":             "Ayala Mall",
    "ayala":                  "Ayala (Business District)",
    "robinsons place":        "Robinsons Place",
    "robinsons":              "Robinsons Place",
    "sm city cebu":           "SM City Cebu",
    "sm cebu":                "SM City Cebu",
    "sm seaside":             "SM Seaside",
    "seaside":                "SM Seaside",
    "carbon market":          "Carbon Market",
    "carbon":                 "Carbon Market",
    "colon street":           "Colon Street",
    "metro colon":            "Colon Street",
    "colon":                  "Colon Street",
    "gaisano":                "Gaisano",
    "pier area":              "Pier Area",
    "pier":                   "Pier Area",
    "cebu city":              "Cebu City",
}


# ─────────────────────────────────────────────────────────────
# TRAFFIC & ENFORCEMENT DOMAIN TERMS
# ─────────────────────────────────────────────────────────────
TRAFFIC_TERMS = {
    "CITOM": True, "CCTO": True, "LTFRB": True, "LTO": True,
    "traffic enforcer": True, "traffic officer": True,
    "traffic police": True, "pulis": True, "polis": True,
    "apprehended": True, "apprehend": True,
    "giapprehend": True, "naapprehend": True,
    "checkpoint": True, "checkpoints": True,
    "violation": True, "violators": True,
    "ticket": True, "fine": True,
    "arrested": True, "towed": True, "towing": True,
    "colorum": True, "kotong": True,
    "counterflow": True, "reckless driving": True,
    "illegal parking": True, "smoke belching": True,
    "overloading": True, "speeding": True,
    "jeepney": True, "jeep": True, "taxi": True,
    "bus": True, "truck": True, "motorcycle": True,
    "motor": True, "motorsiklo": True,
    "angkas": True, "grab": True, "move it": True,
    "habal-habal": True, "multicab": True,
    "PUV": True, "BRT": True,
    "road": True, "highway": True, "street": True,
    "intersection": True, "lane": True,
    "pedestrian lane": True, "sidewalk": True,
    "traffic light": True, "stoplight": True,
    "accident": True, "disgrasya": True, "bangga": True,
    "commute": True, "commuter": True, "commuting": True,
    "pasahero": True, "fare": True, "plite": True,
    "driver": True, "conductor": True,
    "sakay": True, "byahe": True, "trapik": True,
    "traffic": True,
}