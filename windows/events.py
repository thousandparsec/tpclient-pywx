"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

wxEVT_WINDOWS_OBJ_SELECT = wxNewEventType()

def EVT_WINDOWS_OBJ_SELECT(win, func):
	win.Connect(-1, -1, wxEVT_WINDOWS_OBJ_SELECT, func)

def UNEVT_WINDOWS_OBJ_SELECT(win, func):
	win.Disconnect(-1, wxEVT_WINDOWS_OBJ_SELECT, -1)

class WindowsObjSelect(wxPyEvent):
	def __init__(self, id):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_WINDOWS_OBJ_SELECT)
		
		self.value = id

