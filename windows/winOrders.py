
from wxPython.wx import *

# Shows the currently selected object's orders
class winOrders(wxFrame):
	pass


ORDER_LIST = 10010
ORDER_LINE = 10011
ORDER_NEW = 10012
ORDER_DELETE = 10013
ORDER_EDIT = 10014

def panelOrders( parent, call_fit = true, set_sizer = true ):
    item0 = wxFlexGridSizer( 0, 1, 0, 0 )
    item0.AddGrowableCol( 0 )
    item0.AddGrowableRow( 0 )
    item0.AddGrowableRow( 4 )
    
    item1 = wxListCtrl( parent, ORDER_LIST, wxDefaultPosition, wxSize(160,120), wxLC_REPORT|wxSUNKEN_BORDER )
    item0.AddWindow( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item2 = wxStaticLine( parent, ORDER_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

    item3 = wxFlexGridSizer( 1, 0, 0, 0 )
    
    item4 = wxButton( parent, ORDER_NEW, "New Order", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

    item5 = wxButton( parent, ORDER_DELETE, "Delete Order", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item6 = wxStaticLine( parent, ORDER_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

    item7 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item8 = parent.FindWindowById( ORDER_EDIT )
    item7.AddWindow( item8, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item7, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0
