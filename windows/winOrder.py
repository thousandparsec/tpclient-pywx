"""\
The order window.
"""

import time
import copy

# wxPython imports
from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

# Local imports
from winBase import winBase

from extra.wxListCtrl import wxListCtrl
from extra.wxPostEvent import *

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


wxDp = wxDefaultPosition

class winOrder(winBase):
	title = "Orders"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		# Setup to recieve game events
		application.game.WinConnect(self)

		# Create a base panel
		base_panel = wxPanel(self, -1)
		base_panel.SetConstraints(LayoutAnchors(self, 1, 1, 1, 1))
		base_panel.SetAutoLayout( true )

		# Create a base sizer
		base_sizer = wxFlexGridSizer( 0, 1, 0, 0 )
		base_sizer.Fit( base_panel )
		base_sizer.SetSizeHints( base_panel )

		# Link the panel to the sizer
		base_panel.SetSizer( base_sizer )
		
		base_sizer.AddGrowableCol( 0 )

		# List of current orders
		order_list = wxListCtrl( base_panel, ORDER_LIST, wxDefaultPosition, wxSize(160,120), wxLC_REPORT|wxLC_SINGLE_SEL|wxSUNKEN_BORDER )
		order_list.InsertColumn(TURNS_COL, "Turns")
		order_list.SetColumnWidth(TURNS_COL, 75)
		order_list.InsertColumn(ORDERS_COL, "Order Information")
		order_list.SetColumnWidth(ORDERS_COL, wxLIST_AUTOSIZE)

		# A horizontal line
		line_horiz = wxStaticLine( base_panel, -1, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL)

		# Buttons to add/delete orders
		button_sizer = wxFlexGridSizer( 1, 0, 0, 0 )
		new_button = wxButton( base_panel, ORDER_NEW, "New Order", wxDefaultPosition, wxDefaultSize, 0 )
		new_type_list = wxChoice( base_panel, ORDER_TYPE, wxDefaultPosition, wxSize(140,-1), [] , 0 )
		line_vert = wxStaticLine( base_panel, ORDER_LINE, wxDefaultPosition, wxSize(-1,20), wxLI_VERTICAL )
		delete_button = wxButton( base_panel, ORDER_DELETE, "Delete Order",	wxDefaultPosition, wxDefaultSize, 0 )
		
		button_sizer.AddWindow( new_button, 0, wxALIGN_CENTRE|wxALL, 5 )
		button_sizer.AddWindow( new_type_list, 0, wxALIGN_CENTRE|wxALL, 5 )
		button_sizer.AddWindow( line_vert, 0, wxALIGN_CENTRE|wxALL, 5 )
		button_sizer.AddWindow( delete_button, 0, wxALIGN_CENTRE|wxALL, 5 )
		
		# Order arguments
		argument_sizer = wxFlexGridSizer( 0, 1, 0, 0)
		argument_panel = wxPanel(base_panel, -1)

		# Link the argument sizer with the new panel
		argument_panel.SetSizer(argument_sizer)
		argument_panel.SetAutoLayout( true )

		# Put them all on the sizer
		base_sizer.AddWindow( order_list, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		base_sizer.AddGrowableRow( 0 )
		base_sizer.AddWindow( line_horiz, 0, wxALIGN_CENTRE|wxALL, 5 )
		base_sizer.AddSizer ( button_sizer,	0, wxALIGN_CENTRE|wxALL, 5 )
		base_sizer.AddWindow( line_horiz, 0, wxALIGN_CENTRE|wxALL, 5 )
		base_sizer.AddGrowableRow( 4 )
		base_sizer.AddWindow( argument_panel, 0, wxGROW|wxALIGN_CENTER|wxALL, 5 )

		self.oid = -1
		self.app = application
		self.base_panel = base_panel
		self.base_sizer = base_sizer
		self.order_list = order_list
		self.new_type_list = new_type_list
		self.argument_sizer = argument_sizer
		self.argument_panel = argument_panel

		EVT_BUTTON(self,  ORDER_NEW,	self.OnOrderNew)
		EVT_BUTTON(self,  ORDER_DELETE,	self.OnOrderDelete)
		
		EVT_LIST_ITEM_SELECTED(self, ORDER_LIST, self.OnOrderSelect)
		
		EVT_WINDOWS_OBJ_SELECT(self, self.OnSelect)
		EVT_GAME_ORDER_ARRIVE(self,  self.OnOrder)

		self.SetSize(size)
		self.SetPosition(pos)

	# Update the display for the new object
	def OnSelect(self, evt):
		g = self.app.game
		oid = evt.value

		# The object that was selected and set it as the currently selected one
		object = g.universe.Object(oid)
		self.oid = oid

		if object:
			# Set which orders can be added to this object
			self.new_type_list.Clear()
			for type in object.orders_valid:
				orderdesc = g.descs.OrderDesc(type)
				if orderdesc:
					self.new_type_list.Append(orderdesc.name, type)
				else:
					self.new_type_list.Append("Waiting on description for (%i)" % type, type)

			# Add a whole bunch of place holders until we get the order
			self.order_list.DeleteAllItems()
			for slot in range(0, object.orders_no):
				self.order_list.InsertStringItem(slot, "")
				self.order_list.SetStringItem(slot, TURNS_COL, "Unknown")
				self.order_list.SetStringItem(slot, ORDERS_COL, "Waiting on order (%i) information" % slot)
				self.order_list.SetItemData(slot, None)
				
				# Request the order be gotten
				nevt = GameOrderGetEvent(object.id, slot)
				wxPostEvent(nevt)

			self.BuildPanel(None)

	def OnOrder(self, evt):
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
		if orderdesc_id != wxNOT_FOUND:
			
			orderdesc_id = self.new_type_list.GetClientData(orderdesc_id)
			
			# Append a new order to the list below the currently selected one
			slot = self.order_list.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)
			if slot == wxNOT_FOUND:
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
				# FIXME: Need to select the new item..
				#self.order_list.SetSelection(slot)

				# Now send an insert event
				nevt = GameOrderInsertEvent(oid, orderdesc_id, slot)
				wxPostEvent(nevt)

				# FIXME: EVIL HACK
				time.sleep(1)
				
				# Reload the object
				nevt = GameObjectGetEvent(oid)
				wxPostEvent(nevt)
			
			else:
				# Need to raise some type of error here.
				debug(DEBUG_WINDOWS, "Have not got the orderdesc yet (%i) :(" % orderdesc_id)
				
		else:
			debug(DEBUG_WINDOWS, "No order type selected for new!")

	def OnOrderDelete(self, evt):
		g = self.app.game
		oid = self.oid

		# Check that something is selected in the "type" box
		slot = self.order_list.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)
		if slot != wxNOT_FOUND:

			nevt = GameOrderRemoveEvent(oid, slot)
			wxPostEvent(nevt)
			
			# FIXME: EVIL HACK
			time.sleep(1)

			# Reload the object
			nevt = GameObjectGetEvent(oid)
			wxPostEvent(nevt)

			# Update the Panel
			self.BuildPanel(None)

	def OnOrderSave(self, evt):
		g = self.app.game
	
		slot = self.order_list.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)
		if slot == wxNOT_FOUND:
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
			nevt = GameOrderRemoveEvent(order=order)
			wxPostEvent(nevt)
		
			# FIXME: Evil hack
			time.sleep(1)
			
			# Send an add order for that slot
			nevt = GameOrderInsertEvent(order=order)
			wxPostEvent(nevt)

	def OnOrderSelect(self, evt):
		g = self.app.game

		slot = self.order_list.GetNextItem(-1, wxLIST_NEXT_ALL, wxLIST_STATE_SELECTED)
		if slot == wxNOT_FOUND:
			debug(DEBUG_WINDOWS, "No order selected")
			return

		order = self.order_list.GetItemData(slot)
		self.BuildPanel(order)

	def BuildPanel(self, order):
		"""\
		Builds a panel for the entering of orders arguments.
		"""
		g = self.app.game
		
		# Remove the previous panel and stuff
		self.base_sizer.Remove(self.argument_panel)
		self.argument_panel.Hide()
		self.argument_panel.Destroy()

		# Create a new panel
		self.argument_panel = wxPanel(self.base_panel, -1)
		self.argument_sizer = wxFlexGridSizer( 0, 2, 0, 0)
		
		self.argument_sizer.AddGrowableCol( 1 )

		self.argument_panel.SetSizer(self.argument_sizer)
		self.argument_panel.SetAutoLayout( true )
		
		self.base_sizer.AddWindow( self.argument_panel, 0, wxGROW|wxALIGN_CENTER|wxALL, 5 )
		
		# Do we actually have an order
		if order:
			orderdesc = g.descs.OrderDesc(order.otype)
			
			if orderdesc:
				args = list(order.args)
				
				# List for the argument subpanels
				self.argument_subpanels = []
				
				for name, type, desc in orderdesc.parameters:
					# Add there name...
					name = wxStaticText( self.argument_panel, ORDER_TEMP, name, wxDefaultPosition, wxDefaultSize, 0 )
					self.argument_sizer.AddWindow( name, 0, wxALIGN_CENTER|wxALL, 5 )

					# Add the arguments bit
					if type == protocol.OrderDesc.ARG_COORD:
						subpanel = argCoordPanel( self.argument_panel, args)
					elif type == protocol.OrderDesc.ARG_TIME:
						debug(DEBUG_WINDOWS, "Argument type (ARG_TIME) not implimented yet.")
					elif type == protocol.OrderDesc.ARG_OBJECT:
						debug(DEBUG_WINDOWS, "Argument type (ARG_OBJECT) not implimented yet.")
					elif type == protocol.OrderDesc.ARG_PLAYER:
						debug(DEBUG_WINDOWS, "Argument type (ARG_PLAYER) not implimented yet.")
						
					self.argument_sizer.AddWindow( subpanel, 0, wxGROW|wxALIGN_CENTER|wxALL, 5 )
					self.argument_subpanels.append( subpanel )
					self.argument_sizer.AddGrowableRow( len(self.argument_subpanels) - 1 )

				button_sizer = wxFlexGridSizer( 1, 0, 0, 0 )

				save_button = wxButton( self.argument_panel, ORDER_SAVE, "Save", wxDefaultPosition, wxDefaultSize, 0 )
				revert_button = wxButton( self.argument_panel, ORDER_REVERT, "Revert", wxDefaultPosition, wxDefaultSize, 0 )
				
				button_sizer.AddWindow( save_button, 0, wxALIGN_CENTRE|wxALL, 5 )
				button_sizer.AddWindow( revert_button, 0, wxALIGN_CENTRE|wxALL, 5 )
		
				self.argument_sizer.AddSizer( wxBoxSizer( wxHORIZONTAL ) )
				self.argument_sizer.AddSizer( button_sizer, 0, wxALIGN_CENTRE|wxALL, 5 )
				
				EVT_BUTTON(self, ORDER_SAVE, self.OnOrderSave)
				EVT_BUTTON(self, ORDER_REVERT, self.OnOrderSelect)
			
			else:
				# Display a message
				text = "Waiting on order description."
				msg = wxStaticText( self.argument_panel, ORDER_TEMP, text, wxDefaultPosition, wxDefaultSize, 0)
				self.argument_sizer.AddWindow( msg, 0, wxALIGN_CENTER|wxALL, 5)
		else:
			# Display message
			text = "No order selected."
			msg = wxStaticText( self.argument_panel, ORDER_TEMP, text, wxDefaultPosition, wxDefaultSize, 0)
			self.argument_sizer.AddWindow( msg, 0, wxALIGN_CENTER|wxALL, 5)
		
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

	panel = wxPanel(parent_panel, -1)
	item0 = wxBoxSizer( wxHORIZONTAL )

	panel.SetSizer(item0)
	panel.SetAutoLayout( true )
	
	item1 = wxStaticText( panel, ORDER_TEMP, "X", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

	item2 = wxSpinCtrl( panel, ID_X, str(args[X]), wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, args[X] )
	item0.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

	item3 = wxStaticText( panel, ORDER_TEMP, "Y", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

	item4 = wxSpinCtrl( panel, ID_Y, str(args[Y]), wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, args[Y] )
	item0.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

	item5 = wxStaticText( panel, ORDER_TEMP, "Z", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

	item6 = wxSpinCtrl( panel, ID_Z, str(args[Z]), wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, args[Z] )
	item0.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

	item7 = wxButton( panel, ID_PICKPOS, "PP", wxDefaultPosition, wxSize(30,-1), 0 )
	item0.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

	return panel

def argCoordGet(args, panel):
	windows = panel.GetChildren()

	# X
	args.append(windows[1].GetValue())

	# Y
	args.append(windows[3].GetValue())

	# Z
	args.append(windows[5].GetValue())
	
