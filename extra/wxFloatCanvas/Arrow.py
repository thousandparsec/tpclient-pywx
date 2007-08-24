
import numpy as N
from FloatCanvas import Polygon, XYObjectMixin
from Utilities import BBox

class Arrow(Polygon, XYObjectMixin):
	"""\
	Draws a little arrow which can also have a pixel offset.
	"""

	CalcBoundingBox = XYObjectMixin.CalcBoundingBox
	def __init__(self, XY, Color = "Black", InForeground = False, Offset=(0,0)):
		xy = N.array(XY, N.float)
		xy.shape = (2,)
		self.XY = xy

		Polygon.__init__(self, [(0,0), (-5,-10), (0, -8), (5,-10)],
							LineWidth=1,LineColor=Color,FillColor=Color,InForeground=InForeground)

		self.SetOffset(Offset)

	def SetOffset(self, Offset):
		self.Offset = N.array(Offset, N.float_)
		self.Offset.shape = (2,) # Make sure it is a length 2 vector

	def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel = None, HTdc=None):
		print "Drawing Arrow!"
		Points = self.Points + self.Offset + WorldToPixel(self.XY)
		dc.SetPen(self.Pen)
		dc.SetBrush(self.Brush)
		dc.DrawPolygon(Points)
