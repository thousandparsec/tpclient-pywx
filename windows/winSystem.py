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

# Program imports
from extra.wxPostEvent import *

# Show the universe
class winSystem(winBase):
	title = "System"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		# Setup to recieve game events
		self.app = application
		self.app.game.WinConnect(self)
		EVT_GAME_OBJ_ARRIVE(self, self.OnGameArriveObj)

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

		selected_id = self.tree.GetPyData(self.tree.GetSelection())
		if not selected_id:
			selected_id = -1
			
		debug(DEBUG_WINDOWS, "Currently selected object... %i" % selected_id)
		
		# Remove all the current items
		self.tree.DeleteAllItems()

		universe=self.app.game.universe.Object(0)
		selected = self.Add(None, universe, selected_id)
	
		if selected:
			debug(DEBUG_WINDOWS, "Trying to reselect an object... %s" % self.tree.GetPyData(selected))
			self.tree.SelectItem(selected)
			self.tree.EnsureVisible(selected)
			new_evt = WindowsObjSelect(self.tree.GetPyData(selected))
			wxPostEvent(new_evt)
		
	def Add(self, root, object, selected_id=-1):
		selected = None
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
				temp = self.Add(new_root, new, selected_id)

				if temp:
					selected = temp

		else:
			self.tree.AppendItem(root, "Unknown", self.tree.icons['Ship'])
		
		if new_root:
			self.tree.SetPyData(new_root, object.id)

			if object.id == selected_id:
				return new_root
			elif selected:
				return selected
				
		return

	def OnGameArriveObj(self, evt):
		self.Update()

#		g = self.app.game
#		selected = self.tree.GetSelection()
#		
#		object = g.universe.Object(evt.id)
#		parent = g.universe.Object(object.parent)
#
#		# Find the parent of this object
#		root = self.tree.GetItem()
#		new_root = self.tree.AppendItem(root, object.name, self.tree.icons['System'])
#
#		self.tree.SetSelection(selected)
#		self.tree.EnsureVisible(selected)
#		if self.tree.GetPyData(selected) == evt.id:
#			# Okay we need to post an event now
#			new_evt = WindowsObjSelect(evt.id)
#			wxPostEvent(new_evt)
	
	def OnSelectItem(self, evt):
		# Figure out which item it is
		id = self.tree.GetPyData(evt.GetItem())
		
		# Okay we need to post an event now
		new_evt = WindowsObjSelect(id)
		wxPostEvent(new_evt)



