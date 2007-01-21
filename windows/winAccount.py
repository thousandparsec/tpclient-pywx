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
from winBase import winMainBaseXRC
from winConnect import usernameMixIn
from xrc.winAccount import winAccountBase

throbber = os.path.join("graphics", "downloading.gif")
okay = os.path.join("graphics", "finished.gif")

class winAccount(winAccountBase, winMainBaseXRC, usernameMixIn):
	title = _("Account")

	def __init__(self, application):
		winAccountBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)	
		usernameMixIn.__init__(self)

	def Show(self, show=True):
		if not show:
			return self.Hide()

		self.Panel.Layout()
		size = self.Panel.GetBestSize()
		self.SetClientSize(size)
		self.CenterOnScreen(wx.BOTH)

		url = self.application.gui.servers.URL.GetValue()
		g = url.rfind('/')
		url, game = url[:g], url[g+1:]
		self.Server.SetValue(url)

		self.State("start")

		winMainBaseXRC.Show(self, show)

	def State(self, mode):
		if mode == "start":
			# Enable the host entry box
			self.Server.Enable()

			# Show and enable the connect button
			self.Check.Show()
			self.Check.Enable()
			
			# Stop and hide the throbber
			self.Checking.LoadFile(throbber)
			self.Checking.Stop()
			self.Checking.Hide()

			# Disable the okay button
			self.Cancel.Enable()
			self.Okay.Disable()

			# Disable the entries	
			self.Username.Disable()
			self.GameShow.Disable()
			self.Game.Disable()
			self.Password1.Disable()
			self.Password2.Disable()
			self.Email.Disable()

			self.Check.SetDefault()
			self.Server.SetFocus()

		if mode == "connecting":
			# Stop the entry to host 
			self.Server.Disable()

			# Hide the connect button
			self.Check.Hide()
			self.Check.Disable()

			# Show and start the throbber
			self.Checking.LoadFile(throbber)
			self.Checking.Show()
			self.Checking.Play()

			# Disable the okay button
			self.Cancel.Enable()
			self.Okay.Disable()

			# Disable the entries	
			self.Username.Disable()
			self.GameShow.Disable()
			self.Game.Disable()
			self.Password1.Disable()
			self.Password2.Disable()
			self.Email.Disable()

		if mode == "details":
			# Stop the entry to host
			self.Server.Disable()

			# Show the connect button but disabled
			self.Check.Hide()
			self.Check.Disable()

			# Stop and hide the throbber
			self.Checking.LoadFile(okay)
			self.Checking.Show()
			self.Checking.Play()

			# Enable the okay button
			self.Cancel.Enable()
			self.Okay.Enable()
		
			# Enable the entries	
			self.Username.Enable()
			self.GameShow.Enable()
			self.Game.Enable()
			self.Password1.Enable()
			self.Password2.Enable()
			self.Email.Enable()
			
			self.Username.SetFocus()
			self.Okay.SetDefault()

		if mode == "saving":
			# Stop the entry to host
			self.Server.Disable()

			# Show the connect button but disabled
			self.Check.Hide()
			self.Check.Enable()

			# Stop and hide the throbber
			self.Checking.Show()
			self.Checking.Play()

			# Enable the okay button
			self.Okay.Disable()
			self.Cancel.Disable()
		
			# Enable the entries	
			self.Username.Disable()
			self.GameShow.Disable()
			self.Game.Disable()
			self.Password1.Disable()
			self.Password2.Disable()
			self.Email.Disable()

		self.Panel.Layout()
		size = self.Panel.GetBestSize()
		self.SetClientSize(size)
			
	def OnCheck(self, evt):
		self.State("connecting")
		self.application.network.Call(self.application.network.Connect, self.Server.GetValue(), 
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
		username = self.GetUsername()
		password1 = self.Password1.GetValue().strip()
		password2 = self.Password2.GetValue().strip()
		email = self.Email.GetValue().strip()

		# Check the values are sensible
		if username == "" or password1 == "" or password2 == "" or email == "":
			dlg = wx.MessageDialog(self.application.gui.current, "All fields are required.", _("Fields Required"), wx.OK|wx.ICON_ERROR)
			dlg.ShowModal()
			return
		if password1 != password2:
			dlg = wx.MessageDialog(self.application.gui.current, "Password fields do not match.", _("Fields Required"), wx.OK|wx.ICON_ERROR)
			dlg.ShowModal()
			return

		url = self.Server.GetValue()
		p = url.find('://')
		if p != -1:
			p += 3
		else:
			p = 0		

		username, game = self.GetUsernameGame()
		fullurl = "%s%s:%s@%s/%s" % (url[:p], username, password1, url[p:], game)
		print fullurl
		self.application.gui.connectto.ShowURL(fullurl)

		#self.application.network.Call(self.application.network.ConnectTo, host, username, password, debug=self.config['debug'])
		self.application.network.Call(self.application.network.NewAccount, username, password1, email)

	def OnCancel(self, evt):
		self.application.gui.Show(self.application.gui.servers)

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
