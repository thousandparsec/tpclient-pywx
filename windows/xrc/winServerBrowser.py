# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class winServerBrowserBase:
	xrc = os.path.join(location(), "windows", "xrc", 'winServerBrowser.xrc')

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
		res.LoadOnFrame(pre, parent, "winServerBrowser")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.Progress = XRCCTRL(self, "Progress")
		self.Servers = XRCCTRL(self, "Servers")
		self.LocationsPanel = XRCCTRL(self, "LocationsPanel")
		self.LocationsBox = XRCCTRL(self, "LocationsBox")
		self.Locations = XRCCTRL(self, "Locations")
		self.URLTitle = XRCCTRL(self, "URLTitle")
		self.URL = XRCCTRL(self, "URL")
		self.Refresh = XRCCTRL(self, "wxID_REFRESH")
		if hasattr(self, "OnRefresh"):
			self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.Refresh)

		self.NewAccount = XRCCTRL(self, "NewAccount")
		if hasattr(self, "OnNewAccount"):
			self.Bind(wx.EVT_BUTTON, self.OnNewAccount, self.NewAccount)

		self.ConnectTo = XRCCTRL(self, "ConnectTo")
		if hasattr(self, "OnConnectTo"):
			self.Bind(wx.EVT_BUTTON, self.OnConnectTo, self.ConnectTo)

		self.Cancel = XRCCTRL(self, "wxID_CANCEL")
		if hasattr(self, "OnCancel"):
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)



def strings():
	pass
	_("TP: Server Browser");
	_("Thousand Parsec Server Browser");
	_("Servers");
	_("List of all the servers registered on the metaserver.");
	_("Locations");
	_("List of all the servers found on the local network.");
	_("URL");
	_("URL of the currently selected server.");
	_("Copy the URL to the clipboard.");
	_("&Copy");
	_("Force a refresh of the server list.");
	_("&Refresh");
	_("Create a new account on the currently selected server.");
	_("&New Account");
	_("Connect to the currently selected server.");
	_("C&onnect");
	_("&Cancel");
