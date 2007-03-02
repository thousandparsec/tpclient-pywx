"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string
import re
import pprint

# wxPython Imports
import wx
import wx.gizmos

# Local Imports
from winBase import winMainBaseXRC
from xrc.winConnect import winConnectBase
from xrc.configConnect import configConnectBase
from utils import *

from tp.netlib.client import url2bits

class usernameMixIn:
	def __init__(self):
		self.Username.Bind(wx.EVT_CHAR, self.OnUsernameChar)
		self.Game.Bind(wx.EVT_CHAR, self.OnGameChar)

	def OnGameShow(self, evt):
		if self.GameShow.GetValue():
			self.SetUsername(self.Username.GetValue())
			# Show the game boxes
			self.GameTitle.Show()
			self.Game.Show()
	
		else:
			self.SetUsername("%s@%s" % (self.Username.GetValue(), self.Game.GetValue()))
			# Hide the game boxes
			self.GameTitle.Hide()
			self.Game.Hide()

		self.Panel.Layout()
		size = self.Panel.GetBestSize()
		self.SetClientSize(size)

	def OnUsernameChar(self, evt):
		if isinstance(evt.KeyCode, (int,long)):
			key = evt.KeyCode
		else: 
			key = evt.KeyCode()
		if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
			evt.Skip()
			return
		if chr(key) in string.letters+string.digits:
			evt.Skip()
			return

		if not self.GameShow.GetValue():
			if chr(key) == '@':
				evt.Skip()
				return
		return

	def OnGameChar(self, evt):
		if isinstance(evt.KeyCode, (int,long)):
			key = evt.KeyCode
		else: 
			key = evt.KeyCode()
		if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
			evt.Skip()
			return
		if chr(key) in string.letters+string.digits:
			evt.Skip()
			return
		return

	def GetUsername(self):
		game = self.Game.GetValue()
		username = self.Username.GetValue()
		if len(game) > 0:
			return "%s@%s" % (username, game)
		else:
			return username

	def GetUsernameGame(self):
		game = self.Game.GetValue()
		username = self.Username.GetValue()
		if len(game) > 0:
			return (username, game)
		else:
			return (username, "")

	def SetUsername(self, value):
		# Split the part after the @ into the game box
		username = value.split('@')
		if len(username) == 2:
			username, game = username
		else:
			username = username[0]
			game = ""

		if self.GameShow.GetValue() or len(game) == 0:
			self.Username.SetValue(username)
		else:
			self.Username.SetValue("%s@%s" % (username, game))
		self.Game.SetValue(game)

class configConnect(configConnectBase, usernameMixIn):
	def __init__(self, *args, **kw):
		configConnectBase.__init__(self, *args, **kw)
		usernameMixIn.__init__(self)
		self.Panel = self

		self.GameShow.MoveAfterInTabOrder(self.Password)
		self.Servers.SetMinSize(wx.Size(300, -1))
		self.Layout()

		# Use better Art Graphics for the EditableList
		custom = {
			"Del":	wx.ART_DELETE,
			"New":	wx.ART_NEW,
			"Up":	wx.ART_GO_UP,
			"Down":	wx.ART_GO_DOWN,
			"Edit":	wx.ART_REPORT_VIEW,}

		for name, id in custom.items():
			bmp = wx.ArtProvider_GetBitmap(id, wx.ART_TOOLBAR, (16,16))

			if not bmp.Ok():
				continue

			button = getattr(self.Servers, "Get%sButton" % name)()
			button.SetBitmapLabel(bmp)
			button.SetBitmapDisabled(bmp)

	def EnableDetails(self, label):
		self.ServerDetails.SetLabel("Login for " + label)
		self.Username.Enable()
		self.Game.Enable()
		self.GameShow.Enable()
		self.Password.Enable()
		self.AutoConnect.Enable()

	def DisableDetails(self):
		#self.ServerDetails.SetLabel(" ")
		self.Username.Disable()
		self.Username.SetValue("")
		self.Game.Disable()
		self.Game.SetValue("")
		self.GameShow.Disable()
		self.Password.Disable()
		self.Password.SetValue("")
		self.AutoConnect.Disable()

USERNAME=0
PASSWORD=1
AUTOCONNECT=2

# FIXME: The config should use proper URLs, currently you can't have more then one login to a server (and a server could have multiple games).

class winConnect(winConnectBase, winMainBaseXRC, usernameMixIn):
	title = _("Connect")

	def Post(*args):
		pass

	def __init__(self, application):
		winConnectBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)	
		usernameMixIn.__init__(self)

		self.attemps = 0

		self.GameShow.MoveAfterInTabOrder(self.Okay)

		self.Bind(wx.EVT_CLOSE, self.OnExit)
		self.Bind(wx.EVT_COMBOBOX, self.OnChangeServer, self.Server)

	def OnChangeServer(self, evt):
		server = self.Server.GetValue()
		if server in self.config['servers']:
			self.SetUsername(self.config['details'][server][0])
			self.Password.SetValue(self.config['details'][server][1])

	def OnExit(self, evt):
		self.application.Exit()

	def SetFromConfig(self, server):
		if not server in self.config['servers'] or not self.config['details'].has_key(server):
			raise RuntimeError("Server is not in the config settings!")

		self.Server.SetValue(server)
		self.SetUsername(self.config['details'][server][USERNAME])
		self.Password.SetValue(self.config['details'][server][PASSWORD])
		return self.config['details'][server][AUTOCONNECT]

	def Show(self, show=True):
		if not show:
			return self.Hide()

		self.Panel.Layout()
		size = self.Panel.GetBestSize()
		self.SetClientSize(size)
		
		self.CenterOnScreen(wx.BOTH)

		autoconnect = False
		# If the server value is empty we should populate with a server item
		if len(self.Server.GetValue()) == 0:
			# Check that no other server is also set to autoconnect
			for key in self.config['details'].keys():
				if not self.config['details'][key][AUTOCONNECT]: 
					continue
				self.SetFromConfig(key)
				autoconnect = True

			# Is it still empty?
			if len(self.Server.GetValue()) == 0 and len(self.config['servers']) > 0:
				autoconnect = self.SetFromConfig(self.config['servers'][0])

		# FIXME: Gross hack
		if self.attemps == 0 and autoconnect:
			wx.CallAfter(self.OnOkay, None)
		self.attemps += 1

		return winMainBaseXRC.Show(self)

	def OnOkay(self, evt):
		server = self.Server.GetValue()
		username = self.GetUsername()

		password = self.Password.GetValue()
		if server == "" or username == "":
			return

		# Check if this server exists in the config
		print self.config['servers']
		if server in self.config['servers']:
			# Check the values are the same
			(oldusername, oldpassword, oldautoconnect) = self.config['details'][server]

			if oldusername != username:
				print "Username doesn't match.."
			if oldpassword != password:
				print "Password doesn't match.."
				msg = """\
It appears you are using a different password for 
this account, would you like to update the saved 
information?
"""
				dlg = wx.MessageDialog(self, msg, _("Update Password?"), wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
				if dlg.ShowModal() == wx.ID_OK:
					# Update the password
					self.config['details'][server][PASSWORD] = password
					# Save the config now
					self.application.ConfigSave()

		else:
			# Popup a dialog asking if we want to add the account
			msg = """\
Would you like to save this account's details?
"""
			dlg = wx.MessageDialog(self, msg, _("Add Account?"), wx.OK|wx.CANCEL|wx.ICON_INFORMATION)

			rst = dlg.ShowModal()
			if rst == wx.ID_OK:
				# Add the account.
				self.ConfigPanel.Servers.SetStrings([server,] + self.ConfigPanel.Servers.GetStrings())
				self.config['details'][server] = (username, password, False)

				# Save the config now
				self.application.ConfigSave()

		self.application.network.Call(self.application.network.ConnectTo, server, username, password, debug=self.config['debug'])

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnConfig(self, evt):
		self.application.ConfigDisplay()

	def OnFind(self, evt):
		self.application.gui.Show(self.application.gui.servers)

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
		if not game is None:
			username = "%s@%s" % (username, game)
		self.SetUsername(username)
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
			if not isinstance(config['details'], dict):
				raise ValueError('Config-%s: a details value of %s is not valid' % (self, config['details']))

			for server, details in config['details'].items():
				if not isinstance(details, list) or len(details) != 3 or \
						not isinstance(details[0], (str, unicode)) or \
						not isinstance(details[1], (str, unicode)) or \
						not isinstance(details[2], bool):
					print "deleteing", server, details
					del config[server]

		except (ValueError, KeyError), e:
			print e
			config['details'] = {}
		for server in config['servers']:
			if server not in config['details']:
				config['details'][server] = ["guest@tp", "guest", False]

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

		self.Server.SetValue("")
		self.ConfigDisplayUpdate(None)

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		self.config['debug'] = self.ConfigPanel.Debug.GetValue()

		self.config['servers'] = self.ConfigPanel.Servers.GetStrings()
		for removed in self.config['details'].keys():
			if not removed in self.config['servers']:
				del self.config['details'][removed]

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		self.ConfigPanel = configConnect(panel)

		self.ConfigPanel.Servers.Bind(wx.EVT_LIST_ITEM_FOCUSED,   self.OnConfigSelectServer)
		self.ConfigPanel.Servers.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnConfigSelectServer)
		self.ConfigPanel.Username.Bind(wx.EVT_KILL_FOCUS, self.OnConfigUsername)
		self.ConfigPanel.Game.Bind(wx.EVT_KILL_FOCUS, self.OnConfigUsername)
		self.ConfigPanel.Password.Bind(wx.EVT_KILL_FOCUS, self.OnConfigPassword)
		self.ConfigPanel.AutoConnect.Bind(wx.EVT_CHECKBOX, self.OnConfigAutoConnect)
		self.ConfigPanel.Debug.Bind(wx.EVT_CHECKBOX, self.OnConfigDebug)

		sizer.Add( self.ConfigPanel, 1, wx.EXPAND, 5 )

	def ConfigDisplayUpdate(self, evt):
		"""\
		Updates the config details using external sources.
		"""
		if evt != None:
			evt.Skip()

		self.ConfigPanel.Debug.SetValue(self.config['debug'])
		self.ConfigPanel.Servers.SetStrings(self.config['servers'])

	def OnConfigSelectServer(self, evt):
		server = evt.GetText()

		if len(server) > 0:
			self.ConfigPanel.EnableDetails(server)

			if not self.config['details'].has_key(server):
				self.config['details'][server] = [self.ConfigPanel.GetUsername(), self.ConfigPanel.Password.GetValue(), False]

			self.ConfigPanel.SetUsername(self.config['details'][server][0])
			self.ConfigPanel.Password.SetValue(self.config['details'][server][1])
			self.ConfigPanel.AutoConnect.SetValue(self.config['details'][server][2])
		else:
			self.ConfigPanel.DisableDetails()
		evt.Skip()

	def OnConfigUsername(self, evt):
		server = self.ConfigPanel.ServerDetails.GetLabel()[len(_("Login for ")):]
		self.config['details'][server][0] = self.ConfigPanel.GetUsername()
		pprint.pprint(self.config)

	def OnConfigPassword(self, evt):
		server = self.ConfigPanel.ServerDetails.GetLabel()[len(_("Login for ")):]
		self.config['details'][server][1] = self.ConfigPanel.Password.GetValue()
		pprint.pprint(self.config)

	def OnConfigAutoConnect(self, evt):
		server = self.ConfigPanel.ServerDetails.GetLabel()[len(_("Login for ")):]

		if evt.Checked():
			# Check that no other server is also set to autoconnect
			for key, details in self.config['details'].items():
				if not details[2]: 
					continue
				msg = """
The client is already set to autoconnect to %s.

Would you instead like to autoconnect to %s.
""" % (key, server)
				dlg = wx.MessageDialog(self.ConfigPanel, msg, _("Autoconnect to?"), wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
				if dlg.ShowModal() == wx.ID_OK:
					details[2] = False
					break

		print "OnConfigAutoConnect", server, evt.Checked()
		self.config['details'][server][2] = evt.Checked()
		pprint.pprint(self.config)

	def OnConfigDebug(self, evt):
		self.config['debug'] = evt.Checked()
