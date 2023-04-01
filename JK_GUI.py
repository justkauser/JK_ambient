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

libdir = 'module'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))

import JK_Ambient
import JK_Debug
import JK_SF
import JK_INI
import JK_Master
import JK_Event

GUI_user = {} 
GUI_window = None
change_modus = 0
GUI_mod_Counter = 0
GUI_loaded = 0
timer = 0

def CreateGUI():
	global GUI_window, GUI_user, GUI_mod_Counter
	GUI_window = ac.newApp("Ambient")
	ac.setSize(GUI_window, 180, 80)
	
	JK_INI.loading()
	JK_SF.Check_Folder()
	modus_button = ac.addButton(GUI_window, "Change Mode")
	ac.setPosition(modus_button, 10, 45)
	ac.setSize(modus_button, 100, 25)
	ac.addOnClickedListener(modus_button, ChangeModus)
	
	

	JK_Master.Create_Master_GUI()
	JK_Ambient.Create_Ambient_GUI()
	GUI_mod_Counter += 1
	JK_Event.Create_GUI()
	GUI_mod_Counter += 1
	JK_Ambient.hideGUI()
	JK_Event.hideGUI()
	JK_Master.unhideGUI()
	
	JK_Debug.log(" finished")
	

def UpdateGUI(deltaT):
	global GUI_window, GUI_user, change_modus
	
	JK_Ambient.update(deltaT)
	JK_SF.update(deltaT)
	JK_Event.update(deltaT)
	
	
	
	
	
	
def ChangeModus(*args):
	global change_modus
	
	change_modus += 1
	
	if change_modus > GUI_mod_Counter:
		change_modus = 0
	
	if change_modus == 0:
		JK_Event.hideGUI()
		JK_Master.unhideGUI()
	
	elif change_modus == 1:
		JK_Master.hideGUI()
		JK_Ambient.unhideGUI()
	
	elif change_modus == 2:
		JK_Ambient.hideGUI()
		JK_Event.unhideGUI()
		
	
		

			
