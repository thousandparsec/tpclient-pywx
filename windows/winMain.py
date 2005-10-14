"""\
This module contains the main menu window.
"""

# Python imports
import time
import math
import os.path

# wxPython imports
import wx

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

ID_WIN_STARMAP = 11000
ID_WIN_MESSAGES = 11001
ID_WIN_SYSTEM = 11002
ID_WIN_ORDERS = 11003
ID_WIN_DESIGN = 11004
ID_WIN_TIPS = 11005
ID_WIN_INFO = 11006
ID_WIN_HELP = 1105

ID_HELP = 10057

class TimeStatusBar(wx.StatusBar):
	def __init__(self, parent):
		wx.StatusBar.__init__(self, parent, -1)

		self.SetFieldsCount(2)
		self.SetStatusWidths([-3, -1])

		self.SetStatusText("", 0)
		self.endtime = 0

		self.timer = wx.PyTimer(self.Notify)
		self.timer.Start(1000)
		self.Notify()

	def Notify(self):
		sih = 60*60
		sim = 60
	
		left = self.endtime - time.time()
		if left > 0:
			hours = math.floor(left / sih)
			mins = math.floor((left - hours * sih) / sim)
			secs = math.floor((left - hours * sih - mins * sim))
			self.SetStatusText("EOT: %02i:%02i:%02i" % (hours, mins, secs), 1)
		else:
			self.SetStatusText("EOT: Unknown", 1)

	def SetEndTime(self, endtime):
		self.endtime = endtime

class winMain(winMainBase):
	title = _("Main Windows")

	def __init__(self, application):
		winMainBase.__init__(self, application)

		print "main", self.config

		self.SetMenuBar(self.Menu(self))

		self.statusbar = TimeStatusBar(self)
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

		if wx.Platform != "__WXMSW__":
			self.SetClientSize(wx.Size(-1,0))

	def Menu(self, source):
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
		stat.Append( ID_STAT_FLEET,  _("Fleets"), _("") )
		stat.AppendSeparator()
		stat.Append( ID_STAT_BATTLE, _("Battles"), _("") )
	
		# Windows Menu
		win = wx.Menu()
		win.Append(  ID_WIN_INFO,     _("Hide Information"), _(""), True )
		win.Append(  ID_WIN_MESSAGES, _("Hide Messages"), _(""), True )
		win.Append(  ID_WIN_ORDERS,   _("Hide Orders"), _(""), True )
		win.Append(  ID_WIN_STARMAP,  _("Hide StarMap"), _(""), True )
		win.Append(  ID_WIN_SYSTEM,   _("Hide System"), _(""), True )
		win.AppendSeparator()
		win.Append(  ID_WIN_DESIGN,   _("Hide Design"), _(""), True )
		win.AppendSeparator()
		win.Append(  ID_WIN_TIPS, _("Show Tips"), _(""), True )
		win.Append(  ID_WIN_HELP, _("Help"), _(""), True)
	
		help = wx.Menu()
		
		bar = wx.MenuBar()
		bar.Append( file, _("File") )
		bar.Append( stat, _("Statistics") )
		bar.Append( win,  _("Windows") )
		bar.Append( help, _("&Help") )
	
		wx.EVT_MENU(source, ID_OPEN,	self.OnConnect)
		wx.EVT_MENU(source, ID_UNIV,	self.UpdateCache)
		wx.EVT_MENU(source, wx.ID_PREFERENCES,	self.OnConfig)
		wx.EVT_MENU(source, ID_EXIT,	self.OnProgramExit)
	
		wx.EVT_MENU(source, ID_WIN_INFO,        self.OnInformation)
		wx.EVT_MENU(source, ID_WIN_MESSAGES,	self.OnMessages)
		wx.EVT_MENU(source, ID_WIN_ORDERS,		self.OnOrders)
		wx.EVT_MENU(source, ID_WIN_STARMAP,		self.OnStarMap)
		wx.EVT_MENU(source, ID_WIN_SYSTEM,		self.OnSystem)
		wx.EVT_MENU(source, ID_WIN_DESIGN,		self.OnDesign)
		wx.EVT_MENU(source, ID_WIN_TIPS,		self.ShowTips)
		
#		wx.EVT_MENU(source, ID_WIN_HELP,		self.OnHelp)
		return bar

	def Show(self, show=True):
		# Show this window and it's children - also fixes menus for MacOS
		if not show:
			return self.Hide()
		
		for window in self.children.values():
			# FIXME: This is a bit bad
			if window.config['show']:
				window.Show()

			if wx.Platform == "__WXMAC__":
				value.SetMenuBar(self.current.Menu())

		winMainBase.Show(self)

	# Config Functions -----------------------------------------------------------------------------
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		if config == None:
			config = {}
		
		config['raise'] = 'Individual'
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
		self.config = config
		self.ConfigDefault(config)

		for name, window in self.children.items():
			window.ConfigLoad(config.get(name, {}))
	
		self.ConfigDefault(config)
		self.ConfigDisplayUpdate(None)
	
	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		pass
	
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

		raisebox = wx.RadioBox(cpanel, -1, _("Raise Mode"), choices=options, majorDimension=1, style=wx.RA_SPECIFY_COLS)
		raisebox.SetToolTip( wx.ToolTip(_("Choose a method for raising the windows.")) )
		csizer.Add( raisebox, 1, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		#panel.Bind(wx.EVT_RADIOBOX, self.OnConfigRaise, raisebox)

		cpanel.SetSizer( csizer )	
		cpanel.Layout()

		notebook.AddPage(cpanel, "Menubar")

		for name, window in self.children.items():
			cpanel = wx.Panel(notebook, -1)
			csizer = wx.BoxSizer(wx.HORIZONTAL)

			window.ConfigDisplay(cpanel, csizer)

			cpanel.SetSizer( csizer )	
			notebook.AddPage(cpanel, name)

		self.ConfigWidgets = [raisebox]

		sizer.Add(notebook, 1, wx.EXPAND)

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		if not hasattr(self, 'ConfigWidgets'):
			return
		
		raisebox, = self.ConfigWidgets
		raisebox.SetStringSelection(self.config['raise'])

	# Menu bar options
	##################################################################
	def OnConnect(self, evt):
		self.application.connect()

	def OnConfig(self, evt):
		self.application.ConfigDisplay()
		
	def OnDesign(self, evt):
		self.children[_('Design')].Show(not evt.Checked())

	def OnInformation(self, evt):
		self.children[_('Information')].Show(not evt.Checked())
		
	def OnMessages(self, evt):
		self.children[_('Messages')].Show(not evt.Checked())
		
	def OnOrders(self, evt):
		self.children[_('Windows')].Show(not evt.Checked())
		
	def OnStarMap(self, evt):
		self.children[_('StarMap')].Show(not evt.Checked())

	def OnSystem(self, evt):
		self.children[_('System')].Show(not evt.Checked())

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
		self.application.windows.Hide()
		self.application.CacheUpdate()

