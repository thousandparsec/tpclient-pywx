"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

wxEVT_WINDOWS_SELECTOBJ = wxNewEventType()

def EVT_WINDOWS_SELECTOBJ(win, func):
	win.Connect(-1, -1, wxEVT_WINDOWS_SELECTOBJ, func)

def UNEVT_WINDOWS_SELECTOBJ(win, func):
	win.Disconnect(-1, wxEVT_WINDOWS_SELECTOBJ, -1)

class WindowsSelectObj(wxPyEvent):
	def __init__(self, id):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_WINDOWS_SELECTOBJ)
		
		self.value = id

