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


# Set library path
if platform.architecture()[0] == "64bit":
	libdir = 'third_party/lib64'
else:
	libdir = 'third_party/lib'
sys.path.insert(0, os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), libdir))
os.environ['PATH'] = os.environ['PATH'] + ";."

import pygame



# initation

pygame.init()

current_dir = os.path.dirname(os.path.abspath(__file__))

pygame.mixer.pre_init(16000, 16, 2, 512)   # pre init 44.1khz, 16bit, mono, buffer(KB)
pygame.mixer.init(16000)                       # init mixer



libdir = 'module'
sys.path.insert(0, os.path.join(os.path.dirname(__file__), libdir))

import JK_GUI
import JK_Ambient
import JK_Debug
import JK_INI
import JK_Master

n = 0
names = []
sounds = []
timer = 0
loading_preset_active = 0
snr = []
update_vol=0

def Check_Folder():
	global names,n
	
	path = os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), "ambient_sounds_ogg")
	dirs = os.listdir(path)
	n=0
	
	for file in dirs:
		names.append(file)
		n+= 1
		
	names.append("Tunnel")
	JK_Debug.log(" finished")
	
	
def searchSFnames(text,zahl):
	global names, ambient_preset_UI,update_ambient_name
	update_ambient_name = 1
	
	anfang = text[ : zahl].lower()
	length = len(names)
	i=0
	j = 0
	while j < length:
		name = names[j].lower()
		if name.find(anfang) > -1:							#anfang == sfnames[j][ : zahl]:
			if i<8:
				ac.setValue(JK_Ambient.ambient_preset_UI['ambient_sound_number'+str(i)],j+1)	
				i += 1
				
			
		j += 1
		
def init_sounds():
	global sounds, snr
	
	i = 0
	
	while i < 30:
		sounds.append(None)
		snr.append(None)
		i += 1
		
	load_Files_from_Config()
	
def load_Files_from_Config():
	#Ambient Sounds aus aktiven Preset laden
	
	jkthread =  threading.Thread(target=loading_preset, args=(1,))
	jkthread.start()


def loading_preset(name):
	global sounds, names, snr, loading_preset_active
	loading_preset_active += 1
	mythreadnr =  loading_preset_active
	while JK_GUI.GUI_loaded < 1:
		i = 0
	
	sections = JK_INI.config_ambient.sections()
	ambient_name = sections[int(ac.getValue(JK_Master.Master_GUI['ambient_preset'])-1)]
	#ac.log(str(ac.getValue(JK_Master.Master_GUI['ambient_preset'])-1))
	
	i = 0
	while i < 8:
		if mythreadnr < loading_preset_active:
			JK_Debug.log(" recognize higher instance")
			i = 100
		path = os.path.join(os.path.join(os.path.dirname(__file__),os.pardir), "ambient_sounds_ogg")
		if snr[i] != ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_number'+str(i)]):
			soundfile = names[int(ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_number'+str(i)])-1.0)] #JK_INI.config_ambient.get(ambient_name,"ambient"+str(i))
			path_sf = os.path.join(path, soundfile)
			JK_Debug.log(" "+soundfile+" ("+str(i)+")")
			sounds[i] = pygame.mixer.Sound(path_sf)
			snr[i] = ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_number'+str(i)])
		i += 1
	
	if mythreadnr == loading_preset_active:
		JK_Debug.log(" finished")
		loading_preset_active = 0
		i = 0
		while i < 8:
			sounds[i].play(-1)
			sounds[i].set_volume(0)
			i +=1

	

def update_sounds():
	stop_sound()
	load_Files_from_Config()
	
	
	
def stop_sound():
	global sounds, loading_preset_active
	
	i = 0
	if loading_preset_active == 0:
		while i < 8:
			sounds[i].stop()
			i +=1
			
def update_volume(*args):
	global sounds, update_vol
	
	if update_vol == 1:
		JK_Debug.log(" finished")
		JK_Master.update_vol = 0
		update_vol = 0
		
	if update_vol == 2:
		JK_Debug.log(" finished")
		JK_Ambient.update_vol = 0
		update_vol = 0
		
	if JK_Ambient.update_vol == 1:
		vol = ac.getValue(JK_Ambient.ambient_preset_UI['ambient_vol'])
		ac.setValue(JK_Master.Master_GUI['ext_vol'],vol)
		ac.setValue(JK_Master.Master_GUI['int_vol'],JK_Master.int_mult*vol+0.5)
		update_vol = 1
		JK_Ambient.update_vol = 0
		
	if JK_Master.update_vol == 1:
		vol = ac.getValue(JK_Master.Master_GUI['ext_vol'])
		ac.setValue(JK_Master.Master_GUI['int_vol'],JK_Master.int_mult*vol+0.5)
		ac.setValue(JK_Ambient.ambient_preset_UI['ambient_vol'],vol)
		update_vol = 2
		JK_Master.update_vol = 0
	
		
		
	#Ambient
	import math
	pos_x, pos_y, pos_z = ac.ext_getCameraPosition()
	pos = [pos_x,pos_y,pos_z]
	XYZ = ["X","Y","Z"]
	const_scal_x = [ 100.0, 6737.0, 1848.0, 4848.0, 370.0, 824.0, 846.0, 926.0]
	const_scal_z = [ 230.0, 825.0, 880.0, 1480.0, 348.0, 952.0, 786.0, 923.0]
	offset_x = [ 0.0, 152.0, 262.0, 927.0, 400.0, 180.0, 612.0, 552.0]
	offset_z = [ 0.0, 688.0, 28.0, 419.0, 741.0, 302.0, 264.0, 388.0]
	nacht = 0.0
	cam = ac.isCameraOnBoard(ac.getFocusedCar())
	hour = 0.0
	sDebug = ac.ext_weatherDebugText()
	posTime = sDebug.find("current day: ")+13 # len('current day: ') = 13
	vdatetime = sDebug[ posTime : posTime+19 ] 
	if len(vdatetime)>0:
		sdatetime = str(vdatetime).replace("['", "").replace("']", "")
		# current day: 2020-05-06 16:31:25
		f = sdatetime.split(' ')
		# ac.log(str(f))
		sdate = f[0]
		stime = f[1]
		tmp = stime.split(':')
		hour=float(int(tmp[0]))
		minute=float(int(tmp[1]))
		second=int(tmp[2])
	
	posRain = sDebug.find("RainFX ")+20 # len('current day: ') = 13
	Rainval = float(sDebug[ posRain : posRain+4 ])
	if Rainval < 0.5: Rainval = Rainval * 2.0
	else: Rainval = 1.0
	if hour > 20 or hour < 5:
		
		if hour ==21:
			nacht = minute / 60.0
		elif hour ==4:
			nacht = 1.0 -  minute / 60.0
		else:
			nacht = 1.0
	
	i = 0
	while i < 8: 
		if i < 4:
			vol_pos = (math.sin(pos_x / const_scal_x[i] + offset_x[i]) + math.sin(pos_z / const_scal_z[i] + offset_z[i]) + 2.0) / 4.0
			vol_master = ac.getValue(JK_Master.Master_GUI['ext_vol']) / 100.0
			vol_as = ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_vol'+str(i)]) / 100.0
			vol_nacht = 1.0 - nacht
			vol_rain = 1.0 - Rainval
			vol_cam = 1.0
			if cam == True:
				vol_cam = ac.getValue(JK_Master.Master_GUI['int_vol'])/ac.getValue(JK_Master.Master_GUI['ext_vol'])
			sounds[i].set_volume(vol_pos * vol_master * vol_as * vol_nacht * vol_rain * vol_cam)
			#ac.log(str(vol_pos * vol_master * vol_as * vol_nacht * vol_rain * vol_cam))
			ac.setText(JK_Ambient.ambient_preset_UI['ambient_vol_'+str(i)],str(int(vol_pos * 100)))
		elif i < 6:
			vol_pos = (math.sin(pos_x / const_scal_x[i] + offset_x[i]) + math.sin(pos_z / const_scal_z[i] + offset_z[i]) + 2.0) / 4.0
			vol_master = ac.getValue(JK_Master.Master_GUI['ext_vol']) / 100.0
			vol_as = ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_vol'+str(i)]) / 100.0
			vol_nacht =  nacht
			vol_rain = 1.0 - Rainval
			vol_cam = 1.0
			if cam == True:
				vol_cam = ac.getValue(JK_Master.Master_GUI['int_vol'])/ac.getValue(JK_Master.Master_GUI['ext_vol'])
			sounds[i].set_volume(vol_pos * vol_master * vol_as * vol_nacht * vol_rain * vol_cam)
			ac.setText(JK_Ambient.ambient_preset_UI['ambient_vol_n_'+str(i-4)],str(int(vol_pos * 100)))
		elif i < 8:
			vol_pos = (math.sin(pos_x / const_scal_x[i] + offset_x[i]) + math.sin(pos_z / const_scal_z[i] + offset_z[i]) + 2.0) / 4.0
			vol_master = ac.getValue(JK_Master.Master_GUI['ext_vol']) / 100.0
			vol_as = ac.getValue(JK_Ambient.ambient_preset_UI['ambient_sound_vol'+str(i)]) / 100.0
			vol_rain =  Rainval
			vol_cam = 1.0
			vol_nacht = 1.0
			if cam == True:
				vol_cam = ac.getValue(JK_Master.Master_GUI['int_vol'])/ac.getValue(JK_Master.Master_GUI['ext_vol'])
			sounds[i].set_volume(vol_pos * vol_master * vol_as  * vol_rain * vol_cam)
			ac.setText(JK_Ambient.ambient_preset_UI['ambient_vol_r_'+str(i-6)],str(int(vol_pos * 100)))
			
		
		i += 1
	cam = ac.isCameraOnBoard(ac.getFocusedCar())
	dta=[Rainval,minute,cam]
	i = 0	
	while i < 3: 
		
		ac.setText(JK_Ambient.ambient_preset_UI['cam_pos_'+str(i)],XYZ[i]+"="+ str(round(pos[i],1))) #str(dta[i])) #str(round(pos[i],1)))
		i += 1			


def update(deltaT):
	global timer
	timer += deltaT
	
	if timer >= 0.2:
		if loading_preset_active == 0:
			if JK_GUI.GUI_loaded == 1:
				#JK_Debug.log(" ready")
				update_volume()
		
		timer = 0
	
			
	
def quit():
	global sounds
	stop_sound()
	sounds = None
	pygame.quit()
	
	
