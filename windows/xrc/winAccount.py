# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class winAccountBase:
	xrc = 'winAccount.xrc'

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Figure out what Frame class (MDI, MiniFrame, etc) is actually our base...
		bases = set()
		def findbases(klass, set):
			for base in klass.__bases__:
				set.add(base)
				findbases(base, set)
		findbases(self.__class__, bases)

		for base in bases:
			if base.__name__.endswith("Frame"):
				break
		
		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = getattr(wx, "Pre%s" % base.__name__)()
		res.LoadOnFrame(pre, parent, "winAccount")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.Server = XRCCTRL(self, "Server")
		self.Checking = XRCCTRL(self, "Checking")
		self.Check = XRCCTRL(self, "Check")
		if hasattr(self, "OnCheck"):
			self.Bind(wx.EVT_BUTTON, self.OnCheck, self.Check)

		self.Username = XRCCTRL(self, "Username")
		self.GameShow = XRCCTRL(self, "GameShow")
		if hasattr(self, "OnGameShow"):
			self.Bind(wx.EVT_TOGGLEBUTTON, self.OnGameShow, self.GameShow)

		self.GameTitle = XRCCTRL(self, "GameTitle")
		self.Game = XRCCTRL(self, "Game")
		self.Password1 = XRCCTRL(self, "Password1")
		self.Password2 = XRCCTRL(self, "Password2")
		self.Email = XRCCTRL(self, "Email")
		self.Okay = XRCCTRL(self, "wxID_OK")
		if hasattr(self, "OnOkay"):
			self.Bind(wx.EVT_BUTTON, self.OnOkay, self.Okay)

		self.Cancel = XRCCTRL(self, "wxID_CANCEL")
		if hasattr(self, "OnCancel"):
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)



