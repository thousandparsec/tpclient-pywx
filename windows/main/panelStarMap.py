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

from extra.StateTracker import TrackerObject
from extra.wxFloatCanvas import FloatCanvas

from overlays.Resource import Resource
from overlays.Systems  import Systems
from overlays.Path     import Paths

from windows.xrc.panelStarMap import panelStarMapBase

from tp.netlib.objects import OrderDescs

class panelStarMap(panelStarMapBase, TrackerObject):
	title = _("StarMap")

	Overlays = [(Paths, Systems), (Paths, Resource)]
	def __init__(self, application, parent):
		panelStarMapBase.__init__(self, parent)

		self.application = application

		self.Canvas = FloatCanvas.FloatCanvas(self.FloatCanvas, Debug=1, BackgroundColor="black")

		import extra.wxFloatCanvas.GUIMode as GUIMode
		self.GUIZoomIn  =  GUIMode.GUIZoomIn(self.Canvas)
		self.GUIZoomOut =  GUIMode.GUIZoomOut(self.Canvas)
		self.GUIMove    =  GUIMode.GUIMove(self.Canvas)
		self.GUIMouse   =  GUIMode.GUIMouseAndMove(self.Canvas)
		self.SetMode(self.GUIMouse)

		# Create the mouse-mode popup
		self.MouseModePopup = wx.PopupWindow(self)
		p = wx.Panel(self.MouseModePopup)
		s = wx.BoxSizer(wx.VERTICAL)

		for button in [ wx.Button(p, -1, 'Mouse'),
						wx.Button(p, -1, 'Move'),
						wx.Button(p, -1, 'Zoom In'),
						wx.Button(p, -1, 'Zoom Out')]:
			button.Bind(wx.EVT_BUTTON, self.OnMouseModeButton)
			s.Add(button, proportion=1, flag=wx.EXPAND)

		self.WaypointButton = wx.Button(p, -1, 'Waypoint')
		self.WaypointButton.Bind(wx.EVT_BUTTON, self.OnMouseModeButton)
		s.Add(self.WaypointButton, proportion=1, flag=wx.EXPAND)

		p.SetSizer(s)
		p.Layout()
		p.SetSize(p.GetBestSize())
		self.MouseModePopup.SetSize(p.GetBestSize())

		self.Bind(wx.EVT_SIZE, self.OnSize)

		# Populate the overlay chooser
		self.Overlay = None
		for overlay in self.Overlays:
			self.DisplayMode.Append(overlay[-1].name, overlay)
		self.DisplayMode.SetSelection(0)

		self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

		TrackerObject.__init__(self)

	def OnMouseEnter(self, evt):
#		print "OnMouseEnter!", evt
		# FIXME: Should make sure we gain the keyboard focus
#		self.Canvas.SetFocus()
		pass

	def OnMouseLeave(self, evt):
#		print "OnMouseLeave!", evt
		# FIXME: Put the keyboard focus back where it was
		pass

	def OnMouseMode(self, evt):
		"""
		Occurs when a person clicks on the MouseMode button.

		Pops-up a menu which lets them select which MouseMode to change too.
		"""
		if self.MouseModePopup.IsShown():
			self.MouseModePopup.Hide()
		else:
			size = (0, self.MouseMode.GetSize()[1])
			self.MouseModePopup.Position(self.MouseMode.GetScreenPosition(), size)
			self.MouseModePopup.Show()
	
	def OnMouseModeButton(self, evt):
		"""
		Occurs when a person clicks on an option on the MouseMode popup.

		Changes the current GUIMode to the selected option.
		"""
		self.MouseModePopup.Hide()

		mode = evt.GetEventObject().GetLabel()
		mode = mode.replace(' ', '')
		
		GUIMode = getattr(self, 'GUI%s' % mode, self.GUIMouse)
		self.SetMode(GUIMode)

	def SetMode(self, mode):
		"""
		Set the current mode of the canvas to a given type.
		"""
		self.Canvas.SetMode(mode)

		if mode == self.GUIMouse:
			self.Canvas.SetCursor(wx.StockCursor(wx.CURSOR_RIGHT_ARROW))

	def OnDisplayMode(self, evt):
		"""
		Called when the DisplayMode choice box is changed.

		Causes the overlay being displayed on the starmap to be changed.
		"""
		cls = self.DisplayMode.GetClientData(self.DisplayMode.GetSelection())

		oid = -1

		# Clear any overlay which is currently around
		if self.Overlay != None:
			oid = self.Overlay[-1].Focus()[0]

			for Overlay in self.Overlay:
				Overlay.CleanUp()
				Overlay = None

			# Remove the panel from the sizer
			self.DisplayModeExtra.GetSizer().Remove(self.DisplayModePanel)

			# Destroy the panel and all it's children
			self.DisplayModePanel.Destroy()

			# Destory our reference to the panel
			del self.DisplayModePanel

		# Create a new panel
		self.DisplayModePanel = wx.Panel(self.DisplayModeExtra)
		#self.DisplayModePanel.SetBackgroundColour(wx.BLUE) # Only needed for debugging where the panel is covering
		# Add the panel to the sizer
		self.DisplayModeExtra.GetSizer().Add(self.DisplayModePanel, proportion=1, flag=wx.EXPAND)

		# Create the new overlay
		self.Overlay = []
		for Overlay in cls:
			self.Overlay.append(Overlay(self, self.Canvas, self.DisplayModePanel, self.application.cache))
			self.Overlay[-1].UpdateAll()

		if oid != -1:
			for Overlay in self.Overlay:
				try:
					Overlay.SelectObject(oid)
				except NotImplementedError:
					pass

		# Force the panel to layout
		self.DisplayModeExtra.Layout()

		self.Canvas.Draw()

	def GetPaneInfo(self):
		"""
		wx.aui method for getting the initial position and settings of this panel.
		"""
		info = wx.aui.AuiPaneInfo()
		info.Center()
		info.PinButton(True)
		info.MaximizeButton(True)
		return info

	def OnSize(self, evt):
		self.Layout()
		self.FloatCanvas.Layout()
		self.Canvas.SetSize(self.FloatCanvas.GetClientSize())

	def OnZoomLevel(self, evt):
		"""
		Called when the ZoomLevel box is changed.
		"""
		# FIXME: When the ZoomLevel is changed in any there way, we should get called too...

		if isinstance(evt, wx.Event):
			to = evt.GetString().lower()
		else:
			to = str(evt).lower()

		if self.Canvas.GUIMode == self.GUIZoomIn:
			self.SetMode(self.GUIMouse)

		if to == 'fit':
			self.Canvas.ZoomToBB()
			self.ScaleMax = self.Canvas.Scale
		elif to == 'box':
			self.SetMode(self.GUIZoomIn)
		else:
			if to[-1] == '%':
				to = to[:-1]

			try:
				to = float(to)

				self.Canvas.Scale = self.ScaleMax*(100/to)
				self.Canvas.Zoom(1, self.Overlay[-1].Focus()[1], 'World')
			except ValueError:
				# FIXME: This should pop-up some type of error.
				print "Can not zoom to that level"

	def OnCacheUpdate(self, evt):
		"""\
		Called when the cache has been updated.
		"""
		if evt.what == None:
			# FIXME: These shouldn't really be here
			if self.Overlay is not None:
				for Overlay in self.Overlay:
					Overlay.UpdateAll()
			else:
				self.OnDisplayMode(None)		

			self.OnZoomLevel('fit')
			self.Canvas.Draw()

	def ObjectSelect(self, id):
		"""\
		Called when an object is selected.
		"""
		# Check if this object can move so we can enable waypoint mode
		canmove = False
		for orderid in self.application.cache.objects[id].order_types:
			order = OrderDescs()[orderid]

			# FIXME: Needs to be a better way to do this...
			if order._name in ("Move", "Move To", "Intercept"):
				canmove = True
				break

		if canmove:
			self.WaypointButton.Enable()
		else:
			self.WaypointButton.Disable()
