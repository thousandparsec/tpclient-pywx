# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class panelMessageBase(wx.Panel):
	xrc = 'panelMessage.xrc'

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



