
# Python imports
import string

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBaseXRC
from xrc.winUpdate import winUpdateBase

class winUpdate(winUpdateBase, winMainBaseXRC):
	title = _("Updating")
	
	def __init__(self, application):
		winUpdateBase.__init__(self, None)
		winMainBaseXRC.__init__(self, application)

		self.Bind(wx.EVT_IDLE, self.IdleHandler)

	def Show(self, show=True):
		if not show:
			return self.Hide()
		
		# Clear everything
		self.overall.SetLabel("")
		
		for gauge, text in (self.connecting, self.objects, self.order_descs, self.boards, self.designs, self.players, self.remaining):
			gauge.SetValue(0)
			if hasattr(gauge, 'GetRange'):
				gauge.SetRange(0)
			text.SetLabel("")
		
		return winMainBaseXRC.Show(self)

	def IdleHandler(self, event):
		active = None
		if hasattr(active, 'GetMax'):
			count = active.GetValue()
			if count >= active.GetMax():
				self.more = -1
			if count <= active.GetMin():
				self.more = 1

			active.SetValue(count + self.more)
	
	def Update(self, text, mode=None, add=None, of=None):
		self.overall.SetLabel(text)
		
		if mode and getattr(self, mode) != self.mode:
			self.active = None
			
			slider, text = self.mode
			if hasattr(slider, 'GetMax'):
				max = slider.GetMax()
			elif hasattr(slider, 'GetRange'):
				max = slider.GetRange()
			slider.SetValue(max)
			text.SetLabel("Done!")
			
			self.mode = getattr(self, mode)
		
		slider, text = self.mode
		
		if hasattr(slider, 'GetRange'):
			if isinstance(of, long):
				slider.SetRange(of)

			if add and slider.GetValue()+add < slider.GetRange():
				slider.SetValue(slider.GetValue()+add)

			if of != None or add:
				text.SetLabel("%s of %s" % (slider.GetValue(), slider.GetRange()))
		else:
			self.active = slider

		self.sizer.Layout()

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
