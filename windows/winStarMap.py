"""\
This module contains the StarMap window. This window displays a view of the
universe.
"""
# Python imports
import os
from math import *

# wxPython imports
import wx
from extra.wxFloatCanvas.NavCanvas import NavCanvas
from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_DOWN, EVT_FC_RIGHT_DOWN
from extra.wxFloatCanvas.FloatCanvas import Text, Polygon, Rectangle, Line
from extra.wxFloatCanvas.CircleNoSmall import CircleNoSmall
from extra.wxFloatCanvas.PolyNoSize import PolyNoSize

# Network imports
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Fleet import Fleet
from tp.netlib.objects.OrderExtra.Move import Move

# Local imports
from winBase import *
from utils import *

#wxRED = wxColor()
wxYELLOW = wx.Color(0xD6, 0xDC, 0x2A)

POINT = 4

sysPLAIN = 1
sysOWNER = 2
sysHAB = 3
sysMIN = 4

def getpath(application, object):
	orders = application.cache.orders[object.id]
	points = [object.pos[0:2]]
	for order in orders:
		if order.type == 1:
			points += [order.pos[0:2]]
					
	if len(points) > 1:
		return points
	return None

def scale(value):
	if hasattr(value, "__getitem__"):
		r = []
		for i in value:
			r.append(scale(i))
		return r
	else:
		return round(value/(1000*1000))

# Shows the main map of the universe.
class winStarMap(winBase):
	title = _("StarMAP, The Known Universe")

	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		self.application = application

		self.Canvas = NavCanvas(self, size=wx.Size(500,500), Debug = 1, BackgroundColor = "BLACK")
		self.Canvas.ZoomToBB()

		self.cache = {}
		self.path = None

		self.mode = "Normal"

	def OnCacheUpdate(self, evt):
		self.Rebuild()

	def Rebuild(self):
		try:
			application = self.application
			C = self.Create
			
			for object in application.cache.objects.values():
				if isinstance(object, StarSystem):
					s = scale(object.size)
					x = scale(object.pos[0])
					y = scale(object.pos[1])

					# Draw an orbit
					so = round(s * 1.25)

					if len(object.contains) > 0:
						C(object, CircleNoSmall(x,y,so,10,LineWidth=1,LineColor="White",FillColor="Black"))
					else:	
						C(object, CircleNoSmall(x,y,so,10,LineWidth=1,LineColor="Black",FillColor="Black"))

					C(object, CircleNoSmall(x,y,s,4,LineWidth=1,LineColor="Yellow",FillColor="Yellow"))
					C(object, Text(object.name,x,y-100,Position="tc",Color="White",Size=8))

				if isinstance(object, Fleet):
					points = getpath(application, object)
					if points:
						C(object, Line(scale(points), LineColor="Grey"), as="path")

					parent = application.cache.objects[object.parent]
					if parent.pos == object.pos:
						continue

					# Draw the ship
					ship = PolyNoSize([(0,0), (3,0), (0,4), (0,2), (-3,0)], LineWidth=1,LineColor="Blue",FillColor="Blue")
					ship.Move(scale(object.pos))

					C(object, ship, as="icon")
						
					if object.vel != (0, 0, 0):
						# We need to draw in a vector
						velocity = 0
						pass

			self.arrow = PolyNoSize([(0,0), (-5,-10), (0, -8), (5,-10)], LineWidth=1,LineColor="Red",FillColor="Red",InForeground=True)
			self.Canvas.AddObject(self.arrow)

			self.Canvas.ZoomToBB()

		except Exception, e:
			do_traceback()

	def Create(self, object, drawable, as=None):
		drawable.data = object.id

		self.Canvas.AddObject(drawable)

		if as:
			if not self.cache.has_key(object.id):
				self.cache[object.id] = {}
		
			self.cache[object.id][as] = drawable

		drawable.Bind(EVT_FC_LEFT_DOWN, self.OnLeftClick)
		drawable.Bind(EVT_FC_RIGHT_DOWN, self.OnRightClick)

		return drawable

	def OnLeftClick(self, evt):
		if self.mode == "Position":
			pos = self.application.cache.objects[evt.obj.data].pos
			self.application.windows.Post(wx.local.SelectPositionEvent(pos))
			
			self.SetMode("Normal")
		else:
			self.application.windows.Post(wx.local.SelectObjectEvent(evt.obj.data))

	def OnRightClick(self, evt):
		obj = self.application.cache.objects[evt.obj.data]
		
		menu = wx.Menu()
		
		def ac(objects, menu, obj):
			menu.Append(obj.id, obj.name)
			for id in obj.contains:
				ac(objects, menu, objects[id])
		
		ac(self.application.cache.objects, menu, obj)

		self.Bind(wx.EVT_MENU, self.OnOrderMenu)
		self.PopupMenu(menu, evt.GetPosition())

	def OnOrderMenu(self, evt):
		menu = evt.GetEventObject()
		item = menu.FindItemById(evt.GetId())

		self.application.windows.Post(wx.local.SelectObjectEvent(evt.GetId()))
		
		if self.mode == "Position":
			self.SetMode("Normal")

	def SetMode(self, mode):
		if mode in ("Normal", "Position"):
			self.mode = mode

	def OnSelectObject(self, evt):
		object = self.application.cache.objects[evt.id]
		print "Selecting object", evt.id

		self.arrow.Move(scale(object.pos))
		if self.path:
			self.Canvas.RemoveObject(self.path)
			self.path = None

		if isinstance(object, Fleet):
			points = getpath(self.application, object)
			if points:
				self.path = self.Create(object, Line(scale(points), LineColor="Blue", InForeground=True))
	
		self.Canvas.Draw()

	def OnSelectOrder(self, evt):
		object = self.application.cache.objects[evt.id]
		
		if self.path:
			self.Canvas.RemoveObject(self.path)
			self.path = None

		if isinstance(object, Fleet):
			points = getpath(self.application, object)
			if points:
				self.path = self.Create(object, Line(scale(points), LineColor="Blue", InForeground=True))
		
			if evt.save:
				# Need to update the grey line as well
				if self.cache.has_key(evt.id) and self.cache[evt.id].has_key("path"):
					self.Canvas.RemoveObject(self.cache[evt.id]["path"])
				if points:
					self.Create(object, Line(scale(points), LineColor="Grey"), as="path")

				if self.cache.has_key(evt.id) and self.cache[evt.id].has_key("icon"):
					self.Canvas.RemoveObject(self.cache[evt.id]["icon"])
					self.Canvas.AddObject(self.cache[evt.id]["icon"])

		self.Canvas.Draw(evt.save and isinstance(object, Fleet))


