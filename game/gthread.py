"""\
This module contains the code for the network thread which
dispatchs events for incoming packets.
"""
# Python imports
import time
from thread import allocate_lock

# wxWindows imports
from wxPython.wx import * 

# Game imports
from utils import *

# Local imports
from network.protocol import *
from events import *
from extra.evtmgr import eventManager

class GameThread:
	def __init__(self):
		self.windows = []

		self.universe = Universe

	def win_connect(self, window):
		"""\
		Starts a window recieving the events from the game thread.
		"""
		self.windows.append(window)

	def win_disconnect(self, window):
		"""\
		Stops a window from recieving events from the game thread.
		"""
		self.windows.remote(window)

	def OnPacket(self, evt):	
		if isinstance(packet, protocol.Object):
			# Okay, lets get a copy and then mutate this object into a UniverseObject
			new = copy.deepcopy(packet)

			if new.type == 1 or new.type == 0:
				new.__class__ = Container
			elif new.type == 2:
				new.__class__ = Actual
			else:
				raise UnknownObject("Unknown object recieved %r\n%s" % (packet, packet))

			if isinstance(new, Container):
				# Request it's children
				for id in new.contains:
					if id not in self.universe.keys():
						g = protocol.GetObject(id=id)
						network.send(g)

	def __call__(self):
		"""\
		This is the main loop. It will never terminate and should be
		called in it's own thread.
		"""
		# Main thread loop
		while TRUE:
			time.sleep(30)
