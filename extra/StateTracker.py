
import wx

from extra.decorators import *

from tp.client.ChangeList import ChangeNode
from tp.client import objectutils

# Raised when the game cache is made dirty. Contains a reference to what was updated.
#  -- CacheDirtyEvent

# Raised when the game cache is changed. Contains a reference to what was updated. 	
#  -- CacheUpdateEvent

#class StateTracker(object):
class TrackerObject(object):
	"""
	Tracks the state of the selected object. 

	Also provides a functionality to select an object.
	"""

	def __init__(self):
		self.oid   = None

		self.application.gui.Binder(self.application.CacheClass.CacheDirtyEvent,  self.OnObjectCacheUpdate)
		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnObjectCacheUpdate)
		self.application.gui.Binder(self.application.gui.SelectObjectEvent,       self.OnSelectObject)
		self.application.gui.Binder(self.application.gui.PreviewObjectEvent,      self.OnPreviewObject)

	##########################################################################
	# Callbacks for various events
	##########################################################################
	@freeze_wrapper
	def OnObjectCacheUpdate(self, evt):
		"""
		Called when something changes in the cache.
		"""
		assert not self is evt.source, "Got event %s which was sent by %s which is me (%s)!" % (evt, evt.source, self)

		# If there was a whole cache update
		if evt.what is None:
			if self.oid not in self.application.cache.objects:
				self.oid = None

			self.ObjectRefreshAll()

			# Refresh the currently selected object
			if not self.oid is None:
				self.ObjectRefresh(self.oid)
			else:
				self._ObjectSelect(None)

		CacheDirtyEvent, CacheUpdateEvent = self.application.cache.CacheDirtyEvent, self.application.cache.CacheUpdateEvent
		if evt.what == "objects":
			if isinstance(evt, CacheDirtyEvent):
				self.ObjectRefresh(evt.id, evt.change)
			if isinstance(evt, CacheUpdateEvent):
				self.ObjectRefresh(evt.id)
			return


	@freeze_wrapper
	def OnSelectObject(self, evt):
		"""
		Called when something else selects an object.
		"""
		assert not self is evt.source, "Got event %s which was sent by %s which is me (%s)!" % (evt, evt.source, self)

		# Check that if object is not already selected
		if self.oid == evt.id:
			return

		self._ObjectSelect(evt.id)

	@freeze_wrapper
	def OnPreviewObject(self, evt):
		"""
		Called when something else previews an object.
		"""
		assert not self is evt.source, "Got event %s which was sent by %s which is me (%s)!" % (evt, evt.source, self)

		# Check that if object is not already selected
		if self.oid == evt.id:
			return

		self.ObjectPreview(evt.id)

	##########################################################################
	# Methods called when state changes with an object
	##########################################################################
	def _ObjectSelect(self, id):
		self.oid = id
		self.ObjectSelect(id)

	def ObjectSelect(self, id):
		"""
		Called when an object is selected.
		"""
		pass

	def ObjectPreview(self, id):
		"""
		Called when an object is "previewed".
		
		(By default calls ObjectSelect method).
		"""
		self._ObjectSelect(id)
	
	def ObjectRefresh(self, id, object=None):
		"""
		Refresh the selected object.

		If object is given then it should be used as the source of information,
		otherwise the cache should be used.
	
		(By default calls SelectObject.)
		"""
		if object is None:
			self._ObjectSelect(id)

	def ObjectRefreshAll(self):
		"""
		Refresh all objects (apart from the one that is selected.
		"""
		pass

	##########################################################################
	# Methods to change the state
	##########################################################################
	def SelectObject(self, id, forceother=False):
		"""
		Called to select an object.
		"""
		if self.oid == id and not forceother:
			return
		
		self.application.Post(self.application.gui.SelectObjectEvent(id), source=self)

		if self.oid != id:
			self._ObjectSelect(id)

	def PreviewObject(self, id):
		"""
		Called to select an object.
		"""
		if self.oid == id:
			return

		self.application.Post(self.application.gui.PreviewObjectEvent(id), source=self)
		self.ObjectPreview(id)
	
	def SelectNextChild(self):
		if not self.oid is None:
			#print self.application.cache.objects[self.oid].name
			if hasattr(self.application.cache.objects[self.oid], "contains") and self.application.cache.objects[self.oid].contains != []:
				#print "Contains:"
				#for oid in self.application.cache.objects[self.oid].contains:
				#	print oid
				self.application.Post(self.application.gui.SelectObjectEvent(self.application.cache.objects[self.application.cache.objects[self.oid].contains[0]].id))
	
	def SelectNextObject(self):
		"""
		Called to select the next object.
		"""
		if not self.oid is None:
			self.SelectNextSibling(self.oid)
	
	def SelectNextSibling(self, objectid):
		if hasattr(self.application.cache.objects[objectid], "parent"):
			parentid = self.application.cache.objects[objectid].parent
			objectfound = 0
			for object in self.application.cache.objects[parentid].contains:
				if (object == objectid):
					objectfound = 1
					continue
				if (objectfound == 1):
					self.application.Post(self.application.gui.SelectObjectEvent(self.application.cache.objects[object].id))
					objectfound = 2
					break
			if objectfound == 1:
				self.SelectNextSibling(parentid)
						
	def SelectPreviousObject(self):
		"""
		Called to select the previous object.
		"""
		if not self.oid is None:
			self.SelectPreviousSibling(self.oid)
	
	def SelectPreviousSibling(self, objectid):
		if hasattr(self.application.cache.objects[objectid], "parent"):
			parentid = self.application.cache.objects[objectid].parent
			timesthrough = 0
			objectfound = -1
			for object in self.application.cache.objects[parentid].contains:
				if (object == objectid):
					objectfound = timesthrough
					print timesthrough
					continue
				timesthrough = timesthrough + 1
			if objectfound != -1:
				if objectfound == 0:
					self.application.Post(self.application.gui.SelectObjectEvent(parentid))
				else:
					self.application.Post(self.application.gui.SelectObjectEvent(self.application.cache.objects[parentid].contains[objectfound-1]))


from tp.netlib.objects import Order

class TrackerOrder(object):
	"""
	Tracks the currently selected order queue

	Also provides a functionality to select orders.
	"""
		
	def __init__(self):
		self.qid   = None
		self.nodes = []
		
		self.application.gui.Binder(self.application.CacheClass.CacheDirtyEvent,  self.OnOrderCacheUpdate)
		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnOrderCacheUpdate)

		self.application.gui.Binder(self.application.gui.SelectOrderEvent, self.OnSelectOrder)

	##########################################################################
	# Callbacks for various events
	##########################################################################
	def OnOrderCacheUpdate(self, evt):
		assert not self is evt.source, "Got event %s which was sent by %s which is me (%s)!" % (evt, evt.source, self)
	
		# If there was a whole cache update
		if evt.what is None:
			if self.qid not in self.application.cache.orderqueues:
				self.OrderQueueSelect(None)

			if self.qid:
				self.SelectOrders([])
			return

		# Only interested in an CacheUpdates which are for the selected order queue.
		if evt.id != self.qid:
			return

		CacheDirtyEvent, CacheUpdateEvent = self.application.cache.CacheDirtyEvent, self.application.cache.CacheUpdateEvent

		if evt.what == "orders":
			if isinstance(evt, CacheDirtyEvent):
				if evt.action == "create after":
					self.OrderInsertAfter(evt.node, evt.change)
				if evt.action == "create before":
					self.OrderInsertBefore(evt.node, evt.change)

				if evt.action == "change":
					self.OrderRefresh(evt.change)

				if evt.action == "remove":
					self.OrdersRemove(evt.nodes, True)

				return

			if isinstance(evt, CacheUpdateEvent):
				if evt.action in ("create before", "create after", "change"):
					self.OrderRefresh(evt.change)

				if evt.action == "remove":
					# Unselect any slots which are being removed
					leftnodes = []
					for node in self.nodes:
						if not node in evt.nodes:
							leftnodes.append(node)

					if self.nodes != leftnodes:
						self._OrdersSelect(leftnodes)

					self.OrdersRemove(evt.nodes)

				return
		
	def OrderQueueSelect(self, id):
		# Check that if object is not already selected
		if self.qid == id:
			return

		# Clear the selected nodes
		self.nodes = []
		
		self.qid = id
		self._OrdersSelect([])

	def OnSelectOrder(self, evt):
		"""
		Called when something else selects an order.
		"""
		assert not self is evt.source, "Got event %s which was sent by %s which is me (%s)!" % (evt, evt.source, self)

		# Check this order is for the currently selected object
		if self.qid != evt.id:
			return			

		# Check if these nodes have already been selected
		if self.nodes == evt.nodes:
			return

		self._OrdersSelect(evt.nodes)

	def OnKeyUp(self, evt):
		if evt.GetKeyCode() == wx.WXK_ESCAPE:
			self.SetMode(self.GUISelect)	

		if evt.GetKeyCode() == wx.WXK_DELETE:
			if len(self.nodes) == 0:
				return
			elif len(self.nodes) == 1:
				self.RemoveOrders(self.nodes)
			else:
				dlg = wx.MessageDialog(self,
						"You are about to remove multiple\norders, are you sure?",
 						"Remove orders?", 
						wx.OK | wx.CANCEL)

				if dlg.ShowModal() == wx.ID_OK:
					self.RemoveOrders(self.nodes)

				dlg.Destroy()

		if evt.GetKeyCode() in (60, 44): # <
			if len(self.nodes) > 0 and not self.nodes[0].left.left is None:
				if evt.ShiftDown():
					self.SelectOrders([self.nodes[0].left] + self.nodes[:])
				else:
					self.SelectOrders([self.nodes[0].left])
			if len(self.nodes) == 0:
				d = self.application.cache.orders[self.qid]
				if len(d) > 0:
					self.SelectOrders([d.last])

		if evt.GetKeyCode() in (46,): # >
			if len(self.nodes) > 0 and not self.nodes[-1].right is None:
				if evt.ShiftDown():
					self.SelectOrders(self.nodes[:] + [self.nodes[-1].right])
				else:
					self.SelectOrders([self.nodes[-1].right])

			if len(self.nodes) == 0:
				d = self.application.cache.orders[self.qid]
				if len(d) > 0:
					self.SelectOrders([d.first])

	##########################################################################
	# Methods called when state changes with the order
	##########################################################################
	def _OrdersSelect(self, nodes):
		"""
		Select an order (using nodes).
		"""
		self.nodes = nodes

		if self.qid != None:
			d = self.application.cache.orders[self.qid]
			def nodecmp(a, b):
				return cmp(d.index(a), d.index(b))
			self.nodes.sort(nodecmp)

			self.OrdersSelect(nodes)

	def OrdersSelect(self, nodes):
		"""
		Select an order (using nodes).
		"""
		pass

	def OrderInsertAfter(self, afterme, toinsert):
		"""
		Called when a new order is inserted.
		"""
		pass

	def OrderInsertBefore(self, beforeme, toinsert):
		"""
		Called when a new order is inserted.
		"""
		pass

	def OrderRefresh(self, node, override=None):
		"""
		Refresh the selected orders (this might not be all orders).

		If orders is given then it should be used as the source of information,
		otherwise the cache should be used.
		"""
		pass

	def OrdersRemove(self, nodes, override=False):
		"""
		Called when an order is removed.
		"""
		pass

	##########################################################################
	# Methods to change the state (orders)
	##########################################################################
	def SelectOrders(self, nodes):
		"""
		Called to select orders on the current object.
		"""
		# Select orders is only valid when an object is selected
		assert self.qid != None

		if self.nodes == nodes:
			return
		
		d = self.application.cache.orders[self.qid]
		# Nodes must exist in the orders cache
		for node in nodes:
			assert isinstance(node, ChangeNode)
			assert node in d

		# Tell everyone else about the change
		self.application.Post(self.application.gui.SelectOrderEvent(self.qid, nodes), source=self)
		# Call our handler
		self._OrdersSelect(nodes)

	def InsertAfterOrder(self, order, node=None):
		# Insert order is only valid when an object is selected
		assert self.qid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)
		
		queue = self.application.cache.orders[self.qid]

		if node is None:
			if len(self.nodes) > 0:
				node = self.nodes[-1]
			else:
				node = queue.last
			
		assert not node is None

		# Do some sanity checking
		d = queue
		assert node in d

		# Make the change to the cache	
		evt = self.application.cache.apply("orders", "create after", self.qid, node, order)

		# Do some sanity checking
		assert not evt.change is None
		assert evt.change in d
		assert node != evt.change

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrderInsertAfter(node, evt.change)

		return evt.change

	def InsertBeforeOrder(self, order, node=None):
		# Insert order is only valid when an object is selected
		assert self.qid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if node is None:
			if len(self.nodes) > 0:
				node = self.nodes[0]
			else:
				node = self.application.cache.orders[self.qid].first
			
		assert not node is None

		# Make the change to the cache	
		evt = self.application.cache.apply("orders", "create before", self.qid, node, order)

		# Do some sanity checking
		assert not evt.change is None
		d = self.application.cache.orders[self.qid]
		assert evt.change in d

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrderInsertBefore(node, evt.change)

		return evt.change


	def DirtyOrder(self, order, node=None):
		pass

#		# Dirty order is only valid when an object is selected
#		assert self.qid != None
#		# Order must be an order, duh!
#		assert isinstance(order, Order)
#
#		if node is None:
#			assert len(self.nodes) == 1
#			node = self.nodes[0]
#
#		self.application.Post(self.application.gui.DirtyOrderEvent(order), source=self)

	def ChangeOrder(self, order, node=None):
		# Change order is only valid when an object is selected
		assert self.qid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if node is None:
			assert len(self.nodes) == 1
			node = self.nodes[0]
		
		evt = self.application.cache.apply("orders", "change", self.qid, node, order)

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrderRefresh(evt.change)

	def RemoveOrders(self, nodes=None):
		# Remove orders is only valid when an object is selected
		assert self.qid != None

		if nodes is None:
			if len(self.nodes) == 0:
				return

			nodes = self.nodes
		
		evt = self.application.cache.apply("orders", "remove", self.qid, nodes=nodes)

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrdersRemove(nodes, True)


from tp.netlib.objects import Order

class TrackerObjectOrder(TrackerObject, TrackerOrder):
	"""
	Tracks the currently selected object and order.

	Also provides a functionality to select an object and orders.
	"""

	def __init__(self):
		TrackerObject.__init__(self)
		TrackerOrder.__init__(self)

	def _ObjectSelect(self, id):
		TrackerObject._ObjectSelect(self, id)

		qid = None
		if self.oid is not None:
			# FIXME: We currently just select the first order queue...
			queues = objectutils.getOrderQueueList(self.application.cache, id)
			if len(queues) > 0:
				qid = queues[0][1]
		
		print "Selecting queue", qid, " on ", id

		TrackerOrder.OrderQueueSelect(self, qid)
