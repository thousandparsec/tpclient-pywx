# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class panelMessageBase(wx.Panel):
	xrc = os.path.join(location(), "windows", "xrc", 'panelMessage.xrc')

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
		res.LoadOnPanel(pre, parent, "panelMessage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Filter = XRCCTRL(self, "Filter")
		if hasattr(self, "OnFilter"):
			self.Bind(wx.EVT_BUTTON, self.OnFilter, self.Filter)

		self.Title = XRCCTRL(self, "Title")
		self.Counter = XRCCTRL(self, "Counter")
		self.Message = XRCCTRL(self, "Message")
		self.Prev = XRCCTRL(self, "Prev")
		if hasattr(self, "OnPrev"):
			self.Bind(wx.EVT_BUTTON, self.OnPrev, self.Prev)

		self.First = XRCCTRL(self, "First")
		if hasattr(self, "OnFirst"):
			self.Bind(wx.EVT_BUTTON, self.OnFirst, self.First)

		self.Goto = XRCCTRL(self, "Goto")
		if hasattr(self, "OnGoto"):
			self.Bind(wx.EVT_BUTTON, self.OnGoto, self.Goto)

		self.Next = XRCCTRL(self, "Next")
		if hasattr(self, "OnNext"):
			self.Bind(wx.EVT_BUTTON, self.OnNext, self.Next)

		self.Last = XRCCTRL(self, "Last")
		if hasattr(self, "OnLast"):
			self.Bind(wx.EVT_BUTTON, self.OnLast, self.Last)

		self.Delete = XRCCTRL(self, "Delete")
		if hasattr(self, "OnDelete"):
			self.Bind(wx.EVT_BUTTON, self.OnDelete, self.Delete)



def strings():
	pass
	_("Filter");
	_("Static text");
	_("100 of 100");
	_("<html>\n<body>\n<center>\n\t<table cols=1 width=\"100%\">\n\t\t<tr>\n\t\t\t<td><b>Subject:</b> You are unloved!\n\t\t</tr>\n\t\t<tr>\n\t\t\t<td>\n\t\t\tYou have recived no messages this turn!<br><br>\n\t\t\tActually if you didn't recive any messages it most proberly\n\t\t\tmeans that your client couldn't load the results from the server.\n\t\t\tTry reload/restart the client.\n\t\t\t</td>\n\t\t</tr>\n\t </table>\n</center>\n</body>\n</html>");
	_("Prev");
	_("First");
	_("Goto");
	_("Next");
	_("Last");
	_("Delete");
