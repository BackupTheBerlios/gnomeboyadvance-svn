#!/usr/bin/env python
'''
	To use this setup script to install GnomeBoyAdvance:

			python setup.py install

'''

import sys
import os
from distutils.core import setup

from src.const import VERSION, COMMENTS

#DISTUTILS_DEBUG = 1

setup(	name		= 'gnomeboyadvance',
      	version		= VERSION,
	description	= COMMENTS,
	author		= 'Guillaume Desmottes',
	author_email	= 'gnomeboyadvance-devel@lists.berlios.de',
	url		= 'http://developer.berlios.de/projects/gnomeboyadvance/',
	license		= 'GPL',
	data_files	= [	('share/gnomeboyadvance', ['glade/gnomeboyadvance.glade', 'data/gnomeboyadvance.png']),
      		('share/applications', ['data/gnomeboyadvance.desktop']),
		('share/pixmaps', ['data/gba48.png']),
		('share/gconf/schemas', ['data/gnomeboyadvance.schemas']),
		('share/man/man1', ['data/gnomeboyadvance.1.gz'])
			],
      	packages	= ['gnomeboyadvance'],
	package_dir	= {'gnomeboyadvance' : 'src'},
	scripts		= ['gnomeboyadvance']
	)

#VERY bad but the doc of distutils sux!
#TODO: make this clean
try:
	if sys.argv[1] == "install": 
		os.system('GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source` gconftool-2 --makefile-install-rule data/gnomeboyadvance.schemas')
	
except IndexError: pass
