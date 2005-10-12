"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string

# wxPython Imports
import wx
import wx.gizmos

# Local Imports
from winBase import winMainBase
from utils import *

class winConnect(winMainBase):
	title = _("Connect")
	
	def __init__(self, application):
		winMainBase.__init__(self, application)

		panel = wx.Panel(self, -1)

		# Default configuration
		self.config = { \
			"servers": ["mithro.dyndns.org", "code-bear.dyndns.org", "llnz.dyndns.org", "127.0.0.1:6923"],
			"username": "",
			"password": "",
			"auto": False,
			"debug": False }

		# The title
		text_top = wx.StaticText( panel, -1, _("Connect to a Thousand Parsec Server"), wx.DefaultPosition, wx.DefaultSize, 0 )
		text_top.SetFont( wx.Font( 16, wx.ROMAN, wx.NORMAL, wx.BOLD ) )

		# The fill in text areas
		sizer_top = wx.BoxSizer( wx.HORIZONTAL )
		sizer_top.Add( text_top, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		text_host = wx.StaticText( panel, -1, _("Host"))
		self.host = wx.ComboBox( panel, -1, "", wx.DefaultPosition, wx.Size(200,-1), [""], wx.CB_DROPDOWN )

		text_username = wx.StaticText( panel, -1, _("Username"))
		self.username = wx.ComboBox( panel, -1, "", wx.DefaultPosition, wx.Size(200,-1), [""], wx.CB_DROPDOWN )

		text_password = wx.StaticText( panel, -1, _("Password"))
		self.password = wx.TextCtrl( panel, -1, "", wx.DefaultPosition, wx.Size(200,-1), wx.TE_PASSWORD )

		TEXT_FLAGS = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL

		grid = wx.FlexGridSizer( 0, 2, 5, 5 )
		grid.AddGrowableCol(1)
		grid.Add( text_host, 0, TEXT_FLAGS, 5 )
		grid.Add( self.host, 1, wx.GROW, 5 )
		grid.Add( text_username, 0, TEXT_FLAGS, 5 )
		grid.Add( self.username, 1, wx.GROW, 5 )
		grid.Add( text_password, 0, TEXT_FLAGS, 5 )
		grid.Add( self.password, 1, wx.GROW, 5 )

		# The buttons
		button_ok = wx.Button(panel, wx.ID_OK, _("&OK"))
		button_cancel = wx.Button(panel, wx.ID_CANCEL, _("Cancel"))
		button_config = wx.Button(panel, wx.ID_PREFERENCES, _("&Preferences"))
		button_ok.SetDefault()

		buttons = wx.BoxSizer( wx.HORIZONTAL )
		buttons.Add( button_ok, 0, wx.ALIGN_CENTRE)
		buttons.Add( button_cancel, 0, wx.ALIGN_CENTRE)
		buttons.AddSpacer(wx.Size(5, -1))
		buttons.Add( button_config, 0, wx.ALIGN_CENTRE)

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
		self.Bind(wx.EVT_BUTTON, self.OnConfig, button_config)
		self.Bind(wx.EVT_CLOSE,  self.OnExit)

	def OnConfig(self, evt):
		self.application.ConfigDisplay()

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnExit(self, evt):
		self.application.Exit()
			
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

		self.application.network.Call(self.application.network.ConnectTo, host, port, username, password, debug=self.config['debug'])
	
	# Config Functions -----------------------------------------------------------------------------
	def ConfigLoad(self, config):
		self.config = config

		self.host.Clear()
		self.host.AppendItems(self.config['servers'])
		self.host.SetValue(self.config['servers'][0])
		
		self.username.SetValue(self.config['username'])
		self.password.SetValue(self.config['password'])

		self.ConfigDisplayUpdate(None)

	def ConfigUpdate(self):
		pass

	def ConfigDisplay(self, panel, sizer):
		SIZER_FLAGS = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL
		TEXT_FLAGS = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
	
		# List of Servers to Choose From
		servers = wx.gizmos.EditableListBox(panel, -1, "Server List")
		servers.SetStrings([""])

		def OnConfigDisplayServers(evt, f=self.OnConfigDisplayServers, servers=servers):
			return f(evt, servers)
		panel.Bind(wx.EVT_TEXT, OnConfigDisplayServers, servers)

		sizer.Add(servers, 1, SIZER_FLAGS)

		# Username and Password Field
		main = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(main, 1, SIZER_FLAGS, 5)
		
		grid = wx.FlexGridSizer( 0, 2, 1, 5 )
		grid.AddGrowableCol(1)	
		main.Add(grid, 2, SIZER_FLAGS, 5)
	
		# Username Box
		text_username = wx.StaticText( panel, -1, _("Username"))
		grid.Add( text_username, 0, TEXT_FLAGS)
		
		username = wx.TextCtrl( panel, -1, "")
		grid.Add( username, 1, SIZER_FLAGS)
		
		panel.Bind(wx.EVT_TEXT, self.OnConfigDisplayUsername, username)

		# Password Box
		text_password = wx.StaticText( panel, -1, _("Password"))
		grid.Add( text_password, 0, TEXT_FLAGS)
		
		password = wx.TextCtrl( panel, -1, "", style=wx.TE_PASSWORD )
		grid.Add( password, 1, SIZER_FLAGS)

		panel.Bind(wx.EVT_TEXT, self.OnConfigDisplayPassword, password)
		
		# The check boxes
		checks = wx.BoxSizer(wx.HORIZONTAL)
		main.Add(checks, 1, SIZER_FLAGS)
		
		# Autoconnect Checkbox
		auto = wx.CheckBox(panel, -1, _("Autoconnect?"))
		checks.Add(auto, 0, SIZER_FLAGS, 5 )
		panel.Bind(wx.EVT_CHECKBOX, self.OnConfigDisplayAuto, auto)

		# Print debug	
		debug = wx.CheckBox(panel, -1, _("Debug Output?"))
		checks.Add(debug, 0, SIZER_FLAGS, 5 )
		panel.Bind(wx.EVT_CHECKBOX, self.OnConfigDisplayDebug, debug)
	
		# FIXME: This is bad too!
		self.ConfigWidgets = [servers, username, password, auto, debug]
		self.Bind(wx.EVT_ACTIVATE, self.ConfigDisplayUpdate)

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally
		"""
		if not hasattr(self, 'ConfigWidgets'):
			return
		
		servers, username, password, auto, debug = self.ConfigWidgets
		servers.SetStrings(self.config['servers'])
		username.SetValue(self.config['username'])
		password.SetValue(self.config['password'])
		auto.SetValue(self.config['auto'])
		debug.SetValue(self.config['debug'])
	
	def OnConfigDisplayServers(self, evt, servers):
		self.config['servers'] = servers.GetStrings()
		print self.config['servers']

	def OnConfigDisplayDebug(self, evt):
		self.config['debug'] = evt.Checked()
	
	def OnConfigDisplayAuto(self, evt):
		self.config['auto'] = evt.Checked()

	def OnConfigDisplayUsername(self, evt):
		self.config['username'] = evt.GetString()
		
	def OnConfigDisplayPassword(self, evt):
		self.config['password'] = evt.GetString()
