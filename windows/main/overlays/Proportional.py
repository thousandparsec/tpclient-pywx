"""\
*Internal*

This overlay is the base for overlays which use proportional circles.
"""
# wxPython imports
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas import PieChart
from extra.wxFloatCanvas.FloatCanvas   import Point, Group, Line
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects                        import Object

from Overlay import SystemLevelOverlay, Holder

def FindChildren(cache, obj):
	"""
	Figure out all the children of this object.
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	kids = set()
	for cid in obj.contains:
		child = cache.objects[cid]

		kids.update(FindChildren(cache, child))
		kids.add(child)

	return list(kids)

class IconMixIn:
	"""
	"""
	PrimarySize = 3
	ChildSize   = 3

	def __init__(self, cache):
		self.cache = cache

	# FIXME: Should probably just monkey patch this onto Group?
	def XY(self):
		return self.ObjectList[0].XY
	XY = property(XY)

	def GetSize(self):
		return (self.PrimarySize*2, self.PrimarySize*2)

	def ChildOffset(self, i):
		num = len(self.children)

		angle = ((2.0*pi)/num)*(i-0.125)
		return (int(cos(angle)*6), int(sin(angle)*6))

class SystemIcon(Group, Holder, IconMixIn):
	"""
	Display a round dot which is sized proportionally.
	"""
	
	def copy(self):
		# FIXME: Very expensive
		return SystemIcon(self.cache, self.primary, self.proportion, self.scale)

	def __init__(self, cache, system, proportion, scale):
		self.cache = cache
		self.proportion = proportion
		self.scale = scale
		Holder.__init__(self, system, FindChildren(cache, system))

		# Create a list of the objects
		ObjectList = []

		# The center point
		ObjectList.append(FloatCanvas.Point(system.pos[0:2], 'White', self.proportion*self.scale))

		Group.__init__(self, ObjectList, False)
		
	def Amount(self, oid):
		"""\
		The absolute size of this object (non-proportional).
		"""
		return 1
		
class Proportional(SystemLevelOverlay):
	"""\
	Draws proportional circles defined by amount.
	"""
	scale = 60L
	#scale = 150L
	
	#def __init__(self, *args, **kw):
	#	SystemLevelOverlay.__init__(self, *args, **kw)
	def __init__(self, parent, canvas, panel, cache, *args, **kw):
		SystemLevelOverlay.__init__(self, parent, canvas, panel, cache, *args, **kw)
		
		self.cache = cache
		
		self.max = 0
		self.min = 0
		
		self.fco = {}

	def UpdateAll(self):
		"""\
				
		""" 
		
		c = self.cache

		# Remove all the objects.
		self.CleanUp()

		# Calculate all the values so we can figure min/max.
		values = {}
		for oid in c.objects.keys():
			#print oid, self.Amount(oid)
			# Disregard the Universe and the Galaxy
			if (c.objects[oid].subtype > 1):
				values[oid] = self.Amount(oid)

		import pprint
		#pprint.pprint(values)

		# Get min/max values.
		v = values.values()
		self.min = min(v)
		self.max = max(v)

		for oid, value in values.items():
			self.UpdateOne(oid, value)

	def UpdateOne(self, oid, value=None):
		"""\

		"""
		if isinstance(self.cache.objects[oid], StarSystem):
			SystemLevelOverlay.UpdateOne(self, oid)
	
	def Proportion(self, oid, value=None):
		c = self.cache
		
		# Disregard the Universe and the Galaxy
		if (c.objects[oid].subtype > 1):
	
			if value is None:
				# Get the new value.
				value = self.Amount(oid)
	
				# If the min/max value has changed we need to redraw everything.
				#if value < self.min or value > self.max:
					#self.UpdateAll()
					#return
	
			# New proportional value.
			if not (self.max-self.min) is 0:
				proportional = value/float(self.max-self.min)
			else :
				proportional = .01
				
			if (proportional*self.scale) < 10 and proportional > 0:
				proportional = 10.0 / self.scale
			
			#if (proportional*self.scale) > 30:
				#proportional = 30.0 / self.scale
	
			# Create the new object.
			#print proportional
			#'LineColor':'Red', 'FillColor':'Red'
			# 'LineColor':'White', 'FillColor':'White'
			
			return proportional
	
	def Icon(self, obj):
		if isinstance(obj, StarSystem):
			return SystemIcon(self.cache, obj, self.Proportion(obj.id), self.scale)
	
	def ObjectHoverEnter(self, icon, pos):
		"""
		The pop-up contains details about what is in the system.
		Also draws the path of each object in the system.
		"""
		SystemLevelOverlay.ObjectHoverEnter(self, icon, pos)

	def ObjectHovering(self, icon, object):
		SystemLevelOverlay.ObjectHovering(self, icon, object)

		return True

	def ObjectHoverLeave(self, icon):
		SystemLevelOverlay.ObjectHoverLeave(self, icon)
		
	def ObjectPopupText(self, icon):
		return ""