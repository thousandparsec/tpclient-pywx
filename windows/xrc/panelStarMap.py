# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class panelStarMapBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", 'panelStarMap.xrc')

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.PrePanel()
		if not res.LoadOnFrame(pre, parent, "panelStarMap"):
			raise IOError("Did not find the panelStarMap in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.MouseMode = XRCCTRL(self, "MouseMode")
		if hasattr(self, "OnMouseMode"):
			self.Bind(wx.EVT_BUTTON, self.OnMouseMode, self.MouseMode)

		self.ZoomLevel = XRCCTRL(self, "ZoomLevel")
		if hasattr(self, "OnZoomLevel"):
			self.Bind(wx.EVT_COMBOBOX, self.OnZoomLevel, self.ZoomLevel)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnZoomLevel, self.ZoomLevel)
		if hasattr(self, "OnDirtyZoomLevel"):
			self.Bind(wx.EVT_TEXT, self.OnZoomLevel, self.ZoomLevel)

		self.Home = XRCCTRL(self, "Home")
		if hasattr(self, "OnHome"):
			self.Bind(wx.EVT_BUTTON, self.OnHome, self.Home)

		self.Find = XRCCTRL(self, "Find")
		if hasattr(self, "OnFind"):
			self.Bind(wx.EVT_BUTTON, self.OnFind, self.Find)

		self.DisplayMode = XRCCTRL(self, "DisplayMode")
		if hasattr(self, "OnDisplayMode"):
			self.DisplayMode.Bind(wx.EVT_CHOICE, self.OnDisplayMode)

		self.DisplayModeExtra = XRCCTRL(self, "DisplayModeExtra")
		self.FloatCanvas = XRCCTRL(self, "FloatCanvas")


def strings():
	pass
	_("Fit");
	_("80%");
	_("50%");
	_("10%");
	_("Box");
	_("System");
	_("Resources");
