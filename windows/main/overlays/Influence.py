"""\
This overlay shows circles which are proportional to the amount of a certain
resource found in that object.
"""

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas

from tp.client import objectutils

from Overlay import Overlay

class Circle(FloatCanvas.Point):
	"""
	Display a round dot which is sized proportionally.
	"""
	
	def copy(self):
		# FIXME: Very expensive
		return Circle(self.tmpcache, self.obj, self.size)

	def __init__(self, tmpcache, obj, size):
		self.tmpcache = tmpcache
		self.obj = obj
		self.size = size

		

class Influence(Overlay):
	"""\
	"""
	name = "Influences"

	def __init__(self, parent, canvas, panel):
		"""\
		Initializes the overlay and its resource selection panel.
		"""
		Overlay.__init__(self, parent, canvas, panel)
		
		# Create a drop-down on the panel for colorizer
		self.InfluenceMode = wx.Choice(panel)
		self.InfluenceMode.Bind(wx.EVT_CHOICE, self.OnInfluenceMode)

		# Populate the colorizer dropdown with information
		sizer = wx.FlexGridSizer(1)
		sizer.AddGrowableRow(0)
		sizer.Add(self.InfluenceMode, proportion=1, flag=wx.EXPAND)
		panel.SetSizer(sizer)

		self.UpdateAll()
		self.canvas.Draw()

	
	def UpdateAll(self):
		self.shown_influences = None
		self.InfluenceMode.Clear()
		self.InfluenceMode.Append("None", None)
		self.InfluenceMode.SetSelection(0)
		for (group, name), desc in objectutils.possibleInfluences(self.application.cache):
			self.InfluenceMode.Append("%s - %s" % (group, name), (group, name))

		Overlay.UpdateAll(self)

	def OnInfluenceMode(self, evt):
		self.shown_influences = [self.InfluenceMode.GetClientData(self.InfluenceMode.GetSelection())]
		Overlay.UpdateAll(self)
		self.canvas.Draw()

	def UpdateOne(self, oid):
		"""\
		The amount of a specific resource in a specific object.
		"""
		c = self.application.cache 
		o = c.objects[oid]

		pos = objectutils.getPositionList(o)
		if len(pos) <= 0:
			return

		if not self.shown_influences:
			return

		for influence_name in self.shown_influences:
			influence = objectutils.getInfluence(c, oid, influence_name)
			if influence is False:
				return
			icon = FloatCanvas.Circle(pos[0][0:2], influence, LineColor='Blue', FillColor='Blue')
			icon.DrawOrder = -influence
			self[oid] = icon
