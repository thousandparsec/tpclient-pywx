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

if len(sys.argv) > 1 and sys.argv[1].startswith("--media"):
	media_type = sys.argv[1].split('=')[-1].lower()
	del sys.argv[1]
else:
	media_type = "small"

try:
	media_files = {}
	for file in file("MEDIA-%s" % media_type.upper(), 'r').readlines():
		file = file.strip()
		dir = os.path.dirname(file)

		if not media_files.has_key(dir):
			media_files[dir] = []

		media_files[dir].append(file)
	media_files = media_files.items()
except IOError:
	print "Unable to find the required (%s) media list." % media_type
	sys.exit()

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
	data_files=[(".",			("LICENSE", "COPYING", "README")),
				("doc",			("doc/tips.txt",)),
				("graphics",	glob.glob("graphics/*.png")),
				("graphics",	glob.glob("graphics/*.ico")),
	] + media_files,
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

