
from FloatCanvas import RectEllipse

class CircleNoSmall(RectEllipse):
	def __init__(self, (x, y), Diameter, MinDiameter, **kwargs):
		RectEllipse.__init__(self, (x, y), (Diameter, Diameter), **kwargs)
		self.Diameter = Diameter
		self.MinDiameter = MinDiameter
	
	def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		dc.SetPen(self.Pen)
		dc.SetBrush(self.Brush)

		(X,Y) = WorldToPixel(self.XY)

		D = ScaleWorldToPixel((self.Diameter, 0))[0]

		if D < self.MinDiameter:
			D = self.MinDiameter

		R = int(round(D/2))

		dc.DrawEllipse(X-R,Y-R,D,D)
		if HTdc and self.HitAble:
			HTdc.SetBrush(self.HitBrush)
			HTdc.SetPen(self.HitPen)
			HTdc.DrawEllipse(X-R,Y-R,D,D)

