
from wxPython.wx import *

wxEVT_NETWORK_PACKET = wxNewEventType()

def EVT_NETWORK_PACKET(win, func):
	win.Connect(-1, -1, wxEVT_NETWORK_PACKET, func)

def UNEVT_NETWORK_PACKET(win, func):
	win.Disconnect(-1, wxEVT_NETWORK_PACKET, -1)

class NetworkPacketEvent(wxPyEvent):
    def __init__(self, packet):
        wxPyEvent.__init__(self)
        self.SetEventType(wxEVT_NETWORK_PACKET)
        self.value = packet

