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
import inspect 

# Set library path
if platform.architecture()[0] == "64bit":
	libdir = 'third_party/lib64'
else:
	libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import pygame

libdir = 'module'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))

import JK_GUI
import JK_Debug
import JK_SF
import JK_INI

# initation

pygame.init()

current_dir = os.path.dirname(os.path.abspath(__file__))

pygame.mixer.pre_init(16000, 16, 2, 512)   # pre init 44.1khz, 16bit, mono, buffer(KB)
pygame.mixer.init(16000)                       # init mixer


#Variablen init
acUpdate_start = 0

JK_Debug.processing_fun()	
	
def acMain(ac_version):
	JK_GUI.CreateGUI()
	JK_Debug.log_m(" finished","JK_Ambient_tester")	
	return __file__


	
def acUpdate(delta_t):
	global acUpdate_start
	
	if acUpdate_start == 0:
		acUpdate_start += 1
		JK_Debug.log_m(" ready","JK_Ambient_tester")
		JK_GUI.GUI_loaded = 1
		
		
	JK_GUI.UpdateGUI(delta_t)
	

	
		
def acShutdown(*args):
	JK_INI.quit()
	JK_SF.quit()
	pygame.quit()