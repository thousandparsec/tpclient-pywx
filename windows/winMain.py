
from wxPython.wx import *

ID_NEW_GAME = 10039
ID_NEW_RACE = 10040
ID_NEW = 10041
ID_MENU = 10042
ID_OPEN = 10043
ID_SAVE = 10044
ID_CLOSE = 10045
ID_REVERT = 10046
ID_LOADTURN = 10047
ID_GENTURN = 10048
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

		item0 = wxMenuBar()

		item1 = wxMenu() # wxMENU_TEAROFF )

		item2 = wxMenu()
		item2.Append( ID_NEW_GAME, "Game", "Start a new Game" )
		EVT_MENU(self, ID_NEW_GAME, self.gameNew)
		item2.Append( ID_NEW_RACE, "Race", "Start a new Race" )
		EVT_MENU(self, ID_NEW_RACE, None)
		item1.AppendMenu( ID_NEW, "New", item2 )

		item1.AppendSeparator()
		item1.Append( ID_OPEN,   "Open Game\tCtrl-O", "Open a diffrent Game" )
		item1.Append( ID_SAVE,   "Save Game\tCtrl-S", "Save this Game" )
		item1.Append( ID_CLOSE,  "Close Game\tCtrl-C", "Close this Game" )
		item1.AppendSeparator()
		item1.Append( ID_REVERT, "Revert Game", "Forget non-saved changes" )
		item1.AppendSeparator()
		item1.Append( ID_LOADTURN, "Load Turn File\tCtrl-L", "Load a turn file" )
		item1.Append( ID_GENTURN,  "Generate Turn File\tCtrl-T", "Generate a turn file" )
		item1.AppendSeparator()
		item1.Append( ID_EXIT, "Exit", "Exit" )
		EVT_MENU(self, ID_EXIT, self.programExit)
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

	def gameNew(self, evt):
		if self.parent.game != None:
			# Warn the user that creating a new game will stop the current one
			okay = wxMessageDialog(self,
								   "Creating a new game will erase the current game, do you want to continue?",
								   "New Game",
								   wxYES_NO)
			
			if okay.ShowModal() == wxID_NO:
				okay.Destory()
				return
			
			okay.Destroy()
			
		dlg = wxDirDialog(self, "Choose a place for the new game", ".", 0)

		if dlg.ShowModal() == wxID_OK:
			path = dlg.GetPath()
			self.parent.newgame(path)
		
		dlg.Destroy()

	def gameLoad(self, evt):
		dlg = wxDirDialog(self, "Choose a new game", ".", 0)

	def gameSave(self, evt):
		self.parent.savegame()

	def gameClose(self, evt):
		pass

	def gameRevert(self, evt):
		pass

	def programExit(self, evt):
		sys.exit(0)
	
