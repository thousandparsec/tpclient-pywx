"""\
This module contains the code for the network thread which
dispatchs events for incoming packets.
"""
# Python imports
import time
import copy
from thread import allocate_lock

# wxWindows imports
from wxPython.wx import * 

# Game imports
from utils import *
from network import protocol

# Local imports
from events import *
from objects import *

class GameThread:
	def __init__(self):
		self.windows = []

		self.universe = Universe()

	def WinConnect(self, window):
		"""\
		Starts a window recieving the events from the game thread.
		"""
		self.windows.append(window)

	def WinDisconnect(self, window):
		"""\
		Stops a window from recieving events from the game thread.
		"""
		self.windows.remote(window)

	def OnPacket(self, evt):	
		if isinstance(evt.value, protocol.Object):
			# Okay, lets get a copy and then mutate this object into a UniverseObject
			new = copy.deepcopy(evt.value)

			if new.type == 1 or new.type == 0:
				new.__class__ = Container
			elif new.type == 2:
				new.__class__ = Actual
			else:
				raise UnknownObject("Unknown object recieved %r\n%s" % (e.value, e.value))

			self.universe.Add(new)

			# Publish an object arrived event, dont post for the universe
			if new.id != 0:
				for window in self.windows:
					nevt = GameArriveObjectEvent(new.id, new.name)
					wxPostEvent(window, nevt)

			if isinstance(new, Container):
				# Request it's children
				for id in new.contains:
					if id not in self.universe.ObjectIDs():

						# Publish an object getting event
						for window in self.windows:
							nevt = GameGetObjectEvent(id, "")
							wxPostEvent(window, nevt)
					
						g = protocol.GetObject(id=id)
						evt.network.Send(g)

	def __call__(self):
		"""\
		This is the main loop. It will never terminate and should be
		called in it's own thread.
		"""
		# Main thread loop
		while TRUE:
			time.sleep(30)
