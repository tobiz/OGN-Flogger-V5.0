
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QPushButton, QVBoxLayout, QDialog, QSystemTrayIcon
from PyQt5.QtGui import QIcon

from PyQt5 import QtCore, uic
##from PyQt5.Qt import SIGNAL
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
#import subprocess
from parse import *
#from ConfigParser import *
from configobj import ConfigObj
from flogger3 import *
##from .flogger_settings import * 
from flogger_settings import *
import gpxpy
import matplotlib.pyplot as plt
import mplleaflet
from flogger_moviesplash import *
from importlib import import_module
import time
from flogger_path_join import *

from flogger_get_coords import get_coords
##from LatLon import*
from latlon import *

import PyQt5
from flogger_process_log import process_log
##from PyQt5 import QtWidgets, uic
##from PyQt5.QtWidgets import QDialog, QApplication
import importlib
from operator import itemgetter

import folium 
import gpxpy
import os
import subprocess


#
# Convert QtDesigner ui to python file
# And import result as a module
#
print("flogger_gui Start")
path = os.path.dirname(os.path.abspath(__file__))            
ui_in = path_join_dd(os.path.abspath(__file__), ["data", "flogger-v1.2.3.ui"])
ui_out = path_join(path, ["floggerUI.py"])
ui_cmd = "pyuic5 %s -o %s" % (ui_in, ui_out)
print("pyuic5 cmd-1: " + ui_cmd)
os.system(ui_cmd)
flogger_ui = importlib.import_module("floggerUI")

#
# Convert QtDesigner About window 
# to module and import
#
about_in = path_join_dd(os.path.abspath(__file__), ["data", "flogger_about.ui"])
about_out = path_join(path, ["floggerAbout.py"])
about_cmd = "pyuic5 %s -o %s" % (about_in, about_out)
print("pyuic5 cmd-2: " + about_cmd)
os.system(about_cmd)
flogger_About = importlib.import_module("floggerAbout")

#
# Create Python resources file
#
pyrcc5_out = path_join(path, ["flogger_resources_rc.py"])
pyrcc5_in = path_join_dd(os.path.abspath(__file__), ["data", "flogger_resources.qrc"])
##print("pyrcc5_in: ", pyrcc5_in)
##print("pyrcc5_out: ", pyrcc5_out)
pyrcc5_cmd = "pyrcc5 -o %s %s" % (pyrcc5_out, pyrcc5_in)
print ("pyrcc5_cmd-3 is: " + pyrcc5_cmd)
##os.system(pyrcc5_cmd)
print("pyrcc5 ran ok ", pyrcc5_cmd)
print("flogger Exit")
##exit()

class flogger(QtWidgets.QMainWindow):
    def __init__(self, about_popup):
        print("flogger init")
        super().__init__()
        self.ui = flogger_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.about = about_popup
        window = QtWidgets.QMainWindow()  
        
        self.ui.actionAbout.triggered.connect(self.about.floggerAboutButton)
        self.ui.actionStart.triggered.connect(self.floggerStart)
##        self.ui.actionStart.triggered.connect(self.floggerStart)  
        self.ui.actionStop.triggered.connect(self.floggerStop)
        self.ui.actionFlying_End.triggered.connect(self.floggerFlying_End)  
        self.ui.actionQuit.triggered.connect(self.floggerQuit)  
        self.ui.actionEdit.triggered.connect(self.floggerEdit) 
        self.ui.FleetCheckRadioButton.toggled.connect(self.floggerFleetCheckRadioButton) 
        self.ui.RecordTracksRadioButton.toggled.connect(self.floggerRecordTracksRadioButton)  
        self.ui.TakeoffEmailButton.toggled.connect(self.floggerTakeoffEmailButton)  
        self.ui.LandingEmailButton.toggled.connect(self.floggerLandingEmailButton)  
        self.ui.LaunchFailuresButton.toggled.connect(self.floggerLaunchFailuresButton)
        self.ui.LogTugsButton.toggled.connect(self.floggerLogTugsButton)
        self.ui.IGCFormatButton.toggled.connect(self.floggerIGCFormatButton)  
        self.ui.LiveTestButton.toggled.connect(self.floggerLiveTestButton)
        self.ui.UpdateButton.clicked.connect(self.floggerUpdateConfig)
        self.ui.CancelButton.clicked.connect(self.floggerCancelConfigUpdate)
        self.ui.Add2FleetOkButton.clicked.connect(self.floggerAdd2FleetOkButton)
        self.ui.Add2FleetCancelButton.clicked.connect(self.floggerAdd2FleetCancelButton)
        self.ui.DelFromFleetOkButton.clicked.connect(self.floggerDelFromFleetOkButton)
        self.ui.RunningLabel.setStyleSheet("color: red")  
        self.ui.FlightLogcalendar.clicked.connect(self.floggerFlightLog)
        self.ui.IncludeTugsButton.toggled.connect(self.floggerIncludeTugsButton)
        self.ui.FlightLogTable.doubleClicked.connect(self.floggerFlightLogDoubleClicked)
        self.ui.FlightLogTable.verticalHeader().sectionClicked.connect(self.floggerFlightLogDoubleClicked)  
        self.ui.FlightLogTable.setColumnHidden(10, True)
        # Initialise values from config file

        filepath = os.path.join(path, "flogger_settings_file.txt")
        try:
            settings_file_dot_txt = path_join_dd(os.path.abspath(__file__), ["data", "flogger_settings_file.txt"])
            self.ui.config = ConfigObj(settings_file_dot_txt, raise_errors = True)
            print("Opened flogger_settings_file.txt path:", settings_file_dot_txt)
        except:
            print("Open failed")
            print(self.ui.config)
        
        print("flogger init run")
##        window.show()
        
        
        
#
# This section reads all the values from the config file and outputs these in the gui fields.
# It also initialises the corresponding settings object config fields. If the values are changed
# in the gui they must be saved in the config file and used as the current values in the settings object
#          

        try:
            settings_file_dot_txt = path_join_dd(os.path.abspath(__file__), ["data", "flogger_settings_file.txt"])
            self.config = ConfigObj(settings_file_dot_txt, raise_errors = True)
            print("Opened flogger_settings_file.txt path:", settings_file_dot_txt)
        except:
            print("Open failed")
            print(self.config)
            
        
        global settings
        global db
        global cursor
        settings = class_settings()
        db       = class_settings()
        cursor   = class_settings()
        
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
        settings.FLOGGER_AIRFIELD_NAME = old_val
        print ("Airfield Name: " + settings.FLOGGER_AIRFIELD_NAME)
        self.ui.AirfieldBase.setText(old_val)
         
        old_val = self.getOldValue(self.config, "APRS_USER")
        settings.APRS_USER = old_val
        self.ui.APRSUser.setText(old_val)
        
        
        
        old_val = self.getOldValue(self.config, "APRS_PASSCODE")    # This might get parsed as an int - need to watch it!
        settings.APRS_PASSCODE = old_val
        self.ui.APRSPasscode.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")    
        settings.APRS_SERVER_HOST = old_val
        self.ui.APRSServerHostName.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")    # This might get parsed as an int - need to watch it!
        settings.APRS_SERVER_PORT = int(old_val)
        self.ui.APRSServerPort.setText(old_val)
         
        old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME")
        print("FLOGGER_KEEPALIVE_TIME from settings.txt is ", old_val)
#        self.ui.FLOGGERKeep_alive_time = old_val
        settings.FLOGGER_KEEPALIVE_TIME = old_val
        self.ui.APRSKeepAliveTIme.setText(old_val)

        old_val = self.getOldValue(self.config, "FLOGGER_VER")      # Flogger Version Number
        print("FLOGGER_VER from settings.txt is ", old_val)
        self.FLOGGER_VER = old_val
        self.ui.FloggerVersionNo.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_RAD")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_RAD = int(old_val)
        self.ui.AirfieldFlarmRadius.setText(old_val)
         
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_LIMIT")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_AIRFIELD_LIMIT = int(old_val)
        self.ui.LandOutRadius.setText(old_val)
##
## 20220520 Added code to change/set Airfield Radius 
##
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_RADIUS")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_AIRFIELD_RADIUS = int(old_val)
        self.ui.AirfieldRadius.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")    
        settings.FLOGGER_AIRFIELD_DETAILS = old_val
        self.ui.AirfieldDetails.setText(old_val)
          
        old_val = self.getOldValue(self.config, "FLOGGER_QFE_MIN")    
        settings.FLOGGER_QFE_MIN = int(old_val)
        self.ui.MinFlightQFE.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")    
        settings.FLOGGER_MIN_FLIGHT_TIME = old_val
        self.ui.MinFlightTime.setText(old_val)
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_V_TAKEOFF_MIN")    
        settings.FLOGGER_V_TAKEOFF_MIN = old_val
        self.ui.MinFlightTakeoffVelocity.setText(old_val)
            
        old_val = self.getOldValue(self.config, "FLOGGER_V_LANDING_MIN")    
        settings.FLOGGER_V_LANDING_MIN = old_val
        self.ui.MinFlightLandingVelocity.setText(old_val) 
                   
        old_val = self.getOldValue(self.config, "FLOGGER_DT_TUG_LAUNCH")    
        settings.FLOGGER_DT_TUG_LAUNCH = old_val
        self.ui.MinTugLaunchTIme.setText(old_val)
#
# Note this could be done using LatLon
#        
        old_val_lat = self.getOldValue(self.config, "FLOGGER_LATITUDE")    # This might get parsed as a real - need to watch it!
        print("Old_val: " + old_val_lat)
        settings.FLOGGER_LATITUDE = old_val_lat
        
        old_val_lon = self.getOldValue(self.config, "FLOGGER_LONGITUDE")    # This might get parsed as a real - need to watch it!
        print("Old_lon: " + old_val_lon)
        settings.FLOGGER_LONGITUDE = old_val_lon
#        self.AirfieldLongitude.setText(old_val_lon)
        print("start LatLon")
        old_latlon = LatLon(Latitude( old_val_lat), Longitude(old_val_lon))
        old_latlonstr = old_latlon.to_string('D% %H')
        self.ui.AirfieldLatitude.setText(old_latlonstr[0])
        self.ui.AirfieldLongitude.setText(old_latlonstr[1])
        print("End LatLon", old_latlonstr)
               
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_CHECK")
        print("Fleet Check: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.ui.FleetCheckRadioButton.setChecked(True)
        else:
            print("N")   
            self.ui.FleetCheckRadioButton.setChecked(False)
        settings.FLOGGER_FLEET_CHECK = old_val
                          
        old_val = self.getOldValue(self.config, "FLOGGER_LOG_TUGS")
        print("Log Tugs Button: ", old_val) 
        if old_val == "Y":
            print("Y")
            self.ui.LogTugsButton.setChecked(True)
        else:
            print("N")   
            self.ui.LogTugsButton.setChecked(False)
##        settings.FLOGGER_FLEET_CHECK = old_val
        settings.FLOGGER_LOG_TUGS = old_val
        
        old_val = self.getOldValue(self.config, "FLOGGER_TRACKS")
        print("Record Tracks: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.ui.RecordTracksRadioButton.setChecked(True)
        else:
            print("N")   
        settings.FLOGGER_TRACKS = old_val 
                     
        old_val = self.getOldValue(self.config, "FLOGGER_TAKEOFF_EMAIL")
        print("Email takeoffs is: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.ui.TakeoffEmailButton.setChecked(True)
        else:
            print("N")   
        settings.FLOGGER_TAKEOFF_EMAIL = old_val 
        
                             
        old_val = self.getOldValue(self.config, "FLOGGER_LANDING_EMAIL")
        print("Email landings is: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.ui.LandingEmailButton.setChecked(True)
        else:
            print("N")   
        settings.FLOGGER_LANDING_EMAIL = old_val 
        
        old_val = self.getOldValue(self.config, "FLOGGER_DB_SCHEMA")    
        settings.FLOGGER_DB_SCHEMA = old_val
        self.ui.DBSchemaFile.setText(old_val)
        settings.FLOGGER_DB_SCHEMA = old_val
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_DB_NAME")    
        settings.FLOGGER_DB_NAME = old_val
        self.ui.DBName.setText(old_val)
        settings.FLOGGER_DB_NAME = old_val    
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLARMNET_DB_URL")    
        settings.FLOGGER_FLARMNET_DB_URL = old_val
        self.ui.FlarmnetURL.setText(old_val)
#        settings.FLOGGER_FLARMNET_DB_URL = old_val
       
        old_val = self.getOldValue(self.config, "FLOGGER_OGN_DB_URL")    
        settings.FLOGGER_OGN_DB_URL = old_val
        self.ui.OGNURL.setText(old_val)
#       settings.FLOGGER_OGN_DB_URL = old_val
                
        old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME")    
        settings.FLOGGER_KEEPALIVE_TIME = int(old_val)
        self.FLOGGERKeepAliveTime = old_val

        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_URL")  
        print("Initialise FLOGGER_SMTP_SERVER_URL")  
        settings.FLOGGER_SMTP_SERVER_URL = old_val
        self.ui.SMTPServerURL.setText(old_val)
        settings.FLOGGER_SMTP_SERVER_URL = old_val
        print("settings.FLOGGER_SMTP_SERVER_URL: ", settings.FLOGGER_SMTP_SERVER_URL)
        
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_PORT")    
        settings.FLOGGER_SMTP_SERVER_PORT = int(old_val)
        self.ui.SMTPServerPort.setText(old_val)
        settings.FLOGGER_SMTP_SERVER_PORT = int(old_val)
        
                
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_TX") 
        print("TX from file: ", old_val)   
        settings.FLOGGER_SMTP_TX = old_val
        self.ui.EmailSenderTX.setText(old_val)
        settings.FLOGGER_SMTP_TX = old_val     
                
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_RX")    
        settings.FLOGGER_SMTP_RX = old_val
        self.ui.EmailReceiverRX.setText(old_val)
        settings.FLOGGER_SMTP_RX = old_val
                
        old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
        i = 1
        for item in old_val:
#            print "APRS Base: " + item
            if i == 1:
                self.ui.APRSBase1Edit.setText(item)
                i += 1
                continue
            if i == 2:
                self.ui.APRSBase2Edit.setText(item)
                i += 1
                continue
            if i == 3:
                self.ui.APRSBase3Edit.setText(item)
                i += 1
                continue
            if i == 4:
                self.ui.APRSBase4Edit.setText(item)
                i += 1
                continue 
            if i == 5:
                self.ui.APRSBase5Edit.setText(item)
                i += 1
                continue 
            if i == 6:
                self.ui.APRSBase6Edit.setText(item)
                i += 1
                continue 
        settings.FLOGGER_APRS_BASES = old_val
#        print "APRS_BASES: ", old_val
        print("APRS_BASES: ", settings.FLOGGER_APRS_BASES)
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
 #       print "FLOGGER_FLEET_LIST: ", old_val 
        for key in list(old_val.keys()):
            # Convert string form of value to int
            old_val[key] = int(old_val[key])
#            print "Key: ", key, " = ", int(old_val[key])
        settings.FLOGGER_FLEET_LIST = old_val
        print("FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST)
        
        rowPosition = self.ui.FleetListTable.rowCount()
        for registration in settings.FLOGGER_FLEET_LIST:
            print("rowPosition: ", rowPosition, " Registration: ", registration, " Code: ", settings.FLOGGER_FLEET_LIST[registration])
            self.ui.FleetListTable.insertRow(rowPosition)
            self.ui.FleetListTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(registration))
            self.ui.FleetListTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(settings.FLOGGER_FLEET_LIST[registration])))
            rowPosition = rowPosition + 1
                  
        
        old_val = self.getOldValue(self.config, "FLOGGER_DATA_RETENTION")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_DATA_RETENTION = int(old_val)
        self.ui.DataRetentionTime.setText(old_val)
          
        old_val = self.getOldValue(self.config, "FLOGGER_LOG_TIME_DELTA")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_LOG_TIME_DELTA = int(old_val)
        self.ui.LogTimeDelta.setText(old_val) 
                 
        old_val = self.getOldValue(self.config, "FLOGGER_LOCATION_HORIZON")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_LOCATION_HORIZON = old_val
        self.ui.HorizonAdjustment.setText(old_val)   
                      
        old_val = self.getOldValue(self.config, "FLOGGER_DUPLICATE_FLIGHT_DELTA_T")    
        settings.FLOGGER_DUPLICATE_FLIGHT_DELTA_T = old_val
        self.ui.MinFlightDeltaTime.setText(old_val)
                             
        old_val = self.getOldValue(self.config, "FLOGGER_QNH")    
#        settings.FLOGGER_QNH = int(old_val)
        #
        # 20210210 Start
        #  
        if settings.FLOGGER_QNH == 0:
            print("Lookup new QNH")
            settings.FLOGGER_QNH = ""
        else:
            if settings.FLOGGER_QNH != old_val:
                print("Old QNH: ", old_val, " New QNH: ", settings.FLOGGER_QNH)
                old_val = settings.FLOGGER_QNH
        # 
        # 20210210 End
        #    
        settings.FLOGGER_QNH = old_val
        self.ui.AirfieldQNH.setText(old_val)     
                                     
        old_val = self.getOldValue(self.config, "FLOGGER_FLIGHTS_LOG")    
        settings.FLOGGER_FLIGHTS_LOG = old_val
        self.ui.FlightLogFolder.setText(old_val)  
                                           
        old_val = self.getOldValue(self.config, "FLOGGER_LANDOUT_MODE")    
        settings.FLOGGER_LANDOUT_MODE = old_val
        self.ui.LandoutMsgMode.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MODE")
        if old_val == "test":
            print("Live/Test mode state is Test")
            self.ui.LiveTestButton.setChecked(True)
                                                       
        old_val = self.getOldValue(self.config, "FLOGGER_INCLUDE_TUG_FLIGHTS")  
        print("Include Tugs Button: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.ui.IncludeTugsButton.setChecked(True)
        else:
            print("N")  
            self.ui.IncludeTugsButton.setChecked(False)
##        settings.FLOGGER_FLEET_CHECK = old_val  
        settings.FLOGGER_INCLUDE_TUG_FLIGHTS = old_val
            
            

        
             
    def editConfigField (self, file_name, field_name, new_value):
        print("editConfig called")
        self.config[field_name] = new_value
        self.config.write()
#        setattr(self, field_name, new_value) #equivalent to: self.'field_name' = new_value
        if type(new_value) is int: 
            int(new_value)
#        setattr(self, field_name, new_value) #equivalent to: self.'field_name' = new_value
        setattr(settings, field_name, new_value) #equivalent to: settings.'field_name' = new_value
            
    def setOldValue(self, config_field_name): 
#        val = self.config[config_field_name]
        val = settings.config[config_field_name]
        setattr(self, config_field_name, val) #equivalent to: self.varname= 'something'
#        settings.config_field_name = val
        return self.config[config_field_name]
    
    def getOldValue(self, config, config_field_name): 
        val = config[config_field_name]
        setattr(self, config_field_name, val)
        return config[config_field_name]

#
# Actions Start. Menu Bar. Version 5
#      
    def floggerStart(self):
        print("flogger start")
        print("FLOGGER_KEEPALIVE_TIME at start is:", self.FLOGGER_KEEPALIVE_TIME)
        settings.FLOGGER_RUN = True
        flogger = flogger3()
        #self.RunningLabel.setText("Logging Data...")
        #self.RunningProgressBar.setProperty("maximum", 0)
        self.change_status("Logging Data...", "green") 
        flogger.change_status.connect(self.change_status)
        flogger.set_flight_count.connect(self.set_flight_count)
        flogger.set_sunset.connect(self.set_sunset)
        flogger.flogger_run(settings, flogger)
        
    def change_status(self, state, colour):
        # Slot for status change signalled from data collection thread
        print("\nGUI change called with: ", " State: ", state, " Colour: ", colour, "\n")
        
        print("change_status. State: ", state, " Colour: ", colour)
        ##self.RunningLabel.setStyleSheet("color: " + colour)
        ##self.RunningLabel.setText(state)
        ##self.RunningProgressBar.setProperty("maximum", 0)
        
        self.ui.RunningLabel.setStyleSheet("color: " + colour)
        self.ui.RunningLabel.setText(state)
        self.ui.RunningProgressBar.setProperty("maximum", 0)
        return
            
    def set_flight_count(self, number, flightReg, flightEndTime):
        print("set_flight_count called-1: ", number, " Registration: ", flightReg, " Flight end time: ", flightEndTime)
        self.ui.FlightCount.display(int(number))
        self.ui.LastFlightReg.setText(str(flightReg))
        self.ui.FlightEndTime.setText(str(flightEndTime))
        
    def set_sunset(self, ssdt):
        print("Display local sunset time", ssdt)
        ##self.SunsetTime.setText(ssdt)
        self.ui.SunsetTime.setText(ssdt)
        
    def floggerStop(self):
        settings.FLOGGER_RUN = False
        ##self.RunningLabel.setStyleSheet("color: red")
        ##self.RunningLabel.setText("Stopped")
        ##self.RunningProgressBar.setProperty("maximum", 1)
        
        self.ui.RunningLabel.setStyleSheet("color: red")
        self.ui.RunningLabel.setText("Stopped")
        self.ui.RunningProgressBar.setProperty("maximum", 1)
        print("flogger stop")
        
    def floggerFlying_End(self):
        #
        # Add check that all flights taken off have landed
        # Basically this does what floggerFlightLog() does without the date stuff
        #
        settings.FLOGGER_RUN = False
        ##self.RunningLabel.setStyleSheet("color: yellow")
        ##self.RunningLabel.setText("Flying Ended")
        ##self.RunningProgressBar.setProperty("maximum", 1)
        
        self.ui.RunningLabel.setStyleSheet("color: yellow")
        self.ui.RunningLabel.setText("Flying Ended")
        self.ui.RunningProgressBar.setProperty("maximum", 1)
        print("flogger Flying Ended, Process DB")
        try:
            flogger_db_path = path_join_dd(os.path.abspath(__file__), ["db", "flogger.sql3.2"])
            print("DB name(new): ", flogger_db_path)
            db = sqlite3.connect(flogger_db_path) 
            cursor = db.cursor()
        except:
            print("Failed to connect to db")
        print("Stop Data Collection Cycle")
        settings.FLOGGER_RUN = False
        process_log(cursor, db, settings)
        print("Flogger DB processed")
        
    
    def floggerQuit(self):
        print("flogger quit")
        
    def floggerSetState(self, stateTxt, colour):
        print("flogger set state: ", stateTxt, " ", colour) 
        self.RunningLabel.setStyleSheet("color: " + colour)
        self.RunningLabel.setText(stateTxt)
        self.RunningProgressBar.setProperty("maximum", 1)
        

#
# Action Config Menu Bar
#
    def floggerEdit(self):
        print("flogger Config.edit")
        self.floggerUpdateConfig()
        print("flogger Config.edit end")
        
#
# Actions Start, update fields
#

    def floggerUpdateConfig(self):
        print("floggerUpdateConfig Called")
        self.floggerAirfieldEdit2(True)
        self.floggerAirfieldDetailsEdit2(True)
        self.floggerAPRSUserEdit2(True)
        self.floggerAPRSPasscodeEdit2(True)
        self.floggerAPRSServerhostEdit2(True)
        self.floggerAPRSServerportEdit2(True)
##
## 20220511 added call in
##
        print("floggerAPRSKeepAliveTimeEdit2 Called")
        self.floggerAPRSKeepAliveTimeEdit2(True)
        self.floggerFlarmRadiusEdit2(True)
        self.floggerLandoutRadiusEdit2(True)
##
## 20220520 Added code to change/set Airfield Radius 
##
        self.floggerAirfieldRadiusEdit2(True)
        self.floggerDataRetentionTimeEdit2(True)
        self.floggerAirfieldLatLonEdit2(True)
        self.floggerMinFlightTimeEdit2(True)
        self.floggerMinTakeoffVelocityEdit2(True)
        self.floggerMinLandingVelocityEdit2(True)
        self.floggerMinFlightQFEEdit2(True)
        self.floggerTugLaunchEdit2(True)
        self.floggerKeepAliveTimeEdit2(True)
        self.floggerDBSchemaFileEdit2(True)
        self.floggerDBNameEdit2(True)
        self.floggerFlarmnetURL2(True)
        self.floggerOGNURL2(True)
        self.floggerSMTPServerURLEdit2(True)
        self.floggerSMTPServerPortEdit2(True)
        self.floggerEmailSenderEdit2(True)
        self.floggerEmailReceiverEdit2(True)
        self.floggerAPRSBaseEdit2(True)
        self.floggerLogTimeDeltaEdit2(True)
        self.floggerHorizonAdjustmentEdit2(True)
        self.floggerMinFlightDeltaTimeEdit2(True)
        self.floggerMinFlightDeltaTimeEdit2(True)
        self.floggerAirfieldQNHEdit2(True)
        self.floggerFlightLogFolderEdit2(True)
        self.floggerFloggerVersionNoEdit2(True)
        self.floggerLandoutMsgModeEdit2(True)
#        self.floggerIncludeTugFlightsEdit2(True)
        try:
            self.config.write()
        except:
            print("Writing updated config file, flogger_settings_file.txt FAILED")
        return



    def floggerCancelConfigUpdate(self):
        print("floggerCancelConfigUpdate called")
        self.floggerAirfieldEdit2(False)
        self.floggerAirfieldDetailsEdit2(False)
        self.floggerAPRSUserEdit2(False)
        self.floggerAPRSPasscodeEdit2(False)
        self.floggerAPRSServerhostEdit2(False)
        self.floggerAPRSServerportEdit2(False)
##
## 20220511 added call in
##
        self.floggerAPRSKeepAliveTimeEdit2(True)
        self.floggerFlarmRadiusEdit2(False)
        self.floggerLandoutRadiusEdit2(False)
##
## 20220520 Added code to change/set Airfield Radius 
##
        self.floggerAirfieldRadiusEdit2(False)
        self.floggerDataRetentionTimeEdit2(False)
        self.floggerAirfieldLatLonEdit2(False)
        self.floggerMinFlightTimeEdit2(False)
        self.floggerMinTakeoffVelocityEdit2(False)
        self.floggerMinLandingVelocityEdit2(False)
        self.floggerMinFlightQFEEdit2(False)
        self.floggerTugLaunchEdit2(False)
        self.floggerKeepAliveTimeEdit2(False)
        self.floggerDBSchemaFileEdit2(False)
        self.floggerDBNameEdit2(False)
        self.floggerFlarmnetURL2(False)
        self.floggerOGNURL2(False)
        self.floggerSMTPServerURLEdit2(False)
        self.floggerSMTPServerPortEdit2(False)
        self.floggerEmailSenderEdit2(False)
        self.floggerEmailReceiverEdit2(False)
        self.floggerAPRSBaseEdit2(False)
        self.floggerLogTimeDeltaEdit2(False)
        self.floggerHorizonAdjustmentEdit2(False)
        self.floggerMinFlightDeltaTimeEdit2(False)
        self.floggerAirfieldQNHEdit2(False)
        self.floggerFlightLogFolderEdit2(False)
        self.floggerFloggerVersionNoEdit2(True)
        self.floggerLandoutMsgModeEdit2(False)
#        self.floggerIncludeTugFlightsEdit2(False)
        return
    
    def floggerTPOkButton(self):
        print("Add TP")
        field1 = self.AddTPInfo.item(0,0)
        if field1 != "":
            # Add a new turing point row
            print("Add new TP")
            return
        field2 = self.RemoveTPInfo.item(0,0)
        if field2 != "":
            # Remove turning pont row
            return
    
    def floggerTPCancelButton(self):
        return               
        
    def floggerAirfieldEdit2(self, mode):
        # Mode: True - update all fields, variables to latest values
        
        #       False - restore all fields and variables to values from config (settings.txt) file
        print("Base Airfield button clicked ", "Mode: ", mode) 
        if mode:
            # Values have been put into gui field from setting.txt and may then have been changed interactively
            ##airfield_base = self.AirfieldBase.toPlainText() 
            airfield_base = self.ui.AirfieldBase.toPlainText() 
        else:
            # Restore old values from settings.txt
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
#            settings.FLOGGER_AIRFIELD_NAME = old_val
            print(settings.FLOGGER_AIRFIELD_NAME)
            ##self.AirfieldBase.setText(old_val)
            self.ui.AirfieldBase.setText(old_val)
            print("Airfield Base: " + old_val)
            airfield_base = old_val
        # Put current value into settings.txt file for future use
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_NAME", airfield_base)
        # Now update python variable to current value in gui and settings.txt
#        self.FLOGGER_AIRFIELD_NAME = airfield_base
#        settings.FLOGGER_AIRFIELD_NAME = airfield_base
        print("FLOGGER_AIRFIELD_NAME from settings.py: ", settings.FLOGGER_AIRFIELD_NAME)
        

        
    def floggerAPRSUserEdit2(self, mode):
        print("APRS User button clicked")
        if mode: 
            ##APRSUser = self.APRSUser.toPlainText()
            APRSUser = self.ui.APRSUser.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "APRS_USER")
            ##self.APRSUser.setText(old_val)
            self.ui.APRSUser.setText(old_val)
            APRSUser = old_val
#       print "Airfield B: " + airfield_base
        self.editConfigField("flogger_settings_file.txt", "APRS_USER", APRSUser)
        ##self.APRS_USER = APRSUser
        self.ui.APRS_USER = APRSUser
        

    def floggerAPRSPasscodeEdit2(self, mode):
            print("APRS Passcode button clicked")
            if mode: 
                ##APRSPasscode = self.APRSPasscode.toPlainText()   
                APRSPasscode = self.ui.APRSPasscode.toPlainText() 
            else:
                old_val = self.getOldValue(self.config, "APRS_PASSCODE")
                ##self.APRSPasscode.setText(old_val)
                self.ui.APRSPasscode.setText(old_val)
                APRSPasscode = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_PASSCODE", APRSPasscode)
            ##self.APRS_PASSCODE = APRSPasscode
            self.ui.APRS_PASSCODE = APRSPasscode
            
    
    def floggerAPRSServerhostEdit2(self, mode):
            print("APRS Server Host button clicked")
            if mode: 
                ##APRSServerhost = self.APRSServerHostName.toPlainText()  
                APRSServerhost = self.ui.APRSServerHostName.toPlainText()
            else:
                old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")
                ##self.APRSServerHostName.setText(old_val)
                self.ui.APRSServerHostName.setText(old_val)
                APRSServerhost = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_SERVER_HOST", APRSServerhost)
            ##self.APRS_SERVER_HOST = APRSServerhost
            self.ui.APRS_SERVER_HOST = APRSServerhost
            
    
    def floggerAPRSServerportEdit2(self, mode):
            print("APRS Server Port button clicked")
            if mode: 
                ##APRSServerport = self.APRSServerPort.toPlainText()  
                APRSServerport = self.ui.APRSServerPort.toPlainText() 
            else:
                old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")
                ##self.APRSServerPort.setText(old_val)
                self.ui.APRSServerPort.setText(old_val)
                APRSServerport = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_SERVER_PORT", APRSServerport)
            ##self.APRS_SERVER_PORT = int(APRSServerport) 
            self.ui.APRS_SERVER_PORT = int(APRSServerport) 
##
## 20220511 - Added back in to see what happens
##
    def floggerAPRSKeepAliveTimeEdit2(self, mode):
        print ("APRS Keep Alive Time button clicked")
        if mode: 
            ##APRSUser = self.APRSUser.toPlainText() 
            APRSUser = self.ui.APRSUser.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "APRS_USER")
            ##self.APRSUser.setText(old_val)
            self.ui.APRSUser.setText(old_val)
            APRSUser = old_val
        ##print ("Airfield B: " + airfield_base)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_KEEPALIVE_TIME", self.FLOGGERKeepAliveTime)
        ##self.APRS_USER = APRSUser
        self.ui.APRS_USER = APRSUser
            
    def floggerDataRetentionTimeEdit2(self, mode): 
            print("Data Retention TIme button clicked")
            if mode: 
                ##DataRetentionTime = self.DataRetentionTime.toPlainText() 
                DataRetentionTime = self.ui.DataRetentionTime.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_DATA_RETENTION")
                ##self.DataRetentionTime.setText(old_val)
                self.ui.DataRetentionTime.setText(old_val)
                DataRetentionTime = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_DATA_RETENTION", DataRetentionTime)
            self.FLOGGER_DATA_RETENTION = int(DataRetentionTime)
            
    def floggerLogTimeDeltaEdit2(self, mode):    
            print("Log Time Delta button clicked")
            if mode: 
                ##LogTimeDelta = self.LogTimeDelta.toPlainText()
                LogTimeDelta = self.ui.LogTimeDelta.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_LOG_TIME_DELTA")
                ##self.LogTimeDelta.setText(old_val)
                self.ui.LogTimeDelta.setText(old_val)
                LogTimeDelta = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_TIME_DELTA", LogTimeDelta)
            self.FLOGGER_LOG_TIME_DELTA = int(LogTimeDelta)
        
    def floggerHorizonAdjustmentEdit2(self, mode):   
            print("Horizon Adjustment button clicked")
            if mode: 
                ##HorizonAdjustment = self.HorizonAdjustment.toPlainText() 
                HorizonAdjustment = self.ui.HorizonAdjustment.toPlainText()   
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_LOCATION_HORIZON")
                ##self.HorizonAdjustment.setText(old_val)
                self.ui.HorizonAdjustment.setText(old_val)
                HorizonAdjustment = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOCATION_HORIZON", HorizonAdjustment)
            self.FLOGGER_LOCATION_HORIZON = HorizonAdjustment
            
    def floggerAirfieldQNHEdit2(self, mode):
        print("QNH Setting button clicked")
        if mode: 
            ##AirfieldQNH = self.AirfieldQNH.toPlainText()  
            AirfieldQNH = self.ui.AirfieldQNH.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_QNH")
            ##self.AirfieldQNH.setText(old_val)
            self.ui.AirfieldQNH.setText(old_val)
            AirfieldQNH = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_QNH", AirfieldQNH)
#        self.FLOGGER_QNH = int(AirfieldQNH)
        self.FLOGGER_QNH = AirfieldQNH
        
    def floggerFlarmRadiusEdit2(self, mode):
            print("Flarm Radius button clicked")
            if mode: 
                ##FlarmRadius = self.AirfieldFlarmRadius.toPlainText()
                FlarmRadius = self.ui.AirfieldFlarmRadius.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_RAD")
                ##self.AirfieldFlarmRadius.setText(old_val)
                self.ui.AirfieldFlarmRadius.setText(old_val)
                FlarmRadius = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_RAD", FlarmRadius)
            self.FLOGGER_RAD = int(FlarmRadius)
   
    def floggerLandoutRadiusEdit2(self, mode):
            print("Flarm Radius button clicked")
            if mode: 
                ##LandOutRadius = self.LandOutRadius.toPlainText()   
                LandOutRadius = self.ui.LandOutRadius.toPlainText() 
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_LIMIT")
                ##self.LandOutRadius.setText(old_val)
                self.ui.LandOutRadius.setText(old_val)
                LandOutRadius = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_LIMIT", LandOutRadius)
            self.FLOGGER_AIRFIELD_LIMIT = int(LandOutRadius)
        
            
    def floggerAirfieldDetailsEdit2(self, mode):
        #
        # This needs to be changed determine the Lat/Long is AirfieldDetails is supplied
        # and write them back to the form and to settings.py.  Most of the code is similar
        # to that below except the lat/long have to found from the get_coords function
        # in flogger3.py
        #
        print("Airfield Details button clicked. Mode: ", mode)
        if mode:
            ##airfield_details = self.AirfieldDetails.toPlainText()
            airfield_details = self.ui.AirfieldDetails.toPlainText()
            print("Airfield Details: ", airfield_details, " QNH: ", settings.FLOGGER_QNH)
            if airfield_details != "":
                loc = get_coords(airfield_details, settings)
                print("get_coords rtns: ", loc)
                lat = str(loc[0])    # returned as numbers, convert to string
                lon = str(loc[1])    # as above
                qnh = str(loc[2])    # as above    
                self.editConfigField("flogger_settings_file.txt", "FLOGGER_LATITUDE", lat)
                self.editConfigField("flogger_settings_file.txt", "FLOGGER_LONGITUDE", lon)
                self.editConfigField("flogger_settings_file.txt", "FLOGGER_QNH", qnh)
                # The following is just to get Lat & Lon into the right format for display on form
                latlon = LatLon(Latitude(lat), Longitude(lon))
                latlonStr = latlon.to_string('D% %H')
                print("latlonStr: ", latlonStr)
                ##self.AirfieldLatitude.setText(latlonStr[0])
                ##self.AirfieldLongitude.setText(latlonStr[1])
                ##self.AirfieldQNH.setText(qnh)
                
                self.ui.AirfieldLatitude.setText(latlonStr[0])
                self.ui.AirfieldLongitude.setText(latlonStr[1])
                self.ui.AirfieldQNH.setText(qnh)
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")
            ##self.AirfieldDetails.setText(old_val)
            self.ui.AirfieldDetails.setText(old_val)
            airfield_details = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_DETAILS", airfield_details)

    def floggerAirfieldLatLonEdit2(self, mode):
        print("Airfield latitude, longitude called")
        if mode:
            ##airfieldLat = self.AirfieldLatitude.toPlainText()
            ##airfieldLon = self.AirfieldLongitude.toPlainText()
            
            airfieldLat = self.ui.AirfieldLatitude.toPlainText()
            airfieldLon = self.ui.AirfieldLongitude.toPlainText()
            airfieldlatlon = string2latlon(str(airfieldLat), str(airfieldLon), 'D% %H')
            print("Airfield lat/lon: ", airfieldlatlon)
            airfieldLatLonStr = airfieldlatlon.to_string("%D")
            print("Update Lat/Lon: ", airfieldLatLonStr)
            print("Latlonstr: ", airfieldLatLonStr[0], " :", airfieldLatLonStr[1])
            old_val_lat = airfieldLatLonStr[0]
            old_val_lon = airfieldLatLonStr[1]
        else:
            old_val_lat = self.getOldValue(self.config, "FLOGGER_LATITUDE")
            old_val_lon = self.getOldValue(self.config, "FLOGGER_LONGITUDE")
            print("Old Lat: ", old_val_lat, " Old Lon: ", old_val_lon)
            airfieldlatlon = LatLon(Latitude(old_val_lat), Longitude(old_val_lon))
            print("airfieldlatlon: ", airfieldlatlon)
            airfieldLatLonStr = airfieldlatlon.to_string('D% %H')
            print("airfieldlatlonStr: ", airfieldLatLonStr)
            ##self.AirfieldLatitude.setText(airfieldLatLonStr[0])
            ##self.AirfieldLongitude.setText(airfieldLatLonStr[1])
            
            self.ui.AirfieldLatitude.setText(airfieldLatLonStr[0])
            self.ui.AirfieldLongitude.setText(airfieldLatLonStr[1])
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LATITUDE", old_val_lat)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LONGITUDE", old_val_lon)
        return
                  
    def floggerMinFlightTimeEdit2(self, mode):
        print("Min Flight Time button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            ##min_flight_time = self.MinFlightTime.toPlainText() 
            min_flight_time = self.ui.MinFlightTime.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")
            ##self.MinFlightTime.setText(old_val)
            self.ui.MinFlightTime.setText(old_val)
            min_flight_time = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_MIN_FLIGHT_TIME", min_flight_time) 
        
                  
    def floggerMinTakeoffVelocityEdit2(self, mode):
        print("Min Takeoff Velocity button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            ##min_takeoff_velocity = self.MinFlightTakeoffVelocity.toPlainText() 
            min_takeoff_velocity = self.ui.MinFlightTakeoffVelocity.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_V_TAKEOFF_MIN")
            ##self.MinFlightTakeoffVelocity.setText(old_val)
            self.ui.MinFlightTakeoffVelocity.setText(old_val)
            min_takeoff_velocity = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_V_TAKEOFF_MIN", min_takeoff_velocity) 
        
                  
    def floggerMinLandingVelocityEdit2(self, mode):
        print("Min Landing Velocity button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            ##min_landing_velocity = self.MinFlightLandingVelocity.toPlainText() 
            min_landing_velocity = self.ui.MinFlightLandingVelocity.toPlainText()
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_V_LANDING_MIN")
            ##self.MinFlightLandingVelocity.setText(old_val)
            self.ui.MinFlightLandingVelocity.setText(old_val)
            min_landing_velocity = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_V_LANDING_MIN", min_landing_velocity) 
        
                  
    def floggerMinFlightQFEEdit2(self, mode):
        print("Min QFE button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            ##min_QFE = self.MinFlightQFE.toPlainText()
            min_QFE = self.ui.MinFlightQFE.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_QFE_MIN")
            ##self.MinFlightQFE.setText(str(old_val))
            self.ui.MinFlightQFE.setText(str(old_val))
            min_QFE = int(old_val) 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_QFE_MIN", min_QFE) 
        self.FLOGGER_QFE_MIN = min_QFE
                  
    def floggerTugLaunchEdit2(self, mode):
        print("Delta Tug Time button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            ##min_tug_time = self.MinTugLaunchTIme.toPlainText() 
            min_tug_time = self.ui.MinTugLaunchTIme.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_DT_TUG_LAUNCH")
            ##self.MinTugLaunchTIme.setText(old_val)
            self.ui.MinTugLaunchTIme.setText(str(old_val))
            min_tug_time = int(old_val) 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DT_TUG_LAUNCH", min_tug_time) 
        self.FLOGGER_DT_TUG_LAUNCH = min_tug_time
    
    def floggerFleetCheckRadioButton(self):
        print("Fleet Check Radio Button clicked") 
        ##if self.FleetCheckRadioButton.isChecked(): 
        if self.ui.FleetCheckRadioButton.isChecked():
            print("Fleet check checked")
            self.FLOGGER_FLEET_CHECK = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_CHECK", "Y")
        else:
            print("Fleet check unchecked")
            self.FLOGGER_FLEET_CHECK = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_CHECK", "N")
         
    def floggerRecordTracksRadioButton(self):
        print("Record Tracks Radio Button clicked") 
        ##if self.RecordTracksRadioButton.isChecked():
        if self.ui.RecordTracksRadioButton.isChecked():
            print("Record Tracks checked")
            self.FLOGGER_TRACKS = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS", "Y")
        else:
            print("Record Tracks unchecked")
            self.FLOGGER_TRACKS = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS", "N")  
            
            
    def floggerLiveTestButton(self):
        print("Live | Test Radio Button clicked") 
        ##if self.LiveTestButton.isChecked():
        if self.ui.LiveTestButton.isChecked():
            print("Live | Test mode checked: Test Mode")
            self.FLOGGER_MODE = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_MODE", "test")
        else:
            print("Live | Test mode unchecked: Live Mode")
            self.FLOGGER_MODE = "live"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_MODE", "live")  
            
    def floggerTakeoffEmailButton(self):   
        print("Record Takeoff Radio Button clicked") 
        ##if self.TakeoffEmailButton.isChecked():
        if self.ui.TakeoffEmailButton.isChecked():
            print("Record Takeoff checked")
            self.FLOGGER_TAKEOFF_EMAIL = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TAKEOFF_EMAIL", "Y")
        else:
            print("Takeoff Takeoff Button unchecked")
            self.FLOGGER_TAKEOFF_EMAIL = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TAKEOFF_EMAIL", "N")  
            
    def floggerLandingEmailButton(self): 
        print("Landing Email button clicked") 
        ##if self.LandingEmailButton.isChecked():
        if self.ui.LandingEmailButton.isChecked():
            print("Landing Email button checked")
            self.FLOGGER_TAKEOFF_EMAIL = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LANDING_EMAIL", "Y")
        else:
            print("Landing Email button unchecked")
            self.FLOGGER_LANDING_EMAIL = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LANDING_EMAIL", "N")
            
    def floggerLaunchFailuresButton(self):
        print("Launch Failures button clicked") 
        ##if self.LaunchFailuresButton.isChecked():
        if self.ui.LaunchFailuresButton.isChecked():
            print("Launch Failures button checked")
            self.FLOGGER_LOG_LAUNCH_FAILURES = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_LAUNCH_FAILURES", "Y")
        else:
            print("Launch Failures button unchecked")
            self.FLOGGER_LOG_LAUNCH_FAILURES = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_LAUNCH_FAILURES", "N")
    
    def floggerLogTugsButton(self):
        print("Log Tugs button clicked") 
        ##if self.LogTugsButton.isChecked():
        if self.ui.LogTugsButton.isChecked():
            print("Log Tugs button checked")
            self.FLOGGER_LOG_TUGS = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_TUGS", "Y")
        else:
            print("Log Tugs button unchecked")
            self.FLOGGER_LOG_TUGS = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_TUGS", "N")
            
    def floggerIGCFormatButton(self):
        print("IGC Format Button clicked") 
        ##if self.IGCFormatButton.isChecked():
        if self.ui.IGCFormatButton.isChecked():
            print("IGC Format button checked")
            self.FLOGGER_TRACKS_IGC = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS_IGC", "Y")
        else:
            print("IGC Format button unchecked")
            self.FLOGGER_TRACKS_IGC = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS_IGC", "N")
             
    def floggerIncludeTugsButton(self):
        print("Include Tugs Radio Button clicked") 
        ##if self.IncludeTugsButton.isChecked():
        if self.ui.IncludeTugsButton.isChecked():
            print("Include Tugs Button checked")
            self.FLOGGER_INCLUDE_TUG_FLIGHTS = "Y"
        else:
            print("Include Tugs Button unchecked")
            self.FLOGGER_INCLUDE_TUG_FLIGHTS = "N"
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_INCLUDE_TUG_FLIGHTS", self.FLOGGER_INCLUDE_TUG_FLIGHTS)
        
            
    def floggerKeepAliveTimeEdit2_XXX(self, mode):
        print("Keep Alive Time button clicked") 
        if mode:
            keep_alive_time = self.FLOGGERKeepAliveTime.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME") 
            self.APRSKeepAliveTIme.setText(old_val)
            keep_alive_time = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_KEEPALIVE_TIME", self.FLOGGERKeep_alive_time)
        self.FLOGGER_KEEPALIVE_TIME = self.FLOGGERKeep_alive_time 
            
    def floggerDBSchemaFileEdit2(self, mode):
        print("DB Schema File button clicked")
        if mode: 
            ##db_schema_file = self.DBSchemaFile.toPlainText() 
            db_schema_file = self.ui.DBSchemaFile.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_DB_SCHEMA")
            ##self.DBSchemaFile.setText(old_val)
            self.ui.DBSchemaFile.setText(old_val)
            db_schema_file = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_SCHEMA", db_schema_file) 
        self.FLOGGER_DB_SCHEMA = db_schema_file   
                 
    def floggerDBNameEdit2(self, mode):
        print("DB Schema File button clicked")
        if mode: 
            ##db_name = self.DBName.toPlainText() 
            db_name = self.ui.DBName.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_DB_NAME")
            ##self.DBName.setText(old_val)
            self.ui.DBName.setText(old_val)
            db_name = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_NAME", db_name) 
        self.FLOGGER_DB_NAME = db_name
                       
    def floggerFlarmnetURL2(self, mode):
        print("Flarmnet URL button clicked")
        if mode: 
            ##Flarmnet_URL = self.FlarmnetURL.toPlainText() 
            Flarmnet_URL = self.ui.FlarmnetURL.toPlainText()
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_FLARMNET_DB_URL")
            ##elf.FlarmnetURL.setText(old_val)
            self.ui.FlarmnetURL.setText(old_val)
            Flarmnet_URL = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLARMNET_DB_URL", Flarmnet_URL) 
        self.FLOGGER_FLARMNET_DB_URL = Flarmnet_URL
        
                       
    def floggerOGNURL2(self, mode):
        print("OGN URL button clicked")
        if mode: 
            ##OGNURL = self.OGNURL.toPlainText()  
            OGNURL = self.ui.OGNURL.toPlainText()
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_OGN_DB_URL")
            ##self.OGNURL.setText(old_val)
            self.ui.OGNURL.setText(old_val)
            OGNURL = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_OGN_DB_URL", OGNURL) 
        self.FLOGGER_OGN_DB_URL = OGNURL
                
    def floggerSMTPServerURLEdit(self):
        print("SMTP Server URL button clicked") 
        smtp_server_URL = self.SMTPServerURL.toPlainText()  
        print("SMTP Server URL: " + smtp_server_URL)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        smtp_server_URL = self.config["FLOGGER_SMTP_SERVER_URL"]
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL   
                      
    def floggerSMTPServerURLEdit2(self, mode):
        print("SMTP Server URL button clicked")
        if mode: 
            ##smtp_server_URL = self.SMTPServerURL.toPlainText() 
            smtp_server_URL = self.ui.SMTPServerURL.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_URL")
            ##self.SMTPServerURL.setText(old_val)
            self.ui.SMTPServerURL.setText(old_val)
            smtp_server_URL = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL       
                      
    def floggerEmailSenderEdit2(self, mode):
        print("SMTP Sender Tx button clicked")
        if mode: 
            ##EmailSenderTX = self.EmailSenderTX.toPlainText() 
            EmailSenderTX = self.ui.EmailSenderTX.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_TX")
            ##self.EmailSenderTX.setText(old_val)
            self.ui.EmailSenderTX.setText(old_val)
            EmailSenderTX = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_TX", EmailSenderTX)
        self.FLOGGER_SMTP_TX = EmailSenderTX        
                      
    def floggerEmailReceiverEdit2(self, mode):
        print("SMTP Receiver Rx button clicked")
        if mode: 
            ##EmailReceiverRX = self.EmailReceiverRX.toPlainText()   
            EmailReceiverRX = self.ui.EmailReceiverRX.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_RX")
            ##self.EmailReceiverRX.setText(old_val)
            self.ui.EmailReceiverRX.setText(old_val)
            EmailReceiverRX = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_RX", EmailReceiverRX)
        self.FLOGGER_SMTP_RX = EmailReceiverRX 
                             
    def floggerSMTPServerPortEdit2(self, mode):
        print("SMTP Server Port button clicked")
        if mode :
            ##smtp_server_port = self.SMTPServerPort.toPlainText()  
            smtp_server_port = self.ui.SMTPServerPort.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_PORT")
            ##self.SMTPServerPort.setText(old_val)
            self.ui.SMTPServerPort.setText(old_val)
            smtp_server_port = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_PORT", smtp_server_port)
        self.FLOGGER_SMTP_SERVER_PORT = int(smtp_server_port) 
        
    def floggerMinFlightDeltaTimeEdit2(self, mode):     
        print("Minimum Flight Difference Time button clicked")
        if mode :
            ##MinFlightDeltaTime = self.MinFlightDeltaTime.toPlainText()  
            MinFlightDeltaTime = self.ui.MinFlightDeltaTime.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_DUPLICATE_FLIGHT_DELTA_T")
            ##self.MinFlightDeltaTime.setText(old_val)
            self.ui.MinFlightDeltaTime.setText(old_val)
            MinFlightDeltaTime = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DUPLICATE_FLIGHT_DELTA_T", MinFlightDeltaTime)
        self.FLOGGER_DUPLICATE_FLIGHT_DELTA_T = MinFlightDeltaTime
        
    def floggerFlightLogFolderEdit2(self, mode):         
        print("Flight Log Folder button clicked")
        if mode :
            ##FlightLogFolder = self.FlightLogFolder.toPlainText()
            FlightLogFolder = self.ui.FlightLogFolder.toPlainText()   
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_FLIGHTS_LOG")
            ##self.FlightLogFolder.setText(old_val)
            self.ui.FlightLogFolder.setText(old_val)
            FlightLogFolder = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLIGHTS_LOG", FlightLogFolder)
        self.FLOGGER_FLIGHTS_LOG = FlightLogFolder

        
    def floggerFloggerVersionNoEdit2(self, mode):         
        print("Flogger Version Nos clicked")
        if mode :
            ##FloggerVersionNo = self.FloggerVersionNo.toPlainText()
            FloggerVersionNo = self.ui.FloggerVersionNo.toPlainText() 
            print("FloggerVersionNo: ", str(FloggerVersionNo)) 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_FLIGHTS_LOG")
            ##self.FloggerVersionNo.setText(old_val)
            self.ui.FloggerVersionNo.setText(old_val)
            FlightLogFolder = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_VER", FloggerVersionNo)
        self.FLOGGER_VER = FloggerVersionNo       
    
                
    def floggerLandoutMsgModeEdit2(self, mode):         
        print("Landout Msg Mode button clicked")
        if mode :
            ##LandoutMsgMode = self.LandoutMsgMode.toPlainText() 
            LandoutMsgMode = self.ui.LandoutMsgMode.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_LANDOUT_MODE")
            ##self.LandoutMsgMode.setText(old_val)
            self.ui.LandoutMsgMode.setText(old_val)
            LandoutMsgMode = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LANDOUT_MODE", LandoutMsgMode)
        self.FLOGGER_LANDOUT_MODE = LandoutMsgMode
        
    def floggerAPRSBasesListEdit(self):
        print("APRS Bases list clicked")
#        sel_items = listWidget.selectedItems()
        ##sel_items = self.APRSBasesListWidget.selectedItems()
        sel_items = self.ui.APRSBasesListWidget.selectedItems()
        for item in sel_items:
            new_val = item.text()
            print(new_val)
            item.editItem()
#            item.setText(item.text()+"More Text")
     
    def floggerAPRSBaseEdit2(self, mode):  
        print("APRS Base station list called") 
        if mode:
            APRSBaseList = []
            ##APRSBaseList.append(self.APRSBase1Edit.toPlainText())
            ##APRSBaseList.append(self.APRSBase2Edit.toPlainText())
            ##APRSBaseList.append(self.APRSBase3Edit.toPlainText())
            ##APRSBaseList.append(self.APRSBase4Edit.toPlainText())
            ##APRSBaseList.append(self.APRSBase5Edit.toPlainText())
            ##APRSBaseList.append(self.APRSBase6Edit.toPlainText())
            
            APRSBaseList.append(self.ui.APRSBase1Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase2Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase3Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase4Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase5Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase6Edit.toPlainText())
            print("APRSBaseList: ", APRSBaseList)
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
            ##self.APRSBase1Edit.setText(old_val[0])
            ##self.APRSBase2Edit.setText(old_val[1])
            ##self.APRSBase3Edit.setText(old_val[2])
            ##self.APRSBase4Edit.setText(old_val[3])
            ##self.APRSBase5Edit.setText(old_val[4])
            ##self.APRSBase6Edit.setText(old_val[5])
            
            self.ui.APRSBase1Edit.setText(old_val[0])
            self.ui.APRSBase2Edit.setText(old_val[1])
            self.ui.APRSBase3Edit.setText(old_val[2])
            self.ui.APRSBase4Edit.setText(old_val[3])
            self.ui.APRSBase5Edit.setText(old_val[4])
            self.ui.APRSBase6Edit.setText(old_val[5])
            APRSBaseList = old_val
        APRSBaseList = [str(APRSBaseList[0]), 
                        str(APRSBaseList[1]), 
                        str(APRSBaseList[2]), 
                        str(APRSBaseList[3]), 
                        str(APRSBaseList[4]), 
                        str(APRSBaseList[5])]
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_APRS_BASES", APRSBaseList)
        ##self.FLOGGER_APRS_BASES = APRSBaseList 
        self.ui.FLOGGER_APRS_BASES = APRSBaseList 
        print("FLOGGER_APRS_BASES: ", self.FLOGGER_APRS_BASES)

    def floggerAdd2FleetOkButton(self):
        print("floggerAdd2FleetOkButton called")
        if self.Add2FleetRegEdit.toPlainText() == "":
            return
        rowPosition = self.FleetListTable.rowCount()          
#            print "rowPosition: ", rowPosition, " Registration: ", registration, " Code: ", settings.FLOGGER_FLEET_LIST[registration]
        self.FleetListTable.insertRow(rowPosition)
#        self.FleetListTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(self.Add2FleetRegEdit))
        self.FleetListTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(self.Add2FleetRegEdit.toPlainText()))
        self.FleetListTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(self.Add2FleetCodeEdit.toPlainText())) 
        # Add in the new registration to the dictionary 
        old_fleet_list = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
        old_fleet_list[str(self.Add2FleetRegEdit.toPlainText())] = str(self.Add2FleetCodeEdit.toPlainText())
        # Output the updated FleetList to the config file
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_LIST", old_fleet_list)
        settings.FLOGGER_FLEET_LIST = old_fleet_list
        print("FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST)
        # Set fields on form to balnk
        self.Add2FleetRegEdit.setText("")
        self.Add2FleetCodeEdit.setText("")   
        
    def floggerAdd2FleetCancelButton(self): 
        print("floggerAdd2FleetCancelButton called")
        self.Add2FleetRegEdit.setText("")
        self.Add2FleetCodeEdit.setText("")  
        
    def floggerDelFromFleetOkButton(self):
        print("floggerDelFromFleetOkButton")
        if self.DelFromFleetEdit.toPlainText() == "":
            return
        fleet_list = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
        reg = self.DelFromFleetEdit.toPlainText()
        del fleet_list[str(reg)]
#        print "fleet_list: ", fleet_list
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_LIST", fleet_list)
        settings.FLOGGER_FLEET_LIST = fleet_list
        self.DelFromFleetEdit.setText("")
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_LIST")
        print("FLOGGER_FLEET_LIST now: ", self.FLOGGER_FLEET_LIST) 
        for key in list(old_val.keys()):
            # Convert string form of value to int
            old_val[key] = int(old_val[key])
#            print "Key: ", key, " = ", int(old_val[key])
        print("FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST)
        
        self.FleetListTable.clearContents()
        self.FleetListTable.setRowCount(0)
        rowPosition = self.FleetListTable.rowCount()
#        rowPosition = 0
        for registration in settings.FLOGGER_FLEET_LIST:
            print("rowPosition: ", rowPosition, " Registration: ", registration, " Code: ", settings.FLOGGER_FLEET_LIST[registration])
            self.FleetListTable.insertRow(rowPosition)   
            self.FleetListTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(registration))
            self.FleetListTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(settings.FLOGGER_FLEET_LIST[registration])))
            rowPosition = rowPosition + 1 # interesting rowPosition =+ 1 gives wrong result!!
    
    def floggerOkpushButton(self):
        print("About Ok button clicked")
        self.close()
        
    def floggerFlightLog(self):
        
        def setColourtoRow(table, rowIndex, colour):
            for j in range(table.columnCount()):
                table.item(rowIndex, j).setBackground(colour)
                
        print("Flight Log calendar clicked")
##        date_conv = time.strptime(str(self.FlightLogcalendar.selectedDate().toString()),"%a %b %d %Y")
        date_conv = time.strptime(str(self.ui.FlightLogcalendar.selectedDate().toString()),"%a %b %d %Y")
#        print time.strftime("%d/%m/%Y",date_conv)
        date = time.strftime("%y/%m/%d",date_conv)
        print(date)
        # Get flights for date
        try:
            flogger_db_path = path_join_dd(os.path.abspath(__file__), ["db", "flogger.sql3.2"])
            print("DB name(new): ", flogger_db_path)
            db = sqlite3.connect(flogger_db_path) 
            cursor = db.cursor()
        except:
            print("Failed to connect to db")
        try:
            cursor.execute("SELECT flight_no, sdate, stime, etime, duration, src_callsign, max_altitude, registration, track_file_name, tug_registration, tug_altitude, tug_model  FROM flights WHERE sdate=? ORDER BY stime DESC", (date,))
            # row[0] = flight_no, 
            # row[1] = sdate, 
            # row[2] = stime, 
            # row[3] = etime, 
            # row[4] = duration, 
            # row[5] = src_callsign, 
            # row[6] = max_altitude, 
            # row[7] = registration, 
            # row[8] = track_file_name, 
            # row[9] = tug_registration, 
            # row[10] = tug_altitude, 
            # row[11] = tug_model 
        except:
            print("Select failed")
        rows = cursor.fetchall()
        row_count = cursor.rowcount
        if row_count <= -1:
            row_count = 0
        print("row_count: ", row_count)
        header = self.ui.FlightLogTable.horizontalHeader()
##        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        col_nos = 0
        while col_nos < 9:
##            header.setResizeMode(col_nos, QtGui.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(col_nos, QtWidgets.QHeaderView.ResizeToContents)
            col_nos = col_nos + 1
        self.ui.FlightLogTable.clearContents()
        self.ui.FlightLogTable.setRowCount(0)
        rowPosition = self.ui.FlightLogTable.rowCount()
        self.ui.FlightLogTable.setColumnHidden(10, True)
#        row_count = 1
        for row in rows:  
#            print "Row: ", row_count
            in_fleet = True 
            try:
                if settings.FLOGGER_FLEET_LIST[row[7]] > 100 and \
                    settings.FLOGGER_FLEET_LIST[row[7]] <= 200 and \
                    settings.FLOGGER_INCLUDE_TUG_FLIGHTS != "Y":
                    print("Tug only flight so ignore tug: ", row[7])
                    continue
            except KeyError:
                print("Glider not in Fleet hence not a tug: ", row[7]) 
                in_fleet = False                       
            self.ui.FlightLogTable.insertRow(rowPosition)   
#            if row[9] is None: 
            val = "----"                # Default value
            if row[9] is None and row[10] is None and row[11] is None:
                # Check if it's in the fleet?
                if in_fleet:
                    # Is it a motor glider?
                    if settings.FLOGGER_FLEET_LIST[row[7]] > 200 and \
                        settings.FLOGGER_FLEET_LIST[row[7]] <= 300:
                        # It is so blanks
                        val = "----"
                    else:
                        # Must be a winch launch of glider, ie non-motor glider or non-fleet glider, but may be self launcher??
                        val = "Winch"
            else:
                val = row[9]
            self.ui.FlightLogTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(val))           # Tug Reg
            if row[11] is None:
                val = "----"
            else:
                val = row[11]
            self.ui.FlightLogTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(val))           # Tug Type
            self.ui.FlightLogTable.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(row[7]))        # (Moto) Glider     
            self.ui.FlightLogTable.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(row[7][3:]))    # CN
            cursor.execute("SELECT aircraft_model FROM flarm_db WHERE registration = ?", (row[7],))
            plane_type = cursor.fetchone()
            if plane_type[0] == None:
                print("Aircraft_model not found, try Type for Registration : ", row[7])
                cursor.execute("SELECT type FROM flarm_db WHERE registration = ?", (row[7],))   
                plane_type = cursor.fetchone()
            print("Plane Type/model is: ", plane_type[0])
            self.ui.FlightLogTable.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(plane_type[0])) # Plane Type/Model 
            self.ui.FlightLogTable.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(row[2]))        # Glider Takeoff TIme
            self.ui.FlightLogTable.setItem(rowPosition , 6, QtWidgets.QTableWidgetItem(row[3]))        # Glider Landing Time
            self.ui.FlightLogTable.setItem(rowPosition , 7, QtWidgets.QTableWidgetItem(row[4]))        # Glider Flight Time
            if row[10] is None:
                val = "----"
            else:
                val = row[10]
            self.ui.FlightLogTable.setItem(rowPosition , 8, QtWidgets.QTableWidgetItem(val))            # Tug Max ALt (QFE)
            self.ui.FlightLogTable.setItem(rowPosition , 9, QtWidgets.QTableWidgetItem(row[6]))
            self.ui.FlightLogTable.setItem(rowPosition , 10, QtWidgets.QTableWidgetItem(row[8]))

            if row_count % 2 == 0:
                colour = QtGui.QColor(204,255,204)      # Light green 
            else:
                colour = QtGui.QColor(128,255,128)      # Darker green
            setColourtoRow(self.ui.FlightLogTable, rowPosition, colour)     
            row_count = row_count + 1

##    def floggerFlightLogDoubleClicked(self):
##        print("Double Clicked called")
##        self.change_status("Building Track Map...", "orange")
##        self.ui.FlightLogTable.setColumnHidden(10, False)
##        index = self.ui.FlightLogTable.selectedIndexes()
##        
##        print('selected item index found at %s with data: %s' % (index[10].row(), index[10].data().toString()))
##        track_file = index[10].data().toString()
##        self.ui.FlightLogTable.setColumnHidden(10, True)    
##        gpx_file = open(track_file, 'r')
##        gpx = gpxpy.parse(gpx_file)       
##        lat = []
##        lon = []   
##        for track in gpx.tracks:
##            for segment in track.segments:
##                for point in segment.points:
##                    lat.append(point.latitude)
##                    lon.append(point.longitude)
##        #fig = plt.figure(facecolor = '0.05')
##        fig = plt.figure(facecolor = 'w')
##        ax = plt.Axes(fig, [0., 0., 1., 1.], )
##        ax.set_aspect('equal')
##        ax.set_axis_off()
##        fig.add_axes(ax)
##        plt.plot(lon, lat, color = 'black', lw = 1.0, alpha = 0.8)
##        try:
##            mplleaflet.show()
##            mplleaflet.display()
##            
##        except:
##            print("Display track failed")
##        self.change_status("Waiting for sunrise...", "yellow")
        
        
        
#
# Utility functions
# 
    
    def AboutButton(self):
        print("About menu clicked")
        window = AboutWindow(self)
        window.show()
          
    def HelpButton(self):
        print("Help menu clicked")
        window = HelpWindow(self)
        window.show()
          
#    def EditButton(self):
#        print "Edit menu clicked"
#        window = EditWindow(self)
#        window.show()
#
# Actions End
#            
    







       
##    def floggerStart(self):       
    def floggerStart_old(self):
        print("flogger start")
        print("FLOGGER_KEEPALIVE_TIME at start is:", self.FLOGGER_KEEPALIVE_TIME)
        settings.FLOGGER_RUN = True
        flogger = flogger3()
        #self.RunningLabel.setText("Logging Data...")
        #self.RunningProgressBar.setProperty("maximum", 0)
        self.change_status("Logging Data...", "green") 
        flogger.change_status.connect(self.change_status)
        flogger.set_flight_count.connect(self.set_flight_count)
        flogger.set_sunset.connect(self.set_sunset)
        flogger.flogger_run(settings, flogger)
        
#
# End setup
#

#
#  itialisation end
#  

#
# Actions Start. Menu Bar
#      
##    def floggerStart(self):      
    def floggerStart_old(self):
        print("flogger start")
        print("FLOGGER_KEEPALIVE_TIME at start is:", self.FLOGGER_KEEPALIVE_TIME)
        settings.FLOGGER_RUN = True
        flogger = flogger3()
        #self.RunningLabel.setText("Logging Data...")
        #self.RunningProgressBar.setProperty("maximum", 0)
        self.change_status("Logging Data...", "green") 
        flogger.change_status.connect(self.change_status)
        flogger.set_flight_count.connect(self.set_flight_count)
        flogger.set_sunset.connect(self.set_sunset)
        flogger.flogger_run(settings, flogger)
        
##    def change_status(self, state, colour):        
    def change_status_old(self, state, colour):
        # Slot for status change signalled from data collection thread
        print("\nGUI change called with: ", " State: ", state, " Colour: ", colour, "\n")
        
        print("change_status. State: ", state, " Colour: ", colour)
        self.ui.RunningLabel.setStyleSheet("color: " + colour)
        self.ui.RunningLabel.setText(state)
        self.ui.RunningProgressBar.setProperty("maximum", 0)
        return
            
##    def set_flight_count_old(self, number, flightReg, flightEndTime):            
    def set_flight_count(self, number, flightReg, flightEndTime):
        print("set_flight_count called-2: ", number, " Registration: ", flightReg, " Flight end time: ", flightEndTime)
        self.ui.FlightCount.display(int(number))
        self.ui.LastFlightReg.setText(str(flightReg))
        self.ui.FlightEndTime.setText(str(flightEndTime))
        
    def set_sunset_old(self, ssdt):        
##    def set_sunset(self, ssdt):
        print("Display local sunset time", ssdt)
        self.ui.SunsetTime.setText(ssdt)
        
    def floggerStop_old(self):        
##    def floggerStop(self):
        settings.FLOGGER_RUN = False
        self.ui.RunningLabel.setStyleSheet("color: red")
        self.ui.RunningLabel.setText("Stopped")
        self.ui.RunningProgressBar.setProperty("maximum", 1)
        print("flogger stop")
        
    def floggerFlying_End_old(self):        
##    def floggerFlying_End(self):
        #
        # Add check that all flights taken off have landed
        # Basically this does what floggerFlightLog() does without the date stuff
        #
        settings.FLOGGER_RUN = False
        self.ui.RunningLabel.setStyleSheet("color: yellow")
        self.ui.RunningLabel.setText("Flying Ended")
        self.ui.RunningProgressBar.setProperty("maximum", 1)
        print("flogger Flying Ended, Process DB")
        try:
            flogger_db_path = path_join_dd(os.path.abspath(__file__), ["db", "flogger.sql3.2"])
            print("DB name(new): ", flogger_db_path)
            db = sqlite3.connect(flogger_db_path) 
            cursor = db.cursor()
        except:
            print("Failed to connect to db")
        print("Stop Data Collection Cycle")
        settings.FLOGGER_RUN = False
        process_log(cursor, db, settings)
        print("Flogger DB processed")
        
    
    def floggerQuit_old(self):    
##    def floggerQuit(self):
        print("flogger quit")
        
    def floggerSetState_old(self, stateTxt, colour):        
##    def floggerSetState(self, stateTxt, colour):
        print("flogger set state: ", stateTxt, " ", colour) 
        self.ui.RunningLabel.setStyleSheet("color: " + colour)
        self.ui.RunningLabel.setText(stateTxt)
        self.ui.RunningProgressBar.setProperty("maximum", 1)
        

#
# Action Config Menu Bar
#
    def floggerEdit_old(self):
##    def floggerEdit(self):
        print("flogger Config.edit")
        self.floggerUpdateConfig()
        print("flogger Config.edit end")
        
#
# Actions Start, update fields
#

    def floggerUpdateConfig_old(self):
##    def floggerUpdateConfig(self):
        print("floggerUpdateConfig called")
        self.floggerAirfieldEdit2(True)
        self.floggerAirfieldDetailsEdit2(True)
        self.floggerAPRSUserEdit2(True)
        self.floggerAPRSPasscodeEdit2(True)
        self.floggerAPRSServerhostEdit2(True)
        self.floggerAPRSServerportEdit2(True)
        self.floggerFlarmRadiusEdit2(True)
        self.floggerLandoutRadiusEdit2(True)
##
## 20220520 Added code to change/set Airfield Radius 
##
        self.floggerAirfieldRadiusEdit2(True)
        self.floggerDataRetentionTimeEdit2(True)
        self.floggerAirfieldLatLonEdit2(True)
        self.floggerMinFlightTimeEdit2(True)
        self.floggerMinTakeoffVelocityEdit2(True)
        self.floggerMinLandingVelocityEdit2(True)
        self.floggerMinFlightQFEEdit2(True)
        self.floggerTugLaunchEdit2(True)
        self.floggerKeepAliveTimeEdit2(True)
        self.floggerDBSchemaFileEdit2(True)
        self.floggerDBNameEdit2(True)
        self.floggerFlarmnetURL2(True)
        self.floggerOGNURL2(True)
        self.floggerSMTPServerURLEdit2(True)
        self.floggerSMTPServerPortEdit2(True)
        self.floggerEmailSenderEdit2(True)
        self.floggerEmailReceiverEdit2(True)
        self.floggerAPRSBaseEdit2(True)
        self.floggerLogTimeDeltaEdit2(True)
        self.floggerHorizonAdjustmentEdit2(True)
        self.floggerMinFlightDeltaTimeEdit2(True)
        self.floggerMinFlightDeltaTimeEdit2(True)
        self.floggerAirfieldQNHEdit2(True)
        self.floggerFlightLogFolderEdit2(True)
        self.floggerFloggerVersionNoEdit2(True)
        self.floggerLandoutMsgModeEdit2(True)
#        self.floggerIncludeTugFlightsEdit2(True)
        try:
            self.config.write()
        except:
            print("Writing updated config file, flogger_settings_file.txt FAILED")
        return



##    def floggerCancelConfigUpdate(self):
    def floggerCancelConfigUpdate_old(self):
        print("floggerCancelConfigUpdate called")
        self.floggerAirfieldEdit2(False)
        self.floggerAirfieldDetailsEdit2(False)
        self.floggerAPRSUserEdit2(False)
        self.floggerAPRSPasscodeEdit2(False)
        self.floggerAPRSServerhostEdit2(False)
        self.floggerAPRSServerportEdit2(False)
        self.floggerFlarmRadiusEdit2(False)
        self.floggerLandoutRadiusEdit2(False)
        self.floggerDataRetentionTimeEdit2(False)
        self.floggerAirfieldLatLonEdit2(False)
        self.floggerMinFlightTimeEdit2(False)
        self.floggerMinTakeoffVelocityEdit2(False)
        self.floggerMinLandingVelocityEdit2(False)
        self.floggerMinFlightQFEEdit2(False)
        self.floggerTugLaunchEdit2(False)
        self.floggerKeepAliveTimeEdit2(False)
        self.floggerDBSchemaFileEdit2(False)
        self.floggerDBNameEdit2(False)
        self.floggerFlarmnetURL2(False)
        self.floggerOGNURL2(False)
        self.floggerSMTPServerURLEdit2(False)
        self.floggerSMTPServerPortEdit2(False)
        self.floggerEmailSenderEdit2(False)
        self.floggerEmailReceiverEdit2(False)
        self.floggerAPRSBaseEdit2(False)
        self.floggerLogTimeDeltaEdit2(False)
        self.floggerHorizonAdjustmentEdit2(False)
        self.floggerMinFlightDeltaTimeEdit2(False)
        self.floggerAirfieldQNHEdit2(False)
        self.floggerFlightLogFolderEdit2(False)
        self.floggerFloggerVersionNoEdit2(True)
        self.floggerLandoutMsgModeEdit2(False)
#        self.floggerIncludeTugFlightsEdit2(False)
        return
    
##    def floggerTPOkButton(self):    
    def floggerTPOkButton_old(self):
        print("Add TP")
        field1 = self.AddTPInfo.item(0,0)
        if field1 != "":
            # Add a new turing point row
            print("Add new TP")
            return
        field2 = self.RemoveTPInfo.item(0,0)
        if field2 != "":
            # Remove turning pont row
            return
    
    def floggerTPCancelButton(self):    
##    def floggerTPCancelButton_old(self):
        return               
        
##    def floggerAirfieldEdit2(self, mode):
    def floggerAirfieldEdit2_old(self, mode):
        # Mode: True - update all fields, variables to latest values
        
        #       False - restore all fields and variables to values from config (settings.txt) file
        print("Base Airfield button clicked ", "Mode: ", mode) 
        if mode:
            # Values have been put into gui field from setting.txt and may then have been changed interactively
            airfield_base = self.ui.AirfieldBase.toPlainText() 
        else:
            # Restore old values from settings.txt
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
#            settings.FLOGGER_AIRFIELD_NAME = old_val
            print(settings.FLOGGER_AIRFIELD_NAME)
            self.ui.AirfieldBase.setText(old_val)
            print("Airfield Base: " + old_val)
            airfield_base = old_val
        # Put current value into settings.txt file for future use
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_NAME", airfield_base)
        # Now update python variable to current value in gui and settings.txt
        print("FLOGGER_AIRFIELD_NAME from settings.py: ", settings.FLOGGER_AIRFIELD_NAME)
        

        
##    def floggerAPRSUserEdit2(self, mode):        
    def floggerAPRSUserEdit2_old(self, mode):
        print("APRS User button clicked")
        if mode: 
            APRSUser = self.ui.APRSUser.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "APRS_USER")
            self.ui.APRSUser.setText(old_val)
            APRSUser = old_val
#       print "Airfield B: " + airfield_base
        self.editConfigField("flogger_settings_file.txt", "APRS_USER", APRSUser)
        self.ui.APRS_USER = APRSUser
        

##    def floggerAPRSPasscodeEdit2(self, mode):
    def floggerAPRSPasscodeEdit2_old(self, mode):
            print("APRS Passcode button clicked")
            if mode: 
                APRSPasscode = self.ui.APRSPasscode.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "APRS_PASSCODE")
                self.ui.APRSPasscode.setText(old_val)
                APRSPasscode = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_PASSCODE", APRSPasscode)
            self.APRS_PASSCODE = APRSPasscode
            
    
##    def floggerAPRSServerhostEdit2(self, mode):    
    def floggerAPRSServerhostEdit2_old(self, mode):
            print("APRS Server Host button clicked")
            if mode: 
                APRSServerhost = self.ui.APRSServerHostName.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")
                self.ui.APRSServerHostName.setText(old_val)
                APRSServerhost = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_SERVER_HOST", APRSServerhost)
            self.APRS_SERVER_HOST = APRSServerhost
            
    
##    def floggerAPRSServerportEdit2(self, mode):    
    def floggerAPRSServerportEdit2_old(self, mode):
            print("APRS Server Port button clicked")
            if mode: 
                APRSServerport = self.ui.APRSServerPort.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")
                self.ui.APRSServerPort.setText(old_val)
                APRSServerport = old_val
            self.editConfigField("flogger_settings_file.txt", "APRS_SERVER_PORT", APRSServerport)
            self.APRS_SERVER_PORT = int(APRSServerport) 
                   
#    def floggerAPRSKeepAliveTimeEdit2(self, mode):
#        print "APRS Keep Alive Time copy"
#        if mode: 
#            APRSUser = self.APRSUser.toPlainText()  
#        else:
#            old_val = self.getOldValue(self.config, "APRS_USER")
#            self.APRSUser.setText(old_val)
#            APRSUser = old_val
#       print "Airfield B: " + airfield_base
#        self.editConfigField("flogger_settings_file.txt", "FLOGGER_KEEPALIVE_TIME", self.FLOGGERKeepAliveTime)
#        self.APRS_USER = APRSUser
            
##    def floggerDataRetentionTimeEdit2(self, mode):             
    def floggerDataRetentionTimeEdit2_old(self, mode):
            print("Data Retention TIme button clicked")
            if mode: 
                DataRetentionTime = self.ui.DataRetentionTime.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_DATA_RETENTION")
                self.ui.DataRetentionTime.setText(old_val)
                DataRetentionTime = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_DATA_RETENTION", DataRetentionTime)
            self.FLOGGER_DATA_RETENTION = int(DataRetentionTime)
            
##    def floggerLogTimeDeltaEdit2(self, mode):               
    def floggerLogTimeDeltaEdit2_old(self, mode):  
            print("Log Time Delta button clicked")
            if mode: 
                LogTimeDelta = self.ui.LogTimeDelta.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_LOG_TIME_DELTA")
                self.ui.LogTimeDelta.setText(old_val)
                LogTimeDelta = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_TIME_DELTA", LogTimeDelta)
            self.FLOGGER_LOG_TIME_DELTA = int(LogTimeDelta)
        
##    def floggerHorizonAdjustmentEdit2(self, mode):           
    def floggerHorizonAdjustmentEdit2_old(self, mode):
            print("Horizon Adjustment button clicked")
            if mode: 
                HorizonAdjustment = self.ui.HorizonAdjustment.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_LOCATION_HORIZON")
                self.ui.HorizonAdjustment.setText(old_val)
                HorizonAdjustment = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOCATION_HORIZON", HorizonAdjustment)
            self.FLOGGER_LOCATION_HORIZON = HorizonAdjustment
            
##    def floggerAirfieldQNHEdit2(self, mode):            
    def floggerAirfieldQNHEdit2_old(self, mode):
        print("QNH Setting button clicked")
        if mode: 
            AirfieldQNH = self.ui.AirfieldQNH.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_QNH")
            self.ui.AirfieldQNH.setText(old_val)
            AirfieldQNH = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_QNH", AirfieldQNH)
#        self.FLOGGER_QNH = int(AirfieldQNH)
        self.FLOGGER_QNH = AirfieldQNH
        
##    def floggerFlarmRadiusEdit2(self, mode):        
    def floggerFlarmRadiusEdit2_old(self, mode):
            print("Flarm Radius button clicked")
            if mode: 
                FlarmRadius = self.ui.AirfieldFlarmRadius.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_RAD")
                self.ui.AirfieldFlarmRadius.setText(old_val)
                FlarmRadius = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_RAD", FlarmRadius)
            self.FLOGGER_RAD = int(FlarmRadius)
   
##    def floggerLandoutRadiusEdit2(self, mode):   
    def floggerLandoutRadiusEdit2_old(self, mode):
            print("Flarm Radius button clicked")
            if mode: 
                LandOutRadius = self.ui.LandOutRadius.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_LIMIT")
                self.ui.LandOutRadius.setText(old_val)
                LandOutRadius = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_LIMIT", LandOutRadius)
            self.FLOGGER_AIRFIELD_LIMIT = int(LandOutRadius)
            
##
## 20220520 Added code to change/set Airfield Radius 
##
    def floggerAirfieldRadiusEdit2(self, mode):
            print("Airfield Radius button clicked")
            if mode: 
                AirfieldRadius = self.ui.AirfieldRadius.toPlainText()  
            else:
                old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_RADIUS")
                self.ui.AirfieldRadius.setText(old_val)
                AirfieldRadius = old_val
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_RADIUS", AirfieldRadius)
            self.FLOGGER_AIRFIELD_RADIUS = int(AirfieldRadius)
        
            
##    def floggerAirfieldDetailsEdit2(self, mode):            
    def floggerAirfieldDetailsEdit2_old(self, mode):
        #
        # This needs to be changed determine the Lat/Long is AirfieldDetails is supplied
        # and write them back to the form and to settings.py.  Most of the code is similar
        # to that below except the lat/long have to found from the get_coords function
        # in flogger3.py
        #
        print("Airfield Details button clicked. Mode: ", mode)
        if mode:
            airfield_details = self.ui.AirfieldDetails.toPlainText()
            print("Airfield Details: ", airfield_details, " QNH: ", settings.FLOGGER_QNH)
            if airfield_details != "":
                loc = get_coords(airfield_details, settings)
                print("get_coords rtns: ", loc)
                lat = str(loc[0])    # returned as numbers, convert to string
                lon = str(loc[1])    # as above
                qnh = str(loc[2])    # as above    
                self.editConfigField("flogger_settings_file.txt", "FLOGGER_LATITUDE", lat)
                self.editConfigField("flogger_settings_file.txt", "FLOGGER_LONGITUDE", lon)
                self.editConfigField("flogger_settings_file.txt", "FLOGGER_QNH", qnh)
                # The following is just to get Lat & Lon into the right format for display on form
                latlon = LatLon(Latitude(lat), Longitude(lon))
                latlonStr = latlon.to_string('D% %H')
                print("latlonStr: ", latlonStr)
                self.ui.AirfieldLatitude.setText(latlonStr[0])
                self.ui.AirfieldLongitude.setText(latlonStr[1])
                self.ui.AirfieldQNH.setText(qnh)
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")
            self.ui.AirfieldDetails.setText(old_val)
            airfield_details = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_AIRFIELD_DETAILS", airfield_details)

##    def floggerAirfieldLatLonEdit2(self, mode):
    def floggerAirfieldLatLonEdit2_old(self, mode):
        print("Airfield latitude, longitude called")
        if mode:
            airfieldLat = self.ui.AirfieldLatitude.toPlainText()
            airfieldLon = self.ui.AirfieldLongitude.toPlainText()
            airfieldlatlon = string2latlon(str(airfieldLat), str(airfieldLon), 'D% %H')
            print("Airfield lat/lon: ", airfieldlatlon)
            airfieldLatLonStr = airfieldlatlon.to_string("%D")
            print("Update Lat/Lon: ", airfieldLatLonStr)
            print("Latlonstr: ", airfieldLatLonStr[0], " :", airfieldLatLonStr[1])
            old_val_lat = airfieldLatLonStr[0]
            old_val_lon = airfieldLatLonStr[1]
        else:
            old_val_lat = self.getOldValue(self.config, "FLOGGER_LATITUDE")
            old_val_lon = self.getOldValue(self.config, "FLOGGER_LONGITUDE")
            print("Old Lat: ", old_val_lat, " Old Lon: ", old_val_lon)
            airfieldlatlon = LatLon(Latitude(old_val_lat), Longitude(old_val_lon))
            print("airfieldlatlon: ", airfieldlatlon)
            airfieldLatLonStr = airfieldlatlon.to_string('D% %H')
            print("airfieldlatlonStr: ", airfieldLatLonStr)
            self.ui.AirfieldLatitude.setText(airfieldLatLonStr[0])
            self.ui.AirfieldLongitude.setText(airfieldLatLonStr[1])
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LATITUDE", old_val_lat)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LONGITUDE", old_val_lon)
        return
                  
##    def floggerMinFlightTimeEdit2(self, mode):                  
    def floggerMinFlightTimeEdit2_old(self, mode):
        print("Min Flight Time button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_flight_time = self.ui.MinFlightTime.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")
            self.ui.MinFlightTime.setText(old_val)
            min_flight_time = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_MIN_FLIGHT_TIME", min_flight_time) 
        
                  
##    def floggerMinTakeoffVelocityEdit2(self, mode):                  
    def floggerMinTakeoffVelocityEdit2_old(self, mode):
        print("Min Takeoff Velocity button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_takeoff_velocity = self.ui.MinFlightTakeoffVelocity.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_V_TAKEOFF_MIN")
            self.ui.MinFlightTakeoffVelocity.setText(old_val)
            min_takeoff_velocity = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_V_TAKEOFF_MIN", min_takeoff_velocity) 
        
                  
##    def floggerMinLandingVelocityEdit2(self, mode):                  
    def floggerMinLandingVelocityEdit2_old(self, mode):
        print("Min Landing Velocity button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_landing_velocity = self.ui.MinFlightLandingVelocity.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_V_LANDING_MIN")
            self.ui.MinFlightLandingVelocity.setText(old_val)
            min_landing_velocity = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_V_LANDING_MIN", min_landing_velocity) 
        
                  
##    def floggerMinFlightQFEEdit2(self, mode):                  
    def floggerMinFlightQFEEdit2_old(self, mode):
        print("Min QFE button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_QFE = self.ui.MinFlightQFE.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_QFE_MIN")
            self.ui.MinFlightQFE.setText(str(old_val))
            min_QFE = int(old_val) 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_QFE_MIN", min_QFE) 
        self.FLOGGER_QFE_MIN = min_QFE
                  
##    def floggerTugLaunchEdit2(self, mode):                  
    def floggerTugLaunchEdit2_old(self, mode):
        print("Delta Tug Time button clicked")
        # Note. Format is "HH:MM:SS" ie a string
        if mode:
            min_tug_time = self.ui.MinTugLaunchTIme.toPlainText() 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_DT_TUG_LAUNCH")
            self.ui.MinTugLaunchTIme.setText(old_val)
            min_tug_time = int(old_val) 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DT_TUG_LAUNCH", min_tug_time) 
        self.FLOGGER_DT_TUG_LAUNCH = min_tug_time
    
##    def floggerFleetCheckRadioButton(self):    
    def floggerFleetCheckRadioButton_old(self):
        print("Fleet Check Radio Button clicked") 
        if self.ui.FleetCheckRadioButton.isChecked():
            print("Fleet check checked")
            self.FLOGGER_FLEET_CHECK = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_CHECK", "Y")
        else:
            print("Fleet check unchecked")
            self.FLOGGER_FLEET_CHECK = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_CHECK", "N")
         
##    def floggerRecordTracksRadioButton(self):         
    def floggerRecordTracksRadioButton_old(self):
        print("Record Tracks Radio Button clicked") 
        if self.ui.RecordTracksRadioButton.isChecked():
            print("Record Tracks checked")
            self.FLOGGER_TRACKS = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS", "Y")
        else:
            print("Record Tracks unchecked")
            self.FLOGGER_TRACKS = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS", "N")  
            
            
##    def floggerLiveTestButton(self):            
    def floggerLiveTestButton_old(self):
        print("Live | Test Radio Button clicked") 
        if self.ui.LiveTestButton.isChecked():
            print("Live | Test mode checked: Test Mode")
            self.FLOGGER_MODE = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_MODE", "test")
        else:
            print("Live | Test mode unchecked: Live Mode")
            self.FLOGGER_MODE = "live"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_MODE", "live")  
            
##    def floggerTakeoffEmailButton(self):             
    def floggerTakeoffEmailButton_old(self):  
        print("Record Takeoff Radio Button clicked") 
        if self.ui.TakeoffEmailButton.isChecked():
            print("Record Takeoff checked")
            self.FLOGGER_TAKEOFF_EMAIL = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TAKEOFF_EMAIL", "Y")
        else:
            print("Takeoff Takeoff Button unchecked")
            self.FLOGGER_TAKEOFF_EMAIL = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TAKEOFF_EMAIL", "N")  
            
##    def floggerLandingEmailButton(self):             
    def floggerLandingEmailButton_old(self):
        print("Landing Email button clicked") 
        if self.ui.LandingEmailButton.isChecked():
            print("Landing Email button checked")
            self.FLOGGER_TAKEOFF_EMAIL = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LANDING_EMAIL", "Y")
        else:
            print("Landing Email button unchecked")
            self.FLOGGER_LANDING_EMAIL = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LANDING_EMAIL", "N")
            
##    def floggerLaunchFailuresButton(self):            
    def floggerLaunchFailuresButton_old(self):
        print("Launch Failures button clicked") 
        if self.ui.LaunchFailuresButton.isChecked():
            print("Launch Failures button checked")
            self.FLOGGER_LOG_LAUNCH_FAILURES = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_LAUNCH_FAILURES", "Y")
        else:
            print("Launch Failures button unchecked")
            self.FLOGGER_LOG_LAUNCH_FAILURES = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_LAUNCH_FAILURES", "N")
    
##    def floggerLogTugsButton(self):    
    def floggerLogTugsButton_old(self):
        print("Log Tugs button clicked") 
        if self.ui.LogTugsButton.isChecked():
            print("Log Tugs button checked")
            self.FLOGGER_LOG_TUGS = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_TUGS", "Y")
        else:
            print("Log Tugs button unchecked")
            self.FLOGGER_LOG_TUGS = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_LOG_TUGS", "N")
            
##    def floggerIGCFormatButton(self):            
    def floggerIGCFormatButton_old(self):
        print("IGC Format Button clicked") 
        if self.ui.IGCFormatButton.isChecked():
            print("IGC Format button checked")
            self.FLOGGER_TRACKS_IGC = "Y"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS_IGC", "Y")
        else:
            print("IGC Format button unchecked")
            self.FLOGGER_TRACKS_IGC = "N"
            self.editConfigField("flogger_settings_file.txt", "FLOGGER_TRACKS_IGC", "N")
             
##    def floggerIncludeTugsButton(self):             
    def floggerIncludeTugsButton_old(self):
        print("Include Tugs Radio Button clicked") 
        if self.ui.IncludeTugsButton.isChecked():
            print("Include Tugs Button checked")
            self.FLOGGER_INCLUDE_TUG_FLIGHTS = "Y"
        else:
            print("Include Tugs Button unchecked")
            self.FLOGGER_INCLUDE_TUG_FLIGHTS = "N"
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_INCLUDE_TUG_FLIGHTS", self.FLOGGER_INCLUDE_TUG_FLIGHTS)
        
            
    def floggerKeepAliveTimeEdit2(self, mode):            
##    def floggerKeepAliveTimeEdit2_old(self, mode):
        print("Keep Alive Time button clicked") 
        if mode:
            keep_alive_time = self.ui.APRSKeepAliveTIme.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME") 
            self.ui.APRSKeepAliveTIme.setText(old_val)
            keep_alive_time = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_KEEPALIVE_TIME", keep_alive_time)
        self.FLOGGER_KEEPALIVE_TIME = int(keep_alive_time) 
        print("FLOGGER_KEEPALIVE_TIME: ", keep_alive_time)
            
##    def floggerDBSchemaFileEdit2(self, mode):            
    def floggerDBSchemaFileEdit2_old(self, mode):
        print("DB Schema File button clicked")
        if mode: 
            db_schema_file = self.ui.DBSchemaFile.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_DB_SCHEMA")
            self.ui.DBSchemaFile.setText(old_val)
            db_schema_file = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_SCHEMA", db_schema_file) 
        self.FLOGGER_DB_SCHEMA = db_schema_file   
                 
##    def floggerDBNameEdit2(self, mode):                 
    def floggerDBNameEdit2_old(self, mode):
        print("DB Schema File button clicked")
        if mode: 
            db_name = self.ui.DBName.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_DB_NAME")
            self.ui.DBName.setText(old_val)
            db_name = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DB_NAME", db_name) 
        self.FLOGGER_DB_NAME = db_name
                       
##    def floggerFlarmnetURL2(self, mode):                       
    def floggerFlarmnetURL2_old(self, mode):
        print("Flarmnet URL button clicked")
        if mode: 
            Flarmnet_URL = self.ui.FlarmnetURL.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_FLARMNET_DB_URL")
            self.ui.FlarmnetURL.setText(old_val)
            Flarmnet_URL = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLARMNET_DB_URL", Flarmnet_URL) 
        self.FLOGGER_FLARMNET_DB_URL = Flarmnet_URL
        
                       
##    def floggerOGNURL2(self, mode):                       
    def floggerOGNURL2_old(self, mode):
        print("OGN URL button clicked")
        if mode: 
            OGNURL = self.ui.OGNURL.toPlainText() 
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_OGN_DB_URL")
            self.ui.OGNURL.setText(old_val)
            OGNURL = old_val 
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_OGN_DB_URL", OGNURL) 
        self.FLOGGER_OGN_DB_URL = OGNURL
                
    def floggerSMTPServerURLEdit_old(self):
        print("SMTP Server URL button clicked") 
        smtp_server_URL = self.ui.SMTPServerURL.toPlainText()  
        print("SMTP Server URL: " + smtp_server_URL)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        smtp_server_URL = self.config["FLOGGER_SMTP_SERVER_URL"]
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL   
                      
##    def floggerSMTPServerURLEdit2(self, mode):                      
    def floggerSMTPServerURLEdit2_old(self, mode):
        print("SMTP Server URL button clicked")
        if mode: 
            smtp_server_URL = self.ui.SMTPServerURL.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_URL")
            self.ui.SMTPServerURL.setText(old_val)
            smtp_server_URL = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_URL", smtp_server_URL)
        self.FLOGGER_SMTP_SERVER_URL = smtp_server_URL       
                      
##    def floggerEmailSenderEdit2(self, mode):                      
    def floggerEmailSenderEdit2_old(self, mode):
        print("SMTP Sender Tx button clicked")
        if mode: 
            EmailSenderTX = self.ui.EmailSenderTX.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_TX")
            self.ui.EmailSenderTX.setText(old_val)
            EmailSenderTX = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_TX", EmailSenderTX)
        self.FLOGGER_SMTP_TX = EmailSenderTX        
                      
##    def floggerEmailReceiverEdit2(self, mode):                      
    def floggerEmailReceiverEdit2_old(self, mode):
        print("SMTP Receiver Rx button clicked")
        if mode: 
            EmailReceiverRX = self.ui.EmailReceiverRX.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_RX")
            self.ui.EmailReceiverRX.setText(old_val)
            EmailReceiverRX = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_RX", EmailReceiverRX)
        self.FLOGGER_SMTP_RX = EmailReceiverRX 
                             
##    def floggerSMTPServerPortEdit2(self, mode):                             
    def floggerSMTPServerPortEdit2_old(self, mode):
        print("SMTP Server Port button clicked")
        if mode :
            smtp_server_port = self.ui.SMTPServerPort.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_PORT")
            self.ui.SMTPServerPort.setText(old_val)
            smtp_server_port = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_SMTP_SERVER_PORT", smtp_server_port)
        self.FLOGGER_SMTP_SERVER_PORT = int(smtp_server_port) 
        
##    def floggerMinFlightDeltaTimeEdit2(self, mode):        
    def floggerMinFlightDeltaTimeEdit2_old(self, mode):     
        print("Minimum Flight Difference Time button clicked")
        if mode :
            MinFlightDeltaTime = self.ui.MinFlightDeltaTime.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_DUPLICATE_FLIGHT_DELTA_T")
            self.ui.MinFlightDeltaTime.setText(old_val)
            MinFlightDeltaTime = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_DUPLICATE_FLIGHT_DELTA_T", MinFlightDeltaTime)
        self.FLOGGER_DUPLICATE_FLIGHT_DELTA_T = MinFlightDeltaTime
        
##    def floggerFlightLogFolderEdit2(self, mode):        
    def floggerFlightLogFolderEdit2_old(self, mode):         
        print("Flight Log Folder button clicked")
        if mode :
            FlightLogFolder = self.ui.FlightLogFolder.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_FLIGHTS_LOG")
            self.ui.FlightLogFolder.setText(old_val)
            FlightLogFolder = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLIGHTS_LOG", FlightLogFolder)
        self.FLOGGER_FLIGHTS_LOG = FlightLogFolder

        
##    def floggerFloggerVersionNoEdit2(self, mode):         
    def floggerFloggerVersionNoEdit2_old(self, mode):         
        print("Flogger Version Nos clicked")
        if mode :
            FloggerVersionNo = self.ui.FloggerVersionNo.toPlainText() 
            print("FloggerVersionNo: ", str(FloggerVersionNo)) 
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_FLIGHTS_LOG")
            self.ui.FloggerVersionNo.setText(old_val)
            FlightLogFolder = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_VER", FloggerVersionNo)
        self.FLOGGER_VER = FloggerVersionNo       
    
                
##    def floggerLandoutMsgModeEdit2(self, mode):                
    def floggerLandoutMsgModeEdit2_old(self, mode):         
        print("Landout Msg Mode button clicked")
        if mode :
            LandoutMsgMode = self.ui.LandoutMsgMode.toPlainText()  
        else:
            old_val = self.getOldValue(self.config, "FLOGGER_LANDOUT_MODE")
            self.ui.LandoutMsgMode.setText(old_val)
            LandoutMsgMode = old_val
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_LANDOUT_MODE", LandoutMsgMode)
        self.FLOGGER_LANDOUT_MODE = LandoutMsgMode
        
    def floggerAPRSBasesListEdit_old(self):
        print("APRS Bases list clicked")
#        sel_items = listWidget.selectedItems()
        sel_items = self.ui.APRSBasesListWidget.selectedItems()
        for item in sel_items:
            new_val = item.text()
            print(new_val)
            item.editItem()
#            item.setText(item.text()+"More Text")
     
##    def floggerAPRSBaseEdit2(self, mode):       
    def floggerAPRSBaseEdit2_old(self, mode):
        print("APRS Base station list called") 
        if mode:
            APRSBaseList = []
            APRSBaseList.append(self.ui.APRSBase1Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase2Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase3Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase4Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase5Edit.toPlainText())
            APRSBaseList.append(self.ui.APRSBase6Edit.toPlainText())
            print("APRSBaseList: ", APRSBaseList)
        else: 
            old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
            self.ui.APRSBase1Edit.setText(old_val[0])
            self.ui.APRSBase2Edit.setText(old_val[1])
            self.ui.APRSBase3Edit.setText(old_val[2])
            self.ui.APRSBase4Edit.setText(old_val[3])
            self.ui.APRSBase5Edit.setText(old_val[4])
            self.ui.APRSBase6Edit.setText(old_val[5])
            APRSBaseList = old_val
        APRSBaseList = [str(APRSBaseList[0]), 
                        str(APRSBaseList[1]), 
                        str(APRSBaseList[2]), 
                        str(APRSBaseList[3]), 
                        str(APRSBaseList[4]), 
                        str(APRSBaseList[5])]
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_APRS_BASES", APRSBaseList)
        self.FLOGGER_APRS_BASES = APRSBaseList 
        print("FLOGGER_APRS_BASES: ", self.FLOGGER_APRS_BASES)

##    def floggerAdd2FleetOkButton(self):
    def floggerAdd2FleetOkButton_old(self):
        print("floggerAdd2FleetOkButton called")
        if self.ui.Add2FleetRegEdit.toPlainText() == "":
            return
        rowPosition = self.ui.FleetListTable.rowCount()          
#            print "rowPosition: ", rowPosition, " Registration: ", registration, " Code: ", settings.FLOGGER_FLEET_LIST[registration]
        self.ui.FleetListTable.insertRow(rowPosition)
#        self.FleetListTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(self.Add2FleetRegEdit))
        self.ui.FleetListTable.setItem(rowPosition , 0, QtWidgets
                                       .QTableWidgetItem(self.ui.Add2FleetRegEdit.toPlainText()))
        self.ui.FleetListTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(self.ui.Add2FleetCodeEdit.toPlainText())) 
        # Add in the new registration to the dictionary 
        old_fleet_list = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
        old_fleet_list[str(self.ui.Add2FleetRegEdit.toPlainText())] = str(self.ui.Add2FleetCodeEdit.toPlainText())
        # Output the updated FleetList to the config file
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_LIST", old_fleet_list)
        settings.FLOGGER_FLEET_LIST = old_fleet_list
        print("FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST)
        print("Type FLOGGER_FLEET_LIST: ", type(old_fleet_list))
        # Set fields on form to balnk
        self.ui.Add2FleetRegEdit.setText("")
        self.ui.Add2FleetCodeEdit.setText("") 
        
        for key in list(old_fleet_list.keys()):
            # Convert string form of value to int
            old_fleet_list[key] = int(old_fleet_list[key])
        self.flogger_fleet_list_sorted = sorted(old_fleet_list.items(), key=lambda x: x[1], reverse=False)
        print("FLOGGER_FLEET_LIST sorted: ", self.flogger_fleet_list_sorted)
        i = 0
        for item in self.flogger_fleet_list_sorted:
            print("item", i, ":", self.flogger_fleet_list_sorted[i][0], ", ", self.flogger_fleet_list_sorted[i][1])
            self.ui.FleetListTable.setItem(i , 0, QtWidgets.QTableWidgetItem(self.flogger_fleet_list_sorted[i][0]))
            self.ui.FleetListTable.setItem(i , 1, QtWidgets.QTableWidgetItem(str(self.flogger_fleet_list_sorted[i][1])))
            i = i + 1
## Output to config = file sorted Fleet List  
        new_f_l ={}
        for key in self.flogger_fleet_list_sorted:
            print("fleet_list_sorted_key: ", key[0], ",", key[1])
            new_f_l[key[0]] = key[1]
        print("new_f_l", new_f_l)
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_LIST", new_f_l)
                    
            
        
##    def floggerAdd2FleetCancelButton(self):         
    def floggerAdd2FleetCancelButton_old(self): 
        print("floggerAdd2FleetCancelButton called")
        self.ui.Add2FleetRegEdit.setText("")
        self.ui.Add2FleetCodeEdit.setText("")  
        
##    def floggerDelFromFleetOkButton(self):        
    def floggerDelFromFleetOkButton_old(self):
        print("floggerDelFromFleetOkButton")
        if self.ui.DelFromFleetEdit.toPlainText() == "":
            return
        fleet_list = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
        reg = self.ui.DelFromFleetEdit.toPlainText()
        del fleet_list[str(reg)]
#        print "fleet_list: ", fleet_list
        self.editConfigField("flogger_settings_file.txt", "FLOGGER_FLEET_LIST", fleet_list)
        settings.FLOGGER_FLEET_LIST = fleet_list
        self.ui.DelFromFleetEdit.setText("")
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_LIST")
        print("FLOGGER_FLEET_LIST now: ", self.FLOGGER_FLEET_LIST) 
        for key in list(old_val.keys()):
            # Convert string form of value to int
            old_val[key] = int(old_val[key])
#            print "Key: ", key, " = ", int(old_val[key])
        print("FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST)
        self.flogger_fleet_list_sorted = sorted(settings.FLOGGER_FLEET_LIST.items(), key=lambda x: x[1], reverse=False)
        print("FLOGGER_FLEET_LIST sorted: ", self.flogger_fleet_list_sorted)

        
        self.ui.FleetListTable.clearContents()
        self.ui.FleetListTable.setRowCount(0)
        rowPosition = self.ui.FleetListTable.rowCount()
#        rowPosition = 0
        for registration in settings.FLOGGER_FLEET_LIST:
            print("rowPosition: ", rowPosition, " Registration: ", registration, " Code: ", settings.FLOGGER_FLEET_LIST[registration])
            self.ui.FleetListTable.insertRow(rowPosition)   
            self.ui.FleetListTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(registration))
            self.ui.FleetListTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(str(settings.FLOGGER_FLEET_LIST[registration])))
            rowPosition = rowPosition + 1 # interesting rowPosition =+ 1 gives wrong result!!
    
##    def floggerOkpushButton(self):
    def floggerOkpushButton_old(self):
        print("About Ok button clicked")
        self.close()
        
##    def floggerFlightLog(self):        
    def floggerFlightLog_old(self):
        
        def setColourtoRow(table, rowIndex, colour):
            for j in range(table.columnCount()):
                table.item(rowIndex, j).setBackground(colour)
                
        print("Flight Log calendar clicked")
        date_conv = time.strptime(str(self.ui.FlightLogcalendar.selectedDate().toString()),"%a %b %d %Y")
#        print time.strftime("%d/%m/%Y",date_conv)
        date = time.strftime("%y/%m/%d",date_conv)
        print("Current date is: ",date)
        # Get flights for date
        try:
            flogger_db_path = path_join_dd(os.path.abspath(__file__), ["db", "flogger.sql3.2"])
            print("DB name(new): ", flogger_db_path)
            db = sqlite3.connect(flogger_db_path) 
            cursor = db.cursor()
        except:
            print("Failed to connect to db")
        try:
            cursor.execute("SELECT flight_no, sdate, stime, etime, duration, src_callsign, max_altitude, registration, track_file_name, tug_registration, tug_altitude, tug_model  FROM flights WHERE sdate=? ORDER BY stime DESC", (date,))
            # row[0] = flight_no, 
            # row[1] = sdate, 
            # row[2] = stime, 
            # row[3] = etime, 
            # row[4] = duration, 
            # row[5] = src_callsign, 
            # row[6] = max_altitude, 
            # row[7] = registration, 
            # row[8] = track_file_name, 
            # row[9] = tug_registration, 
            # row[10] = tug_altitude, 
            # row[11] = tug_model 
        except:
            print("Select failed")
        rows = cursor.fetchall()
        row_count = cursor.rowcount
        print("row_count: ", row_count)
        if row_count <= -1:
            row_count = 0
        header = self.ui.FlightLogTable.horizontalHeader()
##        header.setResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        col_nos = 0
        while col_nos < 9:
##            header.setResizeMode(col_nos, QtGui.QHeaderView.ResizeToContents)
##            header.setResizeMode(col_nos, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(col_nos, QtWidgets.QHeaderView.ResizeToContents)
            col_nos = col_nos + 1
        self.ui.FlightLogTable.clearContents()
        self.ui.FlightLogTable.setRowCount(0)
        rowPosition = self.ui.FlightLogTable.rowCount()
        self.ui.FlightLogTable.setColumnHidden(10, True)
#        row_count = 1
        for row in rows:  
#            print "Row: ", row_count
            in_fleet = True 
            try:
                if settings.FLOGGER_FLEET_LIST[row[7]] > 100 and \
                    settings.FLOGGER_FLEET_LIST[row[7]] <= 200 and \
                    settings.FLOGGER_INCLUDE_TUG_FLIGHTS != "Y":
                    print("Tug only flight so ignore tug: ", row[7])
                    continue
            except KeyError:
                print("Glider not in Fleet hence not a tug: ", row[7]) 
                in_fleet = False                       
            self.ui.FlightLogTable.insertRow(rowPosition)   
#            if row[9] is None: 
            val = "----"                # Default value
            if row[9] is None and row[10] is None and row[11] is None:
                # Check if it's in the fleet?
                if in_fleet:
                    # Is it a motor glider?
                    if settings.FLOGGER_FLEET_LIST[row[7]] > 200 and \
                        settings.FLOGGER_FLEET_LIST[row[7]] <= 300:
                        # It is so blanks
                        val = "----"
                    else:
                        # Must be a winch launch of glider, ie non-motor glider or non-fleet glider, but may be self launcher??
                        val = "Winch"
            else:
                val = row[9]
            self.ui.FlightLogTable.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(val))           # Tug Reg
            if row[11] is None:
                val = "----"
            else:
                val = row[11]
##
## 20220520 PyQT5 has no attribute QTGui.QTableWidgetItem - replace QtGui with QtWidgets
##
            self.ui.FlightLogTable.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(val))           # Tug Type
            self.ui.FlightLogTable.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(row[7]))        # (Moto) Glider     
            self.ui.FlightLogTable.setItem(rowPosition , 3, QtWidgets.QTableWidgetItem(row[7][3:]))    # CN
            cursor.execute("SELECT aircraft_model FROM flarm_db WHERE registration = ?", (row[7],))
            plane_type = cursor.fetchone()
            if plane_type[0] == None:
                print("Aircraft_model not found, try Type for Registration : ", row[7])
                cursor.execute("SELECT type FROM flarm_db WHERE registration = ?", (row[7],))   
                plane_type = cursor.fetchone()
            print("Plane Type/model is: ", plane_type[0])
            self.ui.FlightLogTable.setItem(rowPosition , 4, QtWidgets.QTableWidgetItem(plane_type[0])) # Plane Type/Model 
            self.ui.FlightLogTable.setItem(rowPosition , 5, QtWidgets.QTableWidgetItem(row[2]))        # Glider Takeoff TIme
            self.ui.FlightLogTable.setItem(rowPosition , 6, QtWidgets.QTableWidgetItem(row[3]))        # Glider Landing Time
            self.ui.FlightLogTable.setItem(rowPosition , 7, QtWidgets.QTableWidgetItem(row[4]))        # Glider Flight Time
            if row[10] is None:
                val = "----"
            else:
                val = row[10]
            self.ui.FlightLogTable.setItem(rowPosition , 8, QtWidgets.QTableWidgetItem(val))            # Tug Max ALt (QFE)
            self.ui.FlightLogTable.setItem(rowPosition , 9, QtWidgets.QTableWidgetItem(row[6]))
            self.ui.FlightLogTable.setItem(rowPosition , 10, QtWidgets.QTableWidgetItem(row[8]))

            if row_count % 2 == 0:
                colour = QtGui.QColor(204,255,204)      # Light green 
            else:
                colour = QtGui.QColor(128,255,128)      # Darker green
            setColourtoRow(self.ui.FlightLogTable, rowPosition, colour)     
            row_count = row_count + 1


##
## 20220530 - floggerFlightLogDoubleClicked Track display section modified to replace mplleaflet with follium.
##              mplleaflet had unresolvable problem (well I couldn't resolve it!), see: https://github.com/mpld3/mpld3/issues/479
##              Just a couple of lines changed, but suggests new config paramters, eg which browser.
##
    def floggerFlightLogDoubleClicked(self):
        print("Double Clicked called")
        self.change_status("Building Track Map...", "orange")
        self.ui.FlightLogTable.setColumnHidden(10, False)
        index = self.ui.FlightLogTable.selectedIndexes()
        
        try:
            # check if base_map.html temp file exists and if so delete it
            outfp_test = open("base_map.html")
            os.remove("base_map.html")
        except :
            pass

        print('selected item index found at %s with data: %s' % (index[10].row(), index[10].data()))
        track_file = index[10].data()
        self.ui.FlightLogTable.setColumnHidden(10, True)    
        gpx_file = open(track_file, 'r')
        gpx = gpxpy.parse(gpx_file)
        points = []       
        lat = []
        lon = []   
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    lon.append(point.longitude)
##                  print('point is: ', point)
                    points.append(tuple([point.latitude, point.longitude]))
        latitude = sum(p[0] for p in points)/len(points)
        longitude = sum(p[1] for p in points)/len(points)
        myMap = folium.Map(location=[latitude,longitude],zoom_start=12)
##        myMap = folium.Map(location=[latitude,longitude],zoom_start=zoom)
        folium.PolyLine(points, color="red", weight=1.5, opacity=1).add_to(myMap)
        outfp = "base_map.html"
        myMap.save(outfp)
        subprocess.run(["firefox", outfp])
        self.change_status("Waiting for sunrise...", "yellow")
        
        
        
        

class AboutWindow(QDialog):
    def __init__(self):
        print("AboutWindow Initialise")
        super().__init__()
        self.ui = flogger_About.Ui_Form()
        self.ui.setupUi(self)
    
    def floggerAboutButton(self):
        print("About Ok button clicked")
        self.show()

     
        

class flogger_splash(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        path = os.path.dirname(os.path.abspath(__file__))
        icon_path = path_join_dd(os.path.abspath(__file__), ["data", "flogger_icon-08.png"])
        print("Icon path: ", icon_path, " Path: ", path)
        movie = QMovie(path_join_dd(os.path.abspath(__file__),["data", "ogn-logo-ani.gif"]))
        splash = MovieSplashScreen(movie)
        splash.show()
        start = time.time()
        i = 0    
        while movie.state() == QMovie.Running and time.time() < start + 5:
            app.processEvents()
            
        
    
##def main():     
def mainX(): 
    print("start main") 
##    app = QtGui.QApplication(sys.argv)
    app = QApplication(sys.argv)
    print ("loadUiType parm: ", path_join_dd(os.path.abspath(__file__), ["data", "flogger-v1.2.3.ui"]))
    Ui_MainWindow, base_class = uic.loadUi(path_join_dd(os.path.abspath(__file__), ["data", "flogger-v1.2.3.ui"]))

    Ui_AboutWindow, base_class = uic.loadUi(path_join_dd(os.path.abspath(__file__), ["data", "flogger_about.ui"]))

##    path = os.path.dirname(os.path.abspath(__file__))
##    icon_path = path_join_dd(os.path.abspath(__file__), ["data", "flogger_icon-08.png"])
##    print("Icon path: ", icon_path, " Path: ", path)
    #app.setWindowIcon(QtGui.QIcon(icon_path))
	# Create and display the splash screen
#    splash_pix = QPixmap(os.path.join(path,"../data/flogger_icon-03.png"))
#    splash_pix = QPixmap(path_join_dd(os.path.abspath(__file__),["data", "flogger_icon-03.png"]))
#    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)

#    movie = QMovie(os.path.join(path,"../data/ogn-logo-ani.gif"))
##    movie = QMovie(path_join_dd(os.path.abspath(__file__),["data", "ogn-logo-ani.gif"]))

##    splash = MovieSplashScreen(movie)
##    splash.show()
    
##    start = time.time()
    
##    i = 0    
##    while movie.state() == QMovie.Running and time.time() < start + 5:
##        app.processEvents()
    # 
    # This section takes time to run building the ui and resources files from flogger.ui 
    #
    
#    try:
#        print "Build UI resource files start"
#        pyrcc4_cmd = "pyrcc4 -o "
#        pyrcc4_out = os.path.join(path,"flogger_resources_rc.py")
#        pyrcc4_in = os.path.join(path,"../data/flogger_resources.qrc")
#        pyrcc4_cmd = "pyrcc4 -o %s %s" % (pyrcc4_out, pyrcc4_in)
#        os.system(pyrcc4_cmd)
#        print "Build UI resource files end"
#        time.sleep(5)
#    except:
#        print "failed to compile resources"
#        exit()
        
    #app1 = QApplication.instance()  
    #trayIcon = QSystemTrayIcon(QtGui.QIcon(icon_path), app) 
    #trayIcon.show()
    
        
    print("Call MyApp")
    window = MyApp()
    
    # Adding an icon
    icon = QIcon(icon_path)
  
    # Adding item on the menu bar
    tray = QSystemTrayIcon()
##    tray.setIcon(icon)
    tray.setVisible(True)
    
##    window.setWindowIcon(QtGui.QIcon(icon_path))
    print("Call window.show()")
###    window.show()
    
##    tray = QtGui.QSystemTrayIcon()
    #icon = QtGui.QIcon(icon_path)
##    tray.setIcon(QtGui.QIcon(icon_path)) 
##    tray.setToolTip("OGN FloggerX")
##    tray.setIcon(icon)
##    tray.setVisible(True)
##    tray.show()
    
##    icon = QSystemTrayIcon(QIcon(icon), parent=app)
##    icon.show()
    
    splash.finish(window)
    
    print("Splash screen end")
    print("cwd is: ", os.path.dirname(os.getcwd()))
    print("path to script is: ", os.path.dirname(os.path.abspath( __file__ )))
    
##    icon = QSystemTrayIcon(QIcon(QIcon(icon)), parent=app)
##    icon.show()
    
    w = QtGui.QWidget()
    trayIcon = SystemTrayIcon(icon, w)

    trayIcon.show()
    sys.exit(app.exec_())



    
##class HelpWindow(QtGui.QMainWindow, Ui_HelpWindow):    
class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setupUi(self)
        # Only one button - Ok
        self.HelppushButton.clicked.connect(self.floggerHelppushButton)
        return
    
    def floggerHelppushButton(self):
        print("Help Ok button clicked")
        self.close()
        return
    

#global settings_file_dot_txt

##class MyApp(flogger):
class MyAppX(flogger):
    def __init__(self):
        print("init MyApp New")
##        QtGui.QMainWindow.__init__(self)
##        QtGui.QMainWindow.__init__(self)
##        QtWidgets.QMainWindow.__init__(self)
##        Ui_MainWindow.__init__(self)
        super(MyApp, self).__init__()
        self.ui = self.Ui_MainWindow
        self.ui.setupUi(self)
        # checkbox scroll area, gives scrollable view on widget
        scroll = QtGui.QScrollArea()
        scroll.setMinimumWidth(120)
        scroll.setMinimumHeight(200) # would be better if resizable
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  
        self.show()
        self.setupUi(self)
        global settings
        global db
        global cursor
        settings = class_settings()
        db       = class_settings()
        cursor   = class_settings()
        
        self.actionAbout.triggered.connect(self.AboutButton)
        self.actionHelp_2.triggered.connect(self.HelpButton)   
        self.actionStart.triggered.connect(self.floggerStart)  
        self.actionStop.triggered.connect(self.floggerStop)
        self.actionFlying_End.triggered.connect(self.floggerFlying_End)  
        self.actionQuit.triggered.connect(self.floggerQuit)  
        self.actionEdit.triggered.connect(self.floggerEdit) 
        self.FleetCheckRadioButton.toggled.connect(self.floggerFleetCheckRadioButton) 
        self.RecordTracksRadioButton.toggled.connect(self.floggerRecordTracksRadioButton)  
        self.TakeoffEmailButton.toggled.connect(self.floggerTakeoffEmailButton)  
        self.LandingEmailButton.toggled.connect(self.floggerLandingEmailButton)  
        self.LaunchFailuresButton.toggled.connect(self.floggerLaunchFailuresButton)
        self.LogTugsButton.toggled.connect(self.floggerLogTugsButton)
        self.IGCFormatButton.toggled.connect(self.floggerIGCFormatButton)  
        self.LiveTestButton.toggled.connect(self.floggerLiveTestButton)
        
        
        self.UpdateButton.clicked.connect(self.floggerUpdateConfig)
        self.CancelButton.clicked.connect(self.floggerCancelConfigUpdate)
        
        #self.TPOkButton.clicked.connect(self.floggerTPOkButton)            # Use with gui 1.2.2
        #self.TPCancelButton.clicked.connect(self.floggerTPCancelButton)
        
        self.Add2FleetOkButton.clicked.connect(self.floggerAdd2FleetOkButton)
        self.Add2FleetCancelButton.clicked.connect(self.floggerAdd2FleetCancelButton)
        
        self.DelFromFleetOkButton.clicked.connect(self.floggerDelFromFleetOkButton)
        self.RunningLabel.setStyleSheet("color: red")  
        
        self.FlightLogcalendar.clicked.connect(self.floggerFlightLog)
        self.IncludeTugsButton.toggled.connect(self.floggerIncludeTugsButton)
        self.ui.FlightLogTable.doubleClicked.connect(self.floggerFlightLogDoubleClicked)
        self.ui.FlightLogTable.verticalHeader().sectionClicked.connect(self.floggerFlightLogDoubleClicked)  
        self.ui.FlightLogTable.setColumnHidden(10, True)
        # Initialise values from config file

        filepath = os.path.join(path, "flogger_settings_file.txt")
        try:
            settings_file_dot_txt = path_join_dd(os.path.abspath(__file__), ["data", "flogger_settings_file.txt"])
            self.config = ConfigObj(settings_file_dot_txt, raise_errors = True)
            print("Opened flogger_settings_file.txt path:", settings_file_dot_txt)
        except:
            print("Open failed")
            print(self.config)
            
#
# This section reads all the values from the config file and outputs these in the gui fields.
# It also initialises the corresponding settings object config fields. If the values are changed
# in the gui they must be saved in the config file and used as the current values in the settings object
#          
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_NAME")
        settings.FLOGGER_AIRFIELD_NAME = old_val
#        print settings.FLOGGER_AIRFIELD_NAME
        self.AirfieldBase.setText(old_val)
         
        old_val = self.getOldValue(self.config, "APRS_USER")
        settings.APRS_USER = old_val
        self.APRSUser.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_PASSCODE")    # This might get parsed as an int - need to watch it!
        settings.APRS_PASSCODE = old_val
        self.APRSPasscode.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_HOST")    
        settings.APRS_SERVER_HOST = old_val
        self.APRSServerHostName.setText(old_val)
        
        old_val = self.getOldValue(self.config, "APRS_SERVER_PORT")    # This might get parsed as an int - need to watch it!
        settings.APRS_SERVER_PORT = int(old_val)
        self.APRSServerPort.setText(old_val)
         
        old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME")
        print("FLOGGER_KEEPALIVE_TIME from settings.txt is ", old_val)
        self.FLOGGERKeep_alive_time = old_val
        self.APRSKeepAliveTIme.setText(old_val)
#        settings.APRS_USER = old_val
#        self.APRSUser.setText(old_val)

        old_val = self.getOldValue(self.config, "FLOGGER_VER")      # Flogger Version Number
        print("FLOGGER_VER from settings.txt is ", old_val)
        self.FLOGGER_VER = old_val
        self.FloggerVersionNo.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_RAD")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_RAD = int(old_val)
        self.AirfieldFlarmRadius.setText(old_val)
         
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_LIMIT")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_AIRFIELD_LIMIT = int(old_val)
        self.LandOutRadius.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_AIRFIELD_DETAILS")    
        settings.FLOGGER_AIRFIELD_DETAILS = old_val
        self.AirfieldDetails.setText(old_val)
          
        old_val = self.getOldValue(self.config, "FLOGGER_QFE_MIN")    
        settings.FLOGGER_QFE_MIN = int(old_val)
        self.MinFlightQFE.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MIN_FLIGHT_TIME")    
        settings.FLOGGER_MIN_FLIGHT_TIME = old_val
        self.MinFlightTime.setText(old_val)
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_V_TAKEOFF_MIN")    
        settings.FLOGGER_V_TAKEOFF_MIN = old_val
        self.MinFlightTakeoffVelocity.setText(old_val)
            
        old_val = self.getOldValue(self.config, "FLOGGER_V_LANDING_MIN")    
        settings.FLOGGER_V_LANDING_MIN = old_val
        self.MinFlightLandingVelocity.setText(old_val) 
                   
        old_val = self.getOldValue(self.config, "FLOGGER_DT_TUG_LAUNCH")    
        settings.FLOGGER_DT_TUG_LAUNCH = old_val
        self.MinTugLaunchTIme.setText(old_val)
#
# Note this could be done using LatLon
#        
        old_val_lat = self.getOldValue(self.config, "FLOGGER_LATITUDE")    # This might get parsed as a real - need to watch it!
        print("Old_val: " + old_val_lat)
        settings.FLOGGER_LATITUDE = old_val_lat
        
        old_val_lon = self.getOldValue(self.config, "FLOGGER_LONGITUDE")    # This might get parsed as a real - need to watch it!
        print("Old_lon: " + old_val_lon)
        settings.FLOGGER_LONGITUDE = old_val_lon
#        self.AirfieldLongitude.setText(old_val_lon)
        print("start LatLon")
        old_latlon = LatLon(Latitude( old_val_lat), Longitude(old_val_lon))
        old_latlonstr = old_latlon.to_string('D% %H')
        self.AirfieldLatitude.setText(old_latlonstr[0])
        self.AirfieldLongitude.setText(old_latlonstr[1])
        print("End LatLon", old_latlonstr)
               
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_CHECK")
        print("Fleet Check: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.FleetCheckRadioButton.setChecked(True)
        else:
            print("N")   
            self.FleetCheckRadioButton.setChecked(False)
        settings.FLOGGER_FLEET_CHECK = old_val
                          
        old_val = self.getOldValue(self.config, "FLOGGER_LOG_TUGS")
        print("Log Tugs Button: ", old_val) 
        if old_val == "Y":
            print("Y")
            self.LogTugsButton.setChecked(True)
        else:
            print("N")   
            self.LogTugsButton.setChecked(False)
##        settings.FLOGGER_FLEET_CHECK = old_val
        settings.FLOGGER_LOG_TUGS = old_val
        
        old_val = self.getOldValue(self.config, "FLOGGER_TRACKS")
        print("Record Tracks: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.RecordTracksRadioButton.setChecked(True)
        else:
            print("N")   
        settings.FLOGGER_TRACKS = old_val 
                     
        old_val = self.getOldValue(self.config, "FLOGGER_TAKEOFF_EMAIL")
        print("Email takeoffs is: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.TakeoffEmailButton.setChecked(True)
        else:
            print("N")   
        settings.FLOGGER_TAKEOFF_EMAIL = old_val 
        
                             
        old_val = self.getOldValue(self.config, "FLOGGER_LANDING_EMAIL")
        print("Email landings is: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.LandingEmailButton.setChecked(True)
        else:
            print("N")   
        settings.FLOGGER_LANDING_EMAIL = old_val 
        
        old_val = self.getOldValue(self.config, "FLOGGER_DB_SCHEMA")    
        settings.FLOGGER_DB_SCHEMA = old_val
        self.DBSchemaFile.setText(old_val)
        settings.FLOGGER_DB_SCHEMA = old_val
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_DB_NAME")    
        settings.FLOGGER_DB_NAME = old_val
        self.DBName.setText(old_val)
        settings.FLOGGER_DB_NAME = old_val    
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLARMNET_DB_URL")    
        settings.FLOGGER_FLARMNET_DB_URL = old_val
        self.FlarmnetURL.setText(old_val)
#        settings.FLOGGER_FLARMNET_DB_URL = old_val
       
        old_val = self.getOldValue(self.config, "FLOGGER_OGN_DB_URL")    
        settings.FLOGGER_OGN_DB_URL = old_val
        self.OGNURL.setText(old_val)
#       settings.FLOGGER_OGN_DB_URL = old_val
                
        old_val = self.getOldValue(self.config, "FLOGGER_KEEPALIVE_TIME")    
        settings.FLOGGER_KEEPALIVE_TIME = int(old_val)
        self.FLOGGERKeepAliveTime = old_val

        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_URL")  
        print("Initialise FLOGGER_SMTP_SERVER_URL")  
        settings.FLOGGER_SMTP_SERVER_URL = old_val
        self.SMTPServerURL.setText(old_val)
        settings.FLOGGER_SMTP_SERVER_URL = old_val
        print("settings.FLOGGER_SMTP_SERVER_URL: ", settings.FLOGGER_SMTP_SERVER_URL)
        
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_SERVER_PORT")    
        settings.FLOGGER_SMTP_SERVER_PORT = int(old_val)
        self.SMTPServerPort.setText(old_val)
        settings.FLOGGER_SMTP_SERVER_PORT = int(old_val)
        
                
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_TX") 
        print("TX from file: ", old_val)   
        settings.FLOGGER_SMTP_TX = old_val
        self.EmailSenderTX.setText(old_val)
        settings.FLOGGER_SMTP_TX = old_val     
                
        old_val = self.getOldValue(self.config, "FLOGGER_SMTP_RX")    
        settings.FLOGGER_SMTP_RX = old_val
        self.EmailReceiverRX.setText(old_val)
        settings.FLOGGER_SMTP_RX = old_val
                
        old_val = self.getOldValue(self.config, "FLOGGER_APRS_BASES")
        i = 1
        for item in old_val:
#            print "APRS Base: " + item
            if i == 1:
                self.APRSBase1Edit.setText(item)
                i += 1
                continue
            if i == 2:
                self.APRSBase2Edit.setText(item)
                i += 1
                continue
            if i == 3:
                self.APRSBase3Edit.setText(item)
                i += 1
                continue
            if i == 4:
                self.APRSBase4Edit.setText(item)
                i += 1
                continue 
            if i == 5:
                self.APRSBase5Edit.setText(item)
                i += 1
                continue 
            if i == 6:
                self.APRSBase6Edit.setText(item)
                i += 1
                continue 
        settings.FLOGGER_APRS_BASES = old_val
#        print "APRS_BASES: ", old_val
        print("APRS_BASES: ", settings.FLOGGER_APRS_BASES)
        
        old_val = self.getOldValue(self.config, "FLOGGER_FLEET_LIST") 
 #       print "FLOGGER_FLEET_LIST: ", old_val 
        for key in list(old_val.keys()):
            # Convert string form of value to int
            old_val[key] = int(old_val[key])
#            print "Key: ", key, " = ", int(old_val[key])
        settings.FLOGGER_FLEET_LIST = old_val
        print("FLOGGER_FLEET_LIST: ", settings.FLOGGER_FLEET_LIST)
        
        rowPosition = self.FleetListTable.rowCount()
        for registration in settings.FLOGGER_FLEET_LIST:
            print("rowPosition: ", rowPosition, " Registration: ", registration, " Code: ", settings.FLOGGER_FLEET_LIST[registration])
            self.FleetListTable.insertRow(rowPosition)
            self.FleetListTable.setItem(rowPosition , 0, QtGui.QTableWidgetItem(registration))
            self.FleetListTable.setItem(rowPosition , 1, QtGui.QTableWidgetItem(str(settings.FLOGGER_FLEET_LIST[registration])))
            rowPosition = rowPosition + 1
        
        
        old_val = self.getOldValue(self.config, "FLOGGER_DATA_RETENTION")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_DATA_RETENTION = int(old_val)
        self.DataRetentionTime.setText(old_val)
          
        old_val = self.getOldValue(self.config, "FLOGGER_LOG_TIME_DELTA")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_LOG_TIME_DELTA = int(old_val)
        self.LogTimeDelta.setText(old_val) 
                 
        old_val = self.getOldValue(self.config, "FLOGGER_LOCATION_HORIZON")    # This might get parsed as an int - need to watch it!
        settings.FLOGGER_LOCATION_HORIZON = old_val
        self.HorizonAdjustment.setText(old_val)   
                      
        old_val = self.getOldValue(self.config, "FLOGGER_DUPLICATE_FLIGHT_DELTA_T")    
        settings.FLOGGER_DUPLICATE_FLIGHT_DELTA_T = old_val
        self.MinFlightDeltaTime.setText(old_val)
                             
        old_val = self.getOldValue(self.config, "FLOGGER_QNH")    
#        settings.FLOGGER_QNH = int(old_val)
        #
        # 20210210 Start
        #  
        if settings.FLOGGER_QNH == 0:
            print("Lookup new QNH")
            settings.FLOGGER_QNH = ""
        else:
            if settings.FLOGGER_QNH != old_val:
                print("Old QNH: ", old_val, " New QNH: ", settings.FLOGGER_QNH)
                old_val = settings.FLOGGER_QNH
        # 
        # 20210210 End
        #    
        settings.FLOGGER_QNH = old_val
        self.AirfieldQNH.setText(old_val)     
                                     
        old_val = self.getOldValue(self.config, "FLOGGER_FLIGHTS_LOG")    
        settings.FLOGGER_FLIGHTS_LOG = old_val
        self.FlightLogFolder.setText(old_val)  
                                           
        old_val = self.getOldValue(self.config, "FLOGGER_LANDOUT_MODE")    
        settings.FLOGGER_LANDOUT_MODE = old_val
        self.LandoutMsgMode.setText(old_val)
        
        old_val = self.getOldValue(self.config, "FLOGGER_MODE")
        if old_val == "test":
            print("Live/Test mode state is Test")
            self.LiveTestButton.setChecked(True)
                                                       
        old_val = self.getOldValue(self.config, "FLOGGER_INCLUDE_TUG_FLIGHTS")  
        print("Include Tugs Button: " + old_val) 
        if old_val == "Y":
            print("Y")
            self.IncludeTugsButton.setChecked(True)
        else:
            print("N")  
            self.IncludeTugsButton.setChecked(False)
##        settings.FLOGGER_FLEET_CHECK = old_val 
        settings.FLOGGER_INCLUDE_TUG_FLIGHTS = old_val
            
            

#
# GUI Initialisation end
#  




##class Form(QDialog):
class Form():
    """ Just a simple dialog with a couple of widgets
    """
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.browser = QTextBrowser()
        self.setWindowTitle('Just a dialog')
        self.lineedit = QLineEdit("Write something and press Enter")
        self.lineedit.selectAll()
        layout = QVBoxLayout()
        layout.addWidget(self.browser)
        layout.addWidget(self.lineedit)
        self.setLayout(layout)
        self.lineedit.setFocus()
        self.connect(self.lineedit, SIGNAL("returnPressed()"), self.update_ui)

    def update_ui(self):
        self.browser.append(self.lineedit.text())

#
# Start of Flogger execution
#
if __name__ == "__main__":
    print ("Start UI")
##    main()
    app = QApplication(sys.argv)
    splash = flogger_splash()
    splash.show
    about = AboutWindow()
    window = flogger(about)
    window.show()
    sys.exit(app.exec())
    ##sys.exit(app.run(use_reloader=False))
    
    ##sys.exit(app.exec(debug=False, use_reloader=False))

    
