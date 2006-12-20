# This file has been automatically generated.
# Please do not edit it manually.

import wx
from wx.xrc import *

from winBase import winMainBase

class UpdateWindowBase(winMainBase):
	xrc = 'UpdateWindow.xrc'

	def OnInit(self):
		""" This function is called during the class's initialization.
		
		Override it for custom setup (setting additional styles, etc.)"""
		pass

	def __init__(self, parent, res):
		""" Pass an initialized wx.xrc.XmlResource into res """
		
		res = XmlResource(self.xrc)

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.PrewinMainBase()
		res.LoadOnPanel(pre, parent, "UpdateWindow")
		self.OnInit()

		# Define variables for the controls
		self.TopText = XRCCTRL(self, "TopText")
		self.MessageBox = XRCCTRL(self, "MessageBox")
		self.ConnectingGauge = XRCCTRL(self, "ConnectingGauge")
		self.ConnectingAnim = XRCCTRL(self, "ConnectingAnim")
		self.ConnectingText = XRCCTRL(self, "ConnectingText")
		self.DescriptionGauge = XRCCTRL(self, "DescriptionGauge")
		self.DescriptionAnim = XRCCTRL(self, "DescriptionAnim")
		self.DescriptionText = XRCCTRL(self, "DescriptionText")
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
		self.CancelButton = XRCCTRL(self, "CancelButton")
		if hasattr(self, "OnCancelButton"):
			self.Bind(self.CancelButton, self.OnCancelButton)

		self.PostCreate(pre)


