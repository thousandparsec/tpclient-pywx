
class ChildBeforeParent(Exception):
	pass

class UnknownObject(Exception):
	pass

class Universe:
	"""\
	The holder of the universe.
	"""
	def __init__(self):
		# Register for object informations
		self.map = {}

	def Add(self, object):
		if isinstance(object, UniverseObject):

			# Insert the object into map
			container = self.GetParent(new.id)
			if not container and new.id != 0:
				# Ekk! we got a child object but no parent
				raise ChildBeforeParent(repr(new.id))
			else:
				new.container = container
			
			self.map[new.id] = new

		else:
			raise UnknownObject("Tried to insert unknown object (%s) into the Universe" % object)

	def GetParent(self, id):
		for theid,o in self.map.items():
			if isinstance(o, Container):
				if id in o.contains:
					return o
		return None

class UniverseObject:
	"""\
	The base of everything in the universe.
	"""
	def __init__(self, container=None, pos=(0,0), velocity=(0,0), acceleration=(0,0), diameter=0):
		self.container = container
		self.contains = []
		
		self.diameter = diameter
		
		self.pos = pos
		self.velocity = velocity
		self.acceleration = acceleration

class Container(UniverseObject):
	"""\
	A universe object which contains other objects.
	"""
	pass

class Actual(UniverseObject):
	"""\
	A real universe object - this object cannot contain other objects.
	"""
	pass

