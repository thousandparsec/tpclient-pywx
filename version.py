
version = (0, 3, 0)

# Add the git version if in a git tree...
import os, os.path
__path__ = os.path.realpath(os.path.dirname(__file__))
installpath = __path__

# Get the git version this tree is based on
if os.path.exists(os.path.join(installpath, '.git')):
	# Read in git's 'HEAD' file which points to the correct reff to look at
	h = open(os.path.join(installpath, '.git', 'HEAD'))
	# Read in the ref
	ref = h.readline().strip().split(': ', 1)[1]
	# This file has the SHA1
	p = open(os.path.join(installpath, '.git', ref))
	del ref

	version_git = p.read().strip()

	# What version are we trying to get too?
	import time
	if version[2] >= 99:
		version_target = (version[0], version[1]+1, 0)
	else:
		version_target = (version[0], version[1], version[2]+1)

	version_target_str = "%i.%i.%i" % version_target

version_str = "%i.%i.%i" % version[:3]

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1 and sys.argv[1] == '--fix':
		print """
import os, os.path
__path__ = os.path.realpath(os.path.dirname(__file__))
installpath = os.path.split(os.path.split(__path__)[0])[0]
"""
		for value in dir():
			if value.startswith('__') or value in ('installpath',):
				continue
			if isinstance(eval(value), (tuple, str, unicode)):
				exec("print '%s =', repr(%s)" % (value, value))

		print """
try:
	print version_str+'+'+version_target_str, "(git %s)" % version_git, "(installed at %s)" % installpath
except (ValueError, NameError):
	print version_str, "(installed at %s)" % installpath
"""
		sys.exit(0)

	if os.path.exists(os.path.join(installpath, '.git')):
		print version_str+'+'+version_target_str, "(git %s)" % version_git, "(installed at %s)" % installpath
	else:
		print version_str, "(installed at %s)" % installpath
