
from extra.decorators import *

from tp.client.ChangeList import ChangeNode

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

		self.application.gui.Binder(self.application.CacheClass.CacheDirtyEvent,  self.OnCacheUpdate)
		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnCacheUpdate)
		self.application.gui.Binder(self.application.gui.SelectObjectEvent,       self.OnSelectObject)
		self.application.gui.Binder(self.application.gui.PreviewObjectEvent,      self.OnPreviewObject)

	##########################################################################
	# Callbacks for various events
	##########################################################################
	@freeze_wrapper
	def OnCacheUpdate(self, evt):
		"""
		Called when something changes in the cache.
		"""
		assert self != evt.source, "Got event %s which I was the source of." % evt

		# If there was a whole cache update
		if evt.what is None:
			# Refresh the currently selected object
			if not self.oid is None:
				self.ObjectRefresh(oid)
			else:
				self._ObjectSelect(None)

	@freeze_wrapper
	def OnSelectObject(self, evt):
		"""
		Called when something else selects an object.
		"""
		assert self != evt.source, "Got event %s which I was the source of." % evt

		# Check that if object is not already selected
		if self.oid == evt.id:
			return

		self._ObjectSelect(evt.id)

	@freeze_wrapper
	def OnPreviewObject(self, evt):
		"""
		Called when something else previews an object.
		"""
		assert self != evt.source, "Got event %s which I was the source of." % evt

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

	##########################################################################
	# Methods to change the state
	##########################################################################
	def SelectObject(self, id):
		"""
		Called to select an object.
		"""
		if self.oid == id:
			return

		self.application.Post(self.application.gui.SelectObjectEvent(id), source=self)
		self._ObjectSelect(id)

	def PreviewObject(self, id):
		"""
		Called to select an object.
		"""
		if self.oid == id:
			return

		self.application.Post(self.application.gui.PreviewObjectEvent(id), source=self)
		self.ObjectPreview(id)


from tp.netlib.objects import Order

class TrackerObjectOrder(TrackerObject):
	"""
	Tracks the currently selected object and order.

	Also provides a functionality to select an object and orders.
	"""

	def __init__(self):
		TrackerObject.__init__(self)

		self.nodes = []

		self.application.gui.Binder(self.application.gui.SelectOrderEvent, self.OnSelectOrder)

	##########################################################################
	# Callbacks for various events
	##########################################################################
	def OnCacheUpdate(self, evt):
		assert self != evt.source, "Got event %s which I was the source of." % evt


		# If there was a whole cache update
		if evt.what is None:
			# Refresh the currently selected object
			if not self.oid is None:
				self.ObjectRefresh(oid)
			else:
				self._ObjectSelect(None)

			# Refresh the currently selected order
			if len(self.nodes) > 0:
				for node in self.nodes:
					self.OrderRefresh(node)

			return
	
		# Only interested in an CacheUpdates which are for the selected object
		if evt.id != self.oid:
			return 

		CacheDirtyEvent, CacheUpdateEvent = self.application.cache.CacheDirtyEvent, self.application.cache.CacheUpdateEvent
		if evt.what == "objects":
			if isinstance(evt, CacheDirtyEvent):
				self.ObjectRefresh(evt.id, evt.change)
			if isinstance(evt, CacheUpdateEvent):
				self.ObjectRefresh(evt.id)
			return

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

	def OnSelectObject(self, evt):
		assert self != evt.source, "Got event %s which I was the source of." % evt

		# Check that if object is not already selected
		if self.oid == evt.id:
			return

		# Clear the selected nodes
		self.nodes = []

		self._ObjectSelect(evt.id)

	def _ObjectSelect(self, id):
		self.oid = id
		self.ObjectSelect(id)
		self._OrdersSelect([])

	def OnSelectOrder(self, evt):
		"""
		Called when something else selects an order.
		"""
		assert self != evt.source, "Got event %s which I was the source of." % evt

		# Check this order is for the currently selected object
		if self.oid != evt.id:
			return			

		# Check if these nodes have already been selected
		if self.nodes == evt.nodes:
			return

		self._OrdersSelect(evt.nodes)

	##########################################################################
	# Methods called when state changes with the order
	##########################################################################
	def _OrdersSelect(self, nodes):
		"""
		Select an order (using nodes).
		"""
		self.nodes = nodes
		if self.oid != None:
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
		assert self.oid != None

		if self.nodes == nodes:
			return

		# Nodes must exist in the orders cache
		d = self.application.cache.orders[self.oid]
		for node in nodes:
			assert isinstance(node, ChangeNode)
			assert node in d

		# Tell everyone else about the change
		self.application.Post(self.application.gui.SelectOrderEvent(self.oid, nodes), source=self)
		# Call our handler
		self._OrdersSelect(nodes)

	def InsertAfterOrder(self, order, node=None):
		# Insert order is only valid when an object is selected
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if node is None:
			if len(self.nodes) > 0:
				node = self.nodes[0]
			else:
				node = self.application.cache.orders[self.oid].last
			
		assert not node is None

		# Make the change to the cache	
		evt = self.application.cache.apply("orders", "create after", self.oid, node, order)

		# Do some sanity checking
		assert not evt.change is None
		d = self.application.cache.orders[self.oid]
		assert evt.change in d

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrderInsertAfter(node, evt.change)

	def InsertBeforeOrder(self, order, node=None):
		# Insert order is only valid when an object is selected
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

	def DirtyOrder(self, order, node=None):
		pass

#		# Dirty order is only valid when an object is selected
#		assert self.oid != None
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
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if node is None:
			assert len(self.nodes) == 1
			node = self.nodes[0]

		evt = self.application.cache.apply("orders", "change", self.oid, node, order)

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrderRefresh(evt.change)

	def RemoveOrders(self, nodes=None):
		# Remove orders is only valid when an object is selected
		assert self.oid != None

		if nodes is None:
			if len(self.nodes) == 0:
				return

			nodes = self.nodes
			
		evt = self.application.cache.apply("orders", "remove", self.oid, nodes=nodes)

		# Tell everyone else about the change
		self.application.Post(evt, source=self)
		# Call our handler
		self.OrdersRemove(nodes, True)
