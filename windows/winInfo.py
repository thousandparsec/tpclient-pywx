"""\
This module contains the Information window. The Information window
displays all objects information.
"""

import os

# wxPython imports
import wx

# Network imports
from netlib.objects.ObjectExtra.StarSystem import StarSystem
from netlib.objects.ObjectExtra.Planet import Planet
from netlib.objects.ObjectExtra.Fleet import Fleet

# Local imports
from winBase import *
from utils import *

class winInfo(winBase):
	title = "Information"

	def __init__(self, application, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
		winBase.__init__(self, application, parent, pos, size, style)

		self.application = application

		self.title = wx.StaticText(self, -1, "No Object Selected.")
		self.picture = wx.StaticBitmap(self, -1, wx.BitmapFromImage(wx.EmptyImage(128, 128)))

		top = wx.BoxSizer(wx.VERTICAL)
		top.Add(self.title, 0, wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER, 3)

		self.information = wx.GridSizer(3, 2, 0, 0)
		middle = wx.BoxSizer(wx.HORIZONTAL)
		middle.Add(self.picture, 0, 0, 0)
		middle.Add(self.information, 1, wx.EXPAND, 0)

		top.Add(middle, 1, wx.EXPAND, 0)

		self.SetAutoLayout(1)
		self.SetSizer(top)
		
		top.Fit(self)
		top.SetSizeHints(self)

		self.Layout()

	def OnSelectObject(self, evt):
		print "Info.OnSelectObject"
		try:
			object = self.application.cache.objects[evt.id]
		except:
			do_traceback()
			debug(DEBUG_WINDOWS, "SelectObject: No such object.")
			return

		self.title.SetLabel(object.name)

		# Figure out the right graphic
		path = os.path.join(".", "graphics", "media")
		if isinstance(object, StarSystem):
			path = os.path.join(path, "star-small")

			stars = ["blue.png", "purple-large.png", "purple-small.png", "rainbow.png",  "red.png",  "yellow.png"]
			path = os.path.join(path, stars[object.id % len(stars)]+".jpg")

			bitmap = wx.BitmapFromImage(wx.Image(path))
		elif isinstance(object, Planet):
			path = os.path.join(path, "planet-small")

			planets = ["earthlike-1.jpg",  "earthlike-2.jpg",  "gasgiant-1.jpg"]
			path = os.path.join(path, planets[object.id % len(planets)])

			bitmap = wx.BitmapFromImage(wx.Image(path))
		else:
			bitmap = wx.BitmapFromImage(wx.EmptyImage(128, 128))

		self.picture.SetBitmap(bitmap)

