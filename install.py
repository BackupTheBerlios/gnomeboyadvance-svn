#!/usr/bin/python
import os

prefix = '/usr/'

if not os.path.exists(dataDir):
	print 'making ' + dataDir
	os.mkdir(dataDir)

if not os.path.exists(installDir):
	# really!
	os.mkdir(installDir)

os.system('install -m 755 src/gnomeboyadvance ' + prefix + 'bin/')
os.system('install -m 644 src/gnomeboyadvance.glade ' + prefix + 'share/gnomeboyadvance/')
os.system('install -m 644 data/gba48.png ' + prefix + 'share/pixmaps/')
os.system('install -m 644 data/gnomeboyadvance.application ' + prefix + 'share/applications/')
os.system('install -m 644 data/gnomeboyadvance.png ' + prefix + 'share/gnomeboyadvance/')

print 'gnomeboyadvance has been installed, happy gaming.'
