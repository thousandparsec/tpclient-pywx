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
		self.hullscat = wx.Choice(panel, -1, choices=[], size=(-1,wx.local.buttonSize[1]))
		self.hullscat.SetFont(wx.local.normalFont)
		self.hullscat.Bind(wx.EVT_CHOICE, self.UpdateHullList)
		self.hulls = wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_NO_HEADER|wx.SUNKEN_BORDER )
		self.hulls.SetFont(wx.local.normalFont)

		top_sizer = wx.BoxSizer( wx.HORIZONTAL ) # The buttons
		
		# The title
		self.title = wx.TextCtrl( panel, -1, "Title", wx.DefaultPosition, (-1,wx.local.buttonSize[1]), wx.TE_RIGHT)
		self.title.SetFont(wx.local.normalFont)
		top_sizer.AddWindow( self.title, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The number of uses
		self.uses = wx.StaticText( panel, -1, "12", size=(-1,wx.local.buttonSize[1]))
		self.uses.SetFont(wx.local.normalFont)
		top_sizer.AddWindow( self.uses, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		middle_sizer = wx.BoxSizer( wx.VERTICAL )
		
		# The currently selected plan
		self.plan = wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.SUNKEN_BORDER )
		self.plan.SetFont(wx.local.normalFont)
		middle_sizer.AddWindow(self.plan, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The buttons
		bottom_sizer = wx.BoxSizer( wx.HORIZONTAL )
		middle_sizer.AddSizer(bottom_sizer, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )

		# The duplicate button
		duplicate = wx.Button( panel, -1, _("Duplicate"), size=wx.local.buttonSize)
		duplicate.SetFont(wx.local.normalFont)
		bottom_sizer.AddWindow( duplicate, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The delete button
		delete = wx.Button( panel, -1, _("Delete"), size=wx.local.buttonSize)
		delete.SetFont(wx.local.normalFont)
		bottom_sizer.AddWindow( delete, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The revert button
		revert = wx.Button( panel, -1, _("Revert"), size=wx.local.buttonSize)
		revert.SetFont(wx.local.normalFont)
		bottom_sizer.AddWindow( revert, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The save button
		save = wx.Button( panel, -1, _("Save"), size=wx.local.buttonSize)
		save.SetFont(wx.local.normalFont)
		save.SetDefault()
		bottom_sizer.AddWindow( save, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The components
		self.compscat = wx.Choice(panel, -1, choices=[], size=(-1,wx.local.buttonSize[1]))
		self.compscat.SetFont(wx.local.normalFont)
		self.compscat.Bind(wx.EVT_CHOICE, self.UpdateCompList)
		self.comps = wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_NO_HEADER|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL )
		self.comps.SetFont(wx.local.normalFont)

		self.compscat.Hide()
		self.comps.Hide()
		
		grid.AddWindow(self.hullscat, 	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		grid.AddSizer(top_sizer, 		0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		grid.AddWindow(self.compscat,	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		grid.AddWindow(self.hulls, 		0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		grid.AddSizer(middle_sizer, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		grid.AddWindow(self.comps, 		0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		panel.SetAutoLayout( True )
		panel.SetSizer( grid )

		grid.Fit( panel )
		grid.SetSizeHints( panel )

		self.mode = "select"


	def OnCacheUpdate(self, evt=None):
		print "OnCacheUpdate of winDesign..."

		# Update the categories
		hulls = self.hullscat.GetClientData(self.hullscat.GetSelection())
		comps = self.compscat.GetClientData(self.compscat.GetSelection())
		
		self.hullscat.Clear()
		self.compscat.Clear()
		for category in self.application.cache.categories.values():
			slot = self.hullscat.GetCount()

			self.hullscat.Append(category.name, category.id)
			self.compscat.Append(category.name, category.id)

			self.hullscat.SetToolTipItem(slot, category.desc)
			self.compscat.SetToolTipItem(slot, category.desc)

			if category.id == hulls:
				self.hullscat.SetSelection(slot)

			if category.id == comps:
				self.compscat.SetSelection(slot)

		self.UpdateHullList()
		self.UpdateCompList()

	def UpdateHullList(self, evt=None):
		print "Updating the Hulls List"
		# Update the 
		hulls = self.hullscat.GetClientData(self.hullscat.GetSelection())
		print "Currently selected category", hulls

		self.hulls.ClearAll()
		for component in self.application.cache.components.values():
			slot = self.hulls.GetItemCount()

			print "Component", component.name, component.types
			if hulls in component.types:
				self.hulls.InsertStringItem(slot, component.name)
				self.hulls.SetItemData(slot, component.id)

#			if category.id == hulls:
#				self.hulls.SetSelected(slot)

	def UpdateCompList(self, evt=None):
		print "Updating the Comps List"
		comps = self.compscat.GetClientData(self.compscat.GetSelection())
		print "Currently selected category", comps

		self.comps.ClearAll()
		for component in self.application.cache.components.values():
			slot = self.comps.GetItemCount()

			print "Component", component.name, component.types
			if comps in component.types:
				print "Adding to ", slot
				self.comps.InsertStringItem(slot, component.name)
				self.comps.SetItemData(slot, component.id)

#			if category.id == comps:
#				self.comps.SetSelected(slot)

