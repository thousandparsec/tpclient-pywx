"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
import random
import os.path

# wxPython imports
import wx
import wx.gizmos

# Local imports
from requirements import graphicsdir
import defaults
from winBase import *
from utils import *

NAME = 0
DESC = 1

##class winSystem(winBase):
##	def __init__(self, application, parent):
##		winBase.__init__(self, application, parent)
##
##		self.Panel = panelSystem(application, self)
##
##	def __getattr__(self, key):
##		try:
##			return winBase.__getattr__(self, key)
##		except AttributeError:
##			return getattr(self.Panel, key)

from xrc.panelSystem import panelSystemBase
class panelSystem(panelSystemBase):
	title = _("System")

	def __init__(self, application, parent):
		panelSystemBase.__init__(self, parent)

		# Setup to recieve game events
		self.application = application
		self.ignore = False

		self.Tree.SetWindowStyle(wx.TR_DEFAULT_STYLE | wx.TR_HAS_VARIABLE_ROW_HEIGHT)

		self.icons = {}
		self.icons['Blank']      = wx.Image(os.path.join(graphicsdir, "blank-icon.png")).ConvertToBitmap()
		self.icons['Root']       = wx.Image(os.path.join(graphicsdir, "tp-icon.png")).ConvertToBitmap()
		self.icons['Container']  = wx.Image(os.path.join(graphicsdir, "link-icon.png")).ConvertToBitmap()
		self.icons['StarSystem'] = wx.Image(os.path.join(graphicsdir, "system-icon.png")).ConvertToBitmap()
		self.icons['Fleet']      = wx.Image(os.path.join(graphicsdir, "ship-icon.png")).ConvertToBitmap()
		self.icons['Planet']     = wx.Image(os.path.join(graphicsdir, "planet-icon.png")).ConvertToBitmap()
		self.icons['Unknown']    = wx.Image(os.path.join(graphicsdir, "starbase-icon.png")).ConvertToBitmap()

		self.il = wx.ImageList(16, 16)
		self.il.Add(wx.Image(os.path.join(graphicsdir, "blank.png")).ConvertToBitmap())
		for i in self.icons.keys():
			self.icons[i] = self.il.Add(self.icons[i])
		self.Tree.SetImageList(self.il)

		self.Tree.SetFont(wx.local.normalFont)
		self.Tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectItem)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()

		info.MinSize(wx.Size(200,-1))

		info.Right()
		info.Layer(1)
		info.PinButton(True)
		return info

	def Rebuild(self):
		"""\
		Rebuilds the list of objects.
		"""
		try:
			selected_id = self.Tree.GetPyData(self.Tree.GetSelection())
		except:
			selected_id = -1

		if not selected_id:
			selected_id = -1
			
		# Remove all the current items
		self.Tree.DeleteAllItems()

		universe = self.application.cache.objects[0]
		selected = self.Add(None, universe, selected_id)
	
		self.Tree.SortChildren(self.Tree.GetRootItem())
	
		if selected:
			self.Tree.SelectItem(selected)
			self.Tree.EnsureVisible(selected)
		
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
			new_root = self.Tree.AddRoot(_("Known Universe"), self.icons['Root'])
		else:
			if object != None:
				if self.icons.has_key(object.__class__.__name__):
					new_root = self.Tree.AppendItem(root, caption, self.icons[object.__class__.__name__])
				else:
					new_root = self.Tree.AppendItem(root, caption, self.icons['Unknown'])
		
		if object != None and hasattr(object, "owner") and object.owner != -1:
			self.Tree.SetItemTextColour(new_root, object.owner == self.application.cache.players[0].id and 'DarkGreen' or 'DarkRed')

		if hasattr(object, "contains"):
			for id in object.contains:
				if not self.application.cache.objects.has_key(id):
					continue
				new = self.application.cache.objects[id]
				temp = self.Add(new_root, new, selected_id)

				if temp:
					selected = temp
		
		if new_root:
			self.Tree.SetPyData(new_root, object.id)

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
		id = self.Tree.GetPyData(evt.GetItem())
		
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
		id = self.Tree.GetPyData(self.Tree.GetSelection())
		if id == evt.id:
			return
		
		item = self.Tree.FindItemByData(evt.id)
		if item:
			self.ignore = True
			
			#self.Tree.CollapseAll()		# Collapse all the other stuff
			self.Tree.SelectItem(item)		# Select Item
			if not self.Tree.IsVisible(item):
				self.Tree.EnsureVisible(item)
			self.Tree.Expand(item)			# Expand the Item

			self.ignore = False
	
		self.Refresh()
