#!/usr/bin/env python

from distutils.core import setup
try:
	import py2exe
except ImportError:
	pass

import glob

from __init__ import version
version = "%s.%s.%s" % version

import os.path
import os

if os.path.exists('CVS'):
	base = ['LICENSE', 'COPYING']
	for file in base:
		if os.path.exists(file):
			os.unlink(file)
		print "Getting %s" % file
		os.link(os.path.join('..', file), file)
		
setup(
	name="pywx-client",
	version=version,
	license="GPL",
	description="wxPython based client for Thousand Parsec",
	author="Tim Ansell",
	author_email="tim@thousandparsec.net",
	url="http://www.thousandparsec.net",
	packages=[ \
		'.',
		'windows',
		'extra',
		'extra.wxFloatCanvas',
		],
	windows=["main.py"], scripts=["main.py"],
)

#	data_files=[("vars", 		glob.glob("vars/config")),
#				("graphics", 	glob.glob("graphics/*.png")),
#				("graphics/media/planet-small",	glob.glob("graphics/media/planet-small/*.png")),
#				("graphics/media/star-small",	glob.glob("graphics/media/star-small/*.png")),
#				],

