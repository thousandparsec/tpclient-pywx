"""\
This module contains the base classes used to build a new overlays for the
Starmap.
"""

from tp.netlib.objects import Object

class Holder(list):
	"""
	A holder is an entity which contains a "primary" object and a bunch of
	"children".

	It also maintains a pointer to the "current" object which can be advanced
	by the Loop methods.  
	"""

	def primary(self):
		"""
		The primary object.
		"""
		return self[0]
	primary = property(primary)

	def children(self):
		"""
		The rest of the objects.
		"""
		return self[1:]
	children = property(children)

	def current(self):
		"""
		The currently 'selected' object.
		"""
		return self[self.__current]
	current = property(current)

	def __init__(self, parent, children=[]):
		if not isinstance(parent, Object):
			raise TypeError("Parent must be an Object not %r" % parent) 
		for i, child in enumerate(children):
			if not isinstance(child, Object):
				raise TypeError("Child %i must be an Object not %r" % (i, child)) 

		self.extend([parent] + children)
		self.ResetLoop()

	def __eq__(self, value):
		if isinstance(value, Holder):
			return self.__eq__([value.primary.id, value.__current])
		return [self.primary.id, self.__current] == value

	def ResetLoop(self):
		"""
		Make the loop go back to the beginning.	
		"""
		self.__current = -1

	def NextLoop(self):
		"""
		Get the next object from the holder, this will loop around.
		"""
		self.__current = (self.__current + 1) % len(self)
		return self.__current, self.current

	def SetLoop(self, v):
		"""
		Set the loop's position to a given object.
		"""
		if not v in self:
			raise TypeError("That object %s doesn't exist in the Holder!" % v)
		self.__current = self.index(v)
		return self.__current

class Overlay(dict):
	"""\
	A layer which displays something on the StarMap.
	"""	

	def __init__(self, parent, canvas, cache):
		self.parent = parent
		self.canvas = canvas
		self.cache  = cache

	def cleanup(self):
		"""\
		Remove this overlay from the Canvas.
		"""
		for oid in self.keys():
			# Remove the old object
			del self[oid]

	def __setitem__(self, key, value):
		"""\
		Adds Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		if self.has_key(key):
			del self[key]

		self.canvas.AddObject(value)
		dict.__setitem__(self, key, value)

	def __delitem__(self, oid):
		"""\
		Removes Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		value = self[oid]

		self.canvas.RemoveObject(value)
		dict.__delitem__(self, oid)

	def __del__(self):
		self.cleanup()

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
