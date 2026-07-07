import jyotishyamitra as jsm
import jyotichart as jc
import support.globalvariables as gvar
from PyQt5.QtWidgets import QApplication
import support.generic as gen
import copy
from datetime import datetime
from PyQt5.QtCore import QDate, QTime

#declare constants related to planet sign placement 
DEBILITATED = "Debilitated / Neecha"
ENEMYSIGN = "Enemy sign / Shatru rashi"
NEUTRALSIGN = "Neutral sign / Sama rashi"
FRIENDSIGN = "Friends sign / Mitra rashi"
OWNSIGN = "Own sign / Swa rashi"
MOOLTRIKONA = "Prime sign / Moolatrikona rashi"
EXHALTED = "Exhalted / Uchha"


def generate_astrodata(bd):

    #step 1 :clear past input data
    jsm.clear_birthdata()

    #Step 2: Providing input birth data - here multiple times the API input_birthdata are invoked but you can do it in single shot too.
    #providing Name and Gender
    inputdata = jsm.input_birthdata(name=bd["name"], gender=bd["gender"])

    #providing Date of birth details
    inputdata = jsm.input_birthdata(year=bd["DOB"]["year"], month=bd["DOB"]["month"], day=bd["DOB"]["day"])

    #Providing Place of birth details
    inputdata = jsm.input_birthdata(place=bd["POB"]["name"], longitude=bd["POB"]["lon"], lattitude=bd["POB"]["lat"], timezone=bd["POB"]["timezone"])

    #Providing Time of birth details
    inputdata = jsm.input_birthdata(hour=bd["TOB"]["hour"], min=bd["TOB"]["min"], sec=bd["TOB"]["sec"])

    #Step 3: Validate Birthdata
    jsm.validate_birthdata()

    #Step 4: If Birthdata is valid then get birthdata
    if(jsm.IsBirthdataValid()):
        birthdata = jsm.get_birthdata()
    else:
        print("Error:birthdata is invalid!!!")


    #Step 5: Invoke the API generate_astrologicalData with retrunval desired to be dictionary and get astrological data in dictionary format.
    ad = jsm.generate_astrologicalData(birthdata, returnval = "ASTRODATA_DICTIONARY") 
    return ad


    
def extract_userdata(uf):
    userdata = {}
    name = str(uf.cmb_name.currentText()).strip()
    if name == "":
        uf.status.setText("Submit button clicked: Name is empty and so no action done.")
        return "FAIL"
    userdata["name"] = name
    userdata["gender"] = str(uf.cmb_gender.currentText()).strip()
    userdata["DOB"] = {}
    date = uf.dob.date().toPyDate()
    userdata["DOB"]["year"] = str(date.year).strip()
    userdata["DOB"]["month"] = str(date.month).strip()
    userdata["DOB"]["day"] = str(date.day).strip()
    userdata["TOB"] = {}
    time = uf.tob.time()
    userdata["TOB"]["hour"] = str(time.hour()).strip()
    userdata["TOB"]["min"] = str(time.minute()).strip()
    userdata["TOB"]["sec"] = str(time.second()).strip()
    userdata["POB"] = {}
    userdata["POB"]["name"] = str(uf.place.text()).strip()
    userdata["POB"]["lon"] = str(uf.lon.text()).strip()
    userdata["POB"]["lat"] = str(uf.lat.text()).strip()
    userdata["POB"]["timezone"] = str(uf.tz.text()).strip()
    return userdata

def extract_transit_userdata(uf):
    transit_userdata = {}
    name = str(uf.cmb_name.currentText()).strip()
    if name == "":
        uf.status.setText("Submit button clicked: Name is empty and so no action done.")
        return "FAIL"
    transit_userdata["name"] = name
    transit_userdata["gender"] = str(uf.cmb_gender.currentText()).strip()
    date = uf.dateEdit_transitdate.date()
    transit_userdata["DOB"] = {}
    transit_userdata["DOB"]["year"] = date.toString("yyyy") # Year as string (e.g., "2025")
    transit_userdata["DOB"]["month"] = date.toString("MM")  # Month as string (e.g., "10" for October)
    transit_userdata["DOB"]["day"] = date.toString("dd")    # Day as string (e.g., "05")
    transit_userdata["TOB"] = {}
    time = uf.timeEdit_transittime.time()
    transit_userdata["TOB"]["hour"] = time.toString("HH")   # Hour in 24-hour format (e.g., "09" or "21")
    transit_userdata["TOB"]["min"] = time.toString("mm") # Minute with leading zero if needed
    transit_userdata["TOB"]["sec"] = "00"
    transit_userdata["POB"] = {}
    transit_userdata["POB"]["name"] = str(uf.place.text()).strip()
    transit_userdata["POB"]["lon"] = str(uf.lon.text()).strip()
    transit_userdata["POB"]["lat"] = str(uf.lat.text()).strip()
    transit_userdata["POB"]["timezone"] = str(uf.tz.text()).strip()
    return transit_userdata

def initialAstroCalculations(uf):
    # Get details from userform
    userdata = extract_userdata(uf)
    if (userdata == "FAIL"):
        return 
    gvar.ufuserdata.clear()
    gvar.ufuserdata = copy.deepcopy(userdata)

    # Generate Astrological data
    uf.status.setText("Submit button clicked: Computing astrological data...")
    QApplication.processEvents()
    gvar.astrodata.clear()
    gvar.astrodata = copy.deepcopy(generate_astrodata(userdata))
    QApplication.processEvents()
    
    uf.status.setText("Submit button clicked: astrological computation finished.")
    return

def transitAstroCalculations(uf):
    # Get Transit details from userform
    transit_userdata = extract_transit_userdata(uf)
    if (transit_userdata == "FAIL"):
        return 
    
    QApplication.processEvents()
    gvar.transit_userdata.clear()
    gvar.transit_userdata = copy.deepcopy(transit_userdata)
    gvar.transit_astrodata.clear()
    gvar.transit_astrodata = copy.deepcopy(generate_astrodata(transit_userdata))
    QApplication.processEvents()

    return




