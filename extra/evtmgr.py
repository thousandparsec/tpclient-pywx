"""\
This module allow the usage of evtmgr even with wxPython 2.3
"""
try:
	from wxPython.lib.evtmgr import *
except ImportError:
	from wx._evtmgr import *
