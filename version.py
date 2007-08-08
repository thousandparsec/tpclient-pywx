
version = (0, 2, 99)

import os.path
if os.path.exists(".git"):
	if version[2] >= 99:
		version_target = (version[0], version[1]+1, 0)
	else:
		version_target = (version[0], version[1],   version[2]+1)

if __name__ == "__main__":
	if os.path.exists(".git"):
		print '%i.%i.%i+%i.%i.%i' % (version+version_target)
	else:
		print '%i.%i.%i' % version
