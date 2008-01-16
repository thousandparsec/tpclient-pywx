
from extra.decorators import *

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

		self._ObjectSelect(id)
		self.application.Post(self.application.gui.SelectObjectEvent(id), source=self)

	def PreviewObject(self, id):
		"""
		Called to select an object.
		"""
		if self.oid == id:
			return

		self.ObjectPreview(id)
		self.application.Post(self.application.gui.PreviewObjectEvent(id), source=self)


from tp.netlib.objects import Order

class TrackerObjectOrder(TrackerObject):
	"""
	Tracks the currently selected object and order.

	Also provides a functionality to select an object and orders.
	"""

	def __init__(self):
		TrackerObject.__init__(self)

		self.slots = []

		self.application.gui.Binder(self.application.gui.SelectOrderEvent,        self.OnSelectOrder)

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
			if len(self.slots) > 0:
				for slot in self.slots:
					self.OrderRefresh(slot)

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
				if evt.action == "create":
					self.OrderInsert(evt.slot, evt.change)

				if evt.action == "change":
					self.OrderRefresh(evt.slot, evt.change)

				if evt.action == "remove":
					self.OrdersRemove(evt.slots, True)

				return

			if isinstance(evt, CacheUpdateEvent):
				if evt.action == "create":
					self.OrderInsert(evt.slot)

				if evt.action == "change":
					self.OrderRefresh(evt.slot)

				if evt.action == "remove":
					# Unselect any slots which are being removed
					leftslots = []
					for slot in self.slots:
						if not slot in evt.slots:
							leftslots.append(slot)
					if self.slots != leftslots:
						self._OrdersSelect(leftslots)

					self.OrdersRemove(evt.slots)

				return

	def OnSelectObject(self, evt):
		assert self != evt.source, "Got event %s which I was the source of." % evt

		# Check that if object is not already selected
		if self.oid == evt.id:
			return

		# Clear the selected slots
		self.slots = []

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

		# Check if these slots have already been selected
		if self.slots == evt.slots:
			return

		self._OrdersSelect(evt.slots)

	##########################################################################
	# Methods called when state changes with the order
	##########################################################################
	def _OrdersSelect(self, slots):
		"""
		Select an order (using slots).
		"""
		self.slots = slots
		self.OrdersSelect(slots)

	def OrdersSelect(self, slots):
		"""
		Select an order (using slots).
		"""
		pass

	def OrderInsert(self, slot, override=None):
		"""
		Called when a new order is inserted.
		"""
		pass

	def OrderRefresh(self, slot, override=None):
		"""
		Refresh the selected orders (this might not be all orders).

		If orders is given then it should be used as the source of information,
		otherwise the cache should be used.
	
		(By default calls SelectOrder)
		"""
		if override is None:
			self.SelectOrder(slots)

	def OrdersRemove(self, slots, override=False):
		"""
		Called when an order is removed.
		"""
		pass

	##########################################################################
	# Methods to change the state (orders)
	##########################################################################
	def SelectOrders(self, slots):
		"""
		Called to select orders on the current object.
		"""
		# Select orders is only valid when an object is selected
		assert self.oid != None
		# Slots must be posative
		for slot in slots:
			assert slot >= 0

		if self.slots == slots:
			return

		self._OrdersSelect(slots)
		self.application.Post(self.application.gui.SelectOrderEvent(self.oid, slots), source=self)

	def InsertOrder(self, order, slot=None):
		# Insert order is only valid when an object is selected
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if slot is None:
			if len(self.slots) > 0:
				slot = self.slots[0]
			else:
				slot = -1

		self.OrderInsert(slot, order)
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "create", self.oid, slot, order), source=self)

	def AppendOrder(self, order, slot=None):
		# Append order is only valid when an object is selected
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if slot is None:
			if len(self.slots) > 0:
				slot = self.slots[-1]+1
			else:
				slot = -1
		else:
			slot += 1

		self.OrderInsert(slot, order)
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "create", self.oid, slot, order), source=self)

	def DirtyOrder(self, order, slot=None):
		# Dirty order is only valid when an object is selected
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if slot is None:
			assert len(self.slots) == 1
			slot = self.slots[0]

		self.application.Post(self.application.gui.DirtyOrderEvent(order), source=self)

	def ChangeOrder(self, order, slot=None):
		# Change order is only valid when an object is selected
		assert self.oid != None
		# Order must be an order, duh!
		assert isinstance(order, Order)

		if slot is None:
			assert len(self.slots) == 1
			slot = self.slots[0]

		self.OrderRefresh(slot, order)
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "change", self.oid, slot, order), source=self)

	def RemoveOrders(self, slots=None):
		# Remove orders is only valid when an object is selected
		assert self.oid != None

		if slots is None:
			assert len(self.slots) > 0
			slots = self.slots

		self.OrdersRemove(slots, True)
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "remove", self.oid, slots=slots), source=self)

