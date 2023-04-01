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

W_x = 1000
W_y = 60

Sections = []
update_vol=0
GUI = {}
int_mult=1

event_count = 0.0
event_show = 0.0
update_event_spinner = 0
event_data =[]
is_active = 0
timer = 0
	
	
	
def hideGUI():
	global GUI
	for v in GUI.values():
		ac.setVisible(v, 0)
			
	
	
def hide_unhide_GUI(name,val):
	global GUI	
	get_key = GUI.keys()
	
	keys_needed = []
	
	if val > 1:
		val == 1
		
	for wert in get_key:
		if wert.find(name) > -1:
			ac.setVisible(GUI[wert], val)	

def unhideGUI():
	global W_x,W_y,GUI,is_playing,first_frame
	ac.setSize(JK_GUI.GUI_window, W_x, W_y)
	for v in GUI.values():
		ac.setVisible(v, 1)
		

	


def update(deltaT):
	global timer, update_event_spinner
	
	timer += deltaT
	
	if timer > 0.2:
		if update_event_spinner == 1:
			update_event_spinner = 0
			update_event_sound_number()
		timer = 0
	

	
def Create_GUI():
	global GUI, W_y, event_data
	
	GUI["create_event_button"] = ac.addButton(JK_GUI.GUI_window , "Create new Event")
	ac.setPosition(GUI["create_event_button"], 10, 80)
	ac.setSize(GUI["create_event_button"], 150, 25)
	ac.addOnClickedListener(GUI["create_event_button"], CreateEvent)
	
	GUI["delete_event_button"] = ac.addButton(JK_GUI.GUI_window , "Delete Event")
	ac.setPosition(GUI["delete_event_button"], 180, 80)
	ac.setSize(GUI["delete_event_button"], 150, 25)
	ac.addOnClickedListener(GUI["delete_event_button"], DeleteEvent)
	
	
	GUI["play_event_button"] = ac.addButton(JK_GUI.GUI_window , "Play ")
	ac.setPosition(GUI["play_event_button"], 600, 80)
	ac.setSize(GUI["play_event_button"], 50, 25)
	ac.addOnClickedListener(GUI["play_event_button"], PlayEvent)
	
	i = 0
	while i < 10:
		y = 140 + i * 60
		
		
		GUI['event_label'+str(i)] = ac.addLabel(JK_GUI.GUI_window , "  Event " + str(i+1))
		ac.setPosition(GUI['event_label'+str(i)], 40, y-25)
		
		GUI['event_del_button'+str(i)] = ac.addButton(JK_GUI.GUI_window , "X" )
		ac.setPosition(GUI['event_del_button'+str(i)], 120, y-25)
		ac.setSize(GUI['event_del_button'+str(i)], 15, 20)
		
		
		GUI['event_sound_number'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , " ")		#"Sound Event " + str(i+1))	
		ac.setPosition(GUI['event_sound_number'+str(i)], 20, y)
		ac.setSize(GUI['event_sound_number'+str(i)], 150, 25)
		ac.setRange(GUI['event_sound_number'+str(i)], 1, JK_SF.n+1)
		ac.setValue(GUI['event_sound_number'+str(i)],1.0) 
		ac.addOnValueChangeListener(GUI['event_sound_number'+str(i)], event_spinner_isclicked)
		
		GUI['event_info'+str(i)] = ac.addLabel(JK_GUI.GUI_window , "ambient_birds.ogg | A: (1000/-1000) | B: (1000/-1000) | dist: 1000")
		ac.setPosition(GUI['event_info'+str(i)], 180, y-15)
		GUI['event_set_A'+str(i)] = ac.addButton(JK_GUI.GUI_window , "Set A" )
		GUI['event_set_B'+str(i)] = ac.addButton(JK_GUI.GUI_window , "Set B" )
		ac.setPosition(GUI['event_set_A'+str(i)], 620, y)
		ac.setSize(GUI['event_set_A'+str(i)], 60, 22)
		ac.setPosition(GUI['event_set_B'+str(i)], 700, y)
		ac.setSize(GUI['event_set_B'+str(i)], 60, 22)
		GUI['event_sound_vol'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , "Volume")
		ac.setPosition(GUI['event_sound_vol'+str(i)], 780, y)
		ac.setSize(GUI['event_sound_vol'+str(i)], 80, 25)
		ac.setRange(GUI['event_sound_vol'+str(i)], 0, 100)
		ac.setValue(GUI['event_sound_vol'+str(i)], 100.0)
		ac.addOnValueChangeListener(GUI['event_sound_vol'+str(i)], event_spinner_isclicked)	
		GUI['event_sound_range'+str(i)] = ac.addSpinner(JK_GUI.GUI_window , "Range")
		ac.setPosition(GUI['event_sound_range'+str(i)], 880, y)
		ac.setSize(GUI['event_sound_range'+str(i)], 80, 25)
		ac.setRange(GUI['event_sound_range'+str(i)], 0, 100)
		ac.setValue(GUI['event_sound_range'+str(i)], 0.0)
		ac.addOnValueChangeListener(GUI['event_sound_range'+str(i)], event_spinner_isclicked)
		i += 1
	
	W_y = 140 + 60 * 10

	ac.addOnClickedListener(GUI['event_del_button'+str(0)], DelEvent1)
	ac.addOnClickedListener(GUI['event_del_button'+str(1)], DelEvent2)
	ac.addOnClickedListener(GUI['event_del_button'+str(2)], DelEvent3)
	ac.addOnClickedListener(GUI['event_del_button'+str(3)], DelEvent4)
	ac.addOnClickedListener(GUI['event_del_button'+str(4)], DelEvent5)
	ac.addOnClickedListener(GUI['event_del_button'+str(5)], DelEvent6)
	ac.addOnClickedListener(GUI['event_del_button'+str(6)], DelEvent7)
	ac.addOnClickedListener(GUI['event_del_button'+str(7)], DelEvent8)
	ac.addOnClickedListener(GUI['event_del_button'+str(8)], DelEvent9)
	ac.addOnClickedListener(GUI['event_del_button'+str(9)], DelEvent10)
		
		
	data1 =[]#sfnr
	data2 =[]#pos1_x,z
	data3 =[]#pos2_x,z
	data4 =[]#Volume,Range (Wo man mit 100% Lautstärke hört)
	

		
	i = 0
	while i < 100:
		data1.append(1)		#random.randint(1, z1))
		data2.append(["n","n"])
		data3.append(["n","n"])
		data4.append([100.0,10.0,1000.0])
		i += 1
	
	event_data =[data1,data2,data3,data4]	
	
	JK_Debug.log(" finished")


def PlayEvent(*args):
	i = 0
	
	'''global sounds,soundbank,is_playing_event,event_show
	
	if is_playing_event==0:
		is_playing_event=1
		
	elif is_playing_event==1:
		is_playing_event=0
'''

def CreateEvent(*args):
	global event_show
	event_show += 1.0
	if event_show > 100:
		event_show = 100
	if event_show > 1: event_data[0][int(event_show)-1] = event_data[0][int(event_show)-2]
	
	Show_Event_Sound()

def DeleteEvent(*args):
	global event_show
	event_show -= 1.0
	if event_show < 0:
		event_show = 0
	Show_Event_Sound()
	
def DelEvent1(*args):	Delete_Event_Sound(1)
def DelEvent2(*args):	Delete_Event_Sound(2)
def DelEvent3(*args):	Delete_Event_Sound(3)
def DelEvent4(*args):	Delete_Event_Sound(4)
def DelEvent5(*args):	Delete_Event_Sound(5)
def DelEvent6(*args):	Delete_Event_Sound(6)
def DelEvent7(*args):	Delete_Event_Sound(7)
def DelEvent8(*args):	Delete_Event_Sound(8)
def DelEvent9(*args):	Delete_Event_Sound(9)
def DelEvent10(*args):	Delete_Event_Sound(10)

def Delete_Event_Sound(i):
	global event_show, event_data
	a = i - 1
	
	if event_show <= 10:
		i = int(a)
		while i < 99	:
			j=0
			while j < 4:
			
				event_data[j][i] = event_data[j][i+1]
				j += 1
			i +=1
			
	if event_show > 10:
		i = int(a)+int(event_show)-10
		while i < 99:
			j=0
			while j < 4:
			
				event_data[j][i] = event_data[j][i+1]
				j += 1
			i +=1	
				
	event_show -= 1.0
	Show_Event_Sound()
	
def Show_Event_Sound():
	global event_count,event_show, GUI,event_data,is_active
	if is_active==2:
		if event_show <= 10:
			i = 0
			while i < event_show:
				ac.setVisible(GUI['event_sound_number'+str(i)],1) 
				ac.setVisible(GUI['event_del_button'+str(i)],1)
				ac.setVisible(GUI['event_label'+str(i)],1)
				ac.setText(GUI['event_label'+str(i)],"  Event " + str(i+1))
				ac.setValue(GUI['event_sound_number'+str(i)],event_data[0][i])
				ac.setVisible(GUI['event_info'+str(i)],1)
				ac.setVisible(GUI['event_set_A'+str(i)],1)
				ac.setVisible(GUI['event_set_B'+str(i)],1)
				ac.setVisible(GUI['event_sound_vol'+str(i)],1)
				ac.setVisible(GUI['event_sound_range'+str(i)],1)
				ac.setText(GUI['event_info'+str(i)],JK_SF.names[int(event_data[0][i])-1][ : 60] +"\n | A: (1000/-1000) | B: (1000/-1000) | dist: 1000")
				i += 1	
			
			i = int(event_show)
			while i < 10:
				ac.setVisible(GUI['event_sound_number'+str(i)],0) 
				ac.setVisible(GUI['event_del_button'+str(i)],0)
				ac.setVisible(GUI['event_label'+str(i)],0)
				ac.setVisible(GUI['event_info'+str(i)],0)
				ac.setVisible(GUI['event_set_A'+str(i)],0)
				ac.setVisible(GUI['event_set_B'+str(i)],0)
				ac.setVisible(GUI['event_sound_vol'+str(i)],0)
				ac.setVisible(GUI['event_sound_range'+str(i)],0)
				i += 1	
		elif event_show > 10:	
			i = 0
			while i < 10:
				ac.setVisible(GUI['event_sound_number'+str(i)],1)
				ac.setVisible(GUI['event_del_button'+str(i)],1)
				ac.setVisible(GUI['event_label'+str(i)],1)
				ac.setText(GUI['event_label'+str(i)],"  Event " + str(i+1+int(event_show)-10))
				ac.setValue(GUI['event_sound_number'+str(i)],event_data[0][i+int(event_show)-10])
				ac.setVisible(GUI['event_info'+str(i)],1)
				ac.setVisible(GUI['event_set_A'+str(i)],1)
				ac.setVisible(GUI['event_set_B'+str(i)],1)
				ac.setVisible(GUI['event_sound_vol'+str(i)],1)
				ac.setVisible(GUI['event_sound_range'+str(i)],1)
				ac.setText(GUI['event_info'+str(i)],JK_SF.names[int(event_data[0][i+int(event_show)-10])-1][ : 60] +"\n | A: (1000/-1000) | B: (1000/-1000) | dist: 1000")
				i += 1	

def event_spinner_isclicked(*args):
	global update_event_spinner
	
	update_event_spinner = 1
	
def update_event_sound_number(*args):
	global event_count,event_show, GUI,event_data,sounds,soundbank,logger,is_playing_event	
	if event_show <= 10:
		i = 0
		while i < event_show:
			event_data[0][i] = ac.getValue(GUI['event_sound_number'+str(i)])
#			if event_data[0][i] >len(JK_SF.names):
#				playlist[i] = JK_SF.names[0]
#			else: playlist[i]= JK_SF.names[int(event_data[0][i])-1]
#			
			i += 1
		Show_Event_Sound()
	elif event_show > 10:	
		i = 0
		while i < 10:
			event_data[0][i+int(event_show)-10] = ac.getValue(GUI['event_sound_number'+str(i)])
#			if event_data[0][i+int(event_show)-10] >len(soundbank):
#				sounds[i+int(event_show)-10] = soundbank[0]
#			else: sounds[i+int(event_show)-10]= soundbank[int(event_data[0][i+int(event_show)-10])-1]
#
			i += 1	
		Show_Event_Sound()