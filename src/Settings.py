import gconf
import sys
import os

#GENERAL_OPTIONS = {'binary': '', 'captureDir': '', 'romsDir': '', 'captureFormat': '0', 'saveDir': '', 'batteryDir': ''}
#CONTROL_OPTIONS = {'Joy0_Left': '0114' , 'Joy0_Right': '0113', 'Joy0_Up': '0111', 'Joy0_Down': '0112', 'Joy0_A': '007a', 'Joy0_B': '0078', 'Joy0_L': '0061', 'Joy0_R': '0073', 'Joy0_Start': '000d', 'Joy0_Select': '0008', 'Joy0_Speed': '0020', 'Joy0_Capture': '0125', 'Motion_Left': '0104', 'Motion_Right': '0106', 'Motion_Up': '0108', 'Motion_Down': '0102'}
#GRAPHIC_OPTIONS = {'video': '1', 'fullScreen': '0', 'throttle': '0', 'filter': '0', 'gbFrameSkip': '0', 'frameSkip': '2', 'ifbType':'0', 'autoFrameSkip': '0', 'colorOption': '1', 'borderAutomatic': '0'}
#SOUND_OPTIONS = {'soundQuality': '2', 'soundVolume': '0', 'soundEnable': '30f', 'soundReverse': '0', 'soundOff': '0', 'soundEcho': '0', 'soundLowPass': '0'}
#ADVANCED_OPTIONS = {'saveType': '0', 'biosFile': 'none', 'flashSize': '0', 'emulatorType': '1', 'showSpeed': '1', 'rewindTimer': '0', 'showSpeedTransparent': '1', 'rtcEnabled': '0', 'useBios': '0', 'skipBios': '0', 'disableStatus': '0', 'pauseWhenInactive': '0', 'agbPrint': '0', 'borderOn': '0', 'disableMMX': '1'}

GENERAL_OPTIONS = ['binary', 'captureDir', 'romsDir', 'captureFormat', 'saveDir', 'batteryDir']
CONTROL_OPTIONS = ['Joy0_Left', 'Joy0_Right', 'Joy0_Up', 'Joy0_Down', 'Joy0_A', 'Joy0_B', 'Joy0_L', 'Joy0_R', 'Joy0_Start', 'Joy0_Select', 'Joy0_Speed', 'Joy0_Capture', 'Motion_Left', 'Motion_Right', 'Motion_Up', 'Motion_Down']
GRAPHIC_OPTIONS = ['video', 'fullScreen', 'throttle', 'filter', 'gbFrameSkip', 'frameSkip', 'ifbType', 'autoFrameSkip', 'colorOption', 'borderAutomatic']
SOUND_OPTIONS = ['soundQuality', 'soundVolume', 'soundEnable', 'soundReverse', 'soundOff', 'soundEcho', 'soundLowPass']
ADVANCED_OPTIONS = ['saveType', 'biosFile', 'flashSize', 'emulatorType', 'showSpeed', 'rewindTimer', 'showSpeedTransparent', 'rtcEnabled', 'useBios', 'skipBios', 'disableStatus', 'pauseWhenInactive', 'agbPrint', 'borderOn', 'disableMMX']


class Settings:
	def __init__(self):
		self.settings = {}
		#TODO: use 'which VisualBoyAdvance' to try to find vba path 
		#humm better to make that when we open the preferences box AND binary == ''

		self.client = gconf.client_get_default();
		self.client.add_dir("/apps/gnomeboyadvance", gconf.CLIENT_PRELOAD_NONE)

		self.readGConf()


	def readGConf(self):
		for elt in GENERAL_OPTIONS:
			self.settings[elt] = self.client.get_string("/apps/gnomeboyadvance/general/"+ elt)

		for elt in CONTROL_OPTIONS:
			self.settings[elt] = self.client.get_string("/apps/gnomeboyadvance/control/"+ elt)
			
		for elt in ADVANCED_OPTIONS:
			self.settings[elt] = self.client.get_string("/apps/gnomeboyadvance/advanced/"+ elt)

		for elt in SOUND_OPTIONS:
			self.settings[elt] = self.client.get_string("/apps/gnomeboyadvance/sound/"+ elt)

		for elt in GRAPHIC_OPTIONS:
			self.settings[elt] = self.client.get_string("/apps/gnomeboyadvance/graphic/"+ elt)
	

	def writeGConf(self):
		for elt in GENERAL_OPTIONS:
			self.client.set_string("/apps/gnomeboyadvance/general/"+ elt, self.settings[elt])

		for elt in CONTROL_OPTIONS:
			self.client.set_string("/apps/gnomeboyadvance/control/"+ elt, self.settings[elt])

		for elt in ADVANCED_OPTIONS:
			self.client.set_string("/apps/gnomeboyadvance/advanced/"+ elt, self.settings[elt])

		for elt in SOUND_OPTIONS:
			self.client.set_string("/apps/gnomeboyadvance/sound/"+ elt, self.settings[elt])
			
		for elt in GRAPHIC_OPTIONS:
			self.client.set_string("/apps/gnomeboyadvance/graphic/"+ elt, self.settings[elt])


	def writeFile(self, path):	
		f = file(path, 'w')

		for elt in GENERAL_OPTIONS:
			if self.settings[elt]: 
				l = elt + '=' + self.settings[elt] + '\n'

		for options in [CONTROL_OPTIONS, GRAPHIC_OPTIONS, SOUND_OPTIONS, ADVANCED_OPTIONS]:
			for elt in options:
				l = elt + '=' + self.settings[elt] + '\n'
				f.write(l)
		
		f.close()

	def readFile(self, path):
		buff = file(path, 'r').readlines()
		#regexp = re.compile("[=\t]")

		for l in buff:
			l = l.lstrip()
			if l.startswith('#') or len(l)<1 : continue #drop comments and empty line
			#TODO: use a regexp insteed of this dirty thing
			#tmp = regexp.split(l)
			tmp = l.split('=')
			if len(tmp) == 1: 
				tmp = l.split()
			else:
				tmp[1] = tmp[1][:-1]	#drop \n (i know it's dirty!)
			
			#if not self.settings.has_key(tmp[0]):
			#	print "FUCK OFF:", tmp[0] #TODO: raise a exception
			#	sys.exit()
			self.settings[tmp[0]] = tmp[1]

	def confFile(self):
		path = os.tmpnam()
		self.writeFile(path)
		return path

if __name__ == "__main__":
	#self test
	set = Settings()
	set.readGConf()
	set.writeGConf()
