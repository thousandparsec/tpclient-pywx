"""\
This file contains useful utilities for useage in the program.
"""

import pprint
import sys
import string
import traceback
import os
import os.path

try:
	import cPickle as pickle
except ImportError:
	import pickle

def do_traceback():
	type, val, tb = sys.exc_info()
	sys.stderr.write(string.join(traceback.format_exception(type, val, tb), ''))
	if hasattr(sys.stderr, "flush"):
		sys.stderr.flush()

DEBUG_NETWORK = "NETWORK:"
DEBUG_MAIN = "MAIN:"
DEBUG_GUI = "GUI:"

DEBUGGING = [DEBUG_MAIN, DEBUG_GUI, DEBUG_NETWORK]

def warn(string):
	print "WARNING:", string

def debug(id, *strings):
	if id in DEBUGGING:
		print id, 
		for s in strings:
			print s,
		print

class Blank:
	pass

def configpath():
	"""\
	Figures out where to save the preferences.
	"""
	dirs = [("APPDATA", "Thousand Parsec"), ("HOME", ".tp"), (".", "var")]
	for base, extra in dirs:
		if base in os.environ:
			base = os.environ[base]
		elif base != ".":
			continue
			
		rc = os.path.join(base, extra)
		if not os.path.exists(rc):
			os.mkdir(rc)
		return rc

cache = {}
def load_data(file):
	"""\
	Loads preference data from a file.
	"""
	try:
		f = open(os.path.join(configpath(), file), "r")
		data = pickle.load(f)
	except IOError:
		return None
	return data
	
def save_data(file, data):
	"""\
	Saves preference data to a file.
	"""
	f = open(os.path.join(configpath(), file), "w")
	pickle.dump(data, f)

__all__ = [
	'Blank', 'save_data', 'load_data', 'configpath', # Config functions
	'debug', 'do_traceback', 'DEBUG_NETWORK', 'DEBUG_MAIN', 'DEBUG_GUI', # Debugging functions
	]
