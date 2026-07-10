import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: KemadrumaYoga
# Purpose: Calculates the presence of KemadrumaYoga in the provided horoscope.
# Description: Evaluates KemadrumaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def KemadrumaYoga(charts):
    IsKemadrumaYogaPresent = False
    
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = ["Mo"]
    cancellation_reason = ""
    
    moon_house = charts["D1"]["planets"]["Moon"]["house-num"]
    
    planets_in_2nd = []
    planets_in_12th = []
    planets_with_moon = []
    planets_in_kendra_from_moon = []
    planets_in_kendra_from_lagna = []
    
    valid_planets = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    for p in valid_planets:
        p_house = charts["D1"]["planets"][p]["house-num"]
        diff_from_moon = gen.housediff(moon_house, p_house)
        diff_from_lagna = p_house  # Lagna is always house 1
        
        if diff_from_moon == 2:
            planets_in_2nd.append(p)
        elif diff_from_moon == 12:
            planets_in_12th.append(p)
        elif diff_from_moon == 1:
            planets_with_moon.append(p)
            
        if diff_from_moon in [1, 4, 7, 10]:
            planets_in_kendra_from_moon.append(p)
            
        if diff_from_lagna in [1, 4, 7, 10]:
            planets_in_kendra_from_lagna.append(p)
            
    # Kemadruma condition: No planets in 2nd and 12th from Moon
    if len(planets_in_2nd) == 0 and len(planets_in_12th) == 0:
        IsKemadrumaYogaPresent = True
        
        # Check Cancellations (Bhanga)
        cancelled = False
        reasons = []
        
        if len(planets_with_moon) > 0:
            cancelled = True
            reasons.append(f"Moon is conjunct with {', '.join(planets_with_moon)}")
            relevant_planets.extend([p[0:2] for p in planets_with_moon])
            
        elif len(planets_in_kendra_from_moon) > 0:
            cancelled = True
            reasons.append(f"Planets ({', '.join(planets_in_kendra_from_moon)}) are in Kendras from Moon")
            relevant_planets.extend([p[0:2] for p in planets_in_kendra_from_moon])
            
        elif len(planets_in_kendra_from_lagna) > 0:
            cancelled = True
            reasons.append(f"Planets ({', '.join(planets_in_kendra_from_lagna)}) are in Kendras from Lagna")
            relevant_planets.extend([p[0:2] for p in planets_in_kendra_from_lagna])
            
        if "Jupiter" in charts["D1"]["planets"]["Moon"]["Aspected-by"]:
            cancelled = True
            reasons.append("Moon is aspected by Jupiter")
            if "Ju" not in relevant_planets:
                relevant_planets.append("Ju")

        key = "KEMADRUMA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = "Kemadruma Yoga (D1)"
        common.yogadoshas_dict[key]["type"] = "Dosha"  # Often considered a dosha due to negative effects
        common.yogadoshas_dict[key]["Rule"] = "There are no planets (excluding Sun, Rahu, Ketu) in the 2nd and 12th houses from the Moon."
        common.yogadoshas_dict[key]["Result"] = "Kemadruma Yoga brings a life of struggle, poverty, sorrow, and a feeling of loneliness or lack of support, even if born in a royal family."
        common.yogadoshas_dict[key]["Note"] = "This yoga is heavily dependent on cancellation rules. If cancelled, it forms Kemadruma Bhanga Yoga, which actually gives good results."
        common.yogadoshas_dict[key]["Source"] = "Brihat Jataka"
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets
        
        if cancelled:
            common.yogadoshas_dict[key]["exist"] = False
            common.yogadoshas_dict[key]["CancellationReason"] = "Kemadruma is cancelled because " + " and ".join(reasons) + ". This forms Kemadruma Bhanga Yoga."
        else:
            common.yogadoshas_dict[key]["exist"] = True
            common.yogadoshas_dict[key]["Remedies"] = "Worship Lord Shiva, offer water to Shivling daily, and respect your mother. Fasting on Mondays is highly beneficial."
            
    return IsKemadrumaYogaPresent
