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

def link(a, b):
	if os.path.isdir(a):
		if hasattr(os, "symlink"):
			os.symlink(a, b)
		else:
			shutil.copytree(a, b)
	else:
		if hasattr(os, "symlink"):
			os.link(a, b)
		else:
			shutil.copy(a, b)

def unlink(a):
	if os.path.isdir(a) and not os.path.islink(a):
		shutil.rmtree(a)
	else:
		os.unlink(a)

if os.path.exists('CVS'):
	base = [ \
		(os.path.join('..', 'LICENSE'), 'LICENSE'),
		(os.path.join('..', 'COPYING'), 'COPYING'),
		(os.path.join('..', 'media'), os.path.join('graphics', 'media')),
	]

	for afile, bfile in base:
		afile, bfile = os.path.abspath(afile), os.path.abspath(bfile)
		try:
			unlink(bfile)
		except OSError, e:
			print e
		link(afile, bfile)

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
		"script": "main.py",
		"icon_resources": [(1, "graphics/icon.ico")],
	}],
	scripts=["main.py"],
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

