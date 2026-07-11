import os
import json

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), '..', 'json', 'display_settings.json')

DEFAULT_SETTINGS = {
    "natal_colour_strategy": "planet_colourstrategy_dispositorRelation",
    "transit_colour_strategy": "planet_colourstrategy_dispositorRelation",
    "chart_background_colour": "black",
    "chart_outer_background_colour": "black",
    "chart_outerbox_colour": "red",
    "chart_innerbox_colour": "red",
    "chart_line_colour": "yellow",
    "chart_sign_colour": "pink"
}

def get_settings():
    """Loads and returns display settings from JSON. If missing, returns defaults."""
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()
        
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            user_settings = json.load(f)
            # Merge with defaults in case of missing keys
            settings = DEFAULT_SETTINGS.copy()
            settings.update(user_settings)
            return settings
    except Exception as e:
        print(f"Error loading display settings: {e}")
        return DEFAULT_SETTINGS.copy()

def save_settings(settings_dict):
    """Saves the given display settings to JSON."""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving display settings: {e}")
        return False
        
def get_default_settings():
    return DEFAULT_SETTINGS.copy()
