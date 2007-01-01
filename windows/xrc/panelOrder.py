# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class panelOrderBase(wx.Panel):
	xrc = 'panelOrder.xrc'

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
		res.LoadOnPanel(pre, parent, "panelOrder")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Orders = XRCCTRL(self, "Orders")
		self.Possible = XRCCTRL(self, "Possible")
		self.New = XRCCTRL(self, "New")
		if hasattr(self, "OnNew"):
			self.Bind(wx.EVT_BUTTON, self.OnNew, self.New)

		self.DetailsPanel = XRCCTRL(self, "DetailsPanel")
		self.ArgumentLine = XRCCTRL(self, "ArgumentLine")
		self.Message = XRCCTRL(self, "Message")
		self.Save = XRCCTRL(self, "Save")
		if hasattr(self, "OnSave"):
			self.Bind(wx.EVT_BUTTON, self.OnSave, self.Save)

		self.Revert = XRCCTRL(self, "Revert")
		if hasattr(self, "OnRevert"):
			self.Bind(wx.EVT_BUTTON, self.OnRevert, self.Revert)

		self.Delete = XRCCTRL(self, "Delete")
		if hasattr(self, "OnDelete"):
			self.Bind(wx.EVT_BUTTON, self.OnDelete, self.Delete)



