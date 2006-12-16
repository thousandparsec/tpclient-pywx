# This file checks you have installed the requirements for tpclient-pywx 
# It can be run as standalone but is also run by the client at startup

notfound = []

try:
	import numarray
except ImportError:
	notfound.append("numarray")

import string
try:
	import wx
	
	version = string.split(wx.__version__, '.')
	intversion = int(version[0])*1000000+int(version[1])*10000+int(version[2])*100
except (ImportError, KeyError), e:
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

import sys
if sys.platform == 'linux2':
	# Check the file is executable
	import os.path, stat
	location = os.path.join(os.path.dirname(os.path.join(os.path.abspath(__file__))), "tpclient-pywx")
	print location
	os.chmod(location, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

	# Register the URL Handlers
	try:
		import gconf
		for prefix in ['tp', 'tps', 'tphttp', 'tphttps']:
			gconf.client_get_default().set_string('/desktop/gnome/url-handlers/%s/command' % prefix, location)
			gconf.client_get_default().set_bool('/desktop/gnome/url-handlers/%s/enabled' % prefix, True)
	except ImportError, e:
		print e
		print "It is recommended that under gnome you have the python-gconf module installed so I can register URL handlers."

if len(notfound) > 0:
	print "The following requirements where not met"
	for module in notfound:
		print notfound

	import sys
	sys.exit(1)
