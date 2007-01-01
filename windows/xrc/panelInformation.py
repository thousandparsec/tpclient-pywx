# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class panelInformationBase(wx.Panel):
	xrc = 'panelInformation.xrc'

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
		res.LoadOnPanel(pre, parent, "panelInformation")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Title = XRCCTRL(self, "Title")
		self.Background = XRCCTRL(self, "Background")
		self.Image = XRCCTRL(self, "Image")
		self.Animation = XRCCTRL(self, "Animation")
		self.Details = XRCCTRL(self, "Details")


