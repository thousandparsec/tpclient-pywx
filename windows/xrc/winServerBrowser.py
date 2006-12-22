# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class winServerBrowserBase:
	xrc = 'winServerBrowser.xrc'

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Figure out what Frame class is actually our base...
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
		res.LoadOnFrame(pre, parent, "winServerBrowser")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.Progress = XRCCTRL(self, "Progress")
		self.InternetServers = XRCCTRL(self, "InternetServers")
		self.LocalServers = XRCCTRL(self, "LocalServers")
		self.ID_TEXTCTRL = XRCCTRL(self, "ID_TEXTCTRL")
		self.NewAccount = XRCCTRL(self, "NewAccount")
		if hasattr(self, "OnNewAccount"):
			self.Bind(wx.EVT_BUTTON, self.OnNewAccount, self.NewAccount)

		self.Connect = XRCCTRL(self, "Connect")
		if hasattr(self, "OnConnect"):
			self.Bind(wx.EVT_BUTTON, self.OnConnect, self.Connect)



