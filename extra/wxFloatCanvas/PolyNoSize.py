
from FloatCanvas import Polygon

class PolyNoSize(Polygon):
	def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		# World out the difference
		NewStart = WorldToPixel(self.Points[0])
		Diff = NewStart[0] - self.Points[0][0], NewStart[1] - self.Points[0][1]
		Points = self.Points + Diff

		dc.SetPen(self.Pen)
		dc.SetBrush(self.Brush)
		dc.DrawPolygon(Points)
		if HTdc and self.HitAble:
			HTdc.SetPen(self.HitPen)
			HTdc.SetBrush(self.HitBrush)
			HTdc.DrawPolygon(Points)

	def Move(self, Delta):
		Diff = Delta[0] - self.Points[0][0], Delta[1] - self.Points[0][1]
		self.Points += Diff

		self.BoundingBox = self.BoundingBox + Diff
		if self._Canvas:
			self._Canvas.BoundingBoxDirty = True

