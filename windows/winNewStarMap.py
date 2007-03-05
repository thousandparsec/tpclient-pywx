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
from extra.wxFloatCanvas.RelativePoint import RelativePoint
from extra.wxFloatCanvas.Icon import Icon

from extra.wxFloatCanvas.NavCanvas import NavCanvas

# Local imports
from winBase import *
from utils import *

# FIXME: Float canvas has problems with the large sizes (when zoomed into planet level)
# We should fix this by doing some prescaling...

class StarMapCanvas(NavCanvas):
	def BuildToolbar(self):
		tb = wx.ToolBar(self)
		self.ToolBar = tb

		tb.SetToolBitmapSize((24,24))

		from extra.wxFloatCanvas import Resources
		self.ZoomButton = tb.AddRadioTool(wx.ID_ANY, bitmap=Resources.getMagPlusBitmap(), shortHelp = "Change Zoom Level.")
		self.Bind(wx.EVT_TOOL, self.OnZoomTool, self.ZoomButton)

		tb.AddSeparator()
		tb.Realize()
		return tb

	def OnZoomTool(self, evt):
#		print evt, #self.ZoomButton.GetPosition()

		# Popup a menu
		menu = wx.Menu()
		menu.Append(100, "Testing")	
		self.PopupMenu(menu)

# Shows the main map of the universe.
class panelStarMap(wx.Panel):
	title = _("StarMap")

	def __init__(self, application, parent):
		wx.Panel.__init__(self, parent)

		self.application = application

#		self.StarMap = StarMapCanvas(self, Debug = 1, BackgroundColor="black")
		self.StarMap = NavCanvas(self, Debug = 1, BackgroundColor="black")
		self.StarMap.ZoomToFit(None)
		self.Canvas = self.StarMap.Canvas

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
		self.StarMap.SetSize(self.GetClientSize())
#		self.Canvas.OnSize(evt)
		self.Canvas.ZoomToBB()
#		self.Canvas.ZoomToBB()

	def OnCacheUpdate(self, evt):
		"""\
		Called when the cache has been updated.
		"""
		print self.application
		print self.application.cache
		from overlays.Systems import Systems
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
