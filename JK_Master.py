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
import JK_SF
import JK_Debug
import JK_INI
import JK_Ambient

W_x = 300
W_y = 60

Sections = []
update_vol=0
Master_GUI = {}
int_mult=1



	
	
	
	
def hideGUI():
	Master_GUI
	for v in Master_GUI.values():
		ac.setVisible(v, 0)
			
	
	
def hide_unhide_GUI(name,val):
	Master_GUI	
	get_key = Master_GUI.keys()
	
	keys_needed = []
	
	if val > 1:
		val == 1
		
	for wert in get_key:
		if wert.find(name) > -1:
			ac.setVisible(Master_GUI[wert], val)	

def unhideGUI():
	global W_x,W_y,Master_GUI,is_playing,first_frame
	ac.setSize(JK_GUI.GUI_window, W_x, W_y)
	for v in Master_GUI.values():
		ac.setVisible(v, 1)
		

	



	
def update(deltaT):	
	global update_ambient_name, first_frame, Master_GUI
	
	if update_ambient_name ==1 or first_frame==1:
		i = 0
		while i < 8:
			ac.setText(Master_GUI['ambient_sound_number_label'+str(i)],JK_SF.names[int(ac.getValue(Master_GUI['ambient_sound_number'+str(i)])-1.0)])
			i += 1
		update_ambient_name = 0
		first_frame = 0
	
	
	
def Reset(*args):
	update_Section()

def Stop(*args):	
	JK_SF.stop_sound()

def update_Section():
	global Master_GUI
	Set_Sect = ac.getValue(Master_GUI['ambient_preset']) 
	Sections = JK_INI.config_ambient.sections()
	ac.setRange(Master_GUI['ambient_preset'], 1, len(Sections))
	ac.setValue(Master_GUI['ambient_preset'],Set_Sect) 
	
def ChangePreset(*args):
	global Master_GUI
	Sections = JK_INI.config_ambient.sections()
	ac.setText(Master_GUI['Ambient_name'],str(Sections[int(ac.getValue(Master_GUI['ambient_preset'])-1)]))
	JK_Ambient.update_preset()
	JK_SF.update_sounds()
		
	
def ChangeVol(*args):
	global update_vol
	update_vol=1

def ChangeVol_int(*args):
	global int_mult, Master_GUI

	int_mult = ac.getValue(Master_GUI['int_vol']) / ac.getValue(Master_GUI['ext_vol'])
	
def Create_Master_GUI():
	global Master_GUI, W_y, textInput, Sections, int_mult
	# Name the Ambient
	
	
	Master_GUI['mode_name'] = ac.addLabel(JK_GUI.GUI_window , "Master")
	ac.setPosition(Master_GUI['mode_name'], 130,47)	
			
	y = 140
	
	Sections = JK_INI.config_ambient.sections()
	
	
	Master_GUI['ambient_preset'] = ac.addSpinner(JK_GUI.GUI_window , "Ambient Preset" )
	preset = 1
	if JK_INI.config_track.has_section("Ambient") == True:
		i = 0
		preset_name = JK_INI.config_track.get("Ambient","Preset")
		while i < len(Sections):
			if Sections[i] == preset_name:
				preset = i
				i = len(Sections)
			i += 1
	
	ac.setPosition(Master_GUI['ambient_preset'], 50, y)
	ac.setSize(Master_GUI['ambient_preset'], 150, 25)
	ac.setRange(Master_GUI['ambient_preset'], 1, len(Sections))
	
	ac.setValue(Master_GUI['ambient_preset'],preset) 		
	ac.addOnValueChangeListener(Master_GUI['ambient_preset'], ChangePreset)
	
	y += 60
	
	Master_GUI['Ambient_name'] = ac.addLabel(JK_GUI.GUI_window , str(Sections[0]))
	ac.setPosition(Master_GUI['Ambient_name'], 80, y-10)
	
	y += 60
	
	intvol = 4.0
	extvol = 10.0
	
	if JK_INI.config_car.has_section(ac.getTrackName(0)) == True:
		intvol = JK_INI.config_car.getfloat(ac.getTrackName(0), "Int_Vol") 
		extvol = JK_INI.config_car.getfloat(ac.getTrackName(0), "Int_Vol")
	elif JK_INI.config_car.has_section(ac.getTrackName(0)) == False:
		tracks = []
		tracks = JK_INI.config_car.sections()
		
		if len(tracks)>0:
			intvol = 0.0
			extvol = 0.0
			i = 0
			while i<len(tracks):
				intvol += JK_INI.config_car.getfloat(tracks[i], "Int_Vol")/len(tracks)
				extvol += JK_INI.config_car.getfloat(tracks[i], "Ext_Vol")/len(tracks)
				i += 1
			intvol += 0.5
			extvol += 0.5 
	
	
	Master_GUI['int_vol'] = ac.addSpinner(JK_GUI.GUI_window , "Internal Volume " )
	ac.setPosition(Master_GUI['int_vol'], 50, y)
	ac.setSize(Master_GUI['int_vol'], 150, 25)
	ac.setRange(Master_GUI['int_vol'], 0, 100)
	ac.setValue(Master_GUI['int_vol'], intvol)
	ac.addOnValueChangeListener(Master_GUI['int_vol'], ChangeVol_int)
	
	y += 60
	
	
	

		
	Master_GUI['ext_vol'] = ac.addSpinner(JK_GUI.GUI_window , "External Volume " )
	ac.setPosition(Master_GUI['ext_vol'], 50, y)
	ac.setSize(Master_GUI['ext_vol'], 150, 25)
	ac.setRange(Master_GUI['ext_vol'], 0, 100)
	ac.setValue(Master_GUI['ext_vol'], extvol)
	ac.addOnValueChangeListener(Master_GUI['ext_vol'], ChangeVol)
	
	int_mult = intvol/ extvol
	
	y += 60
	
	
	
	W_y = y + 40
	
	Master_GUI['reset'] = ac.addButton(JK_GUI.GUI_window , "Reset")
	ac.setPosition(Master_GUI['reset'], 15, y)
	ac.setSize(Master_GUI['reset'], 100, 25)
	ac.addOnClickedListener(Master_GUI['reset'], Reset)
	
	Master_GUI['stop'] = ac.addButton(JK_GUI.GUI_window , "Stop")
	ac.setPosition(Master_GUI['stop'], 175, y)
	ac.setSize(Master_GUI['stop'], 100, 25)
	ac.addOnClickedListener(Master_GUI['stop'], Stop)
	
	JK_SF.init_sounds()
		
	JK_Debug.log(" finished")