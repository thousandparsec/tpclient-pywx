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
from extra.wxFloatCanvas.CrossLine import CrossLine

# Network imports
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Fleet import Fleet

# Local imports
from winBase import *
from utils import *

MOVE_TYPE = 1

def getpath(application, object, overrides={}):
	"""\
	Returns a set of points which show the path of the object.
	"""
	orders = application.cache.orders[object.id]
	points = [object.pos[0:2]]

	for slot in range(0, len(orders)):
		if not overrides.has_key(slot):
			order = orders[slot]
		else:
			order = overrides[slot]

		if order._subtype == MOVE_TYPE:
			points += [order.pos[0:2]]
	
	if len(points) > 1:
		return points
	return None

def scale(value):
	"""\
	Scales the positions to a better size.
	"""
	if hasattr(value, "__getitem__"):
		r = []
		for i in value:
			r.append(scale(i))
		return r
	else:
		return round(value/(1000*1000))

# Shows the main map of the universe.
class winStarMap(winBase):
	title = _("StarMap")

	from defaults import winStarMapDefaultPosition as DefaultPosition
	from defaults import winStarMapDefaultSize as DefaultSize
	from defaults import winStarMapDefaultShow as DefaultShow

	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		self.application = application

		self.Canvas = NavCanvas(self, size=wx.Size(500,500), Debug = 1, BackgroundColor = "BLACK")
		self.Canvas.ZoomToBB()

		self.cache = {}
		self.path = None

		self.mode = "Normal"
		self.current = -1

	def Rebuild(self):
		try:
			self.RemovePath()
			self.Canvas.ClearAll()
		
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
						C(object, Line(scale(points), LineColor="Grey", InForeground=True), as="path")
					elif object.vel != (0, 0, 0):
						C(object, CrossLine(scale(object.pos[0:2]), scale(object.vel[0:2]), 3, LineColor="Grey"), as="path")
						
					parent = application.cache.objects[object.parent]
					if parent.pos == object.pos:
						continue

					# Draw the ship
					ship = PolyNoSize([(0,0), (3,0), (0,4), (0,2), (-3,0)], LineWidth=1,LineColor="Blue",FillColor="Blue")
					ship.Move(scale(object.pos))

					C(object, ship, as="icon")

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
			self.application.Post(self.application.gui.SelectPositionEvent(pos))
			
			self.SetMode("Normal")
		else:
			self.application.Post(self.application.gui.SelectObjectEvent(evt.obj.data))

	def OnRightClick(self, evt):
		obj = self.application.cache.objects[evt.obj.data]
		
		menu = wx.Menu()
		
		def ac(objects, menu, obj):
			menu.Append(obj.id, obj.name)
			for id in obj.contains:
				ac(objects, menu, objects[id])
		
		ac(self.application.cache.objects, menu, obj)

		self.Bind(wx.EVT_MENU, self.OnContextMenu)
		self.PopupMenu(menu, evt.GetPosition())

	def OnContextMenu(self, evt):
		menu = evt.GetEventObject()
		item = menu.FindItemById(evt.GetId())

		if self.mode == "Position":
			pos = self.application.cache.objects[evt.GetId()].pos
			self.application.Post(self.application.gui.SelectPositionEvent(pos))
			
			self.SetMode("Normal")
		else:
			self.application.Post(self.application.gui.SelectObjectEvent(evt.GetId()))

	def SetMode(self, mode):
		if mode in ("Normal", "Position"):
			if mode == "Position":
				self.Canvas.Canvas.SetCursor(wx.StockCursor(wx.CURSOR_CROSS))
			else:
				self.Canvas.Canvas.SetCursor(wx.StockCursor(wx.CURSOR_DEFAULT))
			
			self.mode = mode

	####################################################
	# Remote Event Handlers
	####################################################
	def RemovePath(self):
		if self.path != None:
			print "Removing Path", self.path
			self.Canvas.RemoveObject(self.path)
			self.path = None

	def SetPath(self, path):
		self.RemovePath()

		print "Setting path", path
		self.path = path

	def OnCacheUpdate(self, evt):
		"""\
		Called when the cache has been updated.
		"""
		print self, "OnCacheUpdate"
		if evt.what is None:
			self.Rebuild()
			return

		if evt.what is "orders":
			self.OnUpdateOrder(evt.change)

	def OnSelectObject(self, evt):
		"""\
		Called when an object is selected.
		"""
		print self, "OnSelectObject"
		if evt.id == self.current:
			return
		self.current = evt.id

		object = self.application.cache.objects[evt.id]

		self.arrow.Move(scale(object.pos))
		if isinstance(object, Fleet):
			points = getpath(self.application, object)
			if points:
				path = self.Create(object, Line(scale(points), LineColor="Blue", InForeground=True))
				self.SetPath(path)
			elif object.vel != (0, 0, 0): 
				path = self.Create(object, CrossLine(scale(object.pos[0:2]), scale(object.vel[0:2]), 3, LineColor="Blue", InForeground=True))
				self.SetPath(path)
				
		self.Canvas.Draw()

	def OnUpdateOrder(self, evt):
		"""\
		Called when an order is updated.
		"""
		object = self.application.cache.objects[evt.id]

		self.arrow.Move(scale(object.pos))

		self.RemovePath()
		if isinstance(object, Fleet):
			points = getpath(self.application, object)

#			if self.cache.has_key(evt.id) and self.cache[evt.id].has_key("path"):
#				self.Canvas.RemoveObject(self.cache[evt.id]["path"])

			# Update the lines
			if points:
				self.Create(object, Line(scale(points), LineColor="Grey", InForeground=True), as="path")

				path = self.Create(object, Line(scale(points), LineColor="Blue", InForeground=True))
				self.SetPath(path)
				
			# Put the Icon ontop
			if self.cache.has_key(evt.id) and self.cache[evt.id].has_key("icon"):
				self.Canvas.RemoveObject(self.cache[evt.id]["icon"])
				self.Canvas.AddObject(self.cache[evt.id]["icon"])

		self.Canvas.Draw()

	def OnDirtyOrder(self, evt):
		"""\
		Called when the order has been updated but not yet saved.
		"""
		object = self.application.cache.objects[evt.id]
		order = self.application.cache.orders[evt.id][evt.slot]
		
		if self.path == None:
			return

		if isinstance(object, Fleet) and order._subtype == MOVE_TYPE:
			points = getpath(self.application, object, {evt.slot: evt.order})
			if not points:
				return
			
			path = self.Create(object, Line(scale(points), LineColor="Blue", InForeground=True))
			self.SetPath(path)
			
			self.Canvas.Draw()
			
