"""\
This overlay draws Star Systems on the Starmap.
"""
# Python imports
from math import *

import numpy as N

# wxPython imports
import wx
from extra.wxFloatCanvas.FloatCanvas   import Point, Group
from extra.wxFloatCanvas.RelativePoint import RelativePoint, RelativePointSet
from extra.wxFloatCanvas.PolygonStatic import PolygonArrow, PolygonShip

from extra.wxFloatCanvas.FloatCanvas import EVT_FC_ENTER_OBJECT, EVT_FC_LEAVE_OBJECT
from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_UP, EVT_FC_RIGHT_UP

# tp imports
from tp.netlib.objects                        import Object
from tp.netlib.objects.ObjectExtra.Universe   import Universe
from tp.netlib.objects.ObjectExtra.Galaxy     import Galaxy
from tp.netlib.objects.ObjectExtra.StarSystem import StarSystem
from tp.netlib.objects.ObjectExtra.Planet     import Planet
from tp.netlib.objects.ObjectExtra.Fleet      import Fleet

from Overlay   import Overlay, Holder
from Colorizer import *

def FindChildren(cache, obj):
	"""
	Figure out all the children of this object.
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	kids = set()
	for cid in obj.contains:
		child = cache.objects[cid]

		kids.update(FindChildren(cache, child))
		kids.add(child)

	return list(kids)

def FindOwners(cache, obj):
	"""
	Figure out the owners of this oidect (and it's children).
	"""
	if not isinstance(obj, Object):
		raise TypeError("Object must be an object not %r" % obj)

	owners = set()
	for child in [obj]+FindChildren(cache, obj):
		if not hasattr(child, 'owner'):
			continue

		if child.owner in (0, -1):
			continue
		owners.add(child.owner)
	return list(owners)

class IconMixIn:
	"""
	"""
	PrimarySize = 3
	ChildSize   = 3

	def __init__(self, cache, colorizer):
		self.cache = cache
		self.SetColorizer(colorizer)

	# FIXME: Should probably just monkey patch this onto Group?
	def XY(self):
		return self.ObjectList[0].XY
	XY = property(XY)

	def ChildOffset(self, i):
		num = len(self.children)

		angle = ((2.0*pi)/num)*(i-0.125)
		return (int(cos(angle)*6), int(sin(angle)*6))

	def SetColorizer(self, colorizer):
		if not isinstance(colorizer, Colorizer):
			raise TypeError('Colorizer must be of Colorizer type!')
		self.Colorizer = colorizer

	def GetColors(self):
		parentcolor = self.Colorizer(FindOwners(self.cache, self.primary))
		
		childrencolors = []
		for child in self.children:
			childrencolors.append(self.Colorizer(FindOwners(self.cache, child)))
	
		return parentcolor, childrencolors

class SystemIcon(Group, Holder, IconMixIn):
	"""
	Display a round dot with a dot for each child.
	"""
	def __init__(self, cache, system, colorizer=None):
		if not isinstance(system, StarSystem):
			raise TypeError('SystemIcon must be given a StarSystem, %r' % system)

		Holder.__init__(self, system, FindChildren(cache, system))

		# Get the colors of the object
		IconMixIn.__init__(self, cache, colorizer)
		type, childtype = self.GetColors()

		# Create a list of the objects
		ObjectList = []

		# The center point
		print type, childtype
		ObjectList.append(Point(system.pos[0:2], type, self.PrimarySize, False))

		if len(self.children) > 0:
			# The orbit bits
			ObjectList.insert(0, Point(system.pos[0:2], "Black", 8))
			ObjectList.insert(0, Point(system.pos[0:2], "Grey",  9, False))
	
			# The orbiting children
			for i, childtype in enumerate(childtype):
				ObjectList.append(
					RelativePoint(system.pos[0:2], childtype, self.ChildSize, False, self.ChildOffset(i))
				)

		Group.__init__(self, ObjectList, False)

class FleetIcon(Group, Holder, IconMixIn):
	"""
	Display a little arrow shape thing.
	"""

	def __init__(self, cache, fleet, colorizer=None):
		if not isinstance(system, Fleet):
			raise TypeError('FleetIcon must be given a Fleet, %r' % system)

		if len(FindChildren(fleet)) > 0:
			raise TypeError('The fleet has children! WTF?')

		Holder.__init__(self, fleet, [])

		# Get the colors of the object
		IconMixIn.__init__(self, cache, colorizer)
		type, childtype = self.GetColors()

		# Create a list of the objects
		ObjectList = []

		# The little ship icon
		ObjectList.append(PolygonShip(pos, type))

		Group.__init__(self, ObjectList, False)


from wx.lib.fancytext import StaticFancyText
class NamePopup(wx.PopupWindow):
	Padding = 2

	def __init__(self, parent, style):
		wx.PopupWindow.__init__(self, parent, style)

		self.parent = parent

		self.SetBackgroundColour("#202020")
		self.Bind(wx.EVT_MOTION, parent.MotionEvent)

	def SetText(self, text):
		try:
			self.st.Unbind(wx.EVT_MOTION)
			self.st.Destroy()
		except AttributeError:
			pass

		self.st = StaticFancyText(self.Window, -1, text, pos=(self.Padding, self.Padding))
		sz = self.st.GetSize()
		self.SetSize( (sz.width+2*self.Padding, sz.height+2*self.Padding) )

		self.st.Bind(wx.EVT_MOTION, self.parent.MotionEvent)

class Systems(Overlay):
	toplevel = Galaxy, Universe

	def __init__(self, *args, **kw):
		Overlay.__init__(self, *args, **kw)

		self.canvas.SetCursor(wx.StockCursor(wx.CURSOR_RIGHT_ARROW))

		self.Selected = None
		self.Hovering = None
		self.Timer = wx.Timer()
		self.Timer.Bind(wx.EVT_TIMER, self.OnHover)

		self.PopupText = NamePopup(self.canvas, wx.SIMPLE_BORDER)

	def updateall(self):
		#self.Colorizer = ColorVerses(self.cache.players[0].id)
		self.Colorizer = ColorEach()

		Overlay.updateall(self)

		self['selected-arrow'] = PolygonArrow((0,0), "Red", True)
		self['preview-arrow']  = PolygonArrow((0,0), "#555555", True)
		self['preview-arrow'].Hide()

	def updateone(self, oid):
		"""\

		"""
		obj = self.cache.objects[oid]

		# Only draw top level objects
		if isinstance(obj, Systems.toplevel) or not hasattr(obj, 'parent'):
			return

		# Don't draw objects which parent's are not top level objects
		parent = self.cache.objects[obj.parent]
		if not isinstance(parent, Systems.toplevel):
			return

		if isinstance(obj, Fleet):
			self[oid] =  FleetIcon(self.cache, obj, self.Colorizer)
		else:
			self[oid] = SystemIcon(self.cache, obj, self.Colorizer)

		# These pop-up the name of the object
		self[oid].Bind(EVT_FC_ENTER_OBJECT, self.SystemEnter)
		self[oid].Bind(EVT_FC_LEAVE_OBJECT, self.SystemLeave)
		self[oid].Bind(EVT_FC_LEFT_UP, self.SystemLeftClick)

	def ArrowTo(self, arrow, obj, i):
		arrow.SetPoint(obj.primary.pos[0:2])
		arrow.SetOffset((0,0))
		if i > 0:
			arrow.SetOffset(obj.ChildOffset(i-1))
		self.canvas.Draw()

	def SelectObject(self, oid):
		parentid = oid
		while not self.has_key(parentid):
			try:
				parentid = self.cache.objects[parentid].parent
			except AttributeError:
				return

		obj = self[parentid]
		i   = obj.SetLoop(self.cache.objects[oid])

		self.Selected = obj
		self.ArrowTo(self['selected-arrow'], obj, i)

	def SystemLeftClick(self, obj):
		print "SystemClick", obj

		# Are we clicking on the same object?
		if self.Selected != obj:
			self.Selected = obj
			self.Selected.ResetLoop()

		# Cycle throught the children on each click
		i, real = self.Selected.NextLoop()
		
		self.ArrowTo(self['selected-arrow'], obj, i)

		self.SystemLeave(obj)
		self.SystemEnter(obj)

		self.parent.PostSelectObject(real.id)

	def SystemEnter(self, obj):
		print "SystemEnter", obj
		screen = self.canvas.WorldToPixel(obj.XY)
		pos	= self.canvas.ClientToScreen( screen )

		# Build the string
		s = "<font size='%s'>" % wx.local.normalFont.GetPointSize()
		for i, cobj in enumerate(obj):
			# Italics the currently selected object
			style = 'normal'
			if self.Selected.current == cobj:
				style = 'italic'

			color = obj.Colorizer(FindOwners(self.cache, cobj))

			s += "<font style='%s' color='%s'>%s" % (style, color, cobj.name)
			if isinstance(cobj, Fleet):
				for shipid, amount in cobj.ships:
					s+= "\n  %s %ss" % (amount, self.cache.designs[shipid].name)
			s += "</font>\n"

		s = s[:-1]+"</font>"

		self.PopupText.SetText(s)
		self.PopupText.Position(pos, (IconMixIn.PrimarySize, IconMixIn.PrimarySize))
		self.PopupText.Show(True)

		# Start the "preview" mode
		if obj != self.Selected:
			self.Hovering = obj
			self.Hovering.ResetLoop()

			self.Timer.Start(2000)

	def SystemLeave(self, obj):
		self.PopupText.Hide()

		# Stop the "preview"
		self.Timer.Stop()
		self['preview-arrow'].Hide()
		self.canvas.Draw()
	
		if self.Selected != None:
			self.parent.PostSelectObject(self.Selected.current.id)

	def OnHover(self, evt):
		i, real = self.Hovering.NextLoop()
		self.parent.PostPreviewObject(real.id)

		self['preview-arrow'].Show()
		self.ArrowTo(self['preview-arrow'], self.Hovering, i)
		self.Timer.Start(2000)
		
