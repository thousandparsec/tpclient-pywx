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

# tp imports
from tp.netlib.objects                        import Object
from tp.netlib.objects                        import Order
from tp.netlib.objects.ObjectExtra.Universe   import Universe
from tp.netlib.objects.ObjectExtra.Galaxy     import Galaxy


from Overlay   import SystemLevelOverlay, Holder

def FindPath(cache, obj):
	"""
	Figure out the path this object will take.

	Returns a list of tuples
		(order slot, order destination)
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	locations = [(-1, obj.pos)]
	for order in cache.orders[obj.id]:
		# FIXME: Needs to be a better way to do this...
		if order._name in ("Move", "Move To", "Intercept"):
			if hasattr(order, "pos"):
				locations.append((order.slot, order.pos))
			if hasattr(order, "to"):
				locations.append((order.slot, cache.objects[order.to].pos))
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
	Background = "Black"
	# The color of paths when just shown
	Normal = "Grey"
	# The color of path of the currently selected object
	Active = "Blue"
	# The color of the currently active segment of the path
	Selected = wx.Color(255,0,0)
	# The color of the "split" handles
	SplitHandle = "Yellow"	

	def XY(self):
		return self.ObjectList[0].XY
	XY = property(XY)

	def __init__(self, what, endingat, previous):
		# Check the what parameter
		if not isinstance(what, Order):
			raise TypeError("The what parameter must be an Order object")

		# Check the ending at parameter
		# Must be a set of corrdinates or an object

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
		ObjectList.append(Line([start[0:2], end[0:2]], LineColor=self.Background, InForeground=False, LineWidth = 10))
		# The visible version of the path 
		ObjectList.append(Line([start[0:2], end[0:2]], LineColor=self.Active,     InForeground=True))

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

	def Select(self, yes):
		if yes:
			self.ObjectList[-1].SetColor(self.Selected)
		else:
			self.ObjectList[-1].SetColor(self.Active)

class Paths(SystemLevelOverlay):
	"""\
	Draws a path of ships and similar objects.
	"""
	name     = "Paths"
	toplevel = Galaxy, Universe


	def __init__(self, parent, canvas, panel, cache, *args, **kw):
		SystemLevelOverlay.__init__(self, parent, canvas, panel, cache, *args, **kw)

		self.active = None

	def UpdateOne(self, oid, overrides={}):

		path = FindPath(self.cache, self.cache.objects[oid])
		if not path is None:
			previous = self.cache.objects[oid]
			for slot, end in path[1:]:
				segment = PathSegment(self.cache.orders[oid][slot], end, previous)

				self[(oid, slot)] = segment

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

	def OnClickSegment(self, evt):
		self.parent.OnOverlayObjectSelected(evt.what.id)
		self.parent.OnOverlayOrderSelected(evt.what.id, evt.what.slot)

		if not self.active is None:
			self.active.Select(False)
		self.active = evt
		self.active.Select(True)	

		self.canvas.Draw(Force=True)

	def Empty(self, evt):
		pass
