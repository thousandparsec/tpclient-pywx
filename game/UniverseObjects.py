
class UniverseObject:
	def __init__(self, container=None, pos=(0,0), velocity=(0,0), acceleration=(0,0), diameter=0):
		self.container = container
		self.contains = []
		
		self.diameter = diameter
		
		self.pos = pos
		self.velocity = velocity
		self.acceleration = acceleration


class Container(UniverseObject):
	pass

class Actual(UniverseObject):
	pass

