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
from winBase import *
from utils import *

ORDER_LIST = 10010
ORDER_LINE = 10011
ORDER_NEW = 10012
ORDER_DELETE = 10013
ORDER_EDIT = 10014
ORDER_TYPE = 10015
ORDER_TEMP = 10016
ORDER_SAVE = 10017
ORDER_REVERT = 10018

TURNS_COL = 0
ORDERS_COL = 1

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
		order_list = wx.ListCtrl( base_panel, ORDER_LIST, wx.DefaultPosition, wx.Size(160,120), wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SUNKEN_BORDER )
		order_list.InsertColumn(TURNS_COL, "Turns")
		order_list.SetColumnWidth(TURNS_COL, 75)
		order_list.InsertColumn(ORDERS_COL, "Order Information")
		order_list.SetColumnWidth(ORDERS_COL, wx.LIST_AUTOSIZE)
		order_list.SetFont(wx.local.normalFont)

		# A horizontal line
		line_horiz = wx.StaticLine( base_panel, -1, wx.DefaultPosition, wx.Size(20,-1), wx.LI_HORIZONTAL)

		# Buttons to add/delete orders
		button_sizer = wx.FlexGridSizer( 1, 0, 0, 0 )
		
		new_button = wx.Button( base_panel, ORDER_NEW, "New Order", wx.DefaultPosition, wx.DefaultSize, 0 )
		new_button.SetFont(wx.local.normalFont)
		
		new_type_list = wx.Choice( base_panel, ORDER_TYPE, wx.DefaultPosition, wx.Size(140,-1), [] , 0 )
		new_type_list.SetFont(wx.local.normalFont)
		
		line_vert = wx.StaticLine( base_panel, ORDER_LINE, wx.DefaultPosition, wx.Size(-1,20), wx.LI_VERTICAL )

		delete_button = wx.Button( base_panel, ORDER_DELETE, "Delete Order",	wx.DefaultPosition, wx.DefaultSize, 0 )
		delete_button.SetFont(wx.local.normalFont)
		
		button_sizer.AddWindow( new_button, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		button_sizer.AddWindow( new_type_list, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		button_sizer.AddWindow( line_vert, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		button_sizer.AddWindow( delete_button, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		
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
		base_sizer.AddSizer ( button_sizer,	0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.AddWindow( line_horiz, 0, wx.ALIGN_CENTRE|wx.ALL, 1 )
		base_sizer.AddGrowableRow( 4 )
		base_sizer.AddWindow( argument_panel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 1 )

		self.oid = -1
		self.app = application
		self.base_panel = base_panel
		self.base_sizer = base_sizer
		self.order_list = order_list
		self.new_type_list = new_type_list
		self.argument_sizer = argument_sizer
		self.argument_panel = argument_panel

		self.Bind(wx.EVT_BUTTON, self.OnOrderNew, new_button)
		self.Bind(wx.EVT_BUTTON, self.OnOrderDelete, delete_button)
		
#		EVT_LIST_ITEM_SELECTED(self, ORDER_LIST, self.OnOrderSelect)

		self.SetSize(size)
		self.SetPosition(pos)

	# Update the display for the new object
	def OnSelectObject(self, evt):
		id = evt.id

		# The object that was selected and set it as the currently selected one
		object = self.application.cache[id]
		if object:
			# Add a whole bunch of place holders until we get the order
			self.order_list.DeleteAllItems()
			for slot in range(0, object.order_number):
				order = self.application.connection.get_orders(slot)
				print order
				self.order_list.InsertStringItem(slot, "")
				self.order_list.SetStringItem(slot, TURNS_COL, "Unknown")
				self.order_list.SetStringItem(slot, ORDERS_COL, "Waiting on order (%i) information" % slot)
				self.order_list.SetItemData(slot, None)
				
				# Request the order be gotten
#				nevt = GameOrderGetEvent(object.id, slot)
#				wx.PostEvent(nevt)

			# Set which orders can be added to this object
			self.new_type_list.Clear()
			for type in object.order_types:
				self.new_type_list.Append(str(type), type)
#				orderdesc = g.descs.OrderDesc(type)
#				if orderdesc:
#					self.new_type_list.Append(orderdesc.name, type)
#				else:
#					self.new_type_list.Append("Waiting on description for (%i)" % type, type)

			self.BuildPanel(None)

	def OnSelectOrder(self, evt):
		g = self.app.game
		
		order = evt.value
		orderdesc = g.descs.OrderDesc(order.otype)
		
		if orderdesc:
			debug(DEBUG_WINDOWS, "Got an order object %s" % repr(order))

			self.order_list.SetStringItem(order.slot, TURNS_COL, "Unknown")
			self.order_list.SetStringItem(order.slot, ORDERS_COL, orderdesc.name)
			self.order_list.SetItemData(order.slot, order)
		
		else:
			# Need to raise some type of error here.
			debug(DEBUG_WINDOWS, "Have not got the orderdesc yet (%i) :(" % order.otype)

	def OnOrderNew(self, evt):
		g = self.app.game
		oid = self.oid

		# Check that something is selected in the "type" box
		orderdesc_id = self.new_type_list.GetSelection()
		if orderdesc_id != wx.NOT_FOUND:
			
			orderdesc_id = self.new_type_list.GetClientData(orderdesc_id)
			
			# Append a new order to the list below the currently selected one
			slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
			if slot == wx.NOT_FOUND:
				debug(DEBUG_WINDOWS, "No orders in the order list")
				slot = 0
			else:
				slot += 1
				
			debug(DEBUG_WINDOWS, "Inserting new order to slot %i" % slot)

			orderdesc = g.descs.OrderDesc(orderdesc_id)
			if orderdesc:
				
				self.order_list.InsertStringItem(slot, "")
				self.order_list.SetStringItem(slot, TURNS_COL, "Unknown")
				self.order_list.SetStringItem(slot, ORDERS_COL, "New %s order" % orderdesc.name)
				self.order_list.SetItemData(slot, None)
				
				# Okay lets select this new order
				# FIXME: Need to select the new item.
				#self.order_list.SetSelection(slot)

				# Now send an insert event
#				nevt = GameOrderInsertEvent(oid, orderdesc_id, slot)
#				wx.PostEvent(nevt)

				# FIXME: EVIL HACK
				time.sleep(1)
				
				# Reload the object
#				nevt = GameObjectGetEvent(oid)
#				wx.PostEvent(nevt)
			
			else:
				# Need to raise some type of error here.
				debug(DEBUG_WINDOWS, "Have not got the orderdesc yet (%i) :(" % orderdesc_id)
				
		else:
			debug(DEBUG_WINDOWS, "No order type selected for new!")

	def OnOrderDelete(self, evt):
		g = self.app.game
		oid = self.oid

		# Check that something is selected in the "type" box
		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot != wx.NOT_FOUND:

#			nevt = GameOrderRemoveEvent(oid, slot)
#			wx.PostEvent(nevt)
			
			# FIXME: EVIL HACK
			time.sleep(1)

			# Reload the object
#			nevt = GameObjectGetEvent(oid)
#			wx.PostEvent(nevt)

			# Update the Panel
			self.BuildPanel(None)

	def OnOrderSave(self, evt):
		g = self.app.game
	
		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			return

		order = self.order_list.GetItemData(slot)
		if order:
			orderdesc = g.descs.OrderDesc(order.otype)
			
			if orderdesc:
				args = []

				subpanels = copy.copy(self.argument_subpanels)
				for name, type, desc in orderdesc.parameters:
					panel = subpanels.pop()
					
					if type == protocol.OrderDesc.ARG_COORD:
						argCoordGet( args, panel )
					elif type == protocol.OrderDesc.ARG_TIME:
						debug(DEBUG_WINDOWS, "Argument type (ARG_TIME) not implimented yet.")
					elif type == protocol.OrderDesc.ARG_OBJECT:
						debug(DEBUG_WINDOWS, "Argument type (ARG_OBJECT) not implimented yet.")
					elif type == protocol.OrderDesc.ARG_PLAYER:
						debug(DEBUG_WINDOWS, "Argument type (ARG_PLAYER) not implimented yet.")

			order.args = args

			# Send a remove order for that slot
#			nevt = GameOrderRemoveEvent(order=order)
#			wx.PostEvent(nevt)
		
			# FIXME: Evil hack
			time.sleep(1)
			
			# Send an add order for that slot
#			nevt = GameOrderInsertEvent(order=order)
#			wx.PostEvent(nevt)

	def OnOrderSelect(self, evt):
		g = self.app.game

		slot = self.order_list.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
		if slot == wx.NOT_FOUND:
			debug(DEBUG_WINDOWS, "No order selected")
			return

		order = self.order_list.GetItemData(slot)
		self.BuildPanel(order)

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
			orderdesc = None # g.descs.OrderDesc(order.otype)
			
			if orderdesc:
				args = list(order.args)
				
				# List for the argument subpanels
				self.argument_subpanels = []
				
				for name, type, desc in orderdesc.parameters:
					# Add there name..
					name = wx.StaticText( self.argument_panel, ORDER_TEMP, name, wx.DefaultPosition, wx.DefaultSize, 0 )
					self.argument_sizer.AddWindow( name, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

					# Add the arguments bit
					if type == protocol.OrderDesc.ARG_COORD:
						subpanel = argCoordPanel( self.argument_panel, args)
					elif type == protocol.OrderDesc.ARG_TIME:
						debug(DEBUG_WINDOWS, "Argument type (ARG_TIME) not implimented yet.")
					elif type == protocol.OrderDesc.ARG_OBJECT:
						debug(DEBUG_WINDOWS, "Argument type (ARG_OBJECT) not implimented yet.")
					elif type == protocol.OrderDesc.ARG_PLAYER:
						debug(DEBUG_WINDOWS, "Argument type (ARG_PLAYER) not implimented yet.")
						
					self.argument_sizer.AddWindow( subpanel, 0, wx.GROW|wx.ALIGN_CENTER|wx.ALL, 5 )
					self.argument_subpanels.append( subpanel )
					self.argument_sizer.AddGrowableRow( len(self.argument_subpanels) - 1 )

				button_sizer = wx.FlexGridSizer( 1, 0, 0, 0 )

				save_button = wx.Button( self.argument_panel, ORDER_SAVE, "Save", wx.DefaultPosition, wx.DefaultSize, 0 )
				revert_button = wx.Button( self.argument_panel, ORDER_REVERT, "Revert", wx.DefaultPosition, wx.DefaultSize, 0 )
				
				button_sizer.AddWindow( save_button, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
				button_sizer.AddWindow( revert_button, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
		
				self.argument_sizer.AddSizer( wx.BoxSizer( wx.HORIZONTAL ) )
				self.argument_sizer.AddSizer( button_sizer, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )
				
				EVT_BUTTON(self, ORDER_SAVE, self.OnOrderSave)
				EVT_BUTTON(self, ORDER_REVERT, self.OnOrderSelect)
			
			else:
				# Display a message
				text = "Waiting on order description."
				msg = wx.StaticText( self.argument_panel, ORDER_TEMP, text, wx.DefaultPosition, wx.DefaultSize, 0)
				self.argument_sizer.AddWindow( msg, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		else:
			# Display message
			text = "No order selected."
			msg = wx.StaticText( self.argument_panel, ORDER_TEMP, text, wx.DefaultPosition, wx.DefaultSize, 0)
			self.argument_sizer.AddWindow( msg, 0, wx.ALIGN_CENTER|wx.ALL, 5)
		
		self.base_sizer.Layout()

# The display for an ARG_COORD
ID_X = 10062
ID_Y = 10063
ID_Z = 10064
ID_PICKPOS = 10065

X = 0
Y = 1
Z = 2

def argCoordPanel(parent_panel, args):
	args = [args.pop(0), args.pop(0), args.pop(0)]

	panel = wx.Panel(parent_panel, -1)
	item0 = wx.BoxSizer( wx.HORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( True )
	
	item1 = wx.StaticText( panel, ORDER_TEMP, "X", wx.DefaultPosition, wx.DefaultSize, 0 )
	item0.AddWindow( item1, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	item2 = wx.SpinCtrl( panel, ID_X, str(args[X]), wx.DefaultPosition, wx.Size(50,-1), wx.SP_WRAP, 0, 100, args[X] )
	item0.AddWindow( item2, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	item3 = wx.StaticText( panel, ORDER_TEMP, "Y", wx.DefaultPosition, wx.DefaultSize, 0 )
	item0.AddWindow( item3, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	item4 = wx.SpinCtrl( panel, ID_Y, str(args[Y]), wx.DefaultPosition, wx.Size(50,-1), wx.SP_WRAP, 0, 100, args[Y] )
	item0.AddWindow( item4, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	item5 = wx.StaticText( panel, ORDER_TEMP, "Z", wx.DefaultPosition, wx.DefaultSize, 0 )
	item0.AddWindow( item5, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	item6 = wx.SpinCtrl( panel, ID_Z, str(args[Z]), wx.DefaultPosition, wx.Size(50,-1), wx.SP_WRAP, 0, 100, args[Z] )
	item0.AddWindow( item6, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	item7 = wx.Button( panel, ID_PICKPOS, "PP", wx.DefaultPosition, wx.Size(30,-1), 0 )
	item0.AddWindow( item7, 0, wx.ALIGN_CENTRE|wx.ALL, 5 )

	return panel

def argCoordGet(args, panel):
	windows = panel.GetChildren()

	# X
	args.append(windows[1].GetValue())

	# Y
	args.append(windows[3].GetValue())

	# Z
	args.append(windows[5].GetValue())
	
