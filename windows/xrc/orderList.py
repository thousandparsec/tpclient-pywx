# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class orderListBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", 'orderList.xrc')

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
		if not res.LoadOnFrame(pre, parent, "orderList"):
			raise IOError("Did not find the orderList in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Choices = XRCCTRL(self, "Choices")
		self.Type = XRCCTRL(self, "Type")
		if hasattr(self, "OnType"):
			self.Type.Bind(wx.EVT_CHOICE, self.OnType)

		self.Number = XRCCTRL(self, "Number")
		self.Add = XRCCTRL(self, "Add")
		if hasattr(self, "OnAdd"):
			self.Bind(wx.EVT_BUTTON, self.OnAdd, self.Add)

		self.Delete = XRCCTRL(self, "Delete")
		if hasattr(self, "OnDelete"):
			self.Bind(wx.EVT_BUTTON, self.OnDelete, self.Delete)



def strings():
	pass
	_("Choice 1");
	_("Choice 2");
	_("Number of things to add or remove.");
	_("Add");
	_("Add items.");
	_("D");
	_("Delete selected.");
