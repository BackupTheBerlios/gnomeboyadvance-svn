#!/usr/bin/python
import os

prefix = '/usr'

dataDir = os.path.join(prefix, 'share', 'gnomeboyadvance')
installDir = os.path.join(prefix, 'bin')

if not os.path.exists(dataDir):
	print 'making ' + dataDir
	os.mkdir(dataDir)

if not os.path.exists(installDir):
	# really!
	os.mkdir(installDir)
#Generate gconf info
os.system('gconftool-2 --install-schema-file data/gnomeboyadvance.schemas')

os.system('install -m 755 src/gnomeboyadvance ' + installDir)
os.system('install -m 644 src/gnomeboyadvance.glade ' + dataDir)
os.system('install -m 644 data/gba48.png ' + '/usr/share/pixmaps')
os.system('install -m 644 data/gnomeboyadvance.desktop ' + '/usr/share/applications')
os.system('install -m 644 data/gnomeboyadvance.png ' + dataDir)

print 'gnomeboyadvance has been installed, happy gaming.'
