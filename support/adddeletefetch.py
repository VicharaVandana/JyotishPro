import json
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore

# Steps to add birthdetails to internal database
# 1. get birthdetails of all users in json file to a dictionary
# 2. fetch userdetails from userform
# 3. check if user already exists in birth details
# 3.1. If user already present then give a pop up if they want to update the details
# 3.1.1. If they want to update then delete that userdetail part and proceed to add fresh data
# 3.1.2 If they dont want to update then just exit the function without doing anything.
# 3.2. If user doesnt exist in database then add this new details to dictionary
# 4. write the birth details back to internal database json file.

def adduser2db(uf):
    with open(f'./json/{uf.BirthdetailsDB_filename}', 'r') as json_birthfile:        
        database = json.loads(json_birthfile.read()) 
    
    userdata = {}
    name = str(uf.cmb_name.currentText()).strip()
    if name == "":
        uf.status.setText("Add button clicked: Name is empty and so userdetail not added to database.")
        return
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
    userdata["comments"] = str(uf.comments.toPlainText()).strip()

    userfound = False
    if ("NOT_FOUND" != database.get(name, "NOT_FOUND")):
        userfound = True
        msgBox = QMessageBox()
        msgBox.setText("This username already exist in database. Do you want to update the userdata?")
        msgBox.setWindowTitle("Update Userdata?")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msgBox.setEscapeButton(QMessageBox.No)            
        buttonReply = msgBox.exec()
        if buttonReply == QMessageBox.No:
            uf.status.setText(f"Add button clicked: Existing User {name}. Update not done with fresh data")
            return
    
    if userfound == True:
        database.pop(name)
        database[name] = userdata
        uf.status.setText(f"Add button clicked: Existing User {name}. Update done with fresh data")
    else:
        database[name] = userdata
        uf.status.setText(f"Add button clicked: New User {name} added to the database.")

    with open(f'./json/{uf.BirthdetailsDB_filename}', 'w') as json_birthfile:
        json.dump(dict(database), json_birthfile, indent=4)
    
    #finally add the name to dropdown
    uf.cmb_name.addItem(name)
    
    return
    
# Steps to delete birthdetails od selected user from internal database
# 1. get birthdetails of all users in json file to a dictionary
# 2. fetch username from userform
# 3. check if user already exists in birth details
# 3.1. If user already present then delete the user from database
# 3.2. If user doesnt exist in database then exit saying user doesnt exist
# 4. write the birth details back to internal database json file.

def deluser4mdb(uf):
    with open(f'./json/{uf.BirthdetailsDB_filename}', 'r') as json_birthfile:        
        database = json.loads(json_birthfile.read()) 
    
    name = str(uf.cmb_name.currentText()).strip()
    
    if ("NOT_FOUND" != database.get(name, "NOT_FOUND")):        
        database.pop(name)
        uf.status.setText(f"Delete button clicked: Existing User {name} deleted from the database.")

        with open(f'./json/{uf.BirthdetailsDB_filename}', 'w') as json_birthfile:
            json.dump(dict(database), json_birthfile, indent=4)
        
        uf.cmb_name.removeItem(uf.cmb_name.findText(name))
        uf.cmb_name.setCurrentText(name)
        
    else:
        uf.status.setText(f"Delete button clicked: User {name} doesnt exist in the database. So nothing to delete")

    return

# For Fetching below steps need to be followed
# 1. Read contents of birthdata json file as a dictionary
# 2. get user detail from dictionary of name in userform
# 3. update user values to userform

def fetchuser4mdb(uf):
    with open(f'./json/{uf.BirthdetailsDB_filename}', 'r') as json_birthfile:        
        database = json.loads(json_birthfile.read()) 
    
    name = str(uf.cmb_name.currentText()).strip()
    userdata = database.get(name, "NOT_FOUND")
    if ("NOT_FOUND" != userdata):
        uf.cmb_name.setCurrentText(userdata["name"])
        uf.cmb_gender.setCurrentText(userdata["gender"])
        hr = int(userdata["TOB"]["hour"])
        mn = int(userdata["TOB"]["min"])
        ss = int(userdata["TOB"]["sec"])
        uf.tob.setTime(QtCore.QTime(hr, mn, ss))
        yr = int(userdata["DOB"]["year"])
        mon = int(userdata["DOB"]["month"])
        day = int(userdata["DOB"]["day"])
        uf.dob.setDate(QtCore.QDate(yr, mon, day))
        uf.place.setText(userdata["POB"]["name"])
        uf.lon.setText(userdata["POB"]["lon"])
        uf.lat.setText(userdata["POB"]["lat"])
        uf.tz.setText(userdata["POB"]["timezone"])
        uf.comments.setPlainText(userdata["comments"])
        uf.status.setText(f"Fetch button clicked: User details of {name} are fetched from the database.")
    else:
        uf.status.setText(f"Fetch button clicked: No user called {name} in the database. So nothing is fetched.")
    return


    