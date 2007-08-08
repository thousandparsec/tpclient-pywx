
version = (0, 3, 0)
if version[2] == 0:
	version_dev = (version[0], version[1]-1, 99)
else:
	version_dev = (version[0], version[1], version[2]-1)
