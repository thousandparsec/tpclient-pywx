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

# tp imports
from tp.netlib.objects                        import Object, OrderDescs
from tp.netlib.objects.ObjectExtra.Universe   import Universe
from tp.netlib.objects.ObjectExtra.Galaxy     import Galaxy
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet     import Planet
from tp.netlib.objects.ObjectExtra.Fleet      import Fleet

class winIdleFinder(winReportXRC, IdleFinderBase, TrackerObject):
	"""\
	This window shows a list of objects you own that do not have any orders.
	
	You can use the window to quickly find fleets and planets that are idle,
	and you can double-click on any of these objects to select them.
	
	Clicking on a column heading will sort the list by the data in that column,
	and clicking again on the heading will reverse the sort order.
	
	To refresh the data, close the window and reopen it.
	"""
	
	title = _("Objects Without Orders")
	
	def __init__(self, application, parent):
		"""\
		Create the IdleFinder window and initialize the columns and event bindings.
		"""
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

	def OnShow(self, evt):
		"""\
		Runs when the window is shown. Finds idle objects and adds them to the list.
		"""
		self.idlelist.DeleteAllItems()
		numinlist = 0
		universe = self.application.cache.objects.keys()
		for object in universe:
			numorders = 0
			# The object must have an owner to have orders
			if not hasattr(self.application.cache.objects[object], "owner"):
				continue
			
			# Only show objects owned by this player
			if self.application.cache.objects[object].owner != self.application.cache.players[0].id:
				continue
				
			if object in self.application.cache.orders.keys():
				# Find any orders for this object
				for listpos, node in enumerate(self.application.cache.orders[object]):
					numorders = numorders + 1
				
				# If the object has no orders, add it to the list
				if numorders == 0:
					self.idlelist.InsertStringItem(numinlist, "%d" % object)
					self.idlelist.SetStringItem(numinlist, 1, self.application.cache.objects[object].name)
					self.idlelist.SetItemData(numinlist, object)
					
					# Determine object's type
					if isinstance(self.application.cache.objects[object], Universe):
						self.idlelist.SetStringItem(numinlist, 2, "Universe")
					elif isinstance(self.application.cache.objects[object], Galaxy):
						self.idlelist.SetStringItem(numinlist, 2, "Galaxy")
					elif isinstance(self.application.cache.objects[object], StarSystem):
						self.idlelist.SetStringItem(numinlist, 2, "System")
					elif isinstance(self.application.cache.objects[object], Planet):
						self.idlelist.SetStringItem(numinlist, 2, "Planet")
					elif isinstance(self.application.cache.objects[object], Fleet):
						self.idlelist.SetStringItem(numinlist, 2, "Fleet")
					else:
						self.idlelist.SetStringItem(numinlist, 2, "Unknown")
						
					numinlist = numinlist + 1
		
	def Sort(self, d1, d2):
		"""\
		Simple sorting routine. Compares two objects and returns a value indicating which should be first, based on the current ascending or descending sort order.
		"""
		data1 = self.GetColData(d1, self.col)
		data2 = self.GetColData(d2, self.col)
		if data1 == data2:
			return 0
		elif data1 > data2:
			return self.ascending*1
		else:
			return self.ascending*-1
				
	def GetColData(self, obj, col):
		"""\
		Finds the data held in a specific column of a specific row of the Idle Objects list.
		"""
		if col == 0:
			return obj
		elif col == 1:
			return self.application.cache.objects[obj].name.lower()
		elif col == 2:
			return self.application.cache.objects[obj].subtype
	
	def OnColClick(self, event):
		"""\
		Reverse sort order, then re-sort, when list column heading is clicked.
		"""
		self.col = event.GetColumn()
		self.ascending *= -1
		self.idlelist.SortItems(self.Sort)
	
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
