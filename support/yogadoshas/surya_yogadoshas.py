import support.generic as gen
import support.yogadoshas.common as common

SURYA_EXCLUDED = {"Moon", "Rahu", "Ketu", "Sun"}

def _get_surya_planets(charts, division, house_diff):
    sun_house = charts[division]["planets"]["Sun"]["house-num"]
    target_house = gen.compute_nthsign(sun_house, house_diff)
    occupants = []
    for p, data in charts[division]["planets"].items():
        if p in SURYA_EXCLUDED:
            continue
        if data.get("house-num") == target_house:
            occupants.append(p)
    return occupants, sun_house, target_house

def _categorize_planets(charts, planets, division):
    benefics = []
    malefics = []
    for p in planets:
        if gen.is_planet_benefic(charts, p, division):
            benefics.append(p)
        else:
            malefics.append(p)
    return benefics, malefics

def _check_combustion(charts, planets, division):
    return [p for p in planets if gen.is_planet_combust(charts, p, division)]

# ==============================================================================
# 1-3. Vesi Yogas (2nd from Sun)
# ==============================================================================

def ShubhaVesiYoga(charts):
    key = "SHUBHA_VESI_YOGA_D1"
    occupants, sun_house, target_house = _get_surya_planets(charts, "D1", 2)
    occ_12, _, _ = _get_surya_planets(charts, "D1", 12)
    if occ_12: return False  # Belongs to Ubhayachari
    benefics, malefics = _categorize_planets(charts, occupants, "D1")
    
    if not occupants or malefics:
        return False
        
    combust = _check_combustion(charts, benefics, "D1")
    bhanga = len(combust) == len(benefics)
    
    note = [
        f"Sun is in house {sun_house}. The 2nd house from Sun [House-{target_house}] contains natural benefics: {', '.join(benefics)}.",
        "This satisfies the condition for formation of this auspicious yoga.",
        "Technical Notes: The effects are strongly felt during the Mahadasha of the Sun and the specific planet in the 2nd house from it."
    ]
    
    entry = {
        "name": "Shubha Vesi Yoga",
        "type": "Yoga",
        "exist": not bhanga,
        "Rule": (
            "Formed when only natural benefics (Jupiter, Venus, and well-associated Mercury) "
            "occupy the 2nd house counted from the natal Sun. The Moon, Rahu, and Ketu are strictly excluded."
        ),
        "Note": "\n".join(note),
        "Result": (
            "The 2nd house from the Sun shows what the soul is moving towards, as well as the native's speech "
            "and outward projection of confidence.\n"
            "The native will be truthful, possessing an excellent, balanced, and persuasive speech. "
            "They will be wealthy, charitable, renowned, and respected by authority figures."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": f"Combustion (Asta): {', '.join(combust)} are combust. The ability to yield positive results is destroyed." if bhanga else "",
        "Remedies": "Not applicable. This is an auspicious yoga."
    }
    common.yogadoshas_dict[key] = entry
    return True

def PapaVesiDosha(charts):
    key = "PAPA_VESI_DOSHA_D1"
    occupants, sun_house, target_house = _get_surya_planets(charts, "D1", 2)
    occ_12, _, _ = _get_surya_planets(charts, "D1", 12)
    if occ_12: return False
    benefics, malefics = _categorize_planets(charts, occupants, "D1")
    
    if not occupants or benefics:
        return False
        
    note = [
        f"Sun is in house {sun_house}. The 2nd house from Sun [House-{target_house}] contains natural malefics: {', '.join(malefics)}.",
        "This satisfies the condition for formation of this Dosha.",
        "Technical Notes: Because the 2nd house denotes speech and the Sun denotes ego, Papa Vesi often indicates an ego-driven, aggressive communication style that isolates the native from support systems."
    ]
    
    entry = {
        "name": "Papa Vesi Dosha",
        "type": "Dosha",
        "exist": True,
        "Rule": (
            "Formed when only natural malefics (Saturn, Mars, etc.) occupy the 2nd house from the Sun. "
            "Moon and Nodes are excluded."
        ),
        "Note": "\n".join(note),
        "Result": (
            "The native struggles with harsh or deceitful speech. They often face conflicts with authority, "
            "possess a restless disposition, and may struggle to accumulate wealth due to a lack of moral grounding."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": "",
        "Remedies": "Practice of Mauna (conscious silence) or chanting the Gayatri Mantra to purify the speech and the ego."
    }
    common.yogadoshas_dict[key] = entry
    return True

def MixedVesiYoga(charts):
    key = "MIXED_VESI_YOGA_D1"
    occupants, sun_house, target_house = _get_surya_planets(charts, "D1", 2)
    occ_12, _, _ = _get_surya_planets(charts, "D1", 12)
    if occ_12: return False
    benefics, malefics = _categorize_planets(charts, occupants, "D1")
    
    if not benefics or not malefics:
        return False
        
    combust_benefics = _check_combustion(charts, benefics, "D1")
    bhanga = len(combust_benefics) == len(benefics)
    
    note = [
        f"Sun is in house {sun_house}. The 2nd house from Sun [House-{target_house}] contains both benefics ({', '.join(benefics)}) and malefics ({', '.join(malefics)}).",
        "This creates a mixed projection of the ego.",
        "Technical Notes: The Dasha sequence dictates the active energy. During the Dasha of the benefic, speech and wealth improve; during the malefic's Dasha, conflicts arise."
    ]
    
    entry = {
        "name": "Mixed Vesi Yoga",
        "type": "Yoga",
        "exist": not bhanga,
        "Rule": (
            "Formed when both natural benefics AND natural malefics occupy the 2nd house from the natal Sun."
        ),
        "Note": "\n".join(note),
        "Result": (
            "Creates a mixed projection of the ego. The native will experience fluctuating wealth and speech patterns. "
            "Moments of great eloquence and truthfulness will be interspersed with periods of harshness or conflict with authority."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": f"Combustion (Asta): Benefics ({', '.join(combust_benefics)}) are combust, allowing the malefic planet to dominate the yoga, turning it effectively into a Papa Vesi Dosha." if bhanga else "",
        "Remedies": "General remedies for the Sun (offering Arghya) to balance the ego and clarify the soul's direction."
    }
    common.yogadoshas_dict[key] = entry
    return True

# ==============================================================================
# 4-6. Voshi Yogas (12th from Sun)
# ==============================================================================

def ShubhaVoshiYoga(charts):
    key = "SHUBHA_VOSHI_YOGA_D1"
    occupants, sun_house, target_house = _get_surya_planets(charts, "D1", 12)
    occ_2, _, _ = _get_surya_planets(charts, "D1", 2)
    if occ_2: return False
    benefics, malefics = _categorize_planets(charts, occupants, "D1")
    
    if not occupants or malefics:
        return False
        
    combust = _check_combustion(charts, benefics, "D1")
    bhanga = len(combust) == len(benefics)
    
    note = [
        f"Sun is in house {sun_house}. The 12th house from Sun [House-{target_house}] contains natural benefics: {', '.join(benefics)}.",
        "Technical Notes: This yoga often dictates the intent behind a person's actions (12th house as the background/past driving the Sun/ego)."
    ]
    
    entry = {
        "name": "Shubha Voshi Yoga",
        "type": "Yoga",
        "exist": not bhanga,
        "Rule": (
            "Formed exclusively by natural benefics occupying the 12th house from the natal Sun. "
            "Moon and Nodes excluded."
        ),
        "Note": "\n".join(note),
        "Result": (
            "The 12th house from the Sun represents the foundation of the soul, spiritual inclinations, and subconscious drives.\n"
            "The native is exceptionally learned, spiritually inclined, and charitable. "
            "They possess a strong, noble memory and have a natural affinity for higher philosophical knowledge."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": f"Combustion (Asta): {', '.join(combust)} are combust. The planet loses its power to form an independent foundation for the Sun." if bhanga else "",
        "Remedies": "Not applicable."
    }
    common.yogadoshas_dict[key] = entry
    return True

def PapaVoshiDosha(charts):
    key = "PAPA_VOSHI_DOSHA_D1"
    occupants, sun_house, target_house = _get_surya_planets(charts, "D1", 12)
    occ_2, _, _ = _get_surya_planets(charts, "D1", 2)
    if occ_2: return False
    benefics, malefics = _categorize_planets(charts, occupants, "D1")
    
    if not occupants or benefics:
        return False
        
    note = [
        f"Sun is in house {sun_house}. The 12th house from Sun [House-{target_house}] contains natural malefics: {', '.join(malefics)}.",
        "Technical Notes: The 12th house also governs sleep. Papa Voshi can lead to sleep disturbances fueled by anxiety or unresolved ego conflicts."
    ]
    
    entry = {
        "name": "Papa Voshi Dosha",
        "type": "Dosha",
        "exist": True,
        "Rule": (
            "Formed exclusively by natural malefics occupying the 12th house from the natal Sun."
        ),
        "Note": "\n".join(note),
        "Result": (
            "The native may suffer from a lack of physical vitality, vision problems, and a cruel or vindictive subconscious. "
            "They often face hidden enemies or subconscious fears that drain their confidence."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": "",
        "Remedies": "Donating to spiritual organizations, eye hospitals, or engaging in selfless service (Seva) to burn negative subconscious karma."
    }
    common.yogadoshas_dict[key] = entry
    return True

def MixedVoshiYoga(charts):
    key = "MIXED_VOSHI_YOGA_D1"
    occupants, sun_house, target_house = _get_surya_planets(charts, "D1", 12)
    occ_2, _, _ = _get_surya_planets(charts, "D1", 2)
    if occ_2: return False
    benefics, malefics = _categorize_planets(charts, occupants, "D1")
    
    if not benefics or not malefics:
        return False
        
    combust_benefics = _check_combustion(charts, benefics, "D1")
    bhanga = len(combust_benefics) == len(benefics)
    
    note = [
        f"Sun is in house {sun_house}. The 12th house from Sun [House-{target_house}] contains both benefics ({', '.join(benefics)}) and malefics ({', '.join(malefics)}).",
        "Technical Notes: Reflects a karmic push-and-pull where the native must consciously choose higher philosophical paths over baser subconscious reactions."
    ]
    
    entry = {
        "name": "Mixed Voshi Yoga",
        "type": "Yoga",
        "exist": not bhanga,
        "Rule": (
            "Formed when both benefics and malefics occupy the 12th house from the natal Sun."
        ),
        "Note": "\n".join(note),
        "Result": (
            "Creates a divided subconscious foundation. The native will possess spiritual and charitable inclinations "
            "but will simultaneously battle hidden fears, vindictive thoughts, or vitality drains."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": f"Combustion (Asta): Benefics ({', '.join(combust_benefics)}) are combust. This removes the spiritual protection, leaving the subconscious vulnerable to the malefic energy." if bhanga else "",
        "Remedies": "Seva (selfless service) and donations to charity to activate the benefic 12th house energies and suppress the malefic ones."
    }
    common.yogadoshas_dict[key] = entry
    return True

# ==============================================================================
# 7-9. Ubhayachari Yogas (2nd and 12th from Sun)
# ==============================================================================

def ShubhaUbhayachariYoga(charts):
    key = "SHUBHA_UBHAYA_YOGA_D1"
    occ_2, sun_h, target_2 = _get_surya_planets(charts, "D1", 2)
    occ_12, _, target_12 = _get_surya_planets(charts, "D1", 12)
    
    if not occ_2 or not occ_12:
        return False
        
    ben_2, mal_2 = _categorize_planets(charts, occ_2, "D1")
    ben_12, mal_12 = _categorize_planets(charts, occ_12, "D1")
    
    if mal_2 or mal_12:
        return False
        
    combust = _check_combustion(charts, ben_2 + ben_12, "D1")
    bhanga = len(combust) == len(ben_2 + ben_12)
    
    note = [
        f"Sun is in house {sun_h}. The 2nd house contains {', '.join(ben_2)} and the 12th house contains {', '.join(ben_12)}.",
        "Solar Kartari: Shubha Ubhayachari is effectively a Shubha Kartari around the Sun, cushioning the soul and ego."
    ]
    
    entry = {
        "name": "Shubha Ubhayachari Yoga",
        "type": "Yoga",
        "exist": not bhanga,
        "Rule": (
            "Formed when only natural benefics occupy both the 2nd and 12th houses counted from the natal Sun. "
            "Exclusions: Moon, Rahu, and Ketu."
        ),
        "Note": "\n".join(note),
        "Result": (
            "Dr. B.V. Raman notes this as a powerful configuration. The native will be highly virtuous, possess excellent eyesight, "
            "achieve a high rank or royal equivalent, and exhibit a calm, authoritative, and noble demeanor. "
            "The soul's purpose is supported by pure, ethical means."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": f"Combustion (Asta): {', '.join(combust)} are combust. The yoga suffers a severe weakening as the 'entourage' is burned by the King's rays." if bhanga else "",
        "Remedies": "Not applicable."
    }
    common.yogadoshas_dict[key] = entry
    return True

def PapaUbhayachariDosha(charts):
    key = "PAPA_UBHAYA_DOSHA_D1"
    occ_2, sun_h, target_2 = _get_surya_planets(charts, "D1", 2)
    occ_12, _, target_12 = _get_surya_planets(charts, "D1", 12)
    
    if not occ_2 or not occ_12:
        return False
        
    ben_2, mal_2 = _categorize_planets(charts, occ_2, "D1")
    ben_12, mal_12 = _categorize_planets(charts, occ_12, "D1")
    
    if ben_2 or ben_12:
        return False
        
    note = [
        f"Sun is in house {sun_h}. The 2nd house contains {', '.join(mal_2)} and the 12th house contains {', '.join(mal_12)}.",
        "Solar Kartari: Papa Ubhayachari is effectively a Papa Kartari (malefic hemming) around the Sun."
    ]
    
    entry = {
        "name": "Papa Ubhayachari Dosha",
        "type": "Dosha",
        "exist": True,
        "Rule": (
            "Formed when only natural malefics occupy both the 2nd and 12th houses from the Sun."
        ),
        "Note": "\n".join(note),
        "Result": (
            "The native's vitality and ego are under siege. It makes the native harsh in speech, prone to unethical behavior, "
            "mentally restless, and they may suffer from physical ailments (especially related to the eyes or heart). "
            "Authority is achieved through tyranny or not achieved at all."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": "",
        "Remedies": "Mantra: Daily recitation of the Aditya Hrudayam Stotram or the Gayatri Mantra at sunrise.\nDonations: Donating wheat, jaggery, or copper on Sundays.\nLifestyle: Offering Arghya to the rising Sun daily to strengthen the Atma."
    }
    common.yogadoshas_dict[key] = entry
    return True

def MixedUbhayachariYoga(charts):
    key = "MIXED_UBHAYA_YOGA_D1"
    occ_2, sun_h, target_2 = _get_surya_planets(charts, "D1", 2)
    occ_12, _, target_12 = _get_surya_planets(charts, "D1", 12)
    
    if not occ_2 or not occ_12:
        return False
        
    ben_2, mal_2 = _categorize_planets(charts, occ_2, "D1")
    ben_12, mal_12 = _categorize_planets(charts, occ_12, "D1")
    
    total_ben = ben_2 + ben_12
    total_mal = mal_2 + mal_12
    
    if not total_ben or not total_mal:
        return False
        
    combust_ben = _check_combustion(charts, total_ben, "D1")
    bhanga = len(combust_ben) == len(total_ben)
    
    note = [
        f"Sun is in house {sun_h}. The 2nd house contains {', '.join(occ_2)} and the 12th house contains {', '.join(occ_12)}.",
        "Technical Notes: This configuration most accurately represents the classical concept of the King's 'entourage', "
        "which logically requires both peaceful ministers and military generals to rule effectively."
    ]
    
    entry = {
        "name": "Mixed Ubhayachari Yoga",
        "type": "Yoga",
        "exist": not bhanga,
        "Rule": (
            "Formed when there is a mix of benefics and malefics flanking the Sun in the 2nd and 12th houses."
        ),
        "Note": "\n".join(note),
        "Result": (
            "A native born with a standard/mixed Ubhayachari Yoga will be an eloquent speaker, possess strong physical vitality, "
            "have well-proportioned limbs, find joy in learning, and be wealthy and liked by all.\n"
            "The native employs a balanced approach to leadership-using diplomacy but capable of assertiveness and force when necessary."
        ),
        "Source": "Classical Surya Yogas",
        "CancellationReason": f"Combustion (Asta): Benefics ({', '.join(combust_ben)}) are combust." if bhanga else "",
        "Remedies": "Offering Arghya to the Sun to maintain a balanced, healthy ego."
    }
    common.yogadoshas_dict[key] = entry
    return True
