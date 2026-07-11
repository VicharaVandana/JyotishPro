# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import QDate, QTime
from mainwindow_designer import Ui_MainWindow
import support.generic as gen
import support.importexport as ie
import support.adddeletefetch as ad
import support.astrocalculations as astrocalc
import support.astrochart as chart
import support.globalvariables as gvar
import json
import os
from datetime import datetime

import support.dashascalculation as dashavim
import support.balascalculation as shadbal
import support.places_manager as places_manager
import userforms.missing_place_dialog as missing_place_dialog

import support.prediction_experiments as trial
import support.transit_table as trans_tab

class _ResizeEventFilter(QtCore.QObject):
    """Event filter installed on the real QMainWindow to catch resize events
    and relay them to the MainWindow_cls so charts can be refitted."""

    def __init__(self, ui_owner):
        super().__init__()
        self._ui = ui_owner

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Resize:
            # Delay fitInView slightly so the layout has settled into new sizes
            QtCore.QTimer.singleShot(20, self._ui._fit_charts_in_view)
        return False  # Don't consume the event



class MainWindow_cls(Ui_MainWindow):
    def setupUi_main(self, MainWindow):
        self.setupUi(MainWindow)
        self._mainWindow = MainWindow  # Store reference for event filter
        MainWindow.resize(1300, 700)
        
        # Expand Mixed Chart graphics view dynamically
        self.horizontalLayout_mixedChart.setStretch(0, 7)
        self.horizontalLayout_mixedChart.setStretch(1, 3)

        # Setup translation engine
        self.translator = QtCore.QTranslator()

        self.BirthdetailsDB_filename = self.read_input_birthdataDbFileName()
        self.label_DivDetails.setText(chart.get_division_signification("D1"))
        self.mainchart_planetdetails.setText("CLICK PLANETS TO LOAD ITS DETAILS")
        progress_value = 0
        self.progressBar_planetshadbala.setValue(int(progress_value))
        self.progressBar_planetshadbala.setFormat("%d%%" % progress_value)
        self.dateEdit_transitdate.setDate(QDate.currentDate())
        self.timeEdit_transittime.setTime(QTime.currentTime())
        self.comboBox_DashaSeedPlanet.setCurrentText("Moon")
        self.birthchart.setEnabled(False)
        self.mixedcharttab.setEnabled(False)
        

        # Populate combobox with user names
        with open(f'./json/{self.BirthdetailsDB_filename}', 'r') as json_birthfile:        
            database = json.loads(json_birthfile.read())
        userlist = list(database.keys())
        self.cmb_name.addItems(userlist)

        # Create a QGraphicsScene for the QGraphicsView
        self.mainchartScene = QGraphicsScene()
        self.MainChart.setScene(self.mainchartScene)

        self.mixedchartScene = QGraphicsScene()
        self.graphicsView_MixedChart.setScene(self.mixedchartScene)

        # Make both chart views maintain a square aspect by using a size policy
        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sp.setHeightForWidth(True)
        self.MainChart.setSizePolicy(sp)
        self.graphicsView_MixedChart.setSizePolicy(sp)

        # Install event filter on the real QMainWindow to catch resize events
        self._event_filter = _ResizeEventFilter(self)
        MainWindow.installEventFilter(self._event_filter)

        # Tab highlight styling
        self.user.setStyleSheet("""
            QTabBar::tab {
                padding: 6px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: rgb(180, 220, 255);
            }
            QTabBar::tab:!selected {
                background-color: rgb(230, 230, 230);
            }
            QTabBar::tab:hover {
                background-color: rgb(200, 235, 255);
            }
        """)

        # Signals and Slots
        self.btn_export.clicked.connect(lambda: ie.export2jsm(self))
        self.btn_import.clicked.connect(lambda: ie.import4mjsm(self))
        self.btn_add.clicked.connect(lambda: ad.adduser2db(self))
        self.btn_delete.clicked.connect(lambda: ad.deluser4mdb(self))
        self.btn_fetch.clicked.connect(lambda: ad.fetchuser4mdb(self))
        self.btn_submit.clicked.connect(lambda: self.submitdetails())

        #button actions for planet details on Main chart
        self.pushButton_Sun.clicked.connect(lambda:self.load_planetdetails("Sun"))
        self.pushButton_Moon.clicked.connect(lambda: self.load_planetdetails("Moon"))
        self.pushButton_Mars.clicked.connect(lambda: self.load_planetdetails("Mars"))
        self.pushButton_Mercury.clicked.connect(lambda: self.load_planetdetails("Mercury"))
        self.pushButton_Jupiter.clicked.connect(lambda: self.load_planetdetails("Jupiter"))
        self.pushButton_Venus.clicked.connect(lambda: self.load_planetdetails("Venus"))
        self.pushButton_Saturn.clicked.connect(lambda: self.load_planetdetails("Saturn"))
        self.pushButton_Rahu.clicked.connect(lambda: self.load_planetdetails("Rahu"))
        self.pushButton_Ketu.clicked.connect(lambda: self.load_planetdetails("Ketu"))
        self.pushButton_Ascendant.clicked.connect(lambda: self.load_planetdetails("Ascendant"))

        self.comboBox_ChartDivision.currentIndexChanged.connect(self.on_chart_division_changed)
        self.comboBox_firsthouse.currentIndexChanged.connect(self.on_chart_parameters_changed)
        self.checkBox_aspects.stateChanged.connect(self.on_chart_parameters_changed)

        # Language & Chart Style selection
        self.cmb_language.currentIndexChanged.connect(self.on_display_settings_changed)
        self.cmb_chartStyle.currentIndexChanged.connect(self.on_display_settings_changed)

        #Actions for items on Mixed charts Window
        self.comboBox_outerChartType.currentIndexChanged.connect(self.on_outerChartType_changed)
        self.comboBox_MixedChart_firsthousesign.currentIndexChanged.connect(self.on_mixedchart_parameters_changed)
        self.comboBox_innerChartDivision.currentIndexChanged.connect(self.on_innerchart_division_changed)
        self.comboBox_outerChartDivision.currentIndexChanged.connect(self.on_mixedchart_parameters_changed)
        self.checkBox_innerAspects.stateChanged.connect(self.on_mixedchart_parameters_changed)
        self.checkBox_outerAspects.stateChanged.connect(self.on_mixedchart_parameters_changed)

        self.dateEdit_transitdate.dateChanged.connect(self.on_transitdate_time_changed) 
        self.timeEdit_transittime.timeChanged.connect(self.on_transitdate_time_changed) 
        
        self.comboBox_DashaDivision.currentIndexChanged.connect(lambda: self.update_DashaDetails_in_MixedchartLabel_transit(gvar.astrodata, gvar.transit_astrodata))
        self.comboBox_DashaSeedPlanet.currentIndexChanged.connect(lambda: self.update_DashaDetails_in_MixedchartLabel_transit(gvar.astrodata, gvar.transit_astrodata))
        
        #Trial parts for experimentation
        self.pushButton_transit_dashaTable.clicked.connect(self.show_transitdasha_Table)
        self.pushButton_transitTable.clicked.connect(self.show_transit_table)

        #Action Menu Items Linking
        self.actionPersonal.triggered.connect(lambda: self.update_settings_json("personal_birthdata_db.json"))
        self.actionCelebrity.triggered.connect(lambda: self.update_settings_json("celebrity_birthdata_db.json"))
        self.actionDisplay_Settings.triggered.connect(self.open_display_settings)

        # PDF Report Tab Connections
        self.btn_browseLocation.clicked.connect(self.browse_save_location)
        self.cmb_name.currentTextChanged.connect(self.update_report_name)
        
        self.btn_selectAll.clicked.connect(lambda: self.set_all_pdf_checkboxes(True))
        self.btn_deselectAll.clicked.connect(lambda: self.set_all_pdf_checkboxes(False))
        
        self.chk_yogasDoshas.toggled.connect(self.on_yogas_doshas_toggled)
        self.on_yogas_doshas_toggled(self.chk_yogasDoshas.isChecked()) # initial state
        
        self.btn_generateReport.clicked.connect(self.generate_report_workflow)
        
        # Initialize report name on startup
        if self.cmb_name.count() > 0:
            self.update_report_name(self.cmb_name.currentText())

        # Refit charts whenever the user switches tabs (charts may have been
        # loaded while their tab was hidden, so fitInView used a stale size)
        self.user.currentChanged.connect(self._on_tab_changed)


        # Place of Birth auto-suggest and loading setup
        self.btn_loadPlace.clicked.connect(self.on_load_place_clicked)
        places_manager.load_places_async()
        self.check_places_loaded()

        QtWidgets.QApplication.processEvents()
        return
    
    def read_input_birthdataDbFileName(self):
        json_file = "./json/settings.json"

        try:
            # Read current JSON data
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Update the parameter
            inputfilename = data["inputDB_filename"]

        except Exception as e:
            self.status.setText(f"Failed to read settings Birthdata Database file name:\n{e}")
            inputfilename = "personal_birthdata_db.json"

        return inputfilename
    
    def update_settings_json(self, new_filename = "personal_birthdata_db.json"):
        """Updates settings.json with new inputDB_filename"""
        json_file = "./json/settings.json"

        try:
            # Read current JSON data
            with open(json_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Update the parameter
            data["inputDB_filename"] = new_filename

            # Write back to file
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            self.status.setText("Settings updated successfully!")

            #self.setupUi_main()
        
        except Exception as e:
            self.status.setText(f"Failed to update settings:\n{e}")

        return
    
    def show_transit_table(self):
        self.status.setText("Loading Transit Table...")
        QtWidgets.QApplication.processEvents()
        try:
            idx_planet = self.comboBox_DashaSeedPlanet.currentIndex()
            planet_keys = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
            planet_name = planet_keys[idx_planet] if idx_planet >= 0 else "Moon"
            dasha_div = self.comboBox_DashaDivision.currentText()
            
            dasha_dict = dashavim.get_dasha_dict_fordate(gvar.astrodata, gvar.transit_astrodata, dasha_div, planet_name)
            
            innerDiv = self.comboBox_innerChartDivision.currentText()
            outerDiv = self.comboBox_outerChartDivision.currentText()
            self.transit_window = trans_tab.TransitTableWindow(gvar.astrodata, gvar.transit_astrodata, dasha_dict, innerDiv, outerDiv)
            self.transit_window.show()
            self.status.setText("Transit Table displayed successfully.")
        except Exception as e:
            self.status.setText(f"Failed to load Transit Table: {e}")

    def show_transitdasha_Table(self):
        self.status.setText("Loading Dasha Transit Table...")
        QtWidgets.QApplication.processEvents()
        # Example Data (Replace this with actual dasha_transit_table_dict)
        dasha_transit_table_dict = dashavim.get_dashaplanet_tabletransit_fordate(gvar.astrodata, gvar.transit_astrodata, self.comboBox_outerChartDivision.currentText())

        self.dasha_window = trial.DashaTransitTableWindow(dasha_transit_table_dict)
        self.dasha_window.show()
        self.status.setText("Dasha Transit Table displayed successfully.")
    
    def on_display_settings_changed(self, _index=0):
        """Called when Language or Chart Style combo changes in UserDetails tab.
        Updates global preferences and redraws any currently-loaded charts."""
        lang_keys = ["english", "kannada", "hindi"]
        style_keys = ["north", "south"]

        idx_lang = self.cmb_language.currentIndex()
        gvar.chart_language = lang_keys[idx_lang] if idx_lang >= 0 else "english"
        
        idx_style = self.cmb_chartStyle.currentIndex()
        gvar.chart_style = style_keys[idx_style] if idx_style >= 0 else "north"

        # Handle UI translation dynamically
        app = QtWidgets.QApplication.instance()
        if gvar.chart_language != "english":
            qm_path = os.path.join(os.path.dirname(__file__), "translations", f"{gvar.chart_language}.qm")
            if os.path.exists(qm_path):
                self.translator.load(qm_path)
                app.installTranslator(self.translator)
                self.retranslateUi(self._mainWindow)
            else:
                print(f"Translation file not found: {qm_path}")
        else:
            app.removeTranslator(self.translator)
            self.retranslateUi(self._mainWindow)

        # Redraw charts only if data has already been computed
        if gvar.astrodata:
            self.on_chart_parameters_changed(0)
            if self.mixedcharttab.isEnabled():
                self.on_mixedchart_parameters_changed(0)

        self.status.setText(
            f"Display settings updated: Language={gvar.chart_language.capitalize()}, "
            f"Style={gvar.chart_style.capitalize()} Indian."
        )

    def on_outerChartType_changed(self,index):
        #When the type is natal then the natal date time frame must be visible. else no
        type_keys = ["Transit", "Natal"]
        idx = self.comboBox_outerChartType.currentIndex()
        self.outerChartType = type_keys[idx] if idx >= 0 else "Transit"
        if (self.outerChartType == "Transit"):
            self.frame_transitDateTime.show()
            self.comboBox_DashaSeedPlanet.show()
            self.comboBox_DashaDivision.show()
            self.mixedchart_transittime_dashadetails.show()
            self.on_mixedchart_parameters_changed(index)
            self.status.setText("Outer chart type set to Transit. Transit date/time controls are now visible.")
        else:
            self.frame_transitDateTime.hide()
            self.comboBox_DashaSeedPlanet.hide()
            self.comboBox_DashaDivision.hide()
            self.mixedchart_transittime_dashadetails.hide()
            self.on_mixedchart_parameters_changed(index)
            self.status.setText(f"Outer chart type set to {self.outerChartType}. Mixed chart updated.")
        return
    
    def on_chart_division_changed(self, index):
        div = self.comboBox_ChartDivision.currentText()
        asc_sign = gvar.astrodata[div]["ascendant"]["sign"]
        self.comboBox_firsthouse.setCurrentText(asc_sign)
        self.on_chart_parameters_changed(index)
        self.mainchart_planetdetails.setText("CLICK PLANETS TO LOAD ITS DETAILS")
        progress_value = 0
        self.progressBar_planetshadbala.setValue(int(progress_value))
        self.progressBar_planetshadbala.setFormat("%d%%" % progress_value)
        self.status.setText(f"Chart division changed to {div}. {div} chart is now displayed.")
        return


    def on_chart_parameters_changed(self, index):
        self.mainchartDiv = self.comboBox_ChartDivision.currentText()
        sign_keys = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Saggitarius", "Capricorn", "Aquarius", "Pisces"]
        idx_sign = self.comboBox_firsthouse.currentIndex()
        self.mainchartFirsthousesign = sign_keys[idx_sign] if idx_sign >= 0 else "None"
        self.aspectSts = self.checkBox_aspects.isChecked()
        # Update label text about division significance
        self.label_DivDetails.setText(chart.get_division_signification(self.mainchartDiv))
        # Compute and update the chart in Mainchart window
        chart.plot_astrochart(
            "./images/birthcharts/", f"{self.mainchartDiv}_Chart",
            gvar.astrodata, self.mainchartDiv,
            self.mainchartFirsthousesign,
            IsAspectNeeded=self.aspectSts,
            language=gvar.chart_language,
            chart_style=gvar.chart_style
        )
        self.load_svg_in_graphicsview(f"./images/birthcharts/{self.mainchartDiv}_Chart.svg")
        aspect_msg = "Planetary aspects are displayed on the chart." if self.aspectSts else "Aspects are hidden."
        self.status.setText(f"{self.mainchartDiv} chart updated | First house: {self.mainchartFirsthousesign} | {aspect_msg}")
        return

    def on_innerchart_division_changed(self, index):
        div = self.comboBox_innerChartDivision.currentText()
        asc_sign = gvar.astrodata[div]["ascendant"]["sign"]
        self.comboBox_MixedChart_firsthousesign.setCurrentText(asc_sign)
        self.on_mixedchart_parameters_changed(index)
        self.status.setText(f"Inner chart division changed to {div}. Mixed chart updated.")
        return
    
    def on_transitdate_time_changed(self):
        self.status.setText("Updating transit chart for new date/time...")
        QtWidgets.QApplication.processEvents()
        self.on_mixedchart_parameters_changed(0)
        self.update_DashaDetails_in_MixedchartLabel_transit(gvar.astrodata, gvar.transit_astrodata)
        transit_date = self.dateEdit_transitdate.date().toString("dd-MM-yyyy")
        transit_time = self.timeEdit_transittime.time().toString("hh:mm")
        self.status.setText(f"Transit chart updated for {transit_date} at {transit_time}. Dasha details refreshed.")

    
    def on_mixedchart_parameters_changed(self,index):
        # Read Mixed Chart specific selections
        type_keys = ["Transit", "Natal"]
        idx_type = self.comboBox_outerChartType.currentIndex()
        outer_chartType = type_keys[idx_type] if idx_type >= 0 else "Transit"

        sign_keys = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Saggitarius", "Capricorn", "Aquarius", "Pisces"]
        idx_sign = self.comboBox_MixedChart_firsthousesign.currentIndex()
        mixed_asc_sign = sign_keys[idx_sign] if idx_sign >= 0 else "None"
        
        innerDiv = self.comboBox_innerChartDivision.currentText()
        outerDiv = self.comboBox_outerChartDivision.currentText()
        innerAspects = self.checkBox_innerAspects.isChecked()
        outerAspects = self.checkBox_outerAspects.isChecked()

        if(outer_chartType == "Transit"):
            self.pushButton_transitTable.show()
            astrocalc.transitAstroCalculations(self)    #Compute Transit Astrodata 
            #Plot the Mixed Chart with parameters in place
            chart.plot_astroMixedChart(
                "./images/mixedcharts/", "MixedChart",
                gvar.astrodata, innerDiv, gvar.transit_astrodata, outerDiv,
                mixed_asc_sign, innerAspects, outerAspects,
                language=gvar.chart_language, chart_style=gvar.chart_style
            )
        else:
            self.pushButton_transitTable.hide()
            chart.plot_astroMixedChart(
                "./images/mixedcharts/", "MixedChart",
                gvar.astrodata, innerDiv, gvar.astrodata, outerDiv,
                mixed_asc_sign, innerAspects, outerAspects,
                language=gvar.chart_language, chart_style=gvar.chart_style
            )
        
        #Now load the chart into the MixedChart Box
        self.load_svg_in_mixedchartview("./images/mixedcharts/MixedChart.svg")
        QtWidgets.QApplication.processEvents()
        # Build aspect status message
        aspect_parts = []
        if innerAspects:
            aspect_parts.append("Inner aspects shown")
        if outerAspects:
            aspect_parts.append("Outer aspects shown")
        aspect_msg = " | ".join(aspect_parts) if aspect_parts else "No aspects displayed"
        self.status.setText(f"Mixed chart updated: Inner={innerDiv}, Outer={outerDiv} ({outer_chartType}) | {aspect_msg}")
        return
    
    def update_planet_details_in_MainchartLabel(self, ad, div, planetname):
        if planetname == "Ascendant":
            signlord = ad[div]["ascendant"]["lagna-lord"]
            planet_data = ad[div]["ascendant"]
            houserel = "Not Applicable"
        else:
            planet_data = ad[div]["planets"][planetname]
            signlord = planet_data['dispositor']
            houserel = planet_data['house-rel'].split("/")[0]

            
        try:
            shadbala = ad["Balas"]["Shadbala"]["Total"][planetname]
        except:
            shadbala = 0
        
        minshadbala = shadbal.update_shadbala_progress_bar(self.progressBar_planetshadbala, planetname, shadbala)

        html_content = f"""
        <div style='font-size:16px; color:#333; padding:5px;'>
            <b style='color: #FF5733;'>{planet_data['name']}</b><br>
            <span><U>Position</U>: <b style='color: #3498DB;'>{planet_data['pos']['dec_deg']:.2f}°</b></span><br>
            <span><U>Sign</U>: <b style='color: #2ECC71;'>{planet_data['sign']}</b></span><br>
            <span><U>Dispositor</U>: <b style='color: #F1C40F;'>{signlord}</b></span><br>
            <span><U>House Relation</U>: <b style='color: #9B59B6;'>{houserel}</b></span><br>
            <span><U>Nakshatra</U>: <b style='color: #E67E22;'>{planet_data['nakshatra']} - Pada {planet_data['pada']}</b></span><br>
            <span><U>Nak Ruler</U>: <b>{planet_data['nak-ruler']}</b> | <U>Nak Diety</U>: <b>{planet_data['nak-diety']}</b></span><br>
            <hr>
            <b style='color: #E74C3C;'>Vimshottari Dasha Details:</b> <br>
            {dashavim.get_dasha_details_from_dict(ad,planetname)}
            <hr>
            <b style='color: #E74C3C;'>Shadbala Details:</b> <br>
            <span><U>Shadbala</U>: <b>{shadbala} virupas.</b></span><br>
            <span><U>Min Req</U>: <b>{minshadbala} virupas.</b></span><br>
        </div>
        """

        self.mainchart_planetdetails.setText(html_content)
        self.mainchart_planetdetails.setWordWrap(True)
        
        return
    
    def update_currentDashaDetails_in_MainchartLabel(self, ad):
        html_content = f"""
        <div style='font-size:16px; color:#333; padding:5px;'>
            <U><b>Vimshottari</b></U><br>
            <hr>
            <span><U>Dasha</U>: <b>{ad["Dashas"]["Vimshottari"]["current"]["dasha"]}</b></span><br>
            <span><U>Bhukti</U>: <b>{ad["Dashas"]["Vimshottari"]["current"]["bhukti"]}</b></span><br>
            <span><U>PD</U>: <b>{ad["Dashas"]["Vimshottari"]["current"]["paryantardasha"]}</b></span><br>
        </div>
        """

        self.currentDashaDetails.setText(html_content)
        self.currentDashaDetails.setWordWrap(True)
        
        return
    
    def update_DashaDetails_in_MixedchartLabel_transit(self, ad, td):
        div = self.comboBox_DashaDivision.currentText()
        planet_keys = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        idx_planet = self.comboBox_DashaSeedPlanet.currentIndex()
        planet_name = planet_keys[idx_planet] if idx_planet >= 0 else "Moon"
        html_content = dashavim.get_dashadetails_fordate(ad, td, div, planet_name)

        self.mixedchart_transittime_dashadetails.setText(html_content)
        self.mixedchart_transittime_dashadetails.setWordWrap(True)
        self.status.setText(f"Dasha details updated for {div} division, seed planet: {planet_name}.")
        
        return
    
    def load_planetdetails(self, planetname):
        div = self.comboBox_ChartDivision.currentText()
        self.update_planet_details_in_MainchartLabel(gvar.astrodata,div,planetname)
        self.status.setText(f"{planetname} details loaded for {div} chart.")
        return


    def load_svg_in_graphicsview(self, svg_path):
        """ Load an SVG file into the QGraphicsView and allow resizing """
        self.mainchartScene.clear()  # Clear existing items
        self.svg_item = QGraphicsSvgItem(svg_path)

        # Ensure the SVG has a proper bounding rectangle
        self.svg_item.setFlags(QtWidgets.QGraphicsItem.ItemClipsToShape)
        
        # Add the item to the scene
        self.mainchartScene.addItem(self.svg_item)

        # Force an update of the view
        self.MainChart.setSceneRect(self.svg_item.boundingRect())  # Set scene size
        self.MainChart.update()
        QtWidgets.QApplication.processEvents()

        # Apply fitInView with some delay to allow UI processing
        QtCore.QTimer.singleShot(50, lambda: self.MainChart.fitInView(self.svg_item, Qt.KeepAspectRatio))

        return
    
    def load_svg_in_mixedchartview(self, svg_path):
        """ Load an SVG file into the QGraphicsView and allow resizing """
        self.mixedchartScene.clear()  # Clear existing items
        self.svg_item_mixed = QGraphicsSvgItem(svg_path)

        # Ensure the SVG has a proper bounding rectangle
        self.svg_item_mixed.setFlags(QtWidgets.QGraphicsItem.ItemClipsToShape)
        
        # Add the item to the scene
        self.mixedchartScene.addItem(self.svg_item_mixed)

        # Force an update of the view
        self.graphicsView_MixedChart.setSceneRect(self.svg_item_mixed.boundingRect())  # Set scene size
        self.graphicsView_MixedChart.update()
        QtWidgets.QApplication.processEvents()

        # Apply fitInView with some delay to allow UI processing
        QtCore.QTimer.singleShot(50, lambda: self.graphicsView_MixedChart.fitInView(self.svg_item_mixed, Qt.KeepAspectRatio))

        return


    def _fit_charts_in_view(self):
        """ Fit SVG items into their respective views, keeping aspect ratio """
        if hasattr(self, 'svg_item') and self.svg_item.scene():
            self.MainChart.fitInView(self.svg_item, Qt.KeepAspectRatio)
        if hasattr(self, 'svg_item_mixed') and self.svg_item_mixed.scene():
            self.graphicsView_MixedChart.fitInView(self.svg_item_mixed, Qt.KeepAspectRatio)

    def _on_tab_changed(self, index):
        """ When user switches to a chart tab, refit after layout settles """
        QtCore.QTimer.singleShot(50, self._fit_charts_in_view)

    def submitdetails(self):
        self.status.setText("Computing astrological data... Please wait.")
        QtWidgets.QApplication.processEvents()
        astrocalc.initialAstroCalculations(self)    #Compute Astrodata from the birthdata

        ########## For MainChart Page ################
        self.status.setText("Generating D1 birth chart...")
        QtWidgets.QApplication.processEvents()
        asc_sign = gvar.astrodata["D1"]["ascendant"]["sign"]    #Fetch the ascendant sign of D1 chart for initial mainchart
        chart.plot_astrochart(
            "./images/birthcharts/", "D1_Chart",
            gvar.astrodata, "D1", asc_sign, False,
            language=gvar.chart_language, chart_style=gvar.chart_style
        )
        self.comboBox_firsthouse.setCurrentText(asc_sign)   #Initially the first house sign shall be set to ascendant sign only
        self.checkBox_aspects.setChecked(False) #Untick the aspects checkbox first as aspects is not needed initially

        #Load the D1 chart generated into the Mainchart window and resize it to fit properly
        self.load_svg_in_graphicsview("./images/birthcharts/D1_Chart.svg")
        QtWidgets.QApplication.processEvents()

        #Load Current Dasha details in the label
        self.update_currentDashaDetails_in_MainchartLabel(gvar.astrodata)

        self.birthchart.setEnabled(True)
        self.status.setText("Birth chart generated. Computing transit data...")
        QtWidgets.QApplication.processEvents()

        ########## For MixedChart Page ################
        astrocalc.transitAstroCalculations(self)    #Compute Transit Astrodata 
        #Plot the Mixed Chart initially with inner chart as natal_D1 and outer chart as transit_D1 for current date and time
        chart.plot_astroMixedChart(
            "./images/mixedcharts/", "MixedChart",
            gvar.astrodata, "D1", gvar.transit_astrodata, "D1",
            asc_sign, False, False,
            language=gvar.chart_language, chart_style=gvar.chart_style
        )
        self.comboBox_MixedChart_firsthousesign.setCurrentText(asc_sign)   #Initially the first house sign shall be set to ascendant sign only
        self.load_svg_in_mixedchartview("./images/mixedcharts/MixedChart.svg")
        QtWidgets.QApplication.processEvents() 

        self.update_DashaDetails_in_MixedchartLabel_transit(gvar.astrodata, gvar.transit_astrodata)

        self.mixedcharttab.setEnabled(True)
        selected_name = self.cmb_name.currentText()
        self.status.setText(f"All charts computed successfully for '{selected_name}'. BirthChart and MixedChart tabs are now enabled.")

        # Delayed refit so charts display at full size once the layout settles
        QtCore.QTimer.singleShot(150, self._fit_charts_in_view)
     
        return

    def browse_save_location(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Select Folder for Report")
        if folder:
            self.lineEdit_saveLocation.setText(folder)
            self.status.setText(f"Report save location set to: {folder}")
        else:
            self.status.setText("Browse cancelled. No folder selected.")

    def update_report_name(self, name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = name.replace(" ", "_") if name else "Unknown"
        filename = f"JyotishReport_{safe_name}_{timestamp}"
        self.lineEdit_reportName.setText(filename)

    def open_display_settings(self):
        import userforms.display_settings_dialog as dsd
        dialog = dsd.DisplaySettingsDialog(self._mainWindow)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            if hasattr(gvar, 'astrodata') and gvar.astrodata:
                self.on_chart_parameters_changed(None)
            if hasattr(gvar, 'transit_astrodata') and gvar.transit_astrodata:
                self.on_mixedchart_parameters_changed(None)

    def set_all_pdf_checkboxes(self, state):
        checkboxes = [
            self.chk_divisionalCharts, self.chk_vimshottariDasha,
            self.chk_yogasDoshas, self.chk_cancelledYogas,
            self.chk_vimshopakaBala, self.chk_shadbala,
            self.chk_bhavaBala, self.chk_ashtakaVarga,
            self.chk_lordInHouses
        ]
        for cb in checkboxes:
            cb.setChecked(state)
        action = "selected" if state else "deselected"
        self.status.setText(f"All report sections {action}.")

    def on_yogas_doshas_toggled(self, checked):
        self.chk_cancelledYogas.setEnabled(checked)
        if not checked:
            self.chk_cancelledYogas.setChecked(False)
            self.status.setText("Yogas & Doshas unchecked. Cancelled Yogas option is now disabled.")
        else:
            self.status.setText("Yogas & Doshas selected. You can now also include Cancelled Yogas.")

    def generate_report_workflow(self):
        save_dir = self.lineEdit_saveLocation.text().strip()
        if not save_dir:
            QtWidgets.QMessageBox.warning(self.centralwidget, "Validation Error", "Please select a valid folder to save the report.")
            self.status.setText("Report generation aborted: No save location selected.")
            return

        report_name = self.lineEdit_reportName.text().strip()
        if not report_name:
            report_name = "JyotishReport"
        
        if not report_name.endswith(".pdf"):
            report_name += ".pdf"
            
        target_path = os.path.join(save_dir, report_name)
        
        # Count selected sections
        sections_selected = sum([
            self.chk_divisionalCharts.isChecked(), self.chk_vimshottariDasha.isChecked(),
            self.chk_yogasDoshas.isChecked(), self.chk_cancelledYogas.isChecked(),
            self.chk_vimshopakaBala.isChecked(), self.chk_shadbala.isChecked(),
            self.chk_bhavaBala.isChecked(), self.chk_ashtakaVarga.isChecked(),
            self.chk_lordInHouses.isChecked(), self.chk_elementalMatrix.isChecked()
        ])
        
        lang_keys = ["English", "Kannada", "Hindi"]
        style_keys = ["North Indian", "South Indian"]
        idx_report_lang = self.cmb_reportLanguage.currentIndex()
        idx_report_style = self.cmb_reportChartStyle.currentIndex()

        config = {
            "name": self.cmb_name.currentText(),
            "save_path": target_path,
            "language": lang_keys[idx_report_lang] if idx_report_lang >= 0 else "English",
            "chartStyle": style_keys[idx_report_style] if idx_report_style >= 0 else "North Indian",
            "sections": {
                "divisionalCharts": self.chk_divisionalCharts.isChecked(),
                "vimshottariDasha": self.chk_vimshottariDasha.isChecked(),
                "yogasDoshas": self.chk_yogasDoshas.isChecked(),
                "cancelledYogas": self.chk_cancelledYogas.isChecked(),
                "vimshopakaBala": self.chk_vimshopakaBala.isChecked(),
                "shadbala": self.chk_shadbala.isChecked(),
                "bhavaBala": self.chk_bhavaBala.isChecked(),
                "ashtakaVarga": self.chk_ashtakaVarga.isChecked(),
                "lordInHouses": self.chk_lordInHouses.isChecked(),
                "elementalMatrix": self.chk_elementalMatrix.isChecked()
            },
            "elementalMatrix": self.chk_elementalMatrix.isChecked()
        }
        
        # User Feedback
        self.btn_generateReport.setEnabled(False)
        self.status.setText(f"Generating PDF report with {sections_selected} sections in {config['language']}...")
        QtWidgets.QApplication.processEvents()

        if hasattr(self, 'chkGenerateJsonReport') and self.chkGenerateJsonReport.isChecked():
            json_target = target_path.replace('.pdf', '.json')
            try:
                import json
                with open(json_target, 'w', encoding='utf-8') as jf:
                    json.dump(gvar.astrodata, jf, indent=4)
            except Exception as e:
                print("Failed to save JSON:", e)
        QtWidgets.QApplication.processEvents() # Force UI update
        
        try:
            # Execution
            self.run_pdf_generation(target_path, config)
            self.status.setText(f"Report saved successfully at {target_path}")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self.centralwidget, "Error", f"Failed to generate report: {str(e)}")
            self.status.setText(f"Report generation failed: {str(e)}")
        finally:
            self.btn_generateReport.setEnabled(True)

    def run_pdf_generation(self, target_path, config):
        if not hasattr(gvar, 'astrodata') or not gvar.astrodata:
            raise Exception("Astrological data has not been computed yet. Please click Submit on the User Details tab first.")

        import support.pdf_report as pdfrep
        pdfrep.GeneratePDFReport(gvar.astrodata, target_path, config)

    def check_places_loaded(self):
        if places_manager.is_loaded():
            names = places_manager.get_all_place_names()
            completer = QtWidgets.QCompleter(names, self._mainWindow)
            completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            completer.setFilterMode(QtCore.Qt.MatchContains)
            completer.activated.connect(lambda text: self.on_load_place_clicked())
            self.place.setCompleter(completer)
        else:
            QtCore.QTimer.singleShot(200, self.check_places_loaded)

    def on_load_place_clicked(self):
        place_text = self.place.text().strip()
        if not place_text:
            return
            
        details = places_manager.get_place_details(place_text)
        if details:
            self.lat.setText(details.get("lat", ""))
            self.lon.setText(details.get("lon", ""))
            self.tz.setText(details.get("timezone", ""))
        else:
            dialog = missing_place_dialog.MissingPlaceDialog(initial_name=place_text, parent=self._mainWindow)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                new_details = dialog.get_details()
                success, display_name = places_manager.add_new_place(
                    name=new_details['name'],
                    lat=new_details['lat'],
                    lon=new_details['lon'],
                    timezone=new_details['timezone'],
                    timezone_name=new_details['timezone_name']
                )
                if success:
                    # Update completer model
                    names = places_manager.get_all_place_names()
                    model = QtCore.QStringListModel(names)
                    self.place.completer().setModel(model)
                    
                    self.place.setText(display_name)
                    self.lat.setText(new_details['lat'])
                    self.lon.setText(new_details['lon'])
                    self.tz.setText(new_details['timezone'])
                    QtWidgets.QMessageBox.information(self.centralwidget, "Success", f"Added {display_name} to database.")
                else:
                    QtWidgets.QMessageBox.critical(self.centralwidget, "Error", "Failed to save place to database.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindow_cls()
    ui.setupUi_main(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
