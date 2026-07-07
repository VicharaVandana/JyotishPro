import requests
from bs4 import BeautifulSoup
import json
import os

# Month mapping for conversion
MONTHS = {
    "January": "1", "February": "2", "March": "3", "April": "4",
    "May": "5", "June": "6", "July": "7", "August": "8",
    "September": "9", "October": "10", "November": "11", "December": "12"
}

def dms_to_decimal(dms_str):
    """Converts 'degrees minutes' format (e.g., '12 48') to decimal degrees (e.g., '12.80')"""
    #print(dms_str)
    dmsstr_numpart = dms_str.replace("E"," ").replace("W"," ").replace("N"," ").replace("W"," ")
    parts = dmsstr_numpart.split()
    if len(parts) != 2:
        return "Unknown"  # Handle missing values

    degrees, minutes = int(parts[0]), int(parts[1])
    decimal_value = degrees + (minutes / 60)  # Convert to decimal

    # Add sign for N/S/E/W
    if "S" in dms_str or "W" in dms_str:
        return_val = f"-{decimal_value:.6f}"
    else:
        return_val = f"+{decimal_value:.6f}"

    return return_val # Ensure consistent decimal places

def extract_birth_details(url, output_json="./json/celebrity_birthdata_db.json"):
    """Fetches an HTML page, extracts birth details, and appends them to a JSON file."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a browser request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the div with birth details
        birth_div = soup.find("div", class_="ui-cbcol-l")
        if not birth_div:
            print("❌ Birth details div not found!")
            return

        # Extract details from div
        birth_data = {}
        for div in birth_div.find_all("div", class_="celebcont"):
            text = div.get_text(strip=True).split(":")
            if len(text) == 2:
                key, value = text[0].strip(), text[1].strip()
                birth_data[key] = value

        # Extract and format name
        person_name = birth_data.get("Name", "Unknown").strip()
        person_key = person_name.lower().replace(" ", "_")  # Convert name to lowercase and replace spaces

        month_str = birth_data.get("Date of Birth", "Unknown").split()[-3]
        month_numstr = MONTHS.get(month_str, "Unknown")

        # Convert extracted data to structured JSON format
        structured_data = {
            person_key: {
                "name": person_name,
                "gender": "male",  # Assuming gender is male, modify if needed
                "DOB": {
                    "year": birth_data.get("Date of Birth", "Unknown").split()[-1].replace(",", "").strip(),
                    "month": month_numstr.replace(",", "").strip(),
                    "day": birth_data.get("Date of Birth", "Unknown").split()[-2].replace(",", "").strip()
                },
                "TOB": {
                    "hour": birth_data.get("Time of Birth", "00:00:00").split(":")[0].replace(",", "").strip(),
                    "min": birth_data.get("Time of Birth", "00:00:00").split(":")[1].replace(",", "").strip(),
                    "sec": birth_data.get("Time of Birth", "00:00:00").split(":")[2].replace(",", "").strip()
                },
                "POB": {
                    "name": birth_data.get("Place of Birth", "Unknown"),
                    "lon": dms_to_decimal(birth_data.get("Longitude", "Unknown").replace("\u00a0", "")).replace(",", "").strip(),
                    "lat": dms_to_decimal(birth_data.get("Latitude", "Unknown").replace("\u00a0", "")).replace(",", "").strip(),
                    "timezone": f'{birth_data.get("Time Zone", "Unknown")}'.replace(",", "").strip()
                },
                "comments": f'''Celebrity Horoscope from astrosage. 
Information source: {birth_data.get("Information Source", "Not Found")}
AstroSage Rating: {birth_data.get("AstroSage Rating", "No Rating")}'''
            }
        }

        # Load existing JSON file (if it exists)
        if os.path.exists(output_json):
            with open(output_json, "r", encoding="utf-8") as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    existing_data = {}
        else:
            existing_data = {}

        # Add new data without overwriting existing entries
        existing_data.update(structured_data)

        # Save updated JSON file
        with open(output_json, "w", encoding="utf-8") as json_file:
            json.dump(existing_data, json_file, indent=4)

        print(f"✅ Birth details extracted and added to '{output_json}'")

    except Exception as e:
        print(f"❌ Error: {e}")

# Example Usage
astro_link = "https://celebrity.astrosage.com/indira-gandhi-birth-chart.asp"
extract_birth_details(astro_link)
