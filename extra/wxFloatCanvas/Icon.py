
import numpy as N
from math import *

from FloatCanvas import DrawObject, XYObjectMixin

class Icon(DrawObject, XYObjectMixin):
	def __init__(self, point):
		DrawObject.__init__(self)
		self.SetPoint(point)

		self.icon    = []
		self.subicon = []
		self.real    = []

		self.children = []

	def FindChildren(self):
		children = []
		for child in self.children:
			children.append(child)
			children += child.FindChildren()
		return children

	def _DrawSize(self, WorldToPixel, ScaleWorldToPixel):
		return ScaleWorldToPixel(self.real[0].WH)[0]

	def _DrawSubIcon(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None, Offset=None):
		"""\
		Draw the object as part of another Icon.
		"""
		print self, Offset
		for icon in self.subicon:
			icon.SetOffset(Offset)
		icon._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)

	def _DrawIcon(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		"""\
		Draw the object as an Icon.
		"""

		# Draw the icon
		for i in self.icon:
			i._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)

		# Draw SubIcon of the children
		children = self.FindChildren()
		for i, child in enumerate(children):
			angle = ((2*pi)/len(children))*(i-0.125)
			offset = (int(cos(angle)*6), int(sin(angle)*6))

			child._DrawSubIcon(dc, WorldToPixel, ScaleWorldToPixel, HTdc, Offset=offset)
		
	def _DrawFull(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		"""\
		Draw the full object.
		"""
		for i in self.real:
			i._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)

		for child in self.children:
			child._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)

	def _DrawWeird(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		"""\
		FIXME: This shouldn't be needed.
		"""
		for i in self.real:
			i._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc)

		# Draw SubIcon of the children
		children = self.FindChildren()
		for i, child in enumerate(children):
			angle = ((2*pi)/len(children))*(i-0.125)
			offset = (int(cos(angle)*6), int(sin(angle)*6))

			child._DrawSubIcon(dc, WorldToPixel, ScaleWorldToPixel, HTdc, Offset=offset)

	def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
		# See how big the real object would be on the screen..
		if self._DrawSize(WorldToPixel, ScaleWorldToPixel) <= self.MinSize:
			self._DrawIcon(dc, WorldToPixel, ScaleWorldToPixel)
		else:
			t = False
			for child in self.children:
				if child._DrawSize(WorldToPixel, ScaleWorldToPixel) < self.MinSize:
					t = True

			print self, t
			if t:
				self._DrawWeird(dc, WorldToPixel, ScaleWorldToPixel, HTdc)
			else:		
				self._DrawFull(dc, WorldToPixel, ScaleWorldToPixel)

	def AddChild(self, child):
		self.children.append(child)

		if hasattr(child, "SetCenter"):
			child.SetCenter(self.XY)

