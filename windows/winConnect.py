"""\
This module contains the "connect" window which lets a
person enter the server/username/password.
"""

# Python imports
import string

# wxPython Imports
import wx

# Local Imports
from tp.netlib import failed

from winBase import winBaseMixIn
from utils import *

defaultServers = ["mithro.dyndns.org", "code-bear.dyndns.org", "llnz.dyndns.org", "127.0.0.1:6923"]

ID_OK = 10043
ID_CANCEL = 10044

TITLE_PROGRESS = _("TP: Connecting to Server")
TEXT_PROGRESS = _("""\
pywx-client is now attempting to connect to the specified server.
""")

TITLE_CONNECT = _("TP: Login Failed")
TEXT_CONNECT = _("""\
Failed to connect.
This could be because, the server is busy or the server doesn't exist.
Please try again later.
""")

TITLE_LOGIN = _("TP: Connection Failed")
TEXT_LOGIN = _("""\
Failed to login.
This could be because, the server could be busy or your username and password could be incorrect.
Please try again later.
""")

TITLE_DOWNLOAD = _("TP: Downloding Universe...")
TEXT_DOWNLOAD = _("""\
pywx-client is now downloading the Universe.
""")

# Shows messages from the game system to the player.
class winConnect(wx.Frame, winBaseMixIn):
	title = _("Connect")

	def __init__(self, application, 
			pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, None, -1, 'TP: ' + self.title, pos, size, style)
		winBaseMixIn.__init__(self, application, None, pos, size, style)

		self.application = application

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

		grid = wx.FlexGridSizer( 0, 2, 0, 0 )
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

		# Hook up the events
		self.Bind(wx.EVT_BUTTON, self.OnOkay,   button_ok)
		self.Bind(wx.EVT_BUTTON, self.OnCancel, button_cancel)
		self.Bind(wx.EVT_CLOSE,  self.OnExit)

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

		progress = wx.ProgressDialog(TITLE_PROGRESS, TEXT_PROGRESS, 5, self, wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)

		print host, port, username, password

		dlg = None
		try:
			application.connection.setup(host=host, port=port, debug=True)
			progress.Update(1)
			
			print "Connect...",
			if not failed(application.connection.connect()):
				progress.Update(3)

				print "Login...",
				if failed(application.connection.login(username, password)):
					print "Login Failed"
					dlg = wx.MessageDialog(self, TEXT_LOGIN, TITLE_LOGIN, wx.OK | wx.ICON_INFORMATION)
			else:
				print "Connect Failed"
				dlg = wx.MessageDialog(self, TEXT_CONNECT, TITLE_CONNECT, wx.OK | wx.ICON_INFORMATION)

		except:
			print "Exception Failed"
			do_traceback()
			dlg = wx.MessageDialog(self, TEXT_CONNECT, TITLE_CONNECT, wx.OK | wx.ICON_INFORMATION)

		progress.Update(5)
		if dlg == None:
			print "Success"
			self.Hide()
			application.CacheUpdate()
			application.windows.Show()
			self.Hide()
		else:
			dlg.ShowModal()
			dlg.Destroy()
