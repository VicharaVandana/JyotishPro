import datetime as dt
from datetime import timedelta
import support.generic as gen

# Vimshottari Dasha periods in years
DASHA_PERIODS = {
    'Ketu': 7, 'Venus': 20, 'Sun': 6, 'Moon': 10, 'Mars': 7,
    'Rahu': 18, 'Jupiter': 16, 'Saturn': 19, 'Mercury': 17
}

# Nakshatras and their ruling planets
NAKSHATRAS = [
    ("Ashwini", "Ketu"), ("Bharani", "Venus"), ("Krittika", "Sun"), ("Rohini", "Moon"), ("Mrigashira", "Mars"),
    ("Ardra", "Rahu"), ("Punarvasu", "Jupiter"), ("Pushya", "Saturn"), ("Ashlesha", "Mercury"),
    ("Magha", "Ketu"), ("Purva Phalguni", "Venus"), ("Uttara Phalguni", "Sun"), ("Hasta", "Moon"),
    ("Chitra", "Mars"), ("Swati", "Rahu"), ("Vishakha", "Jupiter"), ("Anuradha", "Saturn"), ("Jyeshtha", "Mercury"),
    ("Mula", "Ketu"), ("Purva Ashadha", "Venus"), ("Uttara Ashadha", "Sun"), ("Shravana", "Moon"),
    ("Dhanishta", "Mars"), ("Shatabhisha", "Rahu"), ("Purva Bhadrapada", "Jupiter"), ("Uttara Bhadrapada", "Saturn"),
    ("Revati", "Mercury")
]

# Order of dashas as per Nakshatra lords
DASHA_SEQUENCE = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']

def get_planet_period_for_event(start_date, end_date, first_planet, event_date):
    """
    Divides the period from start_date to end_date according to the Vimshottari Dasha periods
    and determines which planet's period the event_date falls under.
    
    :param start_date: datetime object representing the start date
    :param end_date: datetime object representing the end date
    :param first_planet: string name of the first planet of the cycle (e.g., 'Moon')
    :param event_date: datetime object representing the event date
    :return: planet name and its period start and end date
    """
    # Calculate total duration between start_date and end_date in days
    total_duration_days = (end_date - start_date).days
    
    # Total Vimshottari period in years
    total_vimshottari_years = sum(DASHA_PERIODS.values())
    
    # Calculate the total Vimshottari period in days
    total_vimshottari_days = total_vimshottari_years * 365.25

    # Calculate the proportion of time each planet's period occupies
    planet_durations = {planet: (DASHA_PERIODS[planet] / total_vimshottari_years) * total_duration_days for planet in DASHA_PERIODS}
    
    # Get the starting index of the planets in the DASHA_SEQUENCE
    #print(first_planet)
    start_index = DASHA_SEQUENCE.index(first_planet)
    
    # Calculate the start and end dates for each planet's period within the given duration
    current_start_date = start_date
    for i in range(9):  # 9 planets in total
        planet = DASHA_SEQUENCE[(start_index + i) % 9]  # Get the planet in cycle order
        planet_duration_days = planet_durations[planet]  # Duration of the current planet's period
        
        # Calculate the end date of the current planet's period
        current_end_date = current_start_date + timedelta(days=planet_duration_days)
        
        #print(f"{current_start_date} <= {event_date} <= {current_end_date}: of planet {planet} with duration {planet_durations[planet]}")
        # Check if the event_date falls within this period
        if current_start_date <= event_date <= current_end_date:
            # Return the planet and the period's start and end date
            return planet, current_start_date, current_end_date
        else:
            # Move to the next planet's period
            current_start_date = current_end_date

    # If the event_date doesn't fall under any planet's period (which shouldn't happen)
    return None, current_start_date, current_end_date

def calculate_dasha(birth_date, event_date, moon_longitude):
    """
    Calculate Vimshottari Dasha levels for a given date, birth date, and moon longitude.
    :param birth_date: datetime object of birth date
    :param event_date: datetime object of the event date
    :param moon_longitude: Moon's longitude in degrees
    """
    dasha_levels = {
        'total': {'lord':'', 'startdate':'', 'enddate':''},
        'Mahadasha': {'lord':'', 'startdate':'', 'enddate':''},
        'Antardasha': {'lord':'', 'startdate':'', 'enddate':''},
        'Pratyantardasha': {'lord':'', 'startdate':'', 'enddate':''},
        'Sookshma Dasha': {'lord':'', 'startdate':'', 'enddate':''},
        'Deha-Antara Dasha': {'lord':'', 'startdate':'', 'enddate':''}
    }
    # Calculate Nakshatra and starting Dasha lord
    nak_duration = 13.0 + (20/60)   #13 degree 20 minutes
    nakshatra = int(moon_longitude // nak_duration)
    first_dashaLord = NAKSHATRAS[nakshatra % 27][1]

    # Calculate elapsed time in the current Mahadasha
    dasha_fraction = (moon_longitude % nak_duration) / nak_duration
    remaining_years = DASHA_PERIODS[first_dashaLord] * (1 - dasha_fraction)

    # Calculate the start date of the Mahadasha
    first_mahadasha_start = birth_date - timedelta(days=int((DASHA_PERIODS[first_dashaLord] - remaining_years) * 365.25))
    #mahadasha_end = first_mahadasha_start + timedelta(days=int((DASHA_PERIODS[first_dashaLord]) * 365.25))
    full_vimshottari_end = first_mahadasha_start + timedelta(days=int((120) * 365.25))
    
    #print(f"The first mahadasha was of {first_dashaLord} started on {first_mahadasha_start} and ended on {mahadasha_end}")
    dasha_levels['total']['lord'] = first_dashaLord
    dasha_levels['total']['startdate'] = first_mahadasha_start
    dasha_levels['total']['enddate'] = full_vimshottari_end
    
    

    # Dynamically compute the levels
    current_level = 'total'
    for level in ['Mahadasha', 'Antardasha', 'Pratyantardasha', 'Sookshma Dasha', 'Deha-Antara Dasha']:
        if dasha_levels[current_level]['lord'] == None:
            break
        # Get planet name and period range for the current level
        planet, period_start, period_end = get_planet_period_for_event(dasha_levels[current_level]['startdate'], dasha_levels[current_level]['enddate'], dasha_levels[current_level]['lord'], event_date)
        
        if planet:
            dasha_levels[level]['lord'] = planet
            dasha_levels[level]['startdate'] = period_start
            dasha_levels[level]['enddate'] = period_end
            current_level = level
        else:
            print(f"Value Error - Event date {event_date} is outside the range of {dasha_levels[current_level]['startdate']} to {dasha_levels[current_level]['enddate']} for level {current_level}.")
            dasha_levels[level]['lord'] = planet
            dasha_levels[level]['startdate'] = period_start
            dasha_levels[level]['enddate'] = period_end
            current_level = level
    return dasha_levels

def get_dasha_dict_fordate(ad, td, div="D1", planet_name="Moon"):
    bd = ad["user_details"]["birthdetails"]["DOB"]
    bt = ad["user_details"]["birthdetails"]["TOB"]
    ed = td["user_details"]["birthdetails"]["DOB"]
    et = td["user_details"]["birthdetails"]["TOB"]

    birth_date = dt.datetime(int(bd["year"]), int(bd["month"]), int(bd["day"]), int(bt["hour"]), int(bt["min"]))
    event_date = dt.datetime(int(ed["year"]), int(ed["month"]), int(ed["day"]), int(et["hour"]), int(et["min"]))
    sign = gen.signnum(ad[div]["planets"][planet_name]["sign"])
    deg_dec = ad[div]["planets"][planet_name]["pos"]["dec_deg"]
    planet_long = (((sign-1)*30) + deg_dec)
    dasha_levels = calculate_dasha(birth_date, event_date, planet_long)
    
    return {
        "MD": dasha_levels['Mahadasha']['lord'],
        "AD": dasha_levels['Antardasha']['lord'],
        "PD": dasha_levels['Pratyantardasha']['lord']
    }

def get_dashadetails_fordate(ad,td,div="D1",planet_name="Moon"):
    bd = ad["user_details"]["birthdetails"]["DOB"]
    bt = ad["user_details"]["birthdetails"]["TOB"]
    ed = td["user_details"]["birthdetails"]["DOB"]
    et = td["user_details"]["birthdetails"]["TOB"]

    birth_date = dt.datetime(bd["year"], bd["month"], bd["day"], bt["hour"], bt["min"])
    event_date = dt.datetime(ed["year"], ed["month"], ed["day"], et["hour"], et["min"])
    sign = gen.signnum(ad[div]["planets"][planet_name]["sign"])
    deg_dec = ad[div]["planets"][planet_name]["pos"]["dec_deg"]
    planet_long = (((sign-1)*30) + deg_dec)
    dasha_levels = calculate_dasha(birth_date, event_date, planet_long)

    # Formatting HTML content for PyQt5 label display with color coding
    try:
        html = f"""
    <div style="font-size: 16px;">
    <h3><b>Dasha Details</b></h3><br>
    
    <b><u>Mahadasha:</u></b><br>
    <span style="color: #3A7CA5;">Planet: <b>{dasha_levels['Mahadasha']['lord']}</b></span><br>
    <span style="color: #2D9038;">Start Date: <b>{dasha_levels['Mahadasha']['startdate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br>
    <span style="color: #D96B6B;">End Date: <b>{dasha_levels['Mahadasha']['enddate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br><br>

    <b><u>Antardasha:</u></b><br>
    <span style="color: #3A7CA5;">Planet: <b>{dasha_levels['Antardasha']['lord']}</b></span><br>
    <span style="color: #2D9038;">Start Date: <b>{dasha_levels['Antardasha']['startdate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br>
    <span style="color: #D96B6B;">End Date: <b>{dasha_levels['Antardasha']['enddate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br><br>

    <b><u>Pratyantardasha:</u></b><br>
    <span style="color: #3A7CA5;">Planet: <b>{dasha_levels['Pratyantardasha']['lord']}</b></span><br>
    <span style="color: #2D9038;">Start Date: <b>{dasha_levels['Pratyantardasha']['startdate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br>
    <span style="color: #D96B6B;">End Date: <b>{dasha_levels['Pratyantardasha']['enddate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br><br>

    <b><u>Sookshma Dasha:</u></b><br>
    <span style="color: #3A7CA5;">Planet: <b>{dasha_levels['Sookshma Dasha']['lord']}</b></span><br>
    <span style="color: #2D9038;">Start Date: <b>{dasha_levels['Sookshma Dasha']['startdate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br>
    <span style="color: #D96B6B;">End Date: <b>{dasha_levels['Sookshma Dasha']['enddate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br><br>

    <b><u>Deha-Antara Dasha:</u></b><br>
    <span style="color: #3A7CA5;">Planet: <b>{dasha_levels['Deha-Antara Dasha']['lord']}</b></span><br>
    <span style="color: #2D9038;">Start Date: <b>{dasha_levels['Deha-Antara Dasha']['startdate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br>
    <span style="color: #D96B6B;">End Date: <b>{dasha_levels['Deha-Antara Dasha']['enddate'].strftime('%Y-%b-%d  [%I:%M %p]')}</b></span><br><br>
    </div>
    """
    except KeyError as e:
        print(f"KeyError: Missing key {e} in dasha_levels.")
        html = ""
    except Exception as e:
        print(f"Unexpected error: {e}")
        html = ""
    except:
        print(dasha_levels)
        html = ""

    return html

def get_dashaplanet_tabletransit_fordate(ad,td, transitdiv="D1", div="D1",planet_name="Moon"):
    bd = ad["user_details"]["birthdetails"]["DOB"]
    bt = ad["user_details"]["birthdetails"]["TOB"]
    ed = td["user_details"]["birthdetails"]["DOB"]
    et = td["user_details"]["birthdetails"]["TOB"]

    birth_date = dt.datetime(bd["year"], bd["month"], bd["day"], bt["hour"], bt["min"])
    event_date = dt.datetime(ed["year"], ed["month"], ed["day"], et["hour"], et["min"])
    sign = gen.signnum(ad[div]["planets"][planet_name]["sign"])
    deg_dec = ad[div]["planets"][planet_name]["pos"]["dec_deg"]
    planet_long = (((sign-1)*30) + deg_dec)
    dasha_levels = calculate_dasha(birth_date, event_date, planet_long)
    dasha_transit_table_dict = {
        'Mahadasha': {'lord':'', 'impacting_signs':[], 'impacting_signNum':[]},
        'Antardasha': {'lord':'', 'impacting_signs':[], 'impacting_signNum':[]},
        'Pratyantardasha': {'lord':'', 'impacting_signs':[], 'impacting_signNum':[]},
        'Sookshma Dasha': {'lord':'', 'impacting_signs':[], 'impacting_signNum':[]},
        'Deha-Antara Dasha': {'lord':'', 'impacting_signs':[], 'impacting_signNum':[]}

    }
    for key in dasha_levels:
        if(key == "total"):
            continue
        if dasha_levels[key]["lord"] != None:
            lord = dasha_levels[key]["lord"]
            dasha_transit_table_dict[key]["lord"] = lord
            dasha_transit_table_dict[key]["impacting_signs"] = td[transitdiv]["planets"][lord]["Aspects"]["signs"].copy()
            dasha_transit_table_dict[key]["impacting_signs"].append(td[transitdiv]["planets"][lord]["sign"])
            dasha_transit_table_dict[key]["impacting_signNum"] = []
            for sign in dasha_transit_table_dict[key]["impacting_signs"]:
                dasha_transit_table_dict[key]["impacting_signNum"].append(gen.signnum(sign))
            dasha_transit_table_dict[key]["impacting_signNum"].sort()  # Sorts the list in-place

    return dasha_transit_table_dict

def get_dasha_details_from_dict(ad, planet_name):
    today = dt.datetime.today()
    antardashas = ad["Dashas"]["Vimshottari"]["antardashas"]
    paryantardashas = ad["Dashas"]["Vimshottari"]["paryantardashas"]
    mahadashas = ad["Dashas"]["Vimshottari"]["mahadashas"]

    def find_periods(data, planet, is_paryantardasha=False):
        relevant_periods = []
        for key, value in data.items():
            parts = key.split('-')
            if is_paryantardasha:
                if parts[-1] == planet:
                    relevant_periods.append((
                        dt.datetime.strptime(value["startDate"].split()[0], '%Y-%m-%d'),
                        dt.datetime.strptime(value["endDate"].split()[0], '%Y-%m-%d'),
                        value["dashaLord"],
                        value["bhuktiLord"],
                        value["startDate"],
                        value["endDate"]
                    ))
            else:
                if parts[-1] == planet:
                    relevant_periods.append((
                        dt.datetime.strptime(value["startDate"].split()[0], '%Y-%m-%d'),
                        dt.datetime.strptime(value["endDate"].split()[0], '%Y-%m-%d'),
                        value["dashaLord"],
                        value["startDate"],
                        value["endDate"]
                    ))
        relevant_periods.sort()
        return relevant_periods

    def get_mahadasha_duration(planet):
        md = mahadashas.get(planet, {})
        if md:
            start_str = dt.datetime.strptime(md["startDate"].split()[0], '%Y-%m-%d').strftime('%d %B %Y')
            end_str = dt.datetime.strptime(md["endDate"].split()[0], '%Y-%m-%d').strftime('%d %B %Y')
            return f"<span style='color: blue;'>{start_str}</span> to <span style='color: green;'>{end_str}</span>"
        return None

    def format_period(period, is_paryantardasha=False):
        start_str = dt.datetime.strptime(period[-2].split()[0], '%Y-%m-%d').strftime('%d %B %Y')
        end_str = dt.datetime.strptime(period[-1].split()[0], '%Y-%m-%d').strftime('%d %B %Y')
        if is_paryantardasha:
            return f"<span style='color: blue;'>{start_str}</span> to <span style='color: green;'>{end_str}</span> under dasha of <span style='color: purple;'>{period[2]}-{period[3]}</span>"
        else:
            return f"<span style='color: blue;'>{start_str}</span> to <span style='color: green;'>{end_str}</span> under dasha of <span style='color: purple;'>{period[2]}</span>"

    ant_periods = find_periods(antardashas, planet_name)
    pary_periods = find_periods(paryantardashas, planet_name, True)

    def extract_details(periods, is_paryantardasha=False):
        last = next = current = ""
        for period in periods:
            if period[0] <= today <= period[1]:
                current = format_period(period, is_paryantardasha)
            elif period[1] < today:
                last = format_period(period, is_paryantardasha)
            elif period[0] > today and not next:
                next = format_period(period, is_paryantardasha)
        return last, current, next

    last_ant, current_ant, next_ant = extract_details(ant_periods)
    last_pary, current_pary, next_pary = extract_details(pary_periods, True)
    dasha_duration = get_mahadasha_duration(planet_name)

    html = f'''<U><b>Dasha Period:</b></U> {dasha_duration if dasha_duration else "Not Running"} <br>
            <U><b>Current Antardasha:</b></U> {current_ant if current_ant else "Not Running"}<br>
            <U><b>Last Antardasha:</b></U> {last_ant}<br>
            <U><b>Next Antardasha:</b></U> {next_ant} <br>
            <U><b>Current Paryantardasha:</b></U> {current_pary if current_pary else "Not Running"}<br>
            <U><b>Last Paryantardasha:</b></U> {last_pary} <br>
            <U><b>Next Paryantardasha:</b></U> {next_pary} <br>'''
    return html


