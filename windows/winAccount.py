"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string
import os

# wxPython Imports
import wx
import wx.gizmos

try:
        from extra.GIFAnimationCtrl import GIFAnimationCtrl
except ImportError:
        from wx.animate import GIFAnimationCtrl

from tp.netlib import constants as features

# Local Imports
from winBase import winMainBase
from utils import *

class winAccount(winMainBase):
	title = _("Account")

	def __init__(self, application):
		winMainBase.__init__(self, application)
		panel = wx.Panel(self, -1)

		# The title
		text_top = wx.StaticText( panel, -1, _("Create new Account"), style=wx.TE_CENTRE)
		text_top.SetFont( wx.Font( 16, wx.ROMAN, wx.NORMAL, wx.BOLD ) )

		# The fill in text areas
		sizer_top = wx.BoxSizer( wx.HORIZONTAL )
		sizer_top.Add( text_top, 1, wx.EXPAND, 5 )

		# Server
		sizer_host = wx.BoxSizer( wx.HORIZONTAL )

		text_host = wx.StaticText( panel, -1, _("Server"), style=wx.TE_RIGHT )
		self.host = wx.TextCtrl( panel, -1, "" )

		# Throbber to display when waiting for connection to server
		self.throbber = GIFAnimationCtrl( panel, -1)
		import os
		print os.getcwd()
		self.throbber.LoadFile(os.path.join("graphics", "throbber.gif"))
		self.throbber.Hide()

		# Button to connect to the server
		self.button_connect = wx.Button( panel, -1, "Check" )
		self.button_connect.SetToolTip( wx.ToolTip("Check the server supports creating accounts.") )
		self.button_connect.SetSize(self.throbber.GetBestSize())

		sizer_host.Add(self.host,     1, wx.EXPAND)
		sizer_host.Add(self.button_connect,  0, 0)
		sizer_host.Add(self.throbber, 0, 0)
		self.sizer_host = sizer_host

		# Username
		text_username = wx.StaticText( panel, -1, _("Username"), style=wx.TE_RIGHT )
		self.username = wx.TextCtrl( panel, -1, "" )

		# Password
		text_password1 = wx.StaticText( panel, -1, _("Password"), style=wx.TE_RIGHT )
		self.password1 = wx.TextCtrl( panel, -1, "", style=wx.TE_PASSWORD )
		text_password2 = wx.StaticText( panel, -1, _(""), style=wx.TE_RIGHT )
		self.password2 = wx.TextCtrl( panel, -1, "", style=wx.TE_PASSWORD )
		self.password2.SetToolTip( wx.ToolTip("Retype the password.") )

		text_email = wx.StaticText( panel, -1, _("Email"), style=wx.TE_RIGHT )
		self.email = wx.TextCtrl( panel, -1, "" )

		FLAGS = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.EXPAND
		grid = wx.FlexGridSizer( 0, 2, 5, 5 )
		grid.AddGrowableCol(1)
		grid.Add( text_host,      1, FLAGS )
		grid.Add( sizer_host,     5, FLAGS )
		grid.Add( text_username,  1, FLAGS )
		grid.Add( self.username,  5, FLAGS )
		grid.Add( text_password1, 1, FLAGS )
		grid.Add( self.password1, 5, FLAGS )
		grid.Add( text_password2, 1, FLAGS )
		grid.Add( self.password2, 5, FLAGS )
		grid.Add( text_email,     1, FLAGS )
		grid.Add( self.email,     5, FLAGS )

		# Buttons
		self.button_ok     = wx.Button(panel, wx.ID_OK)
		self.button_cancel = wx.Button(panel, wx.ID_CANCEL)
		self.button_cancel.SetDefault()

		buttons = wx.BoxSizer( wx.HORIZONTAL )
		buttons.Add( self.button_ok, 0, wx.ALIGN_CENTRE)
		buttons.Add( self.button_cancel, 0, wx.ALIGN_CENTRE)

		# The main sizer
		sizer = wx.BoxSizer( wx.VERTICAL )
		sizer.Add( sizer_top, 0, wx.ALIGN_CENTRE|wx.EXPAND, 5 )
		sizer.Add( grid,      1, wx.ALIGN_CENTRE|wx.EXPAND, 5 )
		sizer.Add( buttons,   0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		# Join the panel and the base sizer
		panel.SetAutoLayout( True )
		panel.SetSizer( sizer )
		sizer.Fit( panel )
		sizer.SetSizeHints( self )

		# Put the windows
		self.SetSize(wx.Size(400, -1))
		self.CenterOnScreen()

		# Hook up the events
		self.Bind(wx.EVT_BUTTON,   self.OnCheck,  self.button_connect)
		self.Bind(wx.EVT_BUTTON,   self.OnOkay,   self.button_ok)
		self.Bind(wx.EVT_BUTTON,   self.OnCancel, self.button_cancel)

	def Show(self, a=True):
		if a:
			self.State("start")

			url = self.application.gui.servers.URL.GetValue()
			g = url.rfind('/')
			url, game = url[:g], url[g+1:]

			self.host.SetValue(url)
		winMainBase.Show(self, a)

	def State(self, mode):
		if mode == "start":
			# Enable the host entry box
			self.host.Enable()

			# Show and enable the connect button
			self.button_connect.Show()
			self.button_connect.Enable()
			
			# Stop and hide the throbber
			self.throbber.Stop()
			self.throbber.Hide()

			# Disable the okay button
			self.button_cancel.Enable()
			self.button_ok.Disable()

			# Disable the entries	
			self.username.Disable()
			self.password1.Disable()
			self.password2.Disable()
			self.email.Disable()

			# Re-layout everything
			self.sizer_host.Layout()

		if mode == "connecting":
			# Stop the entry to host 
			self.host.Disable()

			# Hide the connect button
			self.button_connect.Hide()
			self.button_connect.Disable()

			# Show and start the throbber
			self.throbber.Show()
			self.throbber.Play()

			# Disable the okay button
			self.button_cancel.Enable()
			self.button_ok.Disable()

			# Disable the entries	
			self.username.Disable()
			self.password1.Disable()
			self.password2.Disable()
			self.email.Disable()

			self.sizer_host.Layout()

		if mode == "details":
			# Stop the entry to host
			self.host.Disable()

			# Show the connect button but disabled
			self.button_connect.Show()
			self.button_connect.Disable()

			# Stop and hide the throbber
			self.throbber.Stop()
			self.throbber.Hide()

			# Enable the okay button
			self.button_cancel.Enable()
			self.button_ok.Enable()
		
			# Enable the entries	
			self.username.Enable()
			self.password1.Enable()
			self.password2.Enable()
			self.email.Enable()

			self.sizer_host.Layout()

		if mode == "saving":
			# Stop the entry to host
			self.host.Disable()

			# Show the connect button but disabled
			self.button_connect.Hide()
			self.button_connect.Enable()

			# Stop and hide the throbber
			self.throbber.Show()
			self.throbber.Play()

			# Enable the okay button
			self.button_ok.Disable()
			self.button_cancel.Disable()
		
			# Enable the entries	
			self.username.Disable()
			self.password1.Disable()
			self.password2.Disable()
			self.email.Disable()

			self.sizer_host.Layout()
			
	def OnCheck(self, evt):
		self.State("connecting")
		self.application.network.Call(self.application.network.Connect, self.host.GetValue(), 
				debug=self.application.gui.connectto.config['debug'])

	def OnNetworkConnect(self, evt):
		if features.FEATURE_ACCOUNT_REGISTER in evt.args[0]:
			self.State("details")
		else:
			self.OnNetworkFailure("This server does not support account creation.")

	def OnNetworkAccount(self, evt):
		self.application.gui.Show(self.application.gui.connectto)
		dlg = wx.MessageDialog(self.application.gui.current, str(evt), _("Account Created"), wx.OK|wx.ICON_INFORMATION)
		dlg.ShowModal()

	def OnNetworkFailure(self, evt):
		dlg = wx.MessageDialog(self.application.gui.current, str(evt), _("Network Error"), wx.OK|wx.ICON_ERROR)
		dlg.ShowModal()

		self.State("start")

	def OnOkay(self, evt):
		username = self.username.GetValue().strip().split('@')
		if len(username) == 2:
			username, game = username
		else:
			username = username[0]
			game = ""

		password1 = self.password1.GetValue().strip()
		password2 = self.password2.GetValue().strip()
		email = self.email.GetValue().strip()

		# Check the values are sensible
		if username == "" or password1 == "" or password2 == "" or email == "":
			dlg = wx.MessageDialog(self.application.gui.current, "All fields are required.", _("Fields Required"), wx.OK|wx.ICON_ERROR)
			dlg.ShowModal()
			return
		if password1 != password2:
			dlg = wx.MessageDialog(self.application.gui.current, "Password fields do not match.", _("Fields Required"), wx.OK|wx.ICON_ERROR)
			dlg.ShowModal()
			return

		url = self.host.GetValue()		
		p = url.find('://')+3

		fullurl = "%s%s:%s@%s/%s" % (url[:p], username, password1, url[p:], game)
		print fullurl
		self.application.gui.connectto.ShowURL(fullurl)

		#self.application.network.Call(self.application.network.ConnectTo, host, username, password, debug=self.config['debug'])
		self.application.network.Call(self.application.network.NewAccount, username, password1, email)

	def OnCancel(self, evt):
		self.application.gui.Show(self.application.gui.connectto)

	# Config Functions -----------------------------------------------------------------------------
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		if config is None:
			config = {}

		try:
			if not isinstance(config['debug'], bool):
				raise ValueError('Config-%s: a debug value of %s is not valid' % (self, config['debug']))
		except (ValueError, KeyError), e:
			config['debug'] = False

		return config

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		self.ConfigUpdate()

		self.ConfigLoad(self.config)
		return self.config

	def ConfigLoad(self, config):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		return

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		return

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		return

	def ConfigDisplayUpdate(self, evt):
		"""\
		Updates the config details using external sources.
		"""
		return
