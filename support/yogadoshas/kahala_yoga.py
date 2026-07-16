import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: KahalaYoga
# Purpose: Calculates the presence of Kahala Yoga in the provided horoscope.
# Description: Evaluates Kahala Yoga based on classical definitions (Phaladeepika & BV Raman).
#              Definition: The lords of the 4th and 9th houses should be in mutual Kendras, 
#              and the lord of the Lagna should be strongly disposed.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean: True if the yoga is present, False otherwise.
# ==========================================================================================
def KahalaYoga(charts):
    IsKahalaYogaPresent = False
    
    Name = "Kahala"
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = []

    # Get the lords of 1st (Lagna), 4th, and 9th houses
    lagna_lord = gen.get_nthLord(charts["D1"], 1)
    fourth_lord = gen.get_nthLord(charts["D1"], 4)
    ninth_lord = gen.get_nthLord(charts["D1"], 9)

    # Get the houses where these lords are placed
    if fourth_lord not in charts["D1"]["planets"] or ninth_lord not in charts["D1"]["planets"] or lagna_lord not in charts["D1"]["planets"]:
        return False

    fourth_lord_house = charts["D1"]["planets"][fourth_lord]["house-num"]
    ninth_lord_house = charts["D1"]["planets"][ninth_lord]["house-num"]
    lagna_lord_house = charts["D1"]["planets"][lagna_lord]["house-num"]

    # Check if 4th and 9th lords are in mutual Kendras.
    # Mutual kendras mean their house numbers have a difference that is a multiple of 3 (0, 3, 6, 9)
    # The user correctly noted we must exclude cases where the 4th and 9th lord is the exact same planet 
    # (e.g. Leo and Aquarius Lagnas) because a planet cannot be in mutual kendras with itself to form a combination.
    is_mutual_kendra = (abs(fourth_lord_house - ninth_lord_house) % 3 == 0) and (fourth_lord != ninth_lord)

    # Check if Lagna Lord is strong (Not in 6, 8, 12 and not debilitated)
    # This is a simplified check for "strongly disposed"
    is_lagna_lord_strong = False
    if lagna_lord_house not in [6, 8, 12]:
        lagna_lord_data = charts["D1"]["planets"][lagna_lord]
        is_lagna_lord_strong = True
        
        # Check if debilitated (rough approximation without neechabhanga)
        # Using dignity string if available
        dignity = lagna_lord_data.get("house-rel", "").lower()
        if "debilitated" in dignity or "neecha" in dignity:
            is_lagna_lord_strong = False
            
    if is_mutual_kendra and is_lagna_lord_strong:
        IsKahalaYogaPresent = True
        
        Rule = f"The Lord of the 4th house ({fourth_lord}) and the Lord of the 9th house ({ninth_lord}) are placed in mutual Kendras. Additionally, the Lagna Lord ({lagna_lord}) is strongly placed."
            
        Results = '''According to Phaladeepika and BV Raman, the native with Kahala Yoga will be aggressive, courageous, and highly energetic. They will command a large organization, army, or community. Though they can be somewhat stubborn or harsh in their approach, they are immensely successful, bold, and dynamic leaders who carve their own path to success.'''
        Note = "Kahala translates to a 'large drum' or a military trumpet. It signifies fame that is loud, announcing the arrival of a commander. It is an assertive Raja Yoga rather than a gentle one."
        
        for p in [lagna_lord, fourth_lord, ninth_lord]:
            if p[0:2] not in relevant_planets:
                relevant_planets.append(p[0:2])
                
        key = "KAHALA_YOGA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"{Name} Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Phaladeepika & BV Raman Three Hundred Important Combinations"   
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets

    return IsKahalaYogaPresent
