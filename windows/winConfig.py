"""\
This module contains the config window.
"""

# wxPython Imports
import wx
import wx.lib.anchors

# Local Imports
from winBase import *
from config import *

ID_TEXT=-1
ID_NOTEBOOK = 10045

# Shows messages from the game system to the player.
class winConfig(winBase):
	title = "Config"
	
	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style|wx.TAB_TRAVERSAL)

		self.application = application

		panel = wx.Panel(self, -1)
		panel.SetConstraints(wx.lib.anchors.LayoutAnchors(self, 1, 1, 1, 1))
		self.obj = {}

		item0 = wx.BoxSizer( wx.HORIZONTAL )
	
		item2 = wx.Notebook( panel, ID_NOTEBOOK, wx.DefaultPosition, wx.DefaultSize, 0 )
		item1 = wx.NotebookSizer( item2 )

#		item3 = panelConfigStartup(application, self, item2)
#		item2.AddPage( item3, "Startup" )

		item4 = panelConfigWindows(application, self, item2)
		item2.AddPage( item4, "Windows" )

		item0.AddSizer( item1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		panel.SetAutoLayout( True )
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

class panelConfigStartup(wx.Panel):
	def __init__(self, application, frame, parent):
		wx.Panel.__init__(self, parent, -1)

		self.frame = frame
		self.application = application
		
		self.obj = {}

		item0 = wx.BoxSizer( wx.VERTICAL )
	
		item1 = wx.BoxSizer( wx.HORIZONTAL )
	
		item2 = wx.BoxSizer( wx.VERTICAL )
	
		item3 = wx.CheckBox( self, ID_SPLASH, "Show Splash Screen", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item3, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['splash'] = item3
	
		item4 = wx.CheckBox( self, ID_AUTOCONNECT, "Connect on Startup", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['auto_connect'] = item4

		item5 = wx.CheckBox( self, ID_TIPS, "Show Welcome Tips", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['tips'] = item5

		item1.AddSizer( item2, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item6 = wx.GridSizer( 0, 2, 0, 0 )
	
		item7 = wx.StaticText( self, ID_TEXT, "Startup Server", wx.DefaultPosition, wx.DefaultSize, 0 )
		item6.AddWindow( item7, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
	
		item8 = wx.ComboBox( self, ID_AUTOSERVER, "", wx.DefaultPosition, wx.Size(100,-1), [], wx.CB_DROPDOWN )
		item8.SetToolTip( wx.ToolTip("The server to connect to on autoconnect.") )
		item8.Enable(False)
		item6.AddWindow( item8, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['auto_server'] = item8

		item9 = wx.StaticText( self, ID_TEXT, "Username", wx.DefaultPosition, wx.DefaultSize, 0 )
		item6.AddWindow( item9, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
	
		item10 = wx.ComboBox( self, ID_AUTOUSERNAME, "", wx.DefaultPosition, wx.Size(100,-1), [], wx.CB_DROPDOWN )
		item10.SetToolTip( wx.ToolTip("The username to use on autoconnect.") )
		item10.Enable(False)
		item6.AddWindow( item10, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['auto_username'] = item10

		item11 = wx.StaticText( self, ID_TEXT, "Password", wx.DefaultPosition, wx.DefaultSize, 0 )
		item6.AddWindow( item11, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item12 = wx.TextCtrl( self, ID_AUTOPASSWORD, "", wx.DefaultPosition, wx.Size(80,-1), wx.TE_PASSWORD )
		item12.Enable(False)
		item6.AddWindow( item12, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['auto_password'] = item12

		item1.AddSizer( item6, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item0.AddSizer( item1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item13 = wx.BoxSizer( wx.HORIZONTAL )
	
		item14 = wx.Button( self, ID_SAVE, "Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		item14.SetDefault()
		item13.AddWindow( item14, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		wx.EVT_BUTTON(self, ID_SAVE, self.OnSave)

		item15 = wx.Button( self, ID_REVERT, "Revert", wx.DefaultPosition, wx.DefaultSize, 0 )
		item13.AddWindow( item15, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		wx.EVT_BUTTON(self, ID_SAVE, self.OnRevert)

		item0.AddSizer( item13, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.SetAutoLayout( True )
		self.SetSizer( item0 )
		
		item0.Fit( self )
		item0.SetSizeHints( self )
	
	def OnSave(self, evt):
		pass
	
	def OnRevert(self, evt):
		pass

ID_MESSAGE	= 10054
ID_INFO		= 10064
ID_ORDER	= 10055
ID_STARMAP	= 10056
ID_SYSTEM	= 10057
ID_RAISE	= 10058
ID_RADIOBOX = 10059
ID_XPOS		= 10060
ID_YPOS		= 10061
ID_WIDTH	= 10062
ID_HEIGHT	= 10063

class panelConfigWindows(wx.Panel):
	def __init__(self, application, frame, parent):
		wx.Panel.__init__(self, parent, -1)
	
		self.frame = frame
		self.application = application

		self.obj = {}
		
		item0 = wx.BoxSizer( wx.VERTICAL )
	
		item1 = wx.BoxSizer( wx.HORIZONTAL )
	
		item3 = wx.StaticBox( self, -1, "Show Windows" )
		item2 = wx.StaticBoxSizer( item3, wx.VERTICAL )
		
		item4 = wx.CheckBox( self, ID_MESSAGE, "Message", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['show_message'] = item4
		wx.EVT_CHECKBOX(self, ID_MESSAGE, self.OnShowMessage)

		item4 = wx.CheckBox( self, ID_INFO, "Info", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['show_info'] = item4
		wx.EVT_CHECKBOX(self, ID_INFO, self.OnShowMessage)

		item5 = wx.CheckBox( self, ID_ORDER, "Order", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item5, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['show_order'] = item5
		wx.EVT_CHECKBOX(self, ID_ORDER, self.OnShowOrder)

		item6 = wx.CheckBox( self, ID_STARMAP, "StarMap", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item6, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['show_starmap'] = item6
		wx.EVT_CHECKBOX(self, ID_STARMAP, self.OnShowStarMap)

		item7 = wx.CheckBox( self, ID_SYSTEM, "System", wx.DefaultPosition, wx.DefaultSize, 0 )
		item2.AddWindow( item7, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.obj['show_system'] = item7
		wx.EVT_CHECKBOX(self, ID_SYSTEM, self.OnShowSystem)

		item1.AddSizer( item2, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		if wx.Platform == '__WXMSW__':
			item8 = wx.RadioBox( self, ID_RAISE, "Raise", wx.DefaultPosition, wx.DefaultSize, 
					["Individual", "All on Main"] , 1, wx.RA_SPECIFY_COLS )
		else:
			item8 = wx.RadioBox( self, ID_RAISE, "Raise", wx.DefaultPosition, wx.DefaultSize, 
					["Individual", "All on Main", "All on All"] , 1, wx.RA_SPECIFY_COLS )
			
		item8.SetToolTip( wx.ToolTip("Choose a method for raising the windows.") )
		item1.AddWindow( item8, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		self.obj['raise'] = item8
		wx.EVT_RADIOBOX(self, ID_RAISE, self.OnRaiseSelection)

		item9 = wx.RadioBox( self, ID_RADIOBOX, "Window", wx.DefaultPosition, wx.DefaultSize, 
				["Main", "Info", "Message","Order","StarMap","System"] , 1, wx.RA_SPECIFY_COLS )
		item1.AddWindow( item9, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		self.obj['window'] = item9
		wx.EVT_RADIOBOX(self, ID_RADIOBOX, self.OnWindowSelection)

		item11 = wx.StaticBox( self, -1, "Attributes" )
		item10 = wx.StaticBoxSizer( item11, wx.VERTICAL )
		
		item12 = wx.FlexGridSizer( 0, 2, 0, 0 )
		item12.AddGrowableCol( 1 )
		
		item13 = wx.StaticText( self, ID_TEXT, "X Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item13, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item14 = wx.SpinCtrl( self, ID_XPOS, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item14, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['xpos'] = item14
		wx.EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		item15 = wx.StaticText( self, ID_TEXT, "Y Position", wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item15, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item16 = wx.SpinCtrl( self, ID_YPOS, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item16, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['ypos'] = item16
		wx.EVT_SPINCTRL(self, ID_YPOS, self.OnYPos)

		item17 = wx.StaticText( self, ID_TEXT, "Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item17, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item18 = wx.SpinCtrl( self, ID_WIDTH, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item18, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['width'] = item18
		wx.EVT_SPINCTRL(self, ID_WIDTH, self.OnWidth)

		item19 = wx.StaticText( self, ID_TEXT, "Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item19, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item20 = wx.SpinCtrl( self, ID_HEIGHT, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item20, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['height'] = item20
		wx.EVT_SPINCTRL(self, ID_HEIGHT, self.OnHeight)

		item10.AddSizer( item12, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item1.AddSizer( item10, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		item0.AddSizer( item1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item21 = wx.BoxSizer( wx.HORIZONTAL )
		
		item22 = wx.Button( self, ID_SAVE, "Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		item21.AddWindow( item22, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		wx.EVT_BUTTON(self, ID_SAVE, self.OnSave)

		item23 = wx.Button( self, ID_REVERT, "Revert", wx.DefaultPosition, wx.DefaultSize, 0 )
		item21.AddWindow( item23, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		wx.EVT_BUTTON(self, ID_REVERT, self.OnRevert)

		item0.AddSizer( item21, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.SetAutoLayout( True )
		self.SetSizer( item0 )
		
		item0.Fit( self )
		item0.SetSizeHints( self )
		
		wx.EVT_SET_FOCUS(parent, self.OnFocus) 

	def OnFocus(self, evt):
		self.OnWindowSelection(None)

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
		self.frame.Show(False)
		self.application.windows.Raise()

	def OnRevert(self, evt):
#		self.application.config = self.application.windows.ConfigLoad()
		self.application.windows.ConfigActivate()
		self.frame.Show(False)
		self.application.windows.Raise()

