# This file checks you have installed the requirements for tpclient-pywx 
# It can be run as standalone but is also run by the client at startup

notfound = []

print __file__

try:
	import numarray
except ImportError:
	notfound.append("numarray")

import string
try:
	import wxPython
	
	version = string.split(wxPython.__version__, '.')
	intversion = int(version[0])*1000000+int(version[1])*10000+int(version[2])*100
except ImportError, e:
	print e
	intversion = 0

if intversion < 2060000:
	notfound.append("wxPython > 2.6.0")

try:
	import tp.netlib
except ImportError, e:
	print e
	notfound.append("tp.netlib")

try:
	import tp.client
except ImportError, e:
	print e
	notfound.append("tp.client")

import __builtin__
try:
	import gettext
	
	gettext.install("pywx-client")
	__builtin__._ = gettext.gettext	
except ImportError:
	def _(s):
		return s
	__builtin__._ = _


try:
	import Image
except ImportError, e:
	print e
	print "It is highly recommended to install the PIL library, speed will be greatly improved."

if len(notfound) > 0:
	print "The following requirements where not met"
	for module in notfound:
		print notfound

	import sys
	sys.exit(1)
