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
			if self.endtime != 0:
				self.parent.UpdateEOT()
				self.endtime = 0
			self.StatusTextCtrl.SetValue("EOT: Unknown")
	
	def SetEndTime(self, endtime):
		print endtime
		self.endtime = endtime + time.time()

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
	title = _("Main Windows")

	from defaults import winMainDefaultPosition as DefaultPosition
	from defaults import winMainDefaultSize as DefaultSize
	from defaults import winMainDefaultShow as DefaultShow

	def __init__(self, application):
		winMDIBase.__init__(self, application)

		self.statusbar = StatusBar(application, self)
		self.SetStatusBar(self.statusbar)

		from windows.winDesign import winDesign
		winDesign(application, self)

		from windows.winInfo import winInfo
		winInfo(application, self)

		from windows.winMessage import winMessage
		winMessage(application, self)

		from windows.winOrder import winOrder
		winOrder(application, self)

		from windows.winStarMap import winStarMap
		winStarMap(application, self)

		from windows.winSystem import winSystem
		winSystem(application, self)

		self.SetMenuBar(self.Menu(self))

		if wx.Platform == "__WXMAC__":
			for window in self.children.values():
				window.SetMenuBar(self.Menu(window))

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
			if window.config.has_key('show') and window.config['show']:
				window.Show()

		# Lock the size for non-MDI platforms
		if wx.Platform != "__WXMSW__":
			self.SetSizeHard(self.config['size'])

		winMDIBase.Show(self)

		wx.CallAfter(self.ShowTips)

		self.UpdateEOT()

	def Hide(self, show=True):
		if not show:
			return self.Show()

		for window in self.children.values():
			window.Hide()
		super(self.__class__, self).Hide()

	def SetSizeHard(self, size):
		winMDIBase.SetSize(self, size)
		if wx.Platform != "__WXMSW__":
			self.SetClientSize(wx.Size(-1,0))
			winMDIBase.SetSizeHard(self, (-1, self.GetSize()[1]))

	# Config Functions -----------------------------------------------------------------------------
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		SCREEN_X = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
		SCREEN_Y = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)

		if config == None:
			config = {}

		# Raise mode
		try:
			if not config['raise'] in ("Individual", "All on Main", "All on All"):
				raise ValueError('Config-%s: a raise value of %s is not valid' % (self, config['raise']))
		except (ValueError, KeyError), e:
			config['raise'] = "All on Main"

		# Where is the window position
		try:
			if not isinstance(config['position'][0], int) or not isinstance(config['position'][1], int):
				raise ValueError('Config-%s: position %s is not valid' % (self, config['position']))
			if config['position'][0] > SCREEN_X or config['position'][1] > SCREEN_Y:
				raise ValueError('Config-%s: position %s is off the screen' % (self, config['position']))
		except (ValueError, KeyError), e:
			if self.DefaultPosition.has_key((SCREEN_X, SCREEN_Y)):
				config['position'] = self.DefaultPosition[(SCREEN_X, SCREEN_Y)]
			else:
				print "Config-%s: Did not find a default position for your resolution" % (self,)
				config['position'] = (0,0)

		# How big is the window
		try:
			if not isinstance(config['size'], int):
				raise ValueError('Config-%s: size %s is not valid' % (self, config['size']))
		except (ValueError, KeyError), e:
			if self.DefaultSize.has_key((SCREEN_X, SCREEN_Y)):
				config['size'] = self.DefaultSize[(SCREEN_X, SCREEN_Y)]
			else:
				print "Config-%s: Did not find a default size for your resolution" % (self,)
				if wx.Platform != "__WXMSW__":
					config['size'] = self.DefaultSize[(1024, 768)]
				else:
					config['size'] = (SCREEN_X, SCREEN_Y)

		return config

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		# Get the details from there children
		for window in self.children.values():
			self.config[window.title] = window.ConfigSave()

		return self.config

	def ConfigLoad(self, config={}):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		self.ConfigDefault(config)
		self.config = copy.copy(config)

		for name, window in self.children.items():
			window.ConfigLoad(config.get(name, {}))
			
		self.SetSizeHard(config['size'])
		self.SetPosition(config['position'])

		self.ConfigDisplayUpdate(None)

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		if self.application.gui.current is self:
			self.config['show'] = self.IsShown()
		self.config['position'] = self.GetPosition()
		self.config['size'] = self.GetSize()

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		notebook = wx.Choicebook(panel, -1)
		cpanel = wx.Panel(notebook, -1)
		csizer = wx.BoxSizer(wx.HORIZONTAL)

		if wx.Platform == '__WXMSW__':
			options = [_("Individual"), _("All on Main")]
		elif wx.Platform == '__WXMAC__':
			options = [_("Individual"), _("All on All")]
		else:
			options = [_("Individual"), _("All on Main"), _("All on All")]

		# Sizes we will need
		SCREEN_X = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_X)
		SCREEN_Y = wx.SystemSettings_GetMetric(wx.SYS_SCREEN_Y)
		SIZER_FLAGS = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL

		# The box around the position
		box = wx.StaticBox(cpanel, -1, self.title)
		box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
		csizer.Add(box_sizer, 1, SIZER_FLAGS, 5 )

		# Location Boxes
		location = wx.FlexGridSizer( 0, 2, 0, 0 )
		location.AddGrowableCol( 1 )

		# X Position
		x_text = wx.StaticText(cpanel, -1, _("X Pos"))
		location.Add( x_text, 0, SIZER_FLAGS, 5 )

		x_box = wx.SpinCtrl(cpanel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, SCREEN_X, 0 )
		location.Add( x_box, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		cpanel.Bind(wx.EVT_SPINCTRL, self.OnConfigDisplayX, x_box)

		# Y Position
		y_text = wx.StaticText(cpanel, -1, _("Y Pos"))
		location.Add( y_text, 0, SIZER_FLAGS, 5 )

		y_box = wx.SpinCtrl(cpanel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, SCREEN_Y, 0 )
		location.Add( y_box, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		cpanel.Bind(wx.EVT_SPINCTRL, self.OnConfigDisplayY, y_box)

		# Width
		width_text = wx.StaticText(cpanel, -1, _("Width"))
		location.Add( width_text, 0, SIZER_FLAGS, 5 )

		width = wx.SpinCtrl(cpanel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, SCREEN_X, 0 )
		location.Add( width, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		cpanel.Bind(wx.EVT_SPINCTRL, self.OnConfigDisplayWidth, width)

		box_sizer.Add( location, 0, SIZER_FLAGS, 5)

		self.Bind(wx.EVT_MOVE, self.OnConfigDisplayMove)
		self.Bind(wx.EVT_ACTIVATE, self.ConfigDisplayUpdate)

		raisebox = wx.RadioBox(cpanel, -1, _("Raise Mode"), choices=options, majorDimension=1, style=wx.RA_SPECIFY_COLS)
		raisebox.SetToolTip( wx.ToolTip(_("Choose a method for raising the windows.")) )
		csizer.Add( raisebox, 1, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		cpanel.Bind(wx.EVT_RADIOBOX, self.OnConfigRaise, raisebox)

		cpanel.SetSizer( csizer )
		cpanel.Layout()

		notebook.AddPage(cpanel, "Menubar")

		for name, window in self.children.items():
			cpanel = wx.Panel(notebook, -1)
			csizer = wx.BoxSizer(wx.HORIZONTAL)

			window.ConfigDisplay(cpanel, csizer)

			cpanel.SetSizer( csizer )
			notebook.AddPage(cpanel, name)

		self.ConfigWidgets = [raisebox, x_box, y_box, width]

		sizer.Add(notebook, 1, wx.EXPAND)

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		if evt != None:
			evt.Skip()

		if not hasattr(self, 'ConfigWidgets'):
			return

		raisebox, x_box, y_box, width = self.ConfigWidgets
		raisebox.SetStringSelection(self.config['raise'])

		x_box.SetValue(self.config['position'][0])
		y_box.SetValue(self.config['position'][1])
		width.SetValue(self.config['size'][0])

	def OnConfigDisplayX(self, evt):
		self.SetPosition(wx.Point(evt.GetInt(), -1))
		self.ConfigUpdate()

	def OnConfigDisplayY(self, evt):
		self.SetPosition(wx.Point(-1, evt.GetInt()))
		self.ConfigUpdate()

	def OnConfigDisplayWidth(self, evt):
		self.SetSize(wx.Size(evt.GetInt(), -1))
		self.ConfigUpdate()

	def OnConfigDisplayMove(self, evt):
		self.ConfigUpdate()

	def OnConfigRaise(self, evt):
		self.config['raise'] = evt.GetString()

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

	def OnConnect(self, evt):
		self.application.gui.Show(self.application.gui.connectto)

	def OnConfig(self, evt):
		self.application.ConfigDisplay()

	def OnProgramExit(self, evt):
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

	def UpdateEOT(self):
		self.application.network.Call(self.application.network.EOTUpdate)

