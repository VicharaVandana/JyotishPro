import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: KujaDosha
# Purpose: Calculates the presence of KujaDosha in the provided horoscope.
# Description: Evaluates KujaDosha
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def KujaDosha(charts):
    IsKujaDoshaPresent = False
    
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = ["Ma"]
    cancellation_reason = ""
    
    mars_house = charts["D1"]["planets"]["Mars"]["house-num"]
    mars_sign = charts["D1"]["planets"]["Mars"]["sign"]
    
    if mars_house in [1, 4, 7, 8, 12]:
        IsKujaDoshaPresent = True
        
        # Check Cancellations (Bhanga)
        cancelled = False
        reasons = []
        
        # Mars in own sign or exalted
        if mars_sign in ["Aries", "Scorpio"]:
            cancelled = True
            reasons.append(f"Mars is in its own sign ({mars_sign})")
        elif mars_sign == "Capricorn":
            cancelled = True
            reasons.append("Mars is exalted in Capricorn")
            
        # Aspect or conjunction with Jupiter
        mars_aspected_by = charts["D1"]["planets"]["Mars"].get("Aspected-by", [])
        mars_conjunct = charts["D1"]["planets"]["Mars"].get("conjuncts", [])
        
        if "Jupiter" in mars_aspected_by:
            cancelled = True
            reasons.append("Mars is aspected by Jupiter")
            relevant_planets.append("Ju")
        if "Jupiter" in mars_conjunct:
            cancelled = True
            reasons.append("Mars is conjunct with Jupiter")
            if "Ju" not in relevant_planets:
                relevant_planets.append("Ju")
                
        # Mars in 8th house in specific signs
        if mars_house == 8 and mars_sign in ["Sagittarius", "Pisces"]:
            cancelled = True
            reasons.append(f"Mars is in the 8th house in Jupiter's sign ({mars_sign})")
            
        # Mars in 12th house in Venus signs
        if mars_house == 12 and mars_sign in ["Taurus", "Libra"]:
            cancelled = True
            reasons.append(f"Mars is in the 12th house in Venus's sign ({mars_sign})")
            
        key = "KUJA_DOSHA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = "Kuja Dosha (Manglik)"
        common.yogadoshas_dict[key]["type"] = "Dosha"
        common.yogadoshas_dict[key]["Rule"] = f"Mars is situated in the {mars_house}th house from the Lagna."
        common.yogadoshas_dict[key]["Result"] = "Kuja Dosha can cause friction, delays, or difficulties in marital life. It often brings an aggressive or dominating energy into relationships."
        common.yogadoshas_dict[key]["Note"] = "This is calculated from the Lagna only. Classical astrology also considers from Moon and Venus, but this application strictly applies the Lagna rule."
        common.yogadoshas_dict[key]["Source"] = "Phaladeepika & Brihat Parashara Hora Shastra"
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets
        
        if cancelled:
            common.yogadoshas_dict[key]["exist"] = False
            common.yogadoshas_dict[key]["CancellationReason"] = "Kuja Dosha is cancelled because " + " and ".join(reasons) + "."
        else:
            common.yogadoshas_dict[key]["exist"] = True
            common.yogadoshas_dict[key]["Remedies"] = "Worship Lord Hanuman, recite the Hanuman Chalisa daily. Donating red items or sweet bread (Roti) to dogs on Tuesdays is beneficial."
            
    return IsKujaDoshaPresent
