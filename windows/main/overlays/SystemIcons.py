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
from tp.netlib.objects import Object, OrderDescs

from tp.netlib import GenericRS

from tp.client import objectutils

from requirements import graphicsdir

from tp.client.threads import FileTrackerMixin

from Overlay import SystemLevelOverlay, Holder
from Systems import *
from Colorizer import *

class ImageIcon(Group, Holder, IconMixIn):
	"""
	Display an image for an object.
	"""
	def copy(self):
		# FIXME: Very expensive
		return SystemIcon(self.tmpcache, self.primary, self.Colorizer)

	def __init__(self, tmpcache, canvas, system, image, colorizer=None):

		Holder.__init__(self, system, FindChildren(tmpcache, system))

		# Get the colors of the object
		IconMixIn.__init__(self, tmpcache, colorizer)
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
class SystemIcons(Systems, FileTrackerMixin):
	name = "Icons"
	Colorizers = [ColorVerses, ColorEach]

	def __init__(self, parent, canvas, panel, *args, **kw):
		Systems.__init__(self, parent, canvas, panel, *args, **kw)

		FileTrackerMixin.__init__(self, self.application)

	def Icon(self, obj):
		images = self.application.media.getImages(obj.id)
		self.ClearURLs()
		self.AddObjectURLs(obj.id)
		if len(images) <= 0:
			return SystemIcon(self.application.cache, obj, self.Colorizer)
		else:
			icon = None
			for name, files in images:
				if "Icon" not in name:
					continue
				
				# FIXME: Just use the first file. Might want to do something more?
				icon = wx.Image(files[0]).ConvertToBitmap()
				break
			
			if not icon:
				return SystemIcon(self.application.cache, obj, self.Colorizer)
		
		return ImageIcon(self.application.cache, self.canvas, obj, icon, self.Colorizer)
	
	def OnMediaUpdate(self, evt):
		self.UpdateAll()
	
	def OnMediaDownloadDone(self, evt):
		if evt is None:
			return

		if self.CheckURL(evt.file):
			self.RemoveURL(evt.file)
			self.UpdateAll()
