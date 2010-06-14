"""\
This module contains the System window. The System window displays all objects
at this current location and "quick" details about them.
"""

# Python imports
import random
import os.path
import sys

# wxPython imports
import wx
import wx.gizmos

# Local imports
from requirements import graphicsdir

from extra import objectutils

NAME = 0
DESC = 1

from tp.client.threads import FileTrackerMixin
from extra.StateTracker import TrackerObject
from windows.xrc.panelSystem import panelSystemBase
class panelSystem(panelSystemBase, TrackerObject, FileTrackerMixin):
	title = _("System")

	def __init__(self, application, parent):
		panelSystemBase.__init__(self, parent)
		FileTrackerMixin.__init__(self, application)
		self.parent = parent

		# Setup to recieve game events
		self.application = application

		self.SelectIgnore     = False
		self.SelectedPrevious = None

		self.icons = {}
		self.icons['Blank']      = wx.Image(os.path.join(graphicsdir, "blank-icon.png")).ConvertToBitmap()
		self.icons['Root']       = wx.Image(os.path.join(graphicsdir, "tp-icon.png")).ConvertToBitmap()
		self.icons['Container']  = wx.Image(os.path.join(graphicsdir, "link-icon.png")).ConvertToBitmap()
		self.icons['StarSystem'] = wx.Image(os.path.join(graphicsdir, "system-icon.png")).ConvertToBitmap()
		self.icons['Fleet']      = wx.Image(os.path.join(graphicsdir, "ship-icon.png")).ConvertToBitmap()
		self.icons['Planet']     = wx.Image(os.path.join(graphicsdir, "planet-icon.png")).ConvertToBitmap()
		self.icons['Wormhole']   = wx.Image(os.path.join(graphicsdir, "link-icon.png")).ConvertToBitmap()
		self.icons['Unknown']    = wx.Image(os.path.join(graphicsdir, "unknown-icon.png")).ConvertToBitmap()
		self.icons['Loading']    = wx.Image(os.path.join(graphicsdir, "blank-icon.png")).ConvertToBitmap()

		self.il = wx.ImageList(16, 16)
		self.il.Add(wx.Image(os.path.join(graphicsdir, "blank.png")).ConvertToBitmap())
		for i in self.icons.keys():
			self.icons[i] = self.il.Add(self.icons[i])
		self.Tree.SetImageList(self.il)

		self.Tree.SetFont(wx.local.normalFont)
		self.Tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectItem)

		self.NextObject.Bind(wx.EVT_BUTTON, self.OnNextObject)
		self.PrevObject.Bind(wx.EVT_BUTTON, self.OnPrevObject)
		self.StepInto.Bind(wx.EVT_BUTTON, self.OnStepInto)

		self.Search.Bind(wx.EVT_TEXT, self.Rebuild)
		self.Search.Bind(wx.EVT_TEXT_ENTER, self.Rebuild)
		self.Search.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.Rebuild)
		self.Search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel)

		self.application.gui.Binder(self.application.CacheClass.CacheUpdateEvent, self.OnCacheUpdate)
		self.application.gui.Binder(self.application.gui.SelectObjectEvent, self.OnSelectObject)
		
		self.Bind(wx.EVT_SIZE, self.OnResize)
		self.Layout()

		TrackerObject.__init__(self)

	def OnMediaDownloadDone(self, evt):
		self.Layout()
		self.Update()

		if evt is None:
			return

		if self.CheckURL(evt.file):
			self.RemoveURL(evt.file)
			self.Rebuild()
		
	def OnMediaUpdate(self, evt):
		self.Rebuild()

	def OnResize(self, evt):
		if sys.platform == "darwin":
			self.Tree.SetMinSize((-1,self.GetSize()[1]-self.Search.GetBestSize()[1]-self.StepInto.GetBestSize()[1]-10))
		else:
			self.Tree.SetMinSize((-1,self.GetSize()[1]-self.Search.GetBestSize()[1]-self.StepInto.GetBestSize()[1]))
		self.Layout()
		evt.Skip()

	def OnSearchCancel(self, evt):
		self.Search.SetValue("")
		self.Rebuild()

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()

		s = wx.Size(self.parent.GetSize()[0]/5, -1)
		info.MinSize(s)
		info.BestSize(s)

		info.Right()
		info.Layer(1)
		info.PinButton(True)
		info.CaptionVisible(True)
		info.Caption(self.title)
		return info

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
			return unicode(orders.first.CurrentOrder.turns)
		else:
			turns = 0
			for node in orders[1:]:
				turns += node.CurrentOrder.turns

			return unicode(orders.first.CurrentOrder.turns) + ", " + unicode(turns)

	def Rebuild(self, evt=None):
		"""\
		Rebuilds the list of objects.
		"""
		self.SelectIgnore = True

		selected = self.Tree.GetPyData(self.Tree.GetSelection())
		if selected != None:
			self.SelectedPrevious = selected
		else:
			selected = self.SelectedPrevious

		self.Tree.Freeze()

		# Remove all the current items
		self.Tree.DeleteAllItems()

		self.Add(None, self.application.cache.objects[0], selected)

		# Sort the tree
		self.Tree.SortChildren(self.Tree.GetRootItem())
	
		if self.Filter != '*':
			self.Tree.ExpandAll()

		# Reselect the previously selected item..
		selecteditem = self.Tree.GetSelection()
		if self.Tree.GetPyData(selecteditem) != None:
			self.Tree.EnsureVisible(selecteditem)

		self.Tree.Thaw()

		self.SelectIgnore = False

	def Filter(self):
		filter = self.Search.GetValue()
		if len(filter) == 0:
			return "*"
		elif not '*' in filter:
			return '*'+filter.lower()+'*'
		else:
			return filter

	Filter = property(Filter)

	def Add(self, parent, object, selected=None):
		# Figure out the caption for this text...
		caption = object.name
		if object != None and hasattr(object, "order_types") and len(object.order_types) > 0:
			caption += "  [" + self.ObjectTurnSummary(object) + "]"
			
		# Add the item
		if parent is None:
			if self.Filter == '*':
				item = self.Tree.AddRoot(_("Known Universe"), self.icons['Root'])
				self.Tree.SetPyData(item, 0)
			else:
				item = self.Tree.AddRoot(_("Finding %s") % self.Filter, self.icons['Root'])
		else:
			# Filter the list..
			from fnmatch import fnmatch as match
			if match(caption.lower(), self.Filter.lower()):
				# Do something about multiple icons for the object?
				images = self.application.media.getImages(object.id)
				self.AddObjectURLs(object.id)
				if len(images) <= 0:
					icon = self.icons['Loading']
				else:
					foundimage = False
					for name, files in images:
						if not "Icon" in name:
							continue
						
						foundimage = True
						icon = self.il.Add(wx.Image(files[0]).ConvertToBitmap())
						break
					
					if not foundimage:
						icon = self.icons['Unknown']

				item = self.Tree.AppendItem(parent, caption, icon)
				self.Tree.SetPyData(item, object.id)

				if selected == object.id:
					self.Tree.SelectItem(item)
			else:
				item = parent

		if selected != object.id:
			self.Tree.UnselectItem(item)

		if hasattr(object, "contains"):
			for id in object.contains:
				self.Add(item, self.application.cache.objects[id], selected)

	def OnSelectItem(self, evt):
		"""\
		When somebody selects an item on the list.
		"""
		if self.SelectIgnore:
			return

		if not evt.GetItem().IsOk():
			return

		# Figure out which item it is
		id = self.Tree.GetPyData(evt.GetItem())
		if id != None:
			# Okay we need to post an event now
			self.oid = id
			self.application.Post(self.application.gui.SelectObjectEvent(id), source=self)
				
		self.Refresh()
	
	def OnNextObject(self, evt):
		"""\
		When someone clicks the "Next Object" button.
		"""
		self.SelectNextObject()
	
	def OnPrevObject(self, evt):
		"""\
		When someone clicks the "Prev Object" button.
		"""
		self.SelectPreviousObject()
	
	def OnStepInto(self, evt):
		"""\
		When someone clicks the "Step Into" button.
		"""
		self.SelectNextChild()

	####################################################
	# Remote Event Handlers
	####################################################
	def OnCacheUpdate(self, evt):
		self.Rebuild()

	def OnSelectObject(self, evt):
		"""\
		When somebody selects an object.
		"""
		TrackerObject.OnSelectObject(self, evt)
		id = self.Tree.GetPyData(self.Tree.GetSelection())
		if id == evt.id:
			return
		
		item = self.Tree.FindItemByData(evt.id)
		if item:
			self.SelectIgnore = True
			
			#self.Tree.CollapseAll()		# Collapse all the other stuff
			self.Tree.SelectItem(item)		# Select Item
			if not self.Tree.IsVisible(item):
				self.Tree.EnsureVisible(item)
			self.Tree.Expand(item)			# Expand the Item

			self.SelectIgnore = False
	
		self.Refresh()
