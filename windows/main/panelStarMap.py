"""\
This module contains the StarMap window. This window displays a view of the
universe.
"""
# Python imports
import copy
import os
from math import *
import sys
import numpy as N

from requirements import graphicsdir

# wxPython imports
import wx

from extra.StateTracker import TrackerObjectOrder
from extra.wxFloatCanvas import FloatCanvas

from overlays.Resource import Resource
from overlays.Systems  import Systems
from overlays.SystemIcons  import SystemIcons
from overlays.Path     import Paths

from windows.xrc.panelStarMap import panelStarMapBase

from tp.netlib.objects import OrderDescs
from tp.netlib.objects import parameters
from extra import objectutils

import extra.wxFloatCanvas.GUIMode as GUIMode
class GUIWaypoint(GUIMode.GUIMouse):
	def __init__(self, *args, **kw):
		GUIMode.GUIMouse.__init__(self, *args, **kw)
		self.Overlay  = None
		self.CallNext = None

	def OnLeftUp(self, event):
		print "OnLeftUp", event

		EventType = FloatCanvas.EVT_FC_LEFT_UP
		if not self.parent.HitTest(event, EventType):
			if hasattr(self.Overlay, "OnLeftUpMiss"):
				self.Overlay.OnLeftUpMiss(event)

		if not self.CallNext is None:
			CallNext = self.CallNext
			self.CallNext = None

			wx.CallAfter(CallNext)

	def SetOverlay(self, Overlay):
		self.Overlay = Overlay

	def SetCallNext(self, tocall):
		assert callable(tocall)

		self.CallNext = tocall

class GUIWaypointEdit(GUIWaypoint):
	pass

class panelStarMap(panelStarMapBase, TrackerObjectOrder):
	title = _("StarMap")

	Overlays = [(Paths, Systems), (Paths, Resource), (Paths, SystemIcons)]
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
		
		self.ZoomLevel.SetValidator(wx.SimpleValidator(wx.DIGIT_ONLY))
		self.ZoomLevel.Bind(wx.EVT_SET_FOCUS, self.OnZoomLevelFocus)

		self.ZoomLevel.SetWindowStyleFlag(self.ZoomLevel.GetWindowStyleFlag()|wx.TE_PROCESS_ENTER)

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
		self.GUIWaypointEdit =     GUIWaypointEdit(self.Canvas)

		# Initialize mouse-mode bitmaps
		if sys.platform == "darwin" or sys.platform == "win32":
			self.GUISelect.Icon   = wx.Bitmap(os.path.join(graphicsdir, "mousemode-icon16.png"))
			self.GUIMove.Icon     = wx.Bitmap(os.path.join(graphicsdir, "mousemove-icon16.png"))
			self.GUIZoomIn.Icon   = wx.Bitmap(os.path.join(graphicsdir, "mousezoomin-icon16.png"))
			self.GUIZoomOut.Icon  = wx.Bitmap(os.path.join(graphicsdir, "mousezoomout-icon16.png"))
			self.GUIWaypoint.Icon = wx.Bitmap(os.path.join(graphicsdir, "mousewaypoint-icon16.png"))
			self.GUIWaypointEdit.Icon = wx.Bitmap(os.path.join(graphicsdir, "mousewaypoint-icon16.png"))
		else:
			self.GUISelect.Icon   = wx.Bitmap(os.path.join(graphicsdir, "mousemode-icon24.png"))
			self.GUIMove.Icon     = wx.Bitmap(os.path.join(graphicsdir, "mousemove-icon24.png"))
			self.GUIZoomIn.Icon   = wx.Bitmap(os.path.join(graphicsdir, "mousezoomin-icon24.png"))
			self.GUIZoomOut.Icon  = wx.Bitmap(os.path.join(graphicsdir, "mousezoomout-icon24.png"))
			self.GUIWaypoint.Icon = wx.Bitmap(os.path.join(graphicsdir, "mousewaypoint-icon24.png"))
			self.GUIWaypointEdit.Icon = wx.Bitmap(os.path.join(graphicsdir, "mousewaypoint-icon16.png"))
		
		self.SetMode(self.GUISelect)

		self.Canvas.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
		self.Canvas.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

		self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

		TrackerObjectOrder.__init__(self)


	def Show(self, show=True):
		self.SetFocusIgnoringChildren()

	def OnMouseEnter(self, evt):
		print "OnMouseEnter!", evt
		# FIXME: Should make sure we gain the keyboard focus
		self.SetFocusIgnoringChildren()

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
		if not self.Overlay is None:
			for overlay in self.Overlay:
				if hasattr(overlay, "ModeChange"):
					overlay.ModeChange(self.mode, mode)

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
		info.DefaultPane()
		info.Center()
		info.PinButton(True)
		info.MaximizeButton(True)
		return info

	def OnSize(self, evt):
		self.Layout()
		self.FloatCanvas.Layout()
		self.Canvas.SetSize(self.FloatCanvas.GetClientSize())

	def OnZoomLevelFocus(self, evt):
		self.ZoomLevel.SetMark(-1, -1)
		evt.Skip()

	def OnZoomLevel(self, evt):
		"""
		Called when the ZoomLevel box is changed.
		"""
		# FIXME: When the ZoomLevel is changed in any there way, we should get called too...
		if isinstance(evt, wx.Event):
			to = evt.GetString().lower()
			evt.Skip()
		else:
			to = unicode(evt).lower()

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
			else:
				self.ZoomLevel.SetValue(unicode(to+"%"))

			try:
				to = float(to)

				self.Canvas.Scale = self.ScaleMax*(100/to)
				self.Canvas.Zoom(1, self.Overlay[-1].Focus()[1], 'World')
			except ValueError:
				# FIXME: This should pop-up some type of error.
				print "Can not zoom to that level"

		self.ZoomLevel.SetMark(0, len(self.ZoomLevel.GetValue()))

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
			self.OnHome(None)
			self.Canvas.Draw()

	def ObjectSelect(self, id):
		"""\
		Called when an object is selected.
		"""
		self.SetMode(self.GUISelect)	

		canmove = self.canObjectMove(id)
		
		if canmove:
			self.WaypointButton.Enable()
		else:
			self.WaypointButton.Disable()

	def OnHome(self, evt):
		"""\
		Called when home button is pressed.
		"""
		# Figure out the homeworld resource
		homeresource = None
		for number, resource in self.application.cache.resources.items():
			if resource.name != "Home Planet":
				continue
			homeresource = number
		
		# Figure out the homeworld		
		foundhomeworld = 0
		if not homeresource is None:
			for oid in self.application.cache.objects.keys():
				# Does the player own this object
				objowner = objectutils.getOwner(self.application.cache, oid)
				if objowner != self.application.cache.players[0].id:
					continue
			
				# Does this object have any resources?
				if not objectutils.hasResources(self.application.cache, oid):
					continue

				# Check if the object has a homeworld resource.
				resourcelist = objectutils.getResources(self.application.cache, oid)
				for resource in resourcelist:
					if resource[0] != homeresource:
						continue
						
					if resource[1] == 0:
						continue

					foundhomeworld = oid
					break

				if foundhomeworld != 0:
					break

		# Select the object
		self.SelectObject(foundhomeworld)
		
		poslist = objectutils.getPositionList(self.application.cache.objects[foundhomeworld])
		if len(poslist) > 0:
			# FIXME: Just use the first position?
			pos = poslist[0]
			self.Canvas.Zoom(1, pos[:2])
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
		pass

	def OnKeyUp(self, evt):
		if evt.GetKeyCode() in (77,):
			if self.oid is None:
				return

			canmove = self.canObjectMove(self.oid)

			if canmove:
				if evt.ShiftDown():
					def n(mode=self.mode):
						self.SetMode(mode)
					self.GUIWaypoint.SetCallNext(n)
				self.SetMode(self.GUIWaypoint)
		else:
			TrackerObjectOrder.OnKeyUp(self, evt)
		
		if sys.platform == "win32":
			self.Canvas.ProcessEvent(evt)

	def canObjectMove(self, id):
		ordertypes = objectutils.getOrderTypes(self.application.cache, id)
		# Check if this object can move so we can enable waypoint mode
		for queueid, typelist in ordertypes.items():
			for otype in typelist:
				order = OrderDescs()[otype]

				# FIXME: Needs to be a better way to do this... what if there's an order
				# type where the object can't move but it can place or throw something to
				# a specific point? Then the order will have coordinates, and this will
				# give a false positive, enabling the waypoint button.
				for property in order.properties:
					if type(property) == parameters.OrderParamAbsSpaceCoords \
						or type(property) == parameters.OrderParamRelSpaceCoords:
						return True
		
		return False
