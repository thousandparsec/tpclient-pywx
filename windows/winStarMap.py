"""\
This module contains the StarMap window. This window displays a view of the
universe.
"""
# Python imports
import os
from math import *

# wxPython imports
from wxPython.wx import *
from wxPython.lib.floatbar import *
from extra.wxFloatCanvas.NavCanvas import NavCanvas
from extra.wxFloatCanvas.Dot import Dot

from netlib.objects.ObjectExtra.StarSystem import StarSystem
from netlib.objects.ObjectExtra.Fleet import Fleet

from utils import *
from winBase import winBase

#wxRED = wxColor()
wxYELLOW = wxColor(0xD6, 0xDC, 0x2A)

POINT = 4

sysPLAIN = 1
sysOWNER = 2
sysHAB = 3
sysMIN = 4

# Shows the main map of the universe.
class winStarMap(winBase):
	title = "StarMAP, The Known Universe"

	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		self.application = application

		self.CreateStatusBar()
		self.SetStatusText("")

		self.Canvas = NavCanvas(self, size=(500,500), Debug = 1, BackgroundColor = "BLACK")
		self.Canvas.ZoomToBB()

		EVT_ACTIVATE(self, self.OnFocus)

	def OnFocus(self, evt):
		application = self.application
		
		for object in application.cache.values():
			if isinstance(object, StarSystem):
				s = round(object.size/(1000*100))
				x = round(object.pos[0]/(1000*1000))
				y = round(object.pos[1]/(1000*1000))

				# Draw an orbit
				if len(object.contains) > 0:
					so = round(s * 1.25)
					self.Canvas.AddCircleNoSmall(x,y,so,10,LineWidth=1,LineColor="White",FillColor="Black")
					
				self.Canvas.AddCircleNoSmall(x,y,s,4,LineWidth=1,LineColor="Yellow",FillColor="Yellow")
				self.Canvas.AddText(object.name,x,y-100,Position="tc",Color="White",Size=8)

			if isinstance(object, Fleet):
				if object.vel != (0, 0, 0):
					# We need to draw in a vector
					pass
				pass
				
#		# Tool bar to select what is shown on the starmap
#		self.barTool = wxFloatBar(self, -1)
#		self.SetToolBar(self.barTool)
#		self.barTool.SetFloatable(1)
#		self.barTool.SetTitle("StarMAP: Toolbar")
#		self.barTool.AddSeparator()

#		# This bar displays the current X/Y coordinates of the mouse cursor.
#		class starStatusBar(wxStatusBar):
#			def __init__(self, parent):
#				wxStatusBar.__init__(self, parent, -1)
#				self.SetFieldsCount(4)
#				self.sizeChanged = false
#				EVT_SIZE(self, self.OnSize)
#				EVT_IDLE(self, self.OnIdle)
#
#				self.SetStatusText("StarMAP!", 0)
#
#				# The columns are as follows, Text, Object Name, X/Y Position, Distance from Selected
#				# The current object Name
#				self.name = None
#				# The x/y position
#				self.position = None
#				# Distance from selected
#				self.distance = None
#
#			# Time-out handler
#			def Notify(self):
#				pass
#
#			def OnSize(self, evt):
#				self.Reposition()  # for normal size events
#				self.sizeChanged = TRUE
#
#			def OnIdle(self, evt):
#				if self.sizeChanged:
#					self.Reposition()
#
#			# reposition the objects
#			def Reposition(self):
#				rect = self.GetFieldRect(1)
#				self.sizeChanged = false
#
#		# The Status bar
#		self.barStatus = starStatusBar(self)
#
#
#		class starCanvas(wxScrolledWindow):
#			def __init__(self, parent, id = -1, size = wxDefaultSize):
#				wxScrolledWindow.__init__(self, parent, id, wxPoint(0, 0), size, wxSUNKEN_BORDER)
#
#				self.parent = parent
#
#				self.parent.start = [0,0]
#				self.parent.end = [0,0]
#
#				self.maxWidth  = 3000
#				self.maxHeight = 3000
#				
#				self.SetBackgroundColour(wxBLACK)
#				self.SetCursor(wxStockCursor(wxCURSOR_CROSS))
#				self.SetScrollbars(20, 20, self.maxWidth/20, self.maxHeight/20)
#
#				EVT_PAINT(self, self.OnPaint)
#
#				EVT_LEFT_DOWN(self, self.OnLeftDown)
#				EVT_LEFT_UP(self, self.OnLeftUp)
#				EVT_RIGHT_UP(self, self.OnRightUp)
#				EVT_MOTION(self, self.OnMotion)
#
#			def OnMotion(self, evt):
#				"""
#				Called when the mouse is in motion.  If the left button is
#				dragging then draw a line from the last event position to the
#				current one.  Save the coordinants for redraws.
#				"""
#				if evt.Dragging() and evt.LeftIsDown():
#					dc = wxClientDC(self)
#					self.PrepareDC(dc)
#
#					self.parent.RenderDrag(dc)
#
#					start = self.parent.start
#					end = self.ConvertEventCoords(evt)
#					self.parent.end = end
###					x,y = self.GetViewStart()
###					h,w = self.GetClientSize()
###					px, py = self.GetScrollPixelsPerUnit()
#
#					self.parent.SetStatusText("%i PC" % (sqrt((start[0]-end[0])**2+(start[1]-end[1])**2)), 3)
#					
#					self.parent.RenderDrag(dc)
#				
#				self.parent.SetStatusText("X: %i, Y: %i, Z: 0" % self.ConvertEventCoords(evt), 2)
#
#			def OnLeftDown(self, evt):
#				"""called when the left mouse button is pressed"""
#				#print evt.GetX(), evt.GetY()
#				#print self.ConvertEventCoords(evt)
#				self.parent.start = self.ConvertEventCoords(evt)
#				self.end = self.parent.start
#				self.CaptureMouse()
#				self.parent.dragging = 1
#
#				dc = wxClientDC(self)
#				self.PrepareDC(dc)
#				self.parent.RenderDrag(dc)
#
#			def OnLeftUp(self, evt):
#				"""called when the left mouse button is released"""
#				dc = wxClientDC(self)
#				self.PrepareDC(dc)
#				self.parent.RenderDrag(dc)
#				
#				self.parent.dragging = 0
#				self.ReleaseMouse()
#
#				# Call the approiate call
#				
#
#		self.canvas = starCanvas(self)

#	def RenderDrag(self, dc):
#		#######################
#		# Draw the selector
#		#######################
#		# Draw a line between start and finish
#		if self.dragging:
#			dc.SetBrush(wxTRANSPARENT_BRUSH)
#			dc.SetLogicalFunction(wxINVERT)
#			dc.DrawLine(self.start[0], self.start[1], self.end[0], self.end[1])
#
#	def Update(self, evt=None):
#		self.canvas.OnPaint(None)	
#		
#	# Recenter onto the selected object
#	def OnSelect(self, evt):
#		zoom = self.config['Zoom']
#		id = evt.value
#		
#		# The object that was selected.
#		object = self.app.game.universe.Object(id)
#
#		if object:
#			pos = [ object.pos[X]/zoom + 1500, object.pos[Y]/zoom + 1500 ]
#			
#			# Center on this position
#			cx, cy = self.canvas.GetClientSize()
#			px, py = self.canvas.GetScrollPixelsPerUnit()
#		
#			pos = [(pos[0] - cx/2)/px, (pos[1] - cy/2)/py]
#
#			self.canvas.Scroll(pos[0], pos[1])
#
