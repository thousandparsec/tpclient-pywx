"""\

"""

import copy

from network import protocol
from network.events import *

from UniverseObjects import *

class ChildBeforeParent(Exception):
	pass

class UnknownObject(Exception):
	pass

class Game:
	def __init__(self, app):
		self.app = app

		# Register for object informations
		self.map = {}

	def OnPacket(self, evt):
		packet = evt.value

		try:
			if isinstance(packet, protocol.Object):
				# Okay, lets get a copy and then mutate this object into a UniverseObject
				new = copy.deepcopy(packet)

				if new.type == 1 or new.type == 0:
					new.__class__ = Container
				elif new.type == 2:
					new.__class__ = Actual
				else:
					raise UnknownObject("Unknown object recieveds\n%s" % packet)

				# Insert the object into map
				container = self.GetParent(new.id)
				if not container and new.id != 0:
					# Ekk! we got a child object but no parent
					raise ChildBeforeParent(repr(new.id))
				else:
					new.container = container
				
				self.map[new.id] = new

				if isinstance(new, Container):
					# Request it's children
					for id in new.contains:
						if id not in self.map.keys():
							r = protocol.GetObject(id=id)
							evt.network.socket.send(str(r))

			else:
				# Just ignored it
				pass

		finally:
			evt.next()

	def GetParent(self, id):
		for theid,o in self.map.items():
			if isinstance(o, Container):
				if id in o.contains:
					return o
		return None

