# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class DownloadProgressPanelBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", 'DownloadProgressPanel.xrc')

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
		if not res.LoadOnPanel(pre, parent, "DownloadProgressPanel"):
			raise IOError("Did not find the DownloadProgressPanel in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.ButtonPanel = XRCCTRL(self, "ButtonPanel")
		self.Cancel = XRCCTRL(self, "Cancel")
		if hasattr(self, "OnCancel"):
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)

		self.Spacer = XRCCTRL(self, "Spacer")
		self.FileName = XRCCTRL(self, "FileName")
		self.SpeedETAPanel = XRCCTRL(self, "SpeedETAPanel")
		self.Speed = XRCCTRL(self, "Speed")
		self.ETA = XRCCTRL(self, "ETA")
		self.Progress = XRCCTRL(self, "Progress")


def strings():
	pass
	_("Cancel");
	_("0 kb/s");
	_("N/A s");
