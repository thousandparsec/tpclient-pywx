"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

# Outgoing events
wxEVT_GAME_OBJ_ARRIVE = wxNewEventType()
wxEVT_GAME_ORDER_ARRIVE = wxNewEventType()

def EVT_GAME_OBJ_ARRIVE(win, func):
	win.Connect(-1, -1, wxEVT_GAME_OBJ_ARRIVE, func)

def UNEVT_GAME_OBJ_ARRIVE(win, func):
	win.Disconnect(-1, wxEVT_GAME_OBJ_ARRIVE, -1)
	
def EVT_GAME_ORDER_ARRIVE(win, func):
	win.Connect(-1, -1, wxEVT_GAME_ORDER_ARRIVE, func)

def UNEVT_GAME_ORDER_ARRIVE(win, func):
	win.Disconnect(-1, wxEVT_GAME_ORDER_ARRIVE, -1)

class GameObjectArriveEvent(wxPyEvent):
	def __init__(self, id, name):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_OBJ_ARRIVE)
		
		self.id = id
		self.name = name

class GameOrderArriveEvent(wxPyEvent):
	def __init__(self, order):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_ORDER_ARRIVE)
		
		self.value = order

# Incoming events
wxEVT_GAME_OBJ_GET = wxNewEventType()
wxEVT_GAME_ORDER_INS = wxNewEventType()
wxEVT_GAME_ORDER_GET = wxNewEventType()
wxEVT_GAME_ORDER_RM = wxNewEventType()

def EVT_GAME_OBJ_GET(win, func):
	win.Connect(-1, -1, wxEVT_GAME_OBJ_GET, func)

def UNEVT_GAME_OBJ_GET(win, func):
	win.Disconnect(-1, wxEVT_GAME_OBJ_GET, -1)

def EVT_GAME_ORDER_INS(win, func):
	win.Connect(-1, -1, wxEVT_GAME_ORDER_INS, func)

def UNEVT_GAME_ORDER_INS(win, func):
	win.Disconnect(-1, wxEVT_GAME_ORDER_INS, -1)

def EVT_GAME_ORDER_GET(win, func):
	win.Connect(-1, -1, wxEVT_GAME_ORDER_GET, func)

def UNEVT_GAME_ORDER_GET(win, func):
	win.Disconnect(-1, wxEVT_GAME_ORDER_GET, -1)
	
def EVT_GAME_ORDER_RM(win, func):
	win.Connect(-1, -1, wxEVT_GAME_ORDER_RM, func)

def UNEVT_GAME_ORDER_RM(win, func):
	win.Disconnect(-1, wxEVT_GAME_ORDER_RM, -1)

class GameObjectGetEvent(wxPyEvent):
	def __init__(self, id, name=""):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_OBJ_GET)
		
		self.id = id
		self.name = name
		
class GameOrderInsertEvent(wxPyEvent):
	def __init__(self, oid, type, slot):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_ORDER_INS)
		
		self.oid = oid
		self.type = type
		self.slot = slot
		
class GameOrderGetEvent(wxPyEvent):
	def __init__(self, oid, slot):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_ORDER_GET)
		
		self.oid = oid
		self.slot = slot

class GameOrderRemoveEvent(wxPyEvent):
	def __init__(self, oid, slot):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_GAME_ORDER_RM)
		
		self.oid = oid
		self.slot = slot

