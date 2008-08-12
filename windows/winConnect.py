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
import wx.wizard as wiz

from extra.decorators import freeze_wrapper

# Local Imports
from winBase import winBaseXRC
from xrc.winConnect import winConnectBase
from xrc.configConnect import configConnectBase
from xrc.SinglePlayerWizard import *
from utils import *

from tp.netlib.client import url2bits
from tp.client.SinglePlayer import SinglePlayerGame

# FIXME: The game really isn't part of the username, it's part of the server information
# You could be playing multiple different games on the same server!

class usernameMixIn:
	def __init__(self):
		self.Username.Bind(wx.EVT_CHAR, self.OnUsernameChar)
		self.Game.Bind(wx.EVT_CHAR, self.OnGameChar)

	@freeze_wrapper
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
		username = self.Username.GetValue()
		game     = self.Game.GetValue().strip()
		if self.GameShow.GetValue() and len(game) > 0:
			return "%s@%s" % (username, game)
		else:
			return username

	def GetUsernameGame(self):
		username = self.Username.GetValue()
		game     = self.Game.GetValue().strip()
	
		return (username, game)

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
		self.ServerDetails.SetLabel(_("Login for %s") % (label,))
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

class StartPage(StartPageBase):
	def __init__(self, parent, *args, **kw):
		StartPageBase.__init__(self, parent, *args, **kw)
		if len(parent.game.rulesets) > 0:
			self.ProceedDesc.SetLabel("You appear to have at least one server with rulesets installed on your system.")
			self.ProceedDesc.Wrap(400)
			self.proceed = True
		else:
			self.ProceedDesc.SetLabel("No servers or rulesets were found on your system.")
			self.ProceedDesc.Wrap(400)
			self.proceed = False
	def GetNext(self):
		if self.proceed:
			return self.next
		else:
			return None

class RulesetPage(RulesetPageBase):
	def __init__(self, parent, *args, **kw):
		RulesetPageBase.__init__(self, parent, *args, **kw)
		for ruleset in parent.game.rulesets:
			rs = parent.game.ruleset_info(ruleset)['longname']
			self.Ruleset.Insert(rs, self.Ruleset.GetCount())
		self.Ruleset.SetSelection(0)
		self.OnRuleset(None)

	def GetNext(self):
		# skip server selection if only 1 server supports selected ruleset
		if len(self.parent.game.list_servers_with_ruleset()) == 1:
			self.parent.game.sname = self.parent.game.list_servers_with_ruleset()[0]
			self.next.next.SetPrev(self)
			return self.next.next
		# otherwise, populate the server selection list
		else:
			self.next.servers = self.parent.game.list_servers_with_ruleset()
			self.next.Server.SetItems([])
			for server in self.next.servers:
				ss = self.parent.game.serverlist[server]['longname']
				self.next.Server.Insert(ss, self.next.Server.GetCount())
			self.next.Server.SetSelection(0)
			self.next.OnServer(None)
			self.next.next.SetPrev(self.next)
			return self.next

	def OnRuleset(self, event):
		self.parent.game.rname = self.parent.game.rulesets[self.Ruleset.GetSelection()]
		self.RulesetDesc.SetLabel(self.parent.game.ruleset_info(self.parent.game.rname)['description'])
		self.RulesetDesc.Wrap(400)

class ServerPage(ServerPageBase):
	def OnServer(self, event):
		self.parent.game.sname = self.parent.game.serverlist.keys()[self.Server.GetSelection()]
		self.ServerDesc.SetLabel(self.parent.game.serverlist[self.parent.game.sname]['description'])
		self.ServerDesc.Wrap(400)

class EndPage(EndPageBase):
	pass

class SinglePlayerWizard(SinglePlayerWizardBase):
	def __init__(self, parent, *args, **kw):
		SinglePlayerWizardBase.__init__(self, parent, *args, **kw)

		self.game = SinglePlayerGame()

		self.pages = []

		self.AddPage(StartPage(self))
		self.AddPage(RulesetPage(self))
		self.AddPage(ServerPage(self))
		self.AddPage(EndPage(self))

		self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGED, self.OnPageChanged)
		self.Bind(wx.wizard.EVT_WIZARD_PAGE_CHANGING, self.OnPageChanging)
		self.Bind(wx.wizard.EVT_WIZARD_CANCEL, self.OnCancelWizard)

	def AddPage(self, page):
		i = len(self.pages)
		self.pages.append(page)
		if i > 0:
			self.pages[i].SetPrev(self.pages[i - 1])
			self.pages[i - 1].SetNext(self.pages[i])
		self.GetPageAreaSizer().Add(self.pages[i])


	def Run(self):
		return self.RunWizard(self.pages[0])

	def OnPageChanged(self, event):
		pass

	def OnPageChanging(self, event):
		pass
	
	def OnCancelWizard(self, event):
		pass

USERNAME=0
PASSWORD=1
AUTOCONNECT=2

# FIXME: The config should use proper URLs, currently you can't have more then one login to a server (and a server could have multiple games).

class winConnect(winConnectBase, winBaseXRC, usernameMixIn):
	title = _("Connect")

	def Post(*args):
		pass

	def __init__(self, application):
		winConnectBase.__init__(self, None)
		winBaseXRC.__init__(self, application)	
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

		return winBaseXRC.Show(self)

	def OnOkay(self, evt):
		self.application.StartNetwork()

		server = self.Server.GetValue()
		username = self.GetUsername()

		password = self.Password.GetValue()
		if server == "" or username == "":
			return

		# Check if this server exists in the config
		if server in self.config['servers']:
			# Check the values are the same
			(oldusername, oldpassword, oldautoconnect) = self.config['details'][server]
		else:
			(oldusername, oldpassword, oldautoconnect) = (username, password, False)

		if server not in self.config['servers'] or username != username:
			# Popup a dialog asking if we want to add the account
			msg = _("""\
It appears you havn't access this account before.

Would you like to save this account's details?
""")
			dlg = wx.MessageDialog(self, msg, _("Add Account?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_INFORMATION)

			if dlg.ShowModal() == wx.ID_YES:
				# Add the account.
				if not server in self.ConfigPanel.Servers.GetStrings():
					self.ConfigPanel.Servers.SetStrings([server,] + self.ConfigPanel.Servers.GetStrings())
				self.config['details'][server] = [username, password, False]

				# Save the config now
				self.application.ConfigSave()

		elif password != oldpassword:
			msg = _("""\
It appears you are using a different password for 
this account, would you like to update the saved 
information with the new password?
""")

			dlg = wx.MessageDialog(self, msg, _("Update Password?"), wx.YES_NO|wx.YES_DEFAULT|wx.ICON_INFORMATION)
			if dlg.ShowModal() == wx.ID_YES:
				# Update the password
				self.config['details'][server][PASSWORD] = password
				# Save the config now
				self.application.ConfigSave()

		self.application.network.Call(self.application.network.ConnectTo, server, username, password, debug=self.config['debug'])

	def OnCancel(self, evt):
		self.OnExit(evt)

	def OnConfig(self, evt):
		self.application.ConfigDisplay()

	def OnSinglePlayer(self, evt):
		wizard = SinglePlayerWizard(self)
		if wizard.Run():
			port = wizard.game.start()
			if port:
				self.Server.SetValue("tp://localhost:" + str(port))
				self.OnOkay(None)

	def OnFind(self, evt):
		self.application.gui.Show(self.application.gui.servers)

	def ShowURL(self, url):
		# Split the URL out into username, password, etc
		# <proto>://<username>:<password>@<server>/<game>
		# server = <proto>://<server>/
		# username = <username>@<game>
		# password = <server>
		server, username, game, password = url2bits(url)

		if server is None or len(server) == 0:
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
					del config[server]

		except (ValueError, KeyError), e:
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

		#self.Server.Clear()
		self.Server.AppendItems(self.config['servers'])
		#self.Server.SetValue(self.config['servers'][0])

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

	def OnConfigPassword(self, evt):
		server = self.ConfigPanel.ServerDetails.GetLabel()[len(_("Login for ")):]
		self.config['details'][server][1] = self.ConfigPanel.Password.GetValue()

	def OnConfigAutoConnect(self, evt):
		server = self.ConfigPanel.ServerDetails.GetLabel()[len(_("Login for ")):]

		if evt.Checked():
			# Check that no other server is also set to autoconnect
			for key, details in self.config['details'].items():
				if not details[2]: 
					continue
				msg = _("""
The client is already set to autoconnect to %s.

Would you instead like to autoconnect to %s.
""") % (key, server)
				dlg = wx.MessageDialog(self.ConfigPanel, msg, _("Autoconnect to?"), wx.OK|wx.CANCEL|wx.ICON_INFORMATION)
				if dlg.ShowModal() == wx.ID_OK:
					details[2] = False
					break

		self.config['details'][server][2] = evt.Checked()

	def OnConfigDebug(self, evt):
		self.config['debug'] = evt.Checked()
