import support.generic as gen
import support.yogadoshas.common as common

# ==========================================================================================
# Function Name: GuruYogaDoshas
# Purpose: Calculates the presence of Jupiter-Rahu (Guru Chandala) and Jupiter-Ketu (Ganesha) yogas.
# Description: Evaluates the conjunction of Jupiter with Rahu (Dosha) and Ketu (Yoga).
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - None: Populates the global yogadoshas dictionary.
# ==========================================================================================
def GuruYogaDoshas(charts):
    
    if "Jupiter" not in charts["D1"]["planets"] or "Rahu" not in charts["D1"]["planets"] or "Ketu" not in charts["D1"]["planets"]:
        return

    jupiter_house = charts["D1"]["planets"]["Jupiter"]["house-num"]
    rahu_house = charts["D1"]["planets"]["Rahu"]["house-num"]
    ketu_house = charts["D1"]["planets"]["Ketu"]["house-num"]
    
    jupiter_sign = charts["D1"]["planets"]["Jupiter"]["sign"]

    is_rahu_conjunct = (jupiter_house == rahu_house)
    is_ketu_conjunct = (jupiter_house == ketu_house)

    benefics = charts["D1"]["classifications"]["benefics"].copy()
    if "Jupiter" in benefics: benefics.remove("Jupiter")
    
    aspected_by = charts["D1"]["planets"]["Jupiter"].get("Aspected-by", [])
    benefics_aspecting = gen.list_intersection(benefics, aspected_by)

    # 1. Guru Chandala Dosha (Jupiter + Rahu)
    if is_rahu_conjunct:
        Name = "Guru Chandala"
        Rule = "Jupiter (Guru) and Rahu (Chandala) are placed in the same house, forming the classic Guru Chandala Dosha."
        Results = '''The native possesses a highly unorthodox and rebellious mindset. Jupiter represents traditional wisdom, religion, and ethics, while Rahu represents breaking taboos, illusions, and shortcuts. This conjunction creates a person who questions traditional authority and religious dogmas. If afflicted, it can lead to unethical behavior, hypocrisy, or becoming a fraudulent guru. However, if Jupiter is strong, it can produce a brilliant reformer who brings modern or unconventional wisdom to society. They often possess immense material ambitions and cleverness.
        **Remedies:** Cultivate immense respect for teachers and elders. Consciously avoid shortcuts and unethical practices. Worship Lord Ganesha to tame the chaotic Rahu energy. Wearing yellow sapphire (Pukhraj) is recommended only if Jupiter is highly favorable for the lagna.'''
        relevant_planets = ["Ju", "Ra"]
        Note = ""
        good_cnt = 0
        bad_cnt = 0

        if jupiter_sign in ["Sagittarius", "Pisces"]:
            Note += "Jupiter is in its own sign. The native's innate wisdom and moral compass are strong enough to handle Rahu's disruptive energy, turning it into constructive reform rather than destruction. "
            good_cnt += 1
        elif jupiter_sign == "Cancer":
            Note += "Jupiter is exalted. The native will ultimately use their unorthodox thinking for the highest good, protecting their ethics despite temptations. "
            good_cnt += 1
        elif jupiter_sign == "Capricorn":
            Note += "Jupiter is debilitated. This severely aggravates the Dosha, as the native's moral foundation is weak, making them highly susceptible to Rahu's illusions and deception. "
            bad_cnt += 1

        if len(benefics_aspecting) > 0:
            Note += f"Benefic aspect from {benefics_aspecting} acts as a saving grace, providing wise counsel and mitigating the unethical tendencies of the Dosha. "
            good_cnt += 1

        Note += f"Consider these factors ({good_cnt} mitigating, {bad_cnt} aggravating) when judging the severity of this Dosha."
                
        key = "GURU_CHANDALA_DOSHA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"{Name} Dosha"
        common.yogadoshas_dict[key]["type"] = "Dosha"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Jataka Parijata & BV Raman's Hindu Predictive Astrology"   
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets


    # 2. Ganesha Yoga (Jupiter + Ketu)
    if is_ketu_conjunct:
        Name = "Ganesha"
        Rule = "Jupiter (Guru) and Ketu (Mokshakaraka) are placed in the same house. This forms the highly spiritual Ganesha Yoga, distinct from the Guru Chandala Dosha."
        Results = '''This combination is an explosive mix of spiritual expansion (Jupiter) and absolute detachment/headless renunciation (Ketu). The native may struggle to fit into normal societal structures and might abruptly abandon traditional religious practices for deep, solitary mysticism. They possess profound intuitive intelligence and occult wisdom, much like Lord Ganesha. However, they can be extremely dogmatic, restless, or detached from worldly responsibilities. It is a highly spiritual yoga rather than a materialistic dosha.
        **Remedies:** Worship Lord Ganesha to channel extreme intuitive energy into practical wisdom. Practice grounding techniques to avoid complete isolation from worldly duties.'''
        relevant_planets = ["Ju", "Ke"]
        Note = ""
        good_cnt = 0
        bad_cnt = 0

        if jupiter_sign in ["Sagittarius", "Pisces"]:
            Note += "Jupiter is in its own sign. This immensely strengthens the spiritual wisdom, granting the native profound philosophical insights and true inner peace. "
            good_cnt += 1
        elif jupiter_sign == "Cancer":
            Note += "Jupiter is exalted. The combination produces a highly evolved soul with unparalleled intuitive and healing abilities. "
            good_cnt += 1
        elif jupiter_sign == "Capricorn":
            Note += "Jupiter is debilitated. The native might suffer from extreme fanaticism, a lack of direction, or misinterpreting spiritual texts leading to confusion. "
            bad_cnt += 1

        if len(benefics_aspecting) > 0:
            Note += f"Benefic aspect from {benefics_aspecting} grounds the native, helping them integrate their deep spiritual insights into everyday life without isolating themselves. "
            good_cnt += 1

        Note += f"Consider these factors ({good_cnt} strengthening, {bad_cnt} weakening) when judging this Yoga."
                
        key = "GANESHA_YOGA_D1"
        common.yogadoshas_dict[key] = {}
        common.yogadoshas_dict[key]["name"] = f"{Name} Yoga"
        common.yogadoshas_dict[key]["type"] = "Yoga"
        common.yogadoshas_dict[key]["exist"] = True
        common.yogadoshas_dict[key]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[key]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[key]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[key]["Source"] = "Nadi Astrology & General Classical Texts"   
        common.yogadoshas_dict[key]["relevant_planets"] = relevant_planets
