import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: ParvataYoga
# Purpose: Calculates the presence of ParvataYoga in the provided horoscope.
# Description: Evaluates Parvata Yoga based on classical definitions (Phaladeepika & BV Raman).
#              Definition: Benefic planets in Kendras (1, 4, 7, 10), and the 6th and 8th 
#              houses are either vacant or occupied by benefic planets only.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean: True if the yoga is present, False otherwise.
# ==========================================================================================
def ParvataYoga(charts):
    IsParvataYogaPresent = False
    
    Name = "Parvata"
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = []

    benefics = charts["D1"]["classifications"]["natural-benefics"].copy()
    malefics = charts["D1"]["classifications"]["natural-malefics"].copy()
    malefics.extend(["Rahu", "Ketu"])
    
    planets_in_kendras = []
    benefics_in_kendras = []
    
    for house in [1, 4, 7, 10]:
        planets_in_house = gen.get_planets_in_house(house, charts["D1"]["planets"])
        planets_in_kendras.extend(planets_in_house)
        
    planets_in_6th = gen.get_planets_in_house(6, charts["D1"]["planets"])
    planets_in_8th = gen.get_planets_in_house(8, charts["D1"]["planets"])
    
    all_target_planets = planets_in_kendras + planets_in_6th + planets_in_8th
    malefics_in_targets = gen.list_intersection(malefics, all_target_planets)
    
    if len(all_target_planets) > 0 and len(malefics_in_targets) == 0:
        IsParvataYogaPresent = True
        
        Rule = f"The Kendras (1,4,7,10) and the 6th and 8th houses contain only benefic planets: {all_target_planets} and are devoid of any malefic planets."
            
        Results = '''According to Phaladeepika and BV Raman, the native with Parvata Yoga will have lasting wealth and prosperity. They will be charitable, highly learned, very passionate, and will be a leader or head of a town, city, or organization. They will lead a life of comfort, possess enduring fame, and command immense respect.'''
        Note = "This yoga represents the strength of a 'Mountain' (Parvata), granting stability, unshakeable status, and monumental heights to the native's life."
        
        for p in all_target_planets:
            if p[0:2] not in relevant_planets:
                relevant_planets.append(p[0:2])
                
        key = "PARVATA_YOGA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"{Name} Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Phaladeepika & BV Raman Three Hundred Important Combinations"   
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets

    return IsParvataYogaPresent
