"""\
This overlay draws Star Systems on the Starmap.
"""
# Python imports
from math import *
import copy
from cgi import escape

# wxPython imports
import wx
from extra.wxFloatCanvas.FloatCanvas   import Point, Group, Line
from extra.wxFloatCanvas.RelativePoint import RelativePoint, RelativePointSet
from extra.wxFloatCanvas.PolygonStatic import PolygonArrow, PolygonShip

# tp imports
from tp.netlib.objects.parameters import OrderParamAbsSpaceCoords, OrderParamObject
from tp.netlib.objects                        import Object, OrderDescs

from tp.netlib import GenericRS

from tp.client import objectutils

from Overlay   import SystemLevelOverlay, Holder
from Colorizer import *

def FindChildren(tmpcache, obj):
	"""
	Figure out all the children of this object.
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	kids = set()
	for cid in obj.contains:
		child = tmpcache.objects[cid]

		kids.update(FindChildren(tmpcache, child))
		kids.add(child)

	return list(kids)

def FindOwners(tmpcache, obj):
	"""
	Figure out the owners of this oidect (and it's children).
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	owners = set()
	for child in [obj]+FindChildren(tmpcache, obj):
		owner = objectutils.getOwner(tmpcache, child.id)

		if owner in (0, -1):
			continue
		owners.add(owner)
	return list(owners)

class IconMixIn:
	"""
	"""
	PrimarySize = 3
	ChildSize   = 3

	def __init__(self, tmpcache, colorizer):
		self.tmpcache = tmpcache
		self.SetColorizer(colorizer)

	# FIXME: Should probably just monkey patch this onto Group?
	def XY(self):
		return self.ObjectList[0].XY
	XY = property(XY)

	def GetSize(self):
		return (self.PrimarySize*2, self.PrimarySize*2)

	def ChildOffset(self, i):
		num = len(self.children)

		angle = ((2.0*pi)/num)*(i-0.125)
		return (int(cos(angle)*6), int(sin(angle)*6))

	def SetColorizer(self, colorizer):
		if not isinstance(colorizer, Colorizer):
			raise TypeError('Colorizer must be of Colorizer type!')
		self.Colorizer = colorizer

	def GetColors(self):
		parentcolor = self.Colorizer(FindOwners(self.tmpcache, self.primary))
		
		childrencolors = []
		for child in self.children:
			childrencolors.append(self.Colorizer(FindOwners(self.tmpcache, child)))
	
		return parentcolor, childrencolors

class SystemIcon(Group, Holder, IconMixIn):
	"""
	Display a round dot with a dot for each child.
	"""
	def copy(self):
		# FIXME: Very expensive
		return SystemIcon(self.tmpcache, self.primary, self.Colorizer)

	def __init__(self, tmpcache, system, colorizer=None):

		Holder.__init__(self, system, FindChildren(tmpcache, system))

		# Get the colors of the object
		IconMixIn.__init__(self, tmpcache, colorizer)
		type, childtype = self.GetColors()

		# Create a list of the objects
		ObjectList = []

		positionlist = objectutils.getPositionList(system)
		if positionlist == []:
			raise TypeError('Object passed to SystemIcon has no coordinates, %r' % system)

		prevpos = ()
		# The center point for each position
		for position in positionlist:
			ObjectList.append(Point(position[0:2], type, self.PrimarySize, False))
			if prevpos != ():
				ObjectList.append(Line((prevpos[0:2], position[0:2]), type))
			prevpos = position

		if len(self.children) > 0:
			# The orbit bits
			for position in positionlist:
				ObjectList.insert(0, Point(position[0:2], "Black", 8, InForeground=True))
				ObjectList.insert(0, Point(position[0:2], "Grey",  9, InForeground=True))
	
			# The orbiting children
			for i, childtype in enumerate(childtype):
				for position in positionlist:
					ObjectList.append(
						RelativePoint(position[0:2], childtype, self.ChildSize, True, self.ChildOffset(i))
					)

		Group.__init__(self, ObjectList, False)

class FleetIcon(Group, Holder, IconMixIn):
	"""
	Display a little arrow shape thing.
	"""
	def copy(self):
		# FIXME: Very expensive
		return FleetIcon(self.tmpcache, self.primary, self.Colorizer)

	def __init__(self, tmpcache, fleet, colorizer=None):
		if len(FindChildren(tmpcache, fleet)) > 0:
			raise TypeError('The fleet has children! WTF?')

		Holder.__init__(self, fleet, [])

		# Get the colors of the object
		IconMixIn.__init__(self, tmpcache, colorizer)
		type, childtype = self.GetColors()

		# Create a list of the objects
		ObjectList = []

		positionlist = objectutils.getPositionList(fleet)
		if positionlist == []:
			raise TypeError('Object passed to FleetIcon has no coordinates, %r' % system)

		for position in positionlist:
			# The little ship icon
			ObjectList.append(Point(position[0:2], None, 12))
			ObjectList.append(PolygonShip(position[0:2], type))

		Group.__init__(self, ObjectList, False)

class WormholeIcon(Group, Holder, IconMixIn):
	"""
	Display a little arrow shape thing.
	"""
	def copy(self):
		# FIXME: Very expensive
		return WormholeIcon(self.tmpcache, self.primary, self.Colorizer)

	def XY(self):
		return self.ObjectList[0].Points[0]+(self.ObjectList[0].Points[1]-self.ObjectList[0].Points[0])/2
	XY = property(XY)

	def __init__(self, tmpcache, wormhole, colorizer=None):
		if not isinstance(wormhole, Wormhole):
			raise TypeError('WormholeIcon must be given a Wormhole, %r' % system)

		if len(FindChildren(tmpcache, wormhole)) > 0:
			raise TypeError('The wormhole has children! WTF?')

		Holder.__init__(self, wormhole, [])

		# Get the colors of the object
		IconMixIn.__init__(self, tmpcache, colorizer)
		type, childtype = self.GetColors()

		# Create a list of the objects
		ObjectList = []

		# The little ship icon
		ObjectList.append(Line((wormhole.start[0:2], wormhole.end[0:2]), type))

		Group.__init__(self, ObjectList, False)

from extra.StateTracker import TrackerObjectOrder
class Systems(SystemLevelOverlay, TrackerObjectOrder):
	name     = "Systems"
	Colorizers = [ColorVerses, ColorEach]

	def __init__(self, parent, canvas, panel, *args, **kw):
		SystemLevelOverlay.__init__(self, parent, canvas, panel, *args, **kw)

		self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_RIGHT_ARROW))

		# Create a drop-down on the panel for colorizer
		self.ColorizeMode = wx.Choice(panel)
		self.ColorizeMode.Bind(wx.EVT_CHOICE, self.OnColorizeMode)

		# Populate the colorizer dropdown with information
		for colorizer in self.Colorizers:
			self.ColorizeMode.Append(colorizer.name, colorizer)
		self.ColorizeMode.SetSelection(0)

		self.Colorizer = None
		self.OnColorizeMode(None)

		sizer = wx.FlexGridSizer(10)
		sizer.AddGrowableRow(0)
		sizer.Add(self.ColorizeMode, proportion=1, flag=wx.EXPAND)
		panel.SetSizer(sizer)

		self.menumap = None

		TrackerObjectOrder.__init__(self)

	def OnColorizeMode(self, evt):
		cls = self.ColorizeMode.GetClientData(self.ColorizeMode.GetSelection())

		if not isinstance(self.Colorizer, cls):
			# Change the colorizer
			self.Colorizer = cls(self.application.cache.players[0].id)

			if not evt is None:
				self.CleanUp()
				self.UpdateAll()
				self.canvas.Draw()

	def UpdateAll(self):
		SystemLevelOverlay.UpdateAll(self)

		self['preview-arrow'] = PolygonArrow((0,0), "#555555", True)
		self['preview-arrow'].Hide()
		self['selected-arrow'] = PolygonArrow((0,0), "Red", True)
		if self.Selected is None:
			self['selected-arrow'].Hide()

	def Icon(self, obj):
		if objectutils.isFleet(self.application.cache, obj.id):
			return FleetIcon(self.application.cache, obj, self.Colorizer)
		
		return SystemIcon(self.application.cache, obj, self.Colorizer)

	def ArrowTo(self, arrow, icon, object):
		arrow.SetPoint(icon.XY)
		arrow.SetOffset((0,0))

		i = icon.index(object)
		if i > 0:
			arrow.SetOffset(icon.ChildOffset(i-1))
		arrow.Show()

	def ObjectLeftClick(self, icon, obj, samesystem=False):
		"""
		Move the red arrow to the current object.
		"""
		# FIXME: This really is a horrible hack :(
		if self.parent.mode is self.parent.GUISelect:
			self.ArrowTo(self['selected-arrow'], icon, obj)
			self.canvas.Draw()

			return True
		elif self.parent.mode is self.parent.GUIWaypointEdit:
			# FIXME: Hack
			from windows.main.panelOrder import panelOrder

			order = self.parent.application.gui.main.panels[panelOrder.title]

			if hasattr(order, "OnSelectPosition"):
				positionlist = objectutils.getPositionList(self.Selected.current)
				if positionlist == []:
					raise TypeError('Object passed to FleetIcon has no coordinates, %r' % system)

				# FIXME: Do something about multiple positions?
				order.OnSelectPosition(positionlist[0])

			return False

		elif self.parent.mode is self.parent.GUIWaypoint:
			orderdesc = None
			for orderdesc in OrderDescs().values():
				if orderdesc._name in ("Move",) :
					break

			assert not orderdesc is None

			if samesystem:
				assert len(self.nodes) > 0

				# Modify the last move order
				updatedorder = orderdesc(0, self.oid, -1, orderdesc.subtype, 0, [], self.Selected.current.pos)
				self.ChangeOrder(updatedorder,self.nodes[-1])

				self.ObjectHoverEnter(self.Selected, self.canvas.WorldToPixel(self.Selected.XY))
			else:
				# Insert new move order
				neworder = orderdesc(0, self.oid, -1, orderdesc.subtype, 0, [], self.Selected.current.pos)
				self.InsertAfterOrder(neworder)

			return False

	def SelectObject(self, id, forceother=False):
		if self.parent.mode in (self.parent.GUIWaypoint, self.parent.GUIWaypointEdit) :
			return
		TrackerObjectOrder.SelectObject(self, id, forceother)

	def OrderInsertAfter(self, afterme, what):
		if self.parent.mode in (self.parent.GUIWaypoint, self.parent.GUIWaypointEdit):
			self.SelectOrders([what])

	OrderInsertBefore = OrderInsertAfter

	def SystemHovering(self, event):
		if self.parent.mode in (self.parent.GUIWaypoint, self.parent.GUIWaypointEdit):
			return
		SystemLevelOverlay.SystemHovering(self, event)

	def ModeChange(self, oldmode, newmode):
		print "ModeChange", oldmode, newmode

		if newmode in (self.parent.GUIWaypoint, self.parent.GUIWaypointEdit):
			self.RealSelected = copy.copy(self.Selected)

		if oldmode in (self.parent.GUIWaypoint, self.parent.GUIWaypointEdit):
			self.Selected = self.RealSelected
			self.RealSelected = None

	def ObjectRightClick(self, icon, hover):
		"""
		Popup a selection menu.
		"""
		self.menumap = {}

		# Create popup menu with objects from clicked icon
		menu = wx.Menu()
		for obj in icon:
			id = wx.NewId()

			# A callback function for a menu item
			def ObjectItemSelected(evt, obj=obj):
				self.SelectObject(obj.id)

			self.menumap[id] = ObjectItemSelected

			if obj != hover:
				menu.Append(id, obj.name, "Select previewed %s" % obj.name)
			else:
				menu.AppendCheckItem(id, obj.name, "Select %s" % obj.name)
				menu.Check(id, True)


		# This function returns list of tuples (order description, callback function)
		def MenuOrders():
			orders = []

			# Find possible orders for the currently selected (not clicked) object
			if self.oid is None:
				return orders

			queuelist = objectutils.getOrderQueueList(self.application.cache, self.oid)
			ordertypes = objectutils.getOrderTypes(self.application.cache, self.oid)

			# Find possible order types in all order queues
			for queuename, queueid in queuelist:
				for typeid in ordertypes[queueid]:
					orderdesc = OrderDescs()[typeid]

					# An order should have absolute coordinates
					# or another object as a single parameter
					properties = orderdesc.properties
					if len(properties) != 1:
						continue

					if isinstance(properties[0], OrderParamAbsSpaceCoords):
						# A callback function for a menu item with abs. coordinates order parameter
						def AbsCoordsOrderItemSelected(toobject, toqueueid=queueid, how=orderdesc):
							# Compose arguments list for Order
							# FIXME Handle multiple positions somehow
							positions = objectutils.getPositionList(toobject)

							if len(positions) <= 0:
								raise TypeError("Object must have at least one position: %r" % toobject)

							coords = [positions[0][:3]]
							args = [-1, toqueueid, -1, how.subtype, 0, [], coords]

							neworder = how(*args)
							neworder._dirty = True
							self.InsertAfterOrder(neworder)

						callback = AbsCoordsOrderItemSelected

					elif isinstance(properties[0],OrderParamObject):
						# A callback function for a menu item with object order parameter
						def ObjectOrderItemSelected(toobject, toqueueid=queueid, how=orderdesc):
							# Compose arguments list for Order
							args = [-1, toqueueid, -1, how.subtype, 0, [], toobject.id]
							
							neworder = how(*args)
							neworder._dirty = True

							self.InsertAfterOrder(neworder)
						
						callback = ObjectOrderItemSelected
					else:
						continue

					orders.append((orderdesc._name, callback))

			return orders

		orders = MenuOrders()

		# Add found orders to menu if they exist
		if len(orders) > 0 and self.Selected != None:
			for name, order in orders:
				submenu = wx.Menu()

				for obj in icon:
					id = wx.NewId()

					def OrderItemSelected(evt, obj=obj, order=order):
						order(obj)

					self.menumap[id] = OrderItemSelected
					submenu.Append(id, "to %s" % obj.name)

				menu.AppendSeparator()
				menu.AppendMenu(wx.NewId(), "%s %s" % (name ,self.Selected.current.name), submenu)	

		self.parent.Bind(wx.EVT_MENU, self.OnContextMenu)
		self.parent.Bind(wx.EVT_MENU_CLOSE, self.OnContextMenuClose)

		self.parent.PopupMenu(menu)
		self.menumap = None

	def OnContextMenu(self, evt):
		self.menumap[evt.GetId()](evt)
		
	def OnContextMenuClose(self, evt):
		pass

	def ObjectSelect(self, oid):
		"""
		Called on object selection by external event.
		"""
		SystemLevelOverlay.ObjectSelect(self, oid)
		if self.Selected is not None:
			self['selected-arrow'].Show()
		else:
			self['selected-arrow'].Hide()

		self.canvas.Draw()

	def ObjectHoverEnter(self, icon, pos):
		"""
		The pop-up contains details about what is in the system.
		Also draws the path of each object in the system.
		"""
		SystemLevelOverlay.ObjectHoverEnter(self, icon, pos)

		# Draw the path of the object
		paths = []
##		for i, cobj in enumerate(icon):
##			path = FindPath(self.application.cache, cobj)
##			if path:
##				pr = path[0]
##				for p in path[1:]:
##					paths.append(Line([pr[0:2], p[0:2]], LineColor='Blue', InForeground=True))
##					pr = p

		if len(paths) > 0:
			self['paths'] = paths
			self.canvas.Draw()

	def ObjectHovering(self, icon, object):
		if not self.menumap is None:
			return False

		SystemLevelOverlay.ObjectHovering(self, icon, object)

		self['preview-arrow'].Show()
		self.ArrowTo(self['preview-arrow'], icon, object)
		self.canvas.Draw()

		return True

	def ObjectHoverLeave(self, icon):
		SystemLevelOverlay.ObjectHoverLeave(self, icon)

		# Hide any paths which are showing
		if self.has_key('paths'):
			del self['paths']
		self['preview-arrow'].Hide()
		self.canvas.Draw()

	def ObjectPopupText(self, icon):
		# Build the string
		s = "<font size='%s'>" % wx.local.normalFont.GetPointSize()
		for i, cobj in enumerate(icon):
			# Italics the currently selected object
			weight = 'normal'
			if self.Selected != None and self.Selected.current == cobj:
				weight = 'bold'

			color = icon.Colorizer(FindOwners(self.application.cache, cobj))

			# Tabulate non-systems
			if not objectutils.isTopLevel(self.application.cache, cobj.parent):
				s += "  "
				
			s += "<font weight='%s' color='%s'>%s" % (weight, color, cobj.name)

			# Add text about ships
			for propertygroup in cobj.properties:
				positionattrsstruct = getattr(cobj, propertygroup.name)
				if not hasattr(positionattrsstruct, 'Ship List'):
					continue;
					
				shiplists = getattr(positionattrsstruct, 'Ship List').references
				
				for shiplist in shiplists:
					reftype = shiplist[0]
					shipid = shiplist[1]
					shipcount = shiplist[2]
					if reftype == GenericRS.Types["Design"]:
						try:
							s += escape("\n  %s %ss" % (shipcount, self.application.cache.designs[shipid].name))
						except KeyError:
							s += escape("\n  %s %ss" % (shipcount, "Unknown Ships"))
					elif reftype == GenericRS.Types["Object"]:
						s += escape("\n  %s %ss" % (shipcount, self.application.cache.objects[shipid].name))
					else:
						s += escape("\n  %s %ss" % (shipcount, "Unknown Ships"))

			s += "</font>\n"

		s = s[:-1]+"</font>"

		return s

	def ObjectRefreshAll(self):
		self.UpdateAll()
