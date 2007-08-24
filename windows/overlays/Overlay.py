"""\
This module contains the StarMap window. This window displays a view of the
universe.
"""

class Overlay(dict):
	"""\
	A layer which displays something.
	"""	

	def __init__(self, canvas, cache):
		self.canvas = canvas
		self.cache  = cache

	def cleanup(self):
		"""\
		Remove this overlay from the Canvas.
		"""
		# Remove any old values
		for oid in self.keys():
			# Remove the old object
			del self[oid]

	def __setitem__(self, key, value):
		"""\
		Adds Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		if self.has_key(key):
			del self[key]

		if isinstance(value, (list, tuple)):
			for v in value:
				self.canvas.AddObject(v)
		else:
			self.canvas.AddObject(value)
		dict.__setitem__(self, key, value)

	def __delitem__(self, oid):
		"""\
		Removes Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		value = self[oid]

		if isinstance(value, (list, tuple)):
			for v in value:
				self.canvas.RemoveObject(v)
		else:
			self.canvas.RemoveObject(value)
		dict.__delitem__(self, oid)

	def update(self, oid=None):
		"""\
		Update the FloatCanvas objects for this oid.

		Called when an order on oid changes.
		"""
		if oid is None:
			self.updateall()
		else:
			# Remove the old object.
			if self.has_key(oid):
				del self[oid]

			# If the oid is no longer in the cache we shouldn't continue.
			if not c.objects.has_key(oid):
				return

			# Otherwise update the object.
			self.updateone(oid)

	def updateall(self):
		"""\
		Updates all objects on the Canvas.
		"""
		# Remove all the objects.
		self.cleanup()
		for oid in self.cache.objects.keys():
			self.updateone(oid)

	def updateone(self, oid):
		"""\
		Updates an object on the Canvas.
		"""
		pass
