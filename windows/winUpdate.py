
# Python imports
import string

# wxPython Imports
import wx

# Local Imports
from winBase import winMainBase

class winUpdate(winMainBase):
	title = _("Updating")
	
	def __init__(self, application):
		winMainBase.__init__(self, application)

		# FIXME: We shouldn't need active anymore
		self.active = None

		panel = wx.Panel(self, -1)
		self.overall = wx.StaticText(panel, -1, "", style=wx.ALIGN_CENTER)

	   	self.connecting = (wx.Slider(panel, -1, 0, 0, 600, style=wx.SL_HORIZONTAL), wx.StaticText(panel, -1, ""))
		self.connecting[0].Disable()
		self.objects = (wx.Gauge(panel, -1, 1), wx.StaticText(panel, -1, ""))
		self.boards = (wx.Gauge(panel, -1, 1), wx.StaticText(panel, -1, ""))
		self.order_descs = (wx.Gauge(panel, -1, 1), wx.StaticText(panel, -1, ""))
		self.designs = (wx.Gauge(panel, -1, 4), wx.StaticText(panel, -1, ""))
		self.players = (wx.Gauge(panel, -1, 4), wx.StaticText(panel, -1, ""))
	   	self.remaining = (wx.Slider(panel, -1, 0, 0, 600, style=wx.SL_HORIZONTAL), wx.StaticText(panel, -1, ""))
		self.remaining[0].Disable()
	
		self.mode = self.connecting

		grid = wx.FlexGridSizer( 0, 2, 2, 10 )
		grid.AddGrowableCol(0)
		
		grid.Add( self.connecting[0], 0, wx.ALIGN_CENTER|wx.EXPAND , 5 )
		grid.Add( self.connecting[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.objects[0], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.objects[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.boards[0], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.boards[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.order_descs[0], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.order_descs[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.designs[0], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.designs[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.players[0], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.players[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.remaining[0], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		grid.Add( self.remaining[1], 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )

		sizer = wx.BoxSizer( wx.VERTICAL )
		sizer.AddSpacer(wx.Size(-1, 5))
		sizer.Add( self.overall, 0, wx.ALIGN_CENTER, 5 )
		sizer.AddSpacer(wx.Size(-1, 5))
		sizer.Add( grid, 0, wx.ALIGN_CENTER|wx.EXPAND, 5 )
		self.sizer = sizer

		# Join the panel and the base sizer
		panel.SetAutoLayout( True )
		panel.SetSizer( sizer )
		sizer.Fit( panel )
		sizer.SetSizeHints( self )

		self.SetSize(wx.Size(640, -1))
		self.CenterOnScreen()

		self.Bind(wx.EVT_IDLE, self.IdleHandler)

	def Show(self, show=True):
		print "winUpdate show"
		if not show:
			return self.Hide()
		
		# Clear everything
		self.overall.SetLabel("")
		
		for gauge, text in (self.connecting, self.objects, self.order_descs, self.boards, self.designs, self.players, self.remaining):
			gauge.SetValue(0)
			if hasattr(gauge, 'GetRange'):
				gauge.SetRange(0)
			text.SetLabel("")
		
		print "winUpdate Show - end"
		return winMainBase.Show(self)

	def IdleHandler(self, event):
		active = self.mode[0]
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

			if add:
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
