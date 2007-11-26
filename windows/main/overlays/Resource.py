"""\
This overlay shows circles which are proportional to the amount of a certain
resource found in that object.
"""
# Python imports
import os
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas import PieChart
from extra.wxFloatCanvas.RelativePoint import RelativePoint

from extra.wxFloatCanvas.NavCanvas import NavCanvas

from Proportional import Proportional
class Resource(Proportional):
	"""\
	Draws proportional circles for the relative number of resources.
	"""
	name = "Resources"

	TOTAL        = -1
	SURFACE	     =  1
	MINABLE	     =  2
	INACCESSABLE =  3	

	def __init__(self, parent, canvas, panel, cache, resource=None, type=-1):
		Proportional.__init__(self, parent, canvas, panel, cache)

		self.resource = resource
		self.type     = type
		
		self.UpdateAll()
		self.canvas.Draw()
		
	def UpdateAll(self):
		Proportional.UpdateAll(self)
		
	def UpdateOne(self, oid, value=None):
		proportional = Proportional.UpdateOne(self, oid, value)
		#self.valuesforchart = ()
		c = self.cache 
		o = c.objects[oid]
		#self[oid] = PieChart.PieChart((0, 0), 0.0000001, (1, 1))
		self.valuesforchart = ()
		self.valuesresources = {}
		if (o.subtype == 2):
			if hasattr(o, "contains"):
				for child in o.contains:
					if hasattr(c.objects[child], "resources"):
						for resource in c.objects[child].resources:
							if resource[1:] != 0:
								if self.valuesresources.has_key(resource[0]):
									self.valuesresources[resource[0]] += reduce(int.__add__, resource[1:])
								else:
									self.valuesresources[resource[0]] = reduce(int.__add__, resource[1:])
			for resource, amount in self.valuesresources.items():
				self.valuesforchart += (amount,)
			if proportional*self.scale > 0:
				self[oid] = PieChart.PieChart(c.objects[oid].pos[0:2], proportional*self.scale, self.valuesforchart, Scaled=False)
			else:
				self[oid] = PieChart.PieChart((0,0), 0.001, (1,1))
		else:
			self[oid] = PieChart.PieChart((0,0), 0.001, (1,1))
	def Amount(self, oid):
		"""\
		The amount of this resource on this object.
		"""
		c = self.cache 
		o = c.objects[oid]

		amount = 0
		if hasattr(o, "contains"):
			for child in o.contains:
				amount += self.Amount(child)

		if hasattr(o, "resources"):
			for resource in o.resources:
				if self.type == Resource.TOTAL:
					amount += reduce(int.__add__, resource[1:])
				else:
					amount += resource[self.type]
		
		return amount
