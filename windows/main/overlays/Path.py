"""\
An Overlay which provides a line showing where objects have orders to go.
"""
# Python imports
import os
from math import *

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas.FloatCanvas   import Point, Group, Line

from extra.StateTracker import TrackerObjectOrder

# tp imports
from tp.netlib.objects import constants
from tp.netlib.objects                        import Object, OrderDescs
from tp.netlib.objects                        import Order
from tp.netlib.objects.ObjectExtra.Universe   import Universe
from tp.netlib.objects.ObjectExtra.Galaxy     import Galaxy

from Overlay   import Overlay

def FindPath(cache, obj):
	"""
	Figure out the path this object will take.

	Returns a list of tuples
		(node, order destination)
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	locations = [(-1, obj.pos)]
	for listpos, node in enumerate(cache.orders[obj.id]):
		order = node.CurrentOrder

		# FIXME: Needs to be a better way to do this...
		orderdesc = OrderDescs()[order._subtype]
		if len(orderdesc.names) != 1:
			continue

		argument_name, subtype = orderdesc.names[0]
		if subtype == constants.ARG_ABS_COORD:
			locations.append((node, getattr(order, argument_name)))
		elif subtype == constants.ARG_OBJECT:
			locations.append((node, cache.objects[getattr(order, argument_name)].pos))

	if len(locations) == 1:
		return None
	return locations

class PathSegment(Group):
	"""
	This represents a segment on a path to somewhere.

	It has a reference to which order this path comes from.
	It has a "previous segment" reference which can be an object or another path segment.
	It has a endingat destination
	"""
	BackgroundColor = None
	# The color of paths when just shown
	InactiveColor = "Grey"
	# The color of path of the currently selected object
	ActiveColor = "Blue"
	# The color of the currently active segment of the path
	SelectedColor = "Red"
	# The color of the "split" handles
	SplitHandleColor = "Yellow"	

	class States:
		Inactive = "Inactive"
		Active   = "Active"
		Selected = "Selected"

		transisions = [
			(Inactive, Active),
			(Active, Selected),
			(Selected, Active),
			(Active, Inactive),
			(Selected, Inactive),
		]

	def XY(self):
		return self.ObjectList[0].XY
	XY = property(XY)

	def __init__(self, what, endingat, previous):
		# Check the ending at parameter
		# Must be a set of corrdinates or an object

		self.State = self.States.Inactive

		self.what     = what
		self.endat    = endingat
		self.previous = previous
		self.next = None

		if isinstance(previous, PathSegment):
			# Link this with the previous segment
			self.previous.SetNext(self)

			start = self.previous.endat
		elif isinstance(previous, Object):
			start = self.previous.pos[0:2]		
		else:
			raise TypeError("The previous item must either be an Object or another PathSegment")

		end = self.endat

		ObjectList = []
		# Draw the line
		# A wider version of the path to make it easier to click on the line
		ObjectList.append(Line([start[0:2], end[0:2]], LineColor=self.BackgroundColor, LineWidth = 10))
		# The visible version of the path 
		ObjectList.append(Line([start[0:2], end[0:2]], LineColor=self.InactiveColor))

		# Draw the "ticks" which indicate how far the object will reach each turn

		Group.__init__(self, ObjectList, False)

	def SetNext(self, segment):
		"""
		Insert the given segment as the next segment.
		IE
			a -> b
			a.SetNext(c)
			a -> c -> b
		"""
		if not isinstance(segment, PathSegment):
			raise TypeError("The next object must be a Path Segment!")

		if self.next is None:
			self.next = segment
		else:
			if not segment.next is None:
				raise TypeError("This given segment has stuff after is!")
			segment.SetNext(self.next)

			self.next = segment

	def SetState(self, state):
		if self.State == state:
			return 

		if not (self.State, state) in self.States.transisions:
			raise TypeError("Can not change from %s to %s" % (self.State, state))

		self.State = state

		# Change the color of this segment
		color = getattr(self, unicode(state) + 'Color')
		self.ObjectList[-1].SetColor(color)

	def Select(self, yes):
		if yes:
			self.SetState(self.States.Selected)
		else:
			self.SetState(self.States.Active)

	def Active(self, yes):
		if yes:
			self.SetState(self.States.Active)
		else:
			self.SetState(self.States.Inactive)

# FIXME: The hitpath and the actual path should be seperated for speed reasons..
class Paths(Overlay, TrackerObjectOrder):
	"""\
	Draws a path of ships and similar objects.
	"""
	name     = "Paths"
	toplevel = Galaxy, Universe

	layer = -1

	def __init__(self, parent, canvas, panel, cache, *args, **kw):
		Overlay.__init__(self, parent, canvas, panel, cache, *args, **kw)

		self.active = []
		TrackerObjectOrder.__init__(self)	

	def UpdateOne(self, oid, overrides={}):
		# Remove all the previous segments
		for nid, nodeid in self.keys():
			if oid == nid:
				del self[(oid, nodeid)]

		if oid == self.oid:
			self.active = []

		# Create the new path
		path = FindPath(self.cache, self.cache.objects[oid])
		if not path is None:
			previous = self.cache.objects[oid]
			for node, end in path[1:]:
				segment = PathSegment((oid, node), end, previous)

				# Make sure the selected bits are still selected..
				if oid == self.oid:
					segment.Active(True)

					if node in self.nodes:
						segment.Select(True)

					self.active.append(segment)

				self[(oid, node.id)] = segment

				from extra.wxFloatCanvas.FloatCanvas import EVT_FC_ENTER_OBJECT, EVT_FC_LEAVE_OBJECT
				from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_UP, EVT_FC_RIGHT_UP
				from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_DOWN, EVT_FC_RIGHT_DOWN

				# These pop-up the name of the object
				segment.Bind(EVT_FC_ENTER_OBJECT, self.Empty)
				segment.Bind(EVT_FC_LEAVE_OBJECT, self.Empty)
				# This is needed to the hit test doesn't fall through
				segment.Bind(EVT_FC_LEFT_DOWN, lambda x: True) 
				segment.Bind(EVT_FC_LEFT_UP, self.OnClickSegment)

				previous = segment

	def ClearActive(self):
		for active in self.active:
			active.Select(False)

		self.active = []

	def ObjectSelect(self, oid):
		"""
		Select an object using an external event.

		Simulates this as a mouse click.
		"""
		self.ClearActive()

		# FIXME: This is kind of suckily slow!
		for nid, nodeid in self.keys():
			if oid == nid:
				self[(nid, nodeid)].Active(True)
			else:
				self[(nid, nodeid)].Active(False)

		self.canvas.Draw(True)

	def OrdersSelect(self, nodes):
		self.ClearActive()

		for node in nodes:
			try:
				self.active.append(self[(self.oid, node.id)])
			except KeyError:
				pass

		for active in self.active:
			active.Select(True)	

		self.canvas.Draw(True)

	def OrderInsertAfter(self, node, override=None):
		self.UpdateOne(self.oid)
		self.canvas.Draw()

	OrderInsertBefore = OrderInsertAfter
	OrderRefresh      = OrderInsertAfter

	def OrdersRemove(self, nodes, override=False):
		self.UpdateOne(self.oid)
		self.canvas.Draw()

	def ObjectRefresh(self, oid):
		if oid is None:
			return
		
		self.UpdateOne(self.oid)
		
	def ObjectRefreshAll(self):
		self.UpdateAll()

	def OnClickSegment(self, evt):
		self.SelectObject(evt.what[0])
		self.SelectOrders([evt.what[1]])

	def Empty(self, evt):
		pass

