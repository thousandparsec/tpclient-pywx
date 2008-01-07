
# Raised when the game cache is made dirty. Contains a reference to what was updated.
#  -- CacheDirtyEvent

# Raised when the game cache is changed. Contains a reference to what was updated. 	
#  -- CacheUpdateEvent

#class StateTracker(object):
class TrackerObject(object):
	pass

class TrackerObjectOrder(object):
	REFRESH_DIRTY    = 1
	REFRESH_COMMITED = 2

	def __init__(self):
		self.oid   = None
		self.slots = []

		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnCacheUpdate)
		self.application.gui.Binder(self.application.gui.SelectObjectEvent,       self.OnSelectObject)
		self.application.gui.Binder(self.application.gui.SelectOrderEvent,        self.OnSelectOrder)

	##########################################################################
	# Callbacks for various events
	##########################################################################
	def OnCacheUpdate(self, evt):
		print evt

		# If there was a whole cache update
		if evt.what is None:
			# Refresh the currently selected object
			if not self.oid is None:
				self.ObjectRefresh(oid)
			else:
				self.ObjectSelect(None)

			# Refresh the currently selected order
			if len(self.slots) > 0:
				for slot in self.slots:
					self.OrderRefresh(slot)

			return
	
		# Only interested in an CacheUpdates which are for the selected object
		if evt.id != self.id:
			return 

		if evt.what == "objects":
			if isinstance(evt, CacheDirtyEvent):
				self.ObjectRefresh(evt.id, "---")
			if isinstance(evt, CacheUpdateEvent):
				self.ObjectRefresh(evt.id)
			return

		if evt.what == "orders":
			if isinstance(evt, CacheDirtyEvent):
				if evt.action == "create":
					self.OrderInsert(evt.slot, "---")

				if evt.action == "change":
					self.OrderRefresh(evt.slot, "---")

				if evt.remove == "remove":
					self.OrderRemove(evt.slot, "---")

				return

			if isinstance(evt, CacheUpdateEvent):
				if evt.action == "create":
					self.OrderInsert(evt.slot)

				if evt.action == "change":
					self.OrderRefresh(evt.slot)

				if evt.remove == "remove":
					self.OrderRemove(evt.slot)

				return

	def OnSelectObject(self, evt):
		"""
		Called when 
		"""
		print self, "OnSelectObject", evt

		# Check that if object is not already selected
		if self.oid == evt.id:
			return

		# Clear the selected slots
		self.slots = []

		self.ObjectSelect(evt.id)

	def OnSelectOrder(self, evt):
		print self, "OnSelectOrder", evt

		# Check this order is for the currently selected object
		if self.oid != evt.id:
			return			

		# Check if these slots have already been selected
		if self.slots == evt.slots:
			return

		self.OrdersSelect(evt.slots)

	##########################################################################
	# Methods called when state changes with an object
	##########################################################################
	def ObjectSelect(self, id):
		"""
		Called when an object is selected.
		"""
		self.oid = id
	
	def ObjectRefresh(self, id, object=None):
		"""
		Refresh the selected object.

		If object is given then it should be used as the source of information,
		otherwise the cache should be used.
	
		(By default calls SelectObject)
		"""
		if object is None:
			self.ObjectSelect(id)

	##########################################################################
	# Methods called when state changes with the order
	##########################################################################
	def OrdersSelect(self, slots):
		"""
		Select an order (using slots)
		"""
		self.slots = slots

	def OrderInsert(self, slot, override=None):
		"""
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

	def OrderRemove(self, slot, override=None):
		"""
		"""
		pass

	##########################################################################
	# Methods to change the state
	##########################################################################
	def SelectObject(self, id):
		"""
		Called to select an object.
		"""
		if self.oid == id:
			return

		self.ObjectSelect(id)
		self.application.Post(self.application.gui.SelectObjectEvent(id), source=self)

	def SelectOrders(self, slots):
		"""
		Called to select orders on the current object.
		"""
		if self.slots == slots:
			return

		self.OrdersSelect(slots)
		self.application.Post(self.application.gui.SelectOrderEvent(self.oid, slots), source=self)

	def InsertOrder(self, slot, order):
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "create", self.oid, slot, order), source=self)

	def DirtyOrder(self, slot, order):
		order.slot = slot
		self.application.Post(self.application.gui.DirtyOrderEvent(order), source=self)

	def ChangeOrder(self, slot, order):
		order.slot = slot
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "change", self.oid, slot, order), source=self)

	def RemoveOrder(self, slot, order=None):
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "remove", self.oid, slot, order), source=self)

