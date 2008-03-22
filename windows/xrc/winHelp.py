# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class winHelpBase:
	"""\
Unlike a normal XRC generated class, this is a not a full class but a MixIn.
Any class which uses this as a base must also inherit from a proper wx object
such as the wx.Frame class.

This is so that a the same XRC can be used for both MDI and non-MDI frames.
"""

	xrc = os.path.join(location(), "windows", "xrc", 'winHelp.xrc')

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
		res.LoadOnFrame(pre, parent, "winHelp")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Subject = XRCCTRL(self, "Subject")
		self.Message = XRCCTRL(self, "Message")
		self.ShowAgain = XRCCTRL(self, "ShowAgain")
		if hasattr(self, "OnShowAgain"):
			self.Bind(wx.EVT_CHECKBOX, self.OnShowAgain, self.ShowAgain)

		self.Close = XRCCTRL(self, "wxID_CLOSE")
		if hasattr(self, "OnClose"):
			self.Bind(wx.EVT_BUTTON, self.OnClose, self.Close)



def strings():
	pass
	_("Important Information....");
	_("Do not show this message again.");
	_("&Close");
	_("Help");
