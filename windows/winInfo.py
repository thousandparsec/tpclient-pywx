"""\
This module contains the Information window. The Information window
displays all objects information.
"""

import os
from types import *

# wxPython imports
import wx

# Network imports
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet
from tp.netlib.objects.ObjectExtra.Fleet import Fleet

# Local imports
from winBase import *
from utils import *

class winInfo(winBase):
	title = _("Information")

	from defaults import winInfoDefaultPosition as DefaultPosition
	from defaults import winInfoDefaultSize as DefaultSize
	from defaults import winInfoDefaultShow as DefaultShow

	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		self.titletext = wx.StaticText(self, -1, _("No Object Selected."))
		self.picture = wx.StaticBitmap(self, -1, wx.BitmapFromImage(wx.EmptyImage(128, 128)))
		self.text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)

		top = wx.BoxSizer(wx.VERTICAL)
		top.Add(self.titletext, 0, wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER, 3)

		information = wx.BoxSizer(wx.VERTICAL)
		information.Add(self.text, 1, wx.EXPAND, 0)
		
		middle = wx.BoxSizer(wx.HORIZONTAL)
		middle.Add(self.picture, 0, 0, 0)
		middle.Add(information, 1, wx.EXPAND, 0)

		top.Add(middle, 1, wx.EXPAND, 0)

		self.SetSizer(top)

	def OnSelectObject(self, evt):
		print "winInfo SelectObject", evt
		try:
			object = self.application.cache.objects[evt.id]
		except:
			do_traceback()
			debug(DEBUG_WINDOWS, "SelectObject: No such object.")
			return

		self.titletext.SetLabel(object.name)

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

		# Add the object type specific information
		s = ""
		for key, value in object.__dict__.items():
			if key.startswith("_") or key in \
				('protocol', 'sequence', 'otype', 'length', 'order_types', 'order_number', 'contains'):
				continue

			if key == "ships":
				s += "ships: "
				for t, number in value:
					design = self.application.cache.designs[t]
					s += "%s %s, " % (number, design.name)
				s = s[:-2] + "\n"
				continue

			if type(value) == StringType:
				s += "%s: '%s'\n" % (key, value)
			elif type(value) in (ListType, TupleType):
				s += "%s: " % (key,)
				for i in value:
					s += "%s, " % (i,)
				s = s[:-2] + "\n"
			else:
				s += "%s: %s\n" % (key, value)

		self.text.SetValue(s)

