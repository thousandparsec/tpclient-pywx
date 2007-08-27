
from FloatCanvas import Group
from ArcObject import ArcPoint

from math import *

class PieChart(Group):
	def __init__(self, XY, Diameter, Amounts, InForeground = False):
		if not isinstance(Amounts, (list, tuple)):
			raise TypeError("Amount's must be a tuple of tuples with first value as numbers and values as Arc arguments")

		for number, args in Amounts:
			if not isinstance(number, (int, long, float)):
				raise TypeError("Amount's keys must be a number not %r %s" % (number, type(number)))

			if not isinstance(args, dict):
				raise TypeError("Amount's values must be the arguments for each Arc not %r %s" % (args, type(args)))

		# Convert to percentages
		Total = sum(zip(*Amounts)[0])
		Percentages = [(float(a)/Total, b) for a,b in Amounts]

		ObjectList = []
		
		CenterXY = XY
		StartXY  = XY+(0, Diameter)

		total = 0
		for percentage, args in Percentages:
			total += percentage

			radians = pi/2-2*pi*total
			EndXY = CenterXY + (cos(radians)*Diameter, sin(radians)*Diameter)

			if isinstance(args, dict):
				ObjectList.append(ArcPoint(EndXY, StartXY, CenterXY, **args))
			elif isinstance(args, (list, tuple)):
				ObjectList.append(ArcPoint(EndXY, StartXY, CenterXY,  *args))

			StartXY = EndXY
		
		Group.__init__(self, ObjectList, InForeground)

