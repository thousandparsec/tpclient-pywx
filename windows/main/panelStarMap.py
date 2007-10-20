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

from overlays.Resource import Resource
from overlays.Systems  import Systems

from windows.xrc.panelStarMap import panelStarMapBase
class panelStarMap(panelStarMapBase):
	title = _("StarMap")

	def __init__(self, application, parent):
		panelStarMapBase.__init__(self, parent)

		self.application = application

		self.Canvas = FloatCanvas.FloatCanvas(self.FloatCanvas, Debug=1, BackgroundColor="black")

		import extra.wxFloatCanvas.GUIMode as GUIMode
		self.GUIZoomIn  =  GUIMode.GUIZoomIn(self.Canvas)
		self.GUIZoomOut =  GUIMode.GUIZoomOut(self.Canvas)
		self.GUIMove    =  GUIMode.GUIMove(self.Canvas)
		self.GUIMouse   =  GUIMode.GUIMouse(self.Canvas)
		self.Canvas.SetMode(self.GUIMouse)

		self.Bind(wx.EVT_SIZE, self.OnSize)

	def GetPaneInfo(self):
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
		if isinstance(evt, wx.Event):
			to = evt.GetString().lower()
		else:
			to = str(evt).lower()

		if self.Canvas.GUIMode == self.GUIZoomIn:
			self.Canvas.SetMode(self.GUIMouse)

		if to == 'fit':
			self.Canvas.ZoomToBB()
			self.ScaleMax = self.Canvas.Scale
		elif to == 'box':
			self.Canvas.SetMode(self.GUIZoomIn)
		else:
			if to[-1] == '%':
				to = to[:-1]

			try:
				to = float(to)

				self.Canvas.Scale = self.ScaleMax*(100/to)
				self.Canvas.Zoom(1, self.Overlay.Focus(), 'world')
			except ValueError:
				# FIXME: This should pop-up some type of error.
				print "Can not zoom to that level"

	def OnCacheUpdate(self, evt):
		"""\
		Called when the cache has been updated.
		"""
		if evt.what == None:
			if hasattr(self, 'Overlay'):
				self.Overlay.CleanUp()

			self.Overlay = Systems(self, self.Canvas, self.application.cache)
#			self.Overlay = Resource(self, self.Canvas, self.application.cache)
			self.Overlay.Update()

		self.OnZoomLevel('fit')
		self.Canvas.Draw()

	def PostSelectObject(self, oid):
		self.application.gui.Post(self.application.gui.SelectObjectEvent(oid))

	def PostPreviewObject(self, oid):
		self.application.gui.Post(self.application.gui.PreviewObjectEvent(oid))

	def OnSelectObject(self, evt):
		"""\
		Called when an object is selected.
		"""
		if isinstance(evt, self.application.gui.PreviewObjectEvent):
			return
		self.Overlay.SelectObject(evt.id)

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



