
from wxPython.wx import *

ID_MENU = 10042
ID_OPEN = 10043
ID_REVERT = 10046
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

import sys

# Shows messages from the game system to the player.
class winMain(wxFrame):
	def __init__(self, parent, ID, title=None, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE, message_list=[]):
		wxFrame.__init__(self, None, ID, 'TP: Thousand Parsecs', pos, size, style)

		self.parent = parent
		print parent

		item0 = wxMenuBar()

		item1 = wxMenu() # wxMENU_TEAROFF )

		item1.Append( ID_OPEN,   "Connect to Game\tCtrl-O", "Connect to a diffrent Game" )
		#EVT_MENU(self, ID_OPEN, parent.app.connect)
		item1.AppendSeparator()
		item1.Append( ID_REVERT, "Revert Game", "Forget non-saved changes" )
		item1.AppendSeparator()
		item1.Append( ID_EXIT, "Exit", "Exit" )
		EVT_MENU(self, ID_EXIT, self.OnProgramExit)
		item0.Append( item1, "File" )

		item3 = wxMenu()
		item3.Append( ID_STAT_EAAG, "Empire at a Glance", "" )
		item3.AppendSeparator()
		item3.Append( ID_STAT_SYSTEM, "Systems", "" )
		item3.Append( ID_STAT_PLANET, "Planets", "" )
		item3.Append( ID_STAT_FLEET, "Fleets", "" )
		item3.AppendSeparator()
		item3.Append( ID_STAT_BATTLE, "Battles", "" )
		item0.Append( item3, "Statistics" )

		item4 = wxMenu()
		item4.Append(  ID_WIN_STARMAP,  "TP: Starmap", "", TRUE )
		#EVT_MENU(self, ID_WIN_STARMAP,   self.changeWin)
		item4.Append(  ID_WIN_MESSAGES, "TP: Messages", "", TRUE )
		#EVT_MENU(self, ID_WIN_MESSAGES,  self.changeWin)
		item4.Append(  ID_WIN_SYSTEM,   "TP: Current System", "", TRUE )
		#EVT_MENU(self, ID_WIN_SYSTEM,    self.changeWin)
		item4.Append(  ID_WIN_ORDERS,   "TP: Orders", "", TRUE )
		#EVT_MENU(self, ID_WIN_ORDERS,    self.changeWin)
		item4.AppendSeparator()
		item4.Append(  ID_WIN_TECH, "Tech Browser", "", TRUE)
		#EVT_MENU(self, ID_WIN_TECH,  self.changeWin)
		item4.Append(  ID_WIN_HELP, "Help", "", TRUE)
		#EVT_MENU(self, ID_WIN_HELP,  self.changeWin)
		item0.Append( item4, "Windows" )

		item5 = wxMenu()
		item0.Append( item5, "Help" )
		
		self.SetMenuBar(item0)
		self.CreateStatusBar(1, wxST_SIZEGRIP)

		EVT_CLOSE(self, self.OnProgramExit)

	def OnProgramExit(self, evt):
		self.parent.Exit()
	
