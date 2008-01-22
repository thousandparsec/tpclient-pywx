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

from extra.StateTracker import TrackerObjectOrder
from extra.wxFloatCanvas import FloatCanvas

from overlays.Resource import Resource
from overlays.Systems  import Systems
from overlays.Path     import Paths

from windows.xrc.panelStarMap import panelStarMapBase

from tp.netlib.objects import OrderDescs

import extra.wxFloatCanvas.GUIMode as GUIMode
class GUIWaypoint(GUIMode.GUIMouse):
	def __init__(self, *args, **kw):
		GUIMode.GUIMouse.__init__(self, *args, **kw)
		self.overlay = None

	def OnLeftUp(self, event):
		EventType = FloatCanvas.EVT_FC_LEFT_UP
		if not self.parent.HitTest(event, EventType):
			if hasattr(self.overlay, "OnLeftUpMiss"):
				self.overlay.OnLeftUpMiss(event)

	def SetOverlay(self, overlay):
		self.overlay = overlay

class panelStarMap(panelStarMapBase, TrackerObjectOrder):
	title = _("StarMap")

	Overlays = [(Paths, Systems), (Paths, Resource)]
	def __init__(self, application, parent):
		panelStarMapBase.__init__(self, parent)
		self.parent = parent

		self.application = application

		self.Canvas = FloatCanvas.FloatCanvas(self.FloatCanvas, Debug=1, BackgroundColor="black")

		self.Find.Hide()
		
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
		
		# Create the find popup
		self.FindPopup = wx.PopupWindow(self)
		pf = wx.Panel(self.FindPopup)
		sf = wx.BoxSizer(wx.HORIZONTAL)

		findtext = wx.TextCtrl(pf, -1, "Enter Text")
		findbutton = wx.Button(pf, -1, 'Go')
		#findtext.Bind(wx.EVT_COMMAND_TEXT_ENTER, self.OnFindButton)
		findbutton.Bind(wx.EVT_BUTTON, self.OnFindButton)
		sf.Add(findtext, proportion=1, flag=wx.EXPAND)
		sf.Add(findbutton, proportion=0, flag=wx.EXPAND)

		pf.SetSizer(sf)
		pf.Layout()
		pf.SetSize(pf.GetBestSize())
		self.FindPopup.SetSize(pf.GetBestSize())

		self.Bind(wx.EVT_SIZE, self.OnSize)
				
		self.Home.Bind(wx.EVT_BUTTON, self.OnHome)
		self.Find.Bind(wx.EVT_BUTTON, self.OnFind)

		# Populate the overlay chooser
		self.Overlay = None
		for overlay in self.Overlays:
			self.DisplayMode.Append(overlay[-1].name, overlay)
		self.DisplayMode.SetSelection(0)

		self.GUISelect   = GUIMode.GUIMouseAndMove(self.Canvas)
		self.GUIMove     = GUIMode.GUIMove(self.Canvas)
		self.GUIZoomIn   = GUIMode.GUIZoomIn(self.Canvas)
		self.GUIZoomOut  = GUIMode.GUIZoomOut(self.Canvas)
		self.GUIWaypoint =         GUIWaypoint(self.Canvas)

		# Initialize mouse-mode bitmaps
		self.GUISelect.Icon   = wx.Bitmap("graphics/mousemode-icon.png")
		self.GUIMove.Icon     = wx.Bitmap("graphics/mousemove-icon16.png")
		self.GUIZoomIn.Icon   = wx.Bitmap("graphics/mousezoomin-icon16.png")
		self.GUIZoomOut.Icon  = wx.Bitmap("graphics/mousezoomout-icon16.png")
		self.GUIWaypoint.Icon = wx.Bitmap("graphics/mousewaypoint-icon16.png")
		
		self.SetMode(self.GUISelect)

		self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
		self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

		self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

		TrackerObjectOrder.__init__(self)

	def OnMouseEnter(self, evt):
#		print "OnMouseEnter!", evt
		# FIXME: Should make sure we gain the keyboard focus
		self.Canvas.SetFocus()

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
		
		GUIMode = getattr(self, 'GUI%s' % mode, self.GUISelect)
		self.SetMode(GUIMode)

	def SetMode(self, mode):
		"""
		Set the current mode of the canvas to a given type.
		"""
		self.MouseMode.SetBitmapLabel(mode.Icon)

		self.Canvas.SetMode(mode)
		self.mode = mode

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
			try:
				self.Overlay[-1].UpdateAll()
			except Exception, e:
				import traceback
				traceback.print_exc()

		self.GUIWaypoint.SetOverlay(self.Overlay[-1])

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
			self.SetMode(self.GUISelect)

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

			self.ZoomLevel.SetValue("Fit")
			self.OnZoomLevel('fit')
			self.Canvas.Draw()

	def ObjectSelect(self, id):
		"""\
		Called when an object is selected.
		"""
		self.SetMode(self.GUISelect)	

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

	def OnHome(self, evt):
		"""\
		Called when home button is pressed.
		"""
		self.ZoomLevel.SetValue("Fit")
		self.OnZoomLevel('fit')
		self.Canvas.Draw()
		
	def OnFind(self, evt):
 		"""\
 		Called when find button is pressed.
 		"""
 		if self.FindPopup.IsShown():
 			self.FindPopup.Hide()
 		else:
 			size = (0, self.Find.GetSize()[1])
 			self.FindPopup.Position(self.Find.GetScreenPosition(), size)
 			self.FindPopup.Show()
 	
 	def OnFindButton(self, evt):
 		"""\
 		Called when the enter key is pressed in the find text box
 		or the find button next to the text box is pressed.
 		"""
 		# TODO: Either pop up a list of possible choices matching the selection,
 		# or just select the object that matches most closely.

	def OnKeyUp(self, evt):
		print "OnKeyUp", evt, evt.GetKeyCode()

		if evt.GetKeyCode() == wx.WXK_ESCAPE:
			self.SetMode(self.GUISelect)	

		if evt.GetKeyCode() == wx.WXK_DELETE:
			if len(self.nodes) == 1:
				self.RemoveOrders(self.nodes)
			else:
				dlg = wx.MessageDialog(self,
						"You are about to remove multiple\norders, are you sure?",
 						"Remove orders?", 
						wx.OK | wx.CANCEL)

				if dlg.ShowModal() == wx.ID_OK:
					self.RemoveOrders(self.nodes)

				dlg.Destroy()

		print self.nodes
		print self.nodes[0].left, self.nodes[-1].right

		if evt.GetKeyCode() in (60, 44): # <
			if len(self.nodes) > 0 and not self.nodes[0].left.left is None:
				self.SelectOrders([self.nodes[0].left])

		if evt.GetKeyCode() in (46,): # >
			if len(self.nodes) > 0 and not self.nodes[-1].right is None:
				self.SelectOrders([self.nodes[-1].right])