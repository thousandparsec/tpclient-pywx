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

DEBUG_NETWORK = "NETWORK:"
DEBUG_MAIN = "MAIN:"
DEBUG_WINDOWS = "WINDOWS:"
DEBUG_GAME = "GAME:"

DEBUGGING = [DEBUG_NETWORK, DEBUG_MAIN, DEBUG_WINDOWS, DEBUG_GAME]

def debug(id, string):

	if id in DEBUGGING:
		print id, string

__all__ = ['do_traceback', 'DEBUG_NETWORK', 'DEBUG_MAIN', 'DEBUG_WINDOWS', 'DEBUG_GAME', 'debug']
