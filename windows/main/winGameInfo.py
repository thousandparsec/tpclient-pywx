"""
This is window showing some information about the current game.
"""

from windows.winBase import winReportXRC
from windows.xrc.winGameInfo import winGameInfoBase
from tp.client.threadcheck import thread_safe

class winGameInfo(winReportXRC, winGameInfoBase):
	title = _("Game Info")

	def __init__(self, application, parent):
		winGameInfoBase.__init__(self, parent)
		winReportXRC.__init__(self, application, parent)

		self.Panel.SetSize(self.Panel.GetBestSize())
		self.SetMinSize(self.Panel.GetBestSize())

		self.Okay.SetFocus()
		
		self.application.gui.Binder(self.application.NetworkClass.NetworkConnectEvent, self.OnNetworkConnect)
		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnCacheUpdate)

	def OnNetworkConnect(self, evt):
		"""
		Fills frame controls with information about game.
		"""
		if evt is None:
			return

		game = evt.games[0]
		optional = game.optional_get()

		self.ServerVersionTextCtrl.SetValue(game.server)
		self.GameTextCtrl.SetValue(game.name)
		self.RulesetTextCtrl.SetValue(game.rule)

		if(optional.has_key('plys')):
			self.PlayersNumberTextCtrl.SetValue(str(optional['plys']))

		if(optional.has_key('admin')):
			self.AdminEmailTextCtrl.SetValue(optional['admin'])

		conn = self.application.network.connection
		self.ServerUrlTextCtrl.SetValue("%s:%s" % (conn.hoststring, conn.port))

	def OnCacheUpdate(self, evt=None):
		"""
		Fills frame controls with information from cache.
		"""
		self.PlayerNameTextCtrl.SetValue(self.application.cache.players[0].name)

	def OnOkay(self, evt):
		self.Hide()


