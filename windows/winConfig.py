"""\
This module contains the config window.
"""

from winBase import winBase
from config import load_data
from config import save_data

from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

ID_TEXT=-1
ID_NOTEBOOK = 10045

# Shows messages from the game system to the player.
class winConfig(winBase):
	title = "Config"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style|wxTAB_TRAVERSAL)

		self.application = application

		panel = wxPanel(self, -1)
		panel.SetConstraints(LayoutAnchors(self, 1, 1, 1, 1))
		self.obj = {}

		item0 = wxBoxSizer( wxHORIZONTAL )
	
		item2 = wxNotebook( panel, ID_NOTEBOOK, wxDefaultPosition, wxDefaultSize, 0 )
		item1 = wxNotebookSizer( item2 )

		item3 = panelConfigStartup(application, self, item2)
		item2.AddPage( item3, "Startup" )

		item4 = panelConfigWindows(application, self, item2)
		item2.AddPage( item4, "Windows" )

		item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

		panel.SetAutoLayout( true )
		panel.SetSizer( item1 )
		
		item1.Fit( panel )
		item1.SetSizeHints( panel )

		self.Fit()


ID_SPLASH = 10046
ID_AUTOCONNECT = 10047
ID_TIPS = 10048
ID_AUTOSERVER = 10049
ID_AUTOUSERNAME = 10050
ID_AUTOPASSWORD = 10051
ID_SAVE = 10052
ID_REVERT = 10053

class panelConfigStartup(wxPanel):
	def __init__(self, application, frame, parent):
		wxPanel.__init__(self, parent, -1)

		self.frame = frame
		self.application = application
		
		self.obj = {}

		item0 = wxBoxSizer( wxVERTICAL )
	
		item1 = wxBoxSizer( wxHORIZONTAL )
	
		item2 = wxBoxSizer( wxVERTICAL )
	
		item3 = wxCheckBox( self, ID_SPLASH, "Show Splash Screen", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item3, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['splash'] = item3
	
		item4 = wxCheckBox( self, ID_AUTOCONNECT, "Connect on Startup", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item4, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['auto_connect'] = item4

		item5 = wxCheckBox( self, ID_TIPS, "Show Welcome Tips", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item5, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['tips'] = item5

		item1.AddSizer( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

		item6 = wxGridSizer( 0, 2, 0, 0 )
	
		item7 = wxStaticText( self, ID_TEXT, "Startup Server", wxDefaultPosition, wxDefaultSize, 0 )
		item6.AddWindow( item7, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
	
		item8 = wxComboBox( self, ID_AUTOSERVER, "", wxDefaultPosition, wxSize(100,-1), [], wxCB_DROPDOWN )
		item8.SetToolTip( wxToolTip("The server to connect to on autoconnect.") )
		item8.Enable(false)
		item6.AddWindow( item8, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['auto_server'] = item8

		item9 = wxStaticText( self, ID_TEXT, "Username", wxDefaultPosition, wxDefaultSize, 0 )
		item6.AddWindow( item9, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
	
		item10 = wxComboBox( self, ID_AUTOUSERNAME, "", wxDefaultPosition, wxSize(100,-1), [], wxCB_DROPDOWN )
		item10.SetToolTip( wxToolTip("The username to use on autoconnect.") )
		item10.Enable(false)
		item6.AddWindow( item10, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['auto_username'] = item10

		item11 = wxStaticText( self, ID_TEXT, "Password", wxDefaultPosition, wxDefaultSize, 0 )
		item6.AddWindow( item11, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		item12 = wxTextCtrl( self, ID_AUTOPASSWORD, "", wxDefaultPosition, wxSize(80,-1), wxTE_PASSWORD )
		item12.Enable(false)
		item6.AddWindow( item12, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['auto_password'] = item12

		item1.AddSizer( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

		item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

		item13 = wxBoxSizer( wxHORIZONTAL )
	
		item14 = wxButton( self, ID_SAVE, "Save", wxDefaultPosition, wxDefaultSize, 0 )
		item14.SetDefault()
		item13.AddWindow( item14, 0, wxALIGN_CENTRE|wxALL, 5 )
		EVT_BUTTON(self, ID_SAVE, self.OnSave)

		item15 = wxButton( self, ID_REVERT, "Revert", wxDefaultPosition, wxDefaultSize, 0 )
		item13.AddWindow( item15, 0, wxALIGN_CENTRE|wxALL, 5 )
		EVT_BUTTON(self, ID_SAVE, self.OnRevert)

		item0.AddSizer( item13, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		
		self.SetAutoLayout( true )
		self.SetSizer( item0 )
		
		item0.Fit( self )
		item0.SetSizeHints( self )
	
	def OnSave(self, evt):
		pass
	
	def OnRevert(self, evt):
		pass

ID_MESSAGE	= 10054
ID_ORDER	= 10055
ID_STARMAP	= 10056
ID_SYSTEM	= 10057
ID_RAISE	= 10058
ID_RADIOBOX = 10059
ID_XPOS		= 10060
ID_YPOS		= 10061
ID_WIDTH	= 10062
ID_HEIGHT	= 10063

class panelConfigWindows(wxPanel):
	def __init__(self, application, frame, parent):
		wxPanel.__init__(self, parent, -1)
	
		self.frame = frame
		self.application = application

		self.obj = {}
		
		item0 = wxBoxSizer( wxVERTICAL )
	
		item1 = wxBoxSizer( wxHORIZONTAL )
	
		item3 = wxStaticBox( self, -1, "Show Windows" )
		item2 = wxStaticBoxSizer( item3, wxVERTICAL )
		
		item4 = wxCheckBox( self, ID_MESSAGE, "Message", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item4, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['show_message'] = item4
		EVT_CHECKBOX(self, ID_MESSAGE, self.OnShowMessage)

		item5 = wxCheckBox( self, ID_ORDER, "Order", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item5, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['show_order'] = item5
		EVT_CHECKBOX(self, ID_ORDER, self.OnShowOrder)

		item6 = wxCheckBox( self, ID_STARMAP, "StarMap", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item6, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['show_starmap'] = item6
		EVT_CHECKBOX(self, ID_STARMAP, self.OnShowStarMap)

		item7 = wxCheckBox( self, ID_SYSTEM, "System", wxDefaultPosition, wxDefaultSize, 0 )
		item2.AddWindow( item7, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		self.obj['show_system'] = item7
		EVT_CHECKBOX(self, ID_SYSTEM, self.OnShowSystem)

		item1.AddSizer( item2, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

		if wxPlatform == '__WXMSW__':
			item8 = wxRadioBox( self, ID_RAISE, "Raise", wxDefaultPosition, wxDefaultSize, 
					["Individual", "All on Main"] , 1, wxRA_SPECIFY_COLS )
		else:
			item8 = wxRadioBox( self, ID_RAISE, "Raise", wxDefaultPosition, wxDefaultSize, 
					["Individual", "All on Main", "All on All"] , 1, wxRA_SPECIFY_COLS )
			
		item8.SetToolTip( wxToolTip("Choose a method for raising the windows.") )
		item1.AddWindow( item8, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )
		self.obj['raise'] = item8
		EVT_RADIOBOX(self, ID_RAISE, self.OnRaiseSelection)

		item9 = wxRadioBox( self, ID_RADIOBOX, "Window", wxDefaultPosition, wxDefaultSize, 
				["Main", "Message","Order","StarMap","System"] , 1, wxRA_SPECIFY_COLS )
		item1.AddWindow( item9, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )
		self.obj['window'] = item9
		EVT_RADIOBOX(self, ID_RADIOBOX, self.OnWindowSelection)

		item11 = wxStaticBox( self, -1, "Attributes" )
		item10 = wxStaticBoxSizer( item11, wxVERTICAL )
		
		item12 = wxFlexGridSizer( 0, 2, 0, 0 )
		item12.AddGrowableCol( 1 )
		
		item13 = wxStaticText( self, ID_TEXT, "X Position", wxDefaultPosition, wxDefaultSize, 0 )
		item12.AddWindow( item13, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		item14 = wxSpinCtrl( self, ID_XPOS, "0", wxDefaultPosition, wxSize(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item14, 0, wxALIGN_CENTRE|wxALL, 5 )
		self.obj['xpos'] = item14
		EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		item15 = wxStaticText( self, ID_TEXT, "Y Position", wxDefaultPosition, wxDefaultSize, 0 )
		item12.AddWindow( item15, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		item16 = wxSpinCtrl( self, ID_YPOS, "0", wxDefaultPosition, wxSize(50,-1), 0, 0, 1000, 0 )
		item12.AddWindow( item16, 0, wxALIGN_CENTRE|wxALL, 5 )
		self.obj['ypos'] = item16
		EVT_SPINCTRL(self, ID_YPOS, self.OnYPos)

		item17 = wxStaticText( self, ID_TEXT, "Width", wxDefaultPosition, wxDefaultSize, 0 )
		item12.AddWindow( item17, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		item18 = wxSpinCtrl( self, ID_WIDTH, "0", wxDefaultPosition, wxSize(50,-1), 0, 0, 100, 0 )
		item12.AddWindow( item18, 0, wxALIGN_CENTRE|wxALL, 5 )
		self.obj['width'] = item18
		EVT_SPINCTRL(self, ID_WIDTH, self.OnWidth)

		item19 = wxStaticText( self, ID_TEXT, "Height", wxDefaultPosition, wxDefaultSize, 0 )
		item12.AddWindow( item19, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		item20 = wxSpinCtrl( self, ID_HEIGHT, "0", wxDefaultPosition, wxSize(50,-1), 0, 0, 100, 0 )
		item12.AddWindow( item20, 0, wxALIGN_CENTRE|wxALL, 5 )
		self.obj['height'] = item20
		EVT_SPINCTRL(self, ID_HEIGHT, self.OnHeight)

		item10.AddSizer( item12, 0, wxALIGN_CENTRE|wxALL, 5 )

		item1.AddSizer( item10, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

		item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

		item21 = wxBoxSizer( wxHORIZONTAL )
		
		item22 = wxButton( self, ID_SAVE, "Save", wxDefaultPosition, wxDefaultSize, 0 )
		item21.AddWindow( item22, 0, wxALIGN_CENTRE|wxALL, 5 )
		EVT_BUTTON(self, ID_SAVE, self.OnSave)

		item23 = wxButton( self, ID_REVERT, "Revert", wxDefaultPosition, wxDefaultSize, 0 )
		item21.AddWindow( item23, 0, wxALIGN_CENTRE|wxALL, 5 )
		EVT_BUTTON(self, ID_REVERT, self.OnRevert)

		item0.AddSizer( item21, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		self.SetAutoLayout( true )
		self.SetSizer( item0 )
		
		item0.Fit( self )
		item0.SetSizeHints( self )

	def OnShowMessage(self, evt):
		self.application.windows.config.message.show = not evt.Checked()
		self.application.windows.message.Show(not evt.Checked())

	def OnShowOrder(self, evt):
		self.application.windows.config.order.show = not evt.Checked()
		self.application.windows.order.Show(not evt.Checked())
		
	def OnShowStarMap(self, evt):
		self.application.windows.config.starmap.show = not evt.Checked()
		self.application.windows.starmap.Show(not evt.Checked())
		
	def OnShowSystem(self, evt):
		self.application.windows.config.system.show = not evt.Checked()
		self.application.windows.system.Show(not evt.Checked())
		
	def OnXPos(self, evt):
		self.current_window.SetPosition((self.obj['xpos'].GetValue(), -1))

	def OnYPos(self, evt):
		self.current_window.SetPosition((-1, self.obj['ypos'].GetValue()))

	def OnWidth(self, evt):
		self.current_window.SetSize((self.obj['width'].GetValue(), -1))

	def OnHeight(self, evt):
		self.current_window.SetSize((-1, self.obj['height'].GetValue()))

	def OnWindowSelection(self, evt):
		window = self.obj['window'].GetStringSelection()
		self.current_window = getattr(self.application.windows, window.lower())
		pos = self.current_window.GetPosition()
		size = self.current_window.GetSize()

		self.obj['xpos'].SetValue(pos[0])
		self.obj['ypos'].SetValue(pos[1])
		self.obj['width'].SetValue(size[0])
		self.obj['height'].SetValue(size[1])

	def OnRaiseSelection(self, evt):
		style = self.obj['raise'].GetStringSelection()
		self.application.windows.config.raise_ = style

	def OnSave(self, evt):
		self.application.windows.ConfigSave()
		self.frame.Show(FALSE)

	def OnRevert(self, evt):
		self.application.windows.ConfigLoad()
		self.application.windows.ConfigActivate()
		self.frame.Show(FALSE)

