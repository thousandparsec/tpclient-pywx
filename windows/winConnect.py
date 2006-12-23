"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string
import re

# wxPython Imports
import wx
import wx.gizmos

# Local Imports
from winBase import winMainBaseXRC
from xrc.winConnect import winConnectBase
from utils import *

def url2bits(line):
	urlspliter = r'(.*?://)?(((.*):|(.*@))(.*@)?)?(.*?)(/.*?)?$'

	groups = re.compile(urlspliter, re.M).search(line).groups()
	
	proto = groups[0]
	username = groups[2]
	if not username is None:
		if username[-1] in '@:':
			username = username[:-1]

	server = groups[6]
	password = groups[5]
	if not password is None:
		if password[-1] is '@':
			password = password[:-1]

	game = groups[7]
	if not game is None:
		if game[0] is '/':
			game = game[1:]
		if len(game) == 0:
			game = None

	if proto is None:
		one = server
	else:
		one = "%s%s" % (proto, server)

	return (one, username, game, password)

class winConnect(winConnectBase, winMainBaseXRC):
	title = _("Connect")

	def Post(*args):
		pass

	def __init__(self, application):
		winConnectBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)	

		self.Bind(wx.EVT_CLOSE,  self.OnExit)

	def OnExit(self, evt):
		self.application.Exit()

	def Show(self, show=True):
		if not show:
			return self.Hide()

		self.Panel.Layout()
		size = self.Panel.GetBestSize()
		self.SetClientSize(size)
		
		self.CenterOnScreen(wx.BOTH)
		return winMainBaseXRC.Show(self)
	
	def OnGameShow(self, evt):
		if self.GameShow.GetValue():
			# Split the part after the @ into the game box
			username = self.Username.GetValue().split('@')
			if len(username) == 2:
				username, game = username
			else:
				username = username[0]
				game = ""

			self.Username.SetValue(username)
			self.Game.SetValue(game)

			# Show the game boxes
			self.GameTitle.Show()
			self.Game.Show()
		else:
			game = self.Game.GetValue()
			username = self.Username.GetValue()
			if len(game) > 0:
				username = "%s@%s" % (username, game)

			self.Username.SetValue(username)

			# Hide the game boxes
			self.GameTitle.Hide()
			self.Game.Hide()

		self.Panel.Layout()
		size = self.Panel.GetBestSize()
		self.SetClientSize(size)

	def OnOkay(self, evt):
		server = self.Server.GetValue()
		username = self.Username.GetValue()
		if self.Game.IsShown():
			username = "%s@%s" % (username, self.Game.GetVale())

		password = self.Password.GetValue()
		if server == "" or username == "":
			return

		self.application.network.Call(self.application.network.ConnectTo, server, username, password, debug=self.config['debug'])

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnConfig(self, evt):
		self.application.ConfigDisplay()

	def OnFind(self, evt):
		self.application.gui.Show(self.application.gui.account)

	def ShowURL(self, url):
		# Split the URL out into username, password, etc
		# <proto>://<username>:<password>@<server>/<game>
		# server = <proto>://<server>/
		# username = <username>@<game>
		# password = <server>
		server, username, game, password = url2bits(url)
		if server is None:
			return
		self.Server.SetValue(server)

		if username is None:
			username = ""
		if self.Game.IsShown():
			if game is None:
				game = ""
			self.Game.SetValue(game)
		else:
			if not game is None:
				username = "%s@%s" % (username, game)

		self.Username.SetValue(username)
		if password is None:
			password = ""
		self.Password.SetValue(password)

	# Config Functions -----------------------------------------------------------------------------
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		if config is None:
			config = {}

		try:
			if not isinstance(config['servers'], list):
				raise ValueError('Config-%s: a servers value of %s is not valid' % (self, config['servers']))

			for server in config['servers']:
				if not isinstance(server, (str, unicode)):
					config['servers'].remove(server)

			if len(config['servers']) <= 0:
				raise ValueError('Config-%s: the servers list was empty' % (self,))

		except (ValueError, KeyError), e:
			config['servers'] = ["demo1.thousandparsec.net", "demo2.thousandparsec.net", "127.0.0.1"]

		try:
			if not isinstance(config['username'], (unicode, str)):
				raise ValueError('Config-%s: a username value of %s is not valid' % (self, config['username']))
		except (ValueError, KeyError), e:
			config['username'] = "guest@tp"

		try:
			if not isinstance(config['password'], (unicode, str)):
				raise ValueError('Config-%s: a password value of %s is not valid' % (self, config['password']))
		except (ValueError, KeyError), e:
			config['password'] = "guest"

		try:
			if not isinstance(config['auto'], bool):
				raise ValueError('Config-%s: a auto value of %s is not valid' % (self, config['auto']))
		except (ValueError, KeyError), e:
			config['auto'] = False

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
		self.config = config
		self.ConfigDefault(config)

		self.Server.Clear()
		self.Server.AppendItems(self.config['servers'])
		self.Server.SetValue(self.config['servers'][0])
		
		self.Username.SetValue(self.config['username'])
		self.Password.SetValue(self.config['password'])

		self.ConfigDisplayUpdate(None)

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		if hasattr(self, 'ConfigWidgets'):
			servers, username, password, auto, debug = self.ConfigWidgets

			self.config['servers']  = servers.GetStrings()
			self.config['username'] = username.GetValue()
			self.config['password'] = password.GetValue()

			self.config['auto']  = auto.GetValue()
			self.config['debug'] = debug.GetValue()

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		SIZER_FLAGS = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL
		TEXT_FLAGS = wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL
	
		# List of Servers to Choose From
		servers = wx.gizmos.EditableListBox(panel, -1, "Server List")
		servers.SetStrings([""])

		def OnConfigDisplayServers(evt, f=self.OnConfigDisplayServers, servers=servers):
			return f(evt, servers)
		panel.Bind(wx.EVT_LISTBOX, OnConfigDisplayServers, servers)

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
		Updates the config details using external sources.
		"""
		if evt != None:
			evt.Skip()

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

	def OnConfigDisplayDebug(self, evt):
		self.config['debug'] = evt.Checked()
	
	def OnConfigDisplayAuto(self, evt):
		self.config['auto'] = evt.Checked()

	def OnConfigDisplayUsername(self, evt):
		self.config['username'] = evt.GetString()
		
	def OnConfigDisplayPassword(self, evt):
		self.config['password'] = evt.GetString()
