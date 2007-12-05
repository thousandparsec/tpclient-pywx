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

import operator

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
		
		self.ResourceTypeList = {"All":Resource.TOTAL}
		
		for number, resource in cache.resources.items():
			self.ResourceTypeList[resource.name] = number

		self.resource = resource
		self.type     = type
		
		# Create a drop-down on the panel for colorizer
		self.ResourceSelector = wx.Choice(panel)
		self.ResourceSelector.Bind(wx.EVT_CHOICE, self.OnResourceSelected)

		# Populate the colorizer dropdown with information
		for name, resource in sorted(self.ResourceTypeList.items(), key=operator.itemgetter(1)):
			self.ResourceSelector.Append(name, resource)
		self.ResourceSelector.SetSelection(0)

		sizer = wx.FlexGridSizer(10)
		sizer.AddGrowableRow(0)
		sizer.Add(self.ResourceSelector, proportion=1, flag=wx.EXPAND)
		panel.SetSizer(sizer)
		
		self.UpdateAll()
		self.canvas.Draw()
		
	def OnResourceSelected(self, evt):
		self.type = self.ResourceSelector.GetClientData(self.ResourceSelector.GetSelection())
		
		if not evt is None:
			self.CleanUp()
			self.UpdateAll()
			self.canvas.Draw()
		
	def UpdateAll(self):
		Proportional.UpdateAll(self)
		
	def UpdateOne(self, oid, value=None):
		#print self.type
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
							if reduce(int.__add__, resource[1:]) != 0:
								if self.type == Resource.TOTAL or resource[0] == self.type:
									if self.valuesresources.has_key(resource[0]):
										self.valuesresources[resource[0]] += reduce(int.__add__, resource[1:])
									else:
										self.valuesresources[resource[0]] = reduce(int.__add__, resource[1:])
			
			#print c.objects[oid].name, ":"
			for resource, amount in self.valuesresources.items():
				if amount < (self.Amount(oid) * .10):
					print amount, self.Amount(oid)
					if self.valuesresources.has_key(100000):
						self.valuesresources[100000] += amount
					else:
						self.valuesresources[100000] = amount
					del self.valuesresources[resource]
						
			for resource, amount in sorted(self.valuesresources.iteritems(), key=operator.itemgetter(1), reverse=True):
				if (resource != 100000):
					self.valuesforchart += (amount,)
			
			if (self.valuesresources.has_key(100000)):
				self.valuesforchart += (self.valuesresources[100000],)
				
			if proportional*self.scale > 0:
				self[oid] = PieChart.PieChart(c.objects[oid].pos[0:2], proportional*self.scale, self.valuesforchart, Scaled=False, LineColor="Black")
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
			if self.type == Resource.TOTAL:
				for resource in o.resources:
					amount += reduce(int.__add__, resource[1:])
			else:
				for resource in o.resources:
					if resource[0] == self.type:
						amount += reduce(int.__add__, resource[1:])
			#	amount += resource[self.type]
		
		return amount
