"""\
*Internal*

This overlay is the base for overlays which use proportional circles.
"""
# wxPython imports
from extra.wxFloatCanvas import FloatCanvas

from Overlay import Overlay
class Proportional(Overlay):
	"""\
	Draws proportional circles defined by amount.
	"""
	scale = 100L

	def __init__(self, parent, canvas, cache):
		Overlay.__init__(self, parent, canvas, cache)

		self.max = 0
		self.min = 0

		self.fco = {}

	def amount(self, oid):
		"""\
		The absolute size of this object (non-proportional).
		"""
		return 1

	def updateall(self):
		"""\
				
		"""
		c = self.cache

		# Remove all the objects.
		self.cleanup()

		# Calculate all the values so we can figure min/max.
		values = {}
		for oid in c.objects.keys():
			print oid, self.amount(oid)

			values[oid] = self.amount(oid)

		import pprint
		pprint.pprint(values)

		# Get min/max values.
		v = values.values()
		self.min = min(v)
		self.max = max(v)

		for oid, value in values.items():
			self.updateone(oid, value)

	def updateone(self, oid, value=None):
		"""\

		"""
		c = self.cache

		if value is None:
			# Get the new value.
			value = self.amount(oid)

			# If the min/max value has changed we need to redraw everything.
			if value < self.min or value > self.max:
				self.updateall()
				return

		# New proportional value.
		proportional = value/(self.max-self.min)

		# Create the new object.
		self[oid] = FloatCanvas.Point(c.objects[oid].pos[0:2], 'White', proportional*self.scale)

