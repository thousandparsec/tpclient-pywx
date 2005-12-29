#!/usr/bin/env python

import os
import os.path
import shutil

import glob

from distutils.core import setup
try:
	import py2exe

except ImportError:
	pass

from __init__ import version
version = "%s.%s.%s" % version

excludes = [\
	"Tkconstants","Tkinter","tcl", # TK/TCL
	"pydoc", "unittest"]

setup(
# Meta data
	name="tpclient-pywx",
	version=version,
	license="GPL",
	description="wxPython based client for Thousand Parsec",
	author="Tim Ansell",
	author_email="tim@thousandparsec.net",
	url="http://www.thousandparsec.net",
# Files to include
	windows=[{
		"script": "tpclient-pywx",
		"icon_resources": [(1, "graphics/icon.ico")],
	}],
	scripts=["tpclient-pywx"],
	packages=[ \
		'.',
		'windows',
		'extra',
		'extra.wxFloatCanvas',
		],
	data_files=[(".",			("LICENSE", "COPYING", "README")),
				("doc",			("doc/tips.txt",)),
				("graphics",	glob.glob("graphics/*.png")),
				("graphics",	glob.glob("graphics/*.ico")),
				("graphics/media/planet-small",		glob.glob("graphics/media/planet-small/*.jpg")),
				("graphics/media/star-small",		glob.glob("graphics/media/star-small/*.jpg")),
	],
# Py2EXE stuff
	options={"py2exe": { \
		"dll_excludes": [], \
		"excludes": excludes, \
		"packages": ["tp.netlib"], \
		"optimize": 2,
		"compressed": 0,
		}}, 
)

