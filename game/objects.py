
import time

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

	def ObjectIDs(self):
		return self.map.keys()

	def Objects(self):
		return self.map.values()

	def Add(self, object):
		if isinstance(object, UniverseObject):

			# Insert the object into map
			container = self.GetParent(object.id)
			if not container and object.id != 0:
				# Ekk! we got a child object but no parent
				raise ChildBeforeParent(repr(object.id))
			else:
				object.container = container
			
			self.map[object.id] = object

		else:
			raise UnknownObject("Tried to insert unknown object (%s) into the Universe" % object)

	def GetParent(self, id):
		for theid,o in self.map.items():
			if isinstance(o, Container):
				if id in o.contains:
					return o
		return None

	def Object(self, id):
		try:
			return self.map[id]
		except:
			return None

class DescHolder:
	"""\
	The holder of the descriptions.
	"""
	def __init__(self):
		# Register for object informations
		self.o = {}

	def OrderDescIDs(self):
		return self.o.keys()

	def OrderDescs(self):
		return self.o.values()
		
	def OrderDesc(self, id):
		try:
			# Check to see if I have the order
			if not self.o.has_key(id):
				return None

			return self.o[id]
		except:
			return None

	def OrderDescAdd(self, object):
		self.o[object.id] = object

	def __del__(self):
		print self.o

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

