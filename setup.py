#!/usr/bin/env python

import os
import os.path

import glob

from distutils.core import setup
try:
	import py2exe

	from py2exe.build_exe import py2exe as build_exe
	class new_py2exe(build_exe): 
		def create(self, pathname=os.path.join("dist", "pywx-client.iss")):
			self.pathname = pathname
			self.file = open(pathname, "w")
			self.file.write("; WARNING: This script has been created by py2exe. Changes to this script\n")
			self.file.write("; will be overwritten the next time py2exe is run!\n")
			self.file.write("[Setup]\n")
	
except ImportError:
	class new_py2exe:
		pass

from __init__ import version
version = "%s.%s.%s" % version

if os.path.exists('CVS'):
	base = ['LICENSE', 'COPYING']
	for file in base:
		if os.path.exists(file):
			os.unlink(file)
		print "Getting %s" % file
		if hasattr(os, "link"):
			os.link(os.path.join('..', file), file)
		else:
			import shutil
			shutil.copy(os.path.join('..', file), file)

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
	cmdclass = {"py2exe": new_py2exe}, 
	options = {"py2exe": { "dll_excludes": ["wxbase251h_net_vc.dll"] }}, 
)
