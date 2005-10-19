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
	
	from defaults import winDesignDefaultPosition as DefaultPosition
	from defaults import winDesignDefaultSize as DefaultSize
	from defaults import winDesignDefaultShow as DefaultShow

	modes = ["Select", "Edit"]

	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		panel = wx.Panel(self, -1)

		self.grid = wx.FlexGridSizer(2, 3, 0, 0)
		self.grid.AddGrowableCol(1)		# Middle Column is growable
		self.grid.AddGrowableRow(1)		# Bottom row is growable

		# The designs which are avalible
		self.designscat = wx.Choice( panel, -1, choices=[], size=(-1,wx.local.buttonSize[1]))
		self.designscat.SetFont(wx.local.normalFont)
		self.designscat.Bind(wx.EVT_CHOICE, self.UpdateDesignList)
		self.designs = wx.ListCtrl( panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_NO_HEADER|wx.SUNKEN_BORDER )
		self.designs.SetFont(wx.local.normalFont)

		self.top = wx.BoxSizer( wx.HORIZONTAL ) # The labels
		
		# The title
		self.titleedit = wx.TextCtrl( panel, -1, "Title", size=(-1,wx.local.buttonSize[1]), style=wx.TE_CENTRE)
		self.titleedit.SetFont(wx.local.normalFont)
		self.top.Add( self.titleedit, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		self.titletext = wx.StaticText( panel, -1, "Title", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
		self.titletext.SetFont(wx.local.normalFont)
		self.top.Add( self.titletext, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1)

		# The number of uses
		self.used = wx.StaticText( panel, -1, "0000", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
		self.used.SetFont(wx.local.normalFont)
		self.top.Add( self.used, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		self.middle = wx.BoxSizer( wx.VERTICAL )
		
		# The categories this component is in
		self.categories = wx.StaticText( panel, -1, "", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
		self.categories.SetFont(wx.local.normalFont)
		self.middle.Add( self.categories, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 0 )
		
		# The currently selected plan
		self.plan = wx.ListCtrl( panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_EDIT_LABELS )
		self.plan.InsertColumn(0, "#", format=wx.LIST_FORMAT_RIGHT, width=20)
		self.plan.InsertColumn(1, "Component")
		self.plan.SetFont(wx.local.normalFont)
		
		self.middle.Add(self.plan, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
	
		# The description...
		self.desc = wx.TextCtrl( panel, -1, " ", style=wx.TE_RIGHT|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		self.desc.SetFont(wx.local.normalFont)
		self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The buttons
		self.buttons = wx.BoxSizer( wx.HORIZONTAL )
		self.middle.Add(self.buttons, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )

		# The edit button
		self.edit = wx.Button( panel, -1, _("Edit"), size=wx.local.buttonSize)
		self.edit.SetFont(wx.local.normalFont)
		self.buttons.Add( self.edit, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The duplicate button
		self.duplicate = wx.Button( panel, -1, _("Duplicate"), size=wx.local.buttonSize)
		self.duplicate.SetFont(wx.local.normalFont)
		self.buttons.Add( self.duplicate, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The delete button
		self.delete = wx.Button( panel, -1, _("Delete"), size=wx.local.buttonSize)
		self.delete.SetFont(wx.local.normalFont)
		self.buttons.Add( self.delete, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The revert button
		self.revert = wx.Button( panel, -1, _("Revert"), size=wx.local.buttonSize)
		self.revert.SetFont(wx.local.normalFont)
		self.buttons.Add( self.revert, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The save button
		self.save = wx.Button( panel, -1, _("Save"), size=wx.local.buttonSize)
		self.save.SetFont(wx.local.normalFont)
		self.buttons.Add( self.save, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The components
		self.partscat = wx.Choice( panel, -1, choices=[], size=(-1,wx.local.buttonSize[1]))
		self.partscat.SetFont(wx.local.normalFont)
		self.partscat.Bind(wx.EVT_CHOICE, self.UpdateCompList)
		self.parts = wx.ListCtrl( panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_NO_HEADER|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL )
		self.parts.SetFont(wx.local.normalFont)

		self.grid.Add(self.designscat, 	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.top, 		0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.partscat,	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.designs, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.middle, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.parts, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		panel.SetAutoLayout( True )
		panel.SetSizer( self.grid )

		self.grid.Fit( panel )
		self.grid.SetSizeHints( self )

		self.Bind(wx.EVT_BUTTON, self.OnEdit, self.edit)
		self.Bind(wx.EVT_BUTTON, self.OnSelect, self.revert)

		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelectObject, self.designs)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelectObject, self.designs)

		self.panel = panel
		self.OnSelect()

	def OnEdit(self, evt=None):
		# Disable the select side
		self.designscat.Disable()
		self.designs.Disable()

		# Show the component bar
		self.grid.Show(self.partscat)
		self.grid.Show(self.parts)
		self.grid.Layout()
		
		# Make the title and description editable
		self.top.Show(self.titleedit)
		self.top.Hide(self.titletext)
		self.top.Layout()

#		self.middle.Show(self.descedit)
#		self.middle.Hide(self.desc)
#		self.middle.Layout()

		# Disable edit, duplicate, delete
		self.edit.Disable()
		self.duplicate.Disable()
		self.delete.Disable()

		# Enable the save, revert
		self.revert.Enable()
		self.revert.SetDefault()
		self.save.Enable()

	def OnSelect(self, evt=None):
		# Enable the selection side
		self.designscat.Enable()
		self.designs.Enable()

		# Hide the component bar
		self.grid.Hide(self.partscat)
		self.grid.Hide(self.parts)
		self.grid.SetSizeHints( self.panel )
		self.grid.Layout()
#		self.grid.Fit( self.panel )

		# Make the title and description uneditable
		self.top.Hide(self.titleedit)
		self.top.Show(self.titletext)
		self.top.Layout()

#		self.middle.Hide(self.descedit)
#		self.middle.Show(self.desc)
#		self.middle.Layout()

		# Disable save, revert
		self.revert.Disable()
		self.save.Disable()

		self.OnSelectObject()

	def OnSelectObject(self, evt=None):
		s = self.designs.GetSelected()
		if len(s) > 0:
			id = self.designs.GetItemData(s[0])
		else:
			id = -1

		if not id or id == -1:
			# Clear the title
			self.titletext.SetLabel("")

			# Hide the plan
			self.middle.Hide(self.plan)
			self.middle.Layout()
			
			# Set the description
			self.desc.SetValue("No component selected...")
		
			# Disable the buttons
			self.edit.Disable()
			self.duplicate.Disable()
			self.delete.Disable()
			return
		
		design = self.application.cache.designs[id]
		
		# Enable the parts list
		self.middle.Show(self.plan)

		# Populate the parts list
		for number, id in design.components:
			pass
			
		self.middle.Layout()

		# Set the title
		self.titletext.SetLabel(design.name)
		self.titleedit.SetValue(design.name)

		# Set the used
		self.used.SetLabel(str(design.used))
		if design.used == -1:
			self.used.SetForegroundColour(wx.Color(255, 0, 0))
		elif design.used == 0:
			self.used.SetForegroundColour(wx.Color(0, 255, 0))
		else:
			self.used.SetForegroundColour(wx.Color(0, 0, 0))

		# Set the categories
		c = ""
		for id in design.categories:
			c += self.application.cache.categories[id].name + ", "
		c = c[:-2]
		self.categories.SetLabel(c)

		# Set the description
		self.desc.SetValue(str(design.description))

		# Set if edit can work
		if design.used <= 0:
			self.edit.Enable()
			self.edit.SetDefault()

			self.duplicate.Enable()
			self.delete.Enable()
		else:
			self.edit.Disable()
			self.delete.Disable()

			self.duplicate.Enable()
			self.duplicate.SetDefault()

	def OnCacheUpdate(self, evt=None):
		return
		print "OnCacheUpdate of winDesign..."

		# Update the categories
		designs = self.designscat.GetClientData(self.designscat.GetSelection())
		comps = self.partscat.GetClientData(self.partscat.GetSelection())
		
		self.designscat.Clear()
		self.partscat.Clear()
		for category in self.application.cache.categories.values():
			slot = self.designscat.GetCount()

			self.designscat.Append(category.name, category.id)
			self.partscat.Append(category.name, category.id)

			self.designscat.SetToolTipItem(slot, category.description)
			self.partscat.SetToolTipItem(slot, category.description)

			if category.id == designs:
				self.designscat.SetSelection(slot)

			if category.id == comps:
				self.partscat.SetSelection(slot)

		self.UpdateDesignList()
		self.UpdateCompList()

	def UpdateDesignList(self, evt=None):
		print "Updating the Designs List"
		
		des = self.designscat.GetClientData(self.designscat.GetSelection())
		print "Currently selected category", des

		self.designs.ClearAll()
		for design in self.application.cache.designs.values():
			slot = self.designs.GetItemCount()

			print "Design", design.id, design.name, design.categories
			if des in design.categories:
				print "Adding to ", slot
				self.designs.InsertStringItem(slot, design.name)
				self.designs.SetItemData(slot, design.id)

	def UpdateCompList(self, evt=None):
		print "Updating the Comps List"
		comps = self.partscat.GetClientData(self.partscat.GetSelection())
		print "Currently selected category", comps

		self.parts.ClearAll()
		for component in self.application.cache.components.values():
			slot = self.parts.GetItemCount()

			print "Component", component.id, component.name, component.categories
			if comps in component.categories:
				print "Adding to ", slot
				self.parts.InsertStringItem(slot, component.name)
				self.parts.SetItemData(slot, component.id)

