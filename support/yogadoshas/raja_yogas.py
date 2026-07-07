import support.generic as gen
import support.yogadoshas.common as common

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
        Results = f'''According to Brihat Parashara Hora Shastra, this is the highest Raja Yoga (Dharma-Karmadhipati Yoga). It bestows immense fame, royal status, success in endeavors, power, and wealth.'''
        Note = f'''If formed in D9 (Navamsa), the results manifest strongly after marriage or in the latter half of life. If formed in D10 (Dasamsa), it guarantees extraordinary success and rise in one's career and profession. Ensure the lords are not afflicted by malefics or placed in dusthanas (6,8,12) which may reduce the intensity of the results.'''
        
        key = f"DHARMAKARMADHIPATI_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Dharma-Karmadhipati Raja Yoga (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Brihat Parashara Hora Shastra"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        
        # Generate table data

    return IsDharmaKarmadhipatiYogaPresent


def NeechaBhangaRajaYoga(charts):
    IsNeechaBhangaPresent = False
    
    Rule = ""
    Results = ""
    Note = ""
    relevant_planets = set()
    bhanga_planets = []
    
    IsPresent = False
    
    for planet, p_data in charts["D1"]["planets"].items():
        if planet in ["Rahu", "Ketu", "Uranus", "Neptune", "Pluto"]:
            continue
            
        houserel = p_data.get("house-rel", "")
        if "Debilitated" in houserel:
            cancelled = False
            reasons = []

            dispositor = p_data["dispositor"]
            disp_house = charts["D1"]["planets"][dispositor]["house-num"]
            if disp_house in [1, 4, 7, 10]:
                cancelled = True
                reasons.append(f"its dispositor ({dispositor}) is in a Kendra from Lagna")
                relevant_planets.add(dispositor)

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
                bhanga_planets.append(f"{planet} (cancelled because {', '.join(reasons)})")
                relevant_planets.add(planet)
                
    if IsPresent:
        IsNeechaBhangaPresent = True
        Rule = f'''In D1, the following debilitated planets have their debilitation cancelled: {"; ".join(bhanga_planets)}.'''
        Results = f'''According to Phaladeepika, when the debilitation of a planet is cancelled, it creates a powerful Neecha Bhanga Raja Yoga. The native will experience initial struggles, hurdles, and delays in areas governed by the debilitated planet, but will eventually experience a sudden and immense rise to power, success, and prosperity.'''
        Note = f'''The intensity of the rise is proportional to the number of cancellation conditions met. The initial struggles are necessary stepping stones for the massive success that follows.'''

        key = f"NEECHABHANGA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Neecha Bhanga Raja Yoga (D1)"
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
        Results = f'''According to Brihat Parashara Hora Shastra, the association of a Kendra lord and a Trikona lord forms a highly auspicious Raja Yoga. It bestows fortune, status, leadership, and great success upon the native.'''
        Note = f'''The strength of this Yoga is immense, provided the participating planets are not debilitated or afflicted by natural malefics.'''

        key = f"KENDRATRIKONA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"Kendra-Trikona Raja Yoga (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Brihat Parashara Hora Shastra"
        
        planet_list = list(relevant_planets)
        common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in planet_list]
        

    return IsKendraTrikonaPresent

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
            common.yogadoshas_dict[key]["name"] = f"Sreenatha Yoga (D1)"
            common.yogadoshas_dict[key]["type"] = "Yoga"
            common.yogadoshas_dict[key]["exist"] = True
            common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
            common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
            common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
            common.yogadoshas_dict[key]["Source"] = "Phaladeepika"
            
            common.yogadoshas_dict[key]["relevant_planets"] = [p[0:2] for p in relevant_planets]
            

    return IsSreenathaYogaPresent
