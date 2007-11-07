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
from windows.winBase import winReportXRC, ShiftMixIn
from windows.xrc.winDesign import winDesignBase

from tp.client.parser import DesignCalculator
from tp.netlib.objects import Design, Component, Category

NAME = 0
DESC = 1

COL_SIZE=150

wx.ArtProvider()
Art = wx.ArtProvider_GetBitmap
wx.ArtSize = (16, 16)

def comparetoid(a, b):
	if not b is None and a[0] == type(b) and a[1] == b.id:
		return True
	return False

def comparebyid(a, b):
	if not b is None and type(a) == type(b) and a.id == b.id:
		return True
	return False


# Show the universe
class winDesign(winDesignBase, winReportXRC, ShiftMixIn):
	title = _("Design")
	
	def __init__(self, application, parent):
		winDesignBase.__init__(self, parent)
		winReportXRC.__init__(self, application, parent)
		ShiftMixIn.__init__(self)
		
		self.selected = None	# Currently selected design
		self.updating = []		# Designs which are been saved to the server

		#Panel = wx.Panel(self, -1)
		
		self.icons = wx.ImageList(*wx.ArtSize)
		self.icons.Add(Art(wx.ART_FOLDER, wx.ART_OTHER, wx.ArtSize))
		self.icons.Add(Art(wx.ART_FILE_OPEN, wx.ART_OTHER, wx.ArtSize))
		self.icons.Add(Art(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.ArtSize))

		self.grid = self.Panel.GetSizer()
		#self.grid.AddGrowableCol(0, 15)		# Middle Column is growable
		#self.grid.AddGrowableCol(1, 50)		# Middle Column is growable
		#self.grid.AddGrowableCol(2, 15)		# Middle Column is growable
		#self.grid.AddGrowableRow(1)			# Bottom row is growable

		#self.DesignsTree = wx.OrderedTreeCtrl( Panel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)
		self.DesignsTree.SetFont(wx.local.normalFont)
		self.DesignsTree.SetImageList(self.icons)

		# The labels
		################################################################
		self.top = self.TitlePanel.GetSizer()
		
		# The title (editable version)
		#self.TitleEditable = wx.TextCtrl( Panel, -1, _("Title"), size=(-1,wx.local.buttonSize[1]), style=wx.TE_CENTRE)
		self.TitleEditable.SetFont(wx.local.normalFont)
		#self.top.Add( self.TitleEditable, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The title (noneditable version)
		#self.TitleStatic = wx.StaticText( Panel, -1, _("Title"), size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
		self.TitleStatic.SetFont(wx.local.normalFont)
		#self.top.Add( self.TitleStatic, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1)

		# The number of times the design is in use
		#self.Used = wx.StaticText( Panel, -1, "0000", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_RIGHT|wx.ST_NO_AUTORESIZE)
		self.Used.SetFont(wx.local.normalFont)
		#self.top.Add( self.Used, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		self.middle = self.DesignPanel.GetSizer()
		
		# The Categories this design is in
		#self.Categories = wx.StaticText( Panel, -1, "", size=(-1,wx.local.buttonSize[1]), style=wx.ALIGN_CENTRE|wx.ST_NO_AUTORESIZE)
		self.Categories.SetFont(wx.local.normalFont)
		#self.middle.Add( self.Categories, 0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 0 )
		
		# The currently selected design
		self.designsizer = self.DesignInfoPanel.GetSizer()
		#self.middle.Add(self.designsizer, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The components in the design
		#self.PartsList = wx.ListCtrl(Panel, -1, wx.DefaultPosition, wx.DefaultSize, wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_EDIT_LABELS )
		self.PartsList.InsertColumn(0, "#", format=wx.LIST_FORMAT_RIGHT, width=20)
		self.PartsList.InsertColumn(1, _("Component"))
		self.PartsList.SetFont(wx.local.normalFont)
		#self.designsizer.Add(self.PartsList, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The properties of the design
		#self.design_ps = self.DesignProperties.GetSizer()
		self.design_ps = wx.BoxSizer(wx.HORIZONTAL)
		#self.DesignPropertyGroup1 = wx.Panel(Panel, -1)
		#self.DesignPropertyGroup1.SetSizer(self.design_ps)
		#self.designsizer.Add(self.DesignPropertyGroup1, 2, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The description of the current design
		#self.desc = wx.TextCtrl( Panel, -1, " ", style=wx.TE_RIGHT|wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)
		#self.desc.SetFont(wx.local.normalFont)
		#self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The "component description Panel"
		#self.middle.Add( self.desc, 1, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The buttons
		buttons = self.DesignButtonsPanel.GetSizer()
		#self.middle.Add(buttons, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )

		# The Edit button
		#self.Edit = wx.Button( Panel, -1, _("Edit"), size=wx.local.buttonSize)
		self.Edit.SetFont(wx.local.normalFont)
		#buttons.Add( self.Edit, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The Duplicate button
		#self.Duplicate = wx.Button( Panel, -1, _("Duplicate"), size=wx.local.buttonSize)
		self.Duplicate.SetFont(wx.local.normalFont)
		#buttons.Add( self.Duplicate, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The Delete button
		#self.Delete = wx.Button( Panel, -1, _("Delete"), size=wx.local.buttonSize)
		self.Delete.SetFont(wx.local.normalFont)
		#buttons.Add( self.Delete, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The Revert button
		#self.Revert = wx.Button( Panel, -1, _("Revert"), size=wx.local.buttonSize)
		self.Revert.SetFont(wx.local.normalFont)
		#buttons.Add( self.Revert, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

		# The Save button
		#self.Save = wx.Button( Panel, -1, _("Save"), size=wx.local.buttonSize)
		self.Save.SetFont(wx.local.normalFont)
		#buttons.Add( self.Save, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
		# The components
		
		self.compssizer = self.ComponentsPanel.GetSizer()
		
		#self.ComponentsTree = wx.OrderedTreeCtrl( Panel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT | wx.TR_MULTIPLE)
		self.ComponentsTree.SetFont(wx.local.normalFont)
		self.ComponentsTree.SetImageList(self.icons)
		#self.compssizer.Add(self.ComponentsTree, 1, wx.GROW|wx.ALIGN_RIGHT|wx.ALL, 1 )

		self.addsizer = self.ComponentsButtonPanel.GetSizer()
		#self.compssizer.Add(self.addsizer, 0, wx.ALIGN_RIGHT|wx.ALL, 0)

		#self.ComponentsAdd = wx.Button( Panel, -1, _("Add"), size=wx.local.buttonSize)
		self.ComponentsAdd.SetFont(wx.local.normalFont)
		#self.addsizer.Add(self.ComponentsAdd, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )

		#self.ComponentsAddMany = wx.Button( Panel, -1, _("Add Many"), size=wx.local.buttonSize)
		self.ComponentsAddMany.SetFont(wx.local.normalFont)
		#self.addsizer.Add(self.ComponentsAddMany, 0, wx.ALIGN_RIGHT|wx.ALL, 1 )
		
		
		#blank = wx.Panel( Panel, -1 )
		#self.grid.Add(blank,    0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		#self.grid.Add(self.top,         0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		#blank = wx.Panel( Panel, -1 )
		#self.grid.Add(blank,    0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		#self.grid.Add(self.DesignsTree,     0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		#self.grid.Add(self.middle,      0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )
		#self.grid.Add(self.compssizer,  0, wx.GROW|wx.ALIGN_CENTRE|wx.ALL, 1 )

		self.Panel.SetAutoLayout( True )
		#self.Panel.SetSizer( self.grid )

		#self.grid.Fit( Panel )
		#self.grid.SetSizeHints( self )

		self.Bind(wx.EVT_BUTTON, self.OnEdit, self.Edit)
		self.Bind(wx.EVT_BUTTON, self.OnSelect, self.Revert)
		self.Bind(wx.EVT_BUTTON, self.OnSave, self.Save)

		self.Bind(wx.EVT_BUTTON, self.OnAdd, self.ComponentsAdd)
		self.Bind(wx.EVT_BUTTON, self.OnAddMany, self.ComponentsAddMany)

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectObject, self.DesignsTree)
		
		self.DesignsSearch.Bind(wx.EVT_TEXT, self.BuildDesignList)
		self.DesignsSearch.Bind(wx.EVT_TEXT_ENTER, self.BuildDesignList)
		self.DesignsSearch.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.BuildDesignList)
		self.DesignsSearch.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnDesignsSearchCancel)
		
		self.ComponentsSearch.Bind(wx.EVT_TEXT, self.BuildCompList)
		self.ComponentsSearch.Bind(wx.EVT_TEXT_ENTER, self.BuildCompList)
		self.ComponentsSearch.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.BuildCompList)
		self.ComponentsSearch.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnComponentsSearchCancel)

		#self.Panel = Panel
		self.OnSelect()

	# Functions to manipulate the Tree controls....
	# FIXME: These should be part of the tree controls themselves...
	#################################################################################
	def TreeAddCategory(self, tree, category):
		child = tree.AppendItem(tree.GetRootItem(), category.name)
		tree.SetPyData(child, category)
		tree.SetItemImage(child, 0, wx.TreeItemIcon_Normal)
		tree.SetItemImage(child, 1, wx.TreeItemIcon_Expanded)
		return child

	def TreeAddItem(self, tree, category, object):
		child = tree.AppendItem(category, object.name)
		tree.SetPyData(child, object)
		tree.SetItemImage(child, 2, wx.TreeItemIcon_Normal)

	def TreeColourItem(self, tree, item, mode):
		if mode == "normal":
			tree.SetItemTextColour(item, wx.Color(0, 0, 0))
		elif mode == "updating":
			tree.SetItemTextColour(item, wx.Color(0, 0, 255))
		elif mode == "removing":
			tree.SetItemTextColour(item, wx.Color(255, 0, 0))

	def TreeSelectedData(self, tree, criteria):
		selected = []
		for tid in tree.GetSelections():
			object = self.ComponentsTree.GetPyData(tid)
			if isinstance(object, criteria):
				selected.append(object)
		return selected

	# Functions to build PartsList of the interface
	#################################################################################
	def DesignsFilter(self):
		filter = self.DesignsSearch.GetValue()
		if len(filter) == 0:
			return "*"
		if filter[-1] != '*':
			return '*'+filter.lower()+'*'
	DesignsFilter = property(DesignsFilter)
	
	def BuildDesignList(self, evt=None):
		self.DesignsTree.DeleteAllItems()

		root = self.DesignsTree.AddRoot(_("Designs"))
		self.DesignsTree.SetPyData(root, None)
		self.DesignsTree.SetItemImage(root, 0, wx.TreeItemIcon_Normal)
		self.DesignsTree.SetItemImage(root, 1, wx.TreeItemIcon_Expanded)

		blank = Design(-1, -1, -1, [1], _("New Design"), "", -1, -1, [], "", [])
		self.TreeAddItem(self.DesignsTree, root, blank)

		# FIXME: Designs which have no Categories are not shown.

		cache = self.application.cache
		for category in cache.categories.values():
			categoryitem = self.TreeAddCategory(self.DesignsTree, category)

			for design in cache.designs.values():
				if category.id in design.categories:
					# Filter the list..
					from fnmatch import fnmatch as match
					if match(design.name.lower(), self.DesignsFilter.lower()):
						self.TreeAddItem(self.DesignsTree, categoryitem, design)

			if not self.DesignsTree.ItemHasChildren(categoryitem):
				self.DesignsTree.Delete(categoryitem)

		self.DesignsTree.SortChildren(self.DesignsTree.GetRootItem())
		self.DesignsTree.ExpandAll()

	def ComponentsFilter(self):
		filter = self.ComponentsSearch.GetValue()
		if len(filter) == 0:
			return "*"
		if filter[-1] != '*':
			return '*'+filter.lower()+'*'
	ComponentsFilter = property(ComponentsFilter)

	def BuildCompList(self, evt=None):
		#FIXME: This is broken as it does not take into account the change of position of items
		#selected = self.ComponentsTree.GetSelection()

		self.ComponentsTree.DeleteAllItems()

		root = self.ComponentsTree.AddRoot(_("Components"))
		self.ComponentsTree.SetPyData(root, None)
		self.ComponentsTree.SetItemImage(root, 0, wx.TreeItemIcon_Normal)
		self.ComponentsTree.SetItemImage(root, 1, wx.TreeItemIcon_Expanded)

		cache = self.application.cache
		for category in cache.categories.values():
			categoryitem = self.TreeAddCategory(self.ComponentsTree, category)

			for component in cache.components.values():
				if category.id in component.categories:
					# Filter the list..
					from fnmatch import fnmatch as match
					if match(component.name.lower(), self.ComponentsFilter.lower()):
						self.TreeAddItem(self.ComponentsTree, categoryitem, component)

			if not self.ComponentsTree.ItemHasChildren(categoryitem):
				self.ComponentsTree.Delete(categoryitem)

		self.ComponentsTree.SortChildren(self.ComponentsTree.GetRootItem())
		self.ComponentsTree.ExpandAll()
	
		# FIXME: This is broken as it does not take into account the change of position of items
#		if selected:
#			self.ComponentsTree.SelectItem(selected)
#			self.ComponentsTree.EnsureVisible(selected)

	def BuildHeaderPanel(self, design):
		# Set the title
		self.TitleStatic.SetLabel(design.name)
		self.TitleEditable.SetValue(design.name)

		# Set the Used
		self.Used.SetLabel(str(design.used))
		if design.used == -1:
			self.Used.SetForegroundColour(wx.Color(255, 0, 0))
		elif design.used == 0:
			self.Used.SetForegroundColour(wx.Color(0, 255, 0))
		else:
			self.Used.SetForegroundColour(wx.Color(0, 0, 0))

		# Set the Categories
		c = ""
		for cid in design.categories:
			c += self.application.cache.categories[cid].name + ", "
		c = c[:-2]
		self.Categories.SetLabel(c)
		
	def BuildPropertiesPanel(self, design):
		SIZER_FLAGS = wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL
		cache = self.application.cache
		
		# Remove the previous Panel and stuff
		if hasattr(self, 'properties'):
			self.properties.Hide()
			self.design_ps.Remove(self.properties)
			self.properties.Destroy()
			del self.properties
		if hasattr(self, 'DesignPropertyGroup1'):
			self.DesignProperties.Hide()
			self.designsizer.Remove(self.DesignPropertyGroup1)
			self.DesignPropertyGroup1.Destroy()
			del self.DesignPropertyGroup1

		# Create a new Panel
		Panel = wx.Panel(self.DesignProperties, -1)
		sizer = wx.BoxSizer(wx.VERTICAL) 
		Panel.SetSizer(sizer)
		Panel.SetSize((250, 390))

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
			box = wx.StaticBox(Panel, -1, category.name)
			box.SetFont(wx.local.normalFont)
			box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
			sizer.Add(box_sizer, 1, SIZER_FLAGS, 5)

			# The properties
			prop_sizer = wx.FlexGridSizer( 0, 2, 0, 0 )
			box_sizer.Add(prop_sizer, 1, SIZER_FLAGS, 5)

			for property, pstring in properties[cid]:
				# Property name
				name = wx.StaticText(Panel, -1, property.display_name)
				name.SetFont(wx.local.normalFont)
				prop_sizer.Add(name, 0, SIZER_FLAGS|wx.ALIGN_RIGHT, 5)

				# Property value
				value = wx.StaticText(Panel, -1, pstring)
				value.SetFont(wx.local.normalFont)
				prop_sizer.Add(value, 1, SIZER_FLAGS|wx.ALIGN_RIGHT, 5)
				
				self.design_ps.Layout()
				Panel.Layout()
		self.DesignProperties.Show()
		self.design_ps.Show(Panel)

		self.properties = Panel

	def BuildPartsPanel(self, design):
		# Populate the PartsList list
		self.PartsList.DeleteAllItems()
		for cid, number in design.components:
			component = self.application.cache.components[cid]
		
			self.PartsList.InsertStringItem(0, str(number))
			self.PartsList.SetStringItem(0, 1, component.name)

	# Functions to update the component lists
	#################################################################################
	def OnAddMany(self, evt):
		"""\
		Pops up a selection box to ask for how many to ComponentsAdd.
		"""
		self.OnAdd(evt, amount)
	
	def OnAdd(self, evt, amount=1):
		"""\
		Adds components to the current design.
		"""
		# Figure out if a component is selected
		components = self.TreeSelectedData(self.ComponentsTree, Component)
		
		dc = DesignCalculator(self.application.cache, self.selected)
		for component in components:
			dc.change(component, amount)
		dc.update()
	
		if self.selected.Used == -1:
			if amount > 1 or len(components) > 1:
				reason = self.selected.feedback + _("\nWould you like to continue adding these components?")
			else:
				reason = self.selected.feedback + _("\nWould you like to continue adding this component?")
			dlg = wx.MessageDialog(self, reason, _('Design Warning'), wx.YES_NO|wx.NO_DEFAULT|wx.ICON_ERROR)
			
			if dlg.ShowModal() == wx.ID_NO:
				for component in components:
					dc.change(component, -amount)
				dc.update()

			dlg.Destroy()

		# Redisplay the panels
		self.BuildPartsPanel(self.selected)
		self.BuildPropertiesPanel(self.selected)

	# Functions to change the mode of the dialog
	#################################################################################
	def OnEdit(self, evt=None):
		# FIXME: Check if we can modify this Design.
	
		# Disable the select side
		self.DesignsTree.Disable()

		# Show the component bar
		self.grid.Show(self.ComponentsPanel)
		self.grid.Show(self.ComponentsSearch)
		self.ComponentsPanel.SetSize((0, 0))
		self.ComponentsSearch.SetSize((0, 0))
		self.ComponentsPanel.Layout()
		
		# Make the title and description editable
		self.top.Show(self.TitleEditable)
		self.top.Hide(self.TitleStatic)
		self.top.Layout()

		# Disable Edit, Duplicate, Delete
		self.Edit.Disable()
		self.Duplicate.Disable()
		self.Delete.Disable()

		# Enable the Save, Revert
		self.Revert.Enable()
		self.Revert.SetDefault()
		self.Save.Enable()

		# Re-layout everything
		self.grid.Layout()

		# Start the timer so that Add -> Add Many
		self.ShiftStart()

	def OnSave(self, evt):
		design = self.selected

		# Is this a new design?
		if design.id == -1:
			self.application.Post(self.application.cache.CacheDirtyEvent("DesignsTree", "create", -1, design))
			self.selected = None
		else:
			# Add the design to ones which are being updated
			self.updating.append(design.id)

			# Change the colour on the side
			for item in self.DesignsTree.FindAllByData(design, comparebyid):
				self.TreeColourItem(self.DesignsTree, item, "updating")
	
			# Tell the world about the change
			self.application.Post(self.application.cache.CacheDirtyEvent("DesignsTree", "change", design.id, design))

		self.OnSelect(None)

	def OnRemove(self, evt):
		design = self.selected

		# Add the design to ones which are being updated
		self.updating.append(design.id)
		
		# Change the colour on the side
		for item in self.DesignsTree.FindAllByData(design, comparebyid):
			self.TreeColourItem(self.DesignsTree, item, "removing")
			
		self.application.Post(self.application.cache.CacheDirtyEvent("DesignsTree", "remove", design.id, design))

	def OnSelect(self, evt=None):
		# Stop any running Shift timers
		self.ShiftStop()
	
		# Enable the selection side
		self.DesignsTree.Enable()

		# Hide the component bar
		self.grid.Hide(self.ComponentsPanel)
		self.grid.Hide(self.ComponentsSearch)
		self.ComponentsPanel.SetSize((0,0))
		self.ComponentsSearch.SetSize((0,0))
		self.ComponentsPanel.Layout()

		# Make the title and description uneditable
		self.top.Hide(self.TitleEditable)
		self.top.Show(self.TitleStatic)
		self.top.Layout()

		# Disable Save, Revert
		self.Revert.Disable()
		self.Save.Disable()

		# Re-layout everything
		self.grid.Layout()

		self.OnSelectObject()

	def OnSelectObject(self, evt=None):
		selected = self.TreeSelectedData(self.DesignsTree, Design)
		if len(selected) != 1:
			self.selected = None
		else:
			if selected[0].id in self.updating:
				self.selected = None
			else:
				self.selected = deepcopy(selected[0])

		if self.selected == None:
			# Clear the title
			self.TitleStatic.SetLabel("")

			# Hide the design
			self.grid.Hide(self.DesignPanel)
			self.grid.Layout()
			
			# Disable the buttons
			self.Edit.Disable()
			self.Duplicate.Disable()
			self.Delete.Disable()
			return

#		# Recalculate all the properties if they are empty
#		if len(self.selected.properties) == 0:
#			self.Recalculate()

		# Build the Header Panel
		self.BuildHeaderPanel(self.selected)

		# Show the PartsList list
		self.grid.Show(self.DesignPanel)
		self.grid.Layout()

		# Populate the PartsList list
		self.BuildPartsPanel(self.selected)
		
		# Populate the properties
		self.BuildPropertiesPanel(self.selected)

		# Set if Edit can work
		if self.selected.used <= 0:
			self.Edit.Enable()
			self.Edit.SetDefault()

			self.Duplicate.Enable()
			self.Delete.Enable()
		else:
			self.Edit.Disable()
			self.Delete.Disable()

			self.Duplicate.Enable()
			self.Duplicate.SetDefault()
		
		# Re-layout everything
		self.grid.Layout()

	def OnCacheUpdate(self, evt=None):
		# Full cache update, rebuild everything
		if evt.what is None:
			self.BuildDesignList()
			self.BuildCompList()

		if evt.what is "DesignsTree":
			design = evt.change
		
			if evt.action in ("change", "remove"):
				for item in self.DesignsTree.FindAllByData(design, comparebyid):
					categoryitem = self.DesignsTree.GetItemParent(item)
					self.DesignsTree.Delete(item)
					
					# Remove the category if it will be empty
					if self.DesignsTree.ItemHasChildren(categoryitem):
						self.DesignsTree.Delete(categoryitem)
				
			if evt.action in ("change", "create"):
				for categoryid in design.Categories:
					# Check the category exists
					parent = self.DesignsTree.FindItemByData((Category, categoryid), comparetoid)
					if parent is None:
						parent = self.TreeAddCategory(self.DesignsTree, self.application.cache.Categories[categoryid])
					
					# Add the new design under this category
					self.TreeAddItem(self.DesignsTree, parent, design)

			if design.id in self.updating:
				self.updating.remove(design.id)

			self.DesignsTree.SortChildren(self.DesignsTree.GetRootItem())
	
	def OnDesignsSearchCancel(self, evt):
		self.DesignsSearch.SetValue("")
		self.BuildDesignList()
		
	def OnComponentsSearchCancel(self, evt):
		self.ComponentsSearch.SetValue("")
		self.BuildCompList()
