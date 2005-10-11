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
	
	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		self.application = application

	def Show(self, show=True):
		winBase.Show(self, show)
		if not show:
			self.panel.Destory()
			return

		panel = wx.Panel(self, -1)
		sizer = wx.FlexGridSizer(1, 1, 0, 0)
		sizer.AddGrowableCol(0)
		sizer.AddGrowableRow(0)

		self.application.gui.current.ConfigDisplay(panel, sizer)

		panel.SetAutoLayout( True )
		panel.SetSizer( sizer )	
		sizer.Fit( panel )
		sizer.SetSizeHints( panel )

		panel.Layout()

		self.panel = panel

