"""\
This overlay shows circles which are proportional to the amount of a certain
resource found in that object.
"""

# wxPython imports
import wx
from extra.wxFloatCanvas import FloatCanvas
from extra.wxFloatCanvas.CrossLine import CrossLine

from tp.client import objectutils

from Overlay import Overlay


class Velocity(Overlay):
	"""\
	"""
	name = "Velocity"

	def __init__(self, parent, canvas, panel):
		"""\
		Initializes the overlay and its resource selection panel.
		"""
		Overlay.__init__(self, parent, canvas, panel)

		self.Toggle = wx.ToggleButton(panel, -1, "Velocity")
		self.Toggle.SetValue(True)
		self.panel.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggle, self.Toggle)

		# Populate the colorizer dropdown with information
		sizer = wx.FlexGridSizer(1)
		sizer.AddGrowableRow(0)
		sizer.Add(self.Toggle, proportion=1, flag=wx.EXPAND)
		panel.SetSizer(sizer)

	def OnToggle(self, evt):
		self.UpdateAll()
		self.canvas.Draw()

	def UpdateOne(self, oid):
		"""\
		The amount of a specific resource in a specific object.
		"""
		if not self.Toggle.GetValue():
			return

		c = self.application.cache 
		o = c.objects[oid]

		position = objectutils.getPositionList(o)
		velocity = objectutils.getVelocityList(o)

		if len(position) != 1 or len(velocity) != 1:
			return

		if sum(velocity[0][0:3]) > 0:
			self[oid] = CrossLine(position[0][0:2], velocity[0][0:2], 4, LineColor="Grey")
