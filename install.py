#!/usr/bin/python
import os

prefix = '/usr'

dataDir = os.path.join(prefix, 'share', 'gnomeboyadvance')
installDir = os.path.join(prefix, 'bin')
libDir = os.path.join(prefix, 'lib', 'gnomeboyadvance')

LIBS = ['Settings.py', 'Joystick.py']

for dir in [dataDir, installDir, libDir]:
	if not os.path.exists(dir):
		print 'making ' + dir
		os.mkdir(dir)

#Generate gconf info
os.system('GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule data/gnomeboyadvance.schemas')
 

os.system('install -m 755 src/gnomeboyadvance ' + installDir)
os.system('install -m 644 src/gnomeboyadvance.glade ' + dataDir)
os.system('install -m 644 data/gba48.png /usr/share/pixmaps')
os.system('install -m 644 data/gnomeboyadvance.desktop /usr/share/applications')
os.system('install -m 644 data/gnomeboyadvance.png ' + dataDir)

for lib in LIBS:
	libPath = os.path.join('src', lib)
	os.system('install -m 644 ' + libPath + ' ' + libDir)

print 'gnomeboyadvance has been installed, happy gaming.'
