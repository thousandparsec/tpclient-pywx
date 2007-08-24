"""\
This overlay draws Star Systems on the Starmap.
"""
# Python imports
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas.FloatCanvas import Point, Group
from extra.wxFloatCanvas.RelativePoint import RelativePoint, RelativePointSet

from extra.wxFloatCanvas.FloatCanvas import EVT_FC_ENTER_OBJECT, EVT_FC_LEAVE_OBJECT

# tp imports
from tp.netlib.objects.ObjectExtra.Galaxy import Galaxy
from tp.netlib.objects.ObjectExtra.Universe import Universe
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet
from tp.netlib.objects.ObjectExtra.Fleet import Fleet

class GenericIcon(Group):
	Friendly  = "Green"
	Enemy     = "Red"
	Unowned   = "White"
	Contested = "Yellow"

	PrimarySize = 3
	ChildSize   = 3

	def __init__(self, pos, type, children=[]):
		ObjectList = []

		# The center Point
		ObjectList.append(Point(pos, type, self.PrimarySize, True))

		if len(children) > 0:
			# The orbit bits
			ObjectList.insert(0, Point(pos, "Black", 8))
			ObjectList.insert(0, Point(pos, "Grey",  9, True))
	
			# The orbiting children
			for i, childtype in enumerate(children):
				angle = ((2.0*pi)/len(children))*(i-0.125)
				offset = (int(cos(angle)*6), int(sin(angle)*6))

				ObjectList.append(RelativePoint(pos, childtype, self.ChildSize, True, offset))

		Group.__init__(self, ObjectList, True)

	def XY(self):
		return self.ObjectList[0].XY
	XY = property(XY)

class FleetIcon(Group):
	pass

def FindChildren(cache, obj):
	"""
	Figure out all the children of this object.
	"""
	kids = set()
	for child in obj.contains:
		kids.update(FindChildren(cache, cache.objects[child]))
		kids.add(child)

	return list(kids)

def FindOwners(cache, obj):
	"""
	Figure out the owners of this object (and it's children).
	"""
	owners = set()
	for child in [obj.id]+FindChildren(cache, obj):
		if not hasattr(cache.objects[child], 'owner'):
			continue

		owner = cache.objects[child].owner
		if owner in (0, -1):
			continue
		owners.add(owner)
	return owners

def OwnerColor(pid, owners):
	"""

	"""
	type = (GenericIcon.Unowned, GenericIcon.Enemy)[len(owners)>0]
	if pid in owners:
		type = (GenericIcon.Friendly, GenericIcon.Contested)[len(owners)>1]

	return type

from Overlay import Overlay

from wx.lib.fancytext import StaticFancyText
class NamePopup(wx.PopupWindow):
	Padding = 2

	def __init__(self, parent, style):
		wx.PopupWindow.__init__(self, parent, style)
		self.SetBackgroundColour("CADET BLUE")

		wx.CallAfter(self.Refresh)

	def SetText(self, text):
		try:
			self.st.Destroy()
		except AttributeError:
			pass

		self.st = StaticFancyText(self, -1, text, pos=(self.Padding, self.Padding))
		sz = self.st.GetSize()
		self.SetSize( (sz.width+2*self.Padding, sz.height+2*self.Padding) )

class Systems(Overlay):
	toplevel = Galaxy, Universe

	def __init__(self, *args, **kw):
		Overlay.__init__(self, *args, **kw)

		self.PopupText = NamePopup(self.canvas, wx.SIMPLE_BORDER)

	def updateone(self, oid):
		"""\

		"""
		pid = self.cache.players[0].id
		obj = self.cache.objects[oid]

		# Only draw top level objects
		if isinstance(obj, Systems.toplevel):
			return

		parent = self.cache.objects[obj.parent]
		if not isinstance(parent, Systems.toplevel):
			return

		types = []
		for cid in [obj.id]+FindChildren(self.cache, obj):
			cobj = self.cache.objects[cid]
			types.append(OwnerColor(pid, FindOwners(self.cache, cobj)))

		self[oid]    = GenericIcon(obj.pos[0:2], types[0], types[1:])
		self[oid].id = oid

		# These pop-up the name of the object
		# Also do a "preview" event after X seconds
		self[oid].Bind(EVT_FC_ENTER_OBJECT, self.SystemEnter)
		self[oid].Bind(EVT_FC_LEAVE_OBJECT, self.SystemLeave)

	def SystemEnter(self, obj):
		print "SystemEnter", obj
		pid = self.cache.players[0].id

		screen = self.canvas.WorldToPixel(obj.XY)
		pos	= self.canvas.ClientToScreen( screen )

		# Build the string
		s = "<font size='%s'>" % wx.local.tinyFont.GetPointSize()
		for cid in [obj.id]+FindChildren(self.cache, self.cache.objects[obj.id]):
			cobj = self.cache.objects[cid]

			type = OwnerColor(pid, FindOwners(self.cache, cobj))
			s += "<font color='%s'>%s" % (type, cobj.name)
			if isinstance(cobj, Fleet):
				for shipid, amount in cobj.ships:
					s+= "\n  %s %ss" % (amount, self.cache.designs[shipid].name)
			s += "</font>\n"

		s = s[:-1]+"</font>"

		self.PopupText.SetText(s)
		self.PopupText.Position(pos, (GenericIcon.PrimarySize, GenericIcon.PrimarySize))
		self.PopupText.Show(True)

	def SystemLeave(self, evt):
		print "SystemLeave", evt

		self.PopupText.Hide()
