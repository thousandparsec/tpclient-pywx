"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
import random

# wxPython imports
import wx
import wx.gizmos

# Local imports
from winBase import *
from utils import *

NAME = 0
DESC = 1

class TreeListCtrl(wx.gizmos.TreeListCtrl):
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
				cookieo = -1
				child, cookie = self.GetFirstChild(item)

				while cookieo != cookie:
					r = self.FindItemByData(pyData, child)
					if r:
						return r
					
					cookieo = cookie
					child, cookie = self.GetNextChild(item, cookie)

		return None

	def CollapseAll(self, item=None):
		if item == None:
			item = self.GetRootItem()

		if self.ItemHasChildren(item):
			cookieo = -1
			child, cookie = self.GetFirstChild(item)

			while cookieo != cookie:
				self.CollapseAll(child)
			
				cookieo = cookie
				child, cookie = self.GetNextChild(item, cookie)

		self.Collapse(item)

wx.gizmos.TreeListCtrl = TreeListCtrl

# Show the universe
class winSystem(winBase):
	title = "System"
	
	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		# Setup to recieve game events
		self.application = application

		self.tree = wx.gizmos.TreeListCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)

		self.icons = {}
		self.icons['Blank'] = wx.Image("graphics/blank-icon.png").ConvertToBitmap()
		self.icons['Container'] = wx.Image("graphics/link-icon.png").ConvertToBitmap()
		self.icons['StarSystem'] = wx.Image("graphics/system-icon.png").ConvertToBitmap()
		self.icons['Fleet'] = wx.Image("graphics/ship-icon.png").ConvertToBitmap()
		self.icons['Planet'] = wx.Image("graphics/planet-icon.png").ConvertToBitmap()
		self.icons['Unknown'] = wx.Image("graphics/starbase-icon.png").ConvertToBitmap()

		self.il = wx.ImageList(16, 16)
		self.il.Add(wx.Image("graphics/blank.png").ConvertToBitmap())
		for i in self.icons.keys():
			self.icons[i] = self.il.Add(self.icons[i])
		self.tree.SetImageList(self.il)

		self.tree.SetFont(wx.local.normalFont)

		# create some columns
		self.tree.AddColumn("Object")
#		self.tree.AddColumn("Details")
		self.tree.SetMainColumn(0)
		self.tree.SetColumnWidth(0, 225)

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectItem)

	def Rebuild(self):
		"""\
		Rebuilds the list of objects.
		"""
		selected_id = self.tree.GetPyData(self.tree.GetSelection())
		if not selected_id:
			selected_id = -1
			
		debug(DEBUG_WINDOWS, "Selecting object... %i" % selected_id)
		
		# Remove all the current items
		self.tree.DeleteAllItems()

		universe = self.application.cache.objects[0]
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
				if not self.application.cache.objects.has_key(id):
					continue
				new = self.application.cache.objects[id]
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

	def OnSelectItem(self, evt):
		"""\
		When somebody selects an item on the list.
		"""
		# Figure out which item it is
		id = self.tree.GetPyData(evt.GetItem())
		
		# Okay we need to post an event now
		self.application.windows.Post(wx.local.SelectObjectEvent(id))

	def OnCacheUpdate(self, evt):
		self.Rebuild()

	def OnSelectObject(self, evt):
		"""\
		When somebody selects an object.
		"""
		debug(DEBUG_WINDOWS, "Selecting object... %i" % evt.id)
		
		item = self.tree.FindItemByData(evt.id)
		if item:
			self.tree.CollapseAll()			# Collapse all the other stuff
			self.tree.SelectItem(item)		# Select Item
			self.tree.Expand(item)			# Expand the Item
			self.tree.EnsureVisible(item)
