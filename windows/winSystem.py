
from winBase import winBase

from wxPython.wx import *
from wxPython.gizmos import *

# Show the currently selected system
class winSystem(winBase):
	title = "System"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)
		
		class systemTree(wxRemotelyScrolledTreeCtrl):
			def __init__(self, parent, ID, pos=wxDefaultPosition, size=wxDefaultSize, style=wxTR_HAS_BUTTONS):
				wxRemotelyScrolledTreeCtrl.__init__(self, parent, ID, pos, size, style)

				self.icons = {}
				self.icons['System'] = wxImage("graphics/system-icon.png").ConvertToBitmap()
				self.icons['Ship'] = wxImage("graphics/ship-icon.png").ConvertToBitmap()
				self.icons['Starbase'] = wxImage("graphics/starbase-icon.png").ConvertToBitmap()
				self.icons['Planet'] = wxImage("graphics/planet-icon.png").ConvertToBitmap()
				self.icons['Link'] = wxImage("graphics/link-icon.png").ConvertToBitmap()


				# make an image list
				self.il = wxImageList(16, 16)
				for i in self.icons.keys():
					self.icons[i] = self.il.Add(self.icons[i])

				self.SetImageList(self.il)

				# Add some items
				root = self.AddRoot("Root")
				item = self.AppendItem(root, "System", self.icons['System'])
				child = self.AppendItem(item, "Planet 1", self.icons['Planet'])
				child2 = self.AppendItem(child, "Starbase", self.icons['Starbase'])
				child2 = self.AppendItem(child, "Ship 2", self.icons['Ship'])
				child = self.AppendItem(item, "Free Ship", self.icons['Ship'])
				child = self.AppendItem(item, "Link to ABC", self.icons['Link'])

				for i in range(10):
					item = self.AppendItem(root, "")
				
				self.Expand(root)

		class systemValueWindow(wxTreeCompanionWindow):
			def __init__(self, parent, ID, pos=wxDefaultPosition, size=wxDefaultSize, style=0):
				wxTreeCompanionWindow.__init__(self, parent, ID, pos, size, style)
				self.SetBackgroundColour("WHITE")
				EVT_ERASE_BACKGROUND(self, self.OEB)

			def OEB(self, evt):
				pass

			# This method is called to draw each item in the value window
			def DrawItem(self, dc, itemId, rect):
				tree = self.GetTreeCtrl()
				if tree:

					text = tree.GetItemText(itemId)

					# Draw the seperator
					dc.SetPen(wxPen(wxSystemSettings_GetSystemColour(wxSYS_COLOUR_3DLIGHT), 1, wxSOLID))
					dc.SetBrush(wxBrush(self.GetBackgroundColour(), wxSOLID))
					dc.DrawRectangle(rect.x, rect.y, rect.width+1, rect.height+1)

					# Draw the text 
					dc.SetTextForeground("BLACK")
					dc.SetBackgroundMode(wxTRANSPARENT)
					tw, th = dc.GetTextExtent(text)
					x = 5
					y = rect.y + max(0, (rect.height - th) / 2)
					dc.DrawText(text, x, y)


		scroller = wxSplitterScrolledWindow(self, -1, (50,50), (350, 250), style=wxNO_BORDER | wxCLIP_CHILDREN | wxVSCROLL)
		splitter = wxThinSplitterWindow(scroller, -1, style=wxSP_3DBORDER | wxCLIP_CHILDREN)
		splitter.SetSashSize(3)
		
		self.tree = systemTree(splitter, -1, style = wxTR_HAS_BUTTONS | wxTR_NO_LINES | wxTR_ROW_LINES | wxNO_BORDER )
		
		self.value = systemValueWindow(splitter, -1, style=wxNO_BORDER)

		# SET THE SPLITTER HERE!!! -> It's the last value
		splitter.SplitVertically(self.tree, self.value, 150)
		scroller.SetTargetWindow(self.tree)
		scroller.EnableScrolling(FALSE, FALSE)

		self.value.SetTreeCtrl(self.tree)
		self.tree.SetCompanionWindow(self.value)
		
