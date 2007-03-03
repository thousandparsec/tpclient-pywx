"""\
*Internal*

This overlay is a base for things which draw proportional circles to some value.
"""

from Overlay import Overlay
class Value(Overlay):
	"""\
	Draws circles defined by a value.
	"""
	scale = 1

	def __init__(self, canvas, cache):
		Overlay.__init__(self, canvas, cache)

	def value(self, oid):
		"""\
		The absolute size of this object (non-proportional).
		"""
		return 1

	def updateall(self):
		"""\
				
		"""
		# Remove all the objects.
		self.cleanup()
		for oid in self.cache.objects.keys():
			self.updateone(oid)

	def updateone(self, oid):
		"""\

		"""
		# Create the new object.
		value = self.value(oid)
		if value is None:
			return

		self[oid] = FloatCanvas.Circle(self.cache.objects[oid].pos[0:2], self.value(oid)*self.scale, FillColor="White", LineColor="Red")
