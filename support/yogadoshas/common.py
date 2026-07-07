import support.generic as gen

yogadoshas_dict = {}
parivarthanaYogas = []
AshrayaYogas = []
DalaYogas = []
AakritiYogas = []
SankhyaYogas = []

def iterativeReplace(s, old, new):
    while old in s:
        s = s.replace(old, new)
    return s

def reset_globals():
    global yogadoshas_dict, parivarthanaYogas, AshrayaYogas, DalaYogas, AakritiYogas, SankhyaYogas
    yogadoshas_dict = {}
    parivarthanaYogas = []
    AshrayaYogas = []
    DalaYogas = []
    AakritiYogas = []
    SankhyaYogas = []


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
