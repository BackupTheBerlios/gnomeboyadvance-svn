#!/usr/bin/python
import os

installDir = '/usr/bin'
dataDir = '/usr/share/gnomeboyadvance'

if not os.path.exists(dataDir):
	print 'making ' + dataDir
	os.mkdir(dataDir)

if not os.path.exists(installDir):
	# really!
	os.mkdir(installDir)

os.system('cp src/gnomeboyadvance.glade ' + dataDir)
os.system('cp pixmaps/gnomeBoyAdvance.png ' + dataDir)
os.system('cp src/gnomeboyadvance ' + installDir)
os.system('cp pixmaps/gba_icon.png ' + dataDir)
print 'gnomeboyadvance has been installed, happy gaming.'
