
# Python imports
import string
import os, os.path
import time

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBaseXRC
from xrc.winServerBrowser import winServerBrowserBase

throbber = os.path.join("graphics", "downloading.gif")
okay = os.path.join("graphics", "finished.gif")
notokay = os.path.join("graphics", "waiting.gif")

class winServerBrowser(winServerBrowserBase, winMainBaseXRC):
	title = _("Updating")
	
	ServersColumns = ["Name", "Playing", "Server", "P", "C", "O", "Other"]
	ServersColumns_Sizes = [
			wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, 100, 
			wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, 
			-1]
	LocationsColumns = ["Type", "DNS", "IP", "Port"]
	LocationsColumns_Sizes = [
			wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE, wx.LIST_AUTOSIZE]

	def __init__(self, application):
		winServerBrowserBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)
		
		self.Servers.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnServerSelect)
		self.Locations.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnLocationSelect)
		self.LocationsBox.Bind(wx.EVT_LEFT_DOWN, self.OnToggleLocation)
		self.LocationsPanel.Bind(wx.EVT_LEFT_DOWN, self.OnToggleLocation)

		self.OnToggleLocation(False)

	def Setup(self):
		ctrl = self.Servers
		Columns, Columns_Sizes = self.ServersColumns, self.ServersColumns_Sizes

		local, remote = self.application.finder.Games()

		ctrl.ClearAll()
		for i, name in enumerate(Columns):
			ctrl.InsertColumn(i, name)
		for games in (local, remote):
			for game in games.values():
				i = ctrl.GetItemCount()

				ctrl.InsertStringItem(i, "")
				ctrl.SetItemPyData(i, game)

				ctrl.SetStringItem(i, Columns.index("Name"), game.name)
				if game.name in local:
					game.where = "local"
					ctrl.SetItemTextColour(i, wx.Color(0,0,255))
				else:
					game.where = "remote"

				try:
					ctrl.SetStringItem(i, Columns.index("Playing"), "%s (%s)" % (game.rule, game.rulever))
				except AttributeError: pass
				try:
					ctrl.SetStringItem(i, Columns.index("Server"),  "%s (%s)" % (game.sertype, game.server))
				except AttributeError: pass

				try:
					ctrl.SetToolTipItem(i, game.cmt)
				except AttributeError: pass

				try:
					ctrl.SetStringItem(i, Columns.index("C"),  game.cons)
				except AttributeError: pass

				try:
					ctrl.SetStringItem(i, Columns.index("O"),  game.cons)
				except AttributeError: pass

				try:
					ctrl.SetStringItem(i, Columns.index("P"),  game.plys)
				except AttributeError: pass
			for i, name in enumerate(Columns):
				ctrl.SetColumnWidth(i, Columns_Sizes[i])

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
				print repr((type, dns, ip, port))
				i = ctrl.GetItemCount()

				ctrl.InsertStringItem(i, "")
				ctrl.SetStringItem(i, Columns.index("Type"), type)
				ctrl.SetStringItem(i, Columns.index("DNS"),  dns)
				ctrl.SetStringItem(i, Columns.index("IP"),	 ip)
				ctrl.SetStringItem(i, Columns.index("Port"), str(port))

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
		return winMainBaseXRC.Show(self)

	def OnCancel(self, evt):
		self.application.gui.Show(self.application.gui.connectto)	

	def OnRefresh(self, evt=None):
		print "Refresh!"
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
		self.RefreshFinished(False, str(evt))

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

