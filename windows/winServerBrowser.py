
# Python imports
import string
import os, os.path
import time

# wxPython Imports
import wx

# Local Imports
from winBase import winBaseXRC
from xrc.winServerBrowser import winServerBrowserBase

from requirements import graphicsdir

throbber = os.path.join(graphicsdir, "downloading.gif")
okay = os.path.join(graphicsdir, "finished.gif")
notokay = os.path.join(graphicsdir, "waiting.gif")

class winServerBrowser(winServerBrowserBase, winBaseXRC):
	title = _("Updating")
	
	ServersColumns = [_("Name"), _("Playing"), _("Server"), _("P"), _("C"), _("O"), _("Other")]
	ServersColumns_Sizes = [
			wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, 100, 
			wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, 
			-1]
	LocationsColumns = [_("Type"), _("DNS"), _("IP"), _("Port")]
	LocationsColumns_Sizes = [
			wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE]

	def __init__(self, application):
		winServerBrowserBase.__init__(self, None)
		winBaseXRC.__init__(self, application)
		
		self.Servers.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnServerSelect)
		self.Locations.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnLocationSelect)
		self.LocationsBox.Bind(wx.EVT_LEFT_DOWN, self.OnToggleLocation)
		self.LocationsPanel.Bind(wx.EVT_LEFT_DOWN, self.OnToggleLocation)

		self.OnToggleLocation(False)

		self.application.gui.Binder(self.application.FinderClass.FoundLocalGameEvent,  self.OnFoundLocalGame,  self.IsShown)
		self.application.gui.Binder(self.application.FinderClass.FoundRemoteGameEvent, self.OnFoundRemoteGame, self.IsShown)
#		self.application.gui.Binder(self.application.FinderClass.LostLocalGameEvent,   self.OnCacheUpdate)
#		self.application.gui.Binder(self.application.FinderClass.LostRemoteGameEvent,  self.OnCacheUpdate)

	def AddGame(self, game=None, resize=True):
		ctrl = self.Servers
		Columns, Columns_Sizes = self.ServersColumns, self.ServersColumns_Sizes

		if not game is None:
			i = ctrl.GetItemCount()
			ctrl.InsertStringItem(i, "")
			ctrl.SetItemPyData(i, game)

			ctrl.SetStringItem(i, Columns.index(_("Name")), game.name)
			if game.where == "local":
				ctrl.SetItemTextColour(i, wx.Color(0,0,255))

			try:
				ctrl.SetStringItem(i, Columns.index(_("Playing")), "%s (%s)" % (game.rule, game.rulever))
			except AttributeError: pass
			try:
				ctrl.SetStringItem(i, Columns.index(_("Server")),  "%s (%s)" % (game.sertype, game.server))
			except AttributeError: pass

#			try:
#				ctrl.SetToolTipItem(i, game.cmt)
#			except AttributeError: pass

			try:
				ctrl.SetStringItem(i, Columns.index(_("C")),  unicode(game.cons))
			except AttributeError: pass

			try:
				ctrl.SetStringItem(i, Columns.index(_("O")),  unicode(game.objs))
			except AttributeError: pass

			try:
				ctrl.SetStringItem(i, Columns.index(_("P")),  unicode(game.plys))
			except AttributeError: pass

			try:
				ctrl.SetStringItem(i, Columns.index(_("Other")), game.cmt)
			except AttributeError: pass

		if resize:
			for i, name in enumerate(Columns):
				ctrl.SetColumnWidth(i, Columns_Sizes[i])

	def Setup(self):
		ctrl = self.Servers
		Columns, Columns_Sizes = self.ServersColumns, self.ServersColumns_Sizes

		ctrl.ClearAll()
		for i, name in enumerate(Columns):
			ctrl.InsertColumn(i, name)

		local, remote = self.application.finder.Games()
		for games in (local, remote):
			for game in games.values():
				if game.name in local:
					game.where = "local"
				else:
					game.where = "remote"
				self.AddGame(game, False)
			self.AddGame(None, True)

	def OnFoundLocalGame(self, evt):
		game = evt.game
		game.where = "local"
		self.AddGame(game)

	def OnFoundRemoteGame(self, evt):
		game = evt.game
		game.where = "remote"
		self.AddGame(game)

	def OnServerSelect(self, evt):
		ctrl = self.Locations
		shown = ctrl.IsShown()

		Columns, Columns_Sizes = self.LocationsColumns, self.LocationsColumns_Sizes

		game = self.Servers.GetItemPyData(evt.GetIndex())

		ctrl.ClearAll()
		# Add the columns
		for i, name in enumerate(Columns):
			ctrl.InsertColumn(i, name)
		# Populate the columns with data
		for type, addrs in game.locations.items():
			for dns, ip, port in addrs:
				i = ctrl.GetItemCount()

				ctrl.InsertStringItem(i, "")
				ctrl.SetStringItem(i, Columns.index(_("Type")), type)
				ctrl.SetStringItem(i, Columns.index(_("DNS")),  dns)
				ctrl.SetStringItem(i, Columns.index(_("IP")),	 ip)
				ctrl.SetStringItem(i, Columns.index(_("Port")), unicode(port))

				ctrl.SetItemPyData(i, (game, (type, dns, ip, port)))
		# Set the column widths
		for i, name in enumerate(Columns):
			ctrl.SetColumnWidth(i, Columns_Sizes[i])
		ctrl.Show()

		# Set best location item selected and focused
		type, addr = game.bestLocation()

		slot = ctrl.FindItemByPyData((game, (type, addr[0], addr[1], addr[2])))
		t = wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED
		ctrl.SetItemState(slot, t, t) 
		self.OnLocationSelect(slot)

		self.OnToggleLocation(shown)

	def OnToggleLocation(self, evt):
		if not isinstance(evt, bool):
			toggle = not self.Locations.IsShown()
		else:
			toggle = evt

		if toggle:
			self.Locations.Show()
			self.LocationsBox.SetClientSize(self.Locations.GetBestSize())
		else:
			self.Locations.Hide()
			self.LocationsBox.SetSize((-1, 1))
			
		self.LocationsBox.Layout()
		self.LocationsPanel.Layout()
		if wx.Platform == "__WXMAC__":
			self.Servers.SetSize((-1, 10))
		self.Panel.Layout()

	def OnLocationSelect(self, evt):
		if isinstance(evt, int):
			slot = evt
		else:
			slot = evt.GetIndex()
		game, (type, dns, ip, port) = self.Locations.GetItemPyData(slot)

		# We use the IP address for local games as mDNS's might not be resolvable to everyone
		if game.where == "local":
			dns = ip

		# Set the copy box to the URL
		self.URL.SetValue("%s://%s:%s/%s" % (type, dns, port, game.name))

	def OnNewAccount(self, evt):
		self.application.gui.Show(self.application.gui.account)

	def OnConnectTo(self, evt):
		pass

	def Show(self, show=True):
		if not show:
			return self.Hide()
		
		# Setup the ListCtrl
		try:
			self.Setup()
		except Exception, e:
			import traceback
			traceback.print_exc()
			print e

		# Hide the Location Control
		self.OnToggleLocation(False)

		self.CenterOnScreen(wx.BOTH)
		return winBaseXRC.Show(self)

	def OnCancel(self, evt):
		self.application.gui.Show(self.application.gui.connectto)	

	def OnRefresh(self, evt=None):
		self.Progress.LoadFile(throbber)
		self.Progress.Play()

		self.application.finder.Call(self.application.finder.refresh)

		# Disable the refresh button until the finder is done...
		self.Refresh.Disable()

	def OnRefreshFinished(self, worked, message=""):
		# Renable the refresh button
		self.Refresh.Enable()

		if worked:
			self.Progress.LoadFile(okay)
		else:
			self.Progress.LoadFile(notokay)
		self.Progress.Play()

		self.Progress.SetToolTip(message)

	def OnFinderError(self, evt):
		self.RefreshFinished(False, unicode(evt))

	def OnFinderFinished(self, evt):
		self.RefreshFinished(True)

	# Config Functions -----------------------------------------------------------------------------  
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		return {}

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		return {}
	
	def ConfigLoad(self, config={}):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		pass

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		pass

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		pass

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		pass

