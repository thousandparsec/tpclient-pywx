"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

wxEVT_GAME_GETOBJ = wxNewEventType()
wxEVT_GAME_GETOBJDETAILS = wxNewEventType()
wxEVT_GAME_SENDORDER = wxNewEventType()

def EVT_GAME_GETOBJ(win, func):
	win.Connect(-1, -1, wxEVT_GAME_GETOBJ, func)

def UNEVT_NETWORK_PACKET(win, func):
	win.Disconnect(-1, wxEVT_GAME_GETOBJ, -1)

class GameGetObjectEvent(wxPyEvent):
	def __init__(self, id, name):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_GETOBJ)
		
		self.value = id
		self.name = name
	
