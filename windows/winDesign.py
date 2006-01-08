"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports

# wxPython imports
import wx
import wx.gizmos

# Local imports
from winBase import *
from utils import *

NAME = 0
DESC = 1

COL_SIZE=150

# Show the universe
class winDesign(winReportBase):
	title = _("Design")
	
	from defaults import winDesignDefaultPosition as DefaultPosition
	from defaults import winDesignDefaultSize as DefaultSize
	from defaults import winDesignDefaultShow as DefaultShow

	modes = ["Select", "Edit"]

	def __init__(self, application, parent):
		winReportBase.__init__(self, application, parent)

		panel = wx.Panel(self, -1)

		self.grid = wx.FlexGridSizer(2, 3, 0, 0)
		self.grid.AddGrowableCol(1)		# Middle Column is growable
		self.grid.AddGrowableRow(1)		# Bottom row is growable

		# The designs which are avalible
		self.designscat = wx.Choice( panel, -1, choices=[], size=(COL_SIZE,wx.local.buttonSize[1]))
		self.designscat.SetFont(wx.local.normalFont)
		self.designscat.Bind(wx.EVT_CHOICE, self.UpdateDesignList)
		self.designs = wx.ListCtrl( panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_NO_HEADER|wx.SUNKEN_BORDER )
		self.designs.SetFont(wx.local.normalFont)

		# The labels
		################################################################
		self.top = wx.BoxSizer( wx.HORIZONTAL )
		
		# The title (editable version)
		self.titleedit = wx.TextCtrl( panel, -1, "Title", size=(-1,wx.local.buttonSize[1]), style=wx.TE_CENTRE)
		self.titleedit.SetFont(wx.local.normalFont)
		self.top.Add( self.titleedit, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The title (noneditable version)
		self.titletext = wx.StaticText( panel, -1, "Title", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
		self.titletext.SetFont(wx.local.normalFont)
		self.top.Add( self.titletext, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1)

		# The number of times the design is in use
		self.used = wx.StaticText( panel, -1, "0000", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
		self.used.SetFont(wx.local.normalFont)
		self.top.Add( self.used, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		self.middle = wx.BoxSizer( wx.VERTICAL )
		
		# The categories this design is in
		self.categories = wx.StaticText( panel, -1, "", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
		self.categories.SetFont(wx.local.normalFont)
		self.middle.Add( self.categories, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 0 )
		
		# The currently selected design
		self.design = wx.BoxSizer( wx.HORIZONTAL )
		self.middle.Add(self.design, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The components in the design
		self.parts = wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_EDIT_LABELS )
		self.parts.InsertColumn(0, "#", format=wx.LIST_FORMAT_RIGHT, width=20)
		self.parts.InsertColumn(1, "Component")
		self.parts.SetFont(wx.local.normalFont)
		self.design.Add(self.parts, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The properties of the design
		self.design_ps = wx.BoxSizer(wx.HORIZONTAL)
		self.design_pp = wx.Panel(panel, -1)
		self.design_pp.SetSizer(self.design_ps)
		self.design.Add(self.design_pp, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The description of the current design
		#self.desc = wx.TextCtrl( panel, -1, " ", style=wx.TE_RIGHT|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		#self.desc.SetFont(wx.local.normalFont)
		#self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The "component description panel"
		#self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

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
		self.compscat = wx.Choice( panel, -1, choices=[], size=(COL_SIZE,wx.local.buttonSize[1]))
		self.compscat.SetFont(wx.local.normalFont)
		self.compscat.Bind(wx.EVT_CHOICE, self.UpdateCompList)
		self.comps = wx.ListCtrl( panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_LIST|wx.LC_NO_HEADER|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL )
		self.comps.SetFont(wx.local.normalFont)

		self.grid.Add(self.designscat, 	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.top, 		0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.compscat,	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.designs, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.middle, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.comps, 	0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

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
		self.grid.Show(self.compscat)
		self.grid.Show(self.comps)
		
		# Make the title and description editable
		self.top.Show(self.titleedit)
		self.top.Hide(self.titletext)

		# Disable edit, duplicate, delete
		self.edit.Disable()
		self.duplicate.Disable()
		self.delete.Disable()

		# Enable the save, revert
		self.revert.Enable()
		self.revert.SetDefault()
		self.save.Enable()

		# Re-layout everything
		self.grid.Layout()

	def OnSelect(self, evt=None):
		# Enable the selection side
		self.designscat.Enable()
		self.designs.Enable()

		# Hide the component bar
		self.grid.Hide(self.compscat)
		self.grid.Hide(self.comps)

		# Make the title and description uneditable
		self.top.Hide(self.titleedit)
		self.top.Show(self.titletext)
		self.top.Layout()

		# Disable save, revert
		self.revert.Disable()
		self.save.Disable()

		# Re-layout everything
		self.grid.Layout()

		self.OnSelectObject()

	def BuildPropertiesPanel(self, design):
		SIZER_FLAGS = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL
		cache = self.application.cache

		# Remove the previous panel and stuff
		if hasattr(self, 'properties'):
			self.properties.Hide()
			self.design_ps.Remove(self.properties)
			self.properties.Destroy()
			del self.properties

		# Create a new panel
		panel = wx.Panel(self.design_pp, -1)
		sizer = wx.BoxSizer(wx.VERTICAL) 
		panel.SetSizer(sizer)

		# Sort the properties into category groups
		properties = {}
		for pid, pstring in design.properties:
			property = cache.properties[pid]
			
			for cid in property.categories:
				if not properties.has_key(cid):
					properties[cid] = []
				properties[cid].append((property, pstring))
				
		for cid in properties.keys():
			category = cache.categories[cid]

			# The box around the properties in the category
			box = wx.StaticBox(panel, -1, category.name)
			box.SetFont(wx.local.normalFont)
			box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
			sizer.Add(box_sizer, 1, SIZER_FLAGS, 5)

			# The properties
			prop_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
			box_sizer.Add(prop_sizer, 1, SIZER_FLAGS, 5)

			for property, pstring in properties[cid]:
				# Property name
				name = wx.StaticText(panel, -1, property.display_name)
				name.SetFont(wx.local.normalFont)
				prop_sizer.Add(name, 0, SIZER_FLAGS|wx.ALIGN_RIGHT, 5)

				# Property value
				value = wx.StaticText(panel, -1, pstring)
				value.SetFont(wx.local.normalFont)
				prop_sizer.Add(value, 1, SIZER_FLAGS|wx.ALIGN_RIGHT, 5)

		self.design_ps.Add( panel, 1, SIZER_FLAGS, 5 )
		self.design_ps.Layout()

		self.properties = panel

	def OnSelectObject(self, evt=None):
		s = self.designs.GetSelected()
		if len(s) > 0:
			id = self.designs.GetItemData(s[0])
		else:
			id = -1

		if not id or id == -1:
			# Clear the title
			self.titletext.SetLabel("")

			# Hide the design
			self.middle.Hide(self.design)
			self.middle.Layout()
			
			# Disable the buttons
			self.edit.Disable()
			self.duplicate.Disable()
			self.delete.Disable()
			return
		
		design = self.application.cache.designs[id]

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

		# Enable the parts list
		self.middle.Show(self.design)

		# Populate the parts list
		self.parts.DeleteAllItems()
		for id, number in design.components:
			component = self.application.cache.components[id]
		
			self.parts.InsertStringItem(0, str(number))
			self.parts.SetStringItem(0, 1, component.name)
		
		# Populate the properties
		self.BuildPropertiesPanel(design)

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
		
		# Re-layout everything
		self.grid.Layout()

	def OnCacheUpdate(self, evt=None):
		print "OnCacheUpdate of winDesign..."

		# Update the categories
		if self.designscat.GetSelection() == -1:
			designs = 0
		else:
			designs = self.designscat.GetClientData(self.designscat.GetSelection())
		if self.compscat.GetSelection() == -1:
			comps = 0
		else:
			comps = self.compscat.GetClientData(self.compscat.GetSelection())
		
		self.designscat.Clear()
		self.compscat.Clear()
		for category in self.application.cache.categories.values():
			slot = self.designscat.GetCount()

			for design in self.application.cache.designs.values():
				if category.id in design.categories:
					self.designscat.Append(category.name, category.id)
					break

			for component in self.application.cache.components.values():
				if category.id in component.categories:
					self.compscat.Append(category.name, category.id)
					break

			self.designscat.SetToolTipItem(slot, category.description)
			self.compscat.SetToolTipItem(slot, category.description)

			if category.id == designs:
				self.designscat.SetSelection(slot)

			if category.id == comps:
				self.compscat.SetSelection(slot)

		self.UpdateDesignList()
		self.UpdateCompList()

	def UpdateDesignList(self, evt=None):
		print "Updating the Designs List"
		
		if self.designscat.GetSelection() == -1:
			des = 0
		else:
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
		if self.compscat.GetSelection() == -1:
			comps = 0
		else:
			comps = self.compscat.GetClientData(self.compscat.GetSelection())
		print "Currently selected category", comps

		self.comps.ClearAll()
		for component in self.application.cache.components.values():
			slot = self.comps.GetItemCount()

			print "Component", component.id, component.name, component.categories
			if comps in component.categories:
				print "Adding to ", slot
				self.comps.InsertStringItem(slot, component.name)
				self.comps.SetItemData(slot, component.id)

