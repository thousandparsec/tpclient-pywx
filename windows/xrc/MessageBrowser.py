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
		self.PostCreate(pre)

		# Define variables for the controls
		self.BoardName = XRCCTRL(self, "BoardName")
		self.Filter = XRCCTRL(self, "Filter")
		self.Boards = XRCCTRL(self, "Boards")
		self.Message = XRCCTRL(self, "Message")
		self.New = XRCCTRL(self, "New")
		self.Goto = XRCCTRL(self, "Goto")
		self.Delete = XRCCTRL(self, "Delete")


