
from wxPython.wx import *
from utils import *

defaultServers = ["127.0.0.1:6923","code-bear.dyndns.org:6923","mithro.dyndns.org:6923"] 

ID_TEXT = 10039
ID_HOST = 10040
ID_USERNAME = 10041
ID_PASSWORD = 10042
ID_OK = 10043
ID_CANCEL = 10044

# Shows messages from the game system to the player.
class winConnect(wxFrame):
	def __init__(self, parent, ID, title=None, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE, message_list=[]):
		wxFrame.__init__(self, None, ID, 'TP: Connect', pos, size, style)

		self.parent = parent
		self.obj = {}

		item0 = wxBoxSizer( wxVERTICAL )
	
		item1 = wxBoxSizer( wxHORIZONTAL )
	
		item2 = wxStaticText( self, ID_TEXT, "Connect to a Thousand Parsec Server", wxDefaultPosition, wxDefaultSize, 0 )
		item2.SetFont( wxFont( 16, wxROMAN, wxNORMAL, wxBOLD ) )
		item1.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

		item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

		item3 = wxFlexGridSizer( 0, 2, 0, 0 )
		
		item4 = wxStaticText( self, ID_TEXT, "Host", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

		item5 = wxComboBox( self, ID_HOST, "", wxDefaultPosition, wxSize(200,-1), 
			defaultServers, wxCB_DROPDOWN )
		item3.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.obj['host'] = item5

		item6 = wxStaticText( self, ID_TEXT, "Username", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

		item7 = wxComboBox( self, ID_USERNAME, "", wxDefaultPosition, wxSize(200,-1), [], wxCB_DROPDOWN )
		item3.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.obj['username'] = item7

		item8 = wxStaticText( self, ID_TEXT, "Password", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item8, 0, wxALIGN_CENTRE|wxALL, 5 )

		item9 = wxTextCtrl( self, ID_PASSWORD, "", wxDefaultPosition, wxSize(200,-1), wxTE_PASSWORD )
		item3.AddWindow( item9, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.obj['password'] = item9

		item0.AddSizer( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

		item10 = wxBoxSizer( wxHORIZONTAL )

		item3.AddSizer( item10, 0, wxALIGN_CENTRE|wxALL, 5 )

		item11 = wxBoxSizer( wxHORIZONTAL )

		item12 = wxButton( self, ID_OK, "OK", wxDefaultPosition, wxDefaultSize, 0 )
		item11.AddWindow( item12, 0, wxALIGN_CENTRE|wxALL, 5 )

		item13 = wxButton( self, ID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
		item11.AddWindow( item13, 0, wxALIGN_CENTRE|wxALL, 5 )

		item3.AddSizer( item11, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.SetAutoLayout( true ) 
		self.SetSizer( item0 )
		#item0.Fit( self )
		item0.SetSizeHints( self )

		EVT_BUTTON(self, ID_OK, self.OnOkay)
		EVT_BUTTON(self, ID_CANCEL, self.OnCancel)
		EVT_CLOSE(self, self.OnExit)

	def OnOkay(self, event):
		# Check the host and username arn't blank
		
		#self.parent.connected = TRUE

		host = self.obj['host'].GetValue()
		username = self.obj['username'].GetValue()
		password = self.obj['password'].GetValue()

		if host != "" and username != "":

			try:
				self.parent.Connect(host, username, password)
			
				# We connected successfully
				self.OnExit(event)
			except:
				# Pop-up a dialog telling us why it didn't succed.
				do_traceback()
	
	def OnCancel(self, event):
		self.OnExit(event)

	def OnExit(self, event):
		# Check if the server is connected
		self.Show(FALSE)
		if self.parent.connected:
			self.parent.windows.show()
		else:
			# Exit then
			self.parent.Exit()
