"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

from network import protocol
from network.events import *
from utils import *

from extra.wxProgressDialog import wxProgressDialog
from extra.evtmgr import eventManager

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
		wxFrame.__init__(self, None, ID, 'TP: Connect', pos, size, style|wxTAB_TRAVERSAL)


		panel = wxPanel(self, -1)

		self.parent = parent
		self.obj = {}

		item0 = wxBoxSizer( wxVERTICAL )
	
		item1 = wxBoxSizer( wxHORIZONTAL )
	
		item2 = wxStaticText( panel, ID_TEXT, "Connect to a Thousand Parsec Server", wxDefaultPosition, wxDefaultSize, 0 )
		item2.SetFont( wxFont( 16, wxROMAN, wxNORMAL, wxBOLD ) )
		item1.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

		item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

		item3 = wxFlexGridSizer( 0, 2, 0, 0 )
		
		item4 = wxStaticText( panel, ID_TEXT, "Host", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

		item5 = wxComboBox( panel, ID_HOST, "", wxDefaultPosition, wxSize(200,-1), 
			defaultServers, wxCB_DROPDOWN )
		item3.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.obj['host'] = item5

		item6 = wxStaticText( panel, ID_TEXT, "Username", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

		item7 = wxComboBox( panel, ID_USERNAME, "", wxDefaultPosition, wxSize(200,-1),
			[""], wxCB_DROPDOWN )
		item3.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.obj['username'] = item7

		item8 = wxStaticText( panel, ID_TEXT, "Password", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item8, 0, wxALIGN_CENTRE|wxALL, 5 )

		item9 = wxTextCtrl( panel, ID_PASSWORD, "", wxDefaultPosition, wxSize(200,-1), wxTE_PASSWORD )
		item3.AddWindow( item9, 0, wxALIGN_CENTRE|wxALL, 5 )

		self.obj['password'] = item9

		item0.AddSizer( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

		item10 = wxBoxSizer( wxHORIZONTAL )

		item3.AddSizer( item10, 0, wxALIGN_CENTRE|wxALL, 5 )

		item11 = wxBoxSizer( wxHORIZONTAL )

		item12 = wxButton( panel, ID_OK, "OK", wxDefaultPosition, wxDefaultSize, 0 )
		item11.AddWindow( item12, 0, wxALIGN_CENTRE|wxALL, 5 )

		item13 = wxButton( panel, ID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
		item11.AddWindow( item13, 0, wxALIGN_CENTRE|wxALL, 5 )

		item3.AddSizer( item11, 0, wxALIGN_CENTRE|wxALL, 5 )

		panel.SetAutoLayout( true )
		panel.SetSizer( item0 )
		
		item0.Fit( panel )
		item0.SetSizeHints( self )

		EVT_BUTTON(self, ID_OK, self.OnOkay)
		EVT_BUTTON(self, ID_CANCEL, self.OnCancel)
		EVT_CLOSE(self, self.OnExit)

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnExit(self, evt):
		# Check if the server is connected
		self.Show(FALSE)
		if self.parent.logined:
			self.parent.windows.Show()
		else:
			# Exit then
			self.parent.Exit()
			
	def OnOkay(self, evt):
		host = self.obj['host'].GetValue()
		username = self.obj['username'].GetValue()
		password = self.obj['password'].GetValue()

		if host != "" and username != "":

			try:
				temp = string.split(host, ":", 1)

				if len(temp) == 1:
					host = host
					port = 6923
				else:
					host, port = temp
					port = int(port)

				self.parent.app.network.win_connect(self)
				eventManager.Register(self.OnConnection, EVT_NETWORK_PACKET, self)
				
				self.progress = wxProgressDialog("TP: Connecting to Server",
												"Thousand Parsec is now attempting to connect to the specified server",
												5,
												self,
												wxPD_APP_MODAL | wxPD_AUTO_HIDE)
												
				self.parent.ConnectTo(host, port, username, password)
				self.progress.Update(1)
				
			except:
				# Pop-up a dialog telling us why it didn't succed.
				do_traceback()

	def OnConnection(self, evt):
		try:
			eventManager.DeregisterListener(self.OnConnection)

			if evt != None and isinstance(evt.value, protocol.Ok):
				print "Connect Worked!"
				eventManager.Register(self.OnLogin, EVT_NETWORK_PACKET, self)
				self.progress.Update(2)
			else:
				print "Connect Failed!"
				# Oh no! we didn't connect!
				self.progress.Update(5)
				#self.progress.Destroy()

				dlg = wxMessageDialog(self, 'The connection failed, this could be because,\n' +
											'the server could be busy,\n' +
											'the server doesn\'t exist.\n' +
											'Please try again later.',
											'TP: Connection Failed',
				   						wxOK | wxICON_INFORMATION)
				dlg.ShowModal()
				dlg.Destroy()

		finally:
			print "Connection Finishing"
			print evt
			if evt:
				evt.next()

	def OnLogin(self, evt):
		try:
			self.progress.Update(3)
		
			if isinstance(evt.value, protocol.Ok):
				print "Login Worked!"
				eventManager.DeregisterListener(self.OnLogin)
				self.parent.app.network.win_disconnect(self)
			
				self.progress.Update(4)
			
				self.OnExit(None)
			
				self.progress.Update(5)

			elif isinstance(evt.value, protocol.Fail):
				# Show a message box
				print "Login Failed!"
				self.progress.Update(5)
				
				dlg = wxMessageDialog(self, 'Failed to connect, this could be because,\n' +
											'the server could be busy,\n' +
											'your username and password could be incorrect.\n' +
											'Please try again.',
											'TP: Bad Username or Password',
				   						wxOK | wxICON_INFORMATION)

				dlg.ShowModal()
				dlg.Destroy()
				
				# Disable the host selection box
				self.obj['host'].Enable(FALSE)

		finally:
			print "Login Finishing"
			print evt
			if evt:
				evt.next()
