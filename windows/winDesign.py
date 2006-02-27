"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
from types import TupleType
from copy import deepcopy

# wxPython imports
import wx
import wx.gizmos

# Local imports
from winBase import *
from utils import *

from tp.client.parser import DesignCalculator
from tp.netlib.objects import Design

NAME = 0
DESC = 1

COL_SIZE=150

Art = wx.ArtProvider_GetBitmap
wx.ArtSize = (16, 16)

# Show the universe
class winDesign(winReportBase, winShiftMixIn):
	title = _("Design")
	
	from defaults import winDesignDefaultPosition as DefaultPosition
	from defaults import winDesignDefaultSize as DefaultSize
	from defaults import winDesignDefaultShow as DefaultShow

	modes = ["Select", "Edit"]

	def __init__(self, application, parent):
		winReportBase.__init__(self, application, parent)
		winShiftMixIn.__init__(self)

		panel = wx.Panel(self, -1)
		
		self.icons = wx.ImageList(*wx.ArtSize)
		self.icons.Add(Art(wx.ART_FOLDER, wx.ART_OTHER, wx.ArtSize))
		self.icons.Add(Art(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.ArtSize))
		self.icons.Add(Art(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.ArtSize))

		self.grid = wx.FlexGridSizer(2, 3, 0, 0)
		self.grid.AddGrowableCol(0, 15)		# Middle Column is growable
		self.grid.AddGrowableCol(1, 50)		# Middle Column is growable
		self.grid.AddGrowableCol(2, 15)		# Middle Column is growable
		self.grid.AddGrowableRow(1)			# Bottom row is growable

		self.designs = wx.OrderedTreeCtrl( panel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
		self.designs.SetFont(wx.local.normalFont)
		self.designs.SetImageList(self.icons)

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
		self.designsizer = wx.BoxSizer( wx.HORIZONTAL )
		self.middle.Add(self.designsizer, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The components in the design
		self.parts = wx.ListCtrl(panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_EDIT_LABELS )
		self.parts.InsertColumn(0, "#", format=wx.LIST_FORMAT_RIGHT, width=20)
		self.parts.InsertColumn(1, "Component")
		self.parts.SetFont(wx.local.normalFont)
		self.designsizer.Add(self.parts, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The properties of the design
		self.design_ps = wx.BoxSizer(wx.HORIZONTAL)
		self.design_pp = wx.Panel(panel, -1)
		self.design_pp.SetSizer(self.design_ps)
		self.designsizer.Add(self.design_pp, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The description of the current design
		#self.desc = wx.TextCtrl( panel, -1, " ", style=wx.TE_RIGHT|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		#self.desc.SetFont(wx.local.normalFont)
		#self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The "component description panel"
		#self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The buttons
		buttons = wx.BoxSizer( wx.HORIZONTAL )
		self.middle.Add(buttons, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )

		# The edit button
		self.edit = wx.Button( panel, -1, _("Edit"), size=wx.local.buttonSize)
		self.edit.SetFont(wx.local.normalFont)
		buttons.Add( self.edit, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The duplicate button
		self.duplicate = wx.Button( panel, -1, _("Duplicate"), size=wx.local.buttonSize)
		self.duplicate.SetFont(wx.local.normalFont)
		buttons.Add( self.duplicate, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The delete button
		self.delete = wx.Button( panel, -1, _("Delete"), size=wx.local.buttonSize)
		self.delete.SetFont(wx.local.normalFont)
		buttons.Add( self.delete, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The revert button
		self.revert = wx.Button( panel, -1, _("Revert"), size=wx.local.buttonSize)
		self.revert.SetFont(wx.local.normalFont)
		buttons.Add( self.revert, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The save button
		self.save = wx.Button( panel, -1, _("Save"), size=wx.local.buttonSize)
		self.save.SetFont(wx.local.normalFont)
		buttons.Add( self.save, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The components
		
		self.compssizer = wx.BoxSizer( wx.VERTICAL )
		
		self.comps = wx.OrderedTreeCtrl( panel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_MULTIPLE)
		self.comps.SetFont(wx.local.normalFont)
		self.comps.SetImageList(self.icons)
		self.compssizer.Add(self.comps, 1, wx.GROW|wx.ALIGN_RIGHT|wx.ALL, 1 )

		self.addsizer = wx.BoxSizer( wx.HORIZONTAL )
		self.compssizer.Add(self.addsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 0)

		self.add = wx.Button( panel, -1, _("Add"), size=wx.local.buttonSize)
		self.add.SetFont(wx.local.normalFont)
		self.addsizer.Add(self.add, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )

		self.addmany = wx.Button( panel, -1, _("Add Many"), size=wx.local.buttonSize)
		self.addmany.SetFont(wx.local.normalFont)
		self.addsizer.Add(self.addmany, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )
		
		blank = wx.Panel( panel, -1 )
		
		self.grid.Add(blank,    0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.top,         0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(blank,    0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.designs,     0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.middle,      0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		self.grid.Add(self.compssizer,  0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		panel.SetAutoLayout( True )
		panel.SetSizer( self.grid )

		self.grid.Fit( panel )
		self.grid.SetSizeHints( self )

		self.Bind(wx.EVT_BUTTON, self.OnEdit, self.edit)
		self.Bind(wx.EVT_BUTTON, self.OnSelect, self.revert)
		self.Bind(wx.EVT_BUTTON, self.OnSave, self.save)

		self.Bind(wx.EVT_BUTTON, self.OnAdd, self.add)
		self.Bind(wx.EVT_BUTTON, self.OnAddMany, self.addmany)

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectObject, self.designs)

		self.panel = panel
		self.OnSelect()

	def Change(self, cid, amount):
		"""\
		Changes the current design by adding/subtracting the certain amount of a component.
		"""
		design = self.design

		i = 0
		while True:
			if design.components[i][0] == cid:
				if type(design.components[i]) == TupleType:
					design.components[i] = list(design.components[i])
				design.components[i][1] += amount
	
				if design.components[i][1] < 0:
					del design.components[i]
				break
			
			i += 1
			
			if i >= len(design.components):
				design.components.append([cid, amount])
				break

	def Recalculate(self):
		"""\
		Recalculates the designs properties.
		"""
		design = self.design
		# Recalculate the design properties
		dc = DesignCalculator(self.application.cache, design)
		
		i, d = dc.calculate()
		okay, reason = dc.check(i, d)
		dc.apply(d, okay, reason) 

	def OnEdit(self, evt=None):
		# FIXME: Check if we can modify this Design.
	
		# Disable the select side
		self.designs.Disable()

		# Show the component bar
		self.grid.Show(self.compssizer)
		
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

		# Start the timer so that Add -> Add Many
		self.ShiftStart()

	def OnAddMany(self, evt):
		"""\
		Pops up a selection box to ask for how many to add.
		"""
		self.OnAdd(evt, amount)
	
	def OnAdd(self, evt, amount=1):
		"""\
		Adds components to the current design.
		"""
		# Figure out if a component is selected
		cids = []
		for tid in self.comps.GetSelections():
			cid = self.comps.GetPyData(tid)
			if not cid is None and cid >= 0:
				cids.append(cid)

		print "Adding", cids

		for cid in cids:
			# Add the componets to the design
			self.Change(cid, amount)
			
		self.Recalculate()
	
		if self.design.used == -1:
			if amount > 1 or len(cids) > 1:
				reason = self.design.feedback + """
Would you like to continue adding these components?"""
			else:
				reason = self.design.feedback + """
Would you like to continue adding this component?"""
			dlg = wx.MessageDialog(self, reason, 'Design Warning', wx.YES_NO|wx.NO_DEFAULT|wx.ICON_ERROR)
			
			if dlg.ShowModal() == wx.ID_NO:
				for cid in cids:
					self.Change(cid, -amount)
				self.Recalculate()

			dlg.Destroy()

		# Redisplay the panels
		self.BuildPartsPanel(self.design)
		self.BuildPropertiesPanel(self.design)

	def OnSave(self, evt):
		design = self.design

		# Create a cache event which updates that object
		self.application.Post(self.application.cache.CacheDirtyEvent("designs", "change", design.id, design))

		# FIXME: This should update the panel....
		self.OnSelect()

	def OnSelect(self, evt=None):
		# Stop any running Shift timers
		self.ShiftStop()
	
		# Enable the selection side
		self.designs.Enable()

		# Hide the component bar
		self.grid.Hide(self.compssizer)

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

	def OnSelectObject(self, evt=None):
		s = self.designs.GetSelection()

		if s < 0:
			self.design = None
		else:
			self.design = deepcopy(self.designs.GetPyData(s))
			if not isinstance(self.design, Design):
				self.design = None

		if self.design == None:
			# Clear the title
			self.titletext.SetLabel("")

			# Hide the design
			self.middle.Hide(self.designsizer)
			self.middle.Layout()
			
			# Disable the buttons
			self.edit.Disable()
			self.duplicate.Disable()
			self.delete.Disable()
			
			return

		# Recalculate all the properties if they are empty
		if len(self.design.properties) == 0:
			self.Recalculate()

		# Build the Header Panel
		self.BuildHeaderPanel(self.design)

		# Show the parts list
		self.middle.Show(self.designsizer)

		# Populate the parts list
		self.BuildPartsPanel(self.design)
		
		# Populate the properties
		self.BuildPropertiesPanel(self.design)

		# Set if edit can work
		if self.design.used <= 0:
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

	def BuildHeaderPanel(self, design):
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
		for cid in design.categories:
			c += self.application.cache.categories[cid].name + ", "
		c = c[:-2]
		self.categories.SetLabel(c)

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

	def BuildPartsPanel(self, design):
		# Populate the parts list
		self.parts.DeleteAllItems()
		for cid, number in design.components:
			component = self.application.cache.components[cid]
		
			self.parts.InsertStringItem(0, str(number))
			self.parts.SetStringItem(0, 1, component.name)

	def OnCacheUpdate(self, evt=None):
		print "OnCacheUpdate of winDesign..."

		self.UpdateDesignList()
		self.UpdateCompList()

	def UpdateDesignList(self, evt=None):
# FIXME: This is broken as it does not take into account the change of position of items
#		selected = self.designs.GetSelection()

		self.designs.DeleteAllItems()

		root = self.designs.AddRoot("Designs")
		self.designs.SetPyData(root, None)
		self.designs.SetItemImage(root, 0, wx.TreeItemIcon_Normal)
		self.designs.SetItemImage(root, 1, wx.TreeItemIcon_Expanded)

		child = self.designs.AppendItem(root, "Blank Design")
		self.designs.SetPyData(child, None)
		self.designs.SetItemImage(child, 2, wx.TreeItemIcon_Normal)

		cache = self.application.cache
		for category in cache.categories.values():
			child = self.designs.AppendItem(root, category.name)
			self.designs.SetPyData(child, category)
			self.designs.SetItemImage(child, 0, wx.TreeItemIcon_Normal)
			self.designs.SetItemImage(child, 1, wx.TreeItemIcon_Expanded)

			for design in cache.designs.values():
				if category.id in design.categories:
					last = self.designs.AppendItem(child, design.name)
					self.designs.SetPyData(last, design)
					self.designs.SetItemImage(last, 2, wx.TreeItemIcon_Normal)

			if not self.designs.ItemHasChildren(child):
				self.designs.Delete(child)

		self.designs.SortChildren(self.designs.GetRootItem())

		self.designs.Expand(root)
# FIXME: This is broken as it does not take into account the change of position of items
#		if selected:
#			self.designs.SelectItem(selected)
#			self.designs.EnsureVisible(selected)

		self.designs.SetSize(self.designs.GetVirtualSize())

	def UpdateCompList(self, evt=None):
# FIXME: This is broken as it does not take into account the change of position of items
#		selected = self.comps.GetSelection()

		self.comps.DeleteAllItems()

		root = self.comps.AddRoot("Components")
		self.comps.SetPyData(root, None)
		self.comps.SetItemImage(root, 0, wx.TreeItemIcon_Normal)
		self.comps.SetItemImage(root, 1, wx.TreeItemIcon_Expanded)

		cache = self.application.cache
		for category in cache.categories.values():
			child = self.comps.AppendItem(root, category.name)
			self.comps.SetPyData(child, category)
			self.comps.SetItemImage(child, 0, wx.TreeItemIcon_Normal)
			self.comps.SetItemImage(child, 1, wx.TreeItemIcon_Expanded)

			for component in cache.components.values():
				if category.id in component.categories:
					last = self.comps.AppendItem(child, component.name)
					self.comps.SetPyData(last, component.id)
					self.comps.SetItemImage(last, 2, wx.TreeItemIcon_Normal)

			if not self.comps.ItemHasChildren(child):
				self.comps.Delete(child)

		self.comps.SortChildren(self.comps.GetRootItem())

		self.comps.Expand(root)
	
# FIXME: This is broken as it does not take into account the change of position of items
#		if selected:
#			self.comps.SelectItem(selected)
#			self.comps.EnsureVisible(selected)

