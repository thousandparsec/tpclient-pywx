"""\
The order window.
"""

# Python Imports
import time
import copy

# wxPython Imports
import wx

# Local Imports
from winBase import *
from utils import *

# Protocol Imports
from tp.netlib import failed
from tp.netlib import objects
from tp.netlib.objects import constants

TURNS_COL = 0
ORDERS_COL = 1

buttonSize = (wx.local.buttonSize[0], wx.local.buttonSize[1]+2)

defaults = {
	constants.ARG_ABS_COORD: [0,0,0],
	constants.ARG_TIME: [0],
	constants.ARG_OBJECT: [0],
	constants.ARG_PLAYER: [0,0],
	constants.ARG_STRING: [-1, ""],
	constants.ARG_LIST: [[], []],
	constants.ARG_RANGE: [-1, -1, -1, -1],
}

class winOrder(winBase):
	title = _("Orders")
	
	from defaults import winOrderDefaultPosition as DefaultPosition
	from defaults import winOrderDefaultSize as DefaultSize
	from defaults import winOrderDefaultShow as DefaultShow
	
	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		self.application = application
		self.clipboard = None
		self.ignore = False

		# Create a base panel
		base_panel = wx.Panel(self, -1)
		base_panel.SetAutoLayout( True )

		# Create a base sizer
		base_sizer = wx.BoxSizer( wx.VERTICAL )
		base_sizer.Fit( base_panel )
		base_sizer.SetSizeHints( base_panel )

		# Link the panel to the sizer
		base_panel.SetSizer( base_sizer )
		
		# List of current orders
		order_list = wx.ListCtrl( base_panel, -1, wx.DefaultPosition, wx.Size(160,80), wx.LC_REPORT|wx.SUNKEN_BORDER )
		order_list.InsertColumn(TURNS_COL, _("Turns"))
		order_list.SetColumnWidth(TURNS_COL, 40)
		order_list.InsertColumn(ORDERS_COL, _("Order Information"))
		order_list.SetColumnWidth(ORDERS_COL, 140)
		order_list.SetFont(wx.local.normalFont)

		# A horizontal line
		line_horiz1 = wx.StaticLine( base_panel, -1, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL)
		argument_line = wx.StaticLine( base_panel, -1, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL)

		# Buttons to add/delete orders
		button_sizer = wx.FlexGridSizer( 1, 0, 0, 0 )
		
		type_list = wx.Choice( base_panel, -1, choices=[], size=wx.local.buttonSize)
		type_list.SetFont(wx.local.tinyFont)
		
		new_button = wx.Button( base_panel, -1, _("New"), size=wx.local.buttonSize)
		new_button.SetFont(wx.local.normalFont)
		
		line_vert = wx.StaticLine( base_panel, -1, wx.DefaultPosition, wx.Size(-1,10), wx.LI_VERTICAL )

		delete_button = wx.Button( base_panel, -1, _("Delete"), size=wx.local.buttonSize)
		delete_button.SetFont(wx.local.normalFont)
		
		button_sizer.Add( type_list,     0, wx.ALIGN_CENTRE, 1 )
		button_sizer.Add( new_button,    0, wx.ALIGN_CENTRE, 1 )
		button_sizer.Add( line_vert,     0, wx.ALIGN_CENTRE, 1 )
		button_sizer.Add( delete_button, 0, wx.ALIGN_CENTRE, 1 )
		
		# Order arguments
		argument_sizer = wx.FlexGridSizer( 0, 1, 0, 0)
		argument_panel = wx.Panel(base_panel, -1)

		# Link the argument sizer with the new panel
		argument_panel.SetSizer(argument_sizer)
		argument_panel.SetAutoLayout( True )

		# Put them all on the sizer
		base_sizer.Add( order_list, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )
		base_sizer.Add( line_horiz1, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.Add( button_sizer, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.Add( argument_line, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.Add( argument_panel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 1 )

		self.oid = 0
		self.slots = None
		self.app = application
		self.base_panel = base_panel
		self.base_sizer = base_sizer
		self.order_list = order_list
		self.type_list = type_list
		self.argument_sizer = argument_sizer
		self.argument_panel = argument_panel
		self.argument_line = argument_line

		self.Bind(wx.EVT_BUTTON, self.OnOrderNew, new_button)
		self.Bind(wx.EVT_BUTTON, self.OnOrderDelete, delete_button)
		
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnOrderSelect, order_list)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnOrderSelect, order_list)
		order_list.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

	def InsertListItem(self, slot, order):
		"""\
		Inserts an order a certain position in the list.
		"""
		self.order_list.InsertStringItem(slot, "")
		self.UpdateListItem(slot, order)

	def UpdateListItem(self, slot, order):
		"""\
		Updates an order at a certain position in the list.
		"""
		self.order_list.SetStringItem(slot, TURNS_COL, str(order.turns))
		self.order_list.SetStringItem(slot, ORDERS_COL, order._name)
		#self.order_list.SetToolTipItem(slot, _("Tip %s") % slot)

		if hasattr(order, '_dirty'):
			self.ColourListItem(slot, wx.BLUE)
		else:
			self.ColourListItem(slot, wx.BLACK)

		self.order_list.SetItemPyData(slot, order)
		
	def RemoveListItem(self, slot):
		"""\
		Removes an order from a position in the list.
		"""
		self.order_list.DeleteItem(slot)

	def ColourListItem(self, slot, color):
		"""\
		Makes a slot show that the item is pending changes.
		"""
		item = self.order_list.GetItem(slot)
		item.SetTextColour(color)
		self.order_list.SetItem(item)

	def InsertOrder(self, slot, order):
		"""\
		Inserts the order into a slot.
		"""
		# Update the order
		order.slot = slot
		order._dirty = True
	
		# Update the list box
		self.InsertListItem(slot, order)

		# Tell everyone else about the change
		if slot > self.order_list.GetItemCount():
			slot = -1
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "create", self.oid, slot, order))

	def DeleteOrder(self, slot, order):
		"""\
		Deletes the order from a slot.
		"""
		# Update the order
		order.slot = slot
		order._dirty = True
	
		# Update the list box
		self.UpdateListItem(slot, order)

		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "remove", self.oid, slot, order))
	
	def UpdateOrder(self, slot, order):
		"""\
		Update the order in slot.
		"""
		# Update the order
		order.slot = slot
		order._dirty = True

		# Update the list box
		self.UpdateListItem(slot, order)
		
		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "change", self.oid, slot, order))

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
				if not objects.OrderDescs().has_key(order.type):
					return False

				slot = self.type_list.FindString(objects.OrderDescs()[order.type]._name)
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
		slot = self.order_list.HitTest(evt.GetPosition())[0]
		if slot != wx.NOT_FOUND:
			if not evt.ControlDown() and not evt.ShiftDown():
				# Check if shift or ctrl is being held down...
				self.order_list.SetSelected([slot])
			else:
				self.order_list.AddSelected(slot)

		id = wx.NewId()
		menu = wx.Menu()
		menu.SetTitle(_("Top"))

		# Check to see if we can paste the stuff here...
		nopaste = self.CheckClipBoard()

		slots = self.order_list.GetSelected()
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
		self.PopupMenu(menu, evt.GetPosition())

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
			slots = self.order_list.GetSelected()

			if len(slots) < 1:
				return

			slots.reverse()

			self.clipboard = []

			for slot in slots:
				order = self.order_list.GetItemPyData(slot)
				self.clipboard.append(order)
		
			if t == _("Cut"):
				self.OnOrderDelete(None)
				
		elif t.startswith(_("Paste")):
			if self.CheckClipBoard() == False:
				print "Cant paste because the orders arn't valid on this object."
				return
				
			# Figure out whats out new position
			slots = self.order_list.GetSelected()
			if len(slots) != 0:
				slot = slots[0] + t.endswith(_("After"))
			else:
				slot = self.order_list.GetItemCount()

			for i in xrange(0, len(self.clipboard)):
				order = copy.copy(self.clipboard[i])
				self.InsertOrder(slot+i, order)

		else:
			slot = self.type_list.FindString(t)
			if slot == wx.NOT_FOUND:
				return

			self.type_list.SetSelection(slot)
			
			if menu.GetTitle() == _("Before"):
				self.OnOrderNew(None, after=False)
			else:
				self.OnOrderNew(None)

	####################################################
	# Remote Event Handlers
	####################################################
	def OnSelectObject(self, evt, force=False):
		"""\
		Called when an object is selected.
		"""
		# Don't do anything if the object hasn't actually changed!
		if evt and self.oid == evt.id and not force:
			return
	
		# Check the object exists
		try:
			object = self.application.cache.objects[evt.id]
		except KeyError:
			print "Warning: Object %s does not exist!" % (evt.id)
			evt = None
	
		# Do the clean up first
		self.order_list.DeleteAllItems()
		self.type_list.Clear()
		
		if evt == None:
			self.oid = None
			self.OnOrderSelect(None)
			return

		# We now point to this object
		self.oid = evt.id 
		self.order_list.SetToolTipDefault(_("Current orders on %s.") % object.name)
		
		# Add all the orders to the list
		for slot in range(0, len(self.application.cache.orders[self.oid])):
			self.InsertListItem(slot, self.application.cache.orders[self.oid][slot])

		# Set which orders can be added to this object
		self.type_list.SetToolTipDefault(_("Order type to create"))
		for type in object.order_types:
			if not objects.OrderDescs().has_key(type):
				continue

			od = objects.OrderDescs()[type]
			
			self.type_list.Append(od._name, type)
			if hasattr(od, "doc"):
				desc = od.doc
			else:
				desc = od.__doc__
			desc = desc.strip()
			self.type_list.SetToolTipItem(self.type_list.GetCount()-1, desc)

		# Select no orders
		self.OnOrderSelect(None)

	def OnCacheUpdate(self, evt):
		"""\
		Called when the cache is updated.
		"""
		# If an object or the cache has updated - do a full update
		if evt.what in ("objects", None):
			self.OnSelectObject(self.application.gui.SelectObjectEvent(self.oid), force=True)
			return
		
		# Only intrested in an order has been updated and we are currently looking at that
		if evt.what != "orders" or evt.id != self.oid:
			return
			
		if evt.action in ("create", "change"):
			self.UpdateListItem(evt.slot, evt.change)
			
			# Rebuild the panel
			if evt.slot in self.order_list.GetSelected():
				self.OnOrderSelect(None, force=True)
		elif evt.action == "remove":
			self.RemoveListItem(evt.slot)

	####################################################
	# Local Event Handlers
	####################################################
	def OnOrderSelect(self, evt, force=False):
		"""\
		Called when somebody selects an order.
		"""
		slots = self.order_list.GetSelected()
		if self.slots == slots and not force:
			return
			
		if len(slots) > 1:
			order = _("Multiple orders selected.")
		elif len(slots) < 1:
			order = None
		elif self.oid == None:
			order = _("No object selected.")
		else:
			order = self.order_list.GetItemPyData(slots[0])

		self.slots == slots
		self.BuildPanel(order)

		# Ensure we can see the items
		if len(slots) > 0:
			self.order_list.EnsureVisible(slots[-1])
		
		# FIXME: This should be done better
		if not hasattr(order, '_dirty'):
			self.application.Post(self.application.gui.SelectOrderEvent(self.oid, slots))

	def OnOrderNew(self, evt, after=True):
		"""\
		Called to add a new order.
		"""
		slots = self.order_list.GetSelected()

		# Figure out what type of new order we are creating
		type = self.type_list.GetSelection()
		if type == wx.NOT_FOUND:
			return
		type = self.type_list.GetClientData(type)
		
		# Figure out the slot number
		slots = self.order_list.GetSelected()
		if len(slots) != 0:
			slot = slots[0] + after
		else:
			slot = self.order_list.GetItemCount()
		
		# Build the argument list
		orderdesc = objects.OrderDescs()[type]	

		# sequence, id, slot, type, turns, resources
		args = [-1, self.oid, slot, type, -1, []]
		for name, type in orderdesc.names:
			args += defaults[type]

		# Create the new order
		print args
		new = objects.Order(*args)
		new._dirty = True

		# Insert the new order
		self.InsertOrder(slot, new)
		
		# Select the newly created order
		self.order_list.SetSelected([slot])
		self.OnOrderSelect(None)

	def OnOrderDelete(self, evt):
		"""\
		Called to delete the selected orders.
		"""
		slots = self.order_list.GetSelected()
		for slot in slots:
			self.DeleteOrder(slot, self.order_list.GetItemPyData(slot))

	def OnOrderSave(self, evt):
		"""\
		Called to save the current selected orders.
		"""
		# Figure out which slot is selected
		slots = self.order_list.GetSelected()
		if len(slots) != 1:
			debug(DEBUG_WINDOWS, "OrderSave: No order selected for save. (%s)" % str(slots))
			return
		slot = slots[0]
		
		# Check we arn't trying to save an order with a pending changes
		order = self.order_list.GetItemPyData(slot)
		if hasattr(order, '_dirty'):
			# FIXME: Need to pop-up an error
			return
			
		# Update the order
		order = self.FromPanel(order)

		# Update the list box
		self.UpdateListItem(slot, order)

		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "change", self.oid, slot, order))

	def OnOrderUpdate(self, evt):
		"""\
		Called when an order is updated but not yet saved.
		"""
		# Ignore programatic changes
		if self.ignore:
			pass
		
		# Figure out which slot to use
		slots = self.order_list.GetSelected()
		if len(slots) != 1:
			debug(DEBUG_WINDOWS, "OrderSave: No order selected for update. (%s)" % str(slots))
			return
		slot = slots[0]

		# Check if the order is pending changes
		order = self.order_list.GetItemPyData(slot)
		
		# Update the order
		order.slot = slot
		order = self.FromPanel(order)

		# Tell the gui about the change
		self.application.gui.Post(self.application.gui.DirtyOrderEvent(order))
		
	####################################################
	# Panel Functions
	####################################################
	def BuildPanel(self, order):
		"""\
		Builds a panel for the entering of orders arguments.
		"""
		# Remove the previous panel and stuff
		self.argument_panel.Hide()
		self.base_sizer.Remove(self.argument_panel)
		self.argument_panel.Destroy()

		# Show the dividing line
		self.argument_line.Show()

		# Create a new panel
		self.argument_panel = wx.Panel(self.base_panel, -1)
		self.argument_panel.SetAutoLayout( True )
		self.argument_sizer = wx.FlexGridSizer( 0, 2, 0, 0)
		
		self.argument_panel.SetSizer(self.argument_sizer)
		self.argument_sizer.AddGrowableCol( 1 )

		# Do we actually have an order
		if isinstance(order, objects.Order):
			# Is this object dirty?
			if hasattr(order, '_dirty'):
				#self.argument_panel.SetBackgroundColour(wx.BLUE)
				pass
		
			orderdesc = objects.OrderDescs()[order.type]
			
			# List for the argument subpanels
			self.argument_subpanels = []
				
			for name, type in orderdesc.names:
				# Add there name..
				name_text = wx.StaticText( self.argument_panel, -1, name.title().replace("_","") )
				name_text.SetFont(wx.local.normalFont)

				self.argument_sizer.Add( name_text, 0, wx.ALIGN_CENTER|wx.RIGHT, 4 )

				# Add the arguments bit
				if type == constants.ARG_ABS_COORD:
					subpanel = argCoordPanel( self, self.argument_panel, getattr(order, name) )
				elif type == constants.ARG_TIME:
					subpanel = argTimePanel( self, self.argument_panel, getattr(order, name) )
				elif type == constants.ARG_OBJECT:
					subpanel = argObjectPanel( self, self.argument_panel, getattr(order, name), self.application.cache )
				elif type == constants.ARG_LIST:
					subpanel = argListPanel( self, self.argument_panel, getattr(order, name) )
				elif type == constants.ARG_STRING:
					subpanel = argStringPanel( self, self.argument_panel, getattr(order, name) )
				else:
					subpanel = argNotImplimentedPanel( self, self.argument_panel, None )

				subpanel.SetToolTip(wx.ToolTip(getattr(orderdesc, name+'__doc__')))

				subpanel.SetFont(wx.local.normalFont)
				self.argument_subpanels.append( subpanel )
				
				self.argument_sizer.Add( subpanel, 0, wx.GROW|wx.ALIGN_CENTER)
				self.argument_sizer.AddGrowableRow( len(self.argument_subpanels) - 1 )

			button_sizer = wx.FlexGridSizer( 1, 0, 0, 0 )

			save_button = wx.Button( self.argument_panel, -1, _("Save"), size=wx.local.buttonSize )
			save_button.SetFont(wx.local.normalFont)
			self.Bind(wx.EVT_BUTTON, self.OnOrderSave, save_button)
			revert_button = wx.Button( self.argument_panel, -1, _("Revert"), size=wx.local.buttonSize )
			revert_button.SetFont(wx.local.normalFont)
			self.Bind(wx.EVT_BUTTON, self.OnOrderSelect, revert_button)
			
			button_sizer.Add( save_button, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
			button_sizer.Add( revert_button, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
	
			self.argument_sizer.Add( wx.BoxSizer( wx.HORIZONTAL ) )
			self.argument_sizer.Add( button_sizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
			
		elif isinstance(order, (unicode, str)):
			# Display message
			msg = wx.StaticText( self.argument_panel, -1, str(order), wx.DefaultPosition, wx.DefaultSize, 0)
			msg.SetFont(wx.local.normalFont)
			
			self.argument_sizer.Add( msg, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		else:
			self.argument_line.Hide()
			self.argument_panel.Hide()
		
		self.argument_sizer.Fit(self.argument_panel)
		self.base_sizer.Add( self.argument_panel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 5 )
		self.base_sizer.Layout()

	def FromPanel(self, order):
		orderdesc = objects.OrderDescs()[order.type]
		
		args = [order.sequence, order.id, order.slot, order.type, 0, []]
		subpanels = copy.copy(self.argument_subpanels)
		for name, type in orderdesc.names:
			panel = subpanels.pop(0)
				
			if type == constants.ARG_ABS_COORD:
				args += argCoordGet( panel )
			elif type == constants.ARG_TIME:
				args += argTimeGet( panel )
			elif type == constants.ARG_OBJECT:
				args += argObjectGet( panel )
			elif type == constants.ARG_PLAYER:
				debug(DEBUG_WINDOWS, "Argument type (ARG_PLAYER) not implimented yet.")
			elif type == constants.ARG_RANGE:
				debug(DEBUG_WINDOWS, "Argument type (ARG_RANGE) not implimented yet.")
			elif type == constants.ARG_LIST:
				args += argListGet( panel )
			elif type == constants.ARG_STRING:
				args += argStringGet( panel )

		return apply(objects.Order, args)

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
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	
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
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	
	return panel

def argObjectGet(panel):
	window = panel.GetChildren()[0]
	return [window.GetClientData(window.GetSelection())]
	
def argListPanel(parent, parent_panel, args):
	panel = wx.Panel(parent_panel, -1)
	base = wx.BoxSizer(wx.VERTICAL)

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
		selected.SetStringItem(slot, 0, str(number))
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
	box_add.Add( type_list, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	box_add.Add( number, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	box_add.Add( add, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	box_add.Add( delete, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	base.Add( selected, 1, wx.EXPAND|wx.ALIGN_CENTRE|wx.ALL, 1 )
	base.Add( box_add, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )

	base.Fit(panel)

	def addf(evt, selected=selected, number=number, type_list=type_list):
		"""\
		Add a new selection to the list.
		"""
		amount = number.GetValue()
	
		type = type_list.GetSelection()
		if type == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "ListAdd: No type selected.")
			return
		type = type_list.GetClientData(type)

		slot = selected.FindItemByPyData(type)
		if slot == wx.NOT_FOUND:
			# Insert new object
			slot = 0

			selected.InsertStringItem(slot, "")
			selected.SetStringItem(slot, 0, str(amount))
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
			
			selected.SetStringItem(slot, 0, str(amount + oldamount))

	def deletef(evt, selected=selected):
		"""\
		Delete a selection from the list.
		"""
		slot = selected.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "ListDel: No selection selected.")
			return

		selected.DeleteItem(slot)

	def typef(evt, selected=selected, number=number, types=types, type_list=type_list, nocallback=False):
		"""\
		Update the max for the spinner.
		"""
		type = type_list.GetSelection()
		if type == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "ListAdd: No type selected.")
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
			debug(DEBUG_WINDOWS, "ListSelect: No selection selected.")
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
	
	item1 = wx.SpinCtrl( panel, -1, str(args), min=min, max=max, size=(wx.local.spinSize[0]*2, wx.local.spinSize[1]) )
	item1.SetFont(wx.local.tinyFont)
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	
	return panel
	
def argTimeGet(panel):
	windows = panel.GetChildren()
	return [windows[0].GetValue()]

def argCoordPanel(parent, parent_panel, args):

	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.StaticText( panel, -1, "X")
	item1.SetFont(wx.local.normalFont)
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 0 )

	item2 = wx.TextCtrl( panel, -1, str(args[X]), size=wx.local.spinSize, validator=wx.SimpleValidator(wx.DIGIT_ONLY) )
	item2.SetFont(wx.local.tinyFont)
	item0.Add( item2, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item3 = wx.StaticText( panel, -1, "Y")
	item3.SetFont(wx.local.normalFont)
	item0.Add( item3, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	item4 = wx.TextCtrl( panel, -1, str(args[Y]), size=wx.local.spinSize, validator=wx.SimpleValidator(wx.DIGIT_ONLY) )
	item4.SetFont(wx.local.tinyFont)
	item0.Add( item4, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item5 = wx.StaticText( panel, -1, "Z")
	item5.SetFont(wx.local.normalFont)
	item0.Add( item5, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	item6 = wx.TextCtrl( panel, -1, str(args[Z]), size=wx.local.spinSize, validator=wx.SimpleValidator(wx.DIGIT_ONLY) )
	item6.SetFont(wx.local.tinyFont)
	item0.Add( item6, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item7 = wx.Button( panel, -1, _("P"), size=wx.local.smallSize )
	item7.SetFont(wx.local.normalFont)
	item0.Add( item7, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	def OnSelectPosition(evt, x=item2, y=item4, z=item6, p=parent):
		p.ignore = True
		x.SetValue(str(evt.x))
		y.SetValue(str(evt.y))
		z.SetValue(str(evt.z))
		p.ignore = False

		p.OnOrderUpdate(None)

	parent.OnSelectPosition = OnSelectPosition

	# FIXME: Better way to get the children is needed...
	def p(evt, starmap=parent.parent.children[_('StarMap')]):
		starmap.SetMode("Position")
	parent.Bind(wx.EVT_BUTTON, p, item7)

	parent.Bind(wx.EVT_TEXT, parent.OnOrderUpdate, item2)
	parent.Bind(wx.EVT_TEXT, parent.OnOrderUpdate, item4)
	parent.Bind(wx.EVT_TEXT, parent.OnOrderUpdate, item6)

	return panel

def argCoordGet(panel):
	windows = panel.GetChildren()
	try:
		return [int(windows[1].GetValue()), int(windows[3].GetValue()), int(windows[5].GetValue())]
	except ValueError:
		return [0, 0, 0]
	
