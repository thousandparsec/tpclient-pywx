"""\
The order window.
"""

# Python Imports
import time
import copy

from extra.decorators import *

# wxPython Imports
import wx

# Protocol Imports
from tp.netlib import objects
from tp.netlib.objects import constants

from tp.client.ChangeList import ChangeNode, ChangeHead

TURNS_COL = 0
ORDERS_COL = 1

buttonSize = (wx.local.buttonSize[0], wx.local.buttonSize[1]+2)

CREATING = wx.Color(0, 0, 150)
UPDATING = wx.Color(150, 150, 0)
REMOVING = wx.Color(150, 0, 0)

# FIXME: This is quite annoying..
defaults = {
	constants.ARG_ABS_COORD: [0,0,0],
	constants.ARG_TIME: [0, 0],
	constants.ARG_OBJECT: [0],
	constants.ARG_PLAYER: [0,0],
	constants.ARG_STRING: [0, ""],
	constants.ARG_LIST: [[], []],
	constants.ARG_RANGE: [-1, -1, -1, -1],
}

from extra.StateTracker import TrackerObjectOrder
from windows.xrc.panelOrder import panelOrderBase
class panelOrder(panelOrderBase, TrackerObjectOrder):
	title = _("Orders")

	def __init__(self, application, parent):
		panelOrderBase.__init__(self, parent)

		self.application = application
		self.parent = parent

		TrackerObjectOrder.__init__(self)

		self.clipboard = None
		self.ignore = False

		self.Orders.InsertColumn(TURNS_COL, _("Turns"))
		self.Orders.SetColumnWidth(TURNS_COL, 40)
		self.Orders.InsertColumn(ORDERS_COL, _("Order Information"))
		self.Orders.SetColumnWidth(ORDERS_COL, 140)
		self.Orders.SetFont(wx.local.normalFont)

		self.DetailsSizer = self.DetailsPanel.GetSizer()

		self.Orders.Bind(wx.EVT_LIST_ITEM_SELECTED,   self.OnOrderSelect)
		self.Orders.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnOrderDeselect)
		self.Orders.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
		self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)

	##########################################################################
	# AUI interface bits
	##########################################################################

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize((self.GetBestSize()[0]*1.5,self.GetBestSize()[1]))
		info.Left()
		info.Layer(2)
		return info

	def DockBestSize(self):
		return wx.Size(*self.GetBestSize())
	min_size = property(DockBestSize)

	##########################################################################
	# Update the various bits in the order list
	##########################################################################

	def ColourListItem(self, listpos, color):
		"""\
		Makes a listpos show that the item is pending changes.
		"""
		item = self.Orders.GetItem(listpos)
		item.SetTextColour(color)
		self.Orders.SetItem(item)

	def ColourOrderPanel(self):
		if len(self.nodes) != 1:
			self.DetailsBorderPanel.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
		else:
			node = self.nodes[0]

			# Colour the background of the argument panel depending on the current state of the node
			if node.LastState == "idle":
				self.DetailsBorderPanel.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BACKGROUND))
			if node.LastState == "creating":
				self.DetailsBorderPanel.SetBackgroundColour(CREATING)
			if node.LastState == "removing":
				self.DetailsBorderPanel.SetBackgroundColour(REMOVING)
			if node.LastState == "updating":
				self.DetailsBorderPanel.SetBackgroundColour(UPDATING)

	def InsertListItem(self, listpos, node):
		"""\
		Inserts an order a certain position in the list.
		"""
		assert listpos <= self.Orders.GetItemCount()
		assert not isinstance(node, ChangeHead)
		assert isinstance(node, ChangeNode)

		newlistpos = self.Orders.InsertStringItem(listpos, "")
		assert newlistpos == listpos, "%s == %s" % (newlistpos, listpos)
		self.Orders.SetItemPyData(listpos, node)

		self.UpdateListItem(listpos)

	def UpdateListItem(self, listpos):
		"""\
		Updates an node at a certain position in the list.
		"""
		node = self.Orders.GetItemPyData(listpos)

		if node.CurrentState is "idle":
			self.Orders.SetStringItem(listpos, TURNS_COL, unicode(node.CurrentOrder.turns))
		else:
			self.Orders.SetStringItem(listpos, TURNS_COL, 'U')

		self.Orders.SetStringItem(listpos, ORDERS_COL, node.CurrentOrder._name)

		# FIXME: Hack
		self.ColourOrderPanel()

		if node.LastState == "idle":
			self.ColourListItem(listpos, wx.BLACK)
		if node.LastState == "creating":
			self.ColourListItem(listpos, CREATING)
		if node.LastState == "removing":
			self.ColourListItem(listpos, REMOVING)
		if node.LastState == "updating":
			self.ColourListItem(listpos, UPDATING)

	def RemoveListItem(self, listpos):
		"""\
		Removes an order from a position in the list.
		"""
		# FIXME: Hack
		self.ColourOrderPanel()

		self.Orders.DeleteItem(listpos)

	##########################################################################
	# Methods called when state changes with an object
	##########################################################################

	@freeze_wrapper
	def ObjectSelect(self, id):
		"""\
		Called when an object is selected.
		"""
		# Hide the order panel when no object is selected
		if id is None:
			self.Master.Hide()
			return

		# Check the object exists
		object = self.application.cache.objects[self.oid]

		# Do the clean up first
		self.Orders.DeleteAllItems()
		self.Possible.Clear()

		if object.order_number == 0 and len(object.order_types) == 0:
			# No orders and no possible orders on this object!
			self.Master.Hide()
		else:
			self.Master.Show()
			self.Master.Layout()
			self.Master.Update()

		self.Orders.SetToolTipDefault(_("Current orders on %s.") % object.name)
		
		orders = self.application.cache.orders[self.oid]

		# Add all the orders to the list
		for listpos, node in enumerate(orders):
			self.InsertListItem(listpos, node)
	
		# Set which order types can be added to this object
		self.Possible.SetToolTipDefault(_("Order type to create"))
		for type in object.order_types:
			if not objects.OrderDescs().has_key(type):
				print "WARNING: Unknown order type with id %s" % type
				continue

			od = objects.OrderDescs()[type]
			
			self.Possible.Append(od._name, type)
			if hasattr(od, "doc"):
				desc = od.doc
			else:
				desc = od.__doc__
			desc = desc.strip()

			self.Possible.SetToolTipItem(self.Possible.GetCount()-1, desc)
		
		# Set the order types to the first selection
		if len(object.order_types) > 0:
			self.Possible.Enable()
			self.Possible.SetSelection(0)
		else:
			self.Possible.Disable()

	##########################################################################
	# Methods called when state changes with the order
	##########################################################################
	@freeze_wrapper
	def OrdersSelect(self, nodes):
		# Orders Select is only valid when an object is selected
		assert self.oid != None

		d = self.application.cache.orders[self.oid]

		listpos = []
		for node in nodes:
			assert node in d
			listpos.append(d.index(node))

			assert listpos[-1] < self.Orders.GetItemCount()

		self.Orders.SetSelected(listpos)

		self.BuildPanel()

		# Enable the delete button if we have orders to delete	
		if len(nodes) > 0:
			self.Delete.Enable()
		else:
			self.Delete.Disable()

		# Ensure we can see the items
		if len(listpos) > 0:
			self.Orders.EnsureVisible(listpos[-1])

	@freeze_wrapper
	def OrderInsertAfter(self, afterme, toinsert):
		"""\
		Inserts the order into a slot.
		"""
		assert self.oid != None

		d = self.application.cache.orders[self.oid]

		assert afterme in d
		assert toinsert in d

		# Inserting into an empty list
		listpos = d.index(afterme) + 1

		# Update the list box
		self.InsertListItem(listpos, toinsert)

	@freeze_wrapper
	def OrderInsertBefore(self, beforeme, toinsert):
		"""\
		Inserts the order into a slot.
		"""
		assert self.oid != None

		d = self.application.cache.orders[self.oid]

		assert beforeme in d
		assert toinsert in d

		# Inserting into an empty list
		listpos = d.index(beforeme)-1

		# Update the list box
		self.InsertListItem(listpos, toinsert)

	@freeze_wrapper
	def OrderRefresh(self, node):
		"""\
		"""
		assert self.oid != None

		d = self.application.cache.orders[self.oid]
		assert node in d

		assert self.Orders.GetItemPyData(d.index(node)) is node

		self.UpdateListItem(d.index(node))

		if node in self.nodes:
			self.BuildPanel()

	@freeze_wrapper
	def OrdersRemove(self, nodes, override=False):
		"""\
		Deletes the order from a slot.
		"""
		assert self.oid != None

		d = self.application.cache.orders[self.oid]

		listposes = []
		for i in range(0, self.Orders.GetItemCount()):
			node = self.Orders.GetItemPyData(i)
			if node in nodes:
				listposes.append((i, node))
		listposes.sort(reverse=True)

		if override:
			for listpos, node in listposes:
				self.UpdateListItem(listpos)

				if node in self.nodes:
					self.BuildPanel()
		else:
			for listpos, node in listposes:
				self.RemoveListItem(listpos)

	####################################################
	# Local Event Handlers
	####################################################
	def OnOrderDeselect(self, evt):
		wx.CallAfter(self.OnOrderSelect, evt)

	@freeze_wrapper
	def OnOrderSelect(self, evt):
		"""\
		Called when somebody selects an order.
		"""
		if self.Orders.ignore > 0:
			self.Orders.ignore -= 1
			return

		nodes = []
		for listpos in self.Orders.GetSelected():
			nodes.append(self.Orders.GetItemPyData(listpos))

		if self.nodes == nodes:
			return
		self.SelectOrders(nodes)
		
	@freeze_wrapper
	def OnOrderNew(self, evt, after=True):
		"""\
		Called to add a new order.
		"""
		assert self.oid != None

		# Figure out what type of new order we are creating
		type = self.Possible.GetSelection()
		if type == wx.NOT_FOUND:
			return
		type = self.Possible.GetClientData(type)
		
		# Build the argument list
		orderdesc = objects.OrderDescs()[type]	

		# sequence, id, slot, type, turns, resources
		args = [0, self.oid, -1, type, 0, []]
		for name, type in orderdesc.names:
			args += defaults[type]

		# Create the new order
		new = objects.Order(*args)
		new._dirty = True

		# Insert the new order (after the currently selected)
		if after:
			node = self.InsertAfterOrder(new)
		else:
			node = self.InsertBeforeOrder(new)

		self.SelectOrders([node])

	@freeze_wrapper
	def OnOrderDelete(self, evt):
		"""\
		Called to delete the selected orders.
		"""
		self.RemoveOrders()

	@freeze_wrapper
	def OnOrderSave(self, evt):
		"""\
		Called to save the current selected orders.
		"""
		if len(self.nodes) != 1:
			return
			
		# Update the order
		order = self.FromPanel(self.nodes[0].CurrentOrder)
		self.ChangeOrder(order)

	OnNew    = OnOrderNew
	OnSave   = OnOrderSave
	OnDelete = OnOrderDelete

	@freeze_wrapper
	def OnRevert(self, evt):
		self.BuildPanel()

	@freeze_wrapper
	def OnOrderDirty(self, evt):
		"""\
		Called when an order is updated but not yet saved.
		"""
		# Ignore programatic changes
		if self.ignore:
			return 

		assert len(self.nodes) == 1
		
		# Update the order
		order = self.FromPanel(self.nodes[0].CurrentOrder)

		# Tell the gui about the change
		self.DirtyOrder(order)
	
	####################################################
	# Panel Functions
	####################################################
	@freeze_wrapper
	def BuildPanel(self):
		"""\
		Builds a panel for the entering of orders arguments.
		"""
		try:
			object = self.application.cache.objects[self.oid]
			nodes = self.nodes

			if object.order_number == 0 and len(object.order_types) == 0:
				node = _("No orders avaliable")
			elif len(nodes) > 1:
				node = _("Multiple orders selected.")
			elif len(nodes) < 1:
				node = None
			else:
				node = nodes[0]

				if node.LastState in ("removing", "removed"):
					node = _("Order queued for removal.")
		except KeyError:
			node = _("No object selected.")

		self.ColourOrderPanel()

		# Remove the previous panel and stuff
		if hasattr(self, "ArgumentsPanel"):
			self.ArgumentsPanel.Hide()
			self.DetailsSizer.Remove(self.ArgumentsPanel)
			self.ArgumentsPanel.Destroy()
			del self.ArgumentsPanel

		# Show the details panel
		self.DetailsPanel.Show()
		self.ArgumentLine.Show()
		self.Message.SetLabel("")
		self.Message.Hide()

		if isinstance(node, ChangeNode):
			order = node.CurrentOrder
			assert not order is None

			# Create a new panel
			self.ArgumentsPanel = wx.Panel(self.DetailsPanel, -1)

			self.ArgumentsPanel.SetAutoLayout( True )
			self.ArgumentsSizer = wx.FlexGridSizer( 0, 1, 0, 0)
			self.ArgumentsPanel.SetSizer(self.ArgumentsSizer)
			self.ArgumentsSizer.AddGrowableCol( 0 )

			orderdesc = objects.OrderDescs()[order.subtype]
			
			# List for the argument subpanels
			self.ArgumentsChildren = []
				
			for name, subtype in orderdesc.names:
				# Add there name..
				name_text = wx.StaticText( self.ArgumentsPanel, -1, name.title().replace("_","") )
				name_text.SetFont(wx.local.normalFont)

				# Add the arguments bit
				namepos = wx.LEFT
				if subtype == constants.ARG_ABS_COORD:
					subpanel = argCoordPanel( self, self.ArgumentsPanel, getattr(order, name) )
				elif subtype == constants.ARG_TIME:
					subpanel = argTimePanel( self, self.ArgumentsPanel, getattr(order, name) )
				elif subtype == constants.ARG_OBJECT:
					subpanel = argObjectPanel( self, self.ArgumentsPanel, getattr(order, name), self.application.cache )
				elif subtype == constants.ARG_LIST:
					namepos = wx.TOP
					subpanel = argListPanel( self, self.ArgumentsPanel, getattr(order, name) )
				elif subtype == constants.ARG_STRING:
					subpanel = argStringPanel( self, self.ArgumentsPanel, getattr(order, name) )
				else:
					subpanel = argNotImplimentedPanel( self, self.ArgumentsPanel, None )

				subpanel.SetToolTip(wx.ToolTip(getattr(orderdesc, name+'__doc__')))
				subpanel.SetFont(wx.local.normalFont)
				self.ArgumentsChildren.append( subpanel )
				
				if namepos == wx.TOP:
					self.ArgumentsSizer.Add( name_text, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.LEFT,  border=4)
					self.ArgumentsSizer.Add( subpanel, 1,  wx.GROW|wx.EXPAND|wx.ALIGN_CENTER)
		
				elif namepos == wx.LEFT:
					ArgumentSubSizer = wx.BoxSizer(wx.HORIZONTAL)
					ArgumentSubSizer.Add( name_text, 0, wx.ALIGN_CENTER|wx.RIGHT, 4 )
					ArgumentSubSizer.Add( subpanel,  1, wx.GROW|wx.EXPAND|wx.ALIGN_CENTER)

					self.ArgumentsSizer.Add(ArgumentSubSizer, 1, wx.GROW|wx.EXPAND|wx.ALIGN_CENTER)

				else:
					raise TypeError('WTF?')

			if len(orderdesc.names) == 0:
				name_text = wx.StaticText( self.ArgumentsPanel, -1, "No arguments" )
				name_text.SetFont(wx.local.normalFont)
				self.ArgumentsSizer.Add( name_text, 0, wx.ALIGN_CENTER|wx.CENTER, 4 )

#			self.DetailsPanel.SetClientSize(wx.Size(self.GetBestSize()[0], -1))
			self.DetailsSizer.Add( self.ArgumentsPanel, flag=wx.GROW|wx.EXPAND|wx.ALIGN_CENTER|wx.ALL)
		
			# Show the Save/Revert/Delete buttons
			self.Message.Show()
			self.Save.Show()
			self.Revert.Show()
			self.Delete.Show()
	
		elif isinstance(node, (unicode, str)):
			self.Message.SetLabel(node)
			self.Message.Show()

			# Hide the Save/Revert buttons
			self.Save.Hide()
			self.Revert.Hide()

			# Delete button should still be valid
			self.Delete.Show()
		else:
			self.DetailsPanel.Hide()
			self.ArgumentLine.Hide()

			# Hide the Save/Revert/Delete buttons
			self.Save.Hide()
			self.Revert.Hide()
			self.Delete.Hide()

		self.Orders.SetSize((-1,0))
		self.Master.Layout()
		self.Layout()
		self.Orders._doResize()

	def FromPanel(self, order):
		orderdesc = objects.OrderDescs()[order.subtype]
		
		args = [order.sequence, order.id, -1, order.subtype, 0, []]
		subpanels = copy.copy(self.ArgumentsChildren)
		for name, type in orderdesc.names:
			panel = subpanels.pop(0)
				
			if type == constants.ARG_ABS_COORD:
				args += argCoordGet( panel )
			elif type == constants.ARG_TIME:
				args += argTimeGet( panel )
			elif type == constants.ARG_OBJECT:
				args += argObjectGet( panel )
			elif type == constants.ARG_PLAYER:
				pass
			elif type == constants.ARG_RANGE:
				pass
			elif type == constants.ARG_LIST:
				args += argListGet( panel )
			elif type == constants.ARG_STRING:
				args += argStringGet( panel )

		return apply(objects.Order, args)

	##########################################################################
	# Clipboard functionality
	##########################################################################

	def BuildMenu(self, menu):
		"""\
		Build a menu containing the order types which could be inserted.
		"""
		object = self.application.cache.objects[self.oid]
		
		for type in object.order_types:
			if not objects.OrderDescs().has_key(type):
				continue

			od = objects.OrderDescs()[type]
			
			if hasattr(od, "doc"):
				desc = od.doc
			else:
				desc = od.__doc__
			desc = desc.strip()
			menu.Append(-1, od._name, desc)

	def CheckClipBoard(self):
		"""\
		Check if the items in the clipboard could be pasted on the currently selected object.
		"""
		if self.clipboard != None:
			for order in self.clipboard:
				if not objects.OrderDescs().has_key(order.subtype):
					return False

				slot = self.Possible.FindString(objects.OrderDescs()[order.subtype]._name)
				if slot == wx.NOT_FOUND:
					return False
			return True
		return False

	####################################################
	# Window Event Handlers
	####################################################
	def OnRightClick(self, evt):
		"""\
		Pop-up a menu when a person right clicks on the order list.
		"""
		slot = self.Orders.HitTest(evt.GetPosition())[0]
		if slot != wx.NOT_FOUND:
			if not evt.ControlDown() and not evt.ShiftDown():
				# Check if shift or ctrl is being held down...
				self.Orders.SetSelected([slot])
			else:
				self.Orders.AddSelected(slot)

		id = wx.NewId()
		menu = wx.Menu()
		menu.SetTitle(_("Top"))

		# Check to see if we can paste the stuff here...
		nopaste = self.CheckClipBoard()

		slots = self.Orders.GetSelected()
		if len(slots) > 0:
			before = wx.Menu()
			before.SetTitle(_("Before"))
			menu.AppendMenu(-1, _("New Before"), before)
			self.BuildMenu(before)

			after = wx.Menu()
			after.SetTitle(_("After"))
			menu.AppendMenu(-1, _("New After"), after)
			self.BuildMenu(after)
	
			menu.Append(-1, _("Delete"))

			menu.AppendSeparator()
			
			menu.Append(-1, _("Cut"))
			menu.Append(-1, _("Copy"))

			if self.clipboard != None:
				menu.Append(-1, _("Paste Before"))
				menu.Enable(menu.FindItem(_("Paste Before")), nopaste)
				menu.Append(-1, _("Paste After"))
				menu.Enable(menu.FindItem(_("Paste After")), nopaste)
		else:
			new = wx.Menu()
			new.SetTitle(_("New"))
			menu.AppendMenu(-1, _("New"), new)
			self.BuildMenu(new)
			
			if self.clipboard != None:
				menu.Append(-1, _("Paste"))
				menu.Enable(menu.FindItem(_("Paste")), nopaste)
			
		self.Bind(wx.EVT_MENU, self.OnOrderMenu)
		self.PopupMenu(menu)

	def OnOrderMenu(self, evt):
		"""\
		An action from the right click menu.
		"""
		menu = evt.GetEventObject()
		item = menu.FindItemById(evt.GetId())
		
		t = item.GetText()
		if t == _("Delete"):
			self.OnOrderDelete(None)
		elif t in (_("Copy"), _("Cut")):
			if len(self.nodes) < 1:
				return

			self.clipboard = []

			for node in self.nodes:
				self.clipboard.append(node.CurrentOrder)
		
			if t == _("Cut"):
				self.OnOrderDelete(None)
				
		elif t.startswith(_("Paste")):
			if self.CheckClipBoard() == False:
				print _("Cant paste because the orders arn't valid on this object.")
				return
				
			# Figure out whats out new position

			order = copy.deepcopy(self.clipboard[0])
			if t.endswith(_("After")):
				node = self.InsertAfterOrder(order)
			else:
				node = self.InsertBeforeOrder(order)

			for order in self.clipboard[1:]:
				node = self.InsertAfterOrder(order, node)

		else:
			slot = self.Possible.FindString(t)
			if slot == wx.NOT_FOUND:
				return

			self.Possible.SetSelection(slot)
			
			if menu.GetTitle() == _("Before"):
				self.OnOrderNew(None, after=False)
			else:
				self.OnOrderNew(None)



# The display for an ARG_COORD
X = 0
Y = 1
Z = 2

max = 2**31-1
min = -1*max

def argNotImplimentedPanel(parent, parent_panel, args):
	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.StaticText( panel, -1, _("Not implimented."))
	item1.SetFont(wx.local.normalFont)
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 0 )

	return panel

def argStringPanel(parent, parent_panel, args):
	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )

	item1 = wx.TextCtrl( panel, -1, args[1], size=(wx.local.spinSize[0]*2, wx.local.spinSize[1]))
	item1.SetFont(wx.local.tinyFont)
	item0.Add( item1, 1, wx.ALIGN_CENTRE|wx.LEFT|wx.EXPAND, 1 )
	
	return panel
	
def argStringGet(panel):
	windows = panel.GetChildren()
	return [0, windows[0].GetValue()]
	
def argObjectPanel(parent, parent_panel, args, cache):
	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )

	item1 = wx.ComboBox( panel, -1, "", choices=(), style=wx.CB_READONLY, \
				size=(wx.local.spinSize[0]*4, wx.local.spinSize[1]))

	item1.Append(_("No object"), -1)
	item1.SetSelection(0)
	for id, object in cache.objects.items():
		item1.Append(object.name + " (%s)" % object.id, object.id)
		if hasattr(object, "parent"):
			item1.SetToolTipItem(item1.GetCount()-1, _("At ") + cache.objects[object.parent].name)

		if object.id == args:
			item1.SetSelection(item1.GetCount()-1)
	item1.OnSelection(None)

	item1.SetFont(wx.local.tinyFont)
	item0.Add( item1, 1, wx.ALIGN_CENTRE|wx.LEFT|wx.EXPAND|wx.GROW, 1 )
	
	return panel

def argObjectGet(panel):
	window = panel.GetChildren()[0]
	return [window.GetClientData(window.GetSelection())]
	
def argListPanel(parent, parent_panel, args):
	panel = wx.Panel(parent_panel, -1)

	base = wx.FlexGridSizer(0, 1, 0, 0)
	base.AddGrowableCol(0)
	base.AddGrowableRow(0)

	# Convert the first arg to a dictionary
	types = {}
	for type, name, max in args[0]:
		types[type] = (name, max)

	panel.SetSizer(base)
	panel.SetAutoLayout( True )
	
	selected = wx.ListCtrl( panel, -1, wx.DefaultPosition, wx.Size(130,80), wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SUNKEN_BORDER )
	selected.InsertColumn(0, "#")
	selected.SetColumnWidth(0, 25)
	selected.InsertColumn(1, _("Type"))
	selected.SetColumnWidth(1, 100)
	selected.SetFont(wx.local.tinyFont)

	# Fill in the selected box
	for slot in range(0, len(args[1])):
		type, number = args[1][slot]

		selected.InsertStringItem(slot, "")
		selected.SetStringItem(slot, 0, unicode(number))
		selected.SetStringItem(slot, 1, types[type][0])
		selected.SetItemPyData(slot, type)
		
	type_list = wx.Choice( panel, -1, choices=[], size=wx.local.buttonSize)
	type_list.SetFont(wx.local.tinyFont)

	for type, item in types.items():
		type_list.Append(item[0], type)

	number = wx.SpinCtrl( panel, -1, "", min=0, max=100, size=wx.local.spinSize )
	number.SetFont(wx.local.tinyFont)

	add = wx.Button( panel, -1, _("Add"), size=wx.local.buttonSize )
	add.SetFont(wx.local.normalFont)
	
	delete = wx.Button( panel, -1, _("D"), size=(wx.local.smallSize[0],wx.local.buttonSize[1]) )
	delete.SetFont(wx.local.normalFont)

	box_add = wx.BoxSizer(wx.HORIZONTAL)
	box_add.Add( type_list, 2, wx.ALIGN_CENTRE|wx.LEFT|wx.EXPAND|wx.GROW, 1 )
	box_add.Add( number, 0, wx.ALIGN_CENTRE|wx.LEFT|wx.EXPAND|wx.GROW, 1 )
	box_add.Add( add, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	box_add.Add( delete, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	base.Add( selected, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 1 )
	base.Add( box_add,  1, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 1 )

	base.Fit(panel)

	def addf(evt, selected=selected, number=number, type_list=type_list):
		"""\
		Add a new selection to the list.
		"""
		amount = number.GetValue()
	
		type = type_list.GetSelection()
		if type == wx.NOT_FOUND:
			return
		type = type_list.GetClientData(type)

		slot = selected.FindItemByPyData(type)
		if slot == wx.NOT_FOUND:
			# Insert new object
			slot = 0

			selected.InsertStringItem(slot, "")
			selected.SetStringItem(slot, 0, unicode(amount))
			selected.SetStringItem(slot, 1, types[type][0])
			selected.SetItemPyData(slot, type)

		else:
			# Need to update the amount slot
			oldamount = int(selected.GetStringItem(slot, 0))
		
			max = types[type][1]
			if max != -1 and (amount + oldamount) > max:
				amount = max - oldamount

			if amount + oldamount < 0:
				amount = -1 * oldamount
			
			selected.SetStringItem(slot, 0, unicode(amount + oldamount))

	def deletef(evt, selected=selected):
		"""\
		Delete a selection from the list.
		"""
		slot = selected.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			return

		selected.DeleteItem(slot)

	def typef(evt, selected=selected, number=number, types=types, type_list=type_list, nocallback=False):
		"""\
		Update the max for the spinner.
		"""
		type = type_list.GetSelection()
		if type == wx.NOT_FOUND:
			number.SetRange(0, 0)
		else:
			current = 0
		
			slot = selected.FindItemByPyData(type)
			if slot != wx.NOT_FOUND:
				if not nocallback:
					selected.SetItemState(slot, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
				current = int(selected.GetStringItem(slot, 0))*-1
		
			type = type_list.GetClientData(type)
			if types[type][1] == 4294967295:
				number.SetRange(current, 1000)
			else:
				number.SetRange(current, types[type][1])

	def selectf(evt, selected=selected, type_list=type_list, typef=typef):
		slot = selected.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			return

		type = selected.GetItemPyData(slot)

		for slot in range(0, type_list.GetCount()):
			if type_list.GetClientData(slot) == type:
				type_list.SetSelection(slot)
				typef(None, nocallback=True)
				return
		
	parent.Bind(wx.EVT_LIST_ITEM_SELECTED, selectf, selected)
	parent.Bind(wx.EVT_BUTTON, addf, add)
	parent.Bind(wx.EVT_BUTTON, deletef, delete)
	parent.Bind(wx.EVT_CHOICE, typef, type_list)
	
	return panel

def argListGet(panel):
	selected = panel.GetChildren()[0]
	
	returns = [[], []]
	
	slot = -1
	while True:
		slot = selected.GetNextItem(slot, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE);
		if slot == wx.NOT_FOUND:
			break
		
		type = selected.GetItemPyData(slot)
		amount = int(selected.GetStringItem(slot, 0))
		
		returns[-1].append((type, amount))
	
	return returns

def argTimePanel(parent, parent_panel, args):
	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.SpinCtrl( panel, -1, unicode(args[0]), min=min, max=max, size=(wx.local.spinSize[0]*2, wx.local.spinSize[1]) )
	item1.SetFont(wx.local.tinyFont)
	item0.Add( item1, 1, wx.ALIGN_CENTRE|wx.LEFT|wx.EXPAND, 1 )
	
	return panel
	
def argTimeGet(panel):
	windows = panel.GetChildren()
	return [windows[0].GetValue(), 0]

def argCoordPanel(parent, parent_panel, args):

	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.StaticText( panel, -1, _("X"))
	item1.SetFont(wx.local.normalFont)
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 0 )

	item2 = wx.TextCtrl( panel, -1, unicode(args[X]), size=wx.local.spinSize, validator=wx.SimpleValidator(wx.DIGIT_ONLY) )
	item2.SetFont(wx.local.tinyFont)
	item0.Add( item2, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item3 = wx.StaticText( panel, -1, _("Y"))
	item3.SetFont(wx.local.normalFont)
	item0.Add( item3, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	item4 = wx.TextCtrl( panel, -1, unicode(args[Y]), size=wx.local.spinSize, validator=wx.SimpleValidator(wx.DIGIT_ONLY) )
	item4.SetFont(wx.local.tinyFont)
	item0.Add( item4, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item5 = wx.StaticText( panel, -1, _("Z"))
	item5.SetFont(wx.local.normalFont)
	item0.Add( item5, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	item6 = wx.TextCtrl( panel, -1, unicode(args[Z]), size=wx.local.spinSize, validator=wx.SimpleValidator(wx.DIGIT_ONLY) )
	item6.SetFont(wx.local.tinyFont)
	item0.Add( item6, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item7 = wx.Button( panel, -1, _("P"), size=wx.local.smallSize )
	item7.SetFont(wx.local.normalFont)
	item0.Add( item7, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	def OnSelectPosition(evt, x=item2, y=item4, z=item6, p=parent):
		p.ignore = True
		x.SetValue(unicode(evt[0]))
		y.SetValue(unicode(evt[1]))
		z.SetValue(unicode(evt[2]))
		p.ignore = False

		p.OnOrderDirty(None)

	parent.OnSelectPosition = OnSelectPosition

	# FIXME: Better way to get the children is needed...
	from windows.main.panelStarMap import panelStarMap

	starmap = parent.parent.application.gui.main.panels[panelStarMap.title]
	def p(evt, starmap=starmap):
		starmap.SetMode(starmap.GUIWaypointEdit)
	parent.Bind(wx.EVT_BUTTON, p, item7)

	parent.Bind(wx.EVT_TEXT, parent.OnOrderDirty, item2)
	parent.Bind(wx.EVT_TEXT, parent.OnOrderDirty, item4)
	parent.Bind(wx.EVT_TEXT, parent.OnOrderDirty, item6)

	return panel

def argCoordGet(panel):
	windows = panel.GetChildren()
	try:
		return [int(windows[1].GetValue()), int(windows[3].GetValue()), int(windows[5].GetValue())]
	except ValueError:
		return [0, 0, 0]
	
