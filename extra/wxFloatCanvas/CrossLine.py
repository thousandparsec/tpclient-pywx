
from FloatCanvas import Line
import math

try:
	from Numeric import array, dot, sum, asarray
except ImportError:
	from numarray import array, dot, sum, asarray

t = array([[0,-1],[1,0]])

class CrossLine(Line):
	def __init__(self,Points,Number,
				 LineColor = "Black",
				 LineStyle = "Solid",
				 LineWidth	= 1,
				 InForeground = False):
		self.Number = Number

		Points = array(Points)
		Points.resize((2+Number*4,2))

		for i in range(0, Number*4, 4):
			Points[i+4] = Points[i+1]
			Points[i+5] = Points[i+1]+(Points[1]-Points[0])
	
		Line.__init__(self, Points, LineColor, LineStyle, LineWidth, InForeground)

	def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
	
		Points = array(WorldToPixel(self.Points))
		
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

