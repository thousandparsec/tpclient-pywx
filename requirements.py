#! /usr/bin/env python

# This file checks you have installed the requirements for tpclient-pywx 
# It can be run as standalone but is also run by the client at startup

# Preference the local directory first...
import sys
sys.path.insert(0, '.')

import os.path

notfound    = []
recommended = []

# Try and figure out what type of system this computer is running.
import os
result = os.system('apt-get --version > /dev/null 2>&1') 
if result == 0:
	system = "debian-based"
else:
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

print "My information:"
print "---------------------------------------------------------------"
import version
try:
	print "My version", version.version_str+'+'+version.version_target_str, "(git %s)" % version.version_git
except AttributeError:
	print "My version", version.version_str
print "Running from ", os.path.dirname(os.path.join(os.path.abspath(__file__)))
print

print "Checking requirements:"
print "---------------------------------------------------------------"
try:
	import numpy
except ImportError:
	if system == "debian-based":
		notfound.append("python-numpy")
		notfound.append("python-numpy-ext")
	else:
		notfound.append("NumPy or SciPy")

wx_version = (2, 8, 0, 0)
wx_version_str = '.'.join([str(x) for x in wx_version[0:2]])
try:
	import wxversion
	if os.path.exists("wxversion"):
		wxversion.select(open("wxversion").read())
	else:
		wxversion.ensureMinimal(wx_version_str)
except ImportError, e:
	pass

try:
	import wx
	if not cmp(wx_version, wx.__version__.split('.')):
		raise ImportError("wxPython was too old")

	print "wxPython version is", wx.__version__
except (ImportError, KeyError), e:
	print e

	if system == "debian-based":
		notfound.append("python-wxgtk2.8")
	else:
		notfound.append("wxPython > " + wx_version_str)

import __builtin__
try:
	import gettext
	__builtin__._ = gettext.gettext	

	if True:
		import os
		import wx
		import gettext
		basepath = os.path.abspath(os.path.dirname(__file__))
		localedir = os.path.join(basepath, "locale")

		langid = wx.LANGUAGE_DEFAULT    # use OS default; or use LANGUAGE_JAPANESE, etc.
		domain = "tpclient-pywx"        # the translation file is tpclient-pywx.mo

		# Set locale for wxWidgets
		mylocale = wx.Locale(langid)
		mylocale.AddCatalogLookupPathPrefix(localedir)
		mylocale.AddCatalog(domain)

		# Set up Python's gettext
		print domain
		print localedir
		print mylocale.GetCanonicalName()

		mytranslation = gettext.translation(domain, localedir, [mylocale.GetCanonicalName()], fallback=True)
		mytranslation.install()

		import __builtin__
		__builtin__.__dict__['_'] = wx.GetTranslation

except ImportError, e:
	print e
	def _(s):
		return s
	__builtin__._ = _

	reason = "Without gettext support localisation will be disabled."
	if system == "debian-based":
		recommended.append(("Python gettext should come with Python, please check your python install", reason))
	else:
		recommended.append(("Python with gettext enabled.", reason))

try:
	import psyco
except ImportError, e:
	print e

	reason = "Installing pysco can give a 10-20% speed increase in starmap calculations. (Pysco is x86 only.)"
	if system == "debian-based":
		recommended.append(("python-psyco", reason))
	else:
		recommended.append(("Pysco JIT compiler.", reason))

try:
	try:
		import pyOpenSSL
	except ImportError, e:
		print e

		# Maybe it's using a different name
		import OpenSSL as pyOpenSSL
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

try:
	import pygame
except ImportError, e:
	print e
	reason = "Installing the Pygame library will allow you to see the intro movie and hear sounds."

	if system == "debian-based":
		recommended.append(("python-pygame", reason))
	else:
		recommended.append(("Pygame library.", reason))


netlib_version = (0, 2, 1)
try:
	import tp.netlib

	print "Thousand Parsec Protocol Library Version", tp.netlib.__version__ 
	try:
		print "    (installed at %s)" % tp.netlib.__installpath__
	except AttributeError:
		print "    (version to old to work out install path)"

	try:
		from tp.netlib.version import version_git
		print "    (git %s)" % version_git
	except ImportError:
		print

	if not cmp(netlib_version, tp.netlib.__version__):
		raise ImportError("Thousand Parsec Network Library (libtpproto-py) is to old")

except (ImportError, KeyError, AttributeError), e:
	print e
	notfound.append("tp.netlib > " + tostr(netlib_version))

client_version = (0, 2, 99)
try:
	import tp.client

	print "Thousand Parsec Client Library Version", tp.client.__version__
	try:
		print "    (installed at %s)" % tp.client.__installpath__
	except AttributeError:
		print "    (version to old to work out install path)"
	
	try:
		from tp.client.version import version_git
		print "    (git %s)" % version_git
	except ImportError:
		print

	if not cmp(client_version, tp.client.__version__):
		raise ImportError("Thousand Parsec Client Library (libtpclient-py) is to old")
except (ImportError, KeyError, AttributeError), e:
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
			#print location
			# Check the file is executable
			try:
				os.chmod(location, stat.S_IRUSR|stat.S_IWUSR|stat.S_IXUSR|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)
			except Exception, e:
				pass

			# Register the URL Handlers
			try:
				import gconf
				for prefix in ['tp', 'tps', 'tphttp', 'tphttps', 'tp+http', 'tp+https']:
					prefix = gconf.escape_key(prefix, len(prefix))
					gconf.client_get_default().set_string('/desktop/gnome/url-handlers/%s/command' % prefix, location)
					gconf.client_get_default().set_bool('/desktop/gnome/url-handlers/%s/enabled' % prefix, True)
			except ImportError, e:
				print e

				reason = "It is recommended that under gnome you have the Python Gconf module installed so I can register URL handlers."
				if system == "debian-based":
					recommended.append(("python-gconf", reason))
				else:
					recommended.append(("Recent version of pyGTK.", reason))

	print
	print "Checking locations:"
	print "---------------------------------------------------------------"
	import os
	try:
		graphicsdir = os.environ["TPCLIENT_GRAPHICS"]
	except KeyError:
		graphicsdir = 'graphics'
	print "Graphics are in %s" % graphicsdir
	if not os.path.exists(os.path.join(graphicsdir, 'blank.png')):
		print "Can not find graphics required by this client."
		sys.exit()

	try:
		docdir = os.environ["TPCLIENT_DOC"]
	except KeyError:
		docdir = 'doc'
	print "Documents are in %s" % docdir
	if not os.path.exists(os.path.join(docdir, 'tips.txt')):
		print "Can not find help documentation required by this client."
		sys.exit()

if len(notfound) > 0 or len(recommended) > 0:
	print
	print "Possible problems found:"
	print "---------------------------------------------------------------"

if len(notfound) > 0:
	print "The following requirements where not met:"
	for module in notfound:
		print '    ', module
	print

import os, pprint
try:
	COLS = int(os.environ["COLUMNS"])
except (KeyError, ValueError):
	try:
		import struct, fcntl, sys, termios
		COLS = struct.unpack('hh', fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))[1]
	except:
		COLS = 80

ALIGN = 25
if len(recommended) > 0:
	print "The following recommended modules where not found:"
	for module, reason in recommended:
		
		lines = [""]
		lines[-1] += '    %s,' % module
		lines[-1] += ' ' * (ALIGN-len(lines[-1]))

		for word in reason.split(" "):
			if (len(lines[-1]) + len(word) + 1) > COLS:
				lines.append(' '*ALIGN)

			lines[-1] += word + " "

		print
		print "\n".join(lines)

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

## FIXME: This is here to extra is imported very early on.
#import extra
