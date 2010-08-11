# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class winWaitingBase:
	"""\
Unlike a normal XRC generated class, this is a not a full class but a MixIn.
Any class which uses this as a base must also inherit from a proper wx object
such as the wx.Frame class.

This is so that a the same XRC can be used for both MDI and non-MDI frames.
"""

	xrc = os.path.join(location(), "windows", "xrc", 'winWaiting.xrc')

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
		if not res.LoadOnFrame(pre, parent, "winWaiting"):
			raise IOError("Did not find the winWaiting in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.TitleText = XRCCTRL(self, "TitleText")
		self.Message = XRCCTRL(self, "Message")
		self.WaitingFor = XRCCTRL(self, "WaitingFor")
		self.WaitingList = XRCCTRL(self, "WaitingList")
		self.Cancel = XRCCTRL(self, "wxID_CANCEL")
		if hasattr(self, "OnCancel"):
			self.Bind(wx.EVT_BUTTON, self.OnCancel, self.Cancel)



def strings():
	pass
	_("End of turn requested!");
	_("Thanks for requesting end of turn.\n\nThe turn will end as soon as the other players get their buttocks into gear and click the end of turn button too.");
	_("Waiting for:");
	_("&Cancel");
	_("TP: Connect to a Server");
