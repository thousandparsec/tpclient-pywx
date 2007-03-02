"""\
This module contains the main menu window.
"""

# Python imports
import copy
import time
import math
import os.path

# wxPython imports
import wx
import wx.lib.popupctl as pop

# Local imports
from winBase import *
from utils import *

ID_MENU = 10042
ID_OPEN = 10043
ID_UNIV = 10044
ID_REVERT = 10046
ID_CONFIG = 10047
ID_EXIT = 10049
ID_FILE = 10050

ID_STAT_EAAG = 10051
ID_STAT_SYSTEM = 10052
ID_STAT_PLANET = 10053
ID_STAT_FLEET = 10054
ID_STAT_BATTLE = 10055
ID_STATS = 10056

ID_WIN_TIPS	 = 11006
ID_WIN_HELP = 1105

ID_HELP = 10057

Mb = 1024*1024
Kb = 1024
def tos(n):
	if n > Mb:
		return "%.1fM" % (float(n)/Mb)
	if n > Kb:
		return "%.1fK" % (float(n)/Kb)
	return "%sb" % n

class MediaProgress(wx.PopupCtrl):
	def __init__(self, parent, application, *args, **kw):
		wx.PopupCtrl.__init__(self, parent, *args, **kw)
		self.application = application

		self.SetPopupCtrl(wx.Gauge(self))

		self.win  = wx.Window(self,-1,pos = (0,0),style = 0)
		self.list = wx.ListBox(self.win)

		self.SetPopupContent(self.win)

		self.win.Bind(wx.EVT_LISTBOX, self.OnSelect, self.list)
		self.win.Bind(wx.EVT_LISTBOX_DCLICK, self.OnSelect, self.list)

		self.listitems = []

	def OnSelect(self, evt):
		self.PopDown()
		print "OnSelect", evt.GetString()

	def OnButton(self,evt):
		if len(self.listitems) > 1: 
			self.PopUp()

	def FormatContent(self):
		self.list.Set(self.listitems)

		s = self.list.GetBestSize()
		s += (0, 10)
		self.list.SetSize(s)
		self.win.SetClientSize(s)

class StatusBar(wx.StatusBar):
	WIDGET_PROGRESS = 0
	WIDGET_PROGRESS_CANCEL = 1
	WIDGET_TEXT = 3
	TEXT_PROGRESS = 2
	TEXT_TIMER = 3

	def __init__(self, application, parent):
		wx.StatusBar.__init__(self, parent, -1)

		self.application = application

		self.SetFieldsCount(4)
		self.SetStatusWidths([-3, 20, -3, -2])

		self.Progress = MediaProgress(self, application, -1)
		self.ProgressCancel = wx.Button(self, -1, "X")
		self.ProgressCancel.Enable(False)

		self.StatusTextCtrl = wx.TextCtrl(self, -1, "")
		self.StatusTextCtrl.SetEditable(False)

		self.SetStatusText("", StatusBar.TEXT_TIMER)
		self.SetStatusText("", StatusBar.TEXT_PROGRESS)

		self.endtime = 0
		self.parent = parent

		self.timer = wx.PyTimer(self.Notify)
		self.timer.Start(1000)
		self.Notify()

		self.Reposition()
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_BUTTON, self.OnButtonCancel, self.ProgressCancel)

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

			hours = math.floor(left / sih)
			mins = math.floor((left - hours * sih) / sim)
			secs = math.floor((left - hours * sih - mins * sim))
			self.StatusTextCtrl.SetValue("EOT: %02i:%02i:%02i" % (hours, mins, secs))
		else:
			self.StatusTextCtrl.SetValue("EOT: Unknown")
	
	def SetEndTime(self, endtime):
		print endtime
		self.endtime = endtime

	def Reposition(self):
		rect = self.GetFieldRect(StatusBar.WIDGET_PROGRESS)
		self.Progress.SetPosition((rect.x+4, rect.y+2))
		self.Progress.SetSize((rect.width-6, rect.height-4))

		rect = self.GetFieldRect(StatusBar.WIDGET_PROGRESS_CANCEL)
		self.ProgressCancel.SetPosition((rect.x, rect.y))
		self.ProgressCancel.SetSize((rect.width, rect.height))

		rect = self.GetFieldRect(StatusBar.WIDGET_TEXT)
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

	def OnMediaDownloadStart(self, evt):
		self.progress = evt.file

		self.Progress.SetRange(evt.size)
		files = []
		for file in self.application.media.todownload.keys():
			if file != evt.file:
				files.append(file)
		self.Progress.listitems = files
		self.ProgressCancel.Enable(True)

		self.SetStatusText("Dw: %s" % os.path.basename(evt.file), StatusBar.TEXT_PROGRESS)

	def OnMediaDownloadProgress(self, evt):
		self.Progress.SetRange(evt.size)
		self.Progress.SetValue(evt.progress)
		
		tt = wx.ToolTip("%s of %s" % (tos(evt.progress), tos(evt.size)))
		tt.Enable(True)
		self.SetToolTip(tt)

	def OnMediaDownloadDone(self, evt):
		self.Clear()

	def OnMediaDownloadAbort(self, evt):
		self.Clear()

	def OnButtonCancel(self, evt):
		self.parent.application.media.StopFile(self.progress)


class winMain(winMDIBase):
	title = _("Thousand Parsec")

	def __init__(self, application):
		winMDIBase.__init__(self, application)

		self.statusbar = StatusBar(application, self)
		self.SetStatusBar(self.statusbar)
		self.SetMenuBar(self.Menu(self))

		from windows.winDesign import winDesign
		winDesign(application, self)

		self.mgr = wx.aui.AuiManager()
		self.mgr.SetFrame(self)

		from windows.winInfo    import panelInformation
		from windows.winOrder   import panelOrder
		from windows.winMessage import panelMessage
		from windows.winStarMap import panelStarMap
		from windows.winSystem  import panelSystem

		for window in [panelInformation, panelOrder, panelMessage, panelStarMap, panelSystem]:
			title = window.title

			instance = window(application, self)

			self.mgr.AddPane(instance, instance.GetPaneInfo().Caption(title)) 
			self.children[title] = instance

		self.mgr.Update()

		self.updatepending = False

	def OnMediaDownloadStart(self, evt):
		self.statusbar.OnMediaDownloadStart(evt)
	def OnMediaDownloadProgress(self, evt):
		self.statusbar.OnMediaDownloadProgress(evt)
	def OnMediaDownloadDone(self, evt):
		self.statusbar.OnMediaDownloadDone(evt)		
	def OnMediaDownloadAbort(self, evt):
		self.statusbar.OnMediaDownloadAbort(evt)		

	def Show(self, show=True):
		# Show this window and it's children - also fixes menus for MacOS
		if not show:
			return self.Hide()

		for window in self.children.values():
			try:
				if window.config.has_key('show') and window.config['show']:
					window.Show()
			except Exception, e:
				print e

		winMDIBase.Show(self)

		wx.CallAfter(self.mgr.Update)
		wx.CallAfter(self.ShowTips)

	def Hide(self, show=True):
		if not show:
			return self.Show()

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
		file.Append( ID_OPEN, _("Connect to Game\tCtrl-O"), _("Connect to a diffrent Game") )
		file.Append( ID_UNIV, _("Download the Universe\tCtrl-U"), _("Download the Universe") )
		file.AppendSeparator()
		file.Append( wx.ID_PREFERENCES, _("Preferences"), _("Configure the Client") )
		file.AppendSeparator()
		file.Append( ID_EXIT, _("Exit"), _("Exit") )

		# Statistics Menu
		stat = wx.Menu()
		stat.Append( ID_STAT_EAAG, _("Empire at a Glance"), _("") )
		stat.AppendSeparator()
		stat.Append( ID_STAT_SYSTEM, _("Systems"), _("") )
		stat.Append( ID_STAT_PLANET, _("Planets"), _("") )
		stat.Append( ID_STAT_FLEET,  _("Fleets"),  _("") )
		stat.AppendSeparator()
		stat.Append( ID_STAT_BATTLE, _("Battles"), _("") )

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
		for title in self.children.keys():
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
		bar.Append( stat, _("Statistics") )
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
			tp = wx.CreateFileTipProvider(os.path.join("doc", "tips.txt"), config[1])
			config[0] = wx.ShowTip(None, tp)
			config[1] = tp.GetCurrentTip()

			save_data("pywx_tips", config)

	def UpdateCache(self, evt=None):
		self.application.network.Call(self.application.network.CacheUpdate)

	def OnNetworkTimeRemaining(self, evt):
		if evt.remaining == 0:
			if not self.updatepending:
				self.updatepending = True
				msg = """\
The turn has ended. Would you like to download all the new details?
"""
				dlg = wx.MessageDialog(self.application.gui.current, msg, _("Update?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_INFORMATION)
				if dlg.ShowModal() == wx.ID_YES:
					self.UpdateCache()
				self.updatepending = False
		else:
			print "Got an updated EOT..."
			self.statusbar.SetEndTime(evt.gotat + evt.remaining)

