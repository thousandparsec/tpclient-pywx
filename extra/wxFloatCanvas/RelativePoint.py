
import numpy as N
from FloatCanvas import Point

class RelativePoint(Point):
	"""\
	Relative Point is a point which also has a *pixel* offset.

	This is useful for Icons where you want a point to be at the same location 
	as another graphic but a different offset.
	"""

	def __init__(self, XY, Color = "Black", Diameter =  1, InForeground = False, Offset=(0,0)):
		Point.__init__(self, XY, Color, Diameter, InForeground = False)

		self.SetOffset(Offset)

	def SetOffset(self, Offset):
		self.Offset = N.array(Offset, N.float_)
		self.Offset.shape = (2,) # Make sure it is a length 2 vector

	def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
		dc.SetPen(self.Pen)
		xy = WorldToPixel(self.XY) + self.Offset
		if self.Diameter <= 1:
			dc.DrawPoint(xy[0], xy[1])
		else:
			dc.SetBrush(self.Brush)
			radius = int(round(self.Diameter/2))
			dc.DrawCircle(xy[0],xy[1], radius)
		if HTdc and self.HitAble:
			HTdc.SetPen(self.HitPen)
			if self.Diameter <= 1:
				HTdc.DrawPoint(xy[0], xy[1])
			else:
				HTdc.SetBrush(self.HitBrush)
				HTdc.DrawCircle(xy[0],xy[1], radius)

