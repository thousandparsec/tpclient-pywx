"""\
Events that can be raised by windows.
"""

import wx

class CacheUpdateEvent(wx.PyEvent):
	"""\
	Raised when the game cache is changed.
	"""
	pass
wx.local.CacheUpdateEvent = CacheUpdateEvent

class SelectObjectEvent(wx.PyEvent):
	"""\
	Raised when an object is selected.
	"""
	def __init__(self, id):
		self.id = id
wx.local.SelectObjectEvent = SelectObjectEvent

class SelectPositionEvent(wx.PyEvent):
	"""\
	Raised when a position is selected.
	"""
	def __init__(self, pos):
		self.x, self.y, self.z = pos
wx.local.SelectPositionEvent = SelectPositionEvent

class SelectOrderEvent(wx.PyEvent):
	"""\
	Raised when an order is selected.
	"""
	def __init__(self, id, slots):
		self.id = id
		self.slots = slots
wx.local.SelectOrderEvent = SelectOrderEvent

class UpdateOrderEvent(wx.PyEvent):
	"""\
	Raised when an order has been saved, created or deleted.
	(Hence can be accessed from the cache.)
	"""
	def __init__(self, id, slot):
		self.id = id
		self.slot = slot
wx.local.UpdateOrderEvent = UpdateOrderEvent

class DirtyOrderEvent(wx.PyEvent):
	"""\
	Raised when an order has been changed but not yet saved.
	"""
	def __init__(self, order):
		self.id = order.id
		self.slot = order.slot
		self.order = order
wx.local.DirtyOrderEvent = DirtyOrderEvent

