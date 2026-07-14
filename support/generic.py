from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import support.constants as c

signs = [ "Aries",       "Taurus",    "Gemini",   "Cancer",
          "Leo",         "Virgo",     "Libra",    "Scorpio",
          "Saggitarius", "Capricorn", "Aquarius", "Pisces"
        ]

signnum = lambda signstr: signs.index(signstr) + 1

def get_house_number(firsthouse_sign, planet_sign):
    asc_index = signnum(firsthouse_sign)
    planet_index = signnum(planet_sign)
    house_number = ((planet_index - asc_index) % 12) + 1
    return house_number

def housediff(fromsign, tosign):
  ''' Computes how many houses is difference between from fromsign to tosign
      This function is used to compute housenumber for planets too '''
  if(tosign > fromsign):
    house = tosign - fromsign + 1
  elif(tosign < fromsign):
    house = 12 + tosign - fromsign + 1
  else: #same signs
    house = 1 #first house
  return house

def compute_nthsign(fromsign, n):
    s = (fromsign + n - 1) % 12
    if (s == 0):
        s = 12
    return (s)

#usage: planets = get_planets_in_house(compute_nthsign_backwards(housenum,7), division["planets"])
def get_planets_in_house(houseno, planetgroup):
    houseplanets = []
    for planetname in planetgroup:
        planet = planetgroup[planetname]
        if (planet["house-num"] == houseno):
            houseplanets.append(planet["name"])
    return houseplanets

def list_intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def iterativeReplace(s, old, new):
    while old in s:
        s = s.replace(old, new)
    return s
def get_nthLord(division,n):
    #Gets house-number(n)'s sign lord (who owns the sign in that house in division)
    if "houses" in division:
        return division["houses"][n-1]["sign-lord"]
    
    asc_sign = division["ascendant"]["sign"]
    asc_sign_num = signnum(asc_sign)
    nth_sign_num = asc_sign_num + n - 1
    if nth_sign_num > 12:
        nth_sign_num -= 12
        
    sign_lords = {
        1: "Mars", 2: "Venus", 3: "Mercury", 4: "Moon",
        5: "Sun", 6: "Mercury", 7: "Venus", 8: "Mars",
        9: "Jupiter", 10: "Saturn", 11: "Saturn", 12: "Jupiter"
    }
    return sign_lords[nth_sign_num]



def get_planetPlacedHousenum(division, planet):
    #Gets in which house is the requested planet placed in that housein division
    housenum = division["planets"][planet]["house-num"]
    return housenum



def get_distancebetweenplanets(division, fromplanet, toplanet):
    #Computes whats the distance between from planet to toplanet in given divisional chart in seconds(deg and minutes also converted to seconds)
    fp = division["planets"][fromplanet]
    tp = division["planets"][toplanet]
    #compute distance from start of lagna to from and to planets in seconds.
    sec_fp = (((fp["house-num"]-1)*30*3600) + (fp["pos"]["deg"]*3600) + (fp["pos"]["min"]*60) + (fp["pos"]["sec"]))
    sec_tp = (((tp["house-num"]-1)*30*3600) + (tp["pos"]["deg"]*3600) + (tp["pos"]["min"]*60) + (tp["pos"]["sec"]))

    if(sec_tp >= sec_fp):   #if toplanet is ahead of fromplanet
        dist = sec_tp - sec_fp
    else:   #if toplanet is behind of fromplanet
        gap = sec_fp - sec_tp
        dist = (360*3600) - gap

    return dist



sign_natures =  [   "Movable",       "Fixed",    "Dual",
                    "Movable",       "Fixed",    "Dual",
                    "Movable",       "Fixed",    "Dual",
                    "Movable",       "Fixed",    "Dual"
                ]
sign_nature = dict(zip(signs, sign_natures))



def check_ifAllNumInSetA_in_SetB(SetA,SetB):
    SetA_Copy = SetA.copy()
    SetB_Copy = SetB.copy()
    for item in SetB_Copy:
        while(item in SetA_Copy):
            SetA_Copy.remove(item)
    if(len(SetA_Copy) == 0):
        return True
    else:
        return False



def isPushkaraNavamsha(nak, paada):
    PushkaraNavamshas = [   "Bharani3", "Kritika1", "Kritika4", "Rohini2", "Ardra4", 
                            "Punarvasu2", "Pushya2", "Purva Phalguni3", "Uttara Phalguni1", "Uttara Phalguni4",
                            "Hasta2", "Swati4", "Punarvasu4", "Vishaka4", "Vishaka2", "Anurada2", 
                            "Uttara Ashadha4", "Purva Ashadha3", "Uttara Ashadha1", "Shravana2", "Shatabhishak4", 
                            "Purva Bhadrapada4", "Purva Bhadrapada2", "Uttara Bhadrapada2" ]
    if(f'{nak}{paada}' in PushkaraNavamshas):
        return True
    else:
        return False



def isPushkaraBhaga(SignTatva, Degree):
    #For Fire signs (Aries, Leo and Sagittarius) - 21st degree is the Pushkara bhaga
    #For Earth signs (Taurus, Virgo and Capricorn) - 14th degree is the Pushkara bhaga
    #For Airy signs (Gemini, Libra and Aquarius) - 24th degree is the Pushkara bhaga
    #For Water signs (Cancer, Scorpio and Pisces) - 7th degree is the Pushkara bhaga 
    if (SignTatva == c.FIRE) and (Degree == 21):
        return True
    if (SignTatva == c.EARTH) and (Degree == 14):
        return True
    if (SignTatva == c.AIR) and (Degree == 24):
        return True
    if (SignTatva == c.WATER) and (Degree == 7):
        return True
    return False



def is_planet_combust(charts, planet_name, division="D1"):
    """
    Checks if a planet is combust (Asta) by the Sun based on classical degree thresholds.
    """
    if planet_name in ["Sun", "Rahu", "Ketu"]:
        return False
        
    # get_distancebetweenplanets is designed to take the division dictionary directly.
    div_data = charts[division] if division in charts else charts
    if "planets" not in div_data or planet_name not in div_data["planets"] or "Sun" not in div_data["planets"]:
        return False

    dist_sec = get_distancebetweenplanets(div_data, planet_name, "Sun")
    dist_deg = min(dist_sec, (360 * 3600) - dist_sec) / 3600.0
    
    is_retro = div_data["planets"][planet_name].get("retro", 0) == 1
    
    thresholds = {
        "Moon": 12.0,
        "Mars": 17.0,
        "Jupiter": 11.0,
        "Saturn": 15.0
    }
    
    threshold = thresholds.get(planet_name)
    if planet_name == "Mercury":
        threshold = 12.0 if is_retro else 14.0
    elif planet_name == "Venus":
        threshold = 8.0 if is_retro else 10.0
        
    if threshold and dist_deg <= threshold:
        return True
        
    return False


def is_planet_benefic(charts, planet_name, division="D1"):
    """
    Determines if a planet is acting as a benefic in the chart.
    Jupiter and Venus are natural benefics.
    Sun, Mars, Saturn, Rahu, Ketu are natural malefics.
    Mercury is benefic unless conjunct with a natural malefic.
    Moon is benefic unless it is very close to the Sun (dark Moon/Amavasya).
    """
    natural_benefics = ["Jupiter", "Venus"]
    natural_malefics = ["Sun", "Mars", "Saturn", "Rahu", "Ketu"]
    
    if planet_name in natural_benefics:
        return True
    if planet_name in natural_malefics:
        return False
        
    div_data = charts[division] if division in charts else charts
    
    if planet_name == "Mercury":
        # Benefic unless conjunct with a natural malefic
        conjuncts = div_data["planets"].get("Mercury", {}).get("conjuncts", [])
        for m in natural_malefics:
            if m in conjuncts:
                return False
        return True
        
    if planet_name == "Moon":
        # Moon is malefic if close to the Sun (waning dark moon phase).
        # We'll use 72 degrees as a standard threshold for Ksheena Chandra (weak moon).
        if "Sun" not in div_data["planets"] or "Moon" not in div_data["planets"]:
            return True
        dist_sec = get_distancebetweenplanets(div_data, "Moon", "Sun")
        dist_deg = min(dist_sec, (360 * 3600) - dist_sec) / 3600.0
        if dist_deg < 72.0:
            return False
        return True

    return False
