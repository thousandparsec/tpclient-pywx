# This file checks you have installed the requirements for tpclient-pywx 
# It can be run as standalone but is also run by the client at startup

notfound    = []
recommended = []

# Try and figure out what type of system this computer is running.
import os
result = os.system('apt-get --version > /dev/null 2>&1') 
if result == 0:
	system = "debian-based"
elif result == 32512:
	system = "unknown"

from types import StringTypes
import re
def cmp(ver1, ver2):
	if type(ver2) in StringTypes:
		ver2 = [int(x) for x in ver2.split('.')]

	ver2 = list(ver2)
	for i,x in enumerate(ver2):
		try:
			ver2[i] = int(x)
		except ValueError:
			# This means there could be a "pre" or "rc" something in the version
			# We will treat this version as the one before.
			ver2[i] = int(re.search('(\d+)', x).group())-1

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
	if system == "debian-based":
		notfound.append("python-numarray")
	else:
		notfound.append("numarray")

wx_version = (2, 6, 0, 0)
try:
	import wx

	if not cmp(wx_version, wx.__version__.split('.')):
		raise ImportError("wxPython was too old")
except (ImportError, KeyError), e:
	print e

	if system == "debian-based":
		notfound.append("python-wxgtk2.6")
	else:
		notfound.append("wxPython > 2.6.0")

import __builtin__
try:
	import gettext
	
	gettext.install("pywx-client")
	__builtin__._ = gettext.gettext	
except ImportError, e:
	print e
	def _(s):
		return s
	__builtin__._ = _

	reason = "Without gettext support localisation will be disabled."
	if system == "debian-based":
		recommended.append(("python-gettext", reason))
	else:
		recommended.append(("Python with gettext enabled.", reason))

try:
	import psyco
except ImportError, e:
	print e

	reason = "Installing pysco can give a 10-20% speed increase in starmap calculations."
	if system == "debian-based":
		recommended.append(("python-pysco", reason))
	else:
		recommended.append(("Pysco JIT compiler.", reason))

try:
	import pyOpenSSL
except ImportError, e:
	print e

	reason = "Installing pyOpenSSL allows the client to check if the host you are connecting to has a valid certificate."
	if system == "debian-based":
		recommended.append(("python-pyopenssl", reason))
	else:
		recommended.append(("pyOpenSSL", reason))


try:
	import Image
except ImportError, e:
	print e
	reason = "Installing the PIL library will increase speed of displaying graphics."

	if system == "debian-based":
		recommended.append(("python-imaging", reason))
	else:
		recommended.append(("Python Imaging library.", reason))

netlib_version = (0, 2, 1)
try:
	import tp.netlib
	print "Thousand Parsec Protocol Library Version", tp.netlib.__version__
	if not cmp(netlib_version, tp.netlib.__version__):
		raise ImportError("Thousand Parsec Network Library (libtpproto-py) is to old")

except (ImportError, KeyError), e:
	print e
	notfound.append("tp.netlib > " + tostr(netlib_version))

client_version = (0, 2, 1)
try:
	import tp.client
	print "Thousand Parsec Client Library Version", tp.client.__version__
	if not cmp(client_version, tp.client.__version__):
		raise ImportError("Thousand Parsec Client Library (libtpclient-py) is to old")
except (ImportError, KeyError), e:
	print e
	notfound.append("tp.client > " + tostr(client_version))

if len(notfound) == 0:
	import sys
	if sys.platform == 'linux2':
		import os.path, stat
		location = os.path.join(os.path.dirname(os.path.join(os.path.abspath(__file__))), "tpclient-pywx")
		if not os.path.exists(location):
			print "Hrm, unable to find tpclient-pywx are you running outside a tpclient-pywx tree?"
		else:
			print location
			# Check the file is executable
			os.chmod(location, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

			# Register the URL Handlers
			try:
				import gconf
				for prefix in ['tp', 'tps', 'tphttp', 'tphttps']:
					gconf.client_get_default().set_string('/desktop/gnome/url-handlers/%s/command' % prefix, location)
					gconf.client_get_default().set_bool('/desktop/gnome/url-handlers/%s/enabled' % prefix, True)
			except ImportError, e:
				print e

				reason = "It is recommended that under gnome you have the Python Gconf module installed so I can register URL handlers."
				if system == "debian-based":
					recommended.append(("python-gconf", reason))
				else:
					recommended.append(("Recent version of pyGTK.", reason))

	import os
	if os.environ.has_key("TPCLIENT_MEDIA"):
		graphics = os.environ["TPCLIENT_MEDIA"]
	else:
		graphics = '.'

if len(notfound) > 0:
	print
	print "The following requirements where not met:"
	for module in notfound:
		print '\t', module

if len(recommended) > 0:
	print
	print "The following recommended modules where not found:"
	for module, reason in recommended:
		if len(module+',') > 16:
			i = '\t'
		else:
			i = '\t\t'
		print '\t', module + ',', i, reason

# Check for an apt-get based system,
if system == "debian-based":
	notfound_debian = []
	for module in notfound:
		if module.find(' ') == -1:
			notfound_debian.append(module)
	if len(notfound_debian) > 0:
		print """
You may be able to install some of the requirements by running the following
command as root:

	apt-get install %s
""" % " ".join(notfound_debian)
	if len(recommended) > 0:
		print """
To install the modules recommended for full functionality, run the following
command as root:

	apt-get install %s
""" % " ".join(zip(*recommended)[0])


if len(notfound) > 0:
	import sys
	sys.exit(1)
