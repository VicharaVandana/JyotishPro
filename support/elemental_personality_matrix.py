import os
import matplotlib.pyplot as plt

# Weights
WEIGHT_LAGNA = 10
WEIGHT_LAGNESHA = 10
WEIGHT_MOON = 8
WEIGHT_SUN = 8
WEIGHT_MARS_MERC_VENUS = 5
WEIGHT_JUP_SATURN = 3

# Multipliers
AVASTHA_MULT_YUVA = 1.0
AVASTHA_MULT_KUMARA_VRIDDHA = 0.5
AVASTHA_MULT_BALA_MRIT = 0.2

DIGNITY_MULT_EXALTED_OWN = 1.2
DIGNITY_MULT_FRIENDLY = 1.0
DIGNITY_MULT_NEUTRAL = 0.8
DIGNITY_MULT_ENEMY_DEB = 0.5

# Element Mapping
SIGNS_AGNI = ["Aries", "Leo", "Sagittarius"]
SIGNS_PRUTHVI = ["Taurus", "Virgo", "Capricorn"]
SIGNS_VAAYU = ["Gemini", "Libra", "Aquarius"]
SIGNS_JALA = ["Cancer", "Scorpio", "Pisces"]

SIGN_LORDS = {
    "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
    "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
    "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
}

ELEMENT_COLORS = {
    "Agni": "#FFA500",  # Orange
    "Pruthvi": "#008000",  # Green
    "Vaayu": "#808080",  # Grey
    "Jala": "#0000FF"  # Blue
}

def normalize_sign(sign_name):
    if not sign_name:
        return "Unknown"
    s = sign_name.capitalize().strip()
    mapping = {
        "Mesha": "Aries", 
        "Vrishabha": "Taurus", "Vrushaba": "Taurus", "Vrushabha": "Taurus",
        "Mithuna": "Gemini", 
        "Karka": "Cancer", "Karkata": "Cancer", "Kataka": "Cancer",
        "Simha": "Leo", 
        "Kanya": "Virgo", 
        "Tula": "Libra", 
        "Vrishchika": "Scorpio", "Vrushchika": "Scorpio", "Vrischika": "Scorpio", "Vruschika": "Scorpio",
        "Dhanu": "Sagittarius", "Dhanush": "Sagittarius", "Dhanus": "Sagittarius", 
        "Makara": "Capricorn",
        "Kumbha": "Aquarius", 
        "Meena": "Pisces", "Meenam": "Pisces"
    }
    return mapping.get(s, s)

def get_element(sign):
    if sign in SIGNS_AGNI: return "Agni"
    if sign in SIGNS_PRUTHVI: return "Pruthvi"
    if sign in SIGNS_VAAYU: return "Vaayu"
    if sign in SIGNS_JALA: return "Jala"
    raise ValueError(f"Unknown sign provided to get_element: {repr(sign)}")

def get_avastha_multiplier(sign_name, degree):
    # Odd signs: Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
    odd_signs = ["Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"]
    is_odd = sign_name in odd_signs
    
    if 0 <= degree < 6:
        state = "Bala" if is_odd else "Mrit"
    elif 6 <= degree < 12:
        state = "Kumara" if is_odd else "Vriddha"
    elif 12 <= degree < 18:
        state = "Yuva"
    elif 18 <= degree < 24:
        state = "Vriddha" if is_odd else "Kumara"
    else:
        state = "Mrit" if is_odd else "Bala"
        
    if state == "Yuva":
        return 1.0, state
    elif state in ["Kumara", "Vriddha"]:
        return 0.5, state
    else:
        return 0.2, state

def get_dignity_multiplier(house_rel):
    if not house_rel: return 1.0 # Default
    rel = house_rel.lower()
    if "exhalted" in rel or "exalted" in rel or "own" in rel or "mooltrikona" in rel:
        return DIGNITY_MULT_EXALTED_OWN
    elif "friendly" in rel:
        return DIGNITY_MULT_FRIENDLY
    elif "enemy" in rel or "debilitated" in rel:
        return DIGNITY_MULT_ENEMY_DEB
    else:
        # Neutral or anything else
        return DIGNITY_MULT_NEUTRAL

def calculate_elemental_matrix(charts):
    d1 = charts.get("D1", {})
    if not d1:
        return None
        
    planets = d1.get("planets", {})
    
    raw_data = {"Agni": 0, "Pruthvi": 0, "Vaayu": 0, "Jala": 0}
    weighted_data = {"Agni": 0.0, "Pruthvi": 0.0, "Vaayu": 0.0, "Jala": 0.0}
    detailed_table = []
    
    # Lagna Base Weight
    ascendant = d1.get("ascendant", {})
    lagna_sign = normalize_sign(ascendant.get("rashi"))
    lagna_deg = ascendant.get("pos", {}).get("deg", 0) % 30 # Just in case it's absolute
    lagna_element = get_element(lagna_sign)
    lagna_avastha_mult, lagna_avastha_state = get_avastha_multiplier(lagna_sign, lagna_deg)
    lagna_weight = WEIGHT_LAGNA * lagna_avastha_mult * 1.0 # Dignity is 1.0 for Lagna
    
    raw_data[lagna_element] += 1
    weighted_data[lagna_element] += lagna_weight
    detailed_table.append({
        "Planet": "Lagna",
        "Sign": lagna_sign,
        "Element": lagna_element,
        "Avastha": lagna_avastha_state,
        "Final_Weight": round(lagna_weight, 2)
    })
    
    import support.generic as gen
    lagnesha = gen.get_nthLord(d1, 1)
    
    for p_name, p_data in planets.items():
        if p_name in ["Uranus", "Neptune", "Pluto"]:
            continue
            
        sign = normalize_sign(p_data.get("rashi"))
        element = get_element(sign)
        
        # Base weight
        if p_name == lagnesha:
            base_w = WEIGHT_LAGNESHA
        elif p_name == "Moon":
            base_w = WEIGHT_MOON
        elif p_name == "Sun":
            base_w = WEIGHT_SUN
        elif p_name in ["Mars", "Mercury", "Venus"]:
            base_w = WEIGHT_MARS_MERC_VENUS
        elif p_name in ["Jupiter", "Saturn"]:
            base_w = WEIGHT_JUP_SATURN
        elif p_name in ["Rahu", "Ketu"]:
            dispositor = SIGN_LORDS.get(sign)
            if dispositor == "Moon":
                base_w = WEIGHT_MOON
            elif dispositor == "Sun":
                base_w = WEIGHT_SUN
            elif dispositor in ["Mars", "Mercury", "Venus"]:
                base_w = WEIGHT_MARS_MERC_VENUS
            elif dispositor in ["Jupiter", "Saturn"]:
                base_w = WEIGHT_JUP_SATURN
            else:
                base_w = 0
        else:
            base_w = 0
            
        deg = p_data.get("pos", {}).get("deg", 0)
        avastha_mult, avastha_state = get_avastha_multiplier(sign, deg)
        dig_mult = get_dignity_multiplier(p_data.get("house-rel", ""))
        
        final_w = base_w * avastha_mult * dig_mult
        
        raw_data[element] += 1
        weighted_data[element] += final_w
        
        detailed_table.append({
            "Planet": p_name + (" (Lagnesha)" if p_name == lagnesha else ""),
            "Sign": sign,
            "Element": element,
            "Avastha": avastha_state,
            "Final_Weight": round(final_w, 2)
        })
        
    # Convert weighted data to percentage
    total_w = sum(weighted_data.values())
    if total_w > 0:
        for k in weighted_data:
            weighted_data[k] = round((weighted_data[k] / total_w) * 100, 2)
            
    # Find dominant element
    dominant = max(weighted_data, key=weighted_data.get)
    summary = ""
    if dominant == "Agni":
        summary = "Agni dominates this chart, bringing immense kinetic energy and vision. You are likely a self-starter who thrives on initiative and taking bold action. Your personality is geared towards leading, inspiring, and dynamically overcoming obstacles."
    elif dominant == "Pruthvi":
        summary = "Pruthvi dominates this chart, grounding you in architectural logic, systems, and pragmatic results. You excel at building sustainable structures and executing step-by-step plans. Stability, reliability, and material mastery are core to your personality."
    elif dominant == "Vaayu":
        summary = "Vaayu dominates this chart, highlighting your abilities in data synthesis, communication, and pattern recognition. You navigate the world through ideas, social networks, and intellectual agility. Adaptability and rapid information processing are your key strengths."
    elif dominant == "Jala":
        summary = "Jala dominates this chart, centering your focus on intuition, emotional intelligence, and environmental nurturing. You possess deep empathy and can connect with the subtle emotional undercurrents of any situation. Healing, adapting, and intuitive flow guide your actions."

    result = {
        "DetailedTable": detailed_table,
        "RawData": raw_data,
        "WeightedData": weighted_data,
        "Summary": summary
    }
    return result

def generate_elemental_charts(raw_data, weighted_data, output_path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    labels = list(raw_data.keys())
    raw_vals = [raw_data[k] for k in labels]
    weight_vals = [weighted_data[k] for k in labels]
    colors = [ELEMENT_COLORS[k] for k in labels]
    
    # Filter out zeros for pie chart
    raw_labels = [l for i, l in enumerate(labels) if raw_vals[i] > 0]
    raw_sizes = [v for v in raw_vals if v > 0]
    raw_colors = [c for i, c in enumerate(colors) if raw_vals[i] > 0]
    
    weight_labels = [l for i, l in enumerate(labels) if weight_vals[i] > 0]
    weight_sizes = [v for v in weight_vals if v > 0]
    weight_colors = [c for i, c in enumerate(colors) if weight_vals[i] > 0]
    
    ax1.pie(raw_sizes, labels=raw_labels, colors=raw_colors, autopct=lambda p: '{:.0f}'.format(p * sum(raw_sizes) / 100.0), startangle=90)
    ax1.set_title("Raw Distribution (Count)")
    
    ax2.pie(weight_sizes, labels=weight_labels, colors=weight_colors, autopct='%1.1f%%', startangle=90)
    ax2.set_title("Weighted Distribution (Personality Profile)")
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, format='png')
    plt.close()
