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

	def __init__(self, planet):
		Icon.__init__(self, planet.pos[0:2])

		self.Size = planet.size

		self.icon.append(Point(planet.pos[0:2], "Green", 4))
		self.subicon.append(RelativePoint(planet.pos[0:2], "Blue", 3))

	def SetCenter(self, center):
		# Figure out the "orbit"
		diameter = 2*sqrt((self.XY[0]-center[0])**2 + (self.XY[1]-center[1])**2)

		# The "orbit" of the planet
		self.real.append(Circle(center, diameter, LineColor="Blue"))
		# The actual planet (FIXME: *1000 shouldn't be needed...)
		self.real.append(Circle(self.XY, self.Size*100, LineColor="White", FillColor="White"))

class SystemIcon(Icon):
	"""
	An object which can only become so small before it reverts to "Icon" form.
	"""
	MinSize = 8

	def __init__(self, starsystem):
		Icon.__init__(self, starsystem.pos[0:2])

		self.children = []

		# Icon form consists of a central point, plus a circle plus a bunch of planet points
		self.icon = []
		self.icon.append(Point(starsystem.pos[0:2], "Yellow", 4))

		self.real = []
		self.real.append(Circle(starsystem.pos[0:2], starsystem.size, LineColor="Red"))

	def AddChild(self, child):
		# If this is the first child, add the orbit indicater
		if len(self.children) == 0:
			self.icon.insert(0, Point(self.XY, "Black", 8))
			self.icon.insert(0, Point(self.XY, "White", 9))

		Icon.AddChild(self, child)

from Value import Value
class Systems(Value):
	def updateone(self, oid):
		"""\

		"""
		obj = self.cache.objects[oid]

		if isinstance(obj, StarSystem):
			def pin(obj, cache=self.cache):
				if isinstance(obj, (Planet, Fleet)):
					o = PlanetIcon(obj)

				if isinstance(obj, (StarSystem,)):
					o = SystemIcon(obj)

				for child in obj.contains:
					r = pin(cache.objects[child])

					if hasattr(o, "AddChild"):
						if r != None:
							o.AddChild(r)
				return o

			self[oid] = pin(obj)
