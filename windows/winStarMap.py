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
from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_DOWN
from extra.wxFloatCanvas.FloatCanvas import Text, Polygon, Rectangle
from extra.wxFloatCanvas.CircleNoSmall import CircleNoSmall
from extra.wxFloatCanvas.PolyNoSize import PolyNoSize

# Network imports
from netlib.objects.ObjectExtra.StarSystem import StarSystem
from netlib.objects.ObjectExtra.Fleet import Fleet

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
	title = "StarMAP, The Known Universe"

	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		self.application = application

		self.Canvas = NavCanvas(self, size=wx.Size(500,500), Debug = 1, BackgroundColor = "BLACK")
		self.Canvas.ZoomToBB()

	def OnCacheUpdate(self, evt):
		self.Rebuild()

	def Rebuild(self):
		drawable = Rectangle(0,0,1,1, LineWidth=1,LineColor="White",FillColor="Black")
		drawable.data = 0
		self.Canvas.AddObject(drawable)
		drawable.Bind(EVT_FC_LEFT_DOWN, self.OnClick)
		
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
					ship = PolyNoSize([(0,0), (3,0), (0,4), (0,2), (-3,0)], LineWidth=1,LineColor="Blue",FillColor="Blue")
					ship.Move(scale(object.pos))

					C(object, ship)
					if object.vel != (0, 0, 0):
						# We need to draw in a vector
						velocity = 0
						pass
					pass

			self.arrow = PolyNoSize([(0,0), (-5,-10), (0, -8), (5,-10)], LineWidth=1,LineColor="Red",FillColor="Red")
			self.Canvas.AddObject(self.arrow)

			self.Canvas.ZoomToBB()

		except Exception, e:
			do_traceback()

	def Create(self, object, drawable):
		drawable.data = object.id

		self.Canvas.AddObject(drawable)

		drawable.Bind(EVT_FC_LEFT_DOWN, self.OnClick)
#		drawable.Bind(EVT_FC_ENTER_OBJECT, self.OnEnter)
#		drawable.Bind(EVT_FC_LEAVE_OBJECT, self.OnLeave)

	def OnClick(self, evt):
		self.application.windows.Post(wx.local.SelectObjectEvent(evt.data))

	def OnSelectObject(self, evt):
		object = self.application.cache.objects[evt.id]
		print "Selecting object", evt.id

		self.arrow.Move(scale(object.pos))
		self.Canvas.Zoom(1)
