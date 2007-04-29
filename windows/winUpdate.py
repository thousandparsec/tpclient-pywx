
# Python imports
import string
import os, os.path
import time

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBaseXRC
from xrc.winUpdate import winUpdateBase

throbber = os.path.join("graphics", "downloading.gif")
okay = os.path.join("graphics", "finished.png")
waiting = os.path.join("graphics", "waiting.png")

class winUpdate(winUpdateBase, winMainBaseXRC):
	title = _("Updating")
	
	def __init__(self, application):
		winUpdateBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)

		self.Message.Bind(wx.EVT_UPDATE_UI, self.MessageDown)
		self.GoDown = False

		if wx.Platform == "__WXMAC__":
			self.ConnectingText.SetLabel("___________")
			self.ConnectingText.SetMinSize(self.ConnectingText.GetBestSize())
			self.ProgressText.SetLabel("___________")
			self.ProgressText.SetMinSize(self.ProgressText.GetBestSize())
			self.ProgressTitle.SetLabel("_________________________________")
			self.ProgressTitle.SetMaxSize(self.ProgressTitle.GetBestSize())
			self.ProgressTitle.SetMinSize(self.ProgressTitle.GetBestSize())
			self.ProgressTitle.SetSize(self.ProgressTitle.GetBestSize())

			self.ProgressAnim.SetMinSize((32, 32))
			self.ConnectingAnim.SetMinSize((32, 32))
		else:
			self.Panel.GetSizer().GetItem(2).GetSizer().RemoveGrowableCol(1)

		self.Panel.Layout()

	def OnCancel(self, evt):
		self.application.network.Reset()
		self.application.gui.Show(self.application.gui.connectto)

	def OnSave(self, evt):
		dlg = wx.FileDialog(self, message="Save log as ...", defaultDir=os.getcwd(), 
								defaultFile="update.log", wildcard="Log file (*.log)|*.log", style=wx.SAVE)
		dlg.SetFilterIndex(0)
		if dlg.ShowModal() != wx.ID_OK:
			return

		path = dlg.GetPath()
		self.Message.SaveFile(path)

	def OnOkay(self, evt):
		self.application.gui.Show(self.application.gui.main)
		self.application.Post(self.application.cache.CacheUpdateEvent(None))

	def MessageDown(self, evt):
		if self.GoDown:
			self.Message.ShowPosition(self.Message.GetLastPosition())
			self.GoDown = False

	def Clear(self):
		# Enable the cancel button
		self.Cancel.Enable()

		self.TopText.SetLabel("")
		self.Message.SetValue("")

		self.ConnectingGauge.Enable()
		self.ConnectingGauge.SetRange(1)
		self.ConnectingGauge.SetValue(0)

		self.ConnectingAnim.Enable()
		self.ConnectingAnim.LoadFile(waiting)
		self.ConnectingAnim.Play()

		self.ConnectingText.Enable()
		self.ConnectingText.SetLabel("")

		self.ProgressTitle.SetLabel("")
		self.ProgressTitle.Hide()
		self.ProgressGauge.Disable()
		self.ProgressGauge.SetRange(1)
		self.ProgressGauge.SetValue(0)
		self.ProgressGauge.Hide()
		self.ProgressAnim.LoadFile(waiting)
		self.ProgressAnim.Play()
		self.ProgressAnim.Hide()
		self.ProgressText.SetLabel("")
		self.ProgressText.Hide()

		self.ObjectdescsAnim.LoadFile(waiting)
		self.ObjectdescsAnim.Play()

		self.OrderdescsAnim.LoadFile(waiting)
		self.OrderdescsAnim.Play()

		self.ObjectsAnim.LoadFile(waiting)
		self.ObjectsAnim.Play()

		self.OrdersAnim.LoadFile(waiting)
		self.OrdersAnim.Play()

		self.BoardsAnim.LoadFile(waiting)
		self.BoardsAnim.Play()

		self.MessagesAnim.LoadFile(waiting)
		self.MessagesAnim.Play()

		self.CategoriesAnim.LoadFile(waiting)
		self.CategoriesAnim.Play()

		self.DesignsAnim.LoadFile(waiting)
		self.DesignsAnim.Play()

		self.ComponentsAnim.LoadFile(waiting)
		self.ComponentsAnim.Play()

		self.PropertiesAnim.LoadFile(waiting)
		self.PropertiesAnim.Play()

		self.PlayersAnim.LoadFile(waiting)
		self.PlayersAnim.Play()

		self.ResourcesAnim.LoadFile(waiting)
		self.ResourcesAnim.Play()

		self.Okay.Disable()
		self.Save.Disable()

	def Show(self, show=True):
		if not show:
			return self.Hide()
		
		# Clear everything
		self.Clear()

		self.CenterOnScreen(wx.BOTH)
		return winMainBaseXRC.Show(self)

	def Update(self, mode, state, message="", todownload=None, total=None, amount=None):
		# We do a little bit different for this mode
		if mode == "connecting":
			animation = getattr(self, "%sAnim" % mode.title())

			if state == "start":
				# Start the connection throbber
				animation.LoadFile(throbber)
				animation.Play()

			elif state == "todownload":
				self.ConnectingGauge.SetValue(0)
				self.ConnectingGauge.SetRange(todownload)
			elif state == "downloaded":
				self.ConnectingGauge.SetValue(self.ConnectingGauge.GetValue()+amount)
			elif state == "finished":
				# Change to the tick
				animation.LoadFile(okay)
				animation.Play()
				
				# Set the gauge as completed!
				self.ConnectingGauge.SetValue(self.ConnectingGauge.GetRange())

				# Set the progress text
				self.ConnectingText.SetLabel("Done!")

			elif state == "alreadydone":
				self.ConnectingGauge.Disable()
				self.ConnectingText.Disable()
				animation.Disable()

		elif mode == "finishing":
			# Change the buttons
			self.Okay.Enable()
			self.Save.Enable()
			self.Cancel.Disable()

		else:	
			animation = getattr(self, "%sAnim" % mode.title())

			self.ProgressTitle.Show()
			self.ProgressGauge.Show()
			self.ProgressAnim.Show()
			self.ProgressText.Show()

			if state == "start":
				# Set the progress title
				self.ProgressTitle.SetLabel("Getting %s" % mode.title())

				# Set the progress guage to be empty
				self.ProgressGauge.Enable()
				self.ProgressGauge.SetValue(0)
				self.ProgressGauge.SetRange(1)
				
				# Set the progress text
				self.ProgressText.SetLabel("")

				# Set the progress animation
				self.ProgressAnim.LoadFile(throbber)
				self.ProgressAnim.Play()

				# Start the throbber for this mode
				animation.LoadFile(throbber)
				animation.Play()

			elif state == "todownload":
				# Now we know how big to set the gauge too
				if todownload == 0:
					self.ProgressGauge.SetValue(1)
					self.ProgressGauge.SetRange(1)
				else:	
					self.ProgressGauge.SetValue(0)
					self.ProgressGauge.SetRange(todownload)

				# Update the text
				self.ProgressText.SetLabel("%s of %s" % (0, todownload))

			elif state == "progress":
				# Nothing to do...
				pass

			elif state == "downloaded":
				# Progress the progress gauge
				self.ProgressGauge.SetValue(self.ProgressGauge.GetValue()+amount)

				# Update the text
				self.ProgressText.SetLabel("%s of %s" % \
					(self.ProgressGauge.GetValue(), self.ProgressGauge.GetRange()))
				
			elif state == "finished":
				# Change to the tick
				animation.LoadFile(okay)
				animation.Play()
				
				# Set the gauge as completed!
				self.ProgressGauge.SetValue(self.ProgressGauge.GetRange())

				# Set the progress text
				self.ProgressText.SetLabel("Done!")

				# Stop the progress animation
				self.ProgressAnim.Stop()

		if len(message) > 0:
			self.Message.AppendText(message+"\n")
		self.Panel.Layout()
		self.GoDown = True

		if state == "failure":
			# Don't do anything for now
			end = self.Message.GetLastPosition()
			self.Message.SetStyle(end-len(message)-1, end, wx.TextAttr(wx.RED))


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

