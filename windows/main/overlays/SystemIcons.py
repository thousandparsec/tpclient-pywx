"""\
This overlay draws Star Systems on the Starmap using their self-specified icons.
"""
# Python imports
from math import *
import copy
import numpy as N
import os.path

# wxPython imports
import wx
from extra.wxFloatCanvas.FloatCanvas   import Point, Group, Line, Bitmap, ScaledBitmap
from extra.wxFloatCanvas.RelativePoint import RelativePoint, RelativePointSet
from extra.wxFloatCanvas.PolygonStatic import PolygonArrow, PolygonShip

# tp imports
from tp.netlib.objects import constants
from tp.netlib.objects                        import Object, OrderDescs

from tp.netlib import GenericRS

from extra import objectutils

from requirements import graphicsdir

from Overlay   import SystemLevelOverlay, Holder
from Systems import *
from Colorizer import *

class ImageIcon(Group, Holder, IconMixIn):
	"""
	Display an image for an object.
	"""
	def copy(self):
		# FIXME: Very expensive
		return SystemIcon(self.cache, self.primary, self.Colorizer)

	def __init__(self, cache, canvas, system, image, colorizer=None):

		Holder.__init__(self, system, FindChildren(cache, system))

		# Get the colors of the object
		IconMixIn.__init__(self, cache, colorizer)
		type, childtype = self.GetColors()

		# Create a list of the objects
		ObjectList = []
		
		# Get the positions.
		positionslist = objectutils.getPositionList(system)
		
		# Add the images here.
		if len(positionslist) > 0:
			# FIXME: Should this really just use the first position?
			position = canvas.ScaleWorldToPixel(positionslist[0][0:2])
			centeredpos = (position[0] - image.GetWidth()/2, position[1] - image.GetHeight()/2)
			centeredpos = canvas.ScalePixelToWorld(centeredpos)
			ObjectList.append(Bitmap(image, centeredpos, InForeground=True))
		
		Group.__init__(self, ObjectList, False)

from extra.StateTracker import TrackerObjectOrder
class SystemIcons(Systems):
	name     = "Icons"
	toplevel = [] #Galaxy, Universe

	Colorizers = [ColorVerses, ColorEach]

	def __init__(self, parent, canvas, panel, cache, *args, **kw):
		Systems.__init__(self, parent, canvas, panel, cache, *args, **kw)
		
		self.application.gui.Binder(self.application.MediaClass.MediaUpdateEvent, self.OnMediaUpdate)
		self.application.gui.Binder(self.application.MediaClass.MediaDownloadDoneEvent,	self.OnMediaDownloadDone)

		self.waitingimages = {}


	def Icon(self, obj):
		icons = objectutils.getIconURLs(self.application, obj.id)
		if not len(icons) == 0:
			file = self.application.media.GetFile(icons[0])
			
			if file == None:
				icon = wx.Image(os.path.join(graphicsdir, "unknown-icon.png")).ConvertToBitmap()
				self.waitingimages[icons[0]] = 1
			else:	
				icon = wx.Image(file).ConvertToBitmap()
				
			# FIXME: Should we do something about multiple icons?
			return ImageIcon(self.cache, self.canvas, obj, icon, self.Colorizer)
		
		return SystemIcon(self.cache, obj, self.Colorizer)
		
	
	def OnMediaUpdate(self, evt):
		self.UpdateAll()
	
	def OnMediaDownloadDone(self, evt):
		if evt is None:
			return

		if self.waitingimages.has_key(evt.file):
			del self.waitingimages[evt.file]
			self.UpdateAll()
