
import numpy as N
from FloatCanvas import Point

class Arrow(Polygon):
	"""\
	Draws a little arrow which can also have a pixel offset.
	"""

	def __init__(self, XY, Color = "Black", InForeground = False, Offset=(0,0)):
		Polygon.__init__(self, [(0,0), (-5,-10), (0, -8), (5,-10)],
							LineWidth=1,LineColor=Color,FillColor=Color,InForeground=InForeground)
		self.Move(XY)
		self.SetOffset(Offset)

	def SetOffset(self, Offset):
		self.Offset = N.array(Offset, N.float_)
		self.Offset.shape = (2,) # Make sure it is a length 2 vector

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel = None, HTdc=None):
        Points = WorldToPixel(self.Points) + self.Offset
        dc.SetPen(self.Pen)
        dc.SetBrush(self.Brush)
        dc.DrawPolygon(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.SetBrush(self.HitBrush)
            HTdc.DrawPolygon(Points)

