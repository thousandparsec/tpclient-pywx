
from FloatCanvas import RectEllipse

class Dot(RectEllipse):
    def __init__(self, x ,y, Diameter, **kwargs):
        RectEllipse.__init__(self, x, y, Diameter, Diameter, **kwargs)
        self.Diameter = Diameter

    def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
        dc.SetPen(self.Pen)
        dc.SetBrush(self.Brush)

        radius = int(round(self.Diameter/2))
        (X,Y) = WorldToPixel(self.XY)

        dc.DrawEllipse(X-radius,Y-radius,self.Diameter,self.Diameter)
        if HTdc and self.HitAble:
            HTdc.SetBrush(self.HitBrush)
            HTdc.DrawEllipse(X-radius,Y-radius,self.Diameter,self.Diameter)

