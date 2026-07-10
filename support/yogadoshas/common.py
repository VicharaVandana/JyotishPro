import support.generic as gen

yogadoshas_dict = {}
parivarthanaYogas = []
AshrayaYogas = []
DalaYogas = []
AakritiYogas = []
SankhyaYogas = []


# ==========================================================================================
# Function Name: iterativeReplace
# Purpose: Calculates and evaluates the condition for iterativeReplace.
# Description: Checks the planetary positions and relationships in the provided charts 
#              to determine if iterativeReplace is formed. Applies cancellation rules if any, 
#              and updates the global yogadoshas_dict with the results.
# Parameters:
#   - s, old, new (dict): Dictionary containing astrological charts (D1, D9, etc.) and planet data.
# Returns:
#   - Evaluated status (typically a boolean True/False indicating presence).
# ==========================================================================================
# ==========================================================================================
# Function Name: iterativeReplace
# Purpose: Calculates the presence of iterativeReplace in the provided horoscope.
# Description: Evaluates standard planetary configurations.
# Expected Impact: Returns boolean indicating presence.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def iterativeReplace(s, old, new):
    while old in s:
        s = s.replace(old, new)
    return s


# ==========================================================================================
# Function Name: reset_globals
# Purpose: Calculates and evaluates the condition for reset_globals.
# Description: Checks the planetary positions and relationships in the provided charts 
#              to determine if reset_globals is formed. Applies cancellation rules if any, 
#              and updates the global yogadoshas_dict with the results.
# Parameters:
#   - None: Dictionary containing astrological charts (D1, D9, etc.) and planet data.
# Returns:
#   - Evaluated status (typically a boolean True/False indicating presence).
# ==========================================================================================
# ==========================================================================================
# Function Name: reset_globals
# Purpose: Calculates the presence of reset_globals in the provided horoscope.
# Description: Evaluates standard planetary configurations.
# Expected Impact: Returns boolean indicating presence.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def reset_globals():
    global yogadoshas_dict, parivarthanaYogas, AshrayaYogas, DalaYogas, AakritiYogas, SankhyaYogas
    yogadoshas_dict = {}
    parivarthanaYogas = []
    AshrayaYogas = []
    DalaYogas = []
    AakritiYogas = []
    SankhyaYogas = []



# ==========================================================================================
# Function Name: get_table_data
# Purpose: Calculates and evaluates the condition for get_table_data.
# Description: Checks the planetary positions and relationships in the provided charts 
#              to determine if get_table_data is formed. Applies cancellation rules if any, 
#              and updates the global yogadoshas_dict with the results.
# Parameters:
#   - charts, div, planet_names, extra_cols=None (dict): Dictionary containing astrological charts (D1, D9, etc.) and planet data.
# Returns:
#   - Evaluated status (typically a boolean True/False indicating presence).
# ==========================================================================================
# ==========================================================================================
# Function Name: get_table_data
# Purpose: Calculates the presence of get_table_data in the provided horoscope.
# Description: Evaluates standard planetary configurations.
# Expected Impact: Returns boolean indicating presence.
# Parameters:
#   - charts (dict): Comprehensive dictionary containing D1, D9 charts and planetary attributes.
# Returns:
#   - Boolean/String: True if the yoga/dosha is present, False otherwise.
# ==========================================================================================
def get_table_data(charts, div, planet_names, extra_cols=None):
    headers = ['Planet', 'Degrees', 'Dignity']
    if extra_cols:
        for k in extra_cols.keys():
            headers.append(k)
            
    rows = []
    for i, p in enumerate(planet_names):
        p_data = charts[div]['planets'].get(p, {})
        if not p_data: continue
        
        pos = p_data.get('pos', {})
        deg = pos.get('deg', 0)
        min = pos.get('min', 0)
        sec = pos.get('sec', 0)
        deg_str = f"{deg}° {min}' {sec}''"
        
        dignity = p_data.get('house-rel', '')
        
        row = [p, deg_str, dignity]
        if extra_cols:
            for k in extra_cols.keys():
                row.append(extra_cols[k][i])
        rows.append(row)
        
    return {'headers': headers, 'rows': rows}
