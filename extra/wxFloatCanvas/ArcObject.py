#!/usr/bin/env python
"""
A FloatCanvas arc Object, and a test for it

"""
from FloatCanvas import * 

import numpy as N

# define the new Object:
class ArcPoint(XYObjectMixin, LineAndFillMixin, DrawObject):    
    def __init__(self,
                 StartXY,
                 EndXY,
                 CenterXY,
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 FillColor    = None,
                 FillStyle    = "Solid",
                 InForeground = False):               
        """
        ArcPoint(self, Point StartXY, Point EndXY, Point CenterXY)

        Draws an arc of a circle, centered on point CenterXY, from
        the first point (StartXY) to the second (EndXY).

        The arc is drawn in an anticlockwise direction from the start point to
        the end point.
        """

        DrawObject.__init__(self, InForeground)
       
        # There is probably a more elegant way to do this next section
        # The bounding box just gets set to the WH of a circle, with center at CenterXY
        # This is suitable for a pie chart as it will be a circle anyway
        radius = N.sqrt( (StartXY[0]-CenterXY[0])**2 + (StartXY[1]-CenterXY[1])**2 )
        minX = CenterXY[0]-radius
        minY = CenterXY[1]-radius
        maxX = CenterXY[0]+radius
        maxY = CenterXY[1]+radius      
        XY = [minX,minY]
        WH = [maxX-minX,maxY-minY]

        self.XY = N.asarray( XY, N.float).reshape((2,))
        self.WH = N.asarray( WH, N.float).reshape((2,))

        self.StartXY = N.asarray(StartXY, N.float).reshape((2,))
        self.CenterXY = N.asarray(CenterXY, N.float).reshape((2,))
        self.EndXY = N.asarray(EndXY, N.float).reshape((2,))

        #self.BoundingBox = array((self.XY, (self.XY + self.WH)), Float)
        self.CalcBoundingBox()
       
        #Finish the setup; allocate color,style etc. 
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth
        self.FillColor = FillColor
        self.FillStyle = FillStyle

        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)

        self.SetPen(LineColor, LineStyle, LineWidth)
        self.SetBrush(FillColor, FillStyle)                  #Why isn't this working ???

           
    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        self.SetUpDraw(dc , WorldToPixel, ScaleWorldToPixel, HTdc)
        StartXY = WorldToPixel(self.StartXY)
        EndXY = WorldToPixel(self.EndXY)
        CenterXY = WorldToPixel(self.CenterXY)
       
        dc.DrawArcPoint(StartXY, EndXY, CenterXY)
        if HTdc and self.HitAble:
            HTdc.DrawArcPoint(StartXY, EndXY, CenterXY)


    def CalcBoundingBox(self):
       
        self.BoundingBox = N.array((self.XY, (self.XY + self.WH) ), N.float)
        #self._Canvas.BoundingBoxDirty = True     #um set an error ?
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True

class ArcPoint2(XYObjectMixin, LineAndFillMixin, DrawObject):    
    def __init__(self,
                 StartXY,
                 EndXY,
                 CenterXY,
                 LineColor = "Black",
                 LineStyle = "Solid",
                 LineWidth    = 1,
                 FillColor    = None,
                 FillStyle    = "Solid",
                 InForeground = False):               
        """
		This is a non-resizing 

        ArcPoint(self, Point StartXY, Point EndXY, Point CenterXY)

        Draws an arc of a circle, centered on point CenterXY, from
        the first point (StartXY) to the second (EndXY).

        The arc is drawn in an anticlockwise direction from the start point to
        the end point.
        """

        DrawObject.__init__(self, InForeground)
       
        # There is probably a more elegant way to do this next section
        # The bounding box just gets set to the WH of a circle, with center at CenterXY
        # This is suitable for a pie chart as it will be a circle anyway

		# FIXME: This doesn't work correctly...
        radius = N.sqrt( (StartXY[0]-CenterXY[0])**2 + (StartXY[1]-CenterXY[1])**2 )
        minX = CenterXY[0]-radius
        minY = CenterXY[1]-radius
        maxX = CenterXY[0]+radius
        maxY = CenterXY[1]+radius      
        XY = [minX,minY]
        WH = [maxX-minX,maxY-minY]

        self.XY = N.asarray( XY, N.float).reshape((2,))
        self.WH = N.asarray( WH, N.float).reshape((2,))

        self.StartXY  = N.asarray(StartXY,  N.float).reshape((2,))
        self.CenterXY = N.asarray(CenterXY, N.float).reshape((2,))
        self.EndXY    = N.asarray(EndXY,    N.float).reshape((2,))

        #self.BoundingBox = array((self.XY, (self.XY + self.WH)), Float)
        self.CalcBoundingBox()
       
        #Finish the setup; allocate color,style etc. 
        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth
        self.FillColor = FillColor
        self.FillStyle = FillStyle

        self.HitLineWidth = max(LineWidth,self.MinHitLineWidth)

        self.SetPen(LineColor, LineStyle, LineWidth)
        self.SetBrush(FillColor, FillStyle)                  #Why isn't this working ???

           
    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        self.SetUpDraw(dc , WorldToPixel, ScaleWorldToPixel, HTdc)
        CenterXY = WorldToPixel(self.CenterXY)
        StartXY = self.StartXY+CenterXY
        EndXY   = self.EndXY  +CenterXY
       
        dc.DrawArcPoint(StartXY, EndXY, CenterXY)
        if HTdc and self.HitAble:
            HTdc.DrawArcPoint(StartXY, EndXY, CenterXY)
