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

if sys.platform.startswith('linux') and "install" in sys.argv:
	import os, shutil

	# Clean up locally
	os.system('rm `find -name \*.pyc`')

	def makedirs(s):
		try:
			os.makedirs(s)
		except OSError, e:
			if e.errno != 17:
				raise
		return

	prefix = "/usr/local"
	if "--prefix" in sys.argv:
		prefix = sys.argv[sys.argv.index('--prefix')+1]
	for arg in sys.argv:
		if arg.startswith('--prefix='):
			trash, prefix = arg.split('=')

	print "Installing too...", prefix

	# Documentation goes to
	docpath  = os.path.join(prefix, "share/doc/tpclient-pywx")
	print 'docpath', docpath
	makedirs(docpath)

	docfiles = ['AUTHORS', 'COPYING', 'LICENSE', 'doc/tips.txt']
	for file in docfiles:
		shutil.copy2(file, docpath)

	# Locale files
	localepath = os.path.join(prefix, "share/locale/%s/LC_MESSAGES/")
	print 'localepath', localepath
	for dir in os.listdir('locale'):
		if os.path.isfile(os.path.join('locale', dir)):
			continue
		print "Installing language files for %s" % dir

		llocalepath = localepath % dir
		makedirs(llocalepath)
		shutil.copy2(os.path.join('locale', dir, 'tpclient-pywx.mo'), llocalepath)

	# Graphics files
	graphicspath = os.path.join(prefix, "share/tpclient-pywx")
	print 'graphicspath', graphicspath
	shutil.copytree('graphics', graphicspath)

	# Private python file
	privatepath = os.path.join(prefix, "lib/tpclient-pywx/")
	print 'librarypath', privatepath
	makedirs(privatepath)

	privatefiles = ['tpclient-pywx', 'version.py', 'requirements.py', 'utils.py', 'windows', 'extra']
	for file in privatefiles:
		if os.path.isfile(file):
			shutil.copy2(file, privatepath)
		if os.path.isdir(file):
			shutil.copytree(file, os.path.join(privatepath, file))

	#os.symlink(os.path.join(os.path.abspath(os.curdir), 'tp'), os.path.join(privatepath, 'tp'))

	# Cleanup some files which shouldn't have been copied...
	cleanupfiles = ['windows/xrc/generate.sh', 'windows/xrc/tp.pjd', 'windows/xrc/tp.xrc']
	for file in cleanupfiles:
		os.unlink(os.path.join(privatepath, file))

	# Copy the startup script
	shutil.copy2(os.path.join('doc', 'tp-pywx-installed'), os.path.join(privatepath, 'tp-pywx-installed'))

	# Executables
	binpath     = os.path.join(prefix, "bin")
	print 'binpath', binpath
	makedirs(binpath)
	os.symlink(os.path.join(privatepath, 'tp-pywx-installed'), os.path.join(binpath, 'tpclient-pywx'))

	sys.exit()

if not "py2app" in sys.argv and not "py2exe" in sys.argv:
	print "This file is only provided to do the following,   (python setup.py py2exe)"
	print "  producing py2exe executable bundles for windows (python setup.py py2app)"
	print "  producing py2app dmg packages for Mac OS X      (python setup.py install)"
	print "  installing (a release) on a unix system"
	if os.path.exists(".git"):
		print
		print "WARNING!!"
		print " You seem to be running a git checkout (hence you don't want to be running this file)."
		print " tpclient-pywx can be run straight from this directory by just typing:"
		print "  ./tpclient-pywx"

	sys.exit()

if sys.platform == 'darwin':
	import py2app

	from setuptools import find_packages
	print find_packages()

	os.copy('tpclient-pywx', 'tpclient-pywx.py')
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
else:
	print "You shouldn't be running this (as it's only for Mac or Windows maintainers).."
	sys.exit()

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
	dmg = "tpclient-pywx_%s.dmg" % version
	if os.path.exists(dmg):
		os.unlink(dmg)

	print "Creating dmg package"
	os.system("cd doc/mac/; chmod a+x pkg-dmg make-diskimage; ./make-diskimage ../../%s  ../../dist tpclient-pywx -null- dstore background.jpg" % dmg)
elif sys.platform == 'win32':
	# Check that gdi.dll exists, some windows need it
	if not os.path.exists(os.path.join("dist", "gdiplus.dll")):
		raise IOError("gdiplus.dll doesn't exist! Copy it to dist!")

	# Repack the library.zip file
	os.system(os.path.join("..", "scratchpad", "repack.bat"))
	
	# We should now use upx on the executables to make em smaller.
	os.system("upx --best .\dist\*.pyd")
	os.system("upx --best .\dist\*.dll")
	os.system("upx --best .\dist\*.exe")

	# Should generate the setup.nsi now.

	# Should run NSIS now.
