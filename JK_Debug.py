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
import string

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

def log(job):

	module_name = str(sys._getframe(1).f_code.co_filename)
	module_name = module_name[ len(str(os.path.dirname(__file__)))+1: ]
	tm = time.time()%1.0
	tm = str(int(tm*1000.0))
	ac.log(time.strftime("%H:%M:%S", time.localtime())+":"+tm[0:]+ ": "+module_name +": "+sys._getframe(1).f_code.co_name+job)
def log_m(job,script):

	tm = time.time()%1.0
	tm = str(int(tm*1000.0))
	ac.log(time.strftime("%H:%M:%S", time.localtime())+":"+tm[0:]+ ": "+script +": "+sys._getframe(1).f_code.co_name+job)
	
def processing_fun():
	outvar = ""
	outvar += "\n"+sys._getframe(1).f_code.co_filename+" is \n"
	outvar += "\n /$$$$$$$                                                            /$$                    "
	outvar += "\n| $$__  $$                                                          |__/                    "
	outvar += "\n| $$  \ $$ /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$$ /$$$$$$$ /$$ /$$$$$$$   /$$$$$$ "
	outvar += "\n| $$$$$$$//$$__  $$ /$$__  $$ /$$_____/ /$$__  $$ /$$_____//$$_____/| $$| $$__  $$ /$$__  $$"
	outvar += "\n| $$____/| $$  \__/| $$  \ $$| $$      | $$$$$$$$|  $$$$$$|  $$$$$$ | $$| $$  \ $$| $$  \ $$"
	outvar += "\n| $$     | $$      | $$  | $$| $$      | $$_____/ \____  $$\____  $$| $$| $$  | $$| $$  | $$"
	outvar += "\n| $$     | $$      |  $$$$$$/|  $$$$$$$|  $$$$$$$ /$$$$$$$//$$$$$$$/| $$| $$  | $$|  $$$$$$$"
	outvar += "\n|__/     |__/       \______/  \_______/ \_______/|_______/|_______/ |__/|__/  |__/ \____  $$"
	outvar += "\n                                                                                   /$$  \ $$"
	outvar += "\n                     without fatal exception errors until now                     |  $$$$$$/"
	outvar += "\n                                                                                   \______/ \n "

	ac.log(outvar)