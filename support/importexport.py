from PyQt5.QtWidgets import  QFileDialog
from PyQt5 import QtCore
import json

# For exporting below steps need to be followed
# 1. Fetch all user details from userform
# 2. Create a dictionary of that details
# 3. Pop up the destination directory selection windopw where jsm fiule needs to be stored
# 4. get the location and filename
# 5. Write dictionary into a text file by creating one and save it as jsm file in that directory

def export2jsm(uf):
    userdata = {}
    userdata["name"] = str(uf.cmb_name.currentText()).strip()
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
    print(userdata)

    file_dialog = QFileDialog()
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog  # Use the PyQt file dialog
    
    file_path, _ = file_dialog.getSaveFileName(options=options, filter="Jyotishyamitra files (*.jsm)")
    
    # Check if a file name was selected
    if file_path:
        file_path = file_path.replace(".jsm","")
        with open(f'{file_path}.jsm', 'w') as file:
            # Write your data to the file
            file.write(str(userdata))
    uf.status.setText(f"Export button clicked: User details exported in jsm format as {file_path}.jsm.")
    return


# For importing below steps need to be followed
# 1. Open file dialog and open the file
# 2. Read contents of jsm file as a dictionary
# 3. update dictionary values to userform

def import4mjsm(uf):
    file_dialog = QFileDialog()
    
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog  # Use the PyQt file dialog
    
    file_path, _ = file_dialog.getOpenFileName()
    try:
        with open(file_path, 'r') as file:
            content = file.read().strip()
            json_acceptable_string = content.replace("'", "\"")
            userdata = json.loads(json_acceptable_string)
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
            uf.status.setText(f"Import button clicked: User details of {userdata['name']} are imported from jsm file.")

    except FileNotFoundError:
        uf.status.setText(f"Import button clicked: File not found: {file_path}")
    except json.JSONDecodeError:
        uf.status.setText(f"Import button clicked: Error decoding JSON in the file: {file_path}")
    except Exception as e:
        uf.status.setText(f"Import button clicked: An error occurred: {e}")    
    return "Success"
