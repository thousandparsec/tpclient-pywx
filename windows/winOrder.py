"""\
The order window.
"""

# Python Imports
import time
import copy

# wxPython Imports
import wx
import wx.lib.anchors

# Local Imports
from netlib import failed
from winBase import *
from utils import *

# Protocol Imports
from netlib import objects
from netlib.objects import OrderDescs, constants

TURNS_COL = 0
ORDERS_COL = 1

class wxListCtrl(wx.ListCtrl):
	def SetItemPyData(self, slot, data):
		if not hasattr(self, "objects"):
			self.objects = {}
		self.objects[slot] = data

	def GetItemPyData(self, slot):
		try:
			return self.objects[slot]
		except:
			return None

wx.ListCtrl = wxListCtrl

buttonSize = (wx.local.buttonSize[0], wx.local.buttonSize[1]+2)

class winOrder(winBase):
	title = "Orders"
	
	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		self.application = application

		# Create a base panel
		base_panel = wx.Panel(self, -1)
		base_panel.SetConstraints(wx.lib.anchors.LayoutAnchors(self, 1, 1, 1, 1))
		base_panel.SetAutoLayout( True )

		# Create a base sizer
		base_sizer = wx.FlexGridSizer( 0, 1, 0, 0 )
		base_sizer.Fit( base_panel )
		base_sizer.SetSizeHints( base_panel )

		# Link the panel to the sizer
		base_panel.SetSizer( base_sizer )
		
		base_sizer.AddGrowableCol( 0 )

		# List of current orders
		order_list = wx.ListCtrl( base_panel, -1, wx.DefaultPosition, wx.Size(160,80), wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SUNKEN_BORDER )
		order_list.InsertColumn(TURNS_COL, "Turns")
		order_list.SetColumnWidth(TURNS_COL, 40)
		order_list.InsertColumn(ORDERS_COL, "Order Information")
		order_list.SetColumnWidth(ORDERS_COL, 140)
		order_list.SetFont(wx.local.normalFont)

		# A horizontal line
		line_horiz = wx.StaticLine( base_panel, -1, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL)

		# Buttons to add/delete orders
		button_sizer = wx.FlexGridSizer( 1, 0, 0, 0 )
		
		new_button = wx.Button( base_panel, -1, "New", size=wx.local.buttonSize)
		new_button.SetFont(wx.local.normalFont)
		
		type_list = wx.Choice( base_panel, -1, choices=[], size=wx.local.buttonSize)
		type_list.SetFont(wx.local.tinyFont)
		
		line_vert = wx.StaticLine( base_panel, -1, wx.DefaultPosition, wx.Size(-1,10), wx.LI_VERTICAL )

		delete_button = wx.Button( base_panel, -1, "Delete", size=wx.local.buttonSize)
		delete_button.SetFont(wx.local.normalFont)
		
		button_sizer.AddWindow( new_button,    0, wx.ALIGN_CENTRE, 1 )
		button_sizer.AddWindow( type_list,     0, wx.ALIGN_CENTRE, 1 )
		button_sizer.AddWindow( line_vert,     0, wx.ALIGN_CENTRE, 1 )
		button_sizer.AddWindow( delete_button, 0, wx.ALIGN_CENTRE, 1 )
		
		# Order arguments
		argument_sizer = wx.FlexGridSizer( 0, 1, 0, 0)
		argument_panel = wx.Panel(base_panel, -1)

		# Link the argument sizer with the new panel
		argument_panel.SetSizer(argument_sizer)
		argument_panel.SetAutoLayout( True )

		# Put them all on the sizer
		base_sizer.AddWindow( order_list, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 1 )
		base_sizer.AddGrowableRow( 0 )
		base_sizer.AddWindow( line_horiz, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.AddSizer ( button_sizer, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.AddWindow( line_horiz, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.AddGrowableRow( 4 )
		base_sizer.AddWindow( argument_panel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 1 )

		self.oid = -1
		self.app = application
		self.base_panel = base_panel
		self.base_sizer = base_sizer
		self.order_list = order_list
		self.type_list = type_list
		self.argument_sizer = argument_sizer
		self.argument_panel = argument_panel

		self.Bind(wx.EVT_BUTTON, self.OnOrderNew, new_button)
		self.Bind(wx.EVT_BUTTON, self.OnOrderDelete, delete_button)
		
		self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnOrderSelect, order_list)

		self.SetSize(size)
		self.SetPosition(pos)

	def OnSelectObject(self, evt):
		oslot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

		self.oid = evt.id

		try:
			object = self.application.cache.objects[self.oid]
		except:
			debug(DEBUG_WINDOWS, "SelectObject: No such object.")
			return
			
		# Add a whole bunch of place holders until we get the order
		self.order_list.DeleteAllItems()
		for slot in range(0, object.order_number):
			order = self.application.cache.orders[self.oid][slot]

			self.order_list.InsertStringItem(slot, "")
			self.order_list.SetStringItem(slot, TURNS_COL, str(order.turns))
			self.order_list.SetStringItem(slot, ORDERS_COL, order.__class__.__name__)
			self.order_list.SetItemPyData(slot, order)

			if slot == oslot:
				self.order_list.Select(slot)
			
		# Set which orders can be added to this object
		self.type_list.Clear()
		for type in object.order_types:
			if OrderDescs().has_key(type):
				self.type_list.Append(OrderDescs()[type].name, type)
			else:
				self.type_list.Append("Wait on (%i)" % type, type)

		if oslot != wx.NOT_FOUND:
			order = self.order_list.GetItemPyData(slot)
			self.BuildPanel(order)

	def OnOrderSelect(self, evt):
		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "No order selected")
			return

		order = self.order_list.GetItemPyData(slot)
		self.BuildPanel(order)

	def OnOrderNew(self, evt):
		type = self.type_list.GetSelection()
		if type == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "OrderNew: No order type selected for new.")
			return
			
		type = self.type_list.GetClientData(type)
			
		# Append a new order to the list below the currently selected one
		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "OrderNew: No orders in the order list.")
			slot = 0
		else:
			slot += 1
			
		try:
			orderdesc = OrderDescs()[type]
		except:
			debug(DEBUG_WINDOWS, "OrderNew: Have not got OrderDesc yet (%i)" % type)
			return
			
		args = []
		for name, type in orderdesc.names:
			if type == constants.ARG_ABS_COORD:
				args += [0,0,0]
			elif type == constants.ARG_TIME:
				args += [0]
			elif type == constants.ARG_OBJECT:
				args += [0]
			elif type == constants.ARG_PLAYER:
				args += [0]

		r = self.application.connection.insert_order(self.oid, slot, orderdesc.subtype, *args)
		if failed(r):
			debug(DEBUG_WINDOWS, "OrderNew: Insert failed")
			return
					
		order = self.application.connection.get_orders(self.oid, slot)
		if failed(order):
			debug(DEBUG_WINDOWS, "OrderNew: Get failed")
			return

		self.application.cache.orders[self.oid].insert(slot, order)
		self.application.cache.objects[self.oid].order_number += 1

		self.OnSelectObject(wx.local.SelectObjectEvent(self.oid))

	def OnOrderDelete(self, evt):
		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "OrderDelete: No order selected for delete.")
			return
			
		# Remove the order
		r = self.application.connection.remove_orders(self.oid, slot)
		if failed(r):
			debug(DEBUG_WINDOWS, "OrderDelete: Remove failed!")
			return

		del self.application.cache.orders[self.oid][slot]
		self.application.cache.objects[self.oid].order_number -= 1

		self.OnSelectObject(wx.local.SelectObjectEvent(self.oid))
		
	def OnOrderSave(self, evt):
		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "OrderSave: No order selected for save.")
			return

		try:
			order = self.order_list.GetItemPyData(slot)
		except:
			debug(DEBUG_WINDOWS, "OrderSave: Could not get order")
			return
		
		try:
			orderdesc = OrderDescs()[order.type]
		except:
			debug(DEBUG_WINDOWS, "OrderSave: No order description.")
			return
			
		subpanels = copy.copy(self.argument_subpanels)
		for name, type in orderdesc.names:
			panel = subpanels.pop()
				
			if type == constants.ARG_ABS_COORD:
				args = argCoordGet( panel )
			elif type == constants.ARG_TIME:
				args = argTimeGet( panel )
			elif type == constants.ARG_OBJECT:
				debug(DEBUG_WINDOWS, "Argument type (ARG_OBJECT) not implimented yet.")
			elif type == constants.ARG_PLAYER:
				debug(DEBUG_WINDOWS, "Argument type (ARG_PLAYER) not implimented yet.")

			if args:
				setattr(order, name, args)
					
		order = self.application.connection.insert_order(self.oid, slot, order)
		if failed(order):
			debug(DEBUG_WINDOWS, "OrderSave: Insert failed.")
			return
		
		order = self.application.connection.get_orders(self.oid, slot)
		if failed(order):
			debug(DEBUG_WINDOWS, "OrderSave: Get failed.")
			return
		self.application.cache.orders[self.oid].insert(slot, order)

		r = self.application.connection.remove_orders(self.oid, slot+1)
		if failed(r):
			debug(DEBUG_WINDOWS, "OrderSave: Remove failed.")
			return
		del self.application.cache.orders[self.oid][slot+1]

		self.OnSelectObject(wx.local.SelectObjectEvent(self.oid))

	def BuildPanel(self, order):
		"""\
		Builds a panel for the entering of orders arguments.
		"""
		# Remove the previous panel and stuff
		self.base_sizer.Remove(self.argument_panel)
		self.argument_panel.Hide()
		self.argument_panel.Destroy()

		# Create a new panel
		self.argument_panel = wx.Panel(self.base_panel, -1)
		self.argument_sizer = wx.FlexGridSizer( 0, 2, 0, 0)
		
		self.argument_sizer.AddGrowableCol( 1 )

		self.argument_panel.SetSizer(self.argument_sizer)
		self.argument_panel.SetAutoLayout( True )
		
		self.base_sizer.AddWindow( self.argument_panel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 5 )
		
		# Do we actually have an order
		if order:
			orderdesc = OrderDescs()[order.type]
			
			if orderdesc:
				# List for the argument subpanels
				self.argument_subpanels = []
				
				for name, type in orderdesc.names:
					# Add there name..
					name_text = wx.StaticText( self.argument_panel, -1, name.title())
					name_text.SetFont(wx.local.normalFont)

					self.argument_sizer.AddWindow( name_text, 0, wx.ALIGN_CENTER|wx.RIGHT, 4 )

					# Add the arguments bit
					if type == constants.ARG_ABS_COORD:
						subpanel = argCoordPanel( self.argument_panel, getattr(order, name) )
					elif type == constants.ARG_TIME:
						subpanel = argTimePanel( self.argument_panel, getattr(order, name) )
					else:
						subpanel = argNotImplimentedPanel( self.argument_panel, None )
					
					subpanel.SetFont(wx.local.normalFont)
					self.argument_subpanels.append( subpanel )
					
					self.argument_sizer.AddWindow( subpanel, 0, wx.GROW)
					self.argument_sizer.AddGrowableRow( len(self.argument_subpanels) - 1 )

				button_sizer = wx.FlexGridSizer( 1, 0, 0, 0 )

				save_button = wx.Button( self.argument_panel, -1, "Save", size=wx.local.buttonSize )
				save_button.SetFont(wx.local.normalFont)
				revert_button = wx.Button( self.argument_panel, -1, "Revert", size=wx.local.buttonSize )
				revert_button.SetFont(wx.local.normalFont)
				
				button_sizer.AddWindow( save_button, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
				button_sizer.AddWindow( revert_button, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
				self.argument_sizer.AddSizer( wx.BoxSizer( wx.HORIZONTAL ) )
				self.argument_sizer.AddSizer( button_sizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
				
				self.Bind(wx.EVT_BUTTON, self.OnOrderSave, save_button)
				self.Bind(wx.EVT_BUTTON, self.OnOrderSelect, revert_button)
			
			else:
				# Display a message
				text = "Waiting on order description."
				msg = wx.StaticText( self.argument_panel, -1, text, wx.DefaultPosition, wx.DefaultSize, 0)
				msg.SetFont(wx.local.normalFont)

				self.argument_sizer.AddWindow( msg, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		else:
			# Display message
			text = "No order selected."
			msg = wx.StaticText( self.argument_panel, -1, text, wx.DefaultPosition, wx.DefaultSize, 0)
			msg.SetFont(wx.local.normalFont)
			
			self.argument_sizer.AddWindow( msg, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		
		self.base_sizer.Layout()

# The display for an ARG_COORD
X = 0
Y = 1
Z = 2

max = 2**31-1
min = -1*max

def argNotImplimentedPanel(parent_panel, args):
	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.StaticText( panel, -1, "Not implimented.")
	item1.SetFont(wx.local.normalFont)
	item0.AddWindow( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 0 )

	return panel
						
def argTimePanel(parent_panel, args):
	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.SpinCtrl( panel, -1, str(args), min=min, max=max, size=(wx.local.spinSize[0]*2, wx.local.spinSize[1]) )
	item1.SetFont(wx.local.tinyFont)
	item0.AddWindow( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )
	
	return panel
	
def argTimeGet(panel):
	windows = panel.GetChildren()
	return windows[0].GetValue()

def argCoordPanel(parent_panel, args):
	print args

	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.StaticText( panel, -1, "X")
	item1.SetFont(wx.local.normalFont)
	item0.AddWindow( item1, 0, wx.ALIGN_CENTRE|wx.LEFT, 0 )

	item2 = wx.SpinCtrl( panel, -1, str(args[X]), min=min, max=max, size=wx.local.spinSize )
	item2.SetFont(wx.local.tinyFont)
	item0.AddWindow( item2, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item3 = wx.StaticText( panel, -1, "Y")
	item3.SetFont(wx.local.normalFont)
	item0.AddWindow( item3, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	item4 = wx.SpinCtrl( panel, -1, str(args[Y]), min=min, max=max, size=wx.local.spinSize )
	item4.SetFont(wx.local.tinyFont)
	item0.AddWindow( item4, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item5 = wx.StaticText( panel, -1, "Z")
	item5.SetFont(wx.local.normalFont)
	item0.AddWindow( item5, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	item6 = wx.SpinCtrl( panel, -1, str(args[Z]), min=min, max=max, size=wx.local.spinSize )
	item6.SetFont(wx.local.tinyFont)
	item0.AddWindow( item6, 0, wx.ALIGN_CENTRE|wx.LEFT, 1 )

	item7 = wx.Button( panel, -1, "P", size=wx.local.smallSize )
	item7.SetFont(wx.local.normalFont)
	item0.AddWindow( item7, 0, wx.ALIGN_CENTRE|wx.LEFT, 3 )

	return panel

def argCoordGet(panel):
	windows = panel.GetChildren()
	return windows[1].GetValue(), windows[3].GetValue(), windows[5].GetValue()
	
