
version = (0, 2, 99)

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

	version_git = p.read().strip()

	# What version are we trying to get too?
	import time
	if version[2] >= 99:
		version_target = (version[0], version[1]+1, 0, time.strftime('%Y%m%d'))
	else:
		version_target = (version[0], version[1], version[2]+1, time.strftime('%Y%m%d'))

	version_target_str = "%i.%i.%i.%s" % version_target

version_str = "%i.%i.%i" % version[:3]

if __name__ == "__main__":
	if os.path.exists(".git"):
		print version_str+'+'+version_target_str, "(git %s)" % version_git
	else:
		print version_str
