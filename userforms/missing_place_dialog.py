from PyQt5 import QtCore, QtGui, QtWidgets

class MissingPlaceDialog(QtWidgets.QDialog):
    def __init__(self, initial_name="", parent=None):
        super(MissingPlaceDialog, self).__init__(parent)
        self.setWindowTitle("Add New Place")
        self.resize(400, 250)
        
        layout = QtWidgets.QVBoxLayout(self)
        
        info_label = QtWidgets.QLabel("The place you entered was not found.\\nPlease enter the coordinates to add it to the database.")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        form_layout = QtWidgets.QFormLayout()
        
        self.edit_name = QtWidgets.QLineEdit()
        self.edit_name.setText(initial_name)
        form_layout.addRow("Place Name:", self.edit_name)
        
        self.edit_lat = QtWidgets.QLineEdit()
        self.edit_lat.setPlaceholderText("e.g. 14.2798")
        form_layout.addRow("Latitude:", self.edit_lat)
        
        self.edit_lon = QtWidgets.QLineEdit()
        self.edit_lon.setPlaceholderText("e.g. 74.4439")
        form_layout.addRow("Longitude:", self.edit_lon)
        
        self.edit_tz = QtWidgets.QLineEdit()
        self.edit_tz.setPlaceholderText("e.g. +05:30")
        form_layout.addRow("Timezone:", self.edit_tz)
        
        self.edit_tzname = QtWidgets.QLineEdit()
        self.edit_tzname.setPlaceholderText("e.g. Asia/Kolkata (Optional)")
        form_layout.addRow("Timezone Name:", self.edit_tzname)
        
        layout.addLayout(form_layout)
        
        button_layout = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Add Place")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_cancel)
        layout.addLayout(button_layout)
        
        # Connections
        self.btn_add.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        
    def get_details(self):
        return {
            "name": self.edit_name.text().strip(),
            "lat": self.edit_lat.text().strip(),
            "lon": self.edit_lon.text().strip(),
            "timezone": self.edit_tz.text().strip(),
            "timezone_name": self.edit_tzname.text().strip()
        }
