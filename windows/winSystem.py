"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports

# wxPython imports
from wxPython.wx import *
from wxPython.gizmos import *

# Game imports
from utils import *
from game.events import *
from game import objects

# Local imports
from winBase import winBase
from events import *

# Show the universe
class winSystem(winBase):
	title = "System"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		# Setup to recieve game events
		self.app = application
		self.app.game.WinConnect(self)
		EVT_GAME_ARRIVEOBJ(self, self.OnGameArriveObj)

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
				self.il.Add(wxImage("graphics/blank.png").ConvertToBitmap())
				for i in self.icons.keys():
					self.icons[i] = self.il.Add(self.icons[i])

				self.SetImageList(self.il)

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
		splitter.SplitVertically(self.tree, self.value, 250)
		scroller.SetTargetWindow(self.tree)
		scroller.EnableScrolling(FALSE, FALSE)

		self.value.SetTreeCtrl(self.tree)
		self.tree.SetCompanionWindow(self.value)

		EVT_TREE_SEL_CHANGED(self.tree, -1, self.OnSelectItem)

	def Update(self):

		# Remove all the current items
		self.tree.DeleteAllItems()

		universe=self.app.game.universe.Object(0)
		self.Add(None, universe)
		
		# Append some padding
		#for i in range(10):
		#	item = self.tree.AppendItem(root, "")
	
	def Add(self, root, object):
		new_root = None
		
		if isinstance(object, objects.Actual):
			new_root = self.tree.AppendItem(root, object.name, self.tree.icons['Planet'])
		
		elif isinstance(object, objects.Container):
			if root == None:
				new_root = self.tree.AddRoot("Known Universe")
			else:
				new_root = self.tree.AppendItem(root, object.name, self.tree.icons['System'])
			
			for id in object.contains:
				new = self.app.game.universe.Object(id)
				self.Add(new_root, new)
			
		else:
			self.tree.AppendItem(root, "Unknown", self.tree.icons['Ship'])
		
		if new_root:
			self.tree.SetPyData(new_root, object.id)

	def OnGameArriveObj(self, evt):
		# Okay lets rebuild our tree
		self.Update()
	
	def OnSelectItem(self, evt):
		# Figure out which item it is
		id = self.tree.GetPyData(evt.GetItem())
		
		# Okay we need to post an event now
		new_evt = WindowsSelectObj(id)
		self.app.windows.PostEvent(new_evt)
