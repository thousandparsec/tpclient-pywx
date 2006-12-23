# This file checks you have installed the requirements for tpclient-pywx 
# It can be run as standalone but is also run by the client at startup

notfound = []

from types import StringTypes
def cmp(ver1, ver2):
	if type(ver2) in StringTypes:
		ver2 = [int(x) for x in ver2.split('.')]
	ver2 = [int(x) for x in ver2]

	for a, b in zip(ver1, ver2):
		if a <= b:
			continue
		return False
	return True

def tostr(ver1):
	s = ""
	for a in ver1:
		s += "."+str(a)
	return s[1:]

try:
	import numarray
except ImportError:
	notfound.append("numarray")

wx_version = (2, 6, 0, 0)
try:
	import wx

	if not cmp(wx_version, wx.__version__.split('.')):
		raise ImportError("wxPython was too old")
except (ImportError, KeyError), e:
	print e
	notfound.append("wxPython > 2.6.0")

netlib_version = (0, 2, 1)
try:
	import tp.netlib
	print "Thousand Parsec Protocol Library Version", tp.netlib.__version__
	if not cmp(netlib_version, tp.netlib.__version__):
		raise ImportError("Thousand Parsec Network Library (libtpproto-py) is to old")

except (ImportError, KeyError), e:
	print e
	notfound.append("tp.netlib > " + tostr(netlib_version))

client_version = (0, 3, 0)
try:
	import tp.client
	print "Thousand Parsec Client Library Version", tp.client.__version__
	if not cmp(client_version, tp.client.__version__):
		raise ImportError("Thousand Parsec Client Library (libtpclient-py) is to old")
except (ImportError, KeyError), e:
	print e
	notfound.append("tp.client > " + tostr(client_version))

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
