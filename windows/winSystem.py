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
class panelSystem(wx.Panel):
	title = _("System")

	from defaults import winSystemDefaultSize as DefaultSize
	
	def __init__(self, application, parent):
		wx.Panel.__init__(self, parent)

		# Setup to recieve game events
		self.application = application
		self.ignore = False

		self.tree = wx.OrderedTreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)

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
		self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectItem)

		self.Bind(wx.EVT_SIZE, self.OnSize)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(self.GetMinSize())
		info.Bottom()
		info.Layer(1)
		return info

	def OnSize(self, evt):
		self.tree.SetSize(self.GetClientSize())

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
			
		# Remove all the current items
		self.tree.DeleteAllItems()

		universe = self.application.cache.objects[0]
		selected = self.Add(None, universe, selected_id)
	
		self.tree.SortChildren(self.tree.GetRootItem())
	
		if selected:
			self.tree.SelectItem(selected)
			self.tree.EnsureVisible(selected)
		
	def ObjectTurnSummary(self, object):
		"""\
		Builds a brief string, identifying the number of turns remaining
		on the given object's current order, and the total number of turns
		allocated to all future scheduled orders.
		"""
		orders = self.application.cache.orders[object.id]
		if len(orders) == 0:
			return "#"
		elif len(orders) == 1:
			return str(orders[0].turns)
		else:
			turns = 0
			for order in orders:
				turns += order.turns
			turns -= orders[0].turns

			return str(orders[0].turns) + ", " + str(turns)

	def Add(self, root, object, selected_id=-1):
		"""\
		Recursive method which builds the object list.
		"""
		selected = None
		new_root = None
		orderable = object != None and hasattr(object, "order_types") and len(object.order_types) > 0

		caption = object.name

		if orderable:
			caption += "  [" + self.ObjectTurnSummary(object) + "]"
		
		if root == None:
			new_root = self.tree.AddRoot(_("Known Universe"), self.icons['Root'])
		else:
			if object != None:
				if self.icons.has_key(object.__class__.__name__):
					new_root = self.tree.AppendItem(root, caption, self.icons[object.__class__.__name__])
				else:
					new_root = self.tree.AppendItem(root, caption, self.icons['Unknown'])
		
		if object != None and hasattr(object, "owner") and object.owner != -1:
			self.tree.SetItemTextColour(new_root, object.owner == self.application.cache.players[0].id and 'DarkGreen' or 'DarkRed')

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
			
			#self.tree.CollapseAll()			# Collapse all the other stuff
			self.tree.SelectItem(item)		# Select Item
			if not self.tree.IsVisible(item):
				self.tree.EnsureVisible(item)
			self.tree.Expand(item)			# Expand the Item

			self.ignore = False
	
		self.Refresh()
