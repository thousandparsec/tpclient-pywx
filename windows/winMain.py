"""\
This module contains the main menu window.
"""

# Python imports
import time

# wxPython imports
import wx

# Local imports
from winBase import *
from utils import *

ID_MENU = 10042
ID_OPEN = 10043
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
ID_WIN_TECH = 11004
ID_WIN_HELP = 1105

ID_HELP = 10057

def create_menu(source, target):

	# File Menu
	file = wx.Menu()
	file.Append( ID_OPEN, "Connect to Game\tCtrl-O", "Connect to a diffrent Game" )
	file.AppendSeparator()
	file.Append( ID_CONFIG, "Config", "Configure the Client" )
	file.AppendSeparator()
	file.Append( ID_EXIT, "Exit", "Exit" )

	# Statistics Menu
	stat = wx.Menu()
	stat.Append( ID_STAT_EAAG, "Empire at a Glance", "" )
	stat.AppendSeparator()
	stat.Append( ID_STAT_SYSTEM, "Systems", "" )
	stat.Append( ID_STAT_PLANET, "Planets", "" )
	stat.Append( ID_STAT_FLEET,  "Fleets", "" )
	stat.AppendSeparator()
	stat.Append( ID_STAT_BATTLE, "Battles", "" )

	# Windows Menu
	win = wx.Menu()
	win.Append(  ID_WIN_MESSAGES, "Hide Messages", "", True )
	win.Append(  ID_WIN_ORDERS,   "Hide Orders", "", True )
	win.Append(  ID_WIN_STARMAP,  "Hide Starmap", "", True )
	win.Append(  ID_WIN_SYSTEM,   "Hide System", "", True )
	win.AppendSeparator()
	win.Append(  ID_WIN_TECH, "Tech Browser", "", True)
	win.Append(  ID_WIN_HELP, "Help", "", True)

	help = wx.Menu()
	
	bar = wx.MenuBar()
	bar.Append( file, "File" )
	bar.Append( stat, "Statistics" )
	bar.Append( win,  "Windows" )
	bar.Append( help, "Help" )

	wx.EVT_MENU(source, ID_OPEN,	target.OnConnect)
	wx.EVT_MENU(source, ID_CONFIG,	target.OnConfig)
	wx.EVT_MENU(source, ID_EXIT,	target.OnProgramExit)

	wx.EVT_MENU(source, ID_WIN_MESSAGES,	target.OnMessages)
#	wx.EVT_MENU(source, ID_WIN_ORDERS,		target.OnOrders)
	wx.EVT_MENU(source, ID_WIN_STARMAP,		target.OnStarMap)
	wx.EVT_MENU(source, ID_WIN_SYSTEM,		target.OnSystem)
#	wx.EVT_MENU(source, ID_WIN_TECH,		target.changeWin)
#	wx.EVT_MENU(source, ID_WIN_HELP,		target.OnHelp)
	return bar

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
		left = self.endtime - time.time()
		if left > 0:
			self.SetStatusText(time.strftime("EOT: %I:%M:%S", time.localtime(left)), 1)
		else:
			self.SetStatusText("EOT: Unknown", 1)

	def SetEndTime(self, endtime):
		self.endtime = endtime

class winMain(winMainBase):
	title = "Thousand Parsec"
	
	def __init__(self, application, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winMainBase.__init__(self, application, None, pos, size, style)

		self.menubar = create_menu(self, self)
		self.SetMenuBar(self.menubar)

		self.statusbar = TimeStatusBar(self)
		self.SetStatusBar(self.statusbar)

	def OnConnect(self, evt):
		self.application.windows.Hide()
		self.application.windows.connect.Show(True)

	def OnConfig(self, evt):
		self.application.windows.winconfig.Show(True)

	def OnStarMap(self, evt):
		self.application.windows.starmap.Show(not evt.Checked())

	def OnMessages(self, evt):
		self.application.windows.message.Show(not evt.Checked())

	def OnSystem(self, evt):
		self.application.windows.system.Show(not evt.Checked())

	def OnProgramExit(self, evt):
		self.application.Exit()
