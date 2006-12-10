#!/usr/bin/env python

import shutil
import sys

import glob
import os.path

from setuptools import setup

from version import version
version = ("%s.%s.%s" % version) 
print "Version is %s" % version

arguments = dict(
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
				("graphics",	glob.glob("graphics/*.gif")),
				("graphics",	glob.glob("graphics/*.png")),
				("graphics",	glob.glob("graphics/*.ico"))],
)

if sys.platform == 'darwin':
	import py2app

	from setuptools import find_packages
	print find_packages()

	arguments['scripts']=["tpclient-pywx.py"]
	
	# Py2App stuff
	extra_arguments = dict(
		app=["tpclient-pywx.py"],
		options = { 
			"py2app": {
				"argv_emulation": True,
				"compressed" : True,
				"strip"		: False,
				"optimize"	: 2,
				"packages"	: find_packages(),
				"includes"	: [],
				"excludes"	: ['Tkconstants', 'Tkinter', 'tcl', 'pydoc',],
				"resources"	: arguments['data_files'],
				"iconfile"	: "graphics/tp.icns",
				"plist"		: {
					"CFBundleSignature": "tppy",
					"CFBundleIdentifier": "net.thousandparsec.client.python.wx",
					"CSResourcesFileMapped": True,
					"CFBundleIconFile":	"tp.icns",
					"CFBundleGetInfoString": "Thousand Parsec wxPython Client %s" % version, 
					"CFBundleName": "tpclient-pywx",
					"CFBundleShortVersion": version,
					"CFBundleURLTypes": {
						"CFBundleTypeRole": "Viewer",
						"CFBundleURLIconFile": "tp.icns",
						"CFBundleURLName": "Thousand Parsec URI",
						"CFBundleURLSchemes": ["tp", "tps", "tp-http", "tp-https",],
					},
					"LSMinimumSystemVersion": "10.3.9",
#					"LSUIPresentationMode": 1,
				}
			}
		}
	)


elif sys.platform == 'win32':
	import py2exe

	if os.path.exists("dist"):
		shutil.rmtree("dist")
	bat = os.path.join("..", "scratchpad", "setup.bat")
	if os.path.exists(bat):
		os.system(bat)

	# Py2EXE stuff
	extra_arguments = dict(
		windows=[{
			"script": "tpclient-pywx",
			"icon_resources": [(1, "graphics/icon.ico")],
		}],
		options={
			"py2exe": { 
				"dll_excludes": [], 
				"packages": ["tp.netlib", "tp.client"], 
				"excludes": ["Tkconstants", "Tkinter", "tcl", "pydoc", "unittest"],
				"optimize": 2,
				"compressed": 0,
			}
		}, 
	)

arguments.update(extra_arguments)
setup(**arguments)
if sys.platform == 'darwin':
	if "py2app" in sys.argv:
		# Need to do some cleanup because the modulegraph is a bit brain dead
		base = os.path.join("dist", "tpclient-pywx.app", "Contents", "Resources", "lib", "python2.4")
		for i in (
				"netlib", "objects", "ObjectExtra", "OrderExtra", "support",
				"client", "pyscheme",
				):
			p = os.path.join(base, i)
			if os.path.exists(p):
				print "Removing", p
				shutil.rmtree(p)

	# Create a package
	dmg = os.path.join("dist", "tpclient-pywx_%s.dmg" % version)
	if os.path.exists(dmg):
		os.unlink(dmg)

	print "Creating dmg package"
	os.system("hdiutil create -imagekey zlib-level=9 -srcfolder dist/tpclient-pywx.app %s" % dmg)
elif sys.platform == 'win32':
	# Repack the library.zip file
	os.system(os.path.join("..", "scratchpad", "repack.bat"))
	
	# We should now use upx on the executables to make em smaller.
	os.system("upx --best .\dist\*.pyd")
	os.system("upx --best .\dist\*.dll")
	os.system("upx --best .\dist\*.exe")

	# Should generate the setup.nsi now.

	# Should run NSIS now.
