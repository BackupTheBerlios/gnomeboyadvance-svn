import gconf
import sys
import os

GENERAL_OPTIONS = ['binary', 'captureDir', 'romsDir', 'captureFormat', 'saveDir', 'batteryDir']
CONTROL_OPTIONS = ['Joy0_Left', 'Joy0_Right', 'Joy0_Up', 'Joy0_Down', 'Joy0_A', 'Joy0_B', 'Joy0_L', 'Joy0_R', 'Joy0_Start', 'Joy0_Select', 'Joy0_Speed', 'Joy0_Capture', 'Motion_Left', 'Motion_Right', 'Motion_Up', 'Motion_Down']
GRAPHIC_OPTIONS = ['video', 'fullScreen', 'throttle', 'filter', 'gbFrameSkip', 'frameSkip', 'ifbType', 'autoFrameSkip', 'colorOption', 'borderAutomatic']
SOUND_OPTIONS = ['soundQuality', 'soundVolume', 'soundEnable', 'soundReverse', 'soundOff', 'soundEcho', 'soundLowPass']
ADVANCED_OPTIONS = ['saveType', 'biosFile', 'flashSize', 'emulatorType', 'showSpeed', 'rewindTimer', 'showSpeedTransparent', 'rtcEnabled', 'useBios', 'skipBios', 'disableStatus', 'pauseWhenInactive', 'agbPrint', 'borderOn', 'disableMMX']


class Settings:
	def __init__(self):
		self.settings = {}
		#humm better to make that when we open the preferences box AND binary == ''

		self.client = gconf.client_get_default();
		self.client.add_dir("/apps/gnomeboyadvance", gconf.CLIENT_PRELOAD_NONE)

		self.readGConf()
		if not self.settings['binary']:
			bin = os.popen('which VisualBoyAdvance').read()
			self.settings['binary'] = bin[:-1]

		self.path = os.path.join('/tmp', 'VisualBoyAdvance_' + os.getlogin() + '.cfg')
		self.validity = False


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
		self.validity = False
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
		for elt in ['captureDir', 'captureFormat', 'saveDir', 'batteryDir']:
			if self.settings[elt]: 
				l = elt + '=' + self.settings[elt] + '\n'
				f.write(l)

		for elt in CONTROL_OPTIONS + GRAPHIC_OPTIONS + SOUND_OPTIONS + ADVANCED_OPTIONS:
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
			if len(tmp) != 2: 
				print "droped", tmp
				continue
			self.settings[tmp[0]] = tmp[1]

	def confFile(self):
		if not self.validity: self.writeFile(self.path)
		return self.path

if __name__ == "__main__":
	#self test
	set = Settings()
	print set.settings
	#set.writeGConf()
