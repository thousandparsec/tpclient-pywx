# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class configConnectBase(wx.Panel):
	xrc = 'configConnect.xrc'

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
		res.LoadOnPanel(pre, parent, "configConnect")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Servers = XRCCTRL(self, "Servers")
		self.ServerDetails = XRCCTRL(self, "ServerDetails")
		self.Username = XRCCTRL(self, "Username")
		self.GameShow = XRCCTRL(self, "GameShow")
		if hasattr(self, "OnGameShow"):
			self.Bind(wx.EVT_TOGGLEBUTTON, self.OnGameShow, self.GameShow)

		self.GameTitle = XRCCTRL(self, "GameTitle")
		self.Game = XRCCTRL(self, "Game")
		self.Password = XRCCTRL(self, "Password")
		self.AutoConnect = XRCCTRL(self, "AutoConnect")
		if hasattr(self, "OnAutoConnect"):
			self.Bind(wx.EVT_CHECKBOX, self.OnAutoConnect, self.AutoConnect)

		self.Debug = XRCCTRL(self, "Debug")
		if hasattr(self, "OnDebug"):
			self.Bind(wx.EVT_CHECKBOX, self.OnDebug, self.Debug)



def strings():
	_("Login for");
	_("Username");
	_("The username for the account on the Thousand Parsec server.");
	_("Show seperate game box.");
	_("G");
	_("Game");
	_("Password");
	_("Autoconnect");
	_("Debug Output");
