
from wxPython.wx import *
from wxPython.lib.anchors import LayoutAnchors

# Local imports
from winBase import winBase
from events import *

ORDER_LIST = 10010
ORDER_LINE = 10011
ORDER_NEW = 10012
ORDER_DELETE = 10013
ORDER_EDIT = 10014
ORDER_TYPE = 10015

class winOrder(winBase):
	title = "Orders"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		panel = wxPanel(self, -1)
		panel.SetConstraints(LayoutAnchors(self, 1, 1, 1, 1))
		self.obj = {}

		# Setup to recieve game events
		self.app = application
		self.app.game.WinConnect(self)
		EVT_WINDOWS_SELECTOBJ(self, self.OnSelect)

		item0 = wxFlexGridSizer( 0, 1, 0, 0 )
		item0.AddGrowableCol( 0 )
		item0.AddGrowableRow( 0 )
		item0.AddGrowableRow( 4 )
		
		item1 = wxListCtrl( panel, ORDER_LIST, wxDefaultPosition, wxSize(160,120), wxLC_REPORT|wxSUNKEN_BORDER )
		item0.AddWindow( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )
	
		item2 = wxStaticLine( panel, ORDER_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
		item0.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )
	
		item3 = wxFlexGridSizer( 1, 0, 0, 0 )
		
		item4 = wxButton( panel, ORDER_NEW, "New Order", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )
	
		item5 = wxButton( panel, ORDER_DELETE, "Delete Order", wxDefaultPosition, wxDefaultSize, 0 )
		item3.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )
	
		item0.AddSizer( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

		item6 = wxChoice( panel, ORDER_TYPE, wxDefaultPosition, wxDefaultSize, ["ChoiceItem"] , 0 )
		self.obj['Orders'] = item6
		item0.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

		item7 = wxStaticLine( panel, ORDER_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
		item0.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

		item8 = wxFlexGridSizer( 0, 2, 0, 0 )
	
		#item9 = panel.FindWindowById( ORDER_EDIT )
		#item8.AddWindow( item9, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

		item0.AddSizer( item8, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

		panel.SetAutoLayout( true )
		panel.SetSizer( item0 )
		
		item0.Fit( panel )
		item0.SetSizeHints( panel )
		
		self.SetSize(size)
		self.SetPosition(pos)

	def OnSelectItem(self, evt):
		# Figure out which item it is
		id = self.tree.GetPyData(evt.GetItem())
		
		# Okay we need to post an event now
		new_evt = WindowsSelectObj(id)
		self.app.windows.PostEvent(new_evt)

	# Recenter onto the selected object
	def OnSelect(self, evt):
		g = self.app.game
	
		id = evt.value
		
		# The object that was selected.
		object = g.universe.Object(id)

		if object:
			# Set which orders can be added to this object
			self.obj['Orders'].Clear()
			for id in object.orders_valid:
				order = g.descs.OrderDesc(id)
				if order:
					self.obj['Orders'].Append(order.name, id)
				else:
					self.obj['Orders'].Append("Waiting on description for (%i)" % id, id)
		
			# Okay display the orders on this object
			# orders = Object.Get()
		

# The display for an ARG_COORD
ID_X = 10062
ID_Y = 10063
ID_Z = 10064
ID_PICKPOS = 10065

def argCoord( parent, call_fit = true, set_sizer = true ):
	item0 = wxBoxSizer( wxHORIZONTAL )
	
	item1 = wxStaticText( parent, ID_TEXT, "X", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

	item2 = wxSpinCtrl( parent, ID_X, "0", wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, 0 )
	item0.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

	item3 = wxStaticText( parent, ID_TEXT, "Y", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

	item4 = wxSpinCtrl( parent, ID_Y, "0", wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, 0 )
	item0.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

	item5 = wxStaticText( parent, ID_TEXT, "Z", wxDefaultPosition, wxDefaultSize, 0 )
	item0.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

	item6 = wxSpinCtrl( parent, ID_Z, "0", wxDefaultPosition, wxSize(50,-1), wxSP_WRAP, 0, 100, 0 )
	item0.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

	item7 = wxButton( parent, ID_PICKPOS, "PP", wxDefaultPosition, wxSize(30,-1), 0 )
	item0.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

	if set_sizer == true:
		parent.SetAutoLayout( true )
		parent.SetSizer( item0 )
		if call_fit == true:
			item0.Fit( parent )
			item0.SetSizeHints( parent )
	
	return item0
