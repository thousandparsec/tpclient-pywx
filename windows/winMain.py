"""
This is the primary window for interacting with the game.
"""

# Python imports
import time
import math
import os.path

# wxPython imports
import wx

# Local imports
from requirements import docdir
from winBase import winBase
from utils import *

ID_MENU = 10042
ID_OPEN = 10043
ID_UNIV = 10044
ID_EXIT = 10049
ID_FILE = 10050

ID_WIN_TIPS	 = 11006
ID_WIN_HELP = 1105

ID_HELP = 10057

class StatusBar(wx.StatusBar):
	TEXT_TIMER = 1

	def __init__(self, application, parent):
		wx.StatusBar.__init__(self, parent, -1)

		self.application = application

		self.SetFieldsCount(2)
		self.SetStatusWidths([-10, -2])

		self.StatusTextCtrl = wx.TextCtrl(self, -1, "")
		self.StatusTextCtrl.SetEditable(False)

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

	def Reposition(self):
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

		# Setup the status bar
		self.statusbar = StatusBar(application, self)
		self.SetStatusBar(self.statusbar)

		# Actual windows
		from windows.main.winDesign import winDesign
		from windows.main.winIdleFinder import winIdleFinder

		self.windows = {}
		for window in [winDesign, winIdleFinder]:
			title = window.title
			self.windows[title] = window(application, self)
			
		# Setup the AUI interface
		self.mgr = wx.aui.AuiManager()
		self.mgr.SetManagedWindow(self)

		# Panel in the AUI interface...
		from windows.main.panelInfo    import panelInformation
		from windows.main.panelPicture import panelPicture
		from windows.main.panelOrder   import panelOrder
		from windows.main.panelMessage import panelMessage
		from windows.main.panelStarMap import panelStarMap
		from windows.main.panelSystem  import panelSystem

		self.panels = {}
		for panel in [panelStarMap, panelSystem, panelMessage, panelInformation, panelPicture, panelOrder]:
			title = panel.title

			instance = panel(application, self)

			self.mgr.AddPane(instance, instance.GetPaneInfo().Caption(title)) 
			self.panels[title] = instance

		self.mgr.Update()

		# Setup the Menu
		self.SetMenuBar(self.Menu(self))

		self.updatepending = False
		
		self.application.gui.Binder(self.application.NetworkClass.NetworkTimeRemainingEvent, self.OnNetworkTimeRemaining)

	def Show(self, show=True):
		# Show this window and it's children - also fixes menus for MacOS
		if not show:
			return self.Hide()

		for window in self.children.values():
			try:
				if hasattr(window, 'config'):
					if not window.config.has_key('show') or not window.config['show']:
						continue
				window.Show()
			except Exception, e:
				print "Showing children error", window, e

		winBase.Show(self)

		# FIXME: Hack until perspective loading is done..
		self.Maximize()

		# Make the windows all reposition themselves...
		wx.CallAfter(self.mgr.Update)

		# Show the tips..
		wx.CallAfter(self.ShowTips)

	def Hide(self, show=True):
		if not show:
			return self.Show()

		#if hasattr(self, "tips"):
		#	self.tips.Close()

		for window in self.children.values():
			window.Hide()
		super(self.__class__, self).Hide()

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
		file.Append( ID_OPEN, _("C&onnect to Game\tCtrl-O"), _("Connect to a diffrent Game") )
		file.Append( ID_UNIV, _("Download the &Universe\tCtrl-U"), _("Download the Universe") )
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
			win.Append(id, _("Show " + title), _(""), True )

			# Bind the events
			source.Bind(wx.EVT_MENU, source.OnMenuWindowItem, id=id)
			app.Bind(wx.EVT_UPDATE_UI, source.OnMenuWindowUpdate, id=id)

		win.AppendSeparator()
		win.Append(ID_WIN_TIPS, _("Show Tips"), _(""), True )
		win.Append(ID_WIN_HELP, _("Help"),      _(""), True)

		help = wx.Menu()

		bar.Append( file, _("File") )
		#bar.Append( stat, _("Statistics") )
		bar.Append( win,  _("Windows") )
		bar.Append( help, _("&Help") )

		source.Bind(wx.EVT_MENU, self.OnConnect,     id=ID_OPEN)
		source.Bind(wx.EVT_MENU, self.UpdateCache,   id=ID_UNIV)
		source.Bind(wx.EVT_MENU, self.OnConfig,      id=wx.ID_PREFERENCES)
		source.Bind(wx.EVT_MENU, self.OnProgramExit, id=ID_EXIT)

		source.Bind(wx.EVT_MENU, self.ShowTips, id=ID_WIN_TIPS)
		return bar

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

		if config[0] or override != None:
			self.tips = wx.CreateFileTipProvider(os.path.join(docdir, "tips.txt"), config[1])

			config[0] = wx.ShowTip(self, self.tips)
			config[1] = self.tips.GetCurrentTip()

			save_data("pywx_tips", config)

	def UpdateCache(self, evt=None):
		self.application.network.Call(self.application.network.CacheUpdate)

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

