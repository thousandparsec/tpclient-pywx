"""\
This module contains the "base" for all main windows. It does things
like prepending "TP:" to the title, vetoing closing of the window
and raising all the other windows when one is clicked.
"""

import wx

class Blank:
	pass
wx.local = Blank()

class CacheUpdateEvent:
	pass
wx.local.CacheUpdateEvent = CacheUpdateEvent

class SelectObjectEvent(wx.PyEvent):
	def __init__(self, id):
		self.id = id
wx.local.SelectObjectEvent = SelectObjectEvent

class SelectOrderEvent(wx.PyEvent):
	def __init__(self, id, slot, save=False):
		self.id = id
		self.slot = slot
		self.save = save
wx.local.SelectOrderEvent = SelectOrderEvent

wx.local.smallSize  = wx.Size(15,15)
wx.local.buttonSize = wx.Size(50,20)
wx.local.spinSize   = wx.Size(40,15)

wx.local.normalFont = wx.Font(7,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
try:
    wx.local.tinyFont   = wx.Font(6,  wx.DEFAULT, wx.LIGHT, wx.NORMAL)
except:
    wx.local.tinyFont   = wx.Font(6,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)    
wx.local.largeFont  = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

class winBaseMixIn:
	def __init__(self, application, parent, 
			pos=wx.DefaultPosition, 
			size=wx.DefaultSize, 
			style=wx.DEFAULT_FRAME_STYLE):

		self.application = application
		self.parent = parent

		self.Bind(wx.EVT_ACTIVATE, self.OnRaise)
		self.Bind(wx.EVT_CLOSE, self.OnProgramExit)

	def OnProgramExit(self, evt):
		evt.Veto(true)

	def OnRaise(self, evt):
		if wx.Platform != '__WXMSW__':
			if self.application.windows.config.raise_ == "All on All":
				self.application.windows.Raise()
			elif self.application.windows.config.raise_ == "All on Main":
				if self.title == "Thousand Parsec":
					self.application.windows.Raise()
			elif self.application.windows.config.raise_ == "Individual":
				pass
			else:
				print "Unknown raise method:", self.application.windows.config.raise_

# These give a MDI interface under windows
class winMDIBase(wx.MDIParentFrame, winBaseMixIn):
	def __init__(self, application, parent, 
			pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		wx.MDIParentFrame.__init__(self, None, -1, 'TP: ' + self.title, pos, size, style)
		winBaseMixIn.__init__(self, application, parent, pos, size, style)

		

class winMDISubBase(wx.MDIChildFrame, winBaseMixIn):
	def __init__(self, application, parent, 
			pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		wx.MDIChildFrame.__init__(self, parent, -1, 'TP: ' + self.title, pos, size, style)
		winBaseMixIn.__init__(self, application, parent, pos, size, style)

# These give a non-MDI interface under other operating systems
class winNormalBase(wx.Frame, winBaseMixIn):
	def __init__(self, application, parent, 
			pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		wx.Frame.__init__(self, parent, -1, 'TP: ' + self.title, pos, size, style)
		winBaseMixIn.__init__(self, application, parent, pos, size, style)

class winNormalSubBase(wx.MiniFrame, winBaseMixIn):
	def __init__(self, application, parent, 
			pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		wx.MiniFrame.__init__(self, parent, -1, 'TP: ' + self.title, pos, size, style + wx.FRAME_NO_TASKBAR)
		winBaseMixIn.__init__(self, application, parent, pos, size, style)

		self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

	def OnCreate(self, evt):
		if wx.Platform == '__WXGTK__':
			try:
				import pygtk
				pygtk.require("2.0")
				
				import gtk
				window = gtk.gdk.window_lookup(long(self.GetHandle())).get_toplevel()
				window.set_skip_taskbar_hint(True)
			except:
				print "WARNING: You don't have pygtk (>2.2) installed - I won't be able to hide windows under linux."

if wx.Platform == '__WXMSW__':
	winMainBase = winMDIBase
	winBase = winMDISubBase
else:
	winMainBase = winNormalBase
	winBase = winNormalSubBase

__all__ = ['winMainBase', 'winBase', '__all__']
