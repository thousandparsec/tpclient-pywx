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

from Proportional import SystemIcon, FindChildren, IconMixIn

from Overlay import SystemLevelOverlay, Holder

from extra import objectutils

from windows.xrc.winResourceSelect import ResourceSelectBase
class ResourceSelect(ResourceSelectBase, wx.Frame):
	"""\
	This class is a popup window with a checklist of resources.
	"""
	def __init__(self, parent, cache):
		"""\
		Initialize the window, loading data from XRC, and add the resources.
		"""
		ResourceSelectBase.__init__(self, parent)
		self.parent = parent
		
		self.ResourceTypeList = {}
		
		for number, resource in cache.resources.items():
			self.ResourceTypeList[resource.name] = number
		self.ResourceList.InsertItems(self.ResourceTypeList.keys(), 0)

		self.Bind(wx.EVT_ACTIVATE, self.OnActivate)
		self.Hide()
	
	def OnActivate(self, evt):
		"""\
		Called when the window becomes active or inactive.
		"""
		if evt.GetActive() == False:
			self.OnDone(evt)

	def Show(self, show=True):
		"""\
		Called when the window is shown.
		"""
		self.Panel.Layout()

		size = self.ResourceList.GetBestSize()
		self.ResourceList.SetMinSize(size)

		self.SetMinSize(size)
		self.SetSize(size)
		self.SetMaxSize(size)

		wx.Frame.Show(self)

	def OnDone(self, evt):
		"""\
		Called when the "Done" button is pressed.
		"""
		self.parent.PopDown()

class RsrcSelectorControl(wx.Button):
	"""\
	This class is a button that can be clicked to open a checklist of resources,
	and which takes the data from that window to create a list of the checked
	resources.
	"""
	def __init__(self, resourceview, cache, parent, id):
		"""\
		Called to create the button and the popup window.
		"""
		wx.Button.__init__(self, parent, id, "Resource Types")

		self.Bind(wx.EVT_BUTTON, self.OnClick)
		self.cache = cache
		self.resourceview = resourceview
		self.selected = []
		self.win = ResourceSelect(self, cache)
	
	def OnClick(self, evt):
		"""\
		Called when the button is clicked.
		"""
		if not self.win.IsShown():
			self.win.Move(self.GetScreenRect().GetBottomLeft())
			self.win.Show()
		else:
			self.PopDown()
		
	def PopDown(self):
		"""\
		Closes the popup window and collects the data.
		"""
		self.selected=[]
		self.win.Hide()

		for i in range(0, self.win.ResourceList.GetCount()):
			if self.win.ResourceList.IsChecked(i):
				self.selected.append(self.win.ResourceTypeList[self.win.ResourceList.GetString(i)])
		
		self.resourceview.CleanUp()
		self.resourceview.UpdateAll()
		self.resourceview.canvas.Draw()

class RsrcSelectorPanel(wx.Panel):
	"""\
	A simple panel containing a button that can be clicked to bring up a list of
	resources. This is for use with the Resource overlay.
	"""
	def __init__(self, resourceview, parent, cache):
		"""\
		Creates the panel and its contents.
		"""
		wx.Panel.__init__(self, parent, -1)
		self.selector = RsrcSelectorControl(resourceview, cache, self, -1)

class PieChartIcon(SystemIcon):
	"""\
	This class represents a pie chart, which holds a list of slices and their
	proportions, as well as an overall scale.
	"""
	def copy(self):
		"""\
		Copies the pie chart.
		"""
		return PieChartIcon(self.cache, self.primary, self.proportional, self.scale, self.valuesforchart)

	def __init__(self, cache, system, proportional, scale, valuesforchart):
		"""\
		Creates a new pie chart, initializing the slices.
		"""
		self.cache = cache
		self.proportional = proportional
		self.scale = scale
		self.valuesforchart = valuesforchart
		
		Holder.__init__(self, system, FindChildren(cache, system))

		# Create a list of the objects
		ObjectList = []

		# The center point
		positionlist = objectutils.getPositionList(system)
		if len(positionlist) <= 0:
			return
		
		# FIXME: Should we just use the first position here?
		position = positionlist[0]
		if (self.proportional*self.scale != 0 and self.valuesforchart != ()):
			ObjectList.append(PieChart.PieChart(positionlist[0][0:2], self.proportional*self.scale, self.valuesforchart, Scaled=False, LineColor="Black"))
		else:
			ObjectList.append(PieChart.PieChart(positionlist[0][0:2], .0001, (1,1), Scaled=False, LineColor="Black"))

		Group.__init__(self, ObjectList, False)

from Proportional import Proportional

class Resource(Proportional):
	"""\
	This overlay draws proportional pie charts representing the relative
	resource totals in different star systems. The chart shows all resources by
	default, but the user can select specific resources to be displayed as well.
	When the user hovers over a pie chart, a tooltip will be displayed showing
	exact totals for each resource.
	"""
	name = "Resources"

	TOTAL		= -1
	SURFACE		 =  1
	MINABLE		 =  2
	INACCESSABLE =  3	

	def __init__(self, parent, canvas, panel, cache, resource=None, type=-1):
		"""\
		Initializes the overlay and its resource selection panel.
		"""
		Proportional.__init__(self, parent, canvas, panel, cache)
		
		self.ResourceTypeList = {"All":Resource.TOTAL}
		
		for number, resource in cache.resources.items():
			self.ResourceTypeList[resource.name] = number

		self.resource = resource
		self.type	 = type
		
		# Create a drop-down on the panel for resource selection
		sizer = wx.FlexGridSizer(len(self.ResourceTypeList))
		self.selectpanel = RsrcSelectorPanel(self, panel, cache)
		sizer.Add(self.selectpanel, proportion=1, flag=wx.EXPAND)
		
		sizer.AddGrowableRow(0)
		panel.SetSizer(sizer)
		
		self.UpdateAll()
		self.canvas.Draw()
		
	def UpdateAll(self):
		"""\
		Updates all of the pie charts.
		"""
		Proportional.UpdateAll(self)
		
	def UpdateOne(self, oid, value=None):
		"""\
		Updates a specific pie chart.
		"""
		proportional = Proportional.UpdateOne(self, oid)
			
	def Icon(self, obj):
		"""\
		Creates a pie chart icon that shows the resources that are currently
		selected, for a specific system.
		"""
		proportional = Proportional.Proportion(self, obj.id)
		c = self.cache 
		o = obj
		self.valuesforchart = ()
		self.valuesresources = {}
		
		if o.subtype != 2:
			pass
			return PieChartIcon(self.cache, obj, 0.001, 1, (1,1))
		
		if not hasattr(o, "contains"):
			pass
			return PieChartIcon(self.cache, obj, 0.001, 1, (1,1))
			
		for child in o.contains:
			if not objectutils.hasResources(c, child):
				continue
				
			for resource in objectutils.getResources(c, child):
				if sum(resource[1:]) == 0:
					continue
					
				if len(self.selectpanel.selector.selected) != 0 and not resource[0] in self.selectpanel.selector.selected:
					continue
					
				if self.valuesresources.has_key(resource[0]):
					self.valuesresources[resource[0]] += sum(resource[1:])
				else:
					self.valuesresources[resource[0]] = sum(resource[1:])
		
		smallresources = 0
		for resource, amount in self.valuesresources.items():
			if amount > (self.Amount(obj.id) * .10):
				continue
				
			smallresources += amount
			
			del self.valuesresources[resource]
					
		for resource, amount in sorted(self.valuesresources.iteritems(), key=operator.itemgetter(1), reverse=True):
			self.valuesforchart += (amount,)
		
		if smallresources != 0:
			self.valuesforchart += (smallresources,)
			
		if proportional*self.scale > 0:
			return PieChartIcon(self.cache, obj, proportional, self.scale, self.valuesforchart)
		else:
			return PieChartIcon(self.cache, obj, 0.001, 1, (1,1))

	def Amount(self, oid):
		"""\
		The amount of a specific resource in a specific object.
		"""
		c = self.cache 
		o = c.objects[oid]

		amount = 0
		if hasattr(o, "contains"):
			for child in o.contains:
				amount += self.Amount(child)

		if objectutils.hasResources(c, oid):
			resources = objectutils.getResources(c, oid)
			if self.type == Resource.TOTAL:
				for resource in resources:
					amount += sum(resource[1:])
			else:
				for resource in resources:
					if resource[0] == self.type:
						amount += sum(resource[1:])
		
		return amount
	
	def ObjectPopupText(self, icon):
		"""\
		Creates the text for the tooltip on a pie chart.
		"""
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
			
			if len(self.selectpanel.selector.selected) != 0:
				returnstring += "\n " + child.name + ":"
			
			for resource in objectutils.getResources(self.cache, c):
				if sum(resource[1:]) <= 0:
					continue
					
				if len(self.selectpanel.selector.selected) == 0:
					if valuesresources.has_key(resource[0]):
						valuesresources[resource[0]] += sum(resource[1:])
					else:
						valuesresources[resource[0]] = sum(resource[1:])
				else:
					if not resource[0] in self.selectpanel.selector.selected:
						continue
						
					thisresourcetotal += sum(resource[1:]) 
				 	returnstring += "\n  " + self.cache.resources[resource[0]].name \
				 		+ ": %s " % sum(resource[1:]) \
				 		+ [self.cache.resources[resource[0]].unit_singular, self.cache.resources[resource[0]].unit_plural] \
				 		[sum(resource[1:]) > 1]
	
		if not self.type == Resource.TOTAL:
			returnstring += "\n\nTotal " + self.cache.resources[self.type].name + " in system: %s" % thisresourcetotal
		else :
			for resource, amount in sorted(valuesresources.iteritems(), key=operator.itemgetter(1), reverse=True):	
				returnstring += "\n  " + self.cache.resources[resource].name + \
					": %s " % amount + \
					[self.cache.resources[resource].unit_singular, self.cache.resources[resource].unit_plural][amount > 1]
		
		return returnstring + "</font>"
