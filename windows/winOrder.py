"""\
The order window.
"""

import time

# wxPython imports
from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

# Local imports
from winBase import winBase

from events import *
from game.events import *

from network import protocol

from extra import wxChoiceHelper
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

class winOrder(winBase):
	title = "Orders"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		# Setup to recieve game events
		self.app = application
		self.app.game.WinConnect(self)
		EVT_WINDOWS_OBJ_SELECT(self, self.OnSelect)
		EVT_GAME_ORDER_ARRIVE(self,  self.OnOrder)

		panel = wxPanel(self, -1)
		panel.SetConstraints(LayoutAnchors(self, 1, 1, 1, 1))
		self.panel = panel
		self.obj = {}
		
		item0 = wxFlexGridSizer( 0, 1, 0, 0 )
		item0.AddGrowableCol( 0 )
		item0.AddGrowableRow( 0 )
		item0.AddGrowableRow( 4 )
		
		# The client data on this object is the order's description ID, -1 is for waiting.
		item1 = wxListBox( panel, ORDER_LIST, wxDefaultPosition, wxSize(160,120), [], wxLB_SINGLE|wxSUNKEN_BORDER )
		self.obj['Orders'] = item1
		item0.AddWindow( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
		EVT_LISTBOX(self, ORDER_LIST, self.OnOrderSelect)
	
		item2 = wxStaticLine( panel, ORDER_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
		item0.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )
	
		item3 = wxFlexGridSizer( 1, 0, 0, 0 )
		
		item4 = wxButton( panel, ORDER_NEW, "New Order", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )
		EVT_BUTTON(self, ORDER_NEW, self.OnOrderNew)

		# The client data on this object is the order desc ID
		item5 = wxChoice( panel, ORDER_TYPE, wxDefaultPosition, wxSize(140,-1), [] , 0 )
		item3.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )
		self.obj['OrdersDesc'] = item5
		
		item7 = wxStaticLine( panel, ORDER_LINE, wxDefaultPosition, wxSize(-1,20), wxLI_VERTICAL )
		item3.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )
	
		item6 = wxButton( panel, ORDER_DELETE, "Delete Order", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )
		EVT_BUTTON(self, ORDER_DELETE, self.OnOrderDelete)
	
		item0.AddSizer( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

		item7 = wxStaticLine( panel, ORDER_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
		item0.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

		item8 = wxFlexGridSizer( 0, 2, 0, 0 )
		item0.AddSizer( item8, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )
		self.obj['OrderArgsRegion'] = item8

		panel.SetAutoLayout( true )
		panel.SetSizer( item0 )
		
		item0.Fit( panel )
		item0.SetSizeHints( panel )
		
		self.SetSize(size)
		self.SetPosition(pos)

		self.oid = -1

	def OnOrder(self, evt):
		g = self.app.game
		
		order = evt.value
		orderdesc = g.descs.OrderDesc(order.otype)
		
		if orderdesc:
			debug(DEBUG_WINDOWS, "Got an order object %s" % repr(order))
	
			self.obj['Orders'].SetString(order.slot, orderdesc.name)
			self.obj['Orders'].SetClientData(order.slot, order)
		else:
			# Need to raise some type of error here.
			debug(DEBUG_WINDOWS, "Have not got the orderdesc yet (%i) :(" % order.otype)

	def OnOrderNew(self, evt):
		g = self.app.game
		oid = self.oid

		# Check that something is selected in the "type" box
		orderdesc_id = self.obj['OrdersDesc'].GetSelection()
		if orderdesc_id != wxNOT_FOUND:
			
			orderdesc_id = self.obj['OrdersDesc'].GetClientData(orderdesc_id)
			
			# Append a new order to the list below the currently selected one
			slot = self.obj['Orders'].GetSelection()
			if slot == wxNOT_FOUND:
				debug(DEBUG_WINDOWS, "No orders in the order list")
				slot = 0
			else:
				slot += 1
				
			debug(DEBUG_WINDOWS, "Inserting new order to slot %i" % slot)

			orderdesc = g.descs.OrderDesc(orderdesc_id)
			if orderdesc:
			
				wxChoiceHelper.Insert(self.obj['Orders'], slot, "New order, %s" % orderdesc.name, None)

				# Okay lets select this new order

				self.obj['Orders'].SetSelection(slot)

				# Now we need to somehow raise a selection event...
			
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
		slot = self.obj['Orders'].GetSelection()
		if slot != wxNOT_FOUND:

			nevt = GameOrderRemoveEvent(oid, slot)
			wxPostEvent(nevt)
			
			# FIXME: EVIL HACK
			time.sleep(1)

			# Reload the object
			nevt = GameObjectGetEvent(oid)
			wxPostEvent(nevt)


	def OnOrderSelect(self, evt):
		g = self.app.game

		slot = self.obj['Orders'].GetSelection()
		if slot == wxNOT_FOUND:
			debug(DEBUG_WINDOWS, "No order selected")
			return

		order = self.obj['Orders'].GetClientData(slot)
		self.BuildPanel(order)
	
	def BuildPanel(self, order):
		"""\
		Builds a panel for the entering of orders arguments.
		"""
		g = self.app.game
		orderdesc = g.descs.OrderDesc(order.otype)
		
		if not orderdesc:
			return
		
		# Remove the previous stuff
		p =	self.obj['OrderArgsRegion']
		p.Remove(0)

		# Add the new stuff
		item0 = wxFlexGridSizer( 0, 2, 0, 0 )
		p.AddSizer( item0, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )
		
		arg_pos = 0
		for name, type, desc in orderdesc.parameters:
			# Add there name...
			item1 = wxStaticText( self.panel, ORDER_TEMP, name, wxDefaultPosition, wxDefaultSize, 0 )
			item0.AddWindow( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

			# Add the arguments bit
			if type == protocol.OrderDesc.ARG_COORD:
				item2 = argCoord( self.panel, order )
			elif type == protocol.OrderDesc.ARG_TIME:
				pass
			elif type == protocol.OrderDesc.ARG_OBJECT:
				pass
			elif type == protocol.OrderDesc.ARG_PLAYER:
				pass

			item0.AddSizer( item2, 0, wxALIGN_CENTRE|wxALL, 5 )
			
			# Add the description to the tooltip

			item3 = wxButton( self.panel, ORDER_NEW, "Save", wxDefaultPosition, wxDefaultSize, 0 )
			item0.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )
			EVT_BUTTON(self, ORDER_SAVE, self.OnOrderSave)
			
			item3 = wxButton( self.panel, ORDER_NEW, "Revert", wxDefaultPosition, wxDefaultSize, 0 )
			item0.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )
			EVT_BUTTON(self, ORDER_REVERT, self.OnOrderSelect)

		p.Layout()


	def OnOrderSave(self, evt):
		pass

	# Update the display for the new object
	def OnSelect(self, evt):
		g = self.app.game
		oid = evt.value

		# The object that was selected and set it as the currently selected one
		object = g.universe.Object(oid)
		self.oid = oid

		if object:
			# Set which orders can be added to this object
			self.obj['OrdersDesc'].Clear()
			for type in object.orders_valid:
				orderdesc = g.descs.OrderDesc(type)
				if orderdesc:
					self.obj['OrdersDesc'].Append(orderdesc.name, type)
				else:
					self.obj['OrdersDesc'].Append("Waiting on description for (%i)" % type, type)

			# Add a whole bunch of place holders until we get the order
			self.obj['Orders'].Clear()
			for slot in range(0, object.orders_no):
				self.obj['Orders'].Append("Waiting on order (%i) information" % slot, -1)
			
				# Request the order be gotten
				nevt = GameOrderGetEvent(object.id, slot)
				wxPostEvent(nevt)


# The display for an ARG_COORD
ID_X = 10062
ID_Y = 10063
ID_Z = 10064
ID_PICKPOS = 10065

def argCoord(parent, order):
	item0 = wxBoxSizer( wxHORIZONTAL )
	
	item1 = wxStaticText( parent, ORDER_TEMP, "X", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

	item2 = wxSpinCtrl( parent, ID_X, "0", wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, 0 )
	item0.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

	item3 = wxStaticText( parent, ORDER_TEMP, "Y", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

	item4 = wxSpinCtrl( parent, ID_Y, "0", wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, 0 )
	item0.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

	item5 = wxStaticText( parent, ORDER_TEMP, "Z", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

	item6 = wxSpinCtrl( parent, ID_Z, "0", wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, 0 )
	item0.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

	item7 = wxButton( parent, ID_PICKPOS, "PP", wxDefaultPosition, wxSize(30,-1), 0 )
	item0.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

	return item0
