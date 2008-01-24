# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class winUpdateBase:
	xrc = 'winUpdate.xrc'

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
		res.LoadOnFrame(pre, parent, "winUpdate")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.TopText = XRCCTRL(self, "TopText")
		self.Message = XRCCTRL(self, "Message")
		self.ConnectingGauge = XRCCTRL(self, "ConnectingGauge")
		self.ConnectingText = XRCCTRL(self, "ConnectingText")
		self.ConnectingAnim = XRCCTRL(self, "ConnectingAnim")
		self.ProgressTitle = XRCCTRL(self, "ProgressTitle")
		self.ProgressGauge = XRCCTRL(self, "ProgressGauge")
		self.ProgressText = XRCCTRL(self, "ProgressText")
		self.ProgressAnim = XRCCTRL(self, "ProgressAnim")
		self.ObjectdescsAnim = XRCCTRL(self, "ObjectdescsAnim")
		self.OrderdescsAnim = XRCCTRL(self, "OrderdescsAnim")
		self.ObjectsAnim = XRCCTRL(self, "ObjectsAnim")
		self.OrdersAnim = XRCCTRL(self, "OrdersAnim")
		self.BoardsAnim = XRCCTRL(self, "BoardsAnim")
		self.MessagesAnim = XRCCTRL(self, "MessagesAnim")
		self.CategoriesAnim = XRCCTRL(self, "CategoriesAnim")
		self.DesignsAnim = XRCCTRL(self, "DesignsAnim")
		self.ComponentsAnim = XRCCTRL(self, "ComponentsAnim")
		self.PropertiesAnim = XRCCTRL(self, "PropertiesAnim")
		self.PlayersAnim = XRCCTRL(self, "PlayersAnim")
		self.ResourcesAnim = XRCCTRL(self, "ResourcesAnim")
		self.Okay = XRCCTRL(self, "wxID_OK")
		if hasattr(self, "OnOkay"):
			self.Bind(wx.EVT_BUTTON, self.OnOkay, self.Okay)

		self.Save = XRCCTRL(self, "wxID_SAVE")
		if hasattr(self, "OnSave"):
			self.Bind(wx.EVT_BUTTON, self.OnSave, self.Save)

		self.Cancel = XRCCTRL(self, "wxID_CANCEL")
		if hasattr(self, "OnCancel"):
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)



def strings():
	pass
	_("TP: Universe update");
	_("Universe Download");
	_("Done!");
	_("Progress");
	_("Done!");
	_("Objects Descs");
	_("Order Descs");
	_("Objects");
	_("Orders");
	_("Boards");
	_("Messages");
	_("Categories");
	_("Designs");
	_("Components");
	_("Properties");
	_("Players");
	_("Resources");
	_("Continue to the main game window.");
	_("&OK");
	_("Save a copy of the message box window to a file.");
	_("&Save");
	_("Cancel the current update and go back to the connect screen.");
	_("&Cancel");
