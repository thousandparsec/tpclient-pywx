"""\
This module contains the StarMap window. This window displays a view of the
universe.
"""

import os
from math import *

from winBase import winBase

from wxPython.wx import *
from wxPython.lib.floatbar import *

#wxRED = wxColor()
wxYELLOW = wxColor(0xD6, 0xDC, 0x2A)

POINT = 4

sysPLAIN = 1
sysOWNER = 2
sysHAB = 3
sysMIN = 4

systems = []

# Shows the main map of the universe.
class winStarMap(winBase):
	title = "StarMAP, The Known Universe"

	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		self.config = {}
		self.config['System'] = sysPLAIN
		self.config['DrawNames'] = TRUE
		self.config['Scanner'] = TRUE
		self.config['Ships'] = TRUE
		self.config['Zoom'] = 0.5

		self.dragging = 0

		# This bar displays the current X/Y coordinates of the mouse cursor.
		class starStatusBar(wxStatusBar):
			def __init__(self, parent):
				wxStatusBar.__init__(self, parent, -1)
				self.SetFieldsCount(4)
				self.sizeChanged = false
				EVT_SIZE(self, self.OnSize)
				EVT_IDLE(self, self.OnIdle)

				self.SetStatusText("StarMAP!", 0)

				# The columns are as follows, Text, Object Name, X/Y Position, Distance from Selected
				# The current object Name
				self.name = None
				# The x/y position
				self.position = None
				# Distance from selected
				self.distance = None

			# Time-out handler
			def Notify(self):
				pass

			def OnSize(self, evt):
				self.Reposition()  # for normal size events

				# Set a flag so the idle time handler will also do the repositioning.
				# It is done this way to get around a buglet where GetFieldRect is not
				# accurate during the EVT_SIZE resulting from a frame maximize.
				self.sizeChanged = TRUE

			def OnIdle(self, evt):
				if self.sizeChanged:
					self.Reposition()

			# reposition the objects
			def Reposition(self):
				rect = self.GetFieldRect(1)
				self.sizeChanged = false


		# The Status bar
		self.barStatus = starStatusBar(self)
		self.SetStatusBar(self.barStatus)

		# Tool bar to select what is shown on the starmap
		self.barTool = wxFloatBar(self, -1)
		self.SetToolBar(self.barTool)
		self.barTool.SetFloatable(1)
		self.barTool.SetTitle("StarMAP: Toolbar")
		self.barTool.AddSeparator()

		# Now to create a canvas
		class starCanvas(wxScrolledWindow):
			def __init__(self, parent, id = -1, size = wxDefaultSize):
				wxScrolledWindow.__init__(self, parent, id, wxPoint(0, 0), size, wxSUNKEN_BORDER)

				self.parent = parent

				self.parent.start = [0,0]
				self.parent.end = [0,0]

				self.maxWidth  = 10000/self.parent.config['Zoom']
				self.maxHeight = 10000/self.parent.config['Zoom']
				
				self.SetBackgroundColour(wxBLACK)
				self.SetCursor(wxStockCursor(wxCURSOR_CROSS))
				self.SetScrollbars(20, 20, self.maxWidth/20, self.maxHeight/20)

				EVT_PAINT(self, self.OnPaint)

				EVT_LEFT_DOWN(self, self.OnLeftDown)
				EVT_LEFT_UP(self, self.OnLeftUp)
				EVT_RIGHT_UP(self, self.OnRightUp)
				EVT_MOTION(self, self.OnMotion)

			def OnPaint(self, evt):
				#print "On paint!"
				dst = wxPaintDC(self)
				self.PrepareDC(dst)

				x,y = self.GetViewStart()
				h,w = self.GetClientSize()
				px, py = self.GetScrollPixelsPerUnit()
				self.parent.RenderMap((x*px, y*py), (x*px+w, y*py+h), dst)


			def OnMotion(self, evt):
				"""
				Called when the mouse is in motion.  If the left button is
				dragging then draw a line from the last event position to the
				current one.  Save the coordinants for redraws.
				"""
				if evt.Dragging() and evt.LeftIsDown():
					dc = wxClientDC(self)
					self.PrepareDC(dc)

					self.parent.RenderDrag(dc)

					start = self.parent.start
					end = self.ConvertEventCoords(evt)
					self.parent.end = end
##					x,y = self.GetViewStart()
##					h,w = self.GetClientSize()
##					px, py = self.GetScrollPixelsPerUnit()

					self.parent.SetStatusText("%i PC" % (sqrt((start[0]-end[0])**2+(start[1]-end[1])**2)), 3)
					
					self.parent.RenderDrag(dc)
				
				self.parent.SetStatusText("X: %i, Y: %i, Z: 0" % self.ConvertEventCoords(evt), 2)

			def OnLeftDown(self, evt):
				"""called when the left mouse button is pressed"""
				#print evt.GetX(), evt.GetY()
				#print self.ConvertEventCoords(evt)
				self.parent.start = self.ConvertEventCoords(evt)
				self.end = self.parent.start
				self.CaptureMouse()
				self.parent.dragging = 1

				dc = wxClientDC(self)
				self.PrepareDC(dc)
				self.parent.RenderDrag(dc)

			def OnLeftUp(self, evt):
				"""called when the left mouse button is released"""
				dc = wxClientDC(self)
				self.PrepareDC(dc)
				self.parent.RenderDrag(dc)
				
				self.parent.dragging = 0
				self.ReleaseMouse()

				# Call the approiate call
				

			def OnRightUp(self, evt):
				pass

			def ConvertEventCoords(self, evt):
				xView, yView = self.GetViewStart()
				xDelta, yDelta = self.GetScrollPixelsPerUnit()
				return (evt.GetX() + (xView * xDelta), evt.GetY() + (yView * yDelta))
	

		self.windowScroll = starCanvas(self)
#		self.canvas = self.windowScroll.canvas
		self.maxWidth = self.windowScroll.maxWidth
		self.maxHeight = self.windowScroll.maxHeight

		# Load the graphics
		self.graphics = {}
		self.graphics['background'] = wxImage(os.path.join("graphics", "space_back.gif")).ConvertToBitmap()

	def OnPaint(self, evt):
		print "On paint! main"

	def RenderMap(self, startpos, endpos, dc=None):

		#print "rendering", dc

		dc.BeginDrawing()
		dc.SetBackground(wxBrush(wxBLACK, wxSOLID))
		dc.Clear()
		
		dc.SetPen(wxPen(wxWHITE, 0, wxSOLID))
		
		#########################
		# Draw Background
		#########################

		max = (self.maxWidth, self.maxHeight)
		size = (self.graphics['background'].GetWidth(), self.graphics['background'].GetHeight())

		background = self.graphics['background']

		startpos = startpos[0] - size[0], startpos[1] - size[1]
		endpos = endpos[0] + size[0], endpos[1] + size[1]

		#print startpos, size, endpos, (endpos[0]-startpos[0], endpos[1]-startpos[1])

		x = size[0] * (startpos[0] / size[0])
		while x < endpos[0]:
			y = size[1] * (startpos[1] / size[1])
			while y < endpos[1]:
				if x >= startpos[0] and y >= startpos[1]:
					#print (x,y)
					dc.DrawBitmap(background, x, y, TRUE)
				y += size[1]
			x += size[0]

		#######################
		# Draw the systems
		#######################

		# Check for the current options:
		# options['DrawNames'], toggle, draw the names of the systems
		# options['Scanner'], toggle, draw the scanner circles, yellow circles are penatrating, red and plain
		# options['Routes'], toggle, draw ships routes and planets destination routes
		# options['Ships'], toggle, draws a circle around systems if ships are there and any ships in space
		# options['Systems']
		#                    = sysPLAIN, draws the system as plain dots
		#                    = sysOWNER, draws the system as small dots with color of
		#                                the player that owns them, co-owner ship is
		#                                reported with pink, none with white
		#                    = sysHAB,   draws the system as circles with color being
		#                                red == no Habitable planets
		#                                yellow == one or more habitable planets with terraforming
		#                                green == one or more planets which are habitable
		#                                the larger the circle the more habitable the planets
		#                    = sysMIN,   draws a little graphic showing the total avaible minerals in each system
		#                    = sys
		# options['Zoom'] = the zoom of the map
		#

		dc.SetFont(wxFont(8, wxSWISS, wxNORMAL, wxNORMAL))
		dc.SetTextForeground(wxWHITE)

		zoom = self.config['Zoom']
		
		for i in systems:

			if isinstance(i, System):

				#print i.x/zoom, i.y/zoom

				if self.config['Scanner']:
					scanner = i.getScanner()
					if scanner is not None:
						p, s, a = scanner.getRange()

						#print "Topleft", i.x, i.y, "Range", s, "Scanner topleft", i.x/zoom-s/2/zoom, i.y/zoom-s/2/zoom

						#dc.SetLogicalFunction(wxSET)

						# Non-Penatrating Scanner
						dc.SetPen(wxPen(wxRED, 1, wxSOLID))
						dc.SetBrush(wxBrush(wxRED, wxSOLID))
						dc.DrawEllipse(i.x/zoom-s/2.0/zoom+POINT/2, i.y/zoom-s/2.0/zoom+POINT/2, s/zoom, s/zoom)

						# Penatrating Scanner
						dc.SetPen(wxPen(wxYELLOW, 1, wxSOLID))
						dc.SetBrush(wxBrush(wxYELLOW, wxSOLID))
						dc.DrawEllipse(i.x/zoom-p/2.0/zoom+POINT/2, i.y/zoom-p/2.0/zoom+POINT/2, p/zoom, p/zoom)

						#dc.SetLogicalFunction(wxSET)

				if self.config['DrawNames']:
					#print "Drawing the name", i.name
					tw, th = dc.GetTextExtent(i.name) 
					dc.DrawText(i.name, i.x/zoom-tw/2+POINT/2, i.y/zoom+POINT+1)

				if self.config['System'] == sysOWNER:
					pass

				elif self.config['System'] == sysPLAIN:
					dc.SetBrush(wxBrush(wxWHITE, wxSOLID))
					dc.DrawEllipse(i.x/zoom, i.y/zoom, POINT, POINT)

				if self.config['Ships']:
					# Draw an orbit circle if the ship exists
					dc.SetPen(wxPen(wxWHITE, 1, wxSOLID))
					dc.SetBrush(wxTRANSPARENT_BRUSH)
					dc.DrawEllipse(i.x/zoom+POINT/2-POINT, i.y/zoom+POINT/2-POINT, POINT*2, POINT*2)


		if self.dragging:
			self.RenderDrag(dc)
			
		dc.EndDrawing()


	def RenderDrag(self, dc):
		#######################
		# Draw the selector
		#######################
		# Draw a line between start and finish
		if self.dragging:
			dc.SetBrush(wxTRANSPARENT_BRUSH)
			dc.SetLogicalFunction(wxINVERT)
			dc.DrawLine(self.start[0], self.start[1], self.end[0], self.end[1])
