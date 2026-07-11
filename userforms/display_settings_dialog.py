from PyQt5 import QtCore, QtGui, QtWidgets
import support.display_settings_manager as ds_manager

class DisplaySettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DisplaySettingsDialog, self).__init__(parent)
        self.setWindowTitle("Display Settings")
        self.resize(450, 400)
        self.settings = ds_manager.get_settings()
        self.default_settings = ds_manager.get_default_settings()

        # Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Strategies Group
        self.group_strategies = QtWidgets.QGroupBox("Colour Coding Strategies")
        self.form_strategies = QtWidgets.QFormLayout(self.group_strategies)
        
        self.combo_natal = QtWidgets.QComboBox()
        self.combo_natal.addItem("planet_colourstrategy_dispositorRelation")
        self.form_strategies.addRow("Natal Planets Strategy:", self.combo_natal)

        self.combo_transit = QtWidgets.QComboBox()
        self.combo_transit.addItem("planet_colourstrategy_dispositorRelation")
        self.form_strategies.addRow("Transit Planets Strategy:", self.combo_transit)

        self.main_layout.addWidget(self.group_strategies)

        # Chart Colours Group
        self.group_colours = QtWidgets.QGroupBox("Chart Display Colours")
        self.form_colours = QtWidgets.QFormLayout(self.group_colours)

        self.btn_bg_colour = self._create_colour_btn()
        self.form_colours.addRow("Inner/Birth Chart Background Colour:", self.btn_bg_colour)
        self.btn_bg_colour.clicked.connect(lambda: self._choose_colour(self.btn_bg_colour, "chart_background_colour"))

        self.btn_outer_bg_colour = self._create_colour_btn()
        self.form_colours.addRow("Mixed Chart Background Colour:", self.btn_outer_bg_colour)
        self.btn_outer_bg_colour.clicked.connect(lambda: self._choose_colour(self.btn_outer_bg_colour, "chart_outer_background_colour"))

        self.btn_outbox_colour = self._create_colour_btn()
        self.form_colours.addRow("Outer Box Colour:", self.btn_outbox_colour)
        self.btn_outbox_colour.clicked.connect(lambda: self._choose_colour(self.btn_outbox_colour, "chart_outerbox_colour"))

        self.btn_inbox_colour = self._create_colour_btn()
        self.form_colours.addRow("Inner Box Colour (South Chart):", self.btn_inbox_colour)
        self.btn_inbox_colour.clicked.connect(lambda: self._choose_colour(self.btn_inbox_colour, "chart_innerbox_colour"))

        self.btn_line_colour = self._create_colour_btn()
        self.form_colours.addRow("Line Colour:", self.btn_line_colour)
        self.btn_line_colour.clicked.connect(lambda: self._choose_colour(self.btn_line_colour, "chart_line_colour"))

        self.btn_sign_colour = self._create_colour_btn()
        self.form_colours.addRow("Sign/Ascendant Marker Colour:", self.btn_sign_colour)
        self.btn_sign_colour.clicked.connect(lambda: self._choose_colour(self.btn_sign_colour, "chart_sign_colour"))

        self.main_layout.addWidget(self.group_colours)

        # Buttons
        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.btn_restore = QtWidgets.QPushButton("Restore Defaults")
        self.btn_save = QtWidgets.QPushButton("Save")
        self.btn_cancel = QtWidgets.QPushButton("Cancel")
        
        self.layout_buttons.addWidget(self.btn_restore)
        self.layout_buttons.addStretch()
        self.layout_buttons.addWidget(self.btn_save)
        self.layout_buttons.addWidget(self.btn_cancel)

        self.main_layout.addLayout(self.layout_buttons)

        # Connections
        self.btn_restore.clicked.connect(self.restore_defaults)
        self.btn_save.clicked.connect(self.save_settings)
        self.btn_cancel.clicked.connect(self.reject)

        self.load_ui_from_settings()

    def _create_colour_btn(self):
        btn = QtWidgets.QPushButton()
        btn.setFixedSize(60, 25)
        return btn

    def _set_btn_colour(self, btn, colour_name):
        btn.setStyleSheet(f"background-color: {colour_name}; border: 1px solid #777;")
        # Save as custom property to easily retrieve later
        btn.setProperty("current_colour", colour_name)

    def _choose_colour(self, btn, key):
        initial = btn.property("current_colour")
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(initial), self, "Select Colour")
        if color.isValid():
            name = color.name() # e.g. #ff0000
            self._set_btn_colour(btn, name)
            self.settings[key] = name

    def load_ui_from_settings(self):
        # Set combo boxes
        index = self.combo_natal.findText(self.settings.get("natal_colour_strategy", ""))
        if index >= 0: self.combo_natal.setCurrentIndex(index)
        
        index = self.combo_transit.findText(self.settings.get("transit_colour_strategy", ""))
        if index >= 0: self.combo_transit.setCurrentIndex(index)

        # Set color buttons
        self._set_btn_colour(self.btn_bg_colour, self.settings.get("chart_background_colour", "black"))
        self._set_btn_colour(self.btn_outer_bg_colour, self.settings.get("chart_outer_background_colour", "black"))
        self._set_btn_colour(self.btn_outbox_colour, self.settings.get("chart_outerbox_colour", "red"))
        self._set_btn_colour(self.btn_inbox_colour, self.settings.get("chart_innerbox_colour", "red"))
        self._set_btn_colour(self.btn_line_colour, self.settings.get("chart_line_colour", "yellow"))
        self._set_btn_colour(self.btn_sign_colour, self.settings.get("chart_sign_colour", "pink"))

    def restore_defaults(self):
        self.settings = self.default_settings.copy()
        self.load_ui_from_settings()

    def save_settings(self):
        self.settings["natal_colour_strategy"] = self.combo_natal.currentText()
        self.settings["transit_colour_strategy"] = self.combo_transit.currentText()
        ds_manager.save_settings(self.settings)
        self.accept()
