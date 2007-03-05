"""\
This overlay draws Star Systems on the Starmap.
"""
# Python imports
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas.FloatCanvas	import Circle, Point
from extra.wxFloatCanvas.RelativePoint 	import RelativePoint
from extra.wxFloatCanvas.Icon 			import Icon

# tp imports
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet
from tp.netlib.objects.ObjectExtra.Fleet import Fleet

class PlanetIcon(Icon):
	MinSize = 2

	Friendly 	= "Green"
	Enemy 		= "Red"
	Unowned		= "Blue"

	def __init__(self, planet, type):
		Icon.__init__(self, planet.pos[0:2])

		self.type = type
		self.planet = planet

	def SetCenter(self, center):
		# Create the subicon
		self.subicon.append(RelativePoint(center, self.type, 3))

		# Figure out the "orbit"
		diameter = 2*sqrt((self.XY[0]-center[0])**2 + (self.XY[1]-center[1])**2)

		# The actual planet (FIXME: *1000 shouldn't be needed...)
		self.real.append(Circle(self.XY, self.planet.size*100, LineColor=self.type, FillColor=self.type))
		self.real.append(Circle(center, diameter, LineColor="Grey"))

		# The icon mode of the planet
		self.icon.append(Point(self.planet.pos[0:2], self.type, 2))
		self.icon.append(Circle(center, diameter, LineColor="Grey"))

class SystemIcon(Icon):
	"""
	An object which can only become so small before it reverts to "Icon" form.
	"""
	MinSize = 8

	Contested 	= "Yellow"
	Friendly 	= "Green"
	Enemy 		= "Red"
	Unowned 	= "Blue"

	def __init__(self, starsystem, type):
		Icon.__init__(self, starsystem.pos[0:2])

		self.children = []

		# Icon form consists of a central point, plus a circle plus a bunch of planet points
		self.icon = []
		self.icon.append(Point(starsystem.pos[0:2], type, 4))

		self.real = []
		self.real.append(Circle(starsystem.pos[0:2], starsystem.size, LineColor=type))

	def AddChild(self, child):
		# If this is the first child, add the orbit indicater
		if len(self.children) == 0:
			self.icon.insert(0, Point(self.XY, "Black", 8))
			self.icon.insert(0, Point(self.XY, "Grey", 9))

		Icon.AddChild(self, child)

from Value import Value
class Systems(Value):
	def updateone(self, oid):
		"""\

		"""
		pid = self.cache.players[0].id
		obj = self.cache.objects[oid]

		if isinstance(obj, StarSystem):
			def pin(obj, cache=self.cache):
				# Figure out the owners of the system
				owners = set()
				for child in obj.contains:
					if not hasattr(cache.objects[child], 'owner'):
						continue

					owner = cache.objects[child].owner
					if owner in (0, -1):
						continue
					owners.add(owner)

				print repr(obj), pid, owners,

				if isinstance(obj, (Planet, Fleet)):
					print obj.owner
					if obj.owner in (-1, 0):
						o = PlanetIcon(obj, PlanetIcon.Unowned)
					else:
						o = PlanetIcon(obj, (PlanetIcon.Enemy, PlanetIcon.Friendly)[obj.owner == pid])

				if isinstance(obj, (StarSystem,)):
					print
					if pid in owners:
						o = SystemIcon(obj, (SystemIcon.Friendly, SystemIcon.Contested)[len(owners)>1])
					else:
						o = SystemIcon(obj, (SystemIcon.Unowned, SystemIcon.Enemy)[len(owners)>0])

				for child in obj.contains:
					r = pin(cache.objects[child])
					if r == None:
						continue

					if hasattr(o, "AddChild"):
						o.AddChild(r)

				return o

			self[oid] = pin(obj)


