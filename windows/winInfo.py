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
	
	def __init__(self, application, parent):
		winBase.__init__(self, application, parent)

		self.Panel = panelInformation(application, self)

	def __getattr__(self, key):
		try:
			return winBase.__getattr__(self, key)
		except AttributeError:
			return getattr(self.Panel, key)

from xrc.panelInformation import panelInformationBase
class panelInformation(panelInformationBase):
	title = _("Information")
	from defaults import winInfoDefaultSize as DefaultSize

	def __init__(self, application, parent):
		panelInformationBase.__init__(self, parent)

		self.application = application
		self.current = -1

		self.Animation.Hide()
		self.Image.Hide()

		# Find the images
		self.images = {'nebula':{'still':[]}, 'star':{'still':[]}, 'planet':{'still':[]}}

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(self.GetBestSize())
		info.Left()
		info.Layer(2)
		return info

	def OnMediaUpdate(self, evt):
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
			self.Image.Hide()
			print "Showing the Image"	
			self.Animation.Show()
			print "Loading Image"
			self.Animation.LoadFile(file)
			print "Playing the Image"
			self.Animation.Play()
		else:
			print "Still image!"
			self.Image.Show()
			self.Animation.Stop()
			self.Animation.Hide()

			if file != "":
				bitmap = wx.BitmapFromImage(wx.Image(file))
			else:
				bitmap = wx.BitmapFromImage(wx.EmptyImage(128, 128))
			self.Image.SetBitmap(bitmap)
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

		self.Title.SetLabel(object.name)

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
				s += "Ships: "
				# FIXME: This is a hack :/
				for t, number in value:
					if self.application.cache.designs.has_key(t):
						design = self.application.cache.designs[t]
						s += "%s %s, " % (number, design.name)
					else:
						print "Unknown Design id:", t
						s += "%s %s, " % (number, "Unknown (type: %s)" % t)
				s = s[:-2] + "\n"
				continue

			key = key.title()
			if type(value) == StringType:
				s += "%s: %s\n" % (key, value)
			elif type(value) in (ListType, TupleType):
				s += "%s: " % (key,)
				for i in value:
					s += "%s, " % (i,)
				s = s[:-2] + "\n"
			else:
				s += "%s: %s\n" % (key, value)

		self.Details.SetValue(s)

