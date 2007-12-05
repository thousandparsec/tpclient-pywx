"""\
*Internal*

This overlay is the base for overlays which use proportional circles.
"""
# wxPython imports
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas import PieChart

from Overlay import Overlay
class Proportional(Overlay):
	"""\
	Draws proportional circles defined by amount.
	"""
	scale = 60L
	#scale = 150L

	def __init__(self, *args, **kw):
		Overlay.__init__(self, *args, **kw)

		self.max = 0
		self.min = 0

		self.fco = {}

	def Amount(self, oid):
		"""\
		The absolute size of this object (non-proportional).
		"""
		return 1

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
			
		c = self.cache
		
		# Disregard the Universe and the Galaxy
		if (c.objects[oid].subtype > 1):
	
			if value is None:
				# Get the new value.
				value = self.Amount(oid)
	
				# If the min/max value has changed we need to redraw everything.
				if value < self.min or value > self.max:
					self.UpdateAll()
					return
	
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
			self[oid] = FloatCanvas.Point(c.objects[oid].pos[0:2], 'White', proportional*self.scale)
			#'LineColor':'Red', 'FillColor':'Red'
			# 'LineColor':'White', 'FillColor':'White'
			
			return proportional