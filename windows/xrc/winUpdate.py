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
		print "Base Frame", base.__name__
		pre = getattr(wx, "Pre%s" % base.__name__)()
		res.LoadOnFrame(pre, parent, "winUpdate")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.TopText = XRCCTRL(self, "TopText")
		self.Message = XRCCTRL(self, "Message")
		self.ConnectingGauge = XRCCTRL(self, "ConnectingGauge")
		self.ConnectingAnim = XRCCTRL(self, "ConnectingAnim")
		self.ConnectingText = XRCCTRL(self, "ConnectingText")
		self.ProgressTitle = XRCCTRL(self, "ProgressTitle")
		self.ProgressGauge = XRCCTRL(self, "ProgressGauge")
		self.ProgressAnim = XRCCTRL(self, "ProgressAnim")
		self.ProgressText = XRCCTRL(self, "ProgressText")
		self.ObjectAnim = XRCCTRL(self, "ObjectAnim")
		self.OrderAnim = XRCCTRL(self, "OrderAnim")
		self.BoardAnim = XRCCTRL(self, "BoardAnim")
		self.MessageAnim = XRCCTRL(self, "MessageAnim")
		self.CategoryAnim = XRCCTRL(self, "CategoryAnim")
		self.DesignAnim = XRCCTRL(self, "DesignAnim")
		self.ComponentAnim = XRCCTRL(self, "ComponentAnim")
		self.PropertyAnim = XRCCTRL(self, "PropertyAnim")
		self.PlayerAnim = XRCCTRL(self, "PlayerAnim")
		self.ResourceAnim = XRCCTRL(self, "ResourceAnim")
		self.Cancel = XRCCTRL(self, "Cancel")
		if hasattr(self, "OnCancel"):
			self.Bind(self.Cancel, self.OnCancel)

