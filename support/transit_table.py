import sys
import copy
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import swisseph as swe
from datetime import datetime, timedelta
import support.globalvariables as gvar
import support.generic as gen
import support.gocharphal as gp

# Define the BAV Bindu Matrix as per Phaladeepika.
# Each dictionary represents the positions (1-indexed) from a reference planet
# where the transiting planet contributes a bindu.
BAV_BINDU_MATRIX = {
    "Sun": {
        "Sun": [1, 2, 4, 7, 8, 9, 10, 11],
        "Moon": [3, 6, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [5, 6, 9, 11],
        "Venus": [6, 7, 12],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [3, 4, 6, 10, 11, 12]
    },
    "Moon": {
        "Sun": [3, 6, 7, 8, 10, 11],
        "Moon": [1, 3, 6, 7, 10, 11],
        "Mars": [2, 3, 5, 6, 9, 10, 11],
        "Mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "Jupiter": [1, 4, 7, 8, 10, 11, 12],
        "Venus": [3, 4, 5, 7, 9, 10, 11],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [3, 6, 10, 11]
    },
    "Mars": {
        "Sun": [3, 5, 6, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [3, 5, 6, 11],
        "Jupiter": [6, 10, 11, 12],
        "Venus": [6, 8, 11, 12],
        "Saturn": [1, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 3, 6, 10, 11]
    },
    "Mercury": {
        "Sun": [5, 6, 9, 11, 12],
        "Moon": [2, 4, 6, 8, 10, 11],
        "Mars": [1, 2, 4, 7, 8, 9, 10, 11],
        "Mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "Jupiter": [6, 8, 11, 12],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 11],
        "Saturn": [1, 2, 4, 7, 8, 9, 10, 11],
        "Ascendant": [1, 2, 4, 6, 8, 10, 11]
    },
    "Jupiter": {
        "Sun": [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "Moon": [2, 5, 7, 9, 11],
        "Mars": [1, 2, 4, 7, 8, 10, 11],
        "Mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "Jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "Venus": [2, 5, 6, 9, 10, 11],
        "Saturn": [3, 5, 6, 12],
        "Ascendant": [1, 2, 4, 5, 6, 9, 10, 11]
    },
    "Venus": {
        "Sun": [8, 11, 12],
        "Moon": [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "Mars": [3, 5, 6, 9, 11, 12],
        "Mercury": [3, 5, 6, 9, 11],
        "Jupiter": [5, 8, 9, 10, 11],
        "Venus": [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "Saturn": [3, 4, 5, 8, 9, 10, 11],
        "Ascendant": [1, 2, 3, 4, 5, 8, 9, 11]
    },
    "Saturn": {
        "Sun": [1, 2, 4, 7, 8, 10, 11],
        "Moon": [3, 6, 11],
        "Mars": [3, 5, 6, 10, 11],
        "Mercury": [6, 8, 9, 10, 11, 12],
        "Jupiter": [5, 6, 11, 12],
        "Venus": [6, 11, 12],
        "Saturn": [3, 5, 6, 11],
        "Ascendant": [1, 3, 4, 6, 10, 11]
    }
}

# Mapping Kakshya index (0-7) to its lord
KAKSHYA_LORDS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon", "Ascendant"]

def get_avastha(sign_name, degree):
    """
    Calculate Avastha based on Odd/Even signs and planet degrees.
    Odd Signs: Aries, Gemini, Leo, Libra, Sagittarius, Aquarius
    Even Signs: Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces
    """
    odd_signs = ["Aries", "Gemini", "Leo", "Libra", "Sagittarius", "Aquarius"]
    
    # 5 blocks of 6 degrees
    if 0 <= degree < 6:
        block = 0
    elif 6 <= degree < 12:
        block = 1
    elif 12 <= degree < 18:
        block = 2
    elif 18 <= degree < 24:
        block = 3
    else:
        block = 4
        
    if sign_name in odd_signs:
        avasthas = [
            ("Bala", "pink"),
            ("Kumara", "lightgreen"),
            ("Yuva", "darkgreen"),
            ("Vriddha", "black"),
            ("Mrit", "red")
        ]
    else:
        avasthas = [
            ("Mrit", "red"),
            ("Vriddha", "black"),
            ("Yuva", "darkgreen"),
            ("Kumara", "lightgreen"),
            ("Bala", "pink")
        ]
        
    return avasthas[block]

def get_moorthy_nirnaya(planet, current_transit_astrodata, natal_moon_sign):
    """
    Computes Moorthy Nirnaya by backtracking to find when the planet entered its 
    current sign, finding the Transit Moon at that exact time, and comparing it 
    with the Natal Moon.
    Returns a tuple: (Moorthy_Name, Color)
    """
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    
    planet_map = {
        "Sun": swe.SUN, "Moon": swe.MOON, "Mars": swe.MARS,
        "Mercury": swe.MERCURY, "Jupiter": swe.JUPITER, "Venus": swe.VENUS,
        "Saturn": swe.SATURN, "Rahu": swe.TRUE_NODE, "Ketu": swe.TRUE_NODE  # Ketu is opposite to Rahu
    }
    
    if planet not in planet_map:
        return ("Unknown", "black")
        
    swe_planet = planet_map[planet]
    
    # Base transit date
    dob = gvar.transit_userdata["DOB"]
    tob = gvar.transit_userdata["TOB"]
    
    # Create datetime of the transit
    dt = datetime(int(dob["year"]), int(dob["month"]), int(dob["day"]),
                  int(tob["hour"]), int(tob["min"]), int(tob["sec"]))
                  
    jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60.0 + dt.second/3600.0)
    
    # Get current planet pos
    pos, _ = swe.calc_ut(jd, swe_planet)
    current_lon = pos[0]
    
    # Adjust for Ketu
    if planet == "Ketu":
        current_lon = (current_lon + 180.0) % 360.0
        
    # Get the ayanamsa to find sidereal longitude (Lahiri)
    ayanamsa = swe.get_ayanamsa_ut(jd)
    sidereal_lon = (current_lon - ayanamsa) % 360.0
    
    current_sign_idx = int(sidereal_lon / 30.0)
    
    # Backtrack to find when it crossed into this sign
    # We step back 1 day at a time until the sign changes
    step_jd = jd
    for i in range(7000):  # Safety limit (Saturn takes ~2.5 years = ~900 days)
        step_jd -= 1.0
        pos, _ = swe.calc_ut(step_jd, swe_planet)
        lon = pos[0]
        if planet == "Ketu":
            lon = (lon + 180.0) % 360.0
        ayan = swe.get_ayanamsa_ut(step_jd)
        s_lon = (lon - ayan) % 360.0
        if int(s_lon / 30.0) != current_sign_idx:
            break
            
    # Now we know the transition happened between step_jd and step_jd + 1.0
    # Binary search for exact entry time
    jd_left = step_jd
    jd_right = step_jd + 1.0
    
    for _ in range(20): # 20 iterations is precise enough
        jd_mid = (jd_left + jd_right) / 2.0
        pos, _ = swe.calc_ut(jd_mid, swe_planet)
        lon = pos[0]
        if planet == "Ketu":
            lon = (lon + 180.0) % 360.0
        ayan = swe.get_ayanamsa_ut(jd_mid)
        s_lon = (lon - ayan) % 360.0
        if int(s_lon / 30.0) == current_sign_idx:
            jd_right = jd_mid
        else:
            jd_left = jd_mid
            
    entry_jd = jd_right
    
    # Find Transit Moon at entry_jd
    moon_pos, _ = swe.calc_ut(entry_jd, swe.MOON)
    moon_ayan = swe.get_ayanamsa_ut(entry_jd)
    transit_moon_lon = (moon_pos[0] - moon_ayan) % 360.0
    transit_moon_sign_idx = int(transit_moon_lon / 30.0)
    
    # Find natal moon sign index
    natal_moon_sign_idx = gen.signnum(natal_moon_sign) - 1
    
    # Calculate distance from natal moon to transit moon
    moon_diff = ((transit_moon_sign_idx - natal_moon_sign_idx) % 12) + 1
    
    if moon_diff in [1, 6, 11]:
        return ("Swarna (Gold)", "#FFD700")
    elif moon_diff in [2, 5, 9]:
        return ("Rajata (Silver)", "#C0C0C0")
    elif moon_diff in [3, 7, 10]:
        return ("Tamra (Copper)", "#B87333")
    else:
        return ("Loha (Iron)", "#434B4D")

def get_bav_color(points):
    """Returns color based on BAV points score."""
    colors = {
        8: "#005A00", 7: "#008000", 6: "#228B22", 5: "#6B8E23",
        4: "#B8860B", 3: "#D2691E", 2: "#C83200", 1: "#B22222", 0: "#8B0000"
    }
    return colors.get(points, "#000000")

def get_sav_color(points):
    """Returns color based on SAV points score."""
    if points >= 36: return "#005A00"
    if 33 <= points <= 35: return "#008000"
    if 29 <= points <= 32: return "#6B8E23"
    if 25 <= points <= 28: return "#B8860B"
    if 20 <= points <= 24: return "#D2691E"
    if 16 <= points <= 19: return "#B22222"
    return "#8B0000"

def get_pav_contribution(transiting_planet, transiting_house_num, kakshya_lord, astrodata):
    """
    Check if the Kakshya lord contributes a bindu to the transiting planet's BAV 
    in the transiting house.
    transiting_house_num: The house number (1-12) the planet is currently transiting, relative to Ascendant.
    """
    if transiting_planet not in BAV_BINDU_MATRIX:
        return False
        
    matrix = BAV_BINDU_MATRIX[transiting_planet]
    if kakshya_lord not in matrix:
        return False
        
    contributing_positions = matrix[kakshya_lord]
    
    # We need to find the sign/house of the Kakshya lord in the NATAL chart.
    if kakshya_lord == "Ascendant":
        lord_sign = astrodata["D1"]["ascendant"]["sign"]
    else:
        lord_sign = astrodata["D1"]["planets"][kakshya_lord]["sign"]
        
    lord_sign_num = gen.signnum(lord_sign)
    
    # Difference (relative position)
    rel_pos = gen.housediff(lord_sign_num, transiting_house_num)
    
    return rel_pos in contributing_positions

class TransitTableWindow(QtWidgets.QWidget):
    def __init__(self, astrodata, transit_astrodata, current_dasha, inner_div="D1", outer_div="D1"):
        super().__init__()
        self.astrodata = astrodata
        self.transit_astrodata = transit_astrodata
        self.current_dasha = current_dasha
        self.inner_div = inner_div
        self.outer_div = outer_div
        
        self.setWindowTitle("Transit Table")
        self.resize(1100, 450)
        
        # White background preferred
        self.setStyleSheet("background-color: white; color: black;")
        
        layout = QtWidgets.QVBoxLayout(self)
        
        # Checkbox layout for planet columns
        self.checkbox_layout = QtWidgets.QHBoxLayout()
        
        # Learn Button
        self.learn_btn = QtWidgets.QPushButton("Learn")
        self.learn_btn.setStyleSheet("background-color: #e0f7fa; border: 1px solid #00acc1; padding: 5px; font-weight: bold; color: #006064;")
        self.learn_btn.clicked.connect(self.open_learn_document)
        self.checkbox_layout.addWidget(self.learn_btn)
        
        # Spacer
        self.checkbox_layout.addSpacing(20)
        
        self.checkboxes = {}
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        for i, p in enumerate(planets):
            cb = QtWidgets.QCheckBox(p)
            cb.setChecked(True)
            cb.stateChanged.connect(lambda state, col=i+1: self.toggle_column(col, state))
            self.checkbox_layout.addWidget(cb)
            self.checkboxes[p] = cb
            
        self.checkbox_layout.addStretch()
            
        layout.addLayout(self.checkbox_layout)
        
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)
        
        self.setup_table()
        self.populate_data()
        
        # Auto-size the columns to content first, then window
        self.table.resizeColumnsToContents()
        self.adjust_window_size()
        
    def toggle_column(self, col, state):
        if state == Qt.Checked:
            self.table.showColumn(col)
        else:
            self.table.hideColumn(col)
        self.adjust_window_size()
        
    def adjust_window_size(self):
        QtWidgets.QApplication.processEvents()
        width = self.table.verticalHeader().width() if not self.table.verticalHeader().isHidden() else 0
        for i in range(self.table.columnCount()):
            if not self.table.isColumnHidden(i):
                width += self.table.columnWidth(i)
        
        # Add padding
        width += 40
        self.resize(width, self.height())
        
    def open_learn_document(self):
        try:
            import os
            import markdown
            doc_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Learn", "transits_masterclass.md")
            
            with open(doc_path, "r", encoding="utf-8") as f:
                md_text = f.read()
                
            html = markdown.markdown(md_text, extensions=['extra'])
            
            self.learn_window = QtWidgets.QWidget()
            self.learn_window.setWindowTitle("Transits Masterclass")
            self.learn_window.resize(800, 600)
            layout = QtWidgets.QVBoxLayout(self.learn_window)
            
            text_browser = QtWidgets.QTextBrowser()
            text_browser.setHtml(html)
            text_browser.setOpenExternalLinks(True)
            
            layout.addWidget(text_browser)
            self.learn_window.show()
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Error", f"Could not load Learn document: {e}")
        
    def setup_table(self):
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        headers = ["Property"] + planets
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(False)
        
    def get_dasha_color(self, planet):
        """Color code planet font based on Mahadasha, Bhukti, Pratyantar"""
        if not self.current_dasha:
            return "black"
        md = self.current_dasha.get("MD", "")
        ad = self.current_dasha.get("AD", "")
        pd = self.current_dasha.get("PD", "")
        
        if planet == md:
            return "darkgreen"
        elif planet == ad:
            return "blue"
        elif planet == pd:
            return "lightblue"
        return "black"

    def populate_data(self):
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        properties = [
            "Natal Avastha", "Transit Avastha", "Degree", "Phaladeepika Gochar", 
            "Vedh", "Vipareet Vedh", "Moorthy Nirnaya", "Kakshya", "PAV Bindu", 
            "BAV", "SAV"
        ]
        self.table.setRowCount(len(properties))
        
        # Populate Property names in the first column
        for row, prop in enumerate(properties):
            item = QtWidgets.QTableWidgetItem(prop)
            font = item.font()
            font.setBold(True)
            item.setFont(font)
            item.setBackground(QtGui.QColor("#f0f0f0")) # subtle gray background
            self.table.setItem(row, 0, item)
            
        # Color code the header for planets based on Dasha
        for col_idx, p in enumerate(planets):
            col = col_idx + 1
            header_item = QtWidgets.QTableWidgetItem(p)
            header_item.setForeground(QtGui.QColor(self.get_dasha_color(p)))
            font = header_item.font()
            font.setBold(True)
            header_item.setFont(font)
            self.table.setHorizontalHeaderItem(col, header_item)
            
        natal_moon_sign = self.astrodata[self.inner_div]["planets"]["Moon"]["sign"]
        
        for col_idx, p in enumerate(planets):
            col = col_idx + 1
            font = QtGui.QFont()
            font.setBold(True)
            
            # 0. Natal Avastha
            n_sign = self.astrodata[self.inner_div]["planets"][p]["sign"]
            n_pos = self.astrodata[self.inner_div]["planets"][p]["pos"]
            n_deg = float(n_pos["deg"]) + float(n_pos["min"])/60.0
            n_avastha, n_av_col = get_avastha(n_sign, n_deg)
            item_n_av = QtWidgets.QTableWidgetItem(n_avastha)
            item_n_av.setForeground(QtGui.QColor(n_av_col))
            item_n_av.setFont(font)
            self.table.setItem(0, col, item_n_av)
            
            # 1. Transit Avastha & 2. Degree
            t_sign = self.transit_astrodata[self.outer_div]["planets"][p]["sign"]
            t_pos = self.transit_astrodata[self.outer_div]["planets"][p]["pos"]
            t_deg = float(t_pos["deg"]) + float(t_pos["min"])/60.0
            t_avastha, t_av_col = get_avastha(t_sign, t_deg)
            
            item_t_av = QtWidgets.QTableWidgetItem(t_avastha)
            item_t_av.setForeground(QtGui.QColor(t_av_col))
            item_t_av.setFont(font)
            self.table.setItem(1, col, item_t_av)
            
            item_deg = QtWidgets.QTableWidgetItem(f"{t_sign[:3]} {int(t_pos['deg'])}° {int(t_pos['min'])}'")
            self.table.setItem(2, col, item_deg)
            
            # 3. Phaladeepika, 4. Vedh, 5. Vipareet Vedh
            gochar_details = gp.get_gocharphal_details(p, natal_moon_sign, self.transit_astrodata)
            phal_col = gochar_details["phal_colour"]
            
            item_phal = QtWidgets.QTableWidgetItem("Shubha" if phal_col == gp.SHUBHPHAL else "Ashubha" if phal_col == gp.ASHUBHPHAL else "Neutral")
            if phal_col == gp.SHUBHPHAL:
                item_phal.setForeground(QtGui.QColor("green"))
            elif phal_col == gp.ASHUBHPHAL:
                item_phal.setForeground(QtGui.QColor("red"))
            else:
                item_phal.setForeground(QtGui.QColor("orange"))
            item_phal.setFont(font)
            self.table.setItem(3, col, item_phal)
            
            # 4. Vedh
            item_vedh = QtWidgets.QTableWidgetItem("✓" if gochar_details["is_vedh"] else "✗")
            item_vedh.setForeground(QtGui.QColor("green" if gochar_details["is_vedh"] else "red"))
            item_vedh.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(4, col, item_vedh)
            
            # 5. Vipareet Vedh
            item_vvedh = QtWidgets.QTableWidgetItem("✓" if gochar_details["is_vipareet_vedh"] else "✗")
            item_vvedh.setForeground(QtGui.QColor("green" if gochar_details["is_vipareet_vedh"] else "red"))
            item_vvedh.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(5, col, item_vvedh)
            
            # 6. Moorthy Nirnaya
            mn_name, mn_col = get_moorthy_nirnaya(p, self.transit_astrodata, natal_moon_sign)
            item_mn = QtWidgets.QTableWidgetItem(mn_name)
            item_mn.setForeground(QtGui.QColor(mn_col))
            item_mn.setFont(font)
            self.table.setItem(6, col, item_mn)
            
            # 7. Kakshya
            kakshya_idx = int(t_deg / 3.75)
            if kakshya_idx > 7: kakshya_idx = 7
            k_lord = KAKSHYA_LORDS[kakshya_idx]
            self.table.setItem(7, col, QtWidgets.QTableWidgetItem(k_lord))
            
            # 8. PAV Bindu, 9. BAV, 10. SAV
            transit_sign_num = gen.signnum(t_sign)
            bav_val = "-"
            sav_val = "-"
            has_bindu = False
            
            if "AshtakaVarga" in self.astrodata:
                # BAV
                if p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
                    bav_list = self.astrodata["AshtakaVarga"].get(p, [])
                    if len(bav_list) == 12:
                        bav_score = bav_list[transit_sign_num - 1]
                        bav_val = str(bav_score)
                        item_bav = QtWidgets.QTableWidgetItem(bav_val)
                        item_bav.setForeground(QtGui.QColor(get_bav_color(bav_score)))
                        item_bav.setFont(font)
                        item_bav.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(9, col, item_bav)
                        
                        # PAV check
                        has_bindu = get_pav_contribution(p, transit_sign_num, k_lord, self.astrodata)
                else:
                    self.table.setItem(9, col, QtWidgets.QTableWidgetItem("-"))
                
                # SAV
                sav_list = self.astrodata["AshtakaVarga"].get("Total", [])
                if len(sav_list) == 12:
                    sav_score = sav_list[transit_sign_num - 1]
                    sav_val = str(sav_score)
                    item_sav = QtWidgets.QTableWidgetItem(sav_val)
                    item_sav.setForeground(QtGui.QColor(get_sav_color(sav_score)))
                    item_sav.setFont(font)
                    item_sav.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(10, col, item_sav)
                else:
                    self.table.setItem(10, col, QtWidgets.QTableWidgetItem("-"))
            else:
                self.table.setItem(9, col, QtWidgets.QTableWidgetItem("-"))
                self.table.setItem(10, col, QtWidgets.QTableWidgetItem("-"))
                
            # PAV
            if p in ["Rahu", "Ketu"]:
                item_pav = QtWidgets.QTableWidgetItem("-")
            else:
                item_pav = QtWidgets.QTableWidgetItem("✓" if has_bindu else "✗")
                item_pav.setForeground(QtGui.QColor("green" if has_bindu else "red"))
            item_pav.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(8, col, item_pav)
