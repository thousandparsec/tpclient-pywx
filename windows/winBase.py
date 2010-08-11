"""\
This module contains the "base" for all main windows. It does things
like prepending "TP:" to the title, vetoing closing of the window
and raising all the other windows when one is clicked.
"""

import wx
import os.path

from requirements import graphicsdir

import utils

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

	wx.local.normalFont = wx.Font(10,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)
	try:
		wx.local.tinyFont   = wx.Font(8,  wx.DEFAULT, wx.LIGHT, wx.NORMAL)
	except:
		wx.local.tinyFont   = wx.Font(8,  wx.DEFAULT, wx.NORMAL, wx.NORMAL)	
	wx.local.largeFont  = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

class ShiftMixIn(object):
	def __init__(self):
		# Bits for doing the button changing on shift
		self.shiftimer = wx.Timer(self)
		self.shift = False

	def ShiftStart(self):
		self.shiftimer.Start(50)
		self.Bind(wx.EVT_TIMER, self.OnShiftTimer, self.shiftimer)

	def ShiftStop(self):
		if self.shiftimer.Stop():
			self.Unbind(wx.EVT_TIMER, self.shiftimer)
		
	def OnShiftTimer(self, evt):
		shift = wx.GetKeyState(wx.WXK_SHIFT)
		if self.shift == shift:
			return
		
		self.shift = shift
		if self.shift:
			if hasattr(self, 'OnShiftDown'):
				return self.OnShiftDown(evt)
		else:
			if hasattr(self, 'OnShiftUp'):
				return self.OnShiftUp(evt)

class ConfigMixIn(object):
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		return {}

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		return self.config
		
	def ConfigLoad(self, config={}):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		return

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		raise AssertionError("ConfigUpdate not implimented")

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		raise AssertionError("ConfigDisplay not implimented")
	
	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		raise AssertionError("ConfigDisplayUpdate not implimented")

class winMixIn(object):
	"""
	Applies to all windows.
	"""
	def __init__(self, application, parent):
		self.application = application
		self.parent      = parent

		self.config = self.ConfigDefault()

		# Set the Icon of the window
		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(wx.Bitmap(os.path.join(graphicsdir, "icon.ico"), wx.BITMAP_TYPE_ANY))
		self.SetIcon(icon)

		self.Bind(wx.EVT_CLOSE, self.OnClose)

	def PreCreate(self, pre):
		pre.SetTitle('TP: ' + self.title)

	def __str__(self):
		if hasattr(self, 'title'):
			return "<win %s>" % self.title
		return super(self.__class__, self).__str__()

	def OnClose(self, evt):
		# Ignore close events
		if hasattr(evt, 'CanVeto') and evt.CanVeto():
			evt.Veto(True)
		self.Hide()

class winBaseMixIn(winMixIn):
	"""
	Applies to all top level windows.
	"""
	def __init__(self, application):
		winMixIn.__init__(self, application, None)
		self.children = {}

	def PreCreate(self, pre):
		pre.SetTitle('TP: ' + self.title)

	def OnActivate(self, evt):
		if not evt.GetActive():
			return
		self.RaiseChildren()

	def HideChildren(self):
		for window in self.children.values():
			if isinstance(window, winMixIn):
				window.Hide()

	def RaiseChildren(self):
		for window in self.children.values():
			if isinstance(window, winBase):
				window.Raise()

# These give a non-MDI interface under other operating systems
class winBase(ConfigMixIn, winBaseMixIn, wx.Frame):
	def __init__(self, application):
		x, y, width, height = wx.GetClientDisplayRect()
		wx.Frame.__init__(self, None, -1, 'TP: ' + self.title, (x, y), (width, height), \
				wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		winBaseMixIn.__init__(self, application)

class winBaseXRC(ConfigMixIn, winBaseMixIn, wx.Frame):
	def __init__(self, application):
		winBaseMixIn.__init__(self, application)

class winReportXRC(ConfigMixIn, winMixIn, wx.Frame):
	def __init__(self, application, parent):
		winMixIn.__init__(self, application, parent)

"""\
There are 2 classes of windows in tpclient-pywx
	- winMainBase, This is used for main windows, only one of these windows can be open at one time.
	- winSubBase,  This is used by windows which are children of a main window (reports and such).

A winShiftMixIn is also provided which allows the windows to respond to Shift being pressed.
"""

__all__ = ['winBase', 'winReport', 'ShiftMixIn']
