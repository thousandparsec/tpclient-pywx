"""\
This module contains the config window.
"""

# wxPython Imports
import wx
import wx.lib.anchors

# Local Imports
from winBase import *

# Shows messages from the game system to the player.
class winConfig(winBase):
	title = _("Config")
	
	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style|wx.TAB_TRAVERSAL)

		self.application = application

		panel = wx.Panel(self, -1)
		panel.SetConstraints(wx.lib.anchors.LayoutAnchors(self, 1, 1, 1, 1))
		self.obj = {}

		item0 = wx.BoxSizer( wx.HORIZONTAL )
	
		self.notebook = wx.Notebook( panel, -1, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.notebook.AddPage(panelConfigWindows(application, self, self.notebook), _("Windows") )

		item1 = wx.NotebookSizer( self.notebook )
		item0.AddSizer( item1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		panel.SetAutoLayout( True )
		panel.SetSizer( item1 )
		
		item1.Fit( panel )
		item1.SetSizeHints( panel )

		self.Fit()

		self.Bind(wx.EVT_ACTIVATE, self.OnFocus)
		
	def OnFocus(self, evt):
		page = self.notebook.GetSelection()
		if page >= 0:
			panel = self.notebook.GetPage(page)
			panel.OnFocus(evt)
		

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
	
		self.show_box = wx.StaticBox( self, -1, _("Hide Windows") )
		self.show_sizer = wx.StaticBoxSizer( self.show_box, wx.VERTICAL )
		
		self.show_info = wx.CheckBox( self, -1, _("Info"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.show_sizer.AddWindow( self.show_info, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.Bind(wx.EVT_CHECKBOX, self.OnShowInfo, self.show_info)

		self.show_order = wx.CheckBox( self, -1, _("Order"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.show_sizer.AddWindow( self.show_order, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.Bind(wx.EVT_CHECKBOX, self.OnShowOrder, self.show_order)

		self.show_message = wx.CheckBox( self, -1, _("Message"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.show_sizer.AddWindow( self.show_message, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.Bind(wx.EVT_CHECKBOX, self.OnShowMessage, self.show_message)

		self.show_starmap = wx.CheckBox( self, -1, _("StarMap"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.show_sizer.AddWindow( self.show_starmap, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.Bind(wx.EVT_CHECKBOX, self.OnShowStarMap, self.show_starmap)

		self.show_system = wx.CheckBox( self, -1, _("System"), wx.DefaultPosition, wx.DefaultSize, 0 )
		self.show_sizer.AddWindow( self.show_system, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		self.Bind(wx.EVT_CHECKBOX, self.OnShowSystem, self.show_system)

		item1.AddSizer( self.show_sizer, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		options = []
		if wx.Platform == '__WXMSW__':
			options = [_("Individual"), _("All on Main")]
		elif wx.Platform == '__WXMAC__':
			options = [_("Individual"), _("All on All")]
		else:
			options = [_("Individual"), _("All on Main"), _("All on All")]

		self.raisebox = wx.RadioBox( self, -1, _("Raise"), wx.DefaultPosition, wx.DefaultSize, options, 1, wx.RA_SPECIFY_COLS )
		self.raisebox.SetToolTip( wx.ToolTip(_("Choose a method for raising the windows.")) )
		item1.AddWindow( self.raisebox, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		self.Bind(wx.EVT_RADIOBOX, self.OnRaiseSelection, self.raisebox)

		self.windows = wx.RadioBox( self, -1, _("Window"), wx.DefaultPosition, wx.DefaultSize, 
				[_("Main"), _("Info"), _("Order"), _("Message"), _("StarMap"), _("System")] , 1, wx.RA_SPECIFY_COLS )
		item1.AddWindow( self.windows, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		self.Bind(wx.EVT_RADIOBOX, self.OnWindowSelection, self.windows)

		item11 = wx.StaticBox( self, -1, _("Attributes") )
		item10 = wx.StaticBoxSizer( item11, wx.VERTICAL )
		
		item12 = wx.FlexGridSizer( 0, 2, 0, 0 )
		item12.AddGrowableCol( 1 )
		
		item13 = wx.StaticText( self, -1, _("X Position"), wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item13, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item14 = wx.SpinCtrl( self, ID_XPOS, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item14, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['xpos'] = item14
		wx.EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		item15 = wx.StaticText( self, -1, _("Y Position"), wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item15, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item16 = wx.SpinCtrl( self, ID_YPOS, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item16, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['ypos'] = item16
		wx.EVT_SPINCTRL(self, ID_YPOS, self.OnYPos)

		item17 = wx.StaticText( self, -1, _("Width"), wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item17, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item18 = wx.SpinCtrl( self, ID_WIDTH, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item18, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['width'] = item18
		wx.EVT_SPINCTRL(self, ID_WIDTH, self.OnWidth)

		item19 = wx.StaticText( self, -1, _("Height"), wx.DefaultPosition, wx.DefaultSize, 0 )
		item12.AddWindow( item19, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		item20 = wx.SpinCtrl( self, ID_HEIGHT, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		item12.AddWindow( item20, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.obj['height'] = item20
		wx.EVT_SPINCTRL(self, ID_HEIGHT, self.OnHeight)

		item10.AddSizer( item12, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item1.AddSizer( item10, 0, wx.GROW|wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )

		item0.AddSizer( item1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

		item21 = wx.BoxSizer( wx.HORIZONTAL )
		
		save = wx.Button( self, -1, _("Save"), wx.DefaultPosition, wx.DefaultSize, 0 )
		item21.AddWindow( save, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.Bind(wx.EVT_BUTTON, self.OnSave, save)

		revert = wx.Button( self, -1, _("Revert"), wx.DefaultPosition, wx.DefaultSize, 0 )
		item21.AddWindow( revert, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		self.Bind(wx.EVT_BUTTON, self.OnRevert, revert)
		revert.SetDefault()

		item0.AddSizer( item21, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.SetAutoLayout( True )
		self.SetSizer( item0 )
		
		item0.Fit( self )
		item0.SetSizeHints( self )

	def OnFocus(self, evt):
		self.OnWindowsShow(None)
		self.OnWindowSelection(None)

	def OnShowInfo(self, evt):
		self.application.windows.config.info.show = not evt.Checked()
		self.application.windows.info.Show(not evt.Checked())
		
	def OnShowOrder(self, evt):
		self.application.windows.config.order.show = not evt.Checked()
		self.application.windows.order.Show(not evt.Checked())
		
	def OnShowMessage(self, evt):
		self.application.windows.config.message.show = not evt.Checked()
		self.application.windows.message.Show(not evt.Checked())

	def OnShowStarMap(self, evt):
		self.application.windows.config.starmap.show = not evt.Checked()
		self.application.windows.starmap.Show(not evt.Checked())
		
	def OnShowSystem(self, evt):
		self.application.windows.config.system.show = not evt.Checked()
		self.application.windows.system.Show(not evt.Checked())

	def OnWindowsShow(self, evt):
		if not hasattr(self.application, "windows"):
			return

		# Fill in the show settings
		self.show_info.SetValue(not self.application.windows.config.info.show)
		self.show_order.SetValue(not self.application.windows.config.order.show)
		self.show_message.SetValue(not self.application.windows.config.message.show)
		self.show_starmap.SetValue(not self.application.windows.config.starmap.show)
		self.show_system.SetValue(not self.application.windows.config.system.show)
		
	def OnXPos(self, evt):
		self.current_window.SetPosition((self.obj['xpos'].GetValue(), -1))

	def OnYPos(self, evt):
		self.current_window.SetPosition((-1, self.obj['ypos'].GetValue()))

	def OnWidth(self, evt):
		self.current_window.SetSize((self.obj['width'].GetValue(), -1))

	def OnHeight(self, evt):
		self.current_window.SetSize((-1, self.obj['height'].GetValue()))

	def OnWindowSelection(self, evt):
		if not hasattr(self.application, "windows"):
			return
		window = self.windows.GetStringSelection()
		self.current_window = getattr(self.application.windows, window.lower())
		pos = self.current_window.GetPosition()
		size = self.current_window.GetSize()

		self.obj['xpos'].SetValue(pos[0])
		self.obj['ypos'].SetValue(pos[1])
		self.obj['width'].SetValue(size[0])
		self.obj['height'].SetValue(size[1])

	def OnRaiseSelection(self, evt):
		style = self.raisebox.GetStringSelection()
		self.application.windows.config.raise_ = style

	def OnSave(self, evt):
		print "OnSave"
		self.application.windows.ConfigSave()
		self.frame.Show(False)
		self.application.windows.Raise()

	def OnRevert(self, evt):
		self.application.config = self.application.windows.ConfigLoad()
		self.application.windows.ConfigActivate(show=True)
		self.frame.Show(False)
		self.application.windows.Raise()

