"""\
This module contains the Picture window. The Picture window
displays all objects information.
"""

# Python Imports
import os
import os.path
from types import *

import time
import pprint

# wxPython imports
import wx

try:
	from extra.GIFAnimationCtrl import GIFAnimationCtrl
except ImportError:
	from wx.animate import GIFAnimationCtrl

from extra.decorators import freeze_wrapper

# Network imports
#from tp.netlib.objects.ObjectExtra.Universe import Universe
#from tp.netlib.objects.ObjectExtra.Galaxy import Galaxy
#from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
#from tp.netlib.objects.ObjectExtra.Planet import Planet
#from tp.netlib.objects.ObjectExtra.Fleet import Fleet

from extra import objectutils

from tp.client.threads import FileTrackerMixin

# Config imports
from requirements import graphicsdir

def splitall(start):
	bits = []

	while True:
		start, end = os.path.split(start)
		if end is '':
			break
		bits.append(end)
	bits.reverse()
	return bits

WAITING = os.path.join(graphicsdir, "loading.gif")

from windows.xrc.panelPicture import panelPictureBase
class panelPicture(panelPictureBase, FileTrackerMixin):
	title = _("Picture")

	def __init__(self, application, parent):
		panelPictureBase.__init__(self, parent)
		FileTrackerMixin.__init__(self, application)
		
		self.application = application
		self.current = -1

		self.Animation.Hide()
		self.Static.Hide()

		# Find the images
		self.images = {'nebula':{'still':[]}, 'star':{'still':[]}, 'planet':{'still':[]}}

		self.Download.Hide()
		self.Static.Show()
		self.Animation.Hide()

		self.Layout()
		self.Update()

		self.application.gui.Binder(self.application.gui.SelectObjectEvent, self.OnSelectObject)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()

		s = wx.Size(128, 150)
		info.MinSize(s)
		info.BestSize(s)
		info.MaxSize(s)
		info.FloatingSize(s)
		info.Fixed()

		info.Left()
		info.Layer(2)
		info.CaptionVisible(True)
		info.Caption(self.title)
		return info

	def OnMediaUpdate(self, evt):
		files = {}
		for file in evt.files:
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
				files[key][type].append(file)
		self.images = files

	def OnMediaDownloadDone(self, evt):
		self.Progress.SetRange(0)
		self.Progress.SetValue(0)
		self.Speed.SetLabel('')
		self.ETA.SetLabel('')

		self.Download.Hide()

		self.Layout()
		self.Update()

		if evt is None:
			return
		
		if self.CheckURL(evt.file):
			self.RemoveURL(evt.file)
			self.OnSelectObject(self.application.cache.objects[self.current])

	@freeze_wrapper
	def DisplayImage(self, file, background=wx.BLACK):
		print "Setting background color to ", background
		self.Background.SetBackgroundColour(background)
		self.Static.SetBackgroundColour(background)
		self.Animation.SetBackgroundColour(background)

		print "Displaying", file
		if file.endswith(".gif"):
			print "Animated image!"
			self.Static.Hide()
			print "Showing the Image"	
			self.Animation.Show()
			print "Loading Image"
			self.Animation.LoadFile(file)
			print "Playing the Image"
			self.Animation.Play()
		else:
			print "Still image!"
			self.Static.Show()
			self.Animation.Stop()
			self.Animation.Hide()

			if file != "":
				bitmap = wx.BitmapFromImage(wx.Image(file))
			else:
				bitmap = wx.BitmapFromImage(wx.EmptyImage(128, 128))
			self.Static.SetBitmap(bitmap)

		self.Layout()

	def OnSelectObject(self, evt):
		self.current = evt.id

		try:
			object = self.application.cache.objects[evt.id]
		except:
			do_traceback()
			debug(DEBUG_WINDOWS, "SelectObject: No such object.")
			return

		self.Title.SetLabel(object.name)

		images = self.application.media.getImages(evt.id)
		self.ClearURLs()
		self.AddObjectURLs(evt.id)
		
		if len(images) <= 0:
			self.DisplayImage(os.path.join(graphicsdir, "unknown.png"))
		
		foundimage = False
		for name, files in images:
			if "Icon" in name:
				continue
		
			# Do something about multiple alternatives for the image here?
			filename = files[0]
			self.DisplayImage(filename)
			foundimage = True
		
		if not foundimage:
			file = os.path.join(graphicsdir, "unknown.png")
			self.DisplayImage(file)
