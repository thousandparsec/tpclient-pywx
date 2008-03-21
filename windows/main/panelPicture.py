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
from tp.netlib.objects.ObjectExtra.Universe import Universe
from tp.netlib.objects.ObjectExtra.Galaxy import Galaxy
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet import Planet
from tp.netlib.objects.ObjectExtra.Fleet import Fleet

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
class panelPicture(panelPictureBase):
	title = _("Picture")

	def __init__(self, application, parent):
		panelPictureBase.__init__(self, parent)

		self.application = application
		self.current = -1

		self.Animation.Hide()
		self.Static.Hide()

		# Find the images
		self.images = {'nebula':{'still':[]}, 'star':{'still':[]}, 'planet':{'still':[]}}

		self.progress = []
		self.averages = []

		self.Download.Hide()
		self.Static.Show()
		self.Animation.Hide()

		self.Layout()
		self.Update()

		self.application.gui.Binder(self.application.MediaClass.MediaUpdateEvent,			self.OnMediaUpdate)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadProgressEvent, self.OnMediaDownloadProgress)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadDoneEvent,		self.OnMediaDownloadDone)
		self.application.gui.Binder(self.application.gui.SelectObjectEvent, self.OnSelectObject)

	def GetPaneInfo(self):
		info = wx.aui.AuiPaneInfo()
		info.MinSize(wx.Size(128,150))
		info.MaxSize(wx.Size(128,150))
		info.FloatingSize(wx.Size(128,150))
		info.Fixed()

		info.Left()
		info.Layer(2)
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
	
	def OnMediaDownloadProgress(self, evt):
		self.Download.Show()

		self.Layout()
		self.Update()

		#print "winPicture.MediaDownloadProgress", evt.file

		self.progress.append((time.time(), evt.progress))
		# Trim off the oldest samples
		while len(self.progress) > 200:
			self.progress.pop(0)

		if len(self.progress) < 2:
			return

		average = []
		time1, progress1 = self.progress[0]
		for time2, progress2 in self.progress[1:]:
			average.append((progress2-progress1)/(time2-time1))
			time1, progress1 = time2, progress2

		# Calculate an average
		average = sum(average)/len(average)

		self.Progress.SetRange(evt.size)
		self.Progress.SetValue(evt.progress)

		if average < 10e3:
			self.Speed.SetLabel("%.2f kb/s" % (average/1e3))
		elif average < 1e6:
			self.Speed.SetLabel("%.0f kb/s" % (average/1e3))
		else:
			self.Speed.SetLabel("%.2f mb/s" % (average/1e6))

		self.averages.append(average)

		aaverage = (self.progress[-1][1]-self.progress[0][1])/(self.progress[-1][0]-self.progress[0][0])
		eta = (evt.size - evt.progress)/aaverage
		if eta > 60:
			eta = (int(eta)//60, eta-int(eta)//60*60)
			self.ETA.SetLabel("%im %is" % eta)
		else:
			self.ETA.SetLabel("%is" % eta)

		self.Download.Layout()
		self.Download.Update()

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

		print "winInfo.MediaDownloadDone - Finished D", evt.file, evt.localfile
		print "winInfo.MediaDownloadDone - Waiting On", self.image_waiting
		if evt.file == self.image_waiting:
			# FIXME: Should load the image now...
			self.DisplayImage(evt.localfile)

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
			elif isinstance(object, Fleet):
				images = self.images['ship']
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

			file = self.application.media.GetFile(image)
		except ZeroDivisionError, e:
			file = os.path.join(graphicsdir, "unknown.png")
		except Exception, e:
			print e
			file = None

		if file is None:
			self.image_waiting = image
			self.DisplayImage(os.path.join(graphicsdir, "loading.png"), wx.NullColour)
		else:
			self.image_waiting = None
			self.DisplayImage(file)
