import support.generic as gen
import support.yogadoshas.common as common

"""
karthari_yogadoshas.py
======================
Implements Papa Kartari Dosha and Shubha Kartari Yoga based on classical Vedic
scriptures (BPHS). Kartari (scissors) effect occurs when a house or planet is 
hemmed between natural malefics (Papa) or benefics (Shubha) in the 12th and 2nd 
houses from it.
"""

def get_planetary_natures(charts):
    """
    Classifies planets into Shubha (Benefic) and Papa (Malefic) for Kartari check.
    Returns: (list_of_shubha, list_of_papa)
    """
    shubha = ["Jupiter", "Venus", "Mercury"]
    papa = ["Saturn", "Mars", "Sun", "Rahu", "Ketu"]
    
    # Calculate Moon's Paksha Bala
    try:
        sun_lon = charts["D1"]["planets"]["Sun"]["pos"]["deg"]
        moon_lon = charts["D1"]["planets"]["Moon"]["pos"]["deg"]
        diff = (moon_lon - sun_lon) % 360
        
        # 8th day Shukla (84 deg) to 7th day Krishna (264 deg) = Shubha
        if 84 <= diff <= 264:
            shubha.append("Moon")
        else:
            papa.append("Moon")
    except KeyError:
        # Fallback if positions are missing
        shubha.append("Moon")
        
    return shubha, papa


def get_house_occupants(charts):
    """Returns a dict mapping house number (1-12) to a list of planets occupying it."""
    house_map = {i: [] for i in range(1, 13)}
    for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
        if p in charts["D1"]["planets"]:
            h = charts["D1"]["planets"][p]["house-num"]
            house_map[h].append(p)
    return house_map


PAPA_KARTARI_IMPACT = {
    1: "Struggle for identity, health issues, lack of confidence.",
    2: "Financial instability, family discord, issues with speech.",
    3: "Fearfulness, strained relations with siblings, poor communication.",
    4: "Domestic unhappiness, lack of peace at home, problems with mother.",
    5: "Hurdles regarding progeny, academic or creative blocks.",
    6: "Chronic health issues, persistent debt, recurring disputes.",
    7: "Conflict in marriage, loss in partnerships, business hurdles.",
    8: "Unpredictable crises, fear of hidden matters, inheritance delays.",
    9: "Lack of luck, conflict with father/gurus, spiritual blockage.",
    10: "Career stagnation, loss of reputation, pressure from superiors.",
    11: "Difficulties in realizing gains, unfulfilled desires.",
    12: "Excessive/unnecessary expenses, poor sleep, restlessness."
}

SHUBHA_KARTARI_IMPACT = {
    1: "Strong vitality, sense of purpose, natural grace.",
    2: "Steady accumulation of wealth, harmonious family life.",
    3: "Boldness, successful efforts, good relationship with siblings.",
    4: "Deep emotional security, luxurious home environment, maternal support.",
    5: "Intellectual brilliance, joy from children, good past karma.",
    6: "Ability to overcome rivals, quick recovery from illness.",
    7: "Harmonious marriage, successful alliances, balanced trade.",
    8: "Unexpected gains, deep spiritual insights, resilience.",
    9: "Abundant good fortune, support from elders/mentors.",
    10: "Recognition, steady professional growth, high social status.",
    11: "Easy attainment of desires, prosperity through social circles.",
    12: "Controlled expenditure, peaceful sleep, spiritual inclination."
}

PAPA_KARTARI_PLANET_IMPACT = {
    "Sun": "Ego, vitality, and authority are restricted or pressured.",
    "Moon": "Mental peace, emotions, and maternal relations are disturbed or stressed.",
    "Mars": "Courage and ambitions face obstacles or delays.",
    "Mercury": "Intellect, speech, and business face confusion or hurdles.",
    "Jupiter": "Wisdom, wealth, and joy from children face challenges or lack of expansion.",
    "Venus": "Relationships, luxuries, and artistic talents face restrictions or discord.",
    "Saturn": "Discipline, longevity, and karmic rewards face extreme delays or hardship.",
    "Rahu": "Ambitions and worldly desires face unexpected blocks.",
    "Ketu": "Spiritual progress and intuition feel clouded or disconnected."
}

SHUBHA_KARTARI_PLANET_IMPACT = {
    "Sun": "Ego, vitality, and authority are supported and enhanced.",
    "Moon": "Deep mental peace, emotional stability, and maternal support flourish.",
    "Mars": "Courage and ambitions find constructive and successful outlets.",
    "Mercury": "Intellect, communication, and business skills operate with high efficiency.",
    "Jupiter": "Wisdom, prosperity, and joy from children expand effortlessly.",
    "Venus": "Relationships, luxuries, and artistic talents blossom.",
    "Saturn": "Discipline and hard work yield steady, protected karmic rewards.",
    "Rahu": "Worldly ambitions are achieved smoothly without typical chaos.",
    "Ketu": "Spiritual growth and intuition are profoundly nurtured."
}


def KarthariYogaDoshas(charts):
    shubha_grahas, papa_grahas = get_planetary_natures(charts)
    house_occupants = get_house_occupants(charts)
    
    for house in range(1, 13):
        h12 = 12 if house == 1 else house - 1
        h2 = 1 if house == 12 else house + 1
        
        occupants_12 = house_occupants[h12]
        occupants_2 = house_occupants[h2]
        
        # ── Papa Kartari Check ──
        if occupants_12 and occupants_2:
            # Check if ONLY papa grahas are present in both 12th and 2nd
            if all(p in papa_grahas for p in occupants_12) and all(p in papa_grahas for p in occupants_2):
                target_occupants = house_occupants[house]
                
                # Mitigating factors
                mitigations = []
                mitigating_planets = []
                for p in target_occupants:
                    aspected_by = charts["D1"]["planets"][p].get("Aspected-by", [])
                    bene_aspects = [b for b in aspected_by if b in shubha_grahas]
                    if bene_aspects:
                        mitigations.append(f"{p} is aspected by benefic(s) {', '.join(bene_aspects)}")
                        mitigating_planets.extend(bene_aspects)
                        
                key = f"PAPA_KARTARI_H{house}"
                impact = PAPA_KARTARI_IMPACT[house]
                
                note = f"The {house}th house is hemmed between malefics {', '.join(occupants_12)} (in house {h12}) and {', '.join(occupants_2)} (in house {h2}). "
                if mitigations:
                    note += "Mitigation: " + "; ".join(mitigations) + ". "
                    
                target_str = f"{house}th house"
                result_str = f"The house suffers from restricted energy and constant external pressure. {impact}"
                
                if target_occupants:
                    target_str += f" (containing {', '.join(target_occupants)})"
                    planet_impacts = [f"{p}: {PAPA_KARTARI_PLANET_IMPACT[p]}" for p in target_occupants if p in PAPA_KARTARI_PLANET_IMPACT]
                    if planet_impacts:
                        result_str += "\n\nPlanetary Impacts:\n- " + "\n- ".join(planet_impacts)
                
                common.yogadoshas_dict[key] = {
                    "name": f"Papa Kartari Dosha - House {house}",
                    "type": "Dosha",
                    "exist": True,
                    "is_kartari": True,
                    "kartari_type": "Papa",
                    "impacted_target": target_str,
                    "relevant_planets": [p[:2] for p in list(set(occupants_12 + occupants_2 + target_occupants + mitigating_planets))],
                    "Rule": f"The {house}th house is 'scissored' between natural malefics in the 12th and 2nd houses from it.",
                    "Result": result_str,
                    "Note": note,
                    "Source": "Brihat Parashara Hora Shastra",
                    "Remedies": "Chant Hanuman Chalisa or Maha Mrityunjaya Mantra. Give charity on Saturdays (for Saturn) or Tuesdays (for Mars) to appease the specific energies."
                }
                
        # ── Shubha Kartari Check ──
        if occupants_12 and occupants_2:
            # Check if ONLY shubha grahas are present in both 12th and 2nd
            if all(p in shubha_grahas for p in occupants_12) and all(p in shubha_grahas for p in occupants_2):
                target_occupants = house_occupants[house]
                
                # Mitigating factors (negative in this case)
                mitigations = []
                mitigating_planets = []
                for p in target_occupants:
                    aspected_by = charts["D1"]["planets"][p].get("Aspected-by", [])
                    malefic_aspects = [m for m in aspected_by if m in papa_grahas]
                    if malefic_aspects:
                        mitigations.append(f"{p} is aspected by malefic(s) {', '.join(malefic_aspects)}")
                        mitigating_planets.extend(malefic_aspects)
                        
                key = f"SHUBHA_KARTARI_H{house}"
                impact = SHUBHA_KARTARI_IMPACT[house]
                
                note = f"The {house}th house is hemmed between benefics {', '.join(occupants_12)} (in house {h12}) and {', '.join(occupants_2)} (in house {h2}). "
                if mitigations:
                    note += "Warning: " + "; ".join(mitigations) + " which may destabilize the protective cushion. "
                    
                target_str = f"{house}th house"
                result_str = f"The house receives a 'protective cushion', allowing it to flourish with ease. {impact}"
                
                if target_occupants:
                    target_str += f" (containing {', '.join(target_occupants)})"
                    planet_impacts = [f"{p}: {SHUBHA_KARTARI_PLANET_IMPACT[p]}" for p in target_occupants if p in SHUBHA_KARTARI_PLANET_IMPACT]
                    if planet_impacts:
                        result_str += "\n\nPlanetary Impacts:\n- " + "\n- ".join(planet_impacts)
                
                common.yogadoshas_dict[key] = {
                    "name": f"Shubha Kartari Yoga - House {house}",
                    "type": "Yoga",
                    "exist": True,
                    "is_kartari": True,
                    "kartari_type": "Shubha",
                    "impacted_target": target_str,
                    "relevant_planets": [p[:2] for p in list(set(occupants_12 + occupants_2 + target_occupants + mitigating_planets))],
                    "Rule": f"The {house}th house is 'scissored' between natural benefics in the 12th and 2nd houses from it.",
                    "Result": result_str,
                    "Note": note,
                    "Source": "Brihat Parashara Hora Shastra"
                }
