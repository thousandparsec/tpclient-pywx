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
	
