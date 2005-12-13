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
import defaults
from winBase import *
from utils import *

NAME = 0
DESC = 1

# Show the universe
class winSystem(winBase):
	title = _("System")
	
	from defaults import winSystemDefaultPosition as DefaultPosition
	from defaults import winSystemDefaultSize as DefaultSize
	from defaults import winSystemDefaultShow as DefaultShow
	
	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		# Setup to recieve game events
		self.application = application
		self.ignore = False

		self.tree = wx.gizmos.TreeListCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)

		self.icons = {}
		self.icons['Blank'] = wx.Image("graphics/blank-icon.png").ConvertToBitmap()
		self.icons['Root'] = wx.Image("graphics/tp-icon.png").ConvertToBitmap()
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
		self.tree.AddColumn(_("Object"))
#		self.tree.AddColumn("Details")
		self.tree.SetMainColumn(0)
		self.tree.SetColumnWidth(0, 225)

		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectItem)

	def Rebuild(self):
		"""\
		Rebuilds the list of objects.
		"""
		try:
			selected_id = self.tree.GetPyData(self.tree.GetSelection())
		except:
			selected_id = -1

		if not selected_id:
			selected_id = -1
			
		debug(DEBUG_GUI, "Selecting object... %i" % selected_id)
		
		# Remove all the current items
		self.tree.DeleteAllItems()

		universe = self.application.cache.objects[0]
		selected = self.Add(None, universe, selected_id)
	
		if selected:
			debug(DEBUG_GUI, "Trying select object... %i" % self.tree.GetPyData(selected))
			self.tree.SelectItem(selected)
			self.tree.EnsureVisible(selected)
		
	def Add(self, root, object, selected_id=-1):
		"""\
		Recursive method which builds the object list.
		"""
		selected = None
		new_root = None
		
		if root == None:
			new_root = self.tree.AddRoot(_("Known Universe"), self.icons['Root'])
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
		if self.ignore:
			return

		# Figure out which item it is
		id = self.tree.GetPyData(evt.GetItem())
		
		# Okay we need to post an event now
		self.application.Post(self.application.gui.SelectObjectEvent(id))
		
		self.Refresh()

	####################################################
	# Remote Event Handlers
	####################################################
	def OnCacheUpdate(self, evt):
		self.Rebuild()

	def OnSelectObject(self, evt):
		"""\
		When somebody selects an object.
		"""
		id = self.tree.GetPyData(self.tree.GetSelection())
		if id == evt.id:
			return
		
		item = self.tree.FindItemByData(evt.id)
		if item:
			self.ignore = True
			
			self.tree.CollapseAll()			# Collapse all the other stuff
			self.tree.SelectItem(item)		# Select Item
			if not self.tree.IsVisible(item):
				self.tree.EnsureVisible(item)
			self.tree.Expand(item)			# Expand the Item

			self.ignore = False
	
		self.Refresh()
