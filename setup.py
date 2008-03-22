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
		'windows.main',
		'windows.main.overlays',
		'windows.xrc',
		'extra',
		'extra.wxFloatCanvas',
		'extra.wxFloatCanvas.Utilities',
		],
	data_files=[(".",			("LICENSE", "README")),
				("doc",			("doc/tips.txt","COPYING")),
				("windows/xrc",	glob.glob("windows/xrc/*.xrc")),
				("graphics",	glob.glob("graphics/*.mpg")),
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
	temp   = None

	if "--prefix" in sys.argv:
		prefix = sys.argv[sys.argv.index('--prefix')+1]
	if "--temp" in sys.argv:
		temp = sys.argv[sys.argv.index('--temp')+1]
	for arg in sys.argv:
		if arg.startswith('--prefix='):
			trash, prefix = arg.split('=')
		elif arg.startswith('--temp='):
			trash, temp = arg.split('=')

	include_support = "--include-support" in sys.argv

	# If temp was not set, it should just be the prefix
	if temp is None:
		temp = prefix

	print "Installing to...", temp
	print "Target     is...", prefix

	# Documentation goes to
	#########################################################################
	docpath_temp  = os.path.join(temp,   "share/doc/tpclient-pywx")
	docpath       = os.path.join(prefix, "share/doc/tpclient-pywx")
	print 'docpath', docpath, "(copying to %s)" % docpath_temp

	makedirs(docpath_temp)
	docfiles = ['AUTHORS', 'COPYING', 'LICENSE', 'doc/tips.txt']
	for file in docfiles:
		shutil.copy2(file, docpath_temp)

	# Locale files
	#########################################################################
	localepath_temp = os.path.join(temp,   "share/locale/%s/LC_MESSAGES/")
	localepath      = os.path.join(prefix, "share/locale/%s/LC_MESSAGES/")
	print 'localepath', localepath, "(copying to %s)" % localepath_temp

	for dir in os.listdir('locale'):
		if os.path.isfile(os.path.join('locale', dir)):
			continue
		print "Installing language files for %s" % dir

		llocalepath = localepath_temp % dir
		makedirs(llocalepath)
		shutil.copy2(os.path.join('locale', dir, 'tpclient-pywx.mo'), llocalepath)

	# Graphics files
	#########################################################################
	graphicspath_temp = os.path.join(temp,   "share/tpclient-pywx/graphics")
	graphicspath      = os.path.join(prefix, "share/tpclient-pywx/graphics") 
	print 'graphicspath', graphicspath, "(copying to %s)" % graphicspath_temp

	if os.path.exists(graphicspath_temp):
		shutil.rmtree(graphicspath_temp)
	shutil.copytree('graphics', graphicspath_temp)

	# Private python file
	#########################################################################
	codepath_temp = os.path.join(temp,   "share/tpclient-pywx")
	codepath      = os.path.join(prefix, "share/tpclient-pywx")
	print 'librarypath', codepath, "(copying to %s)" % codepath_temp

	try:
		makedirs(codepath_temp)
	except OSError:
		pass

	privatefiles = ['tpclient-pywx', 'version.py', 'requirements.py', 'utils.py', 'windows', 'extra']
	for file in privatefiles:
		if os.path.isfile(file):
			shutil.copy2(file, codepath_temp)
		if os.path.isdir(file):
			p = os.path.join(codepath_temp, file)
			if os.path.exists(p):
				shutil.rmtree(p)
			shutil.copytree(file, p)

	# Fix the version path
	os.system('python version.py --fix > %s' % os.path.join(codepath_temp, 'version.py'))

	# Cleanup some files which shouldn't have been copied...
	cleanupfiles = ['windows/xrc/generate.sh', 'windows/xrc/tp.pjd', 'windows/xrc/tp.xrc']
	for file in cleanupfiles:
		os.unlink(os.path.join(codepath_temp, file))

	# Create the startup script
	tpin = open(os.path.join('doc', 'tp-pywx-installed'), 'rb').read()
	tpin = tpin.replace("$$CODEPATH$$",     codepath)
	tpin = tpin.replace("$$GRAPHICSPATH$$", graphicspath)
	tpin = tpin.replace("$$DOCPATH$$",      docpath)

	tpout = open(os.path.join(codepath_temp, 'tp-pywx-installed'), 'wb')
	tpout.write(tpin)
	tpout.close()
	os.chmod(os.path.join(codepath_temp, 'tp-pywx-installed'), 0755)


	# Executables
	binpath_temp = os.path.join(temp,   "bin")
	binpath      = os.path.join(prefix, "bin")

	print 'binpath', binpath, "(copying to %s)" % binpath_temp
	makedirs(binpath_temp)
	
	binp = os.path.join(binpath_temp, 'tpclient-pywx')
	if os.path.exists(binp):
		os.unlink(binp)
	os.symlink(os.path.join(codepath, 'tp-pywx-installed'), binp)

	print "Client installed!"

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

	# Fix the version path
	os.system('python version.py --fix > %s' % 'version.py')

	shutil.copy('tpclient-pywx', 'tpclient-pywx.py')

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
				"excludes"	: ['Tkconstants', 'Tkinter', 'tcl', 'pydoc', 
					'numpy.numarray', 'numpy.oldnumeric',
					'numpy.distutils', 'numpy.doc', 'numpy.f2py', 'numpy.fft', 'numpy.lib.tests', 'numpy.testing'],
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
				"excludes": ["Tkconstants", "Tkinter", "tcl", "pydoc" ],
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
		base = os.path.join("dist", "tpclient-pywx.app", "Contents", "Resources", "lib", "python2.5")
		for i in (
				"xrc", "main", "overlays", "wxFloatCanvas", "Utilities", # local excesses
				"netlib", "objects", "ObjectExtra", "OrderExtra", "support", "discover", "pyZeroconf",  # tp.netlib
				"client", "pyscheme", "discover", # tp.client
				):
			p = os.path.join(base, i)
			if os.path.exists(p):
				print "Removing", p
				shutil.rmtree(p)

		# Need to clean up any .py$ files which got included for some unknown reason...
		# Need to clean up any .pyc$ when a .pyo$ exists too

	# Create a package
	dmg = "tpclient-pywx_%s.dmg" % version
	if os.path.exists(dmg):
		os.unlink(dmg)

	print "Creating dmg package"
	os.system("cd doc/mac/; chmod a+x pkg-dmg make-diskimage; ./make-diskimage ../../%s  ../../dist tpclient-pywx -null- dstore background.jpg" % dmg)
elif sys.platform == 'win32':
	# Copy in the manifest file for that "Windows XP look"
	shutil.copy("tpclient-pywx.exe.manifest", os.path.join("dist", "tpclient-pywx.exe.manifest"))

	# Check that gdi.dll exists, some windows need it
	import wx
	gdisrc = os.path.join(os.path.dirname(wx.__file__), "gdiplus.dll")
	if not os.path.exists(gdisrc):
		raise IOError("gdiplus.dll doesn't exist! Copy it to dist!")
	shutil.copy(gdisrc, os.path.join("dist", "gdiplus.dll"))

	# Repack the library.zip file
	os.system(os.path.join("..", "scratchpad", "repack.bat"))
	
	# We should now use upx on the executables to make em smaller.
	os.system("upx --best .\dist\*.pyd")
	os.system("upx --best .\dist\*.dll")
	os.system("upx --best .\dist\*.exe")

	# Should generate the setup.nsi now.

	# Should run NSIS now.
