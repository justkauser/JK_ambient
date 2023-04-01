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
import JK_Master

W_x = 600
W_y = 60

ambient_preset_UI = {}
textInput = ""
update_ambient_name=0
is_playing = 0
first_frame = 0
update_vol=0

def onRename(*args):
	global ambient_preset_UI
	ac.setVisible(ambient_preset_UI['textInput'], 1)
	ac.setVisible(ambient_preset_UI['Ambient_name'], 0)
	ac.setVisible(ambient_preset_UI['Rename_Ambient'], 0)


def onTextinput(string):
	global ambient_preset_UI, textInput
	text = ac.getText(ambient_preset_UI['textInput'])
	ac.setText(ambient_preset_UI['textInput'],text)
	ac.setVisible(ambient_preset_UI['textInput'], 0)
	ac.setVisible(ambient_preset_UI['Ambient_name'], 1)
	ac.setVisible(ambient_preset_UI['Rename_Ambient'], 1)
	textInput = text
	ac.setText(ambient_preset_UI['Ambient_name'],textInput)
	JK_SF.searchSFnames(text,4)

def onAmbientsound(value):
	global update_ambient_name
	update_ambient_name = 1

def onAmbientsound2(value):
	global ambient_sound_number
	ambient_sound_number[1] = value - 1
	

def onUpdatebuttonClick(*args):
	JK_SF.update_sounds()
	
	
def onSavebuttonClick(*args):
	JK_INI.save_ambient()
	JK_Master.update_Section()
	
def update_preset():
	global ambient_preset_UI
	
	ambient_name = ac.getText(JK_Master.Master_GUI['Ambient_name'])
	ac.setText(ambient_preset_UI['Ambient_name'],ambient_name)
	preset = []
	i = 0
	while i < 8:
		
		preset.append(JK_INI.config_ambient.get(ambient_name,"ambient"+str(i)))
		i += 1
	
	
	matched_indexes = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
		
	i = 0
	
	length1 = len(preset)
	length2 = len(JK_SF.names)
	while i < length1:
		j = 0
		while j < length2:
			if preset[i] == JK_SF.names[j]:
				matched_indexes[i]=j+1
				j = length2
			j += 1
		i += 1
	
	
	i = 0
	while i < 8:
		ac.setValue(ambient_preset_UI['ambient_sound_number'+str(i)],matched_indexes[i]) 
		ac.setValue(ambient_preset_UI['ambient_sound_vol'+str(i)], JK_INI.config_ambient.getfloat(ambient_name,"Ambient_vol"+str(i)))
		i += 1
	
def hideGUI():
	ambient_preset_UI
	for v in ambient_preset_UI.values():
		ac.setVisible(v, 0)
			
	
	
def hide_unhide_GUI(name,val):
	ambient_preset_UI	
	get_key = ambient_preset_UI.keys()
	
	keys_needed = []
	
	if val > 1:
		val == 1
		
	for wert in get_key:
		if wert.find(name) > -1:
			ac.setVisible(ambient_preset_UI[wert], val)	

def unhideGUI():
	global W_x,W_y,ambient_preset_UI,is_playing,first_frame
	ac.setSize(JK_GUI.GUI_window, W_x, W_y)
	for v in ambient_preset_UI.values():
		ac.setVisible(v, 1)
		
	ac.setVisible(ambient_preset_UI['textInput'], 0)
	
	'''if is_playing == 0: 
		hide_unhide_GUI("ambient_vol_",0)
		hide_unhide_GUI("Debug_ambient_vol",0)
		hide_unhide_GUI("cam_pos_",0)
	'''
	first_frame = 1

def Volume_koppeln(*args):
	global update_vol
	update_vol=1
	
	
def update(deltaT):	
	global update_ambient_name, first_frame, ambient_preset_UI
	
	if update_ambient_name ==1 or first_frame==1:
		i = 0
		while i < 8:
			ac.setText(ambient_preset_UI['ambient_sound_number_label'+str(i)],JK_SF.names[int(ac.getValue(ambient_preset_UI['ambient_sound_number'+str(i)])-1.0)])
			i += 1
		update_ambient_name = 0
		first_frame = 0
	
	
	
	
	
	
def Create_Ambient_GUI():
	global ambient_preset_UI, W_y, textInput
	# Name the Ambient
	
	ambient_preset_UI['mode_name'] = ac.addLabel(JK_GUI.GUI_window , "Ambient Editor")
	ac.setPosition(ambient_preset_UI['mode_name'], 130,47)
	
	ambient_preset_UI['Ambient_name_desc'] = ac.addLabel(JK_GUI.GUI_window , "Ambient name:")
	ac.setPosition(ambient_preset_UI['Ambient_name_desc'], 15,100)
	ambient_preset_UI['Ambient_name'] = ac.addLabel(JK_GUI.GUI_window , textInput)
	ac.setPosition(ambient_preset_UI['Ambient_name'], 150,100)
	ambient_preset_UI['Rename_Ambient'] = ac.addButton(JK_GUI.GUI_window , "Rename")
	ac.setPosition(ambient_preset_UI['Rename_Ambient'], 250,100)
	ac.setSize(ambient_preset_UI['Rename_Ambient'], 80, 25)
	ac.addOnClickedListener(ambient_preset_UI['Rename_Ambient'], onRename)
	ambient_preset_UI['textInput'] = ac.addTextInput(JK_GUI.GUI_window ,"AMBIENT1")
	ac.setPosition(ambient_preset_UI['textInput'],130,100)
	ac.setSize(ambient_preset_UI['textInput'],160,30)
	ac.addOnValidateListener(ambient_preset_UI['textInput'],onTextinput)

	
	y=160
	
	ambient_name = 'Nature'
	ac.setText(ambient_preset_UI['Ambient_name'],ambient_name)
	preset = []
	i = 0
	while i < 8:
		#ac.log(JK_INI.config_ambient.get(ambient_name,"ambient"+str(i)))
		preset.append(JK_INI.config_ambient.get(ambient_name,"ambient"+str(i)))
		i += 1
	
	#preset=["birds_forrest.ogg","birds_forrest2.ogg","ambient_crows.ogg","japan_kodamas.ogg","night_forrest.ogg","night_forrest2.ogg","wind_forrest1.ogg","wind_forrest2.ogg"]			
	#[3,4,2,13,17,18,31,32]
	matched_indexes = [1,1,1,1,1,1,1,1,1,1,1,1,1,1]
		
	i = 0
	
	length1 = len(preset)
	length2 = len(JK_SF.names)
	while i < length1:
		j = 0
		while j < length2:
			if preset[i] == JK_SF.names[j]:
				matched_indexes[i]=j+1
				j = length2
			j += 1
		i += 1
	
	
	i = 0
	while i < 8:
		y = 160 + i * 60
		if i < 4:
			ambient_preset_UI['ambient_sound_number'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , "Ambient Sound " + str(i+1))
		elif i < 6:
			ambient_preset_UI['ambient_sound_number'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , "Night Sound " + str(i-3))
		elif i < 8:
			ambient_preset_UI['ambient_sound_number'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , "Rain Sound " + str(i-5))
		ac.setPosition(ambient_preset_UI['ambient_sound_number'+str(i)], 20, y)
		ac.setSize(ambient_preset_UI['ambient_sound_number'+str(i)], 150, 25)
		ac.setRange(ambient_preset_UI['ambient_sound_number'+str(i)], 1, JK_SF.n)
		
		ac.setValue(ambient_preset_UI['ambient_sound_number'+str(i)],matched_indexes[i]) 		#random.randint(1, JK_SF.n))
		ac.addOnValueChangeListener(ambient_preset_UI['ambient_sound_number'+str(i)], onAmbientsound)
		ambient_preset_UI['ambient_sound_number_label'+str(i)] = ac.addLabel(JK_GUI.GUI_window , "TEST")
		ac.setPosition(ambient_preset_UI['ambient_sound_number_label'+str(i)], 200, y)
		
		ambient_preset_UI['ambient_sound_vol'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , "Volume " )
		ac.setPosition(ambient_preset_UI['ambient_sound_vol'+str(i)], 490, y)
		ac.setSize(ambient_preset_UI['ambient_sound_vol'+str(i)], 80, 25)
		ac.setRange(ambient_preset_UI['ambient_sound_vol'+str(i)], 0, 100)
		ac.setValue(ambient_preset_UI['ambient_sound_vol'+str(i)], JK_INI.config_ambient.getfloat(ambient_name,"Ambient_vol"+str(i)))
		
		
		
		i += 1
	
	
	y += 60
	
	ambient_preset_UI['Ambient_Update_button'] = ac.addButton(JK_GUI.GUI_window , "Update Preset")
	ac.setPosition(ambient_preset_UI['Ambient_Update_button'], 10, y)
	ac.setSize(ambient_preset_UI['Ambient_Update_button'], 120, 25)
	ac.addOnClickedListener(ambient_preset_UI['Ambient_Update_button'], onUpdatebuttonClick)
	
	ambient_preset_UI['Ambient_save_button'] = ac.addButton(JK_GUI.GUI_window , "Save Ambient")
	ac.setPosition(ambient_preset_UI['Ambient_save_button'], 150, y)
	ac.setSize(ambient_preset_UI['Ambient_save_button'], 120, 25)
	ac.addOnClickedListener(ambient_preset_UI['Ambient_save_button'], onSavebuttonClick)
	
	y += 60
	
	W_y = y + 40
	
	
	
	ambient_preset_UI['ambient_vol'] = ac.addSpinner(JK_GUI.GUI_window , "Volume " )
	ac.setPosition(ambient_preset_UI['ambient_vol'], 20, y)
	ac.setSize(ambient_preset_UI['ambient_vol'], 150, 25)
	ac.setRange(ambient_preset_UI['ambient_vol'], 0, 100)
	ac.setValue(ambient_preset_UI['ambient_vol'], 10.0)
	ac.addOnValueChangeListener(ambient_preset_UI['ambient_vol'],Volume_koppeln)
	
	
	
	ambient_preset_UI['Debug_ambient_vol']= ac.addLabel(JK_GUI.GUI_window , "Debug Ambient Volume by Position:")
	ac.setPosition(ambient_preset_UI['Debug_ambient_vol'], 300, y-60)
	ac.setSize(ambient_preset_UI['Debug_ambient_vol'], 50, 25)
	
	y += 10
	
	
	i = 0
	while i < 3:
		ambient_preset_UI['cam_pos_'+str(i)]= ac.addLabel(JK_GUI.GUI_window , "X=0.00")
		ac.setPosition(ambient_preset_UI['cam_pos_'+str(i)], 250 + 100 * i, y-35)
		ac.setSize(ambient_preset_UI['cam_pos_'+str(i)], 50, 25)
		i += 1
	
	i = 0
	while i < 4:
		ambient_preset_UI['ambient_vol_'+str(i)]= ac.addLabel(JK_GUI.GUI_window , "0.00")
		ac.setPosition(ambient_preset_UI['ambient_vol_'+str(i)], 200 + 40 * i, y)
		ac.setSize(ambient_preset_UI['ambient_vol_'+str(i)], 50, 25)
		i += 1
		
	i = 0
	while i < 2:
		ambient_preset_UI['ambient_vol_Slash'+str(i)]= ac.addLabel(JK_GUI.GUI_window , "|")
		ac.setPosition(ambient_preset_UI['ambient_vol_Slash'+str(i)], 360 + i * 110, y)
		ac.setSize(ambient_preset_UI['ambient_vol_Slash'+str(i)], 50, 25)
		i += 1
	
	i = 0
	while i < 2:
		ambient_preset_UI['ambient_vol_n_'+str(i)]= ac.addLabel(JK_GUI.GUI_window , "0.00")
		ac.setPosition(ambient_preset_UI['ambient_vol_n_'+str(i)], 380 + 40 * i, y)
		ac.setSize(ambient_preset_UI['ambient_vol_n_'+str(i)], 50, 25)
		i += 1
	
	i = 0
	while i < 2	:
		ambient_preset_UI['ambient_vol_r_'+str(i)]= ac.addLabel(JK_GUI.GUI_window , "0.00")
		ac.setPosition(ambient_preset_UI['ambient_vol_r_'+str(i)], 500 + 40 * i, y)
		ac.setSize(ambient_preset_UI['ambient_vol_r_'+str(i)], 50, 25)
		i += 1
		
	JK_Debug.log(" finished")