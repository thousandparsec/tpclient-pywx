#!/usr/bin/env python

"""
Colors.py

Assorted stuff for Colrsd support. At the moment, only a single item:

CatagoricalColor1: A list of colors that are distict.

"""

## Categorical 12-step scheme, after ColorBrewer 11-step Paired Scheme     
## From: http://geography.uoregon.edu/datagraphics/color_scales.htm
# CategoricalColor1 = [ (255, 191, 127),
#                       (255, 127,   0),
#                       (255, 255, 153),
#                       (255, 255,  50),
#                       (178, 255, 140),
#                       ( 50, 255,   0),
#                       (165, 237, 255),
#                       (25, 178, 255),
#                       (204, 191, 255),
#                       (101,  76, 255),
#                       (255, 153, 191),
#                       (229,  25,  50),
#                       ]

CategoricalColor1 = [ (229,  25,  50),
                      (101,  76, 255),
                      ( 50, 255,   0),
                      (255, 127,   0),
                      (255, 255,  50),
                      (255, 153, 191),
                      (25, 178, 255),
                      (178, 255, 140),
                      (255, 191, 127),
                      (204, 191, 255),
                      (165, 237, 255),
                      (255, 255, 153),
                      ]



if __name__ == "__main__":
    import wx
    # tiny test app
    class TestFrame(wx.Frame):
        def __init__(self, *args, **kwargs):
            wx.Frame.__init__(self, *args, **kwargs)
            
            Sizer = wx.BoxSizer(wx.VERTICAL)
            Sizer.Add(wx.StaticText(self, label="CategoricalColor"), 0, wx.ALL, 5)
            for c in CategoricalColor1:
                w = wx.Window(self, size=(100, 20))
                w.SetBackgroundColour(wx.Colour(*c))
                Sizer.Add(w, 0, wx.ALL, 5)
            self.SetSizerAndFit(Sizer)
            self.Show()

    A = wx.App(False)
    F = TestFrame(None)
    A.MainLoop()
    