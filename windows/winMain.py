"""
This is the primary window for interacting with the game.
"""

# Python imports
import time
import math
import os.path
import sys

# wxPython imports
import wx
from wx.lib.wordwrap import wordwrap


# Local imports
from requirements import docdir, graphicsdir
from winBase import winBase
from utils import *
from extra import objectutils
import version

ID_MENU = 10042
ID_OPEN = 10043
ID_UNIV = 10044
ID_TURN = 10045
ID_EXIT = 10049
ID_FILE = 10050

ID_WIN_TIPS	 = 11006
ID_WIN_HELP = 1105

ID_HELP   = 10057
ID_ONLINE = 10058 
ID_ABOUT  = 10059

class StatusBar(wx.StatusBar):
	TURN_NUMBER = 1
	TEXT_TIMER = 2

	def __init__(self, application, parent):
		wx.StatusBar.__init__(self, parent, -1)

		self.application = application

		self.SetFieldsCount(3)
		self.SetStatusWidths([-10, -1, -2])

		self.StatusTextCtrl = wx.TextCtrl(self, -1, "")
		self.StatusTextCtrl.SetEditable(False)

		self.TurnTextCtrl = wx.TextCtrl(self, -1, "")
		self.TurnTextCtrl.SetEditable(False)

		self.endtime = 0
		self.parent = parent

		self.timer = wx.PyTimer(self.Notify)
		self.timer.Start(1000)
		self.Notify()

		self.Reposition()
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)

	def Notify(self):
		sih = 60*60
		sim = 60

		left = self.endtime - time.time()
		if left > 0:
			if left < 120 and left > 0:
				# Flash the bar
				if int(left) % 2 == 0:
					self.StatusTextCtrl.SetOwnBackgroundColour(wx.NullColour)
				else:
					self.StatusTextCtrl.SetOwnBackgroundColour(wx.Colour(255,0,0))
			else:
				self.StatusTextCtrl.SetOwnBackgroundColour(wx.NullColour)

			hours = math.floor(left / sih)
			mins = math.floor((left - hours * sih) / sim)
			secs = math.floor((left - hours * sih - mins * sim))
			self.StatusTextCtrl.SetValue("EOT: %02i:%02i:%02i" % (hours, mins, secs))
		else:
			self.StatusTextCtrl.SetValue("EOT: Unknown")
	
	def SetEndTime(self, endtime):
		self.endtime = endtime

	def SetTurnNumber(self, turn):
		self.TurnTextCtrl.SetValue("Year: %s" % turn)

	def Reposition(self):
		rect = self.GetFieldRect(StatusBar.TURN_NUMBER)
		self.TurnTextCtrl.SetPosition((rect.x, rect.y))
		self.TurnTextCtrl.SetSize((rect.width, rect.height))

		rect = self.GetFieldRect(StatusBar.TEXT_TIMER)
		self.StatusTextCtrl.SetPosition((rect.x, rect.y))
		self.StatusTextCtrl.SetSize((rect.width, rect.height))
		
		self.sizeChanged = False

	def Clear(self):
		self.Progress.SetValue(0)
		self.Progress.SetRange(0)
		self.ProgressCancel.Enable(False)

		tt = wx.ToolTip("")
		tt.Enable(False)
		self.SetToolTip(tt)

		self.SetStatusText("", StatusBar.TEXT_PROGRESS)

		del self.progress

	def OnSize(self, evt):
		self.Reposition()
		self.sizeChanged = True

	def OnIdle(self, evt):
		if self.sizeChanged:
			self.Reposition()

class winMain(winBase):
	title = _("Thousand Parsec")

	def children_get(self):
		r = {}
		r.update(self.windows)
		r.update(self.panels)
		return r
	def children_set(self, value):
		return
	children = property(children_get, children_set)

	def __init__(self, application):
		winBase.__init__(self, application)

		self.Maximize()
		self.Layout()

		# Have to manipulate the ClientSize to stop flickering from the AUI manager.
		self.statusbar = StatusBar(application, self)
		self.SetClientSize((self.GetClientSize()[0], self.GetClientSize()[1]-self.statusbar.GetSize()[1]))

		self.SetStatusBar(self.statusbar)

		# Actual windows
		from windows.main.winDesign import winDesign
		from windows.main.winIdleFinder import winIdleFinder
		from windows.main.winDownloadManager import winDownloadManager

		self.windows = {}
		for window in [winDesign, winIdleFinder, winDownloadManager]:
			title = window.title
			self.windows[title] = window(application, self)
			
		# Setup the AUI interface
		self.mgr = wx.aui.AuiManager()
		self.mgr.SetManagedWindow(self)

		# Panel in the AUI interface...
		from windows.main.panelInfo    import panelInformation
		from windows.main.panelOrder   import panelOrder
		from windows.main.panelMessage import panelMessage
		from windows.main.panelStarMap import panelStarMap
		from windows.main.panelSystem  import panelSystem

		self.panels = {}
		for panel in [panelStarMap, panelMessage, panelSystem, panelOrder, panelInformation]:
			title = panel.title

			instance = panel(application, self)
			# Catch closing panel by X sign
			instance.Bind(wx.EVT_SHOW, self.MenuPanelUpdate)

			self.mgr.AddPane(instance, instance.GetPaneInfo())
			self.panels[title] = instance

		self.mgr.Update()

		# Setup the Menu
		self.SetMenuBar(self.Menu(self))

		self.updatepending = False
		self.application.gui.Binder(self.application.NetworkClass.NetworkTimeRemainingEvent, self.OnNetworkTimeRemaining)

	def Show(self, show=True):
		if not show:
			return self.Hide()

		winBase.Show(self)

		# Show the tips..
		wx.CallAfter(self.ShowTips)

	# Config Functions -----------------------------------------------------------------------------
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		return

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		# Get the details from there children
		for window in self.children.values():
			try:
				self.config[window.title] = window.ConfigSave()
			except Exception, e:
				print e

		return self.config

	def ConfigLoad(self, config={}):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		return

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		return

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		return

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		return

	# Menu bar options
	##################################################################
	def Menu(self, source):
		app = wx.GetApp()
		bar = wx.MenuBar()

		# File Menu
		file = wx.Menu()
		file.Append( ID_OPEN, _("C&onnect to Game\tCtrl-O"),       _("Connect to a different Game") )
		file.Append( ID_UNIV, _("Download the &Universe\tCtrl-U"), _("Download the Universe") )
		file.Append( ID_TURN, _("Request End of &Turn\tCtrl-T"),   _("Send a message to the server requesting the turn end soon.") )
		file.AppendSeparator()
		file.Append( wx.ID_PREFERENCES, _("&Preferences"), _("Configure the Client") )
		file.AppendSeparator()
		file.Append( ID_EXIT, _("Exit"), _("Exit") )

		# Windows Menu
		win = wx.Menu()

		# FIXME: Hack!
		def OnMenuWindowItem(evt, self=source, windows=self.children):
			window = windows[self.menu_ids[evt.GetId()]]
			window.Show(evt.Checked())
		source.OnMenuWindowItem = OnMenuWindowItem

		def OnMenuWindowUpdate(evt, self=source, windows=self.children):
			menu = self.GetMenuBar().FindItemById(evt.GetId())
			if menu.IsChecked() != windows[self.menu_ids[evt.GetId()]].IsShown():
				menu.Toggle()
		source.OnMenuWindowUpdate = OnMenuWindowUpdate

		source.menu_ids = {}
		for title in self.windows.keys():
			id = wx.NewId()
			source.menu_ids[id] = title

			# Add the menu item
			win.Append(id, _("Show " + title), "", True )

			# Bind the events
			source.Bind(wx.EVT_MENU, source.OnMenuWindowItem, id=id)
			app.Bind(wx.EVT_UPDATE_UI, source.OnMenuWindowUpdate, id=id)

		win.AppendSeparator()
		win.Append(ID_WIN_TIPS, _("Show Tips"), "", False )

		# Panels Menu
		panels_menu = wx.Menu()
		self.menu_id_to_panel = {}

		# Create menu item for every panel
		for panel in self.panels.values():
			id = wx.NewId()
			self.menu_id_to_panel[id] = panel
			panels_menu.Append(id, _("Show %s" % panel.title), "Show or hide %s panel.", True)

			# All panels are initially shown, so check corresponding item
			panels_menu.Check(id, True)
			source.Bind(wx.EVT_MENU, source.OnMenuPanelItem, id=id)

		help = wx.Menu()
		help.Append( ID_ONLINE, _("Online Help"), _("Go to the online help page."))
		help.Append( ID_ABOUT,  _("About"),  _("About the client you are running...") )

		# Menu bar and menu bindings
		bar.Append( file, _("File") )
		bar.Append( win,  _("Windows") )
		bar.Append( panels_menu, _("Panels"))
		bar.Append( help, _("&Help") )

		source.Bind(wx.EVT_MENU, self.OnConnect,     id=ID_OPEN)
		source.Bind(wx.EVT_MENU, self.UpdateCache,   id=ID_UNIV)
		source.Bind(wx.EVT_MENU, self.RequestEOT,    id=ID_TURN)
		source.Bind(wx.EVT_MENU, self.OnConfig,      id=wx.ID_PREFERENCES)
		source.Bind(wx.EVT_MENU, self.OnProgramExit, id=ID_EXIT)

		source.Bind(wx.EVT_MENU, self.OnHelp,        id=ID_ONLINE)
		source.Bind(wx.EVT_MENU, self.OnAbout,       id=ID_ABOUT)

		source.Bind(wx.EVT_MENU, self.ShowTips, id=ID_WIN_TIPS)
		return bar

	def OnMenuPanelItem(self, evt):
		id = evt.GetId()
		panel = self.menu_id_to_panel[evt.GetId()]

		self.mgr.GetPane(panel).Show(evt.Checked())
		self.mgr.Update()

	def MenuPanelUpdate(self, evt=None):
		"""\
		Update menu items in Panels submenu according to currenly shown panels.

		This function can be called directly (and then whole menu is rechecked)
		or as a handler to EVT_SHOW from panel.
		"""
		menubar = self.GetMenuBar()
		if(evt is None):
			# Update all menu items
			for id in self.menu_id_to_panel.keys():
				panel = self.menu_id_to_panel[id]
				menubar.FindItemById(id).Check(self.mgr.GetPane(panel).IsShown())
		elif(not evt.GetShow() and evt.EventObject in self.panels.values()):
			# Handle only 'not shown' case, it occurs when the user clicks on X mark in panel title

			# Invert menu_id_to_panel dict
			panel_to_menu_id = dict(zip(self.menu_id_to_panel.values(), self.menu_id_to_panel.keys()))
			id = panel_to_menu_id[evt.EventObject]
			menubar.FindItemById(id).Check(False)

	def AccelTable(self, source):
		source.Bind(wx.EVT_KEY_DOWN, self.temp)

		# File Menu
		table = wx.AcceleratorTable([
			(wx.ACCEL_CTRL, ord('O'), ID_OPEN),
			(wx.ACCEL_CTRL, ord('U'), ID_UNIV),
		])
		source.Bind(wx.EVT_MENU, self.temp)
		source.Bind(wx.EVT_MENU, self.OnConnect,     id=ID_OPEN)
		source.Bind(wx.EVT_MENU, self.UpdateCache,   id=ID_UNIV)
		return table

	def OnConnect(self, evt):
		self.application.gui.Show(self.application.gui.connectto)

	def OnConfig(self, evt):
		self.application.ConfigDisplay()

	def OnClose(self, evt):
		self.OnProgramExit(evt)

	def OnProgramExit(self, evt):
		self.mgr.UnInit()
		self.application.Exit()

	def ShowTips(self, override=None):
		config = load_data("pywx_tips")
		if not config:
			config = [True, 0]

		# FIXME: We need some way to programmatically close the tips dialog
		if config[0] or override != None:
			self.tips = wx.CreateFileTipProvider(os.path.join(docdir, "tips.txt"), config[1])

			config[0] = wx.ShowTip(self, self.tips)
			config[1] = self.tips.GetCurrentTip()

			save_data("pywx_tips", config)
		
		# Show the "No Objects" warning message
		foundanobject = False
		for id in self.application.cache.objects:
			owner = objectutils.getOwner(self.application.cache, id)
			if owner == self.application.cache.players[0].id:

				foundanobject = True
		if foundanobject == False:
			wx.CallAfter(self.ShowNoObjectsWarning)
	
	def ShowNoObjectsWarning(self):
		from windows.main.winHelp import winHelp
		help = winHelp(self.application, self)
		help.SetMessage(help.message_NoObjects_Subject, help.message_NoObjects_Body)
		help.Show()

	def UpdateCache(self, evt=None):
		self.application.network.Call(self.application.network.CacheUpdate)

	def RequestEOT(self, evt):
		"""\
		"""
		self.application.network.Call(self.application.network.RequestEOT)

	def OnNetworkTimeRemaining(self, evt):
		if evt.remaining == 0:
			if not self.updatepending:
				self.updatepending = True
				msg = _("""\
The turn has ended. Would you like to download all the new details?
""")
				dlg = wx.MessageDialog(self.application.gui.current, msg, _("Update?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_INFORMATION)
				if dlg.ShowModal() == wx.ID_YES:
					self.UpdateCache()
				self.updatepending = False
		else:
			self.statusbar.SetEndTime(evt.gotat + evt.remaining)

	def OnHelp(self, evt):
		url = "http://www.thousandparsec.net/tp/documents/tpclient-pywx?version=%s" % version.version_str
		if hasattr(version, "version_git"):
			url += "&version_git=%s" % version.version_git
		from extra.Opener import open
		open(url)

	def OnAbout(self, evt):
		info = wx.AboutDialogInfo()
		info.Name = _("wxPython Client")
		info.Version = version.version_str
		info.Copyright = _("(C) 2001-2008 Thousand Parsec Developers")
		info.Description = wordwrap(_("""\
This Thousand Parsec client, written in python, is an easy way to \
join and start playing in a Thousand Parsec game."""),
			350, wx.ClientDC(self))
		info.WebSite = ("http://www.thousandparsec.net", "Thousand Parsec Website")
		info.License = wordwrap(open(os.path.join(docdir, "COPYING"), 'r').read(), 600, wx.ClientDC(self))

		icon = wx.Icon(os.path.join(graphicsdir, "tp-icon-80x80.png"), wx.BITMAP_TYPE_PNG)
		info.Icon = icon

		# Then we call wx.AboutBox giving it that info object
		wx.AboutBox(info)
		

