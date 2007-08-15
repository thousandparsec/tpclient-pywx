"""\
Draws circles proportional to the actual size of the object.
"""
# wxPython imports
from Value import Value

# Network imports
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet

class Size(Value):
	"""\
	Draws proportional circles for the relative to size of object.
	"""
	def value(self, oid):
		"""\
		The amount of this resource on this object.
		"""
		obj = self.cache.objects[oid]
		if isinstance(obj, (Planet, StarSystem)):
			return obj.size
