
import numpy as N
from FloatCanvas import Polygon, XYObjectMixin

class PolygonStatic(Polygon, XYObjectMixin):
	"""\
	Draws a polygon which always has the same pixel size.
	"""
	CalcBoundingBox = XYObjectMixin.CalcBoundingBox

	def __init__(self, XY, Points, Color="Black", InForeground=False, Offset=(0,0), **kw):
		xy = N.array(XY, N.float)
		xy.shape = (2,)
		self.XY = xy

		Polygon.__init__(self, Points, LineColor=Color, FillColor=Color, InForeground=InForeground, **kw)

		self.SetOffset(Offset)

	def SetOffset(self, Offset):
		self.Offset = N.array(Offset, N.float_)
		self.Offset.shape = (2,) # Make sure it is a length 2 vector

	def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel = None, HTdc=None):
		Points = self.Points + self.Offset + WorldToPixel(self.XY)

		dc.SetPen(self.Pen)
		dc.SetBrush(self.Brush)
		dc.DrawPolygon(Points)
		if HTdc and self.HitAble:
			HTdc.SetPen(self.HitPen)
			HTdc.SetBrush(self.HitBrush)
			HTdc.DrawPolygon(Points)

class PolygonArrow(PolygonStatic):
	def __init__(self, XY, *args, **kw):
		kw['LineWidth'] = 1
		PolygonStatic.__init__(self, XY, [(0,0), (-5,-10), (0, -8), (5,-10)], *args, **kw)

class PolygonShip(PolygonStatic):
	def __init__(self, XY, *args, **kw):
		kw['LineWidth'] = 1
		PolygonStatic.__init__(self, XY, [(0,0), (3,0), (0,4), (0,2), (-3,0)], *args, **kw)

