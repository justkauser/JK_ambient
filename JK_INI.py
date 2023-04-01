#import libaries
import ac
import acsys
import sys
import os
import platform
import configparser
import glob
import functools
import random
import threading
import time

# Set library path
if platform.architecture()[0] == "64bit":
	libdir = 'third_party/lib64'
else:
	libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

libdir = 'module'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))

import JK_GUI
import JK_Ambient
import JK_Master
import JK_Debug
import JK_SF

config_track = None
config_car = None
config_ambient = None

def loading():
	load_ambient_config()
	load_track_config()
	load_car_config()


def load_track_config():
	global config_track
	Foldername = "config/track_config/"
	Trackname = ac.getTrackName(0)
	ini = ".ini"
		
	Config_Name = Foldername+Trackname+ini
	

	config_filename=os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), Config_Name)
	config_track = configparser.ConfigParser()
	config_track.read(config_filename)
	JK_Debug.log(" finished")
	
def load_car_config():
	global config_car
	Foldername = "config/car_config/"
	Carname = ac.getCarName(0)
	ini = ".ini"
	Config_Name = Foldername+Carname+ini
	config_filename=os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), Config_Name)
	config_car = configparser.ConfigParser()
	config_car.read(config_filename)
	JK_Debug.log(" finished")	

def load_ambient_config():
	global config_ambient
	Foldername = "config/ambient_config/"
	ini = "ambient_preset.ini"
	Config_Name = Foldername+ini
	config_filename=os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), Config_Name)
	config_ambient = configparser.ConfigParser()
	config_ambient.read(config_filename)
	JK_Debug.log(" finished XD")
	ambient_name = 'Nature'
	

def saving():
	i = 0
	
	
	
def save_ambient():
	global config_ambient
	Foldername = "config/ambient_config/"
	ini = "ambient_preset.ini"
		
	Config_Name = Foldername+ini
	

	config_filename=os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), Config_Name)
	#config_ambient = configparser.ConfigParser()
	ambient_name = ac.getText(JK_Ambient.ambient_preset_UI['Ambient_name'])
	if config_ambient.has_section(ambient_name) == False:
		config_ambient.add_section(ambient_name)
	i = 0
	while i < 8:
		config_ambient.set(ambient_name, "Ambient"+str(i) , JK_SF.names[int(ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_number'+str(i)])-1.0)])
		i += 1
		
	i = 0
	while i < 8:
		config_ambient.set(ambient_name, "Ambient_vol"+str(i), str(ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_vol'+str(i)])))
		i += 1
	
	with open(config_filename, 'w') as configfile:
		config_ambient.write(configfile)
		
	JK_Debug.log(": Ambient Preset saved")
	
def save_car_ini():	
	i = 0
	global config_car
	Trackname = ac.getTrackName(0)
	if config_car.has_section(Trackname) == False:
		config_car.add_section(Trackname)
	config_car.set(Trackname, "Int_Vol" , str(ac.getValue(JK_Master.Master_GUI['int_vol'])))
	config_car.set(Trackname, "Ext_Vol" , str(ac.getValue(JK_Master.Master_GUI['ext_vol'])))
	
	Foldername = "config/car_config/"
	Carname = ac.getCarName(0)
	ini = ".ini"
	Config_Name = Foldername+Carname+ini
	config_filename=os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), Config_Name)
	
	with open(config_filename, 'w') as configfile:
		config_car.write(configfile)

def save_track_ini():	
	i = 0
	global config_track
	
	if config_track.has_section("Ambient") == False:
		config_track.add_section("Ambient")
	config_track.set("Ambient", "Preset" , ac.getText(JK_Master.Master_GUI['Ambient_name']))
	
	
	Foldername = "config/track_config/"
	Trackname = ac.getTrackName(0)
	ini = ".ini"		
	Config_Name = Foldername+Trackname+ini
	config_filename=os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), Config_Name)
	
	with open(config_filename, 'w') as configfile:
		config_track.write(configfile)

def quit():
	save_track_ini()
	save_car_ini()