"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

from utils import *

defaultServers = ["127.0.0.1:6923"]

ID_OK = 10043
ID_CANCEL = 10044

from lang.en.winConnect import *

# Shows messages from the game system to the player.
class winConnect(wxFrame):
	def __init__(self, application, ID, \
			title=None, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE, message_list=[]):
		wxFrame.__init__(self, None, ID, 'TP: Connect', pos, size, style|wxTAB_TRAVERSAL)

		self.application = application

		panel = wxPanel(self, -1)

		# The title
		text_top = wxStaticText( panel, -1, "Connect to a Thousand Parsec Server", wxDefaultPosition, wxDefaultSize, 0 )
		text_top.SetFont( wxFont( 16, wxROMAN, wxNORMAL, wxBOLD ) )

		# The fill in text areas
		sizer_top = wxBoxSizer( wxHORIZONTAL )
		sizer_top.AddWindow( text_top, 0, wxALIGN_CENTRE|wxALL, 5 )

		text_host = wxStaticText( panel, -1, "Host", wxDefaultPosition, wxDefaultSize, 0 )
		self.host = wxComboBox( panel, -1, "", wxDefaultPosition, wxSize(200,-1), defaultServers, wxCB_DROPDOWN )

		text_username = wxStaticText( panel, -1, "Username", wxDefaultPosition, wxDefaultSize, 0 )
		self.username = wxComboBox( panel, -1, "", wxDefaultPosition, wxSize(200,-1), [""], wxCB_DROPDOWN )

		text_password = wxStaticText( panel, -1, "Password", wxDefaultPosition, wxDefaultSize, 0 )
		self.password = wxTextCtrl( panel, -1, "", wxDefaultPosition, wxSize(200,-1), wxTE_PASSWORD )

		grid = wxFlexGridSizer( 0, 2, 0, 0 )
		grid.AddWindow( text_host, 0, wxALIGN_CENTRE|wxALL, 5 )
		grid.AddWindow( self.host, 0, wxALIGN_CENTRE|wxALL, 5 )
		grid.AddWindow( text_username, 0, wxALIGN_CENTRE|wxALL, 5 )
		grid.AddWindow( self.username, 0, wxALIGN_CENTRE|wxALL, 5 )
		grid.AddWindow( text_password, 0, wxALIGN_CENTRE|wxALL, 5 )
		grid.AddWindow( self.password, 0, wxALIGN_CENTRE|wxALL, 5 )

		# The buttons
		button_ok = wxButton( panel, ID_OK, "OK", wxDefaultPosition, wxDefaultSize, 0 )
		button_cancel = wxButton( panel, ID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )

		buttons = wxBoxSizer( wxHORIZONTAL )
		buttons.AddWindow( button_ok, 0, wxALIGN_CENTRE|wxALL, 5 )
		buttons.AddWindow( button_cancel, 0, wxALIGN_CENTRE|wxALL, 5 )

		# The main sizer
		sizer = wxBoxSizer( wxVERTICAL )
		sizer.AddSizer( sizer_top, 0, wxALIGN_CENTRE|wxALL, 5 )
		sizer.AddSizer( grid, 0, wxALIGN_CENTRE|wxALL, 5 )
		sizer.AddSizer( buttons, 0, wxALIGN_CENTRE|wxALL, 5 )

		# Join the panel and the base sizer
		panel.SetAutoLayout( true )
		panel.SetSizer( sizer )
		sizer.Fit( panel )
		sizer.SetSizeHints( self )

		# Hook up the events
		EVT_BUTTON(self, ID_OK, self.OnOkay)
		EVT_BUTTON(self, ID_CANCEL, self.OnCancel)
		EVT_CLOSE(self, self.OnExit)

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnExit(self, evt):
		application = self.application
		application.Exit()
			
	def OnOkay(self, evt):
		application = self.application

		# Pull out the values
		host = self.host.GetValue()
		username = self.username.GetValue()
		password = self.password.GetValue()

		if host == "" or username == "":
			return

		temp = string.split(host, ":", 1)
		if len(temp) == 1:
			host = host
			port = 6923
		else:
			host, port = temp
			port = int(port)

		progress = wxProgressDialog(TITLE_PROGRESS, TEXT_PROGRESS, 5, self, wxPD_APP_MODAL | wxPD_AUTO_HIDE)

		print host, port, username, password

		dlg = None
		try:
			application.connection.setup(host=host, port=port, debug=False)
			progress.Update(1)
			
			print "Connect...",
			if application.connection.connect():
				progress.Update(3)

				print "Login...",
				if not application.connection.login(username, password):
					print "Login Failed"
					dlg = wxMessageDialog(self, TEXT_LOGIN, TITLE_LOGIN, wxOK | wxICON_INFORMATION)
			else:
				print "Connect Failed"
				dlg = wxMessageDialog(self, TEXT_CONNECT, TITLE_CONNECT, wxOK | wxICON_INFORMATION)

		except:
			print "Exception Failed"
			do_traceback()
			dlg = wxMessageDialog(self, TEXT_CONNECT, TITLE_CONNECT, wxOK | wxICON_INFORMATION)

		progress.Update(5)
		if dlg == None:
			print "Success"
			
			progress = wxProgressDialog(TITLE_DOWNLOAD, TEXT_DOWNLOAD, 100, self, \
				wxPD_APP_MODAL | wxPD_AUTO_HIDE | wxPD_ELAPSED_TIME | wxPD_REMAINING_TIME)
		
			application.cache = {}
		
			objects = application.connection.get_objects(0)
			while len(objects) > 0:
				object = objects.pop(0)
				application.cache[object.id] = object
			
				if len(object.contains) > 0:
					objects += application.connection.get_objects(object.contains)
		
				progress.Update(len(application.cache.keys()))
		
			progress.Update(100)
		
			self.Hide()
			application.windows.Show()
		else:
			dlg.ShowModal()
			dlg.Destroy()
		return
