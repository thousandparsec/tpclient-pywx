"""\
This module contains the main menu window.
"""

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

class winMain(winMainBase):
	title = "Thousand Parsec"
	
	def __init__(self, application, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winMainBase.__init__(self, application, None, pos, size, style)

		# File Menu
		file = wx.Menu()
		file.Append( ID_OPEN, "Connect to Game\tCtrl-O", "Connect to a diffrent Game" )
		file.AppendSeparator()
		file.Append( ID_CONFIG, "Config", "Configure the Client" )
		file.AppendSeparator()
		file.Append( ID_EXIT, "Exit", "Exit" )

		wx.EVT_MENU(self, ID_OPEN, self.OnConnect)
		wx.EVT_MENU(self, ID_CONFIG, self.OnConfig)
		wx.EVT_MENU(self, ID_EXIT, self.OnProgramExit)

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

		wx.EVT_MENU(self, ID_WIN_MESSAGES,  self.OnMessages)
#		wx.EVT_MENU(self, ID_WIN_ORDERS,    self.OnOrders)
		wx.EVT_MENU(self, ID_WIN_STARMAP,   self.OnStarMap)
		wx.EVT_MENU(self, ID_WIN_SYSTEM,    self.OnSystem)
#		wx.EVT_MENU(self, ID_WIN_TECH,  self.changeWin)
#		wx.EVT_MENU(self, ID_WIN_HELP,  self.OnHelp)

		help = wx.Menu()
		
		bar = wx.MenuBar()
		bar.Append( file, "File" )
		bar.Append( stat, "Statistics" )
		bar.Append( win,  "Windows" )
		bar.Append( help, "Help" )
		
		self.SetMenuBar(bar)
		self.CreateStatusBar(1, wx.ST_SIZEGRIP)

		if wx.Platform == "__WXMAC__":
			for value in self.application.windows.__dict__.values():
				if hasattr(value, "SetMenuBar"):
					value.SetMenuBar(bar)

			self.Show(False)

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
