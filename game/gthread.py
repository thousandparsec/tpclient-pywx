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
from network.events import *

# Local imports
from bthread import BaseThread
from events import *
from objects import *

# Program imports
from extra.wxPostEvent import *

typemap = (Container, Container, StarSystem, Planet, Fleet)

class GameThread(BaseThread):
	def __init__(self):
		BaseThread.__init__(self)
		
		EVT_GAME_OBJ_GET(self, self.OnObjectGet)
		EVT_GAME_ORDER_INS(self, self.OnOrderInsert)
		EVT_GAME_ORDER_GET(self, self.OnOrderGet)
		EVT_GAME_ORDER_RM(self, self.OnOrderRemove)

		self.universe = Universe()
		self.descs = DescHolder()

	def OnObjectGet(self, evt):
		debug(DEBUG_GAME, "Got a request for object (%i)" % evt.id)
		packet = protocol.ObjectGet(id=evt.id)
		nevt = NetworkSendEvent(packet)
		wxPostEvent(nevt)

	def OnOrderInsert(self, evt):
		args = None

		if evt.order:
			debug(DEBUG_GAME, "Got a request for insert (built) on %i of type %i at %i" % (evt.order.oid, evt.order.otype, evt.order.slot))
			
			# They have given us an order
			args = [None, evt.order.oid, evt.order.otype, evt.order.slot]

			for i in evt.order.args:
				args.append(i)

		else:
			debug(DEBUG_GAME, "Got a request for insert (unbuilt) on %i of type %i at %i" % (evt.oid, evt.type, evt.slot))
			args = [None, evt.oid, evt.type, evt.slot]
			desc = self.descs.OrderDesc(evt.type)
			if desc:
				for name, type, string in desc.parameters:
					if type == protocol.OrderDesc.ARG_COORD:
						args += [10,10,10]
					elif type == protocol.OrderDesc.ARG_TIME:
						args += [10]
					elif type == protocol.OrderDesc.ARG_OBJECT:
						args += [3]
					elif type == protocol.OrderDesc.ARG_PLAYER:
						args += [1]
			
			else:
				debug(DEBUG_GAME, "Tried to insert an order of type %i before we had the description" % evt.type)
				
		if args:
			packet = apply(protocol.OrderAdd, args)
			nevt = NetworkSendEvent(packet)
			wxPostEvent(nevt)
		
	def OnOrderRemove(self, evt):
		if evt.order:
			debug(DEBUG_GAME, "Got a prebuilt order")
			oid=evt.order.oid
			slot=evt.order.slot
		else:
			debug(DEBUG_GAME, "Have to build an order")
			oid=evt.oid
			slot=evt.slot
		
		debug(DEBUG_GAME, "Got a request to remove an order at %i on %i" % (slot, oid))
		
		packet = protocol.OrderRemove(oid=oid, slot=slot)
		nevt = NetworkSendEvent(packet)
		wxPostEvent(nevt)

	def OnOrderGet(self, evt):
		debug(DEBUG_GAME, "Got a request for an order at %i on %i" % (evt.slot, evt.oid))
		packet = protocol.OrderGet(oid=evt.oid, slot=evt.slot)
		nevt = NetworkSendEvent(packet)
		wxPostEvent(nevt)

	def OnPacket(self, evt):	
		if isinstance(evt.value, protocol.Object):
			debug(DEBUG_GAME, "Got an object packet")
			# Okay, lets get a copy and then mutate this object into a UniverseObject
			new = copy.deepcopy(evt.value)

			if new.type < len(typemap):
				new.__class__ = typemap[new.type]
			else:
				new.__class__ = Unknown

			self.universe.Add(new)

			# Publish an object arrived event, dont post for the universe
			if new.id != 0:
				for window in self.windows:
					nevt = GameObjectArriveEvent(new.id, new.name)
					wxPostEvent(window, nevt)

			if isinstance(new, Container):
				# Request it's children
				for id in new.contains:
					if id not in self.universe.ObjectIDs():

						# Publish an object getting event
						for window in self.windows:
							nevt = GameObjectGetEvent(id, "")
							wxPostEvent(window, nevt)
					
						debug(DEBUG_GAME, "Getting object %i" % id)
						g = protocol.ObjectGet(id=id)
						nevt = NetworkSendEvent(g)
						wxPostEvent(nevt)
			
			for id in new.orders_valid:
				debug(DEBUG_GAME, "Getting order desc for %i" % id)
				g = protocol.OrderDescGet(id=id)
				nevt = NetworkSendEvent(g)
				wxPostEvent(nevt)
		
		elif isinstance(evt.value, protocol.OrderDesc):
			debug(DEBUG_GAME, "Got an order description packet")
			new = copy.deepcopy(evt.value)
			self.descs.OrderDescAdd(new)

		elif isinstance(evt.value, protocol.Order):
			debug(DEBUG_GAME, "Got an order packet")
			new = copy.deepcopy(evt.value)
			new.__class__ = Order
		
			print "Test:", new.args
		
			# Publish an object getting event
			for window in self.windows:
				nevt = GameOrderArriveEvent(new)
				wxPostEvent(window, nevt)

