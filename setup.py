#!/usr/bin/env python
'''
	To use this setup script to install GnomeBoyAdvance:

			python setup.py install

'''

from distutils.core import setup

from src.const import VERSION, COMMENTS

DISTUTILS_DEBUG = 1	#TODO: remove for release

setup(	name		= 'gnomeboyadvance',
      	version		= VERSION,
	description	= COMMENTS,
	author		= 'Guillaume Desmottes',
	author_email	= 'cass@skynet.be',
	url		= 'http://developer.berlios.de/projects/gnomeboyadvance/',
	license		= 'GPL',
	data_files	= [	('share/gnomeboyadvance', ['glade/gnomeboyadvance.glade', 'data/gnomeboyadvance.png']),
      				('share/applications', ['data/gnomeboyadvance.desktop']),
				('share/pixmaps', ['data/gba48.png']),
				('share/gconf/schemas', ['data/gnomeboyadvance.schemas'])
			],
      	packages	= ['gnomeboyadvance'],
	package_dir	= {'gnomeboyadvance' : 'src'},
	scripts		= ['gnomeboyadvance']
      )
