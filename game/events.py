"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

wxEVT_GAME_GETOBJ = wxNewEventType()
wxEVT_GAME_ARRIVEOBJ = wxNewEventType()
wxEVT_GAME_GETORDER = wxNewEventType()
wxEVT_GAME_ARRIVEORDER = wxNewEventType()

def EVT_GAME_GETOBJ(win, func):
	win.Connect(-1, -1, wxEVT_GAME_GETOBJ, func)

def UNEVT_GAME_GETOBJ(win, func):
	win.Disconnect(-1, wxEVT_GAME_GETOBJ, -1)

def EVT_GAME_ARRIVEOBJ(win, func):
	win.Connect(-1, -1, wxEVT_GAME_ARRIVEOBJ, func)

def UNEVT_GAME_ARRIVEOBJ(win, func):
	win.Disconnect(-1, wxEVT_GAME_ARRIVEOBJ, -1)

def EVT_GAME_GETORDER(win, func):
	win.Connect(-1, -1, wxEVT_GAME_GETORDER, func)

def UNEVT_GAME_GETORDER(win, func):
	win.Disconnect(-1, wxEVT_GAME_GETORDER, -1)
	
class GameObjectGetEvent(wxPyEvent):
	def __init__(self, id, name):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_GETOBJ)
		
		self.id = id
		self.name = name

class GameArriveObjectEvent(wxPyEvent):
	def __init__(self, id, name):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_ARRIVEOBJ)
		
		self.id = id
		self.name = name

		
