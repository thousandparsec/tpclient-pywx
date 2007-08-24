
import numpy as N
from FloatCanvas import Point, PointSet

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

class RelativePointSet(PointSet):
    
    def __init__(self, Points, Color = "Black", Diameter =  1, InForeground = False, Offsets=None):
        PointSet.__init__(self, Points, Color, Diameter, InForeground)
        self.SetOffsets(Offsets)

    def SetOffsets(self, Offsets):
        self.Offsets = N.array(Offsets, N.float_)
        if len(self.Offsets) != len(self.Points):
            raise TypeError('The offset list must be the same length as the number of points')

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        dc.SetPen(self.Pen)
        Points = WorldToPixel(self.Points)+self.Offsets
        if self.Diameter <= 1:
            dc.DrawPointList(Points)
        elif self.Diameter <= 2:
            self.DrawD2(dc, Points)
        else:
            dc.SetBrush(self.Brush)
            radius = int(round(self.Diameter/2))
            ##fixme: I really should add a DrawCircleList to wxPython
            if len(Points) > 100:
                xy = Points
                xywh = N.concatenate((xy-radius, N.ones(xy.shape) * self.Diameter ), 1 )
                dc.DrawEllipseList(xywh)
            else:
                for xy in Points:
                    dc.DrawCircle(xy[0],xy[1], radius)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.SetBrush(self.HitBrush)
            if self.Diameter <= 1:
                HTdc.DrawPointList(Points)
            elif self.Diameter <= 2:
                self.DrawD2(HTdc, Points)
            else:
                if len(Points) > 100:
                    xy = Points
                    xywh = N.concatenate((xy-radius, N.ones(xy.shape) * self.Diameter ), 1 )
                    HTdc.DrawEllipseList(xywh)
                else:
                    for xy in Points:
                        HTdc.DrawCircle(xy[0],xy[1], radius)
