"""\
This module contains the idle objects finder display.
"""

# wxPython imports
import wx
import wx.gizmos
#from wx import *
import wx.lib.anchors

# Local imports
from windows.winBase import winReportXRC, ShiftMixIn
from windows.xrc.winIdleFinder import IdleFinderBase
# Shows messages from the game system to the player.
from extra.StateTracker import TrackerObject
class winIdleFinder(winReportXRC, IdleFinderBase, TrackerObject):
	title = _("Objects Without Orders")
	
	def __init__(self, application, parent):
		IdleFinderBase.__init__(self, parent)
		winReportXRC.__init__(self, application, parent)
		
		self.application = application
		self.oid = -1
		# Create a panel for the current window.
		self.idlelist.InsertColumn(0, "Item ID", width = 100)
		self.idlelist.InsertColumn(1, "Item Name", width = 200)
		self.idlelist.InsertColumn(2, "Item Type", width = 100)

		self.ascending = 1

		self.Bind(wx.EVT_SHOW, self.OnShow)
		self.Bind(wx.EVT_ACTIVATE, self.OnShow)
		self.idlelist.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.SelectObject)
		self.idlelist.Bind(wx.EVT_LIST_COL_CLICK, self.OnColClick)
		#self.idlelist.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.SelectObject)

	def OnShow(self, evt):
		"""\
		Runs when the window is shown.
		"""
		self.idlelist.DeleteAllItems()
		numinlist = 0
		universe = self.application.cache.objects.keys()
		for object in universe:
			numorders = 0
			if hasattr(self.application.cache.objects[object], "owner"):
				#if self.application.cache.objects[object].owner == self.application.cache.players[0].id:
					if object in self.application.cache.orders.keys():
						for listpos, node in enumerate(self.application.cache.orders[object]):
							numorders = numorders + 1
						if numorders == 0:
							self.idlelist.InsertStringItem(numinlist, "%d" % object)
							self.idlelist.SetStringItem(numinlist, 1, self.application.cache.objects[object].name)
							self.idlelist.SetItemData(numinlist, object)
							if self.application.cache.objects[object].subtype == 0:
								self.idlelist.SetStringItem(numinlist, 2, "Universe")
							elif self.application.cache.objects[object].subtype == 1:
								self.idlelist.SetStringItem(numinlist, 2, "Galaxy")
							elif self.application.cache.objects[object].subtype == 2:
								self.idlelist.SetStringItem(numinlist, 2, "System")
							elif self.application.cache.objects[object].subtype == 3:
								self.idlelist.SetStringItem(numinlist, 2, "Planet")
							elif self.application.cache.objects[object].subtype == 4:
								self.idlelist.SetStringItem(numinlist, 2, "Fleet")
							numinlist = numinlist + 1
		
	def Sort(self, d1, d2):
		data1 = self.GetColData(d1, self.col)
		data2 = self.GetColData(d2, self.col)
		if data1 == data2:
			return 0
		elif data1 > data2:
			return self.ascending*1
		else:
			return self.ascending*-1
				
	def GetColData(self, obj, col):
		if col == 0:
			return obj
		elif col == 1:
			return self.application.cache.objects[obj].name.lower()
		elif col == 2:
			return self.application.cache.objects[obj].subtype
	
	def OnColClick(self, event):
		self.col = event.GetColumn()
		self.ascending *= -1
		self.idlelist.SortItems(self.Sort)
		#event.Skip()
	
	def OnClose(self, evt):
		"""\
		Runs when the window is closed.
		"""
		self.Hide()
	
	# Config Functions (required by winBase.py) -----------------------------------------------------------------------------
	def ConfigDefault(self, config=None):
		"""\
		Fill out the config with defaults (if the options are not valid or nonexistant).
		"""
		return {}

	def ConfigSave(self):
		"""\
		Returns the configuration of the Window (and it's children).
		"""
		return {}
	
	def ConfigLoad(self, config={}):
		"""\
		Loads the configuration of the Window (and it's children).
		"""
		pass

	def ConfigUpdate(self):
		"""\
		Updates the config details using external sources.
		"""
		pass

	def ConfigDisplay(self, panel, sizer):
		"""\
		Display a config panel with all the config options.
		"""
		pass

	def ConfigDisplayUpdate(self, evt):
		"""\
		Update the Display because it's changed externally.
		"""
		pass
	
	def SelectObject(self, id):
		"""
		Called to select an object.
		"""
		TrackerObject.SelectObject(self, int(id.GetText()))
