"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
import random

# wxPython imports
import wx
import wx.gizmos

# Local imports
from winBase import *
from utils import *

NAME = 0
DESC = 1


# Show the universe
class winDesign(winBase):
	title = _("Design")
	
	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		panel = wx.Panel(self, -1)


		grid = wx.FlexGridSizer(2, 3, 0, 0)
		grid.AddGrowableCol(1)		# Middle Column is growable
		grid.AddGrowableRow(1)		# Bottom row is growable

		# The hulls which are avalible
		self.hullscat 	= wx.ComboBox(panel, -1, "", wx.DefaultPosition, wx.Size(90, 50), [], wx.CB_DROPDOWN)
		self.hulls 		= wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_NO_HEADER|wx.SUNKEN_BORDER )

		# The currently selected plan
		top_sizer = wx.BoxSizer( wx.VERTICAL ) # The buttons
		self.plan  = wx.Panel(panel, -1)
		
		# The components
		self.compscat 	= wx.ComboBox(panel, -1, "", wx.DefaultPosition, wx.Size(90, 50), [], wx.CB_DROPDOWN)
		self.comps		= wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.LC_NO_HEADER|wx.SUNKEN_BORDER )


		# The duplicate button

		# The title

		# The number of uses

		# The delete button

		
		grid.AddWindow(self.hullscat, 	0, wx.GROW|wx.ALIGN_CENTRE, 1 )
		grid.AddSizer(top_sizer, 		0, wx.GROW|wx.ALIGN_CENTRE, 1 )
		grid.AddWindow(self.compscat,	0, wx.GROW|wx.ALIGN_CENTRE, 1 )
		grid.AddWindow(self.hulls, 		0, wx.GROW|wx.ALIGN_CENTRE, 1 )
		grid.AddWindow(self.plan, 		0, wx.GROW|wx.ALIGN_CENTRE, 1 )
		grid.AddWindow(self.comps, 		0, wx.GROW|wx.ALIGN_CENTRE, 1 )

		panel.SetAutoLayout(True)
		panel.SetSizer( grid )

		grid.Fit( panel )
		grid.SetSizeHints( panel )


