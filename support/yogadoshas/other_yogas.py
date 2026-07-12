import support.generic as gen
import support.yogadoshas.common as common
import math

def _check_neechabhanga(planet, charts):
    """
    Evaluates if the specified debilitated planet gets Neechabhanga.
    Returns (True/False, reason_string).
    """
    p_data = charts["D1"]["planets"].get(planet)
    if not p_data: return False, ""
    
    houserel = p_data.get("house-rel", "")
    if "Debilitated" not in houserel:
        return False, ""
        
    cancelled = False
    reasons = []

    dispositor = p_data["dispositor"]
    disp_house = charts["D1"]["planets"][dispositor]["house-num"]
    moon_house = charts["D1"]["planets"]["Moon"]["house-num"]
    disp_from_moon = gen.housediff(moon_house, disp_house)
    
    if disp_house in [1, 4, 7, 10]:
        cancelled = True
        reasons.append(f"its dispositor ({dispositor}) is in a Kendra from Lagna")
        
    if dispositor != "Moon" and disp_from_moon in [1, 4, 7, 10]:
        cancelled = True
        reasons.append(f"its dispositor ({dispositor}) is in a Kendra from Moon")

    if "D9" in charts:
        d9_rel = charts["D9"]["planets"][planet].get("house-rel", "")
        if "Exhalted" in d9_rel or "Exalted" in d9_rel:
            cancelled = True
            reasons.append(f"it is Exalted in Navamsa (D9)")

    if dispositor in p_data.get("Aspected-by", []):
        cancelled = True
        reasons.append(f"it is aspected by its dispositor ({dispositor})")
        
    if cancelled:
        return True, ", ".join(reasons)
    return False, ""

# ==========================================================================================
# Function Name: GajaKesariYoga

# Purpose: Calculates the presence of GajaKesariYoga in the provided horoscope.
# Description: Evaluates GajaKesariYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def GajaKesariYoga(charts):
    IsGajaKesariYogaPresent = False
    
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    cnt = 0
    good_cnt = 0
    relevant_planets = ["Ju", "Mo"]

    lagnaJupiter = charts["D1"]["planets"].get("Jupiter")
    lagnaMoon = charts["D1"]["planets"].get("Moon")
    
    if not lagnaJupiter or not lagnaMoon:
        return IsGajaKesariYogaPresent
        
    if (gen.housediff(lagnaJupiter["house-num"], lagnaMoon["house-num"]) in [1,4,7,10]) and (lagnaJupiter.get("retro", 0) == 0):
        Name = "GajaKesari"
        Rule = f'''In D1, Jupiter [House number : {lagnaJupiter["house-num"]}] is in kendra from Moon[House number : {lagnaMoon["house-num"]}]. And Jupiter is not retrograde.'''

        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.extend(["Rahu", "Ketu"])
        
        aspectedby = lagnaJupiter.get("Aspected-by", [])
        conjuncts = lagnaJupiter.get("conjuncts", [])
        
        benefics_aspectingJupiter = list(set(benefics).intersection(aspectedby))
        benefics_conjunctJupiter = list(set(benefics).intersection(conjuncts))
        malefics_aspectingJupiter = list(set(malefics).intersection(aspectedby))
        malefics_conjunctJupiter = list(set(malefics).intersection(conjuncts))

        if (len(benefics_aspectingJupiter)>0) or (len(benefics_conjunctJupiter)>0):
            Rule += " Jupiter is associated by Benefics by conjunction or aspect."
            good_cnt += 1
        
        if (len(malefics_aspectingJupiter)>0) or (len(malefics_conjunctJupiter)>0):
            Name = "Weak GajaKesari"
            Rule += " But Jupiter is afflicted by Malefics."
            cnt += 1
        
        Rule += f" Hence a {Name} Yoga is formed."

        if lagnaMoon["house-num"] in [6, 8, 12]:
            Note += "Moon is present in dushtana House which weakens the yoga. "
            cnt += 1

        if True:
            lagnaSunHouse = charts["D1"]["planets"]["Sun"]["house-num"]
            sunToMoon = gen.housediff(lagnaSunHouse, lagnaMoon["house-num"])
            if (sunToMoon < 4) or (sunToMoon > 9):
                Note += "Moon is present within 4 houses with respect to the Sun which weakens the yoga. "
                cnt += 1
                if "Su" not in relevant_planets:
                    relevant_planets.append("Su")

        is_cancelled = False
        cancellation_reasons = []

        # Rule 1: Debilitation (without Neechabhanga)
        if lagnaMoon["sign"] == "Scorpio":
            has_nb, nb_reason = _check_neechabhanga("Moon", charts)
            if not has_nb:
                is_cancelled = True
                cancellation_reasons.append("Moon is debilitated without Neechabhanga")
            else:
                Note += f"Moon is debilitated but receives Neechabhanga ({nb_reason}). "
                cnt += 1

        if lagnaJupiter["sign"] == "Capricorn":
            has_nb, nb_reason = _check_neechabhanga("Jupiter", charts)
            if not has_nb:
                is_cancelled = True
                cancellation_reasons.append("Jupiter is debilitated without Neechabhanga")
            else:
                Note += f"Jupiter is debilitated but receives Neechabhanga ({nb_reason}). "
                cnt += 1

        # Rule 2: Combustion or Eclipse (Guru Chandal / Affliction)
        if "Sun" in conjuncts:
            # Simple check for combustion (could be refined with degrees if needed)
            is_cancelled = True
            cancellation_reasons.append("Jupiter is combust by the Sun")
            
        if "Rahu" in conjuncts or "Ketu" in conjuncts:
            is_cancelled = True
            cancellation_reasons.append("Jupiter is severely afflicted by nodes (forming Guru Chandal/Grahan)")

        # Rule 3: Dusthana Placement + Heavy Affliction
        if lagnaMoon["house-num"] in [6, 8, 12]:
            if len(malefics_aspectingJupiter) > 0 or len(malefics_conjunctJupiter) > 0:
                is_cancelled = True
                cancellation_reasons.append(f"Moon is in Dusthana (house {lagnaMoon['house-num']}) and Jupiter is afflicted")
        
        if True:
            if gen.isPushkaraNavamsha(lagnaJupiter.get("nakshatra",""), lagnaJupiter.get("pada",0)):
                Note += "Jupiter is in Pushkara Navamsa, which strengthens this yoga. "
                good_cnt += 1
            if gen.isPushkaraNavamsha(lagnaMoon.get("nakshatra",""), lagnaMoon.get("pada",0)):
                Note += "Moon is in Pushkara Navamsa, which strengthens this yoga. "
                good_cnt += 1
            if gen.isPushkaraBhaga(lagnaJupiter.get("sign-tatva",""), lagnaJupiter.get("pos",{}).get("deg",0)):
                Note += "Jupiter is in Pushkara Bhaga, which strengthens this yoga. "
                good_cnt += 1
            if gen.isPushkaraBhaga(lagnaMoon.get("sign-tatva",""), lagnaMoon.get("pos",{}).get("deg",0)):
                Note += "Moon is in Pushkara Bhaga, which strengthens this yoga. "
                good_cnt += 1

        if lagnaMoon["sign"] == "Taurus":
            Note += "Moon is exhalted, which strengthens this yoga. "
            good_cnt += 1

        if lagnaJupiter["sign"] == "Cancer":
            Note += "Jupiter is exhalted, which strengthens this yoga. "
            good_cnt += 1

        Note += f"Benefic planets aspecting Jupiter: {benefics_aspectingJupiter} and conjunct benefics: {benefics_conjunctJupiter}. Malefic planets aspecting Jupiter: {malefics_aspectingJupiter} and conjunct malefics: {malefics_conjunctJupiter}. Consider all these points [{good_cnt} positive and {cnt} negative] carefully before concluding the results of this Gajakesari yoga."

        for planet in aspectedby + conjuncts:
            if planet[0:2] not in relevant_planets:
                relevant_planets.append(planet[0:2])

        Results = f'''The word Gajakesari means Gaja for Elephant, and Kesari means Lion. Both Elephant and Lion are powerful and represent authority and intelligence. 
        People with Gaja Kesari Yoga seek good wealth, courage, respect from others and are generally good speakers.
        You will never have to worry about money if you have a strong Gajakesari Yoga in your horoscope chart. Even when there are anxious moments and finances are unstable, you will receive last-minute monetary help, putting an end to your anxiety.
        The effects of Gajakesari Yoga are not just limited to monetary gains. ith this yoga, you will be a courageous and happy person who is full of life and vigour. This yoga will make you a leader who can motivate people and change their lives through your inspirational speeches.'''

        IsGajaKesariYogaPresent = True
        key = f"GAJAKESARI_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"{Name} (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        
        if is_cancelled:
            common.yogadoshas_dict[key]["exist"] = False
            common.yogadoshas_dict[key]["CancellationReason"] = "Gajakesari Yoga is cancelled because: " + "; ".join(cancellation_reasons) + "."
        else:
            common.yogadoshas_dict[key]["exist"] = True
            
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "https://astrotalk.com/astrology-blog/know-who-can-seek-benefits-of-gajakesari-yoga-as-per-astrology/"   
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets
        
        full_names = [p for p in charts["D1"]["planets"].keys() if p[0:2] in relevant_planets]

    return IsGajaKesariYogaPresent

# ==========================================================================================
# Function Name: ChandraMangalaYoga
# Purpose: Calculates the presence of ChandraMangalaYoga in the provided horoscope.
# Description: Evaluates ChandraMangalaYoga
# Expected Impact: 
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def ChandraMangalaYoga(charts):
    IsChandraMangalaYogaPresent = False
    
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    bad_cnt = 0
    good_cnt = 0
    relevant_planets = ["Ma", "Mo"]

    lagnamars = charts["D1"]["planets"].get("Mars")
    lagnamoon = charts["D1"]["planets"].get("Moon")
    
    if not lagnamars or not lagnamoon:
        return IsChandraMangalaYogaPresent

    if lagnamars["sign"] == lagnamoon["sign"]:
        Name = "Chandra Mangala"
        Rule = f"In D1, Moon is conjunct with Mars. So Chandra Mangala Yoga is formed."

        is_cancelled = False
        cancellation_reasons = []

        # Rule 1: Debilitation (without Neechabhanga)
        if lagnamoon["sign"] == "Scorpio":
            has_nb, nb_reason = _check_neechabhanga("Moon", charts)
            if not has_nb:
                is_cancelled = True
                cancellation_reasons.append("Moon is debilitated without Neechabhanga")
            else:
                Note += f"Moon is debilitated but receives Neechabhanga ({nb_reason}). "
                bad_cnt += 1
                
        if lagnamars["sign"] == "Cancer":
            has_nb, nb_reason = _check_neechabhanga("Mars", charts)
            if not has_nb:
                is_cancelled = True
                cancellation_reasons.append("Mars is debilitated without Neechabhanga")
            else:
                Note += f"Mars is debilitated but receives Neechabhanga ({nb_reason}). "
                bad_cnt += 1

        if lagnamoon["sign"] == "Taurus":
            Note += "Moon is exhalted, which strengthens this yoga. "
            good_cnt += 1
            
        if lagnamars["sign"] == "Capricorn":
            Note += "Mars is exhalted, which strengthens this yoga. "
            good_cnt += 1

        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.extend(["Rahu", "Ketu"])
        
        aspectedby = lagnamars.get("Aspected-by", [])
        conjuncts = lagnamars.get("conjuncts", [])
        
        benefics_aspectingMars = list(set(benefics).intersection(aspectedby))
        benefics_conjunctMars = list(set(benefics).intersection(conjuncts))
        malefics_aspectingMars = list(set(malefics).intersection(aspectedby))
        malefics_conjunctMars = list(set(malefics).intersection(conjuncts))

        if (len(benefics_aspectingMars)>0) or (len(benefics_conjunctMars)>0):
            Note += "Moon and Mars are associated by Benefics by conjunction or aspect. "
            good_cnt += 1
        
        if (len(malefics_aspectingMars)>0) or (len(malefics_conjunctMars)>0):
            Note += "Moon and Mars is afflicted by Malefics. "
            bad_cnt += 1

        # Rule 2: Severe Affliction in Dusthana
        if lagnamars["house-num"] in [6, 8, 12]:
            if "Saturn" in malefics_aspectingMars or "Saturn" in malefics_conjunctMars or "Rahu" in malefics_aspectingMars or "Rahu" in malefics_conjunctMars:
                is_cancelled = True
                cancellation_reasons.append(f"The conjunction happens in a Dusthana (house {lagnamars['house-num']}) and is severely afflicted by harsh malefics (Saturn/Rahu)")

        if "Mars" in benefics:
            Note += "In this chart Mars is a benefic planet and "
            good_cnt += 1
        elif "Mars" in malefics:
            Note += "In this chart Mars is a malefic planet and "
            bad_cnt += 1
        else:
            Note += "In this chart Mars is a neutral planet and "
        
        if "Moon" in benefics:
            Note += "Moon is a benefic planet.\n"
            good_cnt += 1
        elif "Moon" in malefics:
            Note += "Moon is a malefic planet.\n"
            bad_cnt += 1
        else:
            Note += "Moon is a neutral planet.\n"

        Note += f"Consider all these points [{good_cnt} positive and {bad_cnt} negative] carefully before concluding the results of this Chandra Mangala yoga."

        for planet in aspectedby + conjuncts:
            if planet[0:2] not in relevant_planets:
                relevant_planets.append(planet[0:2])

        Results = f'''As the name suggests this Yoga is formed due to conjunction or aspect between Mars (Mangala) and Moon (Chandra). Chandra is the karaka of Mind and Mangala is the karaka of Power, energy and aggression. This is highly favorable Yoga that bestows the native with high monetary gains and a strong financial status. It grants a steady accumulation of wealth throughout the native's life, securing his financial stability and ensuring continuous prosperity.
        The individual with Chandra Mangal Yoga will have a powerful presence, exhibiting confidence, assertiveness, and leadership qualities. This influence is particularly beneficial in careers that demand authority, such as politics, law enforcement, entrepreneurship, or management. Such individuals often possess the ability to make difficult decisions swiftly and effectively, establishing themselves as influential figures in their chosen fields.
        Such a native earns primarily by means of his own strong determination and relentless hard work. Also he can earn by dealing in business related to women.
        Though this native makes a lot of money, his behavior towards others can sometimes be quite ruthless. He treats his near and dear ones nicely. The native can also be quite restless.
        If Mars and Moon are weakly placed or severely afflicted in native's chart, this yoga may impart negative traits such as impulsiveness, aggression, and emotional instability. The individual might struggle with anger management, leading to strained relationships and conflicts both in personal and professional life. Financial gains may also be accompanied by impulsive spending and unstable economic situations.'''

        IsChandraMangalaYogaPresent = True
        key = f"CHANDRAMANGALA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"{Name} Yoga (D1)"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        
        if is_cancelled:
            common.yogadoshas_dict[key]["exist"] = False
            common.yogadoshas_dict[key]["CancellationReason"] = "Chandra Mangala Yoga is cancelled because: " + "; ".join(cancellation_reasons) + "."
        else:
            common.yogadoshas_dict[key]["exist"] = True
            
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "https://www.astrosage.com/yoga/chandra-mangal-yoga.asp"   
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets
        
        # Distance calculation for custom table
        moon_deg_val = lagnamoon.get("pos",{}).get("deg",0) + lagnamoon.get("pos",{}).get("min",0)/60.0
        mars_deg_val = lagnamars.get("pos",{}).get("deg",0) + lagnamars.get("pos",{}).get("min",0)/60.0
        dist = round(abs(moon_deg_val - mars_deg_val), 2)
        dist_str = f"{dist}°"
        
        full_names = [p for p in charts["D1"]["planets"].keys() if p[0:2] in relevant_planets]
        
        # Provide exact degree distance only for Moon and Mars.
        dist_array = []
        for p in full_names:
            if p in ["Moon", "Mars"]:
                dist_array.append(dist_str)
            else:
                dist_array.append("-")


    return IsChandraMangalaYogaPresent
