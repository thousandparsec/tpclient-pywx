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

# Local Imports
from windows.winBase import winReportXRC
from windows.xrc.winWaiting import winWaitingBase

ID = 0
NAME = 1
STATUS = 2

class winWaiting(winReportXRC, winWaitingBase):
	"""\

	"""
	title = _("Waiting")


	def __init__(self, application, parent):
		"""\

		"""
		winWaitingBase.__init__(self, parent)
		winReportXRC.__init__(self, application, parent)
		
		self.application = application

		self.WaitingList.InsertColumn(ID, "Player ID", width = 100)
		self.WaitingList.InsertColumn(NAME, "Player Name", width = 200)
		self.WaitingList.InsertColumn(STATUS, "Player Status", width = 100)
		
		self.waiting = []

		self.Bind(wx.EVT_SHOW, self.OnShow)
		self.application.gui.Binder(self.application.NetworkClass.NetworkTimeRemainingEvent, self.OnNetworkTimeRemaining)

	def OnShow(self, evt):
		self.CenterOnParent()
		self.Update()
	
	def Update(self, evt=None):
		self.WaitingList.DeleteAllItems()

		for pid, player in self.application.cache.players.items():
			if pid == 0:
				continue

			i = self.WaitingList.GetItemCount()

			self.WaitingList.InsertStringItem(i, "%d" % pid)
			self.WaitingList.SetStringItem(i, NAME, player.name)

			if pid in self.waiting:
				self.WaitingList.SetStringItem(i, STATUS, "Waiting")
			else:
				self.WaitingList.SetStringItem(i, STATUS, "Ready!")

			self.WaitingList.SetItemData(i, pid)

	def OnNetworkTimeRemaining(self, evt):
		self.waiting = evt.frame.waiting
		self.Update()

	@onlyshown
	@onlyenabled("Cancel")
	def OnCancel(self, evt):
		self.OnClose(evt)

	@onlyshown
	def OnClose(self, evt):
		winReportXRC.OnClose(self, evt)
		self.application.gui.Show(self.application.gui.main)
