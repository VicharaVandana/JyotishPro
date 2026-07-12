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
        "name":             "Sunapha Yoga (D1)",
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
        "name":             "Anapha Yoga (D1)",
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
        "name":             "Durdhara Yoga (D1)",
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
        "name":             "Kemadruma Dosha (D1)",
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
        "name":             "Sakata Dosha (D1)",
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
