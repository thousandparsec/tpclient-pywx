"""\
This module contains the wxPython event definitions for
network events.
"""

from wxPython.wx import *

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
	
	def next(self):
		self.network.next()

