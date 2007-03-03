"""\
An Overlay which provides a line showing where objects have orders to go.
"""
# Python imports
import os
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas.RelativePoint import RelativePoint
from extra.wxFloatCanvas.Icon import Icon

class Path(Overlay):
	"""\
	Draws a path of ships and similar objects.
	"""
	def __init__(self, canvas, cache):
		Overlay.__init__(self, canvas, cache)

		self['active'] = None

	def path(self, oid, overrides={}):
		c = self.cache

		# Calculate the path.
		path = [c.objects[oid].pos[0:2]]
		for order in c.orders[oid]:
			if not overrides.has_key(slot):
				order = orders[slot]
			else:
				order = overrides[slot]
			if order.type == MOVE_TYPE:
				path += [order.pos[0:2]]
		return path

	def updateall(self):
		"""\
		Updates all the little grey paths on the map.
		"""
		c = self.cache

		# Remove all the objects.
		self.cleanup()

		# Update all the objects.
		for oid in c.objects.keys():
			self.updateone(oid)

	def updateone(self, oid):
		"""\
		Adds the grey path line to the map.
		"""
		c = self.cache

		path = self.path(oid)
		if len(path) > 1:
			# Create the new object.
			self[oid] = FloatCanvas.Line(path, "Grey")
