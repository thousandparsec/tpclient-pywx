#!/usr/bin/env python

import os
import os.path
import shutil
import sys

import glob

from distutils.core import setup
try:
	import py2exe

except ImportError:
	pass

from __init__ import version
version = ("%s.%s.%s" % version) + "-" + media_type

print "Version is %s" % version

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
	scripts=["tpclient-pywx"],
	packages=[ \
		'.',
		'windows',
		'extra',
		'extra.wxFloatCanvas',
		],
	data_files=((".",			("LICENSE", "COPYING", "README")),
				("doc",			("doc/tips.txt",)),
				("graphics",	glob.glob("graphics/*.png")),
				("graphics",	glob.glob("graphics/*.ico"))),
# Py2EXE stuff
	windows=[{
		"script": "tpclient-pywx",
		"icon_resources": [(1, "graphics/icon.ico")],
	}],
	options={
		"py2exe": { 
			"dll_excludes": [], 
			"excludes": ["Tkconstants", "Tkinter", "tcl", "pydoc", "unittest"],
			"packages": ["tp.netlib"], 
			"optimize": 2,
			"compressed": 0,
		}
	}, 
)

