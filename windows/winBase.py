"""\
This module contains the "base" for all main windows. It does things
like prepending "TP:" to the title, vetoing closing of the window
and raising all the other windows when one is clicked.
"""

import wx
import os.path

class Blank:
	pass
wx.local = Blank()

if wx.Platform == "__WXMAC__":
	wx.local.smallSize  = wx.Size(25,25)
	wx.local.buttonSize = wx.Size(60,30)
	wx.local.spinSize   = wx.Size(50,25)

	wx.local.normalFont = wx.Font(12,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
	try:
	    wx.local.tinyFont   = wx.Font(10,  wx.DEFAULT, wx.LIGHT, wx.NORMAL)
	except:
	    wx.local.tinyFont   = wx.Font(10,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)    
	wx.local.largeFont  = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

else:
	wx.local.smallSize  = wx.Size(15,15)
	wx.local.buttonSize = wx.Size(50,20)
	wx.local.spinSize   = wx.Size(40,15)

	wx.local.normalFont = wx.Font(7,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
	try:
	    wx.local.tinyFont   = wx.Font(6,  wx.DEFAULT, wx.LIGHT, wx.NORMAL)
	except:
	    wx.local.tinyFont   = wx.Font(6,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)    
	wx.local.largeFont  = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

class winBaseMixIn(object):
	def __init__(self, application, parent, config=None):
		self.application = application
		self.parent = parent
		self.children = {}
		self.config = {}
	
		if hasattr(parent, 'children'):
			self.parent.children[self.title] = self

		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(wx.Bitmap(os.path.join("graphics", "icon.ico"), wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)

		self.Bind(wx.EVT_ACTIVATE, self.OnRaise)
		self.Bind(wx.EVT_CLOSE, self.OnProgramExit)

	def OnProgramExit(self, evt):
		evt.Veto(True)

	def OnRaise(self, evt):
		if not evt.GetActive():
			return
		
		if wx.Platform != '__WXMSW__':
			if not self.config.has_key('raise') or self.config['raise'] == "All on All" or self.config['raise'] == "All on Main":
				if hasattr(self, "children"):
					for window in self.children.values():
						window.Raise()

	def ConfigSave(self):
		"""
		Returns the configuration of the Window (and it's children).
		"""
		# Save position, size, other config information
		
		config = self.config
		config['position'] = self.GetPositionTuple()
		config['size'] = self.GetSizeTuple()
		config['shown'] = self.IsShown()
		
		for name, window in self.children.items():
			config['name'] = window.ConfigSave()
		
		return config

	def ConfigLoad(self, config):
		"""
		Loads the configuration of the Window (and it's children).
		"""
		self.config = config
		self.SetPosition(config['position'])
		self.SetSize(config['size'])
		self.Show(config['shown'])

		for name, window in self.children.items():
			window.ConfigLoad(config[name])

	def ConfigDisplay(self, panel, sizer):
		"""
		"""
		box = wx.StaticBox(panel, -1, self.title)
		box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
		
		sizer.Add(box_sizer, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
	
		# Checkbox for "Show"
		show = wx.CheckBox(panel, -1, _("Show?"), wx.DefaultPosition, wx.DefaultSize, 0 )
		box_sizer.Add(show, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		#self.Bind(wx.EVT_CHECKBOX, self.OnShowInfo, self.show_info)

		# Location Boxes
		location = wx.FlexGridSizer( 0, 2, 0, 0 )
		location.AddGrowableCol( 1 )
	
		x_text = wx.StaticText(panel, -1, _("X Pos"), wx.DefaultPosition, wx.DefaultSize, 0 )
		location.Add( x_text, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		x = wx.SpinCtrl(panel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		location.Add( x, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		#wx.EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		y_text = wx.StaticText(panel, -1, _("Y Pos"), wx.DefaultPosition, wx.DefaultSize, 0 )
		location.Add( y_text, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		y = wx.SpinCtrl(panel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		location.Add( y, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		#wx.EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		width_text = wx.StaticText(panel, -1, _("Width"), wx.DefaultPosition, wx.DefaultSize, 0 )
		location.Add( width_text, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		width = wx.SpinCtrl(panel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		location.Add( width, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		#wx.EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		height_text = wx.StaticText(panel, -1, _("Height"), wx.DefaultPosition, wx.DefaultSize, 0 )
		location.Add( height_text, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		height = wx.SpinCtrl(panel, -1, "0", wx.DefaultPosition, wx.Size(50,-1), 0, 0, 10000, 0 )
		location.Add( height, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		#wx.EVT_SPINCTRL(self, ID_XPOS, self.OnXPos)

		box_sizer.Add(location, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

	def Post(self, event):
		func = 'On' + event.__class__.__name__[:-5]	
		if hasattr(self, func):
			getattr(self, func)(event)

		for window in self.children.values():
			window.Post(event)

	def Show(self, show=True):
		if not show:
			return self.Hide()
		
		for window in self.children.values():
			window.Show()

			if wx.Platform == "__WXMAC__":
				value.SetMenuBar(self.current.Menu())
		return super(winBaseMixIn, self).Show()

	def Hide(self):
		for window in self.children.values():
			window.Hide()
		return super(winBaseMixIn, self).Hide()

	def Raise(self):
		for window in self.children.values():
			window.Raise()
		return super(winBaseMixIn, self).Raise()

# These give a MDI interface under windows
class winMDIBase(winBaseMixIn, wx.MDIParentFrame):
	def __init__(self, application):
		wx.MDIParentFrame.__init__(self, None, -1, 'TP: ' + self.title, wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
		winBaseMixIn.__init__(self, application, None)

class winMDISubBase(winBaseMixIn, wx.MDIChildFrame):
	def __init__(self, application, parent):
		wx.MDIChildFrame.__init__(self, parent, -1, 'TP: ' + self.title, wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		winBaseMixIn.__init__(self, application, parent)

# These give a non-MDI interface under other operating systems
class winNormalBase(winBaseMixIn, wx.Frame):
	def __init__(self, application):
		wx.Frame.__init__(self, None, -1, 'TP: ' + self.title, wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
		winBaseMixIn.__init__(self, application, None)

class winNormalSubBase(winBaseMixIn, wx.MiniFrame):
	def __init__(self, application, parent):
		wx.MiniFrame.__init__(self, parent, -1, 'TP: ' + self.title, wx.DefaultPosition, wx.DefaultSize, wx.DEFAULT_FRAME_STYLE|wx.FRAME_NO_TASKBAR|wx.TAB_TRAVERSAL)
		winBaseMixIn.__init__(self, application, parent)

if wx.Platform == '__WXMSW__':
	winMainBase = winMDIBase
	winBase = winMDISubBase
else:
	winMainBase = winNormalBase
	winBase = winNormalSubBase

__all__ = ['winMainBase', 'winBase', '__all__']
