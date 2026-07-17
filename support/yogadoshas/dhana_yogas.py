# Placeholder for future Dhana Yogas
import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: VasumathiYoga
# Purpose: Calculates the presence of Vasumathi Yoga in the provided horoscope.
# Description: Checks if benefics occupy Upachayas (3, 6, 10, 11) from Lagna or Moon.
# Expected Impact: Updates the yogadoshas_dict with results.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def VasumathiYoga(charts):
    IsVasumathiPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = set()
    forming_divs = []
    
    benefics = charts["D1"]["classifications"]["natural-benefics"]
    moon_sign = charts["D1"]["planets"]["Moon"]["sign"]
    
    upachayas = [3, 6, 10, 11]
    
    lagna_upachaya_benefics = []
    moon_upachaya_benefics = []
    
    for p in benefics:
        # Check from Lagna
        if charts["D1"]["planets"][p]["house-num"] in upachayas:
            lagna_upachaya_benefics.append(p)
            
        # Check from Moon
        planet_sign = charts["D1"]["planets"][p]["sign"]
        house_from_moon = gen.get_house_number(moon_sign, planet_sign)
        if house_from_moon in upachayas:
            moon_upachaya_benefics.append(p)
            
    # Typically at least two benefics are needed for a notable dhana yoga effect
    if len(lagna_upachaya_benefics) >= 2:
        IsVasumathiPresent = True
        forming_divs.append("Lagna")
        relevant_planets.update(lagna_upachaya_benefics)
        
    if len(moon_upachaya_benefics) >= 2:
        IsVasumathiPresent = True
        if "Moon" not in forming_divs:
            forming_divs.append("Moon")
        relevant_planets.update(moon_upachaya_benefics)
        relevant_planets.add("Moon")
        
    if IsVasumathiPresent:
        Rule = f'''Benefic planets occupy the Upachaya houses (3rd, 6th, 10th, or 11th) from the {", ".join(forming_divs)}.'''
        Results = f'''According to B.V. Raman and Phaladeepika, the person will not be a dependent but will always command plenty of wealth and live prosperously. It is a powerful Dhana Yoga.'''
        
        malefics = charts["D1"]["classifications"]["natural-malefics"]
        lagna_upachaya_malefics = []
        moon_upachaya_malefics = []
        
        for m in malefics:
            if charts["D1"]["planets"][m]["house-num"] in upachayas:
                lagna_upachaya_malefics.append(m)
            m_sign = charts["D1"]["planets"][m]["sign"]
            if gen.get_house_number(moon_sign, m_sign) in upachayas:
                moon_upachaya_malefics.append(m)
                
        dynamic_note = "Chart-Specific Analysis:\\n"
        if lagna_upachaya_benefics:
            dynamic_note += f"- Benefics in Upachayas from Lagna: {', '.join(lagna_upachaya_benefics)}\\n"
        if moon_upachaya_benefics:
            dynamic_note += f"- Benefics in Upachayas from Moon: {', '.join(moon_upachaya_benefics)}\\n"
            
        bhanga = False
        if lagna_upachaya_malefics or moon_upachaya_malefics:
            bhanga = True
            dynamic_note += f"- Malefics in Upachayas (Bhanga Check): Lagna ({', '.join(lagna_upachaya_malefics)}), Moon ({', '.join(moon_upachaya_malefics)})\\n"
            
        total_unique = len(set(lagna_upachaya_benefics + moon_upachaya_benefics))
        
        if bhanga:
            dynamic_note += "- Conclusion: The presence of malefics in the Upachayas causes partial Bhanga (cancellation). The wealth will still come, but with significant obstacles, fluctuations, or unethical temptations."
        else:
            if total_unique >= 3:
                dynamic_note += "- Conclusion: A highly powerful formation with multiple benefics and NO malefic interference, contributing to immense, uninterrupted wealth accumulation."
            elif "Lagna" in forming_divs:
                dynamic_note += "- Conclusion: A strong formation from the Ascendant ensuring steady, independent, and unobstructed growth of wealth."
            else:
                dynamic_note += "- Conclusion: Formed from the Moon, ensuring good mental disposition towards wealth creation and consistent prosperity."

        Note = dynamic_note
        
        key = f"VASUMATHI_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Vasumathi Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\\n ", "\\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\\n ", "\\n").replace("\\n","\\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\\n ", "\\n")
        common.yogadoshas_dict[key]["Source"] = "B.V. Raman / Phaladeepika"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        
    return IsVasumathiPresent
