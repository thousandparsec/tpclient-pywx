"""\
This module contains the StarMap window. This window displays a view of the
universe.
"""
# Python imports
import os
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas.NavCanvas import NavCanvas

# Network imports
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet
from tp.netlib.objects.ObjectExtra.Fleet import Fleet
from tp.netlib.objects.OrderExtra.Move import Move

# Local imports
from winBase import *
from utils import *

class Overlay(dict):
	"""\
	A layer which displays something.
	"""	

	def __init__(self, canvas, cache):
		self.canvas = canvas
		self.cache  = cache

	def cleanup(self):
		"""\
		Remove this overlay from the Canvas.
		"""
		# Remove any old values
		for oid in self.keys():
			# Remove the old object
			del self[oid]

	def __setitem__(self, key, value):
		"""\
		Adds Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		if self.has_key(key):
			del self[key]

		if isinstance(value, (list, tuple)):
			for v in value:
				self.canvas.AddObject(v)
		else:
			self.canvas.AddObject(value)
		dict.__setitem__(self, key, value)

	def __delitem__(self, oid):
		"""\
		Removes Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		value = self[oid]

		if isinstance(value, (list, tuple)):
			for v in value:
				self.canvas.RemoveObject(v)
		else:
			self.canvas.RemoveObject(value)
		dict.__delitem__(self, oid)

	def update(self, oid=None):
		"""\
		Update the FloatCanvas objects for this oid.

		Called when an order on oid changes.
		"""
		if oid is None:
			self.updateall()
		else:
			# Remove the old object.
			if self.has_key(oid):
				del self[oid]

			# If the oid is no longer in the cache we shouldn't continue.
			if not c.objects.has_key(oid):
				return

			# Otherwise update the object.
			self.updateone(oid)

	def updateall(self):
		"""\
		Updates all objects on the Canvas.
		"""
		pass

	def updateone(self, oid):
		"""\
		Updates an object on the Canvas.
		"""
		pass

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

class Proportional(Overlay):
	"""\
	Draws proportional circles defined by amount.
	"""
	scale = 10000000000L

	def __init__(self, canvas, cache):
		Overlay.__init__(self, canvas, cache)

		self.max = 0
		self.min = 0

		self.fco = {}

	def amount(self, oid):
		"""\
		The absolute size of this object (non-proportional).
		"""
		return 1

	def updateall(self):
		"""\
				
		"""
		c = self.cache

		# Remove all the objects.
		self.cleanup()

		# Calculate all the values so we can figure min/max.
		values = {}
		for oid in c.objects.keys():
			values[oid] = self.amount(oid)

		# Get min/max values.
		v = values.values()
		self.min = min(v)
		self.max = max(v)

		for oid, value in values.items():
			self.updateone(oid, value)

	def updateone(self, oid, value=None):
		"""\

		"""
		c = self.cache

		if value is None:
			# Get the new value.
			value = self.amount(oid)

			# If the min/max value has changed we need to redraw everything.
			if value < self.min or value > self.max:
				self.updateall()
				return

		# New proportional value.
		proportional = value/(self.max-self.min)

		# Create the new object.
		self[oid] = FloatCanvas.Circle(c.objects[oid].pos[0:2], proportional*self.scale, FillColor="White")

class Value(Overlay):
	"""\
	Draws circles defined by a value.
	"""
	scale = 1

	def __init__(self, canvas, cache):
		Overlay.__init__(self, canvas, cache)

	def value(self, oid):
		"""\
		The absolute size of this object (non-proportional).
		"""
		return 1

	def updateall(self):
		"""\
				
		"""
		# Remove all the objects.
		self.cleanup()
		for oid in self.cache.objects.keys():
			self.updateone(oid)

	def updateone(self, oid):
		"""\

		"""
		# Create the new object.
		value = self.value(oid)
		if value is None:
			return

		self[oid] = FloatCanvas.Circle(self.cache.objects[oid].pos[0:2], self.value(oid)*self.scale, FillColor="White", LineColor="Red")

class RelativePoint(FloatCanvas.Point):
	def __init__(self, XY, Color = "Black", Diameter =  1, InForeground = False, Offset=(0,0)):
		FloatCanvas.Point.__init__(self, XY, Color, Diameter, InForeground = False)

		self.SetOffset(Offset)

	def SetOffset(self, Offset):
		self.Offset = N.array(Offset, N.float_)
		self.Offset.shape = (2,) # Make sure it is a length 2 vector

	def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
		dc.SetPen(self.Pen)
		xy = WorldToPixel(self.XY) + self.Offset
		if self.Diameter <= 1:
			dc.DrawPoint(xy[0], xy[1])
		else:
			dc.SetBrush(self.Brush)
			radius = int(round(self.Diameter/2))
			dc.DrawCircle(xy[0],xy[1], radius)
		if HTdc and self.HitAble:
			HTdc.SetPen(self.HitPen)
			if self.Diameter <= 1:
				HTdc.DrawPoint(xy[0], xy[1])
			else:
				HTdc.SetBrush(self.HitBrush)
				HTdc.DrawCircle(xy[0],xy[1], radius)

class Icon(FloatCanvas.DrawObject, FloatCanvas.XYObjectMixin):

	def __init__(self, point):
		FloatCanvas.DrawObject.__init__(self)
		self.SetPoint(point)

	def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		# See how big the real object would be on the screen..
		D = ScaleWorldToPixel(self.real[0].WH)[0]
		if D <= self.MinSize:
			things = self.icon
		else:
			things = self.real

		# Draw the things
		for i in things:
			i._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)

class OrbittedIcon(Icon):
	def __init__(self, pos):
		Icon.__init__(self, pos)

		self.children = []

	def AddChild(self, child):
		if hasattr(child, "SetCenter"):
			child.SetCenter(self.XY)

		self.children.append(child)

		# Reposition all the children.
		for i, child in enumerate(self.children):
			angle = ((2*pi)/len(self.children))*(i-0.125)
	
			x = int(cos(angle)*6)
			y = int(sin(angle)*6)

			child.SetOffset(self.XY, (x, y))

class PlanetIcon(OrbittedIcon):
	MinSize = 2

	def __init__(self, planet):
		OrbittedIcon.__init__(self, planet.pos[0:2])

		self.Size = planet.size

		self.icon = []
		self.icon.append(RelativePoint(planet.pos[0:2], "Blue", 3))

		self.real = []

	def SetOffset(self, point, offset):
		for icon in self.icon:
			if hasattr(icon, "SetOffset"):
				icon.SetPoint(point)
				icon.SetOffset(offset)

	def SetCenter(self, center):
		# Figure out the "orbit"
		diameter = 2*sqrt((self.XY[0]-center[0])**2 + (self.XY[1]-center[1])**2)

		print self, center, self.XY, diameter, self.Size
	
		# The actual planet (FIXME: *1000 should be needed...)
		self.real.append(FloatCanvas.Circle(self.XY, self.Size*1000, LineColor="White", FillColor="White"))
		# The "orbit" of the planet
		self.real.append(FloatCanvas.Circle(center, diameter, LineColor="Blue"))

class SystemIcon(OrbittedIcon):
	"""
	An object which can only become so small before it reverts to "Icon" form.
	"""
	MinSize = 8

	def __init__(self, starsystem):
		OrbittedIcon.__init__(self, starsystem.pos[0:2])

		self.children = []

		# Icon form consists of a central point, plus a circle plus a bunch of planet points
		self.icon = []
		self.icon.append(FloatCanvas.Point(starsystem.pos[0:2], "Yellow", 4))

		self.real = []
		self.real.append(FloatCanvas.Circle(starsystem.pos[0:2], starsystem.size, LineColor="Red"))

	def AddChild(self, child):
		# If this is the first child, add the orbit indicater
		if len(self.children) == 0:
			self.icon.insert(0, FloatCanvas.Point(self.XY, "Black", 8))
			self.icon.insert(0, FloatCanvas.Point(self.XY, "White", 9))

		OrbittedIcon.AddChild(self, child)

class Systems(Value):
	def updateone(self, oid):
		"""\

		"""
		obj = self.cache.objects[oid]

		if isinstance(obj, StarSystem):
			fc = []
			def pin(obj, cache=self.cache, fc=fc):
				if isinstance(obj, (Planet, Fleet)):
					o = PlanetIcon(obj)
					fc.append(o)

				if isinstance(obj, (StarSystem,)):
					o = SystemIcon(obj)
					fc.append(o)

				for child in obj.contains:
					r = pin(cache.objects[child])

					if hasattr(o, "AddChild"):
						if r != None:
							o.AddChild(r)
				return o

			pin(obj)

			self[oid] = fc

class Resource(Proportional):
	"""\
	Draws proportional circles for the relative number of resources.
	"""
	TOTAL		= -1
	SURFACE	  = 1
	MINABLE	  = 2
	INACCESSABLE = 3	

	def __init__(self, canvas, cache, resource, type=-1):
		Overlay.__init__(self, canvas, cache)

		self.resource = resource
		self.type     = type
	
	def amount(self, oid):
		"""\
		The amount of this resource on this object.
		"""
		c = self.cache 
		o = c.objects[oid]

		amount = 0
		if hasattr(self, "contains"):
			for child in o.contains:
				amount += self.amount(child)

		if hasattr(self, "resources"):
			for resource in o.resources:
				rid = resource[0]

				if rid == self.resource:
					if self.type == Resource.TOTAL:
						amount += reduce(int.__add__, resource[1:])
					else:
						amount += resouce[self.type]
					break

		return amount

class Size(Value):
	"""\
	Draws proportional circles for the relative to size of object.
	"""
	def value(self, oid):
		"""\
		The amount of this resource on this object.
		"""
		obj = self.cache.objects[oid]
		if isinstance(obj, (Planet, StarSystem)):
			return obj.size

# Shows the main map of the universe.
class panelStarMap(wx.Panel):
	title = _("StarMap")

	def __init__(self, application, parent):
		wx.Panel.__init__(self, parent)

		self.application = application

		self.Navigator = NavCanvas(self, Debug = 1, BackgroundColor="black")
		self.Navigator.ZoomToFit(None)
		self.Canvas = self.Navigator.Canvas

#		self.Canvas = FloatCanvas.FloatCanvas(self, BackgroundColor="black")
		self.Overlays = []

		self.Bind(wx.EVT_SIZE, self.OnSize)
#		self.Bind(wx.EVT_ACTIVATE, self.OnShow)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.Center()
		info.PinButton(True)
		info.MaximizeButton(True)
		return info

	def OnShow(self, evt):
		self.Canvas.Draw()

	def OnSize(self, evt):
#		self.Canvas.SetSize(self.GetClientSize())
		self.Navigator.SetSize(self.GetClientSize())
#		self.Canvas.OnSize(evt)
		self.Canvas.ZoomToBB()
#		self.Canvas.ZoomToBB()

	def OnCacheUpdate(self, evt):
		"""\
		Called when the cache has been updated.
		"""
		print self.application
		print self.application.cache
		self.Overlay = Systems(self.Canvas, self.application.cache)
		self.Overlay.update()

	def OnSelectObject(self, evt):
		"""\
		Called when an object is selected.
		"""
		pass

	def OnUpdateOrder(self, evt):
		"""\
		Called when an order is updated.
		"""
		pass

	def OnDirtyOrder(self, evt):
		"""\
		Called when the order has been updated but not yet saved.
		"""
		pass
