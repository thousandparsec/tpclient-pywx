"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBase
from utils import *

defaultServers = ["mithro.dyndns.org", "code-bear.dyndns.org", "llnz.dyndns.org", "127.0.0.1:6923"]

ID_OK = 10043
ID_CANCEL = 10044

class winConnect(winMainBase):
	title = _("Connect")
	
	def __init__(self, application):
		winMainBase.__init__(self, application)

		panel = wx.Panel(self, -1)

		# The title
		text_top = wx.StaticText( panel, -1, _("Connect to a Thousand Parsec Server"), wx.DefaultPosition, wx.DefaultSize, 0 )
		text_top.SetFont( wx.Font( 16, wx.ROMAN, wx.NORMAL, wx.BOLD ) )

		# The fill in text areas
		sizer_top = wx.BoxSizer( wx.HORIZONTAL )
		sizer_top.Add( text_top, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		text_host = wx.StaticText( panel, -1, _("Host"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.host = wx.ComboBox( panel, -1, "", wx.DefaultPosition, wx.Size(200,-1), defaultServers, wx.CB_DROPDOWN )

		text_username = wx.StaticText( panel, -1, _("Username"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.username = wx.ComboBox( panel, -1, "", wx.DefaultPosition, wx.Size(200,-1), [""], wx.CB_DROPDOWN )

		text_password = wx.StaticText( panel, -1, _("Password"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.password = wx.TextCtrl( panel, -1, "", wx.DefaultPosition, wx.Size(200,-1), wx.TE_PASSWORD )

		grid = wx.FlexGridSizer( 0, 2, 10, 10 )
		grid.Add( text_host, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		grid.Add( self.host, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		grid.Add( text_username, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		grid.Add( self.username, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		grid.Add( text_password, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		grid.Add( self.password, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		# The buttons
		button_ok = wx.Button( panel, ID_OK, _("OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
		button_cancel = wx.Button( panel, ID_CANCEL, _("Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
		button_ok.SetDefault()

		buttons = wx.BoxSizer( wx.HORIZONTAL )
		buttons.Add( button_ok, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		buttons.Add( button_cancel, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		# The main sizer
		sizer = wx.BoxSizer( wx.VERTICAL )
		sizer.Add( sizer_top, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		sizer.Add( grid, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		sizer.Add( buttons, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		# Join the panel and the base sizer
		panel.SetAutoLayout( True )
		panel.SetSizer( sizer )
		sizer.Fit( panel )
		sizer.SetSizeHints( self )
		
		self.CenterOnScreen()

		# Hook up the events
		self.Bind(wx.EVT_BUTTON, self.OnOkay,   button_ok)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, button_cancel)
		self.Bind(wx.EVT_CLOSE,  self.OnExit)

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnExit(self, evt):
		self.application.exit()
			
	def OnOkay(self, evt):
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

		self.application.network.Call(self.application.network.ConnectTo, host, port, username, password)

