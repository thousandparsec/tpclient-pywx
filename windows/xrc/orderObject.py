# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class orderObjectBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", 'orderObject.xrc')

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
		if not res.LoadOnPanel(pre, parent, "orderObject"):
			raise IOError("Did not find the orderObject in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Value = XRCCTRL(self, "Value")
		if hasattr(self, "OnValue"):
			self.Bind(wx.EVT_COMBOBOX, self.OnValue, self.Value)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnValue, self.Value)
		if hasattr(self, "OnDirtyValue"):
			self.Bind(wx.EVT_TEXT, self.OnValue, self.Value)



def strings():
	pass

