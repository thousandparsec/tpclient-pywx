"""\
This module contains the Information window. The Information window
displays all objects information.
"""

# Python Imports
import os
import os.path
from types import *

import pprint

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

def splitall(start):
	bits = []

	while True:
		start, end = os.path.split(start)
		if end is '':
			break
		bits.append(end)
	bits.reverse()
	return bits


WAITING = os.path.join(".", "graphics", "loading.gif")

class winInfo(winBase):
	title = _("Information")

	from defaults import winInfoDefaultPosition as DefaultPosition
	from defaults import winInfoDefaultSize as DefaultSize
	from defaults import winInfoDefaultShow as DefaultShow

	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		# Create a base panel
		base_panel = wx.Panel(self, -1)
		base_panel.SetAutoLayout( True )

		# Create a base sizer
		base_sizer = wx.BoxSizer( wx.VERTICAL )
		base_sizer.Fit( base_panel )
		base_sizer.SetSizeHints( base_panel )

		# Link the panel to the sizer
		base_panel.SetSizer( base_sizer )

		# Title Display
		self.titletext = wx.StaticText(base_panel, -1, _("No Object Selected."))

		# Picture Display
		self.picture_panel = wx.Panel(base_panel)
		self.picture_panel.SetBackgroundColour(wx.Colour(0, 0, 0))
		self.picture_still = wx.StaticBitmap(self.picture_panel, -1, wx.BitmapFromImage(wx.EmptyImage(128, 128)))
		self.picture_animated = GIFAnimationCtrl(self.picture_panel, -1)
		self.picture_animated.SetBackgroundColour(wx.Colour(0, 0, 0))
		self.picture_animated.Stop(); self.picture_animated.Hide()

		# Property Display
		self.text = wx.TextCtrl(base_panel, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)

		base_sizer.Add(self.titletext, 0, wx.BOTTOM|wx.TOP|wx.ALIGN_CENTER, 3)

		#information = wx.BoxSizer(wx.VERTICAL)
		#information.Add(self.text, 1, wx.EXPAND, 0)
		
		middle = wx.BoxSizer(wx.HORIZONTAL)
		middle.Add(self.picture_panel, 0, 0, 0)
		middle.Add(self.text, 1, wx.EXPAND, 0)

		base_sizer.Add(middle, 1, wx.EXPAND, 0)

		self.current = -1

		# Find the images
		self.images = {'nebula':{'still':[]}, 'star':{'still':[]}, 'planet':{'still':[]}}

	def OnMediaUpdate(self, evt):
		print
		print "winInfo.OnMediaUpdate", evt
		files = {}
		for file, timestamp in evt.files:
			bits = splitall(file)
	
			if bits[-2] in ['animation', 'still']:
				type = bits[-2]
				del bits[-2]
			else:
				type = 'still'
	
			if not bits[-2].endswith("-small"):
				continue
			else:
				key = bits[-2][:-6]
				if not files.has_key(key):
					files[key] = {}
				if not files[key].has_key(type):
					files[key][type] = []
				files[key][type].append((file, timestamp))
		self.images = files
	
	def OnMediaDownloadDone(self, evt):
		print "winInfo.MediaDownloadDone - Finished D", evt.file, evt.localfile
		print "winInfo.MediaDownloadDone - Waiting On", self.image_waiting
		if evt.file == self.image_waiting:
			# FIXME: Should load the image now...
			self.DisplayImage(evt.localfile)

	def DisplayImage(self, file):
		print "Displaying", file
		if file.endswith(".gif"):
			print "Animated image!"
			self.picture_still.Hide()
			print "Showing the Image"	
			self.picture_animated.Show()
			print "Loading Image"
			self.picture_animated.LoadFile(file)
			print "Playing the Image"
			self.picture_animated.Play()
		else:
			print "Still image!"
			self.picture_still.Show()
			self.picture_animated.Stop()
			self.picture_animated.Hide()

			if file != "":
				bitmap = wx.BitmapFromImage(wx.Image(file))
			else:
				bitmap = wx.BitmapFromImage(wx.EmptyImage(128, 128))
			self.picture_still.SetBitmap(bitmap)
		self.Layout()

	def OnSelectObject(self, evt):
		print "winInfo SelectObject", evt
		if evt.id == self.current:
			return
		self.current = evt.id

		try:
			object = self.application.cache.objects[evt.id]
		except:
			do_traceback()
			debug(DEBUG_WINDOWS, "SelectObject: No such object.")
			return

		self.titletext.SetLabel(object.name)

		# Figure out the right graphic
		try:
			if isinstance(object, (Universe, Galaxy)):
				images = self.images['nebula']
			elif isinstance(object, StarSystem):
				images = self.images['star']
			elif isinstance(object, Planet):
				images = self.images['planet']
			else:
				images = {'still': []}
		except KeyError, e:
			print e
			images = {'still': []}

		if images.has_key("animation"):
			images = images["animation"]
		else:
			images = images["still"]

		try:
			image = images[object.id % len(images)]
			print "Choose:", image

			file = self.application.media.GetFile(*image)
		except ZeroDivisionError, e:
			file = os.path.join("graphics", "unknown.png")
		except Exception, e:
			print e
			file = None

		if file is None:
			self.image_waiting = image[0]
			self.DisplayImage(os.path.join("graphics", "loading.png"))
		else:
			self.DisplayImage(file)

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

