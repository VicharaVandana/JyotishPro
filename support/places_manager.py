import json
import os
import threading

PLACES_FILE = os.path.join(os.path.dirname(__file__), '..', 'json', 'places.json')

_places_data = []
_place_names = []
_load_lock = threading.Lock()
_loaded = False

def load_places_async(callback=None):
    def _load():
        global _places_data, _place_names, _loaded
        with _load_lock:
            if _loaded:
                if callback: callback()
                return
                
            if not os.path.exists(PLACES_FILE):
                print(f"Places file not found: {PLACES_FILE}")
                _loaded = True
                if callback: callback()
                return
                
            try:
                with open(PLACES_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                temp_names = []
                for p in data:
                    name = p.get('name', 'Unknown')
                    tz = p.get('timezone_name', '')
                    display = f"{name} ({tz})" if tz else name
                    temp_names.append(display)
                    p['_display_name'] = display
                
                _places_data = data
                _place_names = temp_names
                _loaded = True
            except Exception as e:
                print(f"Error loading places.json: {e}")
                
        if callback:
            callback()

    # Start the loading in a daemon thread so it doesn't block app shutdown
    t = threading.Thread(target=_load, daemon=True)
    t.start()
    return t

def is_loaded():
    return _loaded

def get_all_place_names():
    # If not loaded, this will return whatever is available (likely empty if still loading)
    # The UI will update the completer once the callback fires.
    return _place_names

def get_place_details(display_name):
    if not _loaded:
        # If they try to search before loaded, we can't help much, return None
        return None
        
    for p in _places_data:
        if p.get('_display_name') == display_name or p.get('name') == display_name:
            return p
    return None

def add_new_place(name, lat, lon, timezone, timezone_name=""):
    global _places_data, _place_names
    
    new_place = {
        "name": name,
        "lat": str(lat),
        "lon": str(lon),
        "timezone": str(timezone),
        "timezone_name": str(timezone_name)
    }
    
    display = f"{name} ({timezone_name})" if timezone_name else name
    new_place['_display_name'] = display
    
    with _load_lock:
        _places_data.append(new_place)
        _place_names.append(display)
        
        # Save to file
        try:
            save_data = []
            for p in _places_data:
                clean_p = p.copy()
                clean_p.pop('_display_name', None)
                save_data.append(clean_p)
                
            with open(PLACES_FILE, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=4)
            return True, display
        except Exception as e:
            print(f"Error saving places.json: {e}")
            return False, display
