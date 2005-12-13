
from FloatCanvas import Line
import math

try:
	from Numeric import array, empty, dot, sum, asarray, Float
except ImportError:
	from numarray import array, dot, sum, asarray, Float
	def empty(shape, typecode):
		return array(shape=shape, typecode=typecode)

t = array([[0,-1],[1,0]])

class CrossLine(Line):
	def __init__(self,start,delta,Number,
				 LineColor = "Black",
				 LineStyle = "Solid",
				 LineWidth	= 1,
				 InForeground = False):
		self.Number = Number

		Points = empty((Number*4,2), Float)
		Points[0] = start
		Points[1] = array(start,Float)+array(delta,Float)
		Points[2] = Points[3] = Points[1]

		for i in range(4, len(Points), 4):
			# i   = normal start
			# i+1 = normal end
			# i+2 = cross start
			# i+3 = cross end
			Points[i] = Points[i-3]
			Points[i+1] = Points[i-3]+array(delta)

			Points[i+2] = Points[i+3] = Points[i-3]

		Line.__init__(self, Points, LineColor, LineStyle, LineWidth, InForeground)

	def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		Points = WorldToPixel(self.Points)
		
		pslop = dot(Points[1]-Points[0], t)
		length = math.sqrt(sum(pslop**2))
		pslop = pslop/length

		for i in range(0, self.Number*4, 4):
			Points[i+2] = (Points[i+1]+pslop*2.5).astype('i')
			Points[i+3] = (Points[i+1]-pslop*2.5).astype('i')

		dc.SetPen(self.Pen)
		dc.DrawLines(Points)
		if HTdc and self.HitAble:
			HTdc.SetPen(self.HitPen)
			HTdc.DrawLines(Points)

