import support.generic as gen
import support.yogadoshas.common as common

"""
chandra_yogadoshas.py
=====================
Implements the primary Chandra (Lunar) yoga/dosha configurations as per
classical Vedic frameworks (BPHS, Phaladeepika, Varahamihira).

By design exactly ONE of the four below will always be present in any kundali:
  1. Durdhara Yoga   -- planets in BOTH 2nd and 12th from Moon
  2. Sunapha Yoga    -- planet(s) ONLY in 2nd from Moon
  3. Anapha Yoga     -- planet(s) ONLY in 12th from Moon
  4. Kemadruma Dosha -- NO valid planets in 2nd OR 12th from Moon

Additionally, independently checked:
  5. Sakata Dosha    -- Jupiter in 6th, 8th or 12th from Moon

Rule for valid planets in Sunapha/Anapha/Durdhara/Kemadruma:
  Only Mars, Mercury, Jupiter, Venus, Saturn count.
  Sun, Rahu, Ketu are EXCLUDED.

Detection priority: Durdhara -> Sunapha/Anapha -> Kemadruma
"""

# Planets that can form Chandra yogas (Sun, Rahu, Ketu excluded)
VALID_PLANETS = ["Mars", "Mercury", "Jupiter", "Venus", "Saturn"]
PLANET_ABBREV = {"Mars": "Ma", "Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa"}


def _describe_planet_flavors(planets):
    """Return a short note about what each forming planet signifies."""
    flavor_map = {
        "Mars":    "Mars: Prosperity through courage, real estate, and physical endeavor.",
        "Mercury": "Mercury: Wealth through commerce, writing, trade, and sharp business acumen.",
        "Jupiter": "Jupiter: Prosperity tied to wisdom, advisory roles, teaching, academia, and law.",
        "Venus":   "Venus: Wealth through luxury, arts, entertainment, beauty, and social grace.",
        "Saturn":  "Saturn: Stable, long-lasting wealth built slowly through discipline and persistence.",
    }
    return " | ".join(flavor_map[p] for p in planets if p in flavor_map)


def ChandraYogaDoshas(charts):
    """
    Detects and registers exactly one of the four Chandra yoga/dosha
    configurations present in the native's D1 chart.

    Parameters:
        charts (dict): Full astrodata dictionary with D1 chart data.

    Returns:
        str: Key of the detected yoga/dosha ("SUNAPHA_D1", "ANAPHA_D1",
             "DURDHARA_D1", or "KEMADRUMA_D1").
    """
    moon_house = charts["D1"]["planets"]["Moon"]["house-num"]

    planets_in_2nd  = []
    planets_in_12th = []

    for p in VALID_PLANETS:
        p_house = charts["D1"]["planets"][p]["house-num"]
        diff    = gen.housediff(moon_house, p_house)
        if diff == 2:
            planets_in_2nd.append(p)
        elif diff == 12:
            planets_in_12th.append(p)

    has_2nd  = len(planets_in_2nd)  > 0
    has_12th = len(planets_in_12th) > 0

    # ── Priority 1: Durdhara — planets on BOTH sides ──────────────────────────
    if has_2nd and has_12th:
        _register_durdhara(charts, planets_in_2nd, planets_in_12th)
        return "DURDHARA_D1"

    # ── Priority 2a: Sunapha — only 2nd house from Moon ───────────────────────
    if has_2nd and not has_12th:
        _register_sunapha(charts, planets_in_2nd)
        return "SUNAPHA_D1"

    # ── Priority 2b: Anapha — only 12th house from Moon ───────────────────────
    if has_12th and not has_2nd:
        _register_anapha(charts, planets_in_12th)
        return "ANAPHA_D1"

    # ── Priority 3: Kemadruma — no valid planets on either side ───────────────
    _register_kemadruma(charts, moon_house)
    return "KEMADRUMA_D1"


# ──────────────────────────────────────────────────────────────────────────────
# Individual registration helpers
# ──────────────────────────────────────────────────────────────────────────────

def _register_sunapha(charts, forming_planets):
    key     = "SUNAPHA_D1"
    abbrevs = [PLANET_ABBREV[p] for p in forming_planets]
    flavor  = _describe_planet_flavors(forming_planets)

    common.yogadoshas_dict[key] = {
        "name":             "Sunapha Yoga",
        "type":             "Yoga",
        "exist":            True,
        "relevant_planets": ["Mo"] + abbrevs,
        "Rule": (
            "One or more planets (Mars, Mercury, Jupiter, Venus, or Saturn) occupy the "
            "2nd house from the natal Moon. The Sun, Rahu, and Ketu are excluded. "
            f"Forming planet(s): {', '.join(forming_planets)}."
        ),
        "Note": (
            "Sunapha Yoga also cancels Kemadruma Dosha. Effects manifest most strongly "
            "during the Mahadasha/Antardasha of the forming planet(s). "
            + flavor
        ),
        "Result": (
            "As per BPHS, Phaladeepika, and Varahamihira: The native will be self-made, "
            "intelligent, happy, and immensely wealthy through their own effort and intellect. "
            "They achieve widespread respect and establish a powerful reputation. "
            "Unlike Raja Yogas, this specifically indicates self-earned wealth."
        ),
        "Source": "Brihat Parashara Hora Shastra (BPHS), Phaladeepika, Varahamihira",
        "CancellationReason": "",
    }


def _register_anapha(charts, forming_planets):
    key     = "ANAPHA_D1"
    abbrevs = [PLANET_ABBREV[p] for p in forming_planets]
    flavor  = _describe_planet_flavors(forming_planets)

    common.yogadoshas_dict[key] = {
        "name":             "Anapha Yoga",
        "type":             "Yoga",
        "exist":            True,
        "relevant_planets": ["Mo"] + abbrevs,
        "Rule": (
            "One or more planets (Mars, Mercury, Jupiter, Venus, or Saturn) occupy the "
            "12th house from the natal Moon. The Sun, Rahu, and Ketu are excluded. "
            f"Forming planet(s): {', '.join(forming_planets)}."
        ),
        "Note": (
            "The 12th from the Moon represents subconscious expenditures, physical comforts, "
            "and spiritual inclinations. Benefics here grant peaceful sleep, spiritual wealth, "
            "and charitable tendencies. Malefics may channel expenses toward health or disputes. "
            "Effects are strongest during the Mahadasha/Antardasha of the forming planet(s). "
            + flavor
        ),
        "Result": (
            "As per BPHS and Phaladeepika: The native will possess great self-respect, be "
            "healthy, well-mannered, and famous. They enjoy material and sensual comforts "
            "while maintaining a generous and unattached disposition."
        ),
        "Source": "Brihat Parashara Hora Shastra (BPHS), Phaladeepika",
        "CancellationReason": "",
    }


def _register_durdhara(charts, planets_in_2nd, planets_in_12th):
    key          = "DURDHARA_D1"
    all_forming  = planets_in_2nd + planets_in_12th
    abbrevs      = [PLANET_ABBREV[p] for p in all_forming]
    only_malefics_both_sides = (
        all(p in ["Mars", "Saturn"] for p in planets_in_2nd) and
        all(p in ["Mars", "Saturn"] for p in planets_in_12th)
    )

    note = (
        "Durdhara Yoga is a complete protective shield for the mind. "
        f"Planet(s) in 2nd from Moon: {', '.join(planets_in_2nd)}. "
        f"Planet(s) in 12th from Moon: {', '.join(planets_in_12th)}. "
        "Effects are most prominent during the combined Dashas of the forming planets. "
    )
    if only_malefics_both_sides:
        note += (
            "CAUTION: Both sides are occupied exclusively by harsh malefics (Mars/Saturn), "
            "forming a Papa Kartari Yoga around the Moon. While wealth is generated, this "
            "configuration may also bring mental anguish, paranoia, or a harsh demeanor."
        )
    else:
        note += (
            "Pure benefics (Jupiter, Venus) or well-placed Mercury on both sides create "
            "supreme emotional peace and unblemished wealth."
        )

    common.yogadoshas_dict[key] = {
        "name":             "Durdhara Yoga",
        "type":             "Yoga",
        "exist":            True,
        "relevant_planets": ["Mo"] + abbrevs,
        "Rule": (
            "Planets (excluding Sun, Rahu, Ketu) are simultaneously present in BOTH the "
            "2nd and 12th houses from the natal Moon, flanking it on both sides. "
            f"2nd house: {', '.join(planets_in_2nd)}. "
            f"12th house: {', '.join(planets_in_12th)}."
        ),
        "Note": note,
        "Result": (
            "As per BPHS and Phaladeepika: The native will be abundantly wealthy, possess "
            "conveyances and property, command loyal followers or employees, and exhibit "
            "highly ethical conduct. The mind is perfectly balanced, drawing on resources "
            "from both past (12th) and future (2nd), creating immense emotional stability."
        ),
        "Source": "Brihat Parashara Hora Shastra (BPHS), Phaladeepika",
        "CancellationReason": "",
    }


def _register_kemadruma(charts, moon_house):
    key = "KEMADRUMA_D1"

    # ── Cancellation checks (classical Kemadruma Bhanga rules) ────────────────
    # Source: BPHS, Brihat Jataka, Phaladeepika
    #
    # Rule 1: Moon is CONJUNCT any valid planet (same house as Moon)
    # Rule 2: Any valid planet occupies a KENDRA (1, 4, 7, 10) from the Moon
    # Rule 3: Any valid planet occupies a KENDRA (house 1, 4, 7, 10) from the Lagna
    # Rule 4: Moon receives a direct aspect from Jupiter
    cancelled            = False
    reasons              = []
    cancellation_planets = []

    for p in VALID_PLANETS:
        p_house   = charts["D1"]["planets"][p]["house-num"]
        diff_moon = gen.housediff(moon_house, p_house)
        diff_lagn = p_house   # Lagna is always house 1

        # Rule 1 & 2: Conjunct or Kendra from Moon
        if diff_moon in [1, 4, 7, 10]:
            cancelled = True
            label = "conjunct" if diff_moon == 1 else f"in the {diff_moon}th from the Moon (Kendra)"
            reasons.append(f"{p} is {label}")
            abbr = PLANET_ABBREV[p]
            if abbr not in cancellation_planets:
                cancellation_planets.append(abbr)

        # Rule 3: Planet in a Kendra from the Lagna (houses 1, 4, 7, 10)
        if diff_lagn in [1, 4, 7, 10]:
            cancelled = True
            reasons.append(f"{p} is in house {p_house} (a Kendra from the Lagna)")
            abbr = PLANET_ABBREV[p]
            if abbr not in cancellation_planets:
                cancellation_planets.append(abbr)

    # Rule 4: Jupiter directly aspects the Moon
    if "Jupiter" in charts["D1"]["planets"]["Moon"].get("Aspected-by", []):
        cancelled = True
        reasons.append("Moon is aspected by Jupiter")
        if "Ju" not in cancellation_planets:
            cancellation_planets.append("Ju")

    # ── Build entry ────────────────────────────────────────────────────────────
    entry = {
        "name":             "Kemadruma Dosha",
        "type":             "Dosha",
        "relevant_planets": ["Mo"] + cancellation_planets,
        "Rule": (
            "There are NO valid planets (excluding Sun, Rahu, Ketu) in both the 2nd "
            "and 12th houses from the natal Moon. The Moon receives no flanking support, "
            "leaving the mind exposed and unsupported."
        ),
        "Note": (
            "Kemadruma Bhanga (cancellation) occurs when: (1) any valid planet is conjunct "
            "or in a Kendra (1st, 4th, 7th, or 10th) from the Moon, (2) any valid planet "
            "occupies a Kendra house (1, 4, 7, 10) from the Lagna, or (3) Jupiter directly "
            "aspects the Moon. Even when cancelled, the native may experience brief periods "
            "of isolation or mental uncertainty during Moon Dasha/Antardasha."
        ),
        "Result": (
            "As per BPHS: Even if born into a royal family, Kemadruma Dosha can reduce "
            "the native to destitution, sorrow, and menial labor. The native suffers from "
            "profound loneliness, mental instability, unexplainable fears, and a constant "
            "feeling of lacking support from family and society."
        ),
        "Source": "Brihat Parashara Hora Shastra (BPHS), Brihat Jataka",
        "Remedies": (
            "1. Fast every Monday. "
            "2. Chant 'Om Namah Shivaya' daily or recite the Shiva Panchakshari Stotram. "
            "3. Offer raw milk, water, and Bilva leaves to a Shivalinga - especially on "
            "Mondays or during Pradosham. "
            "4. Wear a high-quality natural Pearl (Moti) set in silver on the little finger, "
            "provided the Moon is a functional benefic for the native's Lagna."
        ),
    }

    if cancelled:
        entry["exist"]              = False
        entry["CancellationReason"] = (
            "Kemadruma Dosha is cancelled (Kemadruma Bhanga) because: "
            + "; ".join(reasons)
            + ". This Bhanga itself confers resilience and inner strength."
        )
    else:
        entry["exist"] = True

    common.yogadoshas_dict[key] = entry


# ──────────────────────────────────────────────────────────────────────────────
# Sakata Dosha (independent Chandra-Guru check)
# ──────────────────────────────────────────────────────────────────────────────

def SakataDosha(charts):
    """
    Checks for Sakata Dosha: Jupiter placed in the 6th, 8th, or 12th house
    (a Dusthana) from the natal Moon.

    Source: BPHS, Phaladeepika (Chandra-Guru Yoga chapter)

    Cancellation (Bhanga) rules:
      1. Lagna Kendra Bhanga: Moon is in a Kendra (1, 4, 7, 10) from the Lagna.
      2. Jupiter in own sign (Sagittarius or Pisces) significantly mitigates results.

    Modifying factors:
      - Jupiter combust (conjunct Sun) => strengthens the dosha (more severe).
      - Jupiter retrograde            => partially neutralises the negative effects.

    Returns:
        True if Sakata Dosha is detected (active or cancelled), False otherwise.
    """
    key        = "SAKATA_D1"
    moon_house = charts["D1"]["planets"]["Moon"]["house-num"]
    ju_house   = charts["D1"]["planets"]["Jupiter"]["house-num"]

    # Formation check: Jupiter in 6th, 8th, or 12th from Moon
    diff_ju_from_moon = gen.housediff(moon_house, ju_house)
    if diff_ju_from_moon not in [6, 8, 12]:
        return False   # Sakata Dosha is not formed

    ju_sign   = charts["D1"]["planets"]["Jupiter"].get("sign", "")
    ju_retro  = charts["D1"]["planets"]["Jupiter"].get("retro", 0)
    ju_conjuncts = charts["D1"]["planets"]["Jupiter"].get("conjuncts", [])

    # ── Cancellation checks ────────────────────────────────────────────────────
    cancelled  = False
    mitigated  = False   # partial mitigation (not full cancellation)
    cancel_reasons  = []
    mitig_notes     = []

    # Rule 1: Lagna Kendra Bhanga -- Moon in house 1, 4, 7 or 10
    if moon_house in [1, 4, 7, 10]:
        cancelled = True
        cancel_reasons.append(
            f"Moon is in house {moon_house} (a Kendra from the Lagna), "
            "which nullifies Sakata Dosha per BPHS and Phaladeepika"
        )

    # Rule 2: Jupiter in own sign (Sagittarius or Pisces) -- significant mitigation
    if ju_sign in ["Sagittarius", "Pisces"]:
        mitigated = True
        mitig_notes.append(
            f"Jupiter is in its own sign ({ju_sign}), which significantly "
            "reduces the negative results of Sakata Dosha"
        )

    # ── Modifying factors ──────────────────────────────────────────────────────
    dosha_severity_notes = []

    # Jupiter combust (Sun conjunct Jupiter) => dosha is more severe
    if "Sun" in ju_conjuncts:
        dosha_severity_notes.append(
            "Jupiter is combust by the Sun, intensifying the fluctuations and "
            "instability described by Sakata Dosha"
        )

    # Jupiter retrograde => partial neutralisation / some recovery
    if ju_retro == 1:
        mitig_notes.append(
            "Jupiter is retrograde (Vakri), which in some classical traditions "
            "partially neutralises the negative effects, turning the 'wheel of fortune' "
            "toward a more stable upward trajectory over time"
        )

    # ── Compose Note text ─────────────────────────────────────────────────────
    note_parts = []
    note_parts.append(
        "Sakata Dosha is a Chandra-Guru Yoga where the planet of wisdom (Jupiter) "
        f"is in the {diff_ju_from_moon}th house from the Moon (house {moon_house}), "
        "a Dusthana placement. This creates a 'wheel-like' alternation between "
        "peaks of prosperity and troughs of difficulty throughout life."
    )
    if mitig_notes:
        note_parts.append("Mitigating factors: " + "; ".join(mitig_notes) + ".")
    if dosha_severity_notes:
        note_parts.append("Severity notes: " + "; ".join(dosha_severity_notes) + ".")

    note_text = " ".join(note_parts)

    # ── Build entry ────────────────────────────────────────────────────────────
    entry = {
        "name":             "Sakata Dosha",
        "type":             "Dosha",
        "relevant_planets": ["Mo", "Ju"],
        "Rule": (
            f"Jupiter (house {ju_house}) is placed in the {diff_ju_from_moon}th house "
            f"from the natal Moon (house {moon_house}), which is a Dusthana (6th, 8th "
            "or 12th). This specific Jupiter-Moon configuration forms Sakata Dosha as "
            "per BPHS and Phaladeepika."
        ),
        "Note": note_text,
        "Result": (
            "As per BPHS and Phaladeepika: 'Sakata' means 'cart' or 'wheel'. The native's "
            "fortunes oscillate like the turning of a wheel -- alternating between phases "
            "of prosperity and hardship. The native may suffer loss of wealth, social "
            "status, or family support, only to regain them later. There is often an "
            "internal psychological conflict regarding faith, wisdom, and belief systems, "
            "as Jupiter (Guru, the planet of wisdom) is estranged from the Moon (mind)."
        ),
        "Source": "Brihat Parashara Hora Shastra (BPHS), Phaladeepika",
        "Remedies": (
            "1. Offer prayers daily to Lord Dakshinamurthy or perform Guru Puja on Thursdays. "
            "2. Donate yellow items (turmeric, yellow lentils/daal, yellow cloth) to a "
            "Brahmin or temple on Thursdays. "
            "3. Chant the Guru (Jupiter) Beeja Mantra: 'Om Brim Brihaspataye Namah' "
            "108 times daily, especially on Thursdays. "
            "4. Wear a natural Yellow Sapphire (Pukhraj) or Yellow Topaz set in gold "
            "on the index finger of the right hand, only after consulting an astrologer "
            "to confirm Jupiter is a functional benefic for the Lagna."
        ),
    }

    if cancelled:
        entry["exist"]              = False
        entry["CancellationReason"] = (
            "Sakata Dosha is cancelled (Sakata Bhanga) because: "
            + "; ".join(cancel_reasons)
            + ". The native will not experience the characteristic fluctuations of Sakata Dosha."
        )
    else:
        entry["exist"] = True

    common.yogadoshas_dict[key] = entry
    return True



# ──────────────────────────────────────────────────────────────────────────────
# Adhi Yoga and Papa Adhi Dosha (Lagna-based and Chandra-based)
# Classical sources: BPHS, Phaladeepika, B.V. Raman "Three Hundred Important
# Combinations", Varahamihira's Brihat Jataka (Bhattotpala commentary).
#
# KEY RULES (corrected):
#  1. Formation: All three benefics (Mercury, Jupiter, Venus) must collectively
#     occupy the 6th, 7th, and 8th houses from the pivot. Fewer = Partial yoga.
#  2. Raman Grading: Based on how many of the PARTICIPATING benefics are STRONG
#     (exalted / own sign / Moolatrikona) -- NOT on how many are present.
#  3. Primary Bhanga for Adhi Yoga: Any natural malefic CO-OCCUPYING any of
#     the 6/7/8 houses from the pivot destroys the yoga's purity.
#  4. Additional weakeners for Adhi Yoga:
#       - Natural malefics ASPECTING any of the 6/7/8 houses
#       - Participating benefics DEBILITATED
#       - Venus or Mercury COMBUST by the Sun
#  5. Primary Bhanga for Papa Adhi Dosha: Any natural benefic CO-OCCUPYING
#     those same houses breaks the Dosha's full force.
#  6. Additional mitigators for Papa Adhi Dosha:
#       - Benefics ASPECTING the 6/7/8 houses
#       - Forming malefics DEBILITATED
#       - Strong Moon (for Chandra variant); benefic aspects on the Moon
# ──────────────────────────────────────────────────────────────────────────────

ADHI_BENEFICS        = ["Mercury", "Jupiter", "Venus"]
ADHI_BENEFIC_ABBREV  = {"Mercury": "Me", "Jupiter": "Ju", "Venus": "Ve"}
ADHI_MALEFICS        = ["Saturn", "Mars", "Rahu", "Ketu", "Sun"]
ADHI_MALEFIC_ABBREV  = {"Saturn": "Sa", "Mars": "Ma", "Rahu": "Ra", "Ketu": "Ke", "Sun": "Su"}
ADHI_NAT_MAL_SET     = {"Saturn", "Mars", "Rahu", "Ketu"}

# Full-name to 2-letter abbreviation for ALL planets (needed for relevant_planets in partial charts)
ADHI_ALL_ABBREV = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa", "Rahu": "Ra", "Ketu": "Ke",
}



def _adhi_raman_grade(strong_count):
    """
    Raman grading by how many PARTICIPATING benefics are STRONG (exalted/own).
    All 3 must be in the 6-7-8 zone; this function grades their quality only.
    """
    if strong_count == 3:
        return (
            "B.V. Raman (Three Hundred Important Combinations): All three benefics are "
            "in full strength -- the native occupies a supremely eminent station in life: "
            "a king, high commander, or national luminary of the highest order."
        )
    elif strong_count == 2:
        return (
            "B.V. Raman (Three Hundred Important Combinations): Two participating "
            "benefics are in full strength -- the native rises to the stature of a "
            "minister or senior administrator with great authority and public trust."
        )
    elif strong_count == 1:
        return (
            "B.V. Raman (Three Hundred Important Combinations): One participating "
            "benefic is in full strength -- the native becomes a distinguished leader "
            "in their chosen field."
        )
    else:
        return (
            "B.V. Raman (Three Hundred Important Combinations): All three benefics are "
            "present in the zone but devoid of exceptional strength. The Adhi Yoga is "
            "formed but its influence is feeble -- results come only in a reduced degree "
            "during the relevant Mahadasha/Antardasha periods."
        )


def _adhi_is_strong(charts, planet):
    """True if planet is exalted, Moolatrikona, or in own sign."""
    rel = charts["D1"]["planets"].get(planet, {}).get("house-rel", "")
    return any(k in rel for k in ("Exalted", "Exhalted", "Own", "Moolatrikona"))


def _adhi_is_debilitated(charts, planet):
    """True if planet is debilitated (Neecha)."""
    rel = charts["D1"]["planets"].get(planet, {}).get("house-rel", "")
    return "Debilitated" in rel or "Neecha" in rel


def _adhi_is_combust(charts, planet):
    """True if Mercury or Venus is combust by the Sun."""
    if planet not in ("Mercury", "Venus"):
        return False
    return "Sun" in charts["D1"]["planets"].get(planet, {}).get("conjuncts", [])


def _planets_aspecting_house(charts, target_house):
    """
    Returns list of planet names that cast a Vedic aspect on target_house.
    Standard Vedic aspects from a planet at house H:
      All planets : H + 6  (7th aspect)
      Mars        : H + 3, H + 7  (4th, 8th aspects)
      Jupiter     : H + 4, H + 8  (5th, 9th aspects)
      Saturn      : H + 2, H + 9  (3rd, 10th aspects)
    """
    aspecting = []
    for planet, pdata in charts["D1"]["planets"].items():
        ph = pdata.get("house-num")
        if ph is None:
            continue
        aspect_set = {gen.compute_nthsign(ph, 7)}
        if planet == "Mars":
            aspect_set |= {gen.compute_nthsign(ph, 4), gen.compute_nthsign(ph, 8)}
        elif planet == "Jupiter":
            aspect_set |= {gen.compute_nthsign(ph, 5), gen.compute_nthsign(ph, 9)}
        elif planet == "Saturn":
            aspect_set |= {gen.compute_nthsign(ph, 3), gen.compute_nthsign(ph, 10)}
        if target_house in aspect_set:
            aspecting.append(planet)
    return aspecting


def _adhi_bhanga(charts, yoga_house_set, base_house=1):
    """Bhanga for Adhi Yoga: any natural malefic co-occupying the yoga zone."""
    bhanga, reasons = False, []
    for p in ADHI_MALEFICS:
        h = charts["D1"]["planets"][p]["house-num"]
        if h in yoga_house_set:
            bhanga = True
            rel_h = gen.housediff(base_house, h) if base_house != 1 else h
            house_str = f"{rel_h}th house from Moon [House-{h}]" if base_house != 1 else f"house {h}"
            reasons.append(
                f"{p} (natural malefic) co-occupies {house_str} in the Adhi Yoga zone -- "
                "a malefic presence in the 6-7-8 axis destroys the yoga's purity (Bhanga)."
            )
    return bhanga, reasons


def _papa_bhanga(charts, dosha_house_set, base_house=1):
    """Bhanga for Papa Adhi Dosha: any natural benefic co-occupying the dosha zone."""
    bhanga, reasons = False, []
    for p in ADHI_BENEFICS:
        h = charts["D1"]["planets"][p]["house-num"]
        if h in dosha_house_set:
            bhanga = True
            rel_h = gen.housediff(base_house, h) if base_house != 1 else h
            house_str = f"{rel_h}th house from Moon [House-{h}]" if base_house != 1 else f"house {h}"
            reasons.append(
                f"{p} (natural benefic) co-occupies {house_str} in the Papa Adhi zone -- "
                "a benefic presence neutralises the full force of the Dosha (Bhanga)."
            )
    return bhanga, reasons


def _adhi_weakness_notes(charts, forming_planets, yoga_house_set):
    """Collect combustion, debilitation, and malefic-aspect weakening notes."""
    notes = []
    for p in forming_planets:
        if _adhi_is_combust(charts, p):
            notes.append(
                f"{p} is combust (Asta) by the Sun -- severely curtails its "
                "capacity to deliver Adhi Yoga benefits."
            )
        if _adhi_is_debilitated(charts, p):
            notes.append(
                f"{p} is debilitated (Neecha) -- significantly weakens its contribution "
                "unless Neechabhanga applies."
            )
    for h in sorted(yoga_house_set):
        aspectors = _planets_aspecting_house(charts, h)
        mal_asp = [a for a in aspectors if a in ADHI_NAT_MAL_SET]
        if mal_asp:
            notes.append(
                f"Natural malefic(s) {', '.join(mal_asp)} aspect house {h} -- "
                "malefic aspects on the yoga zone weaken Adhi Yoga."
            )
    return notes


def _papa_mitigation_notes(charts, forming_malefics, dosha_house_set):
    """Collect debilitation and benefic-aspect mitigation notes for Papa Adhi Dosha."""
    notes = []
    for p in forming_malefics:
        if _adhi_is_debilitated(charts, p):
            notes.append(
                f"{p} is debilitated (Neecha) -- a debilitated malefic exerts reduced "
                "force, partially easing the Dosha."
            )
    for h in sorted(dosha_house_set):
        aspectors = _planets_aspecting_house(charts, h)
        ben_asp = [a for a in aspectors if a in ADHI_BENEFICS]
        if ben_asp:
            notes.append(
                f"Benefic(s) {', '.join(ben_asp)} aspect house {h} -- benefic aspects "
                "on the Dosha zone mitigate its malefic effects."
            )
    return notes


# -- 1. Lagna Adhi Yoga -------------------------------------------------------

def LagnaAdhiYoga(charts):
    """
    Detects Lagna Adhi Yoga (full or partial).
    ALL three benefics must occupy houses 6, 7, 8 from the Lagna for full yoga.
    Fewer = partial yoga at reduced capacity.
    Primary Bhanga: any natural malefic co-occupying those houses.
    Raman grading: by count of STRONG participants, not by presence count.
    """
    key         = "LAGNA_ADHI_YOGA_D1"
    yoga_houses = {6, 7, 8}

    in_zone = {p: charts["D1"]["planets"][p]["house-num"]
               for p in ADHI_BENEFICS
               if charts["D1"]["planets"][p]["house-num"] in yoga_houses}

    if len(in_zone) < 3:
        return False

    forming  = list(in_zone.keys())
    strong   = [p for p in forming if _adhi_is_strong(charts, p)]

    bhanga, bhanga_r = _adhi_bhanga(charts, yoga_houses)
    weak_notes       = _adhi_weakness_notes(charts, forming, yoga_houses)

    # Build comprehensive relevant_planets:
    #  - benefics IN the zone
    #  - any malefic co-occupying (Bhanga planets)
    #  - any planet aspecting the yoga houses
    relevant_set = set(forming)
    for p in ADHI_MALEFICS:
        if charts["D1"]["planets"][p]["house-num"] in yoga_houses:
            relevant_set.add(p)
    for h in yoga_houses:
        for p in _planets_aspecting_house(charts, h):
            relevant_set.add(p)
    abbrevs = sorted({ADHI_ALL_ABBREV[p] for p in relevant_set if p in ADHI_ALL_ABBREV})

    hmap = {}
    for p, h in in_zone.items():
        hmap.setdefault(h, []).append(p)
    
    house_desc_parts = []
    for h, ps in sorted(hmap.items()):
        house_desc_parts.append(f"the {h}th house contains {' and '.join(ps)}")
    house_desc = ". ".join(house_desc_parts)

    note = []
    note.append(
        f"Lagna is the 1st house. {house_desc.capitalize()}. "
        f"This satisfies the condition for formation of this yoga."
    )
    note.append(
        "Shubha Kartari Secret: Benefics in the 6th and 8th hem the 7th house "
        "(partnerships & public life) in pure benefic energy, guaranteeing success."
    )
    if strong:
        note.append(
            f"Strong Benefics: {', '.join(strong)} are exalted/own sign -- amplifies "
            "the yoga toward a supreme Raja Yoga."
        )
    if weak_notes:
        note.append("Weakening Factors: " + "; ".join(weak_notes))

    entry = {
        "name":             "Lagna Adhi Yoga",
        "type":             "Yoga",
        "exist":            not bhanga,
        "relevant_planets": abbrevs,
        "Rule": (
            "All three natural benefics--Mercury, Jupiter, Venus--must collectively "
            "occupy the 6th, 7th, and 8th houses from the Lagna for Adhi Yoga. "
            "Primary Bhanga: any natural malefic co-occupying those houses. "
            "Additional weakeners: malefics aspecting those houses; "
            "debilitated or combust participating benefics. "
            f"Benefics found in zone: {', '.join(forming)}."
        ),
        "Note":             "\n".join(note),
        "Result": (
            "As per BPHS and B.V. Raman's Three Hundred Important Combinations:\n"
            "The native will be polite and trustworthy, live a happy and affluent life "
            "surrounded by luxuries, inflict defeats on enemies, and enjoy good health "
            "and longevity. Raman equates Adhi Yoga to a Raja Yoga or its equivalent.\n"
            "The native may rise to the position of king, minister, or commander."
        ),
        "Source":             "BPHS Ch.36, B.V. Raman - 300 Important Combinations (#38-39), Phaladeepika Ch.6",
        "CancellationReason": " | ".join(bhanga_r) if bhanga else "",
        "Remedies":           "",
    }
    if bhanga:
        entry["CancellationReason"] = (
            " | ".join(bhanga_r) + "\nResults will be obstructed and require immense effort to manifest."
        )
    common.yogadoshas_dict[key] = entry
    return True


# -- 2. Chandra Adhi Yoga -----------------------------------------------------

def ChandraAdhiYoga(charts):
    """
    Detects Chandra Adhi Yoga (full or partial).
    All three benefics must collectively occupy the 6th, 7th, 8th from the Moon.
    Same Bhanga and Raman-grading rules as Lagna Adhi Yoga.
    Moon's own strength/affliction further modifies the yoga's potency.
    """
    key        = "CHANDRA_ADHI_YOGA_D1"
    moon_house = charts["D1"]["planets"]["Moon"]["house-num"]

    yoga_houses = {
        gen.compute_nthsign(moon_house, 6),
        gen.compute_nthsign(moon_house, 7),
        gen.compute_nthsign(moon_house, 8),
    }

    in_zone = {p: charts["D1"]["planets"][p]["house-num"]
               for p in ADHI_BENEFICS
               if charts["D1"]["planets"][p]["house-num"] in yoga_houses}

    if len(in_zone) < 3:
        return False

    forming  = list(in_zone.keys())
    is_full  = (len(forming) == 3)
    strong   = [p for p in forming if _adhi_is_strong(charts, p)]

    bhanga, bhanga_r = _adhi_bhanga(charts, yoga_houses, moon_house)
    weak_notes       = _adhi_weakness_notes(charts, forming, yoga_houses)

    # Build comprehensive relevant_planets:
    #  - Moon (pivot) + benefics IN the zone
    #  - any malefic co-occupying (Bhanga planets)
    #  - any planet aspecting the yoga houses
    relevant_set = {"Moon"} | set(forming)
    for p in ADHI_MALEFICS:
        if charts["D1"]["planets"][p]["house-num"] in yoga_houses:
            relevant_set.add(p)
    for h in yoga_houses:
        for p in _planets_aspecting_house(charts, h):
            relevant_set.add(p)
    abbrevs = sorted({ADHI_ALL_ABBREV[p] for p in relevant_set if p in ADHI_ALL_ABBREV})

    moon_rel     = charts["D1"]["planets"]["Moon"].get("house-rel", "")
    moon_conj    = charts["D1"]["planets"]["Moon"].get("conjuncts", [])
    moon_asp_by  = charts["D1"]["planets"]["Moon"].get("Aspected-by", [])
    moon_strong  = any(k in moon_rel for k in ("Exalted", "Exhalted", "Own"))
    moon_afflict = bool(ADHI_NAT_MAL_SET.intersection(set(moon_conj) | set(moon_asp_by)))

    hmap = {}
    for p, h in in_zone.items():
        hmap.setdefault(h, []).append(p)
        
    house_desc_parts = []
    for h, ps in sorted(hmap.items()):
        rel_h = gen.housediff(moon_house, h)
        house_desc_parts.append(f"the {rel_h}th house from Moon [House-{h}] contains {' and '.join(ps)}")
    house_desc = ". ".join(house_desc_parts)

    note = []
    note.append(
        f"Moon is in {moon_house}th house. {house_desc.capitalize()}. "
        f"This satisfies the condition for formation of this yoga."
    )
    note.append(
        "Dasha Timing: Greatest rise in authority and wealth during Mahadashas/"
        "Antardashas of Mercury, Jupiter, or Venus forming this yoga."
    )
    if moon_strong:
        note.append(
            "Strong Moon: Exalted/own sign (Purnima quality) -- powerfully anchors the "
            "yoga and multiplies its benefits."
        )
    if moon_afflict:
        note.append(
            "Afflicted Moon: Conjunct/aspected by malefics (Amavasya quality) -- drastically "
            "weakens the yoga's psychological and material foundation."
        )
    if strong:
        note.append(f"Strong Benefics: {', '.join(strong)} (exalted/own sign).")
    if weak_notes:
        note.append("Weakening Factors: " + "; ".join(weak_notes))

    entry = {
        "name":             "Chandra Adhi Yoga",
        "type":             "Yoga",
        "exist":            not bhanga,
        "relevant_planets": abbrevs,
        "Rule": (
            "All three natural benefics--Mercury, Jupiter, Venus--must collectively "
            "occupy the 6th, 7th, and 8th houses from the natal Moon for the yoga. "
            "Primary Bhanga: any natural malefic co-occupying those houses. "
            "Additional weakeners: malefics aspecting those houses; debilitated or "
            "combust benefics; severely afflicted or dark Moon. "
            f"Moon in house {moon_house}. Benefics in zone: {', '.join(forming)}."
        ),

        "Note":             "\n".join(note),
        "Result": (
            "As per BPHS and B.V. Raman's Three Hundred Important Combinations:\n"
            "The native possesses an extremely polite and trustworthy demeanor. "
            "Psychological peace translates to material affluence, luxury, resilience "
            "during crises, longevity, respect, authority, and social standing."
        ),
        "Source":             "BPHS Ch.36, B.V. Raman - 300 Important Combinations, Phaladeepika Ch.6",
        "CancellationReason": " | ".join(bhanga_r) if bhanga else "",
        "Remedies":           "",
    }
    common.yogadoshas_dict[key] = entry
    return True


# -- 3. Lagna Papa Adhi Dosha -------------------------------------------------

def LagnaPapaAdhiDosha(charts):
    """
    Detects Lagna Papa Adhi Dosha: natural malefics in the 6th, 7th, 8th from
    the Lagna -- malefic reversal of Adhi Yoga.
    Primary Bhanga: any natural benefic also co-occupying those houses.
    Mitigation: benefic aspects on those houses; debilitated malefics.
    Severity worsened: retrograde malefics.
    """
    key          = "LAGNA_PAPA_ADHI_DOSHA_D1"
    dosha_houses = {6, 7, 8}

    in_zone = {p: charts["D1"]["planets"][p]["house-num"]
               for p in ADHI_MALEFICS
               if charts["D1"]["planets"][p]["house-num"] in dosha_houses}

    if len(in_zone) < 3:
        return False

    forming = list(in_zone.keys())

    bhanga, bhanga_r = _papa_bhanga(charts, dosha_houses)
    mitig_notes      = _papa_mitigation_notes(charts, forming, dosha_houses)
    retro            = [p for p in forming
                        if charts["D1"]["planets"].get(p, {}).get("retro", 0) == 1]

    # Build comprehensive relevant_planets:
    #  - malefics IN the zone
    #  - any benefic co-occupying (Bhanga planets)
    #  - any planet aspecting the dosha houses
    relevant_set = set(forming)
    for p in ADHI_BENEFICS:
        if charts["D1"]["planets"][p]["house-num"] in dosha_houses:
            relevant_set.add(p)
    for h in dosha_houses:
        for p in _planets_aspecting_house(charts, h):
            relevant_set.add(p)
    abbrevs = sorted({ADHI_ALL_ABBREV[p] for p in relevant_set if p in ADHI_ALL_ABBREV})

    hmap = {}
    for p, h in in_zone.items():
        hmap.setdefault(h, []).append(p)
        
    house_desc_parts = []
    for h, ps in sorted(hmap.items()):
        house_desc_parts.append(f"the {h}th house contains {' and '.join(ps)}")
    house_desc = ". ".join(house_desc_parts)

    note = [
        "Classical Note: Varahamihira did not explicitly classify this as a distinct yoga; "
        "however Bhattotpala--his erudite commentator--confirmed Papadhi Yoga, tying it to "
        "life's bitterest struggles.",
        f"Lagna is the 1st house. {house_desc.capitalize()}. This satisfies the condition for formation of this Dosha.",
        "Papa Kartari: The 7th house (partnerships, public life) is hemmed between malefics "
        "in the adjacent 6th and 8th -- restricting energy, creating persistent obstacles, "
        "and inflicting constant external pressure."
    ]
    if retro:
        note.append(
            f"Severity Amplifier: {', '.join(retro)} are retrograde -- intensifying "
            "the struggles and opposition described by this Dosha."
        )
    if mitig_notes:
        note.append("Mitigating Factors: " + "; ".join(mitig_notes))

    entry = {
        "name":             "Lagna Papa Adhi Dosha",
        "type":             "Dosha",
        "exist":            not bhanga,
        "relevant_planets": abbrevs,
        "Rule": (
            "At least three natural malefics--Saturn, Mars, Rahu, Ketu, or the Sun--occupy the 6th, 7th, "
            "and/or 8th houses from the Lagna. Primary Bhanga: any natural benefic "
            "(Mercury, Jupiter, Venus) co-occupying those same houses. "
            "Mitigation: benefics aspecting those houses; debilitated malefics. "
            f"Forming malefics: {', '.join(forming)}."
        ),
        "Note":   "\n".join(note),
        "Result": (
            "As per Bhattotpala/Raman synthesis:\n"
            "Chronic struggles, powerful enemies, marital distress, and constant external pressure. "
            "The 7th house is in Papa Kartari, creating persistent obstacles in public life and partnerships.\n"
            "If the forming malefics are also functional benefics for the Ascendant, "
            "the negative impact is partially reduced."
        ),
        "Source": (
            "B.V. Raman - Three Hundred Important Combinations, "
            "Bhattotpala commentary on Brihat Jataka, BPHS"
        ),
        "CancellationReason": " | ".join(bhanga_r) + "\nStruggles will occur but are significantly offset by benefic co-presence." if bhanga else "",
        "Remedies": (
            "1. Saturn: Chant 'Om Sham Shanaishcharaya Namah' 108 times on Saturdays; "
            "donate black sesame seeds and iron to a temple or needy on Saturdays.\n"
            "2. Mars: Chant the Hanuman Chalisa daily; donate red lentils on Tuesdays; "
            "fast on Tuesdays for 21 consecutive weeks.\n"
            "3. Rahu: Chant 'Om Raam Rahave Namah' 108 times; offer blue/black flowers "
            "at a Durga temple on Saturdays.\n"
            "4. Ketu: Chant 'Om Kem Ketave Namah' 108 times; donate multi-colored cloth "
            "and camphor on Saturdays.\n"
            "5. Sun: Offer Arghya (water) to the rising Sun every morning; chant "
            "'Om Suryaya Namah' 108 times; donate wheat and jaggery on Sundays.\n"
            "6. General: Worship Lord Hanuman daily; visit a Shiva temple on Mondays; "
            "strengthen functional benefics through appropriate gemstones after consulting "
            "an experienced astrologer.\n"
            "7. Recite the Navagraha Stotram daily to propitiate all nine planets."
        ),
    }
    common.yogadoshas_dict[key] = entry
    common.yogadoshas_dict[key] = entry
    return True


# -- 4. Chandra Papa Adhi Dosha -----------------------------------------------

def ChandraPapaAdhiDosha(charts):
    """
    Detects Chandra Papa Adhi Dosha: natural malefics in the 6th, 7th, 8th
    from the natal Moon -- Mental Papa Kartari around the 7th from Moon.
    Primary Bhanga: any natural benefic co-occupying those houses.
    Mitigation: strong Moon; benefic aspects on those houses or on the Moon itself.
    Severity worsened: retrograde malefics; afflicted/dark Moon.
    """
    key        = "CHANDRA_PAPA_ADHI_DOSHA_D1"
    moon_house = charts["D1"]["planets"]["Moon"]["house-num"]

    dosha_houses = {
        gen.compute_nthsign(moon_house, 6),
        gen.compute_nthsign(moon_house, 7),
        gen.compute_nthsign(moon_house, 8),
    }

    in_zone = {p: charts["D1"]["planets"][p]["house-num"]
               for p in ADHI_MALEFICS
               if charts["D1"]["planets"][p]["house-num"] in dosha_houses}

    if len(in_zone) < 3:
        return False

    forming = list(in_zone.keys())

    bhanga, bhanga_r = _papa_bhanga(charts, dosha_houses)
    mitig_notes      = _papa_mitigation_notes(charts, forming, dosha_houses)
    retro            = [p for p in forming
                        if charts["D1"]["planets"].get(p, {}).get("retro", 0) == 1]

    # Build comprehensive relevant_planets:
    #  - Moon (pivot) + malefics IN the zone
    #  - any benefic co-occupying (Bhanga planets)
    #  - any planet aspecting the dosha houses
    relevant_set = {"Moon"} | set(forming)
    for p in ADHI_BENEFICS:
        if charts["D1"]["planets"][p]["house-num"] in dosha_houses:
            relevant_set.add(p)
    for h in dosha_houses:
        for p in _planets_aspecting_house(charts, h):
            relevant_set.add(p)
    abbrevs = sorted({ADHI_ALL_ABBREV[p] for p in relevant_set if p in ADHI_ALL_ABBREV})

    moon_rel     = charts["D1"]["planets"]["Moon"].get("house-rel", "")
    moon_conj    = charts["D1"]["planets"]["Moon"].get("conjuncts", [])
    moon_asp_by  = charts["D1"]["planets"]["Moon"].get("Aspected-by", [])
    moon_strong  = any(k in moon_rel for k in ("Exalted", "Exhalted", "Own"))
    moon_afflict = bool(ADHI_NAT_MAL_SET.intersection(set(moon_conj) | set(moon_asp_by)))
    ben_asp_moon = bool(set(ADHI_BENEFICS).intersection(set(moon_asp_by)))

    hmap = {}
    for p, h in in_zone.items():
        hmap.setdefault(h, []).append(p)
        
    house_desc_parts = []
    for h, ps in sorted(hmap.items()):
        rel_h = gen.housediff(moon_house, h)
        house_desc_parts.append(f"the {rel_h}th house from Moon [House-{h}] contains {' and '.join(ps)}")
    house_desc = ". ".join(house_desc_parts)

    note = [
        f"Moon is in {moon_house}th house. {house_desc.capitalize()}. This satisfies the condition for formation of this Dosha.",
        "Mental Papa Kartari: The 7th from the Moon (desires, relational interaction) "
        "is hemmed between malefics -- causing mental stress, fear of rivals, and a "
        "feeling of being trapped in relationships and desires.",
        "Aligning with Bhattotpala's view: this creates a mental "
        "landscape dominated by psychological unrest and fear of opposition."
    ]
    if moon_strong:
        note.append(
            "Mitigating: Moon is exalted/own sign (Purnima quality) -- gives the mind "
            "inherent resilience to withstand malefic pressures."
        )
    if moon_afflict:
        note.append(
            "Severity Amplifier: Moon itself is conjunct/aspected by malefics "
            "(Amavasya quality) -- intensifies this Dosha's psychological impact."
        )
    if ben_asp_moon:
        note.append(
            "Benefic Aspect: Moon receives benefic aspects -- partial psychological shelter and "
            "mitigation of the emotional pressure."
        )
    if retro:
        note.append(
            f"Retrograde Malefics ({', '.join(retro)}): Intensify internal pressure."
        )
    if mitig_notes:
        note.append("Mitigating Factors: " + "; ".join(mitig_notes))

    entry = {
        "name":             "Chandra Papa Adhi Dosha",
        "type":             "Dosha",
        "exist":            not bhanga,
        "relevant_planets": abbrevs,
        "Rule": (
            "At least three natural malefics--Saturn, Mars, Rahu, Ketu, or the Sun--occupy the 6th, 7th, "
            "and/or 8th houses from the natal Moon. Primary Bhanga: any natural benefic "
            "co-occupying those houses. Mitigation: benefic aspects on those houses; "
            "strong Moon; benefic aspects on the Moon itself. "
            f"Moon in house {moon_house}. Forming malefics: {', '.join(forming)}."
        ),
        "Note":   "\n".join(note),

        "Result": (
            "As per Bhattotpala/Raman synthesis:\n"
            "Causes chronic mental struggles, fear of enemies, immense marital distress, and emotional instability.\n"
            "The native's mental landscape is dominated by fear of rivals and psychological unrest. "
            "The 7th from the Moon suffers restricted energy -- a perpetual feeling of "
            "being hemmed in by external opposition in relational matters."
        ),
        "Source": (
            "B.V. Raman - Three Hundred Important Combinations, "
            "Bhattotpala commentary on Brihat Jataka, BPHS"
        ),
        "CancellationReason": " | ".join(bhanga_r) + "\nMental struggles will occur but are significantly offset by benefic presence." if bhanga else "",
        "Remedies": (
            "1. Moon (pivot): Chant 'Om Som Somaya Namah' 108 times every Monday; "
            "offer raw milk, water, and white flowers to a Shivalinga on Mondays.\n"
            "2. Saturn: Chant 'Om Sham Shanaishcharaya Namah' 108 times; donate black "
            "sesame seeds and iron on Saturdays.\n"
            "3. Mars: Chant the Hanuman Chalisa daily; fast on Tuesdays; donate red lentils.\n"
            "4. Rahu: Chant 'Om Raam Rahave Namah' 108 times; offer blue/black flowers.\n"
            "5. Ketu: Chant 'Om Kem Ketave Namah' 108 times; donate camphor and cloth.\n"
            "6. Sun: Offer Arghya to the rising Sun every morning; chant 'Om Suryaya Namah'.\n"
            "7. Wear a high-quality natural Pearl (Moti) in silver on the little finger "
            "ONLY if the Moon is a functional benefic for the Lagna (consult an astrologer).\n"
            "8. Practise daily meditation and mindfulness to strengthen the mind.\n"
            "9. Recite the Chandra Kavacham weekly for mental protection."
        ),
    }
    common.yogadoshas_dict[key] = entry
    return True

