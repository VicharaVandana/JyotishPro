import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: DharmaKarmadhipatiYoga
# Purpose: Calculates the presence of DharmaKarmadhipatiYoga in the provided horoscope.
# Description: Evaluates DharmaKarmadhipatiYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def DharmaKarmadhipatiYoga(charts):
    IsDharmaKarmadhipatiYogaPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    forming_divs = []
    relevant_planets = set()
    
    ninth_lord = gen.get_nthLord(charts["D1"], 9)
    tenth_lord = gen.get_nthLord(charts["D1"], 10)
    
    if ninth_lord == tenth_lord:
        forming_divs.append(f"D1 (Yogakaraka {ninth_lord})")
        relevant_planets.add(ninth_lord)
        IsPresent = True
    else:
        ninth_lord_data = charts["D1"]["planets"][ninth_lord]
        tenth_lord_data = charts["D1"]["planets"][tenth_lord]
        
        ninth_lord_house = ninth_lord_data["house-num"]
        tenth_lord_house = tenth_lord_data["house-num"]

        is_conjunct = ninth_lord in tenth_lord_data["conjuncts"]
        is_mutual_aspect = (ninth_lord in tenth_lord_data["Aspected-by"]) and (tenth_lord in ninth_lord_data["Aspected-by"])
        is_exchange = (ninth_lord_house == 10) and (tenth_lord_house == 9)

        IsPresent = is_conjunct or is_mutual_aspect or is_exchange
        if IsPresent:
            relation = "Conjunct" if is_conjunct else "in Mutual Aspect" if is_mutual_aspect else "in Exchange"
            forming_divs.append(f"D1 ({ninth_lord} and {tenth_lord} {relation})")
            relevant_planets.add(ninth_lord)
            relevant_planets.add(tenth_lord)

    if IsPresent:
        IsDharmaKarmadhipatiYogaPresent = True
        Rule = f'''The Lord of the 9th House (Dharma) and the Lord of the 10th House (Karma) are associated in D1: {", ".join(forming_divs)}.'''
        Results = f'''According to BPHS, this is the highest Raja Yoga (Dharma-Karmadhipati Yoga). It bestows immense fame, royal status, success in endeavors, power, and wealth.'''
        Note = f'''If formed in D9 (Navamsa), the results manifest strongly after marriage or in the latter half of life. If formed in D10 (Dasamsa), it guarantees extraordinary success and rise in one's career and profession. Ensure the lords are not afflicted by malefics or placed in dusthanas (6,8,12) which may reduce the intensity of the results.'''
        
        key = f"DHARMAKARMADHIPATI_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Dharma-Karmadhipati Raja Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "BPHS"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        
        # Generate table data

    return IsDharmaKarmadhipatiYogaPresent


# ==========================================================================================
# Function Name: NeechaBhangaRajaYoga
# Purpose: Calculates the presence of NeechaBhangaRajaYoga in the provided horoscope.
# Description: Evaluates NeechaBhangaRajaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def NeechaBhangaRajaYoga(charts):
    IsNeechaBhangaPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = set()
    bhanga_planets = []
    
    IsPresent = False
    
    exaltation_signs = {
        "Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo",
        "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra"
    }
    exalted_planet_in_sign = {
        "Aries": "Sun", "Taurus": "Moon", "Cancer": "Jupiter", "Virgo": "Mercury",
        "Libra": "Saturn", "Capricorn": "Mars", "Pisces": "Venus"
    }
    sign_lords = {
        "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury", "Cancer": "Moon",
        "Leo": "Sun", "Virgo": "Mercury", "Libra": "Venus", "Scorpio": "Mars",
        "Sagittarius": "Jupiter", "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
    }
    
    for planet, p_data in charts["D1"]["planets"].items():
        if planet in ["Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]:
            continue
            
        houserel = p_data.get("house-rel", "")
        if "Debilitated" in houserel:
            cancelled = False
            is_raja_yoga = False
            reasons = []

            moon_house = charts["D1"]["planets"]["Moon"]["house-num"]
            
            planet_house = p_data["house-num"]
            planet_from_moon = gen.housediff(moon_house, planet_house)
            
            kendra_trikona = [1, 4, 5, 7, 9, 10]
            in_kt_lagna = planet_house in kendra_trikona
            in_kt_moon = (planet != "Moon") and (planet_from_moon in kendra_trikona)
            is_well_placed = in_kt_lagna or in_kt_moon
            
            dispositor = p_data["dispositor"]
            disp_house = charts["D1"]["planets"][dispositor]["house-num"]
            disp_from_moon = gen.housediff(moon_house, disp_house)
            
            if disp_house in [1, 4, 7, 10]:
                cancelled = True
                if is_well_placed: is_raja_yoga = True
                reasons.append(f"its dispositor ({dispositor}) is in a Kendra from Lagna as per BPHS and Phaladeepika")
                relevant_planets.add(dispositor)
                
            if dispositor != "Moon" and disp_from_moon in [1, 4, 7, 10]:
                cancelled = True
                if is_well_placed: is_raja_yoga = True
                reasons.append(f"its dispositor ({dispositor}) is in a Kendra from Moon as per BPHS and Phaladeepika")
                relevant_planets.add(dispositor)
                relevant_planets.add("Moon")

            exalt_sign = exaltation_signs.get(planet)
            if exalt_sign:
                exalt_lord = sign_lords.get(exalt_sign)
                if exalt_lord and exalt_lord in charts["D1"]["planets"]:
                    exalt_lord_house = charts["D1"]["planets"][exalt_lord]["house-num"]
                    exalt_lord_from_moon = gen.housediff(moon_house, exalt_lord_house)
                    
                    if exalt_lord_house in [1, 4, 7, 10]:
                        cancelled = True
                        if is_well_placed: is_raja_yoga = True
                        reasons.append(f"the lord of its exaltation sign ({exalt_lord}) is in a Kendra from Lagna as per Phaladeepika")
                        relevant_planets.add(exalt_lord)
                        
                    if exalt_lord != "Moon" and exalt_lord_from_moon in [1, 4, 7, 10]:
                        cancelled = True
                        if is_well_placed: is_raja_yoga = True
                        reasons.append(f"the lord of its exaltation sign ({exalt_lord}) is in a Kendra from Moon as per Phaladeepika")
                        relevant_planets.add(exalt_lord)
                        if exalt_lord != "Moon": relevant_planets.add("Moon")

            debil_sign = p_data["sign"]
            planet_exalted_here = exalted_planet_in_sign.get(debil_sign)
            if planet_exalted_here and planet_exalted_here in charts["D1"]["planets"]:
                peh_house = charts["D1"]["planets"][planet_exalted_here]["house-num"]
                peh_from_moon = gen.housediff(moon_house, peh_house)
                
                if peh_house in [1, 4, 7, 10]:
                    cancelled = True
                    if is_well_placed: is_raja_yoga = True
                    reasons.append(f"the planet exalted in its debilitation sign ({planet_exalted_here}) is in a Kendra from Lagna as per Jataka Parijata and BPHS")
                    relevant_planets.add(planet_exalted_here)
                    
                if planet_exalted_here != "Moon" and peh_from_moon in [1, 4, 7, 10]:
                    cancelled = True
                    if is_well_placed: is_raja_yoga = True
                    reasons.append(f"the planet exalted in its debilitation sign ({planet_exalted_here}) is in a Kendra from Moon as per Jataka Parijata and BPHS")
                    relevant_planets.add(planet_exalted_here)
                    if planet_exalted_here != "Moon": relevant_planets.add("Moon")

            if "D9" in charts:
                d9_rel = charts["D9"]["planets"][planet].get("house-rel", "")
                if "Exhalted" in d9_rel or "Exalted" in d9_rel:
                    cancelled = True
                    reasons.append(f"it is Exalted in the Navamsa (D9) chart")

            if dispositor in p_data["Aspected-by"]:
                cancelled = True
                reasons.append(f"it is aspected by its dispositor ({dispositor})")
                relevant_planets.add(dispositor)

            if cancelled:
                IsPresent = True
                if is_raja_yoga:
                    bhanga_planets.append(f"{planet} (Raja Yoga formed: {', '.join(reasons)})")
                else:
                    if not is_well_placed:
                        bhanga_planets.append(f"{planet} (Simple Bhanga formed: {', '.join(reasons)}. Restricted from Raja Yoga as {planet} is not in a Kendra or Trikona from Lagna/Moon)")
                    else:
                        bhanga_planets.append(f"{planet} (Simple Bhanga formed: {', '.join(reasons)})")
                relevant_planets.add(planet)
                
    if IsPresent:
        IsNeechaBhangaPresent = True
        has_raja_yoga = any("Raja Yoga formed" in s for s in bhanga_planets)
        
        Rule = f'''In D1, the following debilitated planets have their debilitation cancelled: {"; ".join(bhanga_planets)}.'''
        if has_raja_yoga:
            Results = f'''According to classical texts like Phaladeepika and Jataka Parijata, when the debilitation of a planet is cancelled by strong planetary associations (like a dispositor or exaltation lord in a Kendra), AND the debilitated planet itself is placed in a Kendra (Angle) or Trikona (Trine), it creates a powerful Neecha Bhanga Raja Yoga. The native will experience initial struggles, hurdles, and delays, but will eventually experience a sudden and immense rise to power, success, and prosperity.'''
            yoga_name = "Neecha Bhanga Raja"
            differentiate = "Note: A simple 'Neecha Bhanga' only cancels the negative effects of debilitation. However, because your debilitated planet is well-placed in a Kendra or Trikona from the Lagna or Moon, and its cancellation conditions involve strong angular placements, this elevates into a powerful 'Neecha Bhanga Raja Yoga', bestowing significant success after initial struggles."
        else:
            Results = f'''The debilitation of the planet is cancelled, forming a Neecha Bhanga Yoga. This removes the negative effects of the debilitation, allowing the planet to function normally instead of giving malefic results. However, it does not elevate to a Raja Yoga (which grants kingship or extreme success) because the debilitated planet is not placed in a Kendra (Angle) or Trikona (Trine) from Lagna or Moon, restricting its ability to exert power.'''
            yoga_name = "Neecha Bhanga"
            differentiate = "Note: Your debilitated planet achieves a 'Neecha Bhanga' (cancellation of debilitation), which neutralizes its negative effects. However, it does NOT form a 'Neecha Bhanga Raja Yoga'. For a true Raja Yoga to form, the debilitated planet must be placed in a Kendra (1, 4, 7, 10) or Trikona (1, 5, 9) from the Lagna or Moon. Thus, it gives normal rather than extraordinary results."
            
        Note = f'''{differentiate}\n\nThe intensity is proportional to the number of cancellation conditions met. The initial struggles are necessary stepping stones.'''

        key = f"NEECHABHANGA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = yoga_name
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Phaladeepika"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        
        # Generate table data

    return IsNeechaBhangaPresent

# ==========================================================================================
# Function Name: KendraTrikonaYoga
# Purpose: Calculates the presence of KendraTrikonaYoga in the provided horoscope.
# Description: Evaluates KendraTrikonaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def KendraTrikonaYoga(charts):
    IsKendraTrikonaPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = set()
    associations = []
    IsPresent = False

    kendras = [1, 4, 7, 10]
    trikonas = [1, 5, 9]

    kendra_lords = {k: gen.get_nthLord(charts["D1"], k) for k in kendras}
    trikona_lords = {t: gen.get_nthLord(charts["D1"], t) for t in trikonas}

    for k_house, k_lord in kendra_lords.items():
        for t_house, t_lord in trikona_lords.items():
            if k_house == t_house:
                continue
            if (k_house == 10 and t_house == 9) or (k_house == 9 and t_house == 10):
                continue

            if k_lord == t_lord:
                associations.append(f"Lord of {k_house} and {t_house} ({k_lord}) acting as a Yogakaraka")
                relevant_planets.add(k_lord)
                IsPresent = True
                continue

            k_data = charts["D1"]["planets"][k_lord]
            t_data = charts["D1"]["planets"][t_lord]

            is_conjunct = k_lord in t_data["conjuncts"]
            is_mutual_aspect = (k_lord in t_data["Aspected-by"]) and (t_lord in k_data["Aspected-by"])
            is_exchange = (k_data["house-num"] == t_house) and (t_data["house-num"] == k_house)

            if is_conjunct or is_mutual_aspect or is_exchange:
                relation = "Conjunct" if is_conjunct else "in Mutual Aspect" if is_mutual_aspect else "in Exchange"
                assoc_str = f"Lord of {k_house} ({k_lord}) and Lord of {t_house} ({t_lord}) are {relation}"
                if assoc_str not in associations:
                    associations.append(assoc_str)
                    relevant_planets.add(k_lord)
                    relevant_planets.add(t_lord)
                    IsPresent = True

    if IsPresent:
        IsKendraTrikonaPresent = True
        Rule = f'''In D1, association between Kendra (angular) and Trikona (trinal) lords detected: {"; ".join(associations)}.'''
        Results = f'''According to BPHS, the association of a Kendra lord and a Trikona lord forms a highly auspicious Raja Yoga. It bestows fortune, status, leadership, and great success upon the native.'''
        Note = f'''The strength of this Yoga is immense, provided the participating planets are not debilitated or afflicted by natural malefics.'''

        key = f"KENDRATRIKONA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Kendra-Trikona Raja Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "BPHS"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        

    return IsKendraTrikonaPresent

# ==========================================================================================
# Function Name: SreenathaYoga
# Purpose: Calculates the presence of SreenathaYoga in the provided horoscope.
# Description: Evaluates SreenathaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def SreenathaYoga(charts):
    IsSreenathaYogaPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = []

    lagna_sign = charts["D1"]["ascendant"]["sign"]
    
    if lagna_sign == "Sagittarius":
        mercury = charts["D1"]["planets"]["Mercury"]
        sun = charts["D1"]["planets"]["Sun"]
        
        if mercury["sign"] == "Virgo" and "Sun" in mercury["conjuncts"]:
            IsSreenathaYogaPresent = True
            relevant_planets = ["Mercury", "Sun"]
            Rule = f"For Sagittarius Ascendant in D1, the 7th lord Mercury is exalted in the 10th house (Virgo) and conjunct the 9th lord Sun."
            Results = f"According to Phaladeepika, the native will have marks of Lord Vishnu (Sreenatha), be extremely wealthy, happy, loved by rulers, and achieve tremendous fame."
            Note = f"This is an extraordinarily rare and powerful Yoga specifically for Sagittarius ascendants."

            key = f"SREENATHA_D1"
            common.yogadoshas_dict[key] = {}
            common.yogadoshas_dict[key]["name"] = f"Sreenatha Yoga"
            common.yogadoshas_dict[key]["type"] = "Yoga"
            common.yogadoshas_dict[key]["exist"] = True
            common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
            common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
            common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
            common.yogadoshas_dict[key]["Source"] = "Phaladeepika"
            
            common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in relevant_planets]
            

    return IsSreenathaYogaPresent

# ==========================================================================================
# Function Name: ChatussagaraYoga
# Purpose: Calculates the presence of Chatussagara Yoga in the provided horoscope.
# Description: Checks if all four Kendra houses (1st, 4th, 7th, 10th) are occupied by planets.
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def ChatussagaraYoga(charts):
    IsChatussagaraPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = set()
    
    # Check all kendras (1, 4, 7, 10)
    kendras = [1, 4, 7, 10]
    valid_planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
    
    kendra_planets = {1: [], 4: [], 7: [], 10: []}
    
    for house in kendras:
        planets_in_house = gen.get_planets_in_house(house, charts["D1"]["planets"])
        for p in planets_in_house:
            if p in valid_planets:
                kendra_planets[house].append(p)
                relevant_planets.add(p)
                
    if all(len(kendra_planets[house]) > 0 for house in kendras):
        IsChatussagaraPresent = True
        
    if IsChatussagaraPresent:
        Rule = f'''All the Kendra houses (1st, 4th, 7th, and 10th) are occupied by planets.'''
        Results = f'''According to B.V. Raman, this yoga endows the native with a good reputation, status comparable to a ruler, a long, healthy, and prosperous life, and good children. The native's fame and influence will spread to the confines of the four oceans.'''
        Note = f'''The strength of this yoga depends on the dignity of the planets occupying the kendras. Exalted or own-sign planets enhance the results significantly.'''
        
        key = f"CHATUSSSAGARA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Chatussagara Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\\n ", "\\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\\n ", "\\n").replace("\\n","\\n        ") 
        
        # Dynamic Note Calculation
        exaltation_signs = {"Sun": "Aries", "Moon": "Taurus", "Mars": "Capricorn", "Mercury": "Virgo", "Jupiter": "Cancer", "Venus": "Pisces", "Saturn": "Libra"}
        own_signs = {"Sun": ["Leo"], "Moon": ["Cancer"], "Mars": ["Aries", "Scorpio"], "Mercury": ["Gemini", "Virgo"], "Jupiter": ["Sagittarius", "Pisces"], "Venus": ["Taurus", "Libra"], "Saturn": ["Capricorn", "Aquarius"]}
        debilitation_signs = {"Sun": "Libra", "Moon": "Scorpio", "Mars": "Cancer", "Mercury": "Pisces", "Jupiter": "Capricorn", "Venus": "Virgo", "Saturn": "Aries"}
        
        benefics = charts["D1"]["classifications"]["natural-benefics"]
        malefics = charts["D1"]["classifications"]["natural-malefics"]
        
        exalted = []
        own_sign = []
        debilitated = []
        benefics_present = []
        malefics_present = []
        
        planet_list = list(relevant_planets)
        for p in planet_list:
            sign = charts["D1"]["planets"][p]["sign"]
            if sign == exaltation_signs.get(p):
                exalted.append(p)
            elif sign in own_signs.get(p, []):
                own_sign.append(p)
            elif sign == debilitation_signs.get(p):
                debilitated.append(p)
                
            if p in benefics:
                benefics_present.append(p)
            elif p in malefics:
                malefics_present.append(p)
        
        dynamic_note = "Chart-Specific Analysis:\\n"
        if exalted:
            dynamic_note += f"- Exalted Planets: {', '.join(exalted)} (Massively strengthens the yoga)\\n"
        if own_sign:
            dynamic_note += f"- Planets in Own Sign: {', '.join(own_sign)} (Adds significant stability and power)\\n"
        if debilitated:
            dynamic_note += f"- Debilitated Planets: {', '.join(debilitated)} (May introduce initial struggles or weaknesses before success)\\n"
        if not exalted and not own_sign and not debilitated:
            dynamic_note += "- The planets are in neutral/friendly/enemy signs. The results will be moderate.\\n"
            
        dynamic_note += f"- Benefics contributing: {', '.join(benefics_present) if benefics_present else 'None'}\\n"
        dynamic_note += f"- Malefics contributing: {', '.join(malefics_present) if malefics_present else 'None'}\\n"
        
        if len(benefics_present) > len(malefics_present):
            dynamic_note += "- Conclusion: The yoga is dominated by benefics, bringing power through righteous, peaceful, and harmonious means."
        elif len(malefics_present) > len(benefics_present):
            dynamic_note += "- Conclusion: The yoga is dominated by malefics, suggesting that success and authority will come through intense struggle, aggressive action, or overcoming significant opposition."
        else:
            dynamic_note += "- Conclusion: A balanced mix of benefics and malefics, providing both the aggressive drive to succeed and the wisdom to sustain it."
        
        common.yogadoshas_dict[key]["Note"] = dynamic_note
        common.yogadoshas_dict[key]["Source"] = "B.V. Raman"
        
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        
    return IsChatussagaraPresent
