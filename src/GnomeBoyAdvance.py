#!/usr/bin/env python
#authors cass@skynet.be, jay@socialistsoftware.com
#web http://developer.berlios.de/projects/gnomeboyadvance/
#license GPL http://www.gnu.org/copyleft/gpl.html

import os, sys
import string, re

try:
	import pygtk
	pygtk.require('2.0')
	import gtk, gtk.glade
	import gnome, gnome.ui
except:
	print 'You must have python-gtk2, python-gnome2 and python-glade2 installed.'
	sys.exit()

import Settings
import GameList
import key

from const import *

ENTRY_WIDG = ['binary', 'romsDir', 'batteryDir', 'captureDir', 'saveDir', 'throttle', 'gbFrameSkip', 'frameSkip', 'biosFile', 'rewindTimer', 'commandLineOptions']
CHOOSE_WIDG = ['captureFormat', 'video', 'ifbType', 'soundVolume', 'saveType', 'flashSize', 'emulatorType', 'showSpeed']
BOOL_WIDG = ['fullScreen', 'colorOption', 'borderAutomatic', 'autoFrameSkip', 'soundEcho', 'soundLowPass', 'soundReverse', 'soundOff', 'showSpeedTransparent', 'rtcEnabled', 'useBios', 'skipBios', 'disableStatus', 'pauseWhenInactive', 'agbPrint', 'borderOn', 'disableMMX']
CONTROL_WIDG = ['Joy0_Left', 'Joy0_Right', 'Joy0_Up', 'Joy0_Down', 'Joy0_A', 'Joy0_B', 'Joy0_L', 'Joy0_R', 'Joy0_Start', 'Joy0_Select', 'Joy0_Speed', 'Joy0_Capture']
#TODO: we will use Settings.CONTROL_OPTIONS when the motions settings will be configurable with widgets
CALLBACKS = ['on_about1_activate', 'on_quit1_activate', 'on_playGame_clicked', 'on_reload_gamelist_activate', 'on_search_changed', 'on_preferences_activate', 'on_preferences_close_button_clicked', 'on_import_activate', 'on_export_activate', 'on_configure_control_clicked', 'on_binding_press_event', 'on_joy_enable_toggled','on_game_double_click', 'on_exit_activate']


def find_glade():
	#little hack usefull for the developpement
	if os.path.isfile("../glade/gnomeboyadvance.glade"): 
		print "Use glade dev file"
		return '../glade/gnomeboyadvance.glade'
	else: return os.path.join(DATADIR, 'gnomeboyadvance.glade')


class GnomeBoyAdvance:
	def __init__(self):
		gnome.init(PROG_NAME, VERSION)

		glade_f = find_glade()
		
		self.gladeHandler = gtk.glade.XML(glade_f)
                #self.gladeHandler.signal_autoconnect(self.__class__.__dict__)
		#TODO: try to make this dynamic
		dic = {}
		for callback in CALLBACKS:
			dic[callback] = getattr(self, callback)
		self.gladeHandler.signal_autoconnect (dic)

		self.mySettings = Settings.Settings()
		self.joy = None

		if os.access(SETTINGSFILE,os.R_OK):
		#TODO: remove in a futur version
			mySettings.oldVersion(SETTINGSFILE)
			os.unlink(SETTINGSFILE)
		
		self.gameList = GameList.GameList(self.gladeHandler)
		self.gameList.captureDir = self.mySettings.settings['captureDir']
		self.gameList.populate( self.mySettings.settings['romsDir'])
	
		self.mainFrame = self.gladeHandler.get_widget('main')
		self.appBar = self.gladeHandler.get_widget('appbar1')
		self.preferences_dialog = self.gladeHandler.get_widget('preferences_dialog')
		self.binding_dialog = self.gladeHandler.get_widget('binding_dialog')

		if os.path.isfile(ICONFILE):
			#old version of python-gtk have not set_icon_from_file
			try:
				self.mainFrame.set_icon_from_file(ICONFILE)
				self.preferences_dialog.set_icon_from_file(ICONFILE)
				self.binding_dilaog.set_icon_from_file(ICONFILE)
			except AttributeError: pass

	def __del__(self):
		#remove the tmp conf file
		if os.path.isfile(self.mySettings.path): os.unlink(self.mySettings.path)


	def run(self):
		gtk.main()
			

	def on_about1_activate(self, imageMenuItem):
		pixbuf = gtk.gdk.pixbuf_new_from_file( os.path.join(DATADIR, LOGOFILE))
	        copyright = unicode(COPYRIGHT, "latin-1").encode("utf8")
	        gnome.ui.About(PROG_NAME, str(VERSION), copyright, COMMENTS, AUTHORS, logo_pixbuf=pixbuf).show()

	def on_quit1_activate(self, imageMenuItem):
		#exit from menu
		gtk.main_quit()
		
	def on_exit_activate(self, app, gdkEvent):
		#exit by clicking on the cross
		gtk.main_quit()

	def on_playGame_clicked(self, button):
		if self.gameList.theGame:
			self.playGame(self.gameList.theGame)
		else : 
			self.appBar.set_status('No game selected')
	
	def playGame(self, rom):
		if os.access(self.mySettings.settings['binary'], os.X_OK ):
			if rom:
				launch =  self.mySettings.settings['binary']
				if self.mySettings.settings['commandLineOptions']:
					launch += ' ' + self.mySettings.settings['commandLineOptions']
				launch += ' --config='+ self.mySettings.confFile()
				launch += ' "' + os.path.join(self.mySettings.settings['romsDir'], rom) + '" &'
				
				print launch
				self.appBar.set_status('playing ' + rom)
				os.system(launch)
			else : 
				self.appBar.set_status('No game selected')
		else :  
			self.appBar.set_status('Invalide path to VBA or not an executable, please fit it in preference')


	def on_reload_gamelist_activate(self, menuItem):
		self.gameList.populate(self.mySettings.settings['romsDir'])
	
	def on_search_changed(self, entry):
		tosearch = self.gladeHandler.get_widget('searchbox').get_text()
		self.gameList.populate(self.mySettings.settings['romsDir'],tosearch)

	def on_preferences_activate(self, imageMenuItem):
		self.preferences_dialog.show()
	
		#TODO: make the get_widget at the init
		for widg in ENTRY_WIDG:
			self.gladeHandler.get_widget(widg).set_text( self.mySettings.settings[widg])

		for widg in CHOOSE_WIDG:
			self.gladeHandler.get_widget(widg).set_history( int(self.mySettings.settings[widg]))

		for widg in CONTROL_WIDG:
		#TODO: centralize the conversion, etc
		#TODO: try to put the no button of the joystick
			tmp = int(self.mySettings.settings[widg], 16)
			try:
				key_gtk = key.sdl_to_gtk[tmp]
			except KeyError:
				key_gtk = tmp
			name = gtk.gdk.keyval_name(key_gtk)
			if not name: name = "Joystick"
			self.gladeHandler.get_widget(widg).set_text(name)
			
		#filter	
		fil = self.mySettings.settings['filter']
		if fil == 'A': fil = '10'
		elif fil == 'B': fil = '11'
		elif fil == 'C': fil = '12'
		self.gladeHandler.get_widget('filter').set_history(int(fil))
		
		#soundQuality
		snd = self.mySettings.settings['soundQuality']
		if snd == '1': snd=0
		elif snd == '2': snd=1
		elif snd == '4': snd=2
		self.gladeHandler.get_widget('soundQuality').set_history(snd)

		#soundEnable
		snd = self.mySettings.settings['soundEnable']
		if snd == '1': snd=0
		elif snd == '2': snd=1
		elif snd == '4': snd=2
		elif snd == '8': snd=3
		elif snd == '100': snd=4
		elif snd == '200': snd=5
		elif snd == '30f': snd=6
		elif snd == '0': snd=7
		self.gladeHandler.get_widget('soundEnable').set_history(snd)

		for widg in BOOL_WIDG:
			ok = True
			if self.mySettings.settings[widg] == '0': ok =False
			self.gladeHandler.get_widget(widg).set_active(ok)
		

	def on_preferences_close_button_clicked(self, button):
		for widg in ENTRY_WIDG:
			self.mySettings.settings[widg] = self.gladeHandler.get_widget(widg).get_text()

		for widg in CHOOSE_WIDG:
			self.mySettings.settings[widg] = `self.gladeHandler.get_widget(widg).get_history()`

			
		#filter	
		fil = `self.gladeHandler.get_widget('filter').get_history()`
		if fil == '10': fil = 'A'
		elif fil == '11': fil = 'B'
		elif fil == '12': fil = 'C'
		self.mySettings.settings['filter'] = fil
		
		#soundQuality
		snd = self.gladeHandler.get_widget('soundQuality').get_history()
		if snd == 0: snd='1'
		elif snd == 1: snd='2'
		elif snd == 2: snd='4'
		self.mySettings.settings['soundQuality'] = snd

		#soundEnable
		snd = self.gladeHandler.get_widget('soundEnable').get_history()
		if snd == 0: snd='1'
		elif snd == 1: snd='2'
		elif snd == 2: snd='4'
		elif snd == 3: snd='8'
		elif snd == 4: snd='100'
		elif snd == 5: snd='200'
		elif snd == 6: snd='30f'
		elif snd == 7: snd='0'
		self.mySettings.settings['soundEnable'] = snd

		for widg in BOOL_WIDG:
			if(self.gladeHandler.get_widget(widg).get_active()): ok = '1'
			else: ok = '0'
			self.mySettings.settings[widg] = ok
		
	
		self.gameList.catpureDir = self.mySettings.settings['captureDir']
		
		#check if all is valid
		msg = self.mySettings.check()
		if msg: popupError(msg)
		else:
			self.gladeHandler.get_widget("preferences_dialog").hide()
			self.mySettings.writeGConf()
			self.appBar.set_status('settings saved')
			self.gameList.populate(self.mySettings.settings['romsDir'])

	def on_import_activate(self, imageMenuItem):
		fs = gtk.FileSelection('Choose the file to import')
		result = fs.run()
		fs.hide()
		path = fs.get_filename()
		if result == gtk.RESPONSE_OK:
			try:
				self.mySettings.readFile(path)
			except "GBAError", msg:
				popupError(msg)
		self.mySettings.writeGConf()

	def on_export_activate(self, imageMenuItem):
		fs = gtk.FileSelection('Choose the export directory')
		result = fs.run()
		fs.hide()
		if result == gtk.RESPONSE_OK: 
			path = fs.get_filename()
			if os.path.isdir(path): path = os.path.join(path, 'VisualBoyAdvance.cfg')
			self.mySettings.writeFile(path)

	def on_configure_control_clicked(self, button):
		entry = button.get_parent().get_children()[0]

		if self.joy: 
			res_sdl = self.joy.get_binding()
			try:
				res_gtk = int(key.sdl_to_gtk[res_sdl])
			except KeyError:
				res_gtk = int(res_sdl)
		else:
			res_gtk = self.binding_dialog.run()
			self.binding_dialog.hide()
			if res_gtk not in (-4, 65307):  #-4: close the window, 65307: ESC
				try:
					res_sdl = key.gtk_to_sdl[res_gtk]
				except KeyError:
					res_sdl = res_gtk
				#print "name", gtk.gdk.keyval_name(res)
				#entry.set_text("%04x" % res_sdl)
			else: res_sdl = None
		if res_sdl: #not escape or close the window
			if not res_sdl in key.sdl_refused:
			#TODO: inform the user that this key is refused
				name = gtk.gdk.keyval_name(res_gtk)
				if not name: name = "Joystick"
				#TODO: make a test to see if it's really the joystick
				#TODO: try to put the no button of the joystick
				
				entry.set_text(name)
				set_key = entry.get_name()
				self.mySettings.settings[set_key] = "%04x" % res_sdl

	def on_binding_press_event(self, dialog, event):
		self.binding_dialog.response(event.keyval)

	def on_joy_enable_toggled(self, button):
		if button.get_active():
			try: import Joystick
			except ImportError:
				popupError("You must have pygame installed to use Joystick support.\nThen restart GnomeBoyAdvance")
				button.set_active(False)
				button.set_sensitive(False)
				return
			self.joy = Joystick.Joystick(ICONFILE)
			label = button.get_label() + " (%d joystick detected)" % self.joy.nbJoy
			button.set_label(label)
		else:
			button.set_label("Enable joystick support")
			#TODO: it's dirty. This info is also in the glade file. Correct this!
			self.joy = None
		
	def on_game_double_click(self, treeView, path, treeViewColumn):
		
		model = treeView.get_model()
		iter = model.get_iter(path)
		rom =model.get_value(iter,0)
		self.playGame(rom)
		
#not callback
def popupError(msg):
	pop = gtk.MessageDialog(type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_CLOSE, message_format=msg)
	pop.run()
	pop.destroy()
	
if __name__ == "__main__":
	gba = GnomeBoyAdvance()
	gba.run()
