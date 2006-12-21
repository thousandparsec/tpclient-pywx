
# Python imports
import string
import os.path

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBaseXRC
from xrc.winUpdate import winUpdateBase

throbber = os.path.join("graphics", "throbber.gif")
okay = os.path.join("graphics", "tick.gif")

class winUpdate(winUpdateBase, winMainBaseXRC):
	title = _("Updating")
	
	def __init__(self, application):
		winUpdateBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)

	def Clear(self):
		self.TopText.SetLabel("")
		self.Message.SetLabel("")

		self.ConnectingGauge.SetRange(1)
		self.ConnectingGauge.SetValue(0)

		self.ConnectingAnim.LoadFile(throbber)
		self.ConnectingAnim.Stop()

		self.ConnectingText.SetLabel("")

		self.ProgressTitle.SetLabel("")

		self.ProgressGauge.SetRange(1)
		self.ProgressGauge.SetValue(0)

		self.ProgressAnim.LoadFile(throbber)
		self.ProgressAnim.Stop()

		self.ProgressText.SetLabel("")

		self.ObjectsAnim.LoadFile(throbber)
		self.ObjectsAnim.Stop()

		self.OrdersAnim.LoadFile(throbber)
		self.OrdersAnim.Stop()

		self.BoardsAnim.LoadFile(throbber)
		self.BoardsAnim.Stop()

		self.MessagesAnim.LoadFile(throbber)
		self.MessagesAnim.Stop()

		self.CategoriesAnim.LoadFile(throbber)
		self.CategoriesAnim.Stop()

		self.DesignsAnim.LoadFile(throbber)
		self.DesignsAnim.Stop()

		self.ComponentsAnim.LoadFile(throbber)
		self.ComponentsAnim.Stop()

		self.PropertiesAnim.LoadFile(throbber)
		self.PropertiesAnim.Stop()

		self.PlayersAnim.LoadFile(throbber)
		self.PlayersAnim.Stop()

		self.ResourcesAnim.LoadFile(throbber)
		self.ResourcesAnim.Stop()

	def Show(self, show=True):
		if not show:
			return self.Hide()
		
		# Clear everything
		self.Clear()

		return winMainBaseXRC.Show(self)

	def Update(self, mode, state, message="", todownload=None, total=None, amount=None):
		# We do a little bit different for this mode
		if mode == "connecting":
			return
		
		animation = getattr(self, "%sAnim" % mode.title())
		if state == "start":
			# Set the progress title
			self.ProgressTitle.SetLabel("Getting %s" % mode.title())

			# Set the progress guage to be empty
			self.ProgressGauge.SetValue(0)
			self.ProgressGauge.SetRange(1)
			
			# Set the progress text
			self.ProgressText.SetLabel("")

			# Start the throbber for this mode
			animation.LoadFile(throbber)
			animation.Play()

		elif state == "todownload":
			# Now we know how big to set the gauge too
			if todownload == 0:
				todownload = 1
			
			self.ProgressGauge.SetRange(todownload)

		elif state == "progress":
			# Nothing to do...
			pass

		elif state == "failure":
			# Don't do anything for now
			# FIXME: Should highlight the line in red....
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

		self.Message.SetValue(message + "\n" + self.Message.GetValue())

		self.Panel.Layout()

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
