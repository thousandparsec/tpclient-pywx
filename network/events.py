"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

# Outgoing events
wxEVT_NETWORK_PACKET = wxNewEventType()
wxEVT_NETWORK_CONNECT = wxNewEventType()
wxEVT_NETWORK_DISCONNECT = wxNewEventType()

def EVT_NETWORK_PACKET(win, func):
	win.Connect(-1, -1, wxEVT_NETWORK_PACKET, func)

def UNEVT_NETWORK_PACKET(win, func):
	win.Disconnect(-1, wxEVT_NETWORK_PACKET, -1)

class NetworkPacketEvent(wxPyEvent):
	"""\
	A packet has been recived accross the wire.

	evt.value is the packet
	evt.network is the thread the packet came in on.
	"""
	def __init__(self, packet, network):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_NETWORK_PACKET)
		
		self.value = packet
		self.network = network
	
	def Next(self):
		self.network.Next()

# Incoming events
wxEVT_NETWORK_SEND = wxNewEventType()

def EVT_NETWORK_SEND(win, func):
	win.Connect(-1, -1, wxEVT_NETWORK_SEND, func)

def UNEVT_NETWORK_SEND(win, func):
	win.Disconnect(-1, wxEVT_NETWORK_SEND, -1)

class NetworkSendEvent(wxPyEvent):
	"""\
	A packet needs to be send accross the wire.

	evt.value is the packet
	"""
	def __init__(self, packet):
		wxPyEvent.__init__(self)
		self.SetEventType(wxEVT_NETWORK_SEND)
		
		self.value = packet
