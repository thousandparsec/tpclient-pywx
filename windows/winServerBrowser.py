
# Python imports
import string
import os, os.path
import time

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBaseXRC
from xrc.winServerBrowser import winServerBrowserBase

throbber = os.path.join("graphics", "downloading.gif")
okay = os.path.join("graphics", "finished.gif")
notokay = os.path.join("graphics", "waiting.gif")

class winServerBrowser(winServerBrowserBase, winMainBaseXRC):
	title = _("Updating")
	
	def __init__(self, application):
		winServerBrowserBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)

		# Setup the columns in each 
		Columns = ("ID", "Name", "Players", "Server")
		for i in range(0, len(Columns)):
			self.InternetServers.InsertColumn(i, Columns[i])
			self.LocalServers.InsertColumn(i, Columns[i])

	def Clear(self):
		pass

	def Show(self, show=True):
		if not show:
			return self.Hide()
		
		# Clear everything
		self.Clear()

		self.CenterOnScreen(wx.BOTH)
		return winMainBaseXRC.Show(self)

	def OnCancel(self, evt):
		self.application.gui.Show(self.application.gui.connectto)	

	def OnRefresh(self, evt=None):
		print "Refresh!"
		self.Progress.LoadFile(throbber)
		self.Progress.Play()

		self.application.finder.Call(self.application.finder.refresh)

		# Disable the refresh button until the finder is done...
		self.Refresh.Disable()

	def OnRefreshFinished(self, worked, message=""):
		# Renable the refresh button
		self.Refresh.Enable()

		if worked:
			self.Progress.LoadFile(okay)
		else:
			self.Progress.LoadFile(notokay)
		self.Progress.Play()

		self.Progress.SetToolTip(message)

	def OnFinderError(self, evt):
		self.RefreshFinished(False, str(evt))

	def OnFinderFinished(self, evt):
		self.RefreshFinished(True)

	# Config Functions -----------------------------------------------------------------------------  
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		return {}

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		return {}
	
	def ConfigLoad(self, config={}):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		pass

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		pass

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		pass

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		pass
