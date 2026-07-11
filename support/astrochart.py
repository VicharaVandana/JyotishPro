import jyotichart as chart
import support.generic as gen
import support.display_settings_manager as ds_manager
import os
import support.globalvariables as gvar
import calendar

# ---------------------------------------------------------------------------
# Image sub-folder paths (relative to JyotishPro working directory)
# ---------------------------------------------------------------------------
BIRTHCHART_IMG_DIR  = "./images/birthcharts/"
MIXEDCHART_IMG_DIR  = "./images/mixedcharts/"

# ---------------------------------------------------------------------------
# Helper: post-process SVG so that QSvgRenderer renders fonts correctly.
# QSvgRenderer ignores <style> CSS blocks; we inline the font attributes.
# ---------------------------------------------------------------------------
def fix_svg_styling_for_qsvgrenderer(svg_path):
    if not os.path.exists(svg_path):
        return
    
    with open(svg_path, 'r', encoding='utf-16') as f:
        content = f.read()
    
    # Standard North/South chart classes
    content = content.replace('class="sign-num"',    'font-size="22px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="planet"',      'font-size="20px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="aspect"',      'font-size="22px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="chart-details"','font-size="14px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="num-value"',   'font-size="22px" font-weight="bold" font-family="sans-serif"')
    
    # Mixed/Transit chart specific classes
    content = content.replace('class="natal-planet"',   'font-size="20px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="transit-planet"', 'font-size="20px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="natal-aspect"',   'font-size="22px" font-weight="bold" font-family="sans-serif"')
    content = content.replace('class="transit-aspect"', 'font-size="22px" font-weight="bold" font-family="sans-serif"')
    
    # Fix Retrograde underlines for QSvgRenderer
    import re
    pattern = r'<text([^>]*text-decoration="underline"[^>]*)>([^<]+)</text>'
    
    def replacer(match):
        tag_attrs = match.group(1)
        text_content = match.group(2)
        
        x_match = re.search(r'x="([\d\.]+)"', tag_attrs)
        y_match = re.search(r'y="([\d\.]+)"', tag_attrs)
        fill_match = re.search(r'fill="([^"]+)"', tag_attrs)
        
        if x_match and y_match:
            x_val = float(x_match.group(1))
            y_val = float(y_match.group(1))
            fill_color = fill_match.group(1) if fill_match else "black"
            
            new_attrs = tag_attrs.replace('text-decoration="underline"', '')
            new_text = f'<text{new_attrs}>{text_content}</text>'
            
            width = len(text_content) * 12
            x1 = x_val
            y1 = y_val + 4
            x2 = x_val + width
            y2 = y_val + 4
            
            new_line = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{fill_color}" stroke-width="2" />'
            return new_text + new_line
            
        return match.group(0)

    content = re.sub(pattern, replacer, content)

    with open(svg_path, 'w', encoding='utf-16') as f:
        f.write(content)

# ---------------------------------------------------------------------------
# Division signification lookup
# ---------------------------------------------------------------------------
def get_division_signification(division):
    division_map = {
        "D1":  "Rashi chart - Overview of individual's life, personality, and overall life",
        "D2":  "Hora chart - Wealth, financial prosperity, and stability",
        "D3":  "Drekkana chart - Siblings, talents, and challenges",
        "D4":  "Chaturthamsa chart - Home, property, family, and prosperity",
        "D7":  "Sapthamsa chart - Children, progeny, and relationships with offspring",
        "D9":  "Navamsa chart - Spouse, marriage, inner self, and post-marriage growth",
        "D10": "Dasamsa chart - Profession, career, achievements, and social standing",
        "D12": "Dwadasamsa chart - Parents, their influence, and relationships",
        "D16": "Shodasamsa chart - Vehicles, luxuries, comfort, and discomfort",
        "D20": "Vimsamsa chart - Religious inclinations, spirituality, and devotion",
        "D24": "Chaturvimsamsa chart - Education, knowledge, and intellectual pursuits",
        "D27": "Saptavimsamsa chart - Innate strength, talents, and inherent nature",
        "D30": "Trimsamsa chart - Obstacles, challenges, karmic influences, and subconscious aspects",
        "D40": "Khavedamsa chart - Life events, mother's side, and ancestral connections",
        "D45": "Akshavedamsa chart - Life overview, father's side, and ancestral connections",
        "D60": "Shastyamasa chart - Karmic influences, past lives, and soul evolution"
    }
    return division_map.get(division, "Unknown division chart")

# ---------------------------------------------------------------------------
# Internal helper: populate all 9 planets onto a chart object
# ---------------------------------------------------------------------------
def _populate_planets(mychart, astrodata, div, firsthouse):
    mychart.set_ascendantsign(firsthouse)
    for planet_key in [
        chart.SUN, chart.MOON, chart.MARS, chart.MERCURY,
        chart.JUPITER, chart.VENUS, chart.SATURN, chart.RAHU, chart.KETU
    ]:
        symbol = chart.get_planet_symbol(planet_key, mychart.language)
        planet_name = {
            chart.SUN: "Sun", chart.MOON: "Moon", chart.MARS: "Mars",
            chart.MERCURY: "Mercury", chart.JUPITER: "Jupiter",
            chart.VENUS: "Venus", chart.SATURN: "Saturn",
            chart.RAHU: "Rahu", chart.KETU: "Ketu"
        }[planet_key]
        mychart.delete_planet(planet_key)
        mychart.add_planet(
            planet_key, symbol,
            gen.get_house_number(firsthouse, astrodata[div]["planets"][planet_name]["sign"]),
            colour=planet_colourstrategy_dispositorRelation(astrodata[div]["planets"][planet_name]),
            retrograde=astrodata[div]["planets"][planet_name]["retro"]
        )

# ---------------------------------------------------------------------------
# Planet colour strategy
# ---------------------------------------------------------------------------
def planet_colourstrategy_dispositorRelation(planetdata):
    rel = planetdata["house-rel"]
    if rel == "Exhalted / Uchha":
        return "gold"
    elif rel == "Own sign / Swa rashi":
        return "lime"
    elif rel == "Friends sign / Mitra rashi":
        return "sky blue"
    elif rel == "Neutral sign / Sama rashi":
        return "white"
    elif rel == "Enemy sign / Shatru rashi":
        return "magenta"
    elif rel == "Debilitated / Neecha":
        return "red"
    return "yellow"

# ---------------------------------------------------------------------------
# Draw a single-divisional birth chart
# ---------------------------------------------------------------------------

def _apply_display_settings(chart_obj, chart_style, aspect_val=False, is_outer_chart=False):
    settings = ds_manager.get_settings()
    
    if is_outer_chart:
        bg_col = settings.get("chart_outer_background_colour", "black")
    else:
        bg_col = settings.get("chart_background_colour", "black")
        
    houses_list = [bg_col] * 12

    if chart_style == "south":
        chart_obj.updatechartcfg(
            aspect=aspect_val,
            clr_background=bg_col,
            clr_houses=houses_list,
            clr_outbox=settings.get("chart_outerbox_colour", "red"),
            clr_inbox=settings.get("chart_innerbox_colour", "red"),
            clr_line=settings.get("chart_line_colour", "yellow"),
            clr_Asc=settings.get("chart_sign_colour", "pink")
        )
    else:
        chart_obj.updatechartcfg(
            aspect=aspect_val,
            clr_background=bg_col,
            clr_houses=houses_list,
            clr_outbox=settings.get("chart_outerbox_colour", "red"),
            clr_line=settings.get("chart_line_colour", "yellow"),
            clr_sign=settings.get("chart_sign_colour", "pink")
        )

# ---------------------------------------------------------------------------
def plot_astrochart(chart_loc, chart_name, astrodata, div,
                    firsthousesign="None", IsAspectNeeded=False,
                    language="english", chart_style="north"):
    firsthouse = astrodata[div]["ascendant"]["sign"] if firsthousesign == "None" else firsthousesign

    # Select chart class based on style
    name = getattr(gvar, 'ufuserdata', {}).get("name", "User")
    if not name:
        name = "User"
        
    if chart_style == "south":
        mychart = chart.SouthChart(div, name, IsFullChart=True)
    else:
        mychart = chart.NorthChart(div, name, IsFullChart=True)

    # Set language
    mychart.language = language

    if chart_style == "south":
        dob_dict = getattr(gvar, 'ufuserdata', {}).get("DOB", {})
        if dob_dict:
            try:
                day = str(dob_dict.get("day", "")).zfill(2)
                month_num = int(dob_dict.get("month", "1"))
                month_name = calendar.month_name[month_num]
                year = dob_dict.get("year", "")
                dob_str = f"{day} {month_name} {year}"
                
                tob_dict = getattr(gvar, 'ufuserdata', {}).get("TOB", {})
                hour = str(tob_dict.get("hour", "0")).zfill(2)
                minute = str(tob_dict.get("min", "0")).zfill(2)
                tob_str = f"{hour}:{minute}"
                
                pob_str = getattr(gvar, 'ufuserdata', {}).get("POB", {}).get("name", "")
                mychart.set_birth_details(dob_str, tob_str, pob_str)
            except Exception as e:
                print(f"Error setting birth details: {e}")

    _populate_planets(mychart, astrodata, div, firsthouse)
    _apply_display_settings(mychart, chart_style, aspect_val=IsAspectNeeded)
    mychart.draw(chart_loc, chart_name)

    svg_file = os.path.join(chart_loc, f"{chart_name}.svg")
    fix_svg_styling_for_qsvgrenderer(svg_file)

    mychart = None
    return

# ---------------------------------------------------------------------------
# Draw a mixed (inner natal + outer transit/natal) chart
# ---------------------------------------------------------------------------
def plot_astroMixedChart(chart_loc, chart_name,
                         inner_astrodata, inner_div,
                         outer_astrodata, outer_div,
                         firsthousesign="None",
                         IsInnerAspectNeeded=False,
                         IsOuterAspectNeeded=False,
                         language="english",
                         chart_style="north"):
    firsthouse = inner_astrodata[inner_div]["ascendant"]["sign"] if firsthousesign == "None" else firsthousesign

    # Select chart classes based on style
    if chart_style == "south":
        InnerChartClass  = chart.SouthChart
        OuterChartClass  = chart.SouthTransitChart
    else:
        InnerChartClass  = chart.NorthChart
        OuterChartClass  = chart.NorthTransitChart

    name = getattr(gvar, 'ufuserdata', {}).get("name", "User")
    if not name:
        name = "User"

    # --- Prepare the inner chart ---
    innerchart = InnerChartClass(inner_div, name, IsFullChart=True)
    innerchart.language = language

    if chart_style == "south":
        dob_dict = getattr(gvar, 'ufuserdata', {}).get("DOB", {})
        if dob_dict:
            try:
                day = str(dob_dict.get("day", "")).zfill(2)
                month_num = int(dob_dict.get("month", "1"))
                month_name = calendar.month_name[month_num]
                year = dob_dict.get("year", "")
                dob_str = f"{day} {month_name} {year}"
                
                tob_dict = getattr(gvar, 'ufuserdata', {}).get("TOB", {})
                hour = str(tob_dict.get("hour", "0")).zfill(2)
                minute = str(tob_dict.get("min", "0")).zfill(2)
                tob_str = f"{hour}:{minute}"
                
                pob_str = getattr(gvar, 'ufuserdata', {}).get("POB", {}).get("name", "")
                innerchart.set_birth_details(dob_str, tob_str, pob_str)
            except Exception as e:
                print(f"Error setting inner birth details: {e}")
    _populate_planets(innerchart, inner_astrodata, inner_div, firsthouse)
    _apply_display_settings(innerchart, chart_style, aspect_val=IsInnerAspectNeeded)

    # --- Prepare the outer chart ---
    outerchart = OuterChartClass(outer_div, "Transit", innerchart)
    outerchart.language = language

    if chart_style == "south":
        dob_dict = getattr(gvar, 'transit_userdata', {}).get("DOB", {})
        if not dob_dict:
            dob_dict = getattr(gvar, 'ufuserdata', {}).get("DOB", {})  # fallback if it's not transit
        
        if dob_dict:
            try:
                day = str(dob_dict.get("day", "")).zfill(2)
                month_num = int(dob_dict.get("month", "1"))
                month_name = calendar.month_name[month_num][:3] # Short month name for transit
                year = dob_dict.get("year", "")
                date_str = f"{day} {month_name} {year}"
                
                tob_dict = getattr(gvar, 'transit_userdata', {}).get("TOB", {})
                if not tob_dict:
                    tob_dict = getattr(gvar, 'ufuserdata', {}).get("TOB", {})
                hour = str(tob_dict.get("hour", "0")).zfill(2)
                minute = str(tob_dict.get("min", "0")).zfill(2)
                time_str = f"{hour}:{minute}"
                
                outerchart.set_transit_details(date_str, time_str)
            except Exception as e:
                print(f"Error setting transit details: {e}")

    # Populate outer planets
    for planet_key in [
        chart.SUN, chart.MOON, chart.MARS, chart.MERCURY,
        chart.JUPITER, chart.VENUS, chart.SATURN, chart.RAHU, chart.KETU
    ]:
        symbol = chart.get_planet_symbol(planet_key, outerchart.language)
        planet_name = {
            chart.SUN: "Sun", chart.MOON: "Moon", chart.MARS: "Mars",
            chart.MERCURY: "Mercury", chart.JUPITER: "Jupiter",
            chart.VENUS: "Venus", chart.SATURN: "Saturn",
            chart.RAHU: "Rahu", chart.KETU: "Ketu"
        }[planet_key]
        outerchart.delete_planet(planet_key)
        outerchart.add_planet(
            planet_key, symbol,
            gen.get_house_number(firsthouse, outer_astrodata[outer_div]["planets"][planet_name]["sign"]),
            colour=planet_colourstrategy_dispositorRelation(outer_astrodata[outer_div]["planets"][planet_name]),
            retrograde=outer_astrodata[outer_div]["planets"][planet_name]["retro"]
        )

    _apply_display_settings(outerchart, chart_style, aspect_val=IsOuterAspectNeeded, is_outer_chart=True)
    outerchart.draw(chart_loc, chart_name)

    svg_file = os.path.join(chart_loc, f"{chart_name}.svg")
    fix_svg_styling_for_qsvgrenderer(svg_file)

    innerchart = None
    outerchart = None
    return

# ---------------------------------------------------------------------------
# Draw a partial chart highlighting only specific relevant planets
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# Draw a numerical astrological chart
# ---------------------------------------------------------------------------
def plot_numerical_astrochart(chart_loc, chart_name, astrodata, values_dict, div="D1",
                              firsthousesign="None", language="english", chart_style="north",
                              default_color="lime"):
    firsthouse = astrodata[div]["ascendant"]["sign"] if firsthousesign == "None" else firsthousesign

    name = getattr(gvar, 'ufuserdata', {}).get("name", "User")
    if not name:
        name = "User"

    # Select numerical chart class based on style
    if chart_style == "south":
        mychart = chart.SouthNumericalChart(div, name)
    else:
        mychart = chart.NorthNumericalChart(div, name)

    mychart.language = language
    mychart.set_ascendantsign(firsthouse)

    for i in range(1, 13):
        val = str(values_dict.get(i, ""))
        mychart.set_house_value(i, val, colour=default_color)

    _apply_display_settings(mychart, chart_style, aspect_val=False)
    mychart.draw(chart_loc, chart_name)

    svg_file = os.path.join(chart_loc, f"{chart_name}.svg")
    fix_svg_styling_for_qsvgrenderer(svg_file)

    mychart = None
    return

def plot_partial_astrochart(chart_loc, chart_name, astrodata, relevant_planets,
                            div="D1", firsthousesign="None", language="english", chart_style="north"):
    firsthouse = astrodata[div]["ascendant"]["sign"] if firsthousesign == "None" else firsthousesign

    name = getattr(gvar, 'ufuserdata', {}).get("name", "User")
    if not name:
        name = "User"

    # Select chart class based on style
    if chart_style == "south":
        mychart = chart.SouthChart(div, name, IsFullChart=False)
    else:
        mychart = chart.NorthChart(div, name, IsFullChart=False)

    mychart.language = language
    mychart.set_ascendantsign(firsthouse)

    planet_map = {
        "Su": (chart.SUN, "Sun"), "Mo": (chart.MOON, "Moon"),
        "Ma": (chart.MARS, "Mars"), "Me": (chart.MERCURY, "Mercury"),
        "Ju": (chart.JUPITER, "Jupiter"), "Ve": (chart.VENUS, "Venus"),
        "Sa": (chart.SATURN, "Saturn"), "Ra": (chart.RAHU, "Rahu"),
        "Ke": (chart.KETU, "Ketu")
    }

    # Only add the planets present in the relevant_planets array
    for p_abbr in relevant_planets:
        if p_abbr in planet_map:
            p_const, p_fullname = planet_map[p_abbr]
            symbol = chart.get_planet_symbol(p_const, mychart.language)
            house_num = gen.get_house_number(firsthouse, astrodata[div]["planets"][p_fullname]["sign"])
            
            mychart.add_planet(
                p_const, symbol, house_num,
                colour=planet_colourstrategy_dispositorRelation(astrodata[div]["planets"][p_fullname]),
                retrograde=astrodata[div]["planets"][p_fullname]["retro"]
            )

    _apply_display_settings(mychart, chart_style, aspect_val=False)
    mychart.draw(chart_loc, chart_name)

    svg_file = os.path.join(chart_loc, f"{chart_name}.svg")
    fix_svg_styling_for_qsvgrenderer(svg_file)

    mychart = None
    return
