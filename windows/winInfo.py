"""\
This module contains the Information window. The Information window
displays all objects information.
"""

import os
from types import *

# wxPython imports
import wx

try:
	from extra.GIFAnimationCtrl import GIFAnimationCtrl
except ImportError:
	from wx.animate import GIFAnimationCtrl

# Network imports
from tp.netlib.objects.ObjectExtra.Universe import Universe
from tp.netlib.objects.ObjectExtra.Galaxy import Galaxy
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

		picture_still_panel = wx.Panel(self)
		self.picture_still = wx.StaticBitmap(picture_still_panel, -1, wx.BitmapFromImage(wx.EmptyImage(128, 128)))
		picture_still_panel.SetBackgroundColour(wx.Colour(0, 0, 0))

		self.picture_animated = GIFAnimationCtrl(self, -1)
		self.picture_animated.SetBackgroundColour(wx.Colour(0, 0, 0))
		self.picture_animated.Stop(); self.picture_animated.Hide()

		self.text = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)

		top = wx.BoxSizer(wx.VERTICAL)
		top.Add(self.titletext, 0, wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER, 3)

		information = wx.BoxSizer(wx.VERTICAL)
		information.Add(self.text, 1, wx.EXPAND, 0)
		
		middle = wx.BoxSizer(wx.HORIZONTAL)
		middle.Add(picture_still_panel,    0, 0, 0)
		middle.Add(self.picture_animated, 0, 0, 0)
		middle.Add(information, 1, wx.EXPAND, 0)

		top.Add(middle, 1, wx.EXPAND, 0)

		self.SetSizer(top)

		# Find the images
		import os
		self.images = {'nebula':[], 'star':[], 'planet':[]}
		base = os.path.join(".", "media", "common-2d")

		def li(root, dirs, files, images=self.images):
			dir = os.path.split(root)[-1]
			if not '-' in dir:
				return
			type, size = dir.split('-')
			
			if images.has_key(type) and size == "small":
				images[type].extend([os.path.join(root, x) for x in files])

				if "animation" in dirs and "still" in dirs:
					for nroot, ndirs, nfiles in os.walk(os.path.join(root, "animation")):
						images[type].extend([os.path.join(nroot, x) for x in nfiles])
						
					dirs.remove("animation")

					#for t, ndirs, nfiles in os.walk(os.path.join(root, "still")):
					#	li(root, ndirs, nfiles)
					#dirs.remove("still")

		for root, dirs, files in os.walk(base):
			li(root, dirs, files)

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
		if isinstance(object, (Universe, Galaxy)):
			images = self.images['nebula']
		elif isinstance(object, StarSystem):
			images = self.images['star']
		elif isinstance(object, Planet):
			images = self.images['planet']
		else:
			images = []

		try:
			image = images[object.id % len(images)]
		except:
			image = ""

		print "Choose:", image

		if image.endswith(".gif"):
			print "Animated image!"
			self.picture_still.Hide()
			print "Showing the Image"	
			self.picture_animated.Show()
			print "Loading Image"
			self.picture_animated.LoadFile(image)
			print "Playing the Image"
			self.picture_animated.Play()
		else:
			print "Still image!"
			self.picture_still.Show()
			self.picture_animated.Stop()
			self.picture_animated.Hide()

			if image == "":
				bitmap = wx.BitmapFromImage(wx.EmptyImage(128, 128))
			else:
				bitmap = wx.BitmapFromImage(wx.Image(image))
			self.picture_still.SetBitmap(bitmap)

		self.Layout()

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

