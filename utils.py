"""\
This file contains useful utilities for useage in the program.
"""

import sys, string, traceback

lasts = {}

def do_traceback():
	global lasts
	
	type, val, tb = sys.exc_info()
	sys.stderr.write(string.join(traceback.format_exception(type, val, tb), ''))
	lasts = (type, val, tb)

DEBUG_NETWORK = 0
DEBUG_MAIN = 1
DEBUG_WINDOWS = 2

DEBUGGING = [DEBUG_NETWORK, DEBUG_MAIN, DEBUG_WINDOWS]

def debug(id, string):

	if id in DEBUGGING:
		print string


