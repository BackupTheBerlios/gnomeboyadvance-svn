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

os.popen('cp gnomeboyadvance.glade ' + dataDir)
os.popen('cp gnomeBoyAdvance.png ' + dataDir)
os.popen('cp gnomeboyadvance ' + installDir)
print 'gnomeboyadvance has been installed, happy gaming.'
