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
from extra.wxFloatCanvas.FloatCanvas   import Point, Group, Line

import operator

from extra.wxFloatCanvas.NavCanvas import NavCanvas

from Proportional import SystemIcon, FindChildren

from Overlay import SystemLevelOverlay, Holder

import  wx.lib.popupctl as popupctrl
import  wx.calendar as calendar

from windows.xrc.winResourceSelect import ResourceSelectBase
class ResourceSelect(ResourceSelectBase):
	def __init__(self, parent):
		ResourceSelectBase.__init__(self, parent)

class ResourceSelectorControl(popupctrl.PopupControl):
    def __init__(self,*_args,**_kwargs):
        apply(popupctrl.PopupControl.__init__,(self,) + _args,_kwargs)

        self.win = ResourceSelect(self)

        #bz = self.rsrclist.GetBestSize()
        #self.win.SetSize(bz)

        # This method is needed to set the contents that will be displayed
        # in the popup
        self.SetPopupContent(self.win)

        # Event registration for selection finished
        #self.rsrclist.Bind()

    # Method called when a day is selected in the calendar
    def OnRsrcSelected(self,evt):
        self.PopDown()
        evt.Skip()

    # Method overridden from PopupControl
    # This method is called just before the popup is displayed
    # Use this method to format any controls in the popup
    def FormatContent(self):
        pass
            
class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)
        date = ResourceSelectorControl(self, -1, pos = (0,0), size = (100,22))

class PieChartIcon(SystemIcon):
	def copy(self):
		return PieChartIcon(self.cache, self.primary, self.proportional, self.scale, self.valuesforchart)

	def __init__(self, cache, system, proportional, scale, valuesforchart):
		self.cache = cache
		self.proportional = proportional
		self.scale = scale
		self.valuesforchart = valuesforchart
		
		Holder.__init__(self, system, FindChildren(cache, system))

		# Create a list of the objects
		ObjectList = []

		# The center point
		ObjectList.append(PieChart.PieChart(system.pos[0:2], self.proportional*self.scale, self.valuesforchart, Scaled=False, LineColor="Black"))

		Group.__init__(self, ObjectList, False)

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
		
		# Create a drop-down on the panel for resource selection
		#self.ResourceSelector = wx.Choice(panel)
		#self.ResourceSelector.Bind(wx.EVT_CHOICE, self.OnResourceSelected)

		sizer = wx.FlexGridSizer(len(self.ResourceTypeList))
		sizer.Add(TestPanel(panel, None), proportion=1, flag=wx.EXPAND)
		# Populate the dropdown with information
		#for name, resource in sorted(self.ResourceTypeList.items(), key=operator.itemgetter(1)):
			#nametext = wx.StaticText(panel, -1, name)
			#sizer.Add(nametext, proportion=1, flag=wx.EXPAND)
		#self.ResourceSelector.SetSelection(0)
		
		sizer.AddGrowableRow(0)
		#sizer.Add(self.ResourceSelector, proportion=1, flag=wx.EXPAND)
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
			
	def Icon(self, obj):
		proportional = Proportional.Proportion(self, obj.id)
		#self.valuesforchart = ()
		c = self.cache 
		o = obj
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
				if amount < (self.Amount(obj.id) * .10):
					#print amount, self.Amount(oid)
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
				pass
				return PieChartIcon(self.cache, obj, proportional, self.scale, self.valuesforchart)
				#self[oid] = PieChart.PieChart(c.objects[oid].pos[0:2], proportional*self.scale, self.valuesforchart, Scaled=False, LineColor="Black")
			else:
				pass
				return PieChartIcon(self.cache, obj, 0.001, 1, (1,1))
		else:
			pass
			return PieChartIcon(self.cache, obj, 0.001, 1, (1,1))

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
	
	def ObjectPopupText(self, icon):
		returnstring = "<font size='%s' color='White'>" % wx.local.normalFont.GetPointSize()
		system = icon.primary
		returnstring += system.name
		returnstring += ":\nTotal (for all resources) In System: "
		temptype = self.type
		self.type = Resource.TOTAL
		returnstring += "%s" % self.Amount(system.id)
		self.type = temptype
		
		valuesresources = {}
		thisresourcetotal = 0
		
		for c in system.contains:
			child = self.cache.objects[c]
			if not self.type == Resource.TOTAL:
				returnstring += "\n " + child.name + ":"
			if hasattr(child, "resources"):
				for resource in child.resources:
					if reduce(int.__add__, resource[1:]) > 0:
						if self.type == Resource.TOTAL:
							if valuesresources.has_key(resource[0]):
								valuesresources[resource[0]] += reduce(int.__add__, resource[1:])
							else:
								valuesresources[resource[0]] = reduce(int.__add__, resource[1:])
						else:
							if resource[0] == self.type:
								thisresourcetotal += reduce(int.__add__, resource[1:]) 
							 	returnstring += "\n  " + self.cache.resources[resource[0]].name \
							 		+ ": %s " % reduce(int.__add__, resource[1:]) \
							 		+ [self.cache.resources[resource[0]].unit_singular, self.cache.resources[resource[0]].unit_plural] \
							 		[reduce(int.__add__, resource[1:]) > 1]
	
		if not self.type == Resource.TOTAL:
			returnstring += "\n\nTotal " + self.cache.resources[self.type].name + " in system: %s" % thisresourcetotal
		else :
			for resource, amount in sorted(valuesresources.iteritems(), key=operator.itemgetter(1), reverse=True):	
				returnstring += "\n  " + self.cache.resources[resource].name + \
					": %s " % amount + \
					[self.cache.resources[resource].unit_singular, self.cache.resources[resource].unit_plural][amount > 1]
		
		return returnstring + "</font>"