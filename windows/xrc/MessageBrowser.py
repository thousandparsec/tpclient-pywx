# This file has been automatically generated.
# Please do not edit it manually.

import wx
from wx.xrc import *

from winBase import winReportBase

class MessageBrowserBase(winReportBase):
	xrc = 'MessageBrowser.xrc'

	def OnInit(self):
		""" This function is called during the class's initialization.
		
		Override it for custom setup (setting additional styles, etc.)"""
		pass

	def __init__(self, parent, res):
		""" Pass an initialized wx.xrc.XmlResource into res """
		
		res = XmlResource(self.xrc)

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.PrewinReportBase()
		res.LoadOnPanel(pre, parent, "MessageBrowser")
		self.OnInit()

		# Define variables for the controls
		self.BoardName = XRCCTRL(self, "BoardName")
		self.Filter = XRCCTRL(self, "Filter")
		if hasattr(self, "OnFilter"):
			self.Bind(self.Filter, self.OnFilter)

		self.Boards = XRCCTRL(self, "Boards")
		self.Message = XRCCTRL(self, "Message")
		self.New = XRCCTRL(self, "New")
		if hasattr(self, "OnNew"):
			self.Bind(self.New, self.OnNew)

		self.Goto = XRCCTRL(self, "Goto")
		if hasattr(self, "OnGoto"):
			self.Bind(self.Goto, self.OnGoto)

		self.Delete = XRCCTRL(self, "Delete")
		if hasattr(self, "OnDelete"):
			self.Bind(self.Delete, self.OnDelete)

		self.PostCreate(pre)


