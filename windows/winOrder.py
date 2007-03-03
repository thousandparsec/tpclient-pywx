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
	constants.ARG_TIME: [0, 0],
	constants.ARG_OBJECT: [0],
	constants.ARG_PLAYER: [0,0],
	constants.ARG_STRING: [-1, ""],
	constants.ARG_LIST: [[], []],
	constants.ARG_RANGE: [-1, -1, -1, -1],
}

from xrc.panelOrder import panelOrderBase
class panelOrder(panelOrderBase):
	title = _("Orders")
	from defaults import winOrderDefaultSize as DefaultSize

	def __init__(self, application, parent):
		panelOrderBase.__init__(self, parent)

		self.application = application
		self.parent = parent

		self.clipboard = None
		self.ignore = False

		self.oid = None
		self.slots = []

		self.Orders.InsertColumn(TURNS_COL, _("Turns"))
		self.Orders.SetColumnWidth(TURNS_COL, 40)
		self.Orders.InsertColumn(ORDERS_COL, _("Order Information"))
		self.Orders.SetColumnWidth(ORDERS_COL, 140)
		self.Orders.SetFont(wx.local.normalFont)

		self.DetailsSizer = self.DetailsPanel.GetSizer()

		self.Orders.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnOrderSelect)
		self.Orders.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnOrderSelect)
		self.Orders.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(self.GetBestSize())
		info.Left()
		info.Layer(2)
		return info

	def InsertListItem(self, slot, order):
		"""\
		Inserts an order a certain position in the list.
		"""
		self.Orders.InsertStringItem(slot, "")
		self.UpdateListItem(slot, order)

	def UpdateListItem(self, slot, order):
		"""\
		Updates an order at a certain position in the list.
		"""
		self.Orders.SetStringItem(slot, TURNS_COL, str(order.turns))
		self.Orders.SetStringItem(slot, ORDERS_COL, order._name)
		#self.Orders.SetToolTipItem(slot, _("Tip %s") % slot)

		if hasattr(order, '_dirty'):
			self.ColourListItem(slot, wx.BLUE)
		else:
			self.ColourListItem(slot, wx.BLACK)

		self.Orders.SetItemPyData(slot, order)
		
	def RemoveListItem(self, slot):
		"""\
		Removes an order from a position in the list.
		"""
		self.Orders.DeleteItem(slot)

	def ColourListItem(self, slot, color):
		"""\
		Makes a slot show that the item is pending changes.
		"""
		item = self.Orders.GetItem(slot)
		item.SetTextColour(color)
		self.Orders.SetItem(item)

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
		if slot > self.Orders.GetItemCount():
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

				slot = self.Possible.FindString(objects.OrderDescs()[order.type]._name)
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
			slots = self.Orders.GetSelected()

			if len(slots) < 1:
				return

			slots.reverse()

			self.clipboard = []

			for slot in slots:
				order = self.Orders.GetItemPyData(slot)
				self.clipboard.append(order)
		
			if t == _("Cut"):
				self.OnOrderDelete(None)
				
		elif t.startswith(_("Paste")):
			if self.CheckClipBoard() == False:
				print "Cant paste because the orders arn't valid on this object."
				return
				
			# Figure out whats out new position
			slots = self.Orders.GetSelected()
			if len(slots) != 0:
				slot = slots[0] + t.endswith(_("After"))
			else:
				slot = self.Orders.GetItemCount()

			for i in xrange(0, len(self.clipboard)):
				order = copy.copy(self.clipboard[i])
				self.InsertOrder(slot+i, order)

		else:
			slot = self.Possible.FindString(t)
			if slot == wx.NOT_FOUND:
				return

			self.Possible.SetSelection(slot)
			
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
		self.Orders.DeleteAllItems()
		self.Possible.Clear()
		
		if evt == None:
			self.oid = None
			self.OnOrderSelect(None)
			return
		
		print "Orders", object.order_number, "Order Types", object.order_types
#		if object.order_number == 0 and len(object.order_types) == 0:
#			self.Hide()
#		else:
#			self.Show()

		# We now point to this object
		self.oid = evt.id 
		self.Orders.SetToolTipDefault(_("Current orders on %s.") % object.name)
		
		# Add all the orders to the list
		for slot in range(0, len(self.application.cache.orders[self.oid])):
			self.InsertListItem(slot, self.application.cache.orders[self.oid][slot])
		
		if len(self.application.cache.orders[self.oid]) > 0:
			self.Delete.Enable()
		else:
			self.Delete.Disable()

		# Set which orders can be added to this object
		self.Possible.SetToolTipDefault(_("Order type to create"))
		for type in object.order_types:
			if not objects.OrderDescs().has_key(type):
				continue

			od = objects.OrderDescs()[type]
			
			self.Possible.Append(od._name, type)
			if hasattr(od, "doc"):
				desc = od.doc
			else:
				desc = od.__doc__
			desc = desc.strip()
			self.Possible.SetToolTipItem(self.Possible.GetCount()-1, desc)

		if len(object.order_types) > 0:
			self.Possible.SetSelection(0)

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

		if len(self.application.cache.orders[self.oid]) > 0:
			self.Delete.Enable()
		else:
			self.Delete.Disable()
			
		if evt.action in ("create", "change"):

			self.UpdateListItem(evt.slot, evt.change)
			
			# Rebuild the panel
			if evt.slot in self.Orders.GetSelected():
				self.OnOrderSelect(None, force=True)
		elif evt.action == "remove":
			self.RemoveListItem(evt.slot)

			slots = self.Orders.GetSelected()
			print "slots", slots
			if evt.slot in slots or len(slots) == 0:
				self.OnOrderSelect(None)

	####################################################
	# Local Event Handlers
	####################################################
	def OnOrderSelect(self, evt, force=False):
		"""\
		Called when somebody selects an order.
		"""
		slots = self.Orders.GetSelected()
		if self.slots == slots and not force:
			return
			
		if len(slots) > 1:
			order = _("Multiple orders selected.")
		elif len(slots) < 1:
			order = None
		elif self.oid == None:
			order = _("No object selected.")
		else:
			order = self.Orders.GetItemPyData(slots[0])

		self.slots = slots
		self.BuildPanel(order)

		# Ensure we can see the items
		if len(slots) > 0:
			self.Orders.EnsureVisible(slots[-1])
		
		# FIXME: This should be done better
		if not hasattr(order, '_dirty'):
			self.application.Post(self.application.gui.SelectOrderEvent(self.oid, slots))

	def OnOrderNew(self, evt, after=True):
		"""\
		Called to add a new order.
		"""
		slots = self.Orders.GetSelected()

		# Figure out what type of new order we are creating
		type = self.Possible.GetSelection()
		if type == wx.NOT_FOUND:
			return
		type = self.Possible.GetClientData(type)
		
		# Figure out the slot number
		slots = self.Orders.GetSelected()
		if len(slots) != 0:
			slot = slots[0] + after
		else:
			slot = self.Orders.GetItemCount()
		
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
		self.Orders.SetSelected([slot])
		self.OnOrderSelect(None)

	def OnOrderDelete(self, evt):
		"""\
		Called to delete the selected orders.
		"""
		slots = self.Orders.GetSelected()
		for slot in slots:
			self.DeleteOrder(slot, self.Orders.GetItemPyData(slot))

	def OnOrderSave(self, evt):
		"""\
		Called to save the current selected orders.
		"""
		# Figure out which slot is selected
		slots = self.Orders.GetSelected()
		if len(slots) != 1:
			debug(DEBUG_WINDOWS, "OrderSave: No order selected for save. (%s)" % str(slots))
			return
		slot = slots[0]
		
		# Check we arn't trying to save an order with a pending changes
		order = self.Orders.GetItemPyData(slot)
		if hasattr(order, '_dirty'):
			# FIXME: Need to pop-up an error
			return
			
		# Update the order
		order = self.FromPanel(order)

		# Update the list box
		self.UpdateListItem(slot, order)

		# Tell everyone about the change
		self.application.Post(self.application.cache.CacheDirtyEvent("orders", "change", self.oid, slot, order))

	OnNew    = OnOrderNew
	OnSave   = OnOrderSave
	OnDelete = OnOrderDelete

	def OnRevert(self, evt):
		self.OnOrderSelect(evt, force=True)

	def DockBestSize(self):
		print "DockBestSize", self.GetBestSize()
		return wx.Size(*self.GetBestSize())
	min_size = property(DockBestSize)

	def OnOrderUpdate(self, evt):
		"""\
		Called when an order is updated but not yet saved.
		"""
		# Ignore programatic changes
		if self.ignore:
			pass
		
		# Figure out which slot to use
		slots = self.Orders.GetSelected()
		if len(slots) != 1:
			debug(DEBUG_WINDOWS, "OrderSave: No order selected for update. (%s)" % str(slots))
			return
		slot = slots[0]

		# Check if the order is pending changes
		order = self.Orders.GetItemPyData(slot)
		
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
		if hasattr(self, "ArgumentsPanel"):
			self.ArgumentsPanel.Hide()
			self.DetailsSizer.Remove(self.ArgumentsPanel)
			self.ArgumentsPanel.Destroy()
			del self.ArgumentsPanel

		# Show the details panel
		self.DetailsPanel.Show()
		self.Message.SetLabel("")

		if isinstance(order, objects.Order):
			# Create a new panel
			self.ArgumentsPanel = wx.Panel(self.DetailsPanel, -1)
			self.ArgumentsPanel.SetAutoLayout( True )
			self.ArgumentsSizer = wx.FlexGridSizer( 0, 2, 0, 0)
			
			self.ArgumentsPanel.SetSizer(self.ArgumentsSizer)
			self.ArgumentsSizer.AddGrowableCol( 1 )

			# Is this object dirty?
			if hasattr(order, '_dirty'):
				#self.ArgumentsPanel.SetBackgroundColour(wx.BLUE)
				pass
		
			orderdesc = objects.OrderDescs()[order.type]
			
			# List for the argument subpanels
			self.ArgumentsChildren = []
				
			for name, type in orderdesc.names:
				# Add there name..
				name_text = wx.StaticText( self.ArgumentsPanel, -1, name.title().replace("_","") )
				name_text.SetFont(wx.local.normalFont)

				self.ArgumentsSizer.Add( name_text, 0, wx.ALIGN_CENTER|wx.RIGHT, 4 )

				# Add the arguments bit
				if type == constants.ARG_ABS_COORD:
					subpanel = argCoordPanel( self, self.ArgumentsPanel, getattr(order, name) )
				elif type == constants.ARG_TIME:
					subpanel = argTimePanel( self, self.ArgumentsPanel, getattr(order, name) )
				elif type == constants.ARG_OBJECT:
					subpanel = argObjectPanel( self, self.ArgumentsPanel, getattr(order, name), self.application.cache )
				elif type == constants.ARG_LIST:
					subpanel = argListPanel( self, self.ArgumentsPanel, getattr(order, name) )
				elif type == constants.ARG_STRING:
					subpanel = argStringPanel( self, self.ArgumentsPanel, getattr(order, name) )
				else:
					subpanel = argNotImplimentedPanel( self, self.ArgumentsPanel, None )

				subpanel.SetToolTip(wx.ToolTip(getattr(orderdesc, name+'__doc__')))

				subpanel.SetFont(wx.local.normalFont)
				self.ArgumentsChildren.append( subpanel )
				
				self.ArgumentsSizer.Add( subpanel, 0, wx.GROW|wx.ALIGN_CENTER)
				self.ArgumentsSizer.AddGrowableRow( len(self.ArgumentsChildren) - 1 )
			
			self.DetailsPanel.SetClientSize(self.ArgumentsPanel.GetBestSize())
			self.DetailsSizer.Add( self.ArgumentsPanel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 0 )

			# Show the Save/Revert/Delete buttons
			self.Save.Show()
			self.Revert.Show()
			self.Delete.Show()		
	
		elif isinstance(order, (unicode, str)):
			self.Message.SetLabel(order)

			# Hide the Save/Revert buttons
			self.Save.Hide()
			self.Revert.Hide()

			# Delete button should still be valid
			self.Delete.Show()
		else:
			self.DetailsPanel.Hide()

			# Hide the Save/Revert/Delete buttons
			self.Save.Hide()
			self.Revert.Hide()
			self.Delete.Hide()
		
		self.DetailsPanel.Layout()
		self.Layout()

	def FromPanel(self, order):
		orderdesc = objects.OrderDescs()[order.type]
		
		args = [order.sequence, order.id, order.slot, order.type, 0, []]
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
	
	item1 = wx.SpinCtrl( panel, -1, str(args[0]), min=min, max=max, size=(wx.local.spinSize[0]*2, wx.local.spinSize[1]) )
	item1.SetFont(wx.local.tinyFont)
	item0.Add( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	
	return panel
	
def argTimeGet(panel):
	windows = panel.GetChildren()
	return [windows[0].GetValue(), 0]

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
#	def p(evt, starmap=parent.parent.children[_('StarMap')]):
#		starmap.SetMode("Position")
#	parent.Bind(wx.EVT_BUTTON, p, item7)

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
	
