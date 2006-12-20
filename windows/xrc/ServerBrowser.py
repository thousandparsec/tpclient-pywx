# This file has been automatically generated.
# Please do not edit it manually.

import wx
from wx.xrc import *

from winBase import winMainBase

class ServerBrowserBase(winMainBase):
	xrc = 'ServerBrowser.xrc'

	def OnInit(self):
		""" This function is called during the class's initialization.
		
		Override it for custom setup (setting additional styles, etc.)"""
		pass

	def __init__(self, parent, res):
		""" Pass an initialized wx.xrc.XmlResource into res """
		
		res = XmlResource(self.xrc)

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.PrewinMainBase()
		res.LoadOnPanel(pre, parent, "ServerBrowser")
		self.OnInit()

		# Define variables for the controls
		self.InternetServers = XRCCTRL(self, "InternetServers")
		self.LocalServers = XRCCTRL(self, "LocalServers")
		self.NewAccount = XRCCTRL(self, "NewAccount")
		if hasattr(self, "OnNewAccount"):
			self.Bind(self.NewAccount, self.OnNewAccount)

		self.Connect = XRCCTRL(self, "Connect")
		if hasattr(self, "OnConnect"):
			self.Bind(self.Connect, self.OnConnect)

		self.PostCreate(pre)


