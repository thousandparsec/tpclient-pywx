"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string
import os

# wxPython Imports
import wx

from extra.decorators import freeze_wrapper, onlyshown, onlyenabled

from requirements import graphicsdir

from tp.netlib import constants as features

# Local Imports
from winBase import winBaseXRC
from winConnect import usernameMixIn
from xrc.winWaiting import winWaitingBase

ID = 0
NAME = 1
STATUS = 2

class winWaiting(winReportXRC, winWaitingBase):
	title = _("Waiting")

	def __init__(self, application, parent):
		winWaitingBase.__init__(self, None)
		winBaseXRC.__init__(self, application)	

		self.application = application

		self.Players.InsertColumn(ID, "Player ID", width = 100)
		self.Players.InsertColumn(NAME, "Player Name", width = 200)
		self.Players.InsertColumn(STATUS, "Player Status", width = 100)
		
		self.waiting = []

		self.application.gui.Binder(self.application.NetworkClass.NetworkTimeRemainingEvent, self.OnNetworkTimeRemaining)
		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.Update)
	
	def Update(self, evt=None):
		self.Players.DeleteAllItems()

		for i, player in self.application.cache.players.values():
			self.Players.InsertStringItem(i, "%d" % player.pid)
			self.Players.SetStringItem(i, NAME, player.name)

			if pid in self.waiting:
				self.Players.SetStringItem(i, TYPE, "Waiting")
			else:
				self.Players.SetStringItem(i, TYPE, "Ready!")

			self.Players.SetItemData(i, player.pid)

	def OnNetworkTimeRemaining(self, evt):
		self.waiting = evt.frame.waiting
		self.Update()

	@onlyshown
	@onlyenabled("Cancel")
	def OnCancel(self, evt):
		self.Hide()
		self.application.gui.Show(self.application.gui.main)

	@onlyshown
	def OnClose(self, evt):
		evt.Veto(True)
		self.OnCancel(None)
