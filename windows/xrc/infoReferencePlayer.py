# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class infoReferencePlayerBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", 'infoReferencePlayer.xrc')

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
		if not res.LoadOnPanel(pre, parent, "infoReferencePlayer"):
			raise IOError("Did not find the infoReferencePlayer in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Quantity = XRCCTRL(self, "Quantity")
		self.Spacer = XRCCTRL(self, "Spacer")
		self.PlayerName = XRCCTRL(self, "PlayerName")
		self.SendMessage = XRCCTRL(self, "SendMessage")
		if hasattr(self, "OnSendMessage"):
			self.Bind(wx.EVT_BUTTON, self.OnSendMessage, self.SendMessage)



def strings():
	pass
	_("0");
	_("Send Message");
