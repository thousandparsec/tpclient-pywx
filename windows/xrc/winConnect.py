# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class winConnectBase:
	"""\
Unlike a normal XRC generated class, this is a not a full class but a MixIn.
Any class which uses this as a base must also inherit from a proper wx object
such as the wx.Frame class.

This is so that a the same XRC can be used for both MDI and non-MDI frames.
"""

	xrc = os.path.join(location(), "windows", "xrc", 'winConnect.xrc')

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
		if not res.LoadOnFrame(pre, parent, "winConnect"):
			raise IOError("Did not find the winConnect in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.Server = XRCCTRL(self, "Server")
		if hasattr(self, "OnServer"):
			self.Bind(wx.EVT_COMBOBOX, self.OnServer, self.Server)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnServer, self.Server)
		if hasattr(self, "OnDirtyServer"):
			self.Bind(wx.EVT_TEXT, self.OnServer, self.Server)

		self.Find = XRCCTRL(self, "wxID_FIND")
		if hasattr(self, "OnFind"):
			self.Bind(wx.EVT_BUTTON, self.OnFind, self.Find)

		self.Username = XRCCTRL(self, "Username")
		self.GameShow = XRCCTRL(self, "GameShow")
		if hasattr(self, "OnGameShow"):
			self.Bind(wx.EVT_TOGGLEBUTTON, self.OnGameShow, self.GameShow)

		self.GameTitle = XRCCTRL(self, "GameTitle")
		self.Game = XRCCTRL(self, "Game")
		self.Password = XRCCTRL(self, "Password")
		self.Okay = XRCCTRL(self, "wxID_OK")
		if hasattr(self, "OnOkay"):
			self.Bind(wx.EVT_BUTTON, self.OnOkay, self.Okay)

		self.Cancel = XRCCTRL(self, "wxID_CANCEL")
		if hasattr(self, "OnCancel"):
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)

		self.Config = XRCCTRL(self, "wxID_PREFERENCES")
		if hasattr(self, "OnConfig"):
			self.Bind(wx.EVT_BUTTON, self.OnConfig, self.Config)



def strings():
	pass
	_("TP: Connect to a Server");
	_("Connect to Thousand Parsec Server");
	_("Server");
	_("The URL for the Thousand Parsec server.");
	_("&Find");
	_("Username");
	_("The username for the account on the Thousand Parsec server.");
	_("Show seperate game box.");
	_("G");
	_("Game");
	_("Password");
	_("The password for the account on the Thousand Parsec Server");
	_("&OK");
	_("&Cancel");
	_("&Preferences");
