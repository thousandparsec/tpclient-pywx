"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
import random

# wxPython imports
from wxPython.wx import *
from wxPython.gizmos import wxTreeListCtrl

# Game imports
from utils import *

# Local imports
from winBase import *

# Program imports

NAME = 0
DESC = 1

class wxTreeListCtrl(wxTreeListCtrl):
	"""\
	Modified object which includes the ability to get an object by the pyData
	"""
	def FindItemByData(self, pyData, item=None):
		if item == None:
			item = self.GetRootItem()

		if self.GetPyData(item) == pyData:
			return item
		else:
			if self.ItemHasChildren(item):
				child, cookie = self.GetFirstChild(item)

				while child != None:
					r = self.FindItemByData(pyData, child)
					if r:
						return r
					
					child, cookie = self.GetNextChild(item, cookie)

		return None

# Show the universe
class winSystem(winBase):
	title = "System"
	
	def __init__(self, application, parent, pos=wxDefaultPosition, size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		# Setup to recieve game events
		self.application = application

		self.tree = wxTreeListCtrl(self, -1, style = wxTR_DEFAULT_STYLE)

		self.icons = {}
		self.icons['Blank'] = wxImage("graphics/blank-icon.png").ConvertToBitmap()
		self.icons['Container'] = wxImage("graphics/link-icon.png").ConvertToBitmap()
		self.icons['StarSystem'] = wxImage("graphics/system-icon.png").ConvertToBitmap()
		self.icons['Fleet'] = wxImage("graphics/ship-icon.png").ConvertToBitmap()
		self.icons['Planet'] = wxImage("graphics/planet-icon.png").ConvertToBitmap()
		self.icons['Unknown'] = wxImage("graphics/starbase-icon.png").ConvertToBitmap()

		self.il = wxImageList(16, 16)
		self.il.Add(wxImage("graphics/blank.png").ConvertToBitmap())
		for i in self.icons.keys():
			self.icons[i] = self.il.Add(self.icons[i])
		self.tree.SetImageList(self.il)
		
		# create some columns
		self.tree.AddColumn("Object")
		self.tree.AddColumn("Details")
		self.tree.SetMainColumn(0)
		self.tree.SetColumnWidth(0, 250)

		EVT_TREE_SEL_CHANGED(self.tree, -1, self.SelectItem)

		EVT_CACHE_UPDATE(self.application, self.Rebuild)
		EVT_SELECT_OBJECT(self.application, self.OnSelectObject)

	def Rebuild(self, evt):
		"""\
		Rebuilds the list of objects.
		"""
		selected_id = self.tree.GetPyData(self.tree.GetSelection())
		if not selected_id:
			selected_id = -1
			
		debug(DEBUG_WINDOWS, "Selecting object... %i" % selected_id)
		
		# Remove all the current items
		self.tree.DeleteAllItems()

		universe = self.application.cache[0]
		selected = self.Add(None, universe, selected_id)
	
		if selected:
			debug(DEBUG_WINDOWS, "Trying select object... %i" % self.tree.GetPyData(selected))
			self.tree.SelectItem(selected)
			self.tree.EnsureVisible(selected)
		
	def Add(self, root, object, selected_id=-1):
		"""\
		Recursive method which builds the object list.
		"""
		selected = None
		new_root = None
		
		if root == None:
			new_root = self.tree.AddRoot("Known Universe", self.icons['Blank'])
		else:
			if object != None:
				if self.icons.has_key(object.__class__.__name__):
					new_root = self.tree.AppendItem(root, object.name, self.icons[object.__class__.__name__])
				else:
					new_root = self.tree.AppendItem(root, object.name, self.icons['Unknown'])
		
		if hasattr(object, "contains"):
			for id in object.contains:
				new = self.application.cache[id]
				temp = self.Add(new_root, new, selected_id)

				if temp:
					selected = temp
		
		if new_root:
			self.tree.SetPyData(new_root, object.id)

			if object.id == selected_id:
				return new_root
			elif selected:
				return selected
		return

	def OnSelectObject(self, evt):
		"""\
		When somebody selects an object.
		"""
		debug(DEBUG_WINDOWS, "Selecting object... %i" % evt.id)
		item = self.tree.FindItemByData(evt.id)
		if item:
			self.tree.SelectItem(item)
			self.tree.EnsureVisible(item)

	def SelectItem(self, evt):
		"""\
		When somebody selects an item on the list.
		"""
		# Figure out which item it is
		id = self.tree.GetPyData(evt.GetItem())
		
		# Okay we need to post an event now
		wxPostEvent(self.application, SelectObjectEvent(id))

