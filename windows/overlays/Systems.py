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

	PrimarySize = 4
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

from Value import Value
class Systems(Value):
	toplevel = Galaxy, Universe

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

		
		owners = FindOwners(self.cache, obj)
		type = (GenericIcon.Unowned, GenericIcon.Enemy)[len(owners)>0]
		if pid in owners:
			type = (GenericIcon.Friendly, GenericIcon.Contested)[len(owners)>1]

		childtypes = []
		for child in FindChildren(self.cache, obj):
			owners = FindOwners(self.cache, self.cache.objects[child])

			childtype = (GenericIcon.Unowned, GenericIcon.Enemy)[len(owners)>0]
			if pid in owners:
				childtype = (GenericIcon.Friendly, GenericIcon.Contested)[len(owners)>1]

			childtypes.append(childtype)

		self[oid] = GenericIcon(obj.pos[0:2], type, childtypes)

