"""\
This module contains the base classes used to build a new overlays for the
Starmap.
"""

import sys

from tp.netlib.objects import Object

class Overlay(dict):
	"""\
	A layer which displays something on the StarMap.
	"""	
	layer = None

	def name():
		raise NotImplementedError("This overlay has not specified a name! - This is bad!")
	name = property(staticmethod(name))

	def __init__(self, parent, canvas, panel, cache):
		"""
		Create a new Overlay object.

		parent is the application which can be used to post events.
		canvas is the wx.FloatCanvas to draw onto.
		panel  is the toolbar panel which the overlay can add it's own icons/widgets too.
		cache  is the libtpclient-py cache containing the universe data.
		"""
		self.parent      = parent
		self.application = self.parent.application 

		if canvas is None:
			raise TypeError("Canvas can not be none!")
		self.canvas = canvas

		if cache is None:
			raise TypeError("Cache can not be none!")
		self.cache  = cache

		self.panel  = panel

	def CleanUp(self):
		"""\
		Remove this overlay from the Canvas.
		"""
		for oid in self.keys():
			# Remove the old object
			del self[oid]

	def __setitem__(self, key, value):
		"""\
		Adds Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		if self.has_key(key):
			del self[key]

		if type(value) in (list, tuple):
			for v in value:
				if not self.layer is None:
					v.DrawOrder = self.layer
				self.canvas.AddObject(v)
		else:
			if not self.layer is None:
				value.DrawOrder = self.layer
			self.canvas.AddObject(value)
		dict.__setitem__(self, key, value)

	def __delitem__(self, oid):
		"""\
		Removes Drawable (or list of Drawables) for key and updates the Canvas.
		"""
		value = self[oid]

		if type(value) in (list, tuple):
			for v in value:
				v.UnBindAll()

				self.canvas.RemoveObject(v)
		else:
			value.UnBindAll()

			self.canvas.RemoveObject(value)
		dict.__delitem__(self, oid)

	def __del__(self):
		self.CleanUp()

	def __str__(self):
		return "<Overlay-%s %s>" % (self.__class__.__name__, hex(id(self)))
	__repr__ = __str__

	def Update(self, oid=None):
		"""\
		Update the FloatCanvas objects for this oid.

		Called when an object changes.
		"""
		if oid is None:
			self.UpdateAll()
		else:
			# Remove the old object.
			if self.has_key(oid):
				del self[oid]

			# If the oid is no longer in the cache we shouldn't continue.
			if not c.objects.has_key(oid):
				return

			# Otherwise Update the object.
			self.UpdateOne(oid)

	def UpdateAll(self):
		"""\
		Updates all objects on the Canvas.
		"""
		# Remove all the objects.
		self.CleanUp()

		# Sort the objects by name
		oids = self.cache.objects.keys()
		def objcmp(oida, oidb):
			return cmp(self.cache.objects[oida].name, self.cache.objects[oidb].name)
		oids.sort(objcmp)

		for oid in oids:
			self.UpdateOne(oid)

	def UpdateOne(self, oid):
		"""\
		Updates an object on the Canvas.
		"""
		pass

	def Focus(self):
		"""\
		Returns a tuple of,
			Selected object id (-1 for no object)
			The coordinates that the current overlay is focused at.

		This should probably be the selected object (but something else could be focused on other overlays). 
		"""
		return -1, (0,0)

	def ObjectSelect(self, oid):
		"""
		Select an object using an external event.

		Simulates this as a mouse click.
		"""
		raise NotImplementedError("Select Object method has not been implemented!")

class Holder(list):
	"""
	A holder is an entity which contains a "primary" object and a bunch of
	"children".

	It also maintains a pointer to the "current" object which can be advanced
	by the Loop methods.  
	"""

	def primary(self):
		"""
		The primary object.
		"""
		return self[0]
	primary = property(primary)

	def children(self):
		"""
		The rest of the objects.
		"""
		return self[1:]
	children = property(children)

	def current(self):
		"""
		The currently 'selected' object.
		"""
		if self.__current == -1:
			return None
		return self[self.__current]
	current = property(current)

	def __init__(self, primary, children=[]):
		if not isinstance(primary, Object):
			raise TypeError("Parent must be an Object not %r" % primary) 
		for i, child in enumerate(children):
			if not isinstance(child, Object):
				raise TypeError("Child %i must be an Object not %r" % (i, child)) 

		# Sort the children by name
		def childcmp(childa, childb):
			return cmp(childa.name, childb.name)
		children.sort(childcmp)

		self.extend([primary] + children)

		self.ResetLoop()

	def __eq__(self, value):
		if isinstance(value, Holder):
			return self.primary.id == value.primary.id
		return list.__eq__(self, value)

	def __str__(self):
		return "<%s %s>" % (self.__current, dict.__str__(self))

	def copy(self):
		return self.__class__(self.primary, self.children)

	def ResetLoop(self):
		"""
		Make the loop go back to the beginning.	
		"""
		self.__current = -1

	def NextLoop(self):
		"""
		Get the next object from the holder, this will loop around.
		"""
		self.__current = (self.__current + 1) % len(self)
		return self.__current, self.current

	def SetLoop(self, v):
		"""
		Set the loop's position to a given object.
		"""
		if not v in self:
			raise TypeError("That object %r doesn't exist in the Holder!" % v)
		self.__current = self.index(v)
		return self.__current

from extra.StateTracker import TrackerObject
#from tp.netlib.objects.ObjectExtra.Universe   import Universe
#from tp.netlib.objects.ObjectExtra.Galaxy     import Galaxy
class SystemLevelOverlay(Overlay, TrackerObject):
	"""
	A SystemLevelOverlay groups objects together at the Systems level.
	"""
	TopLevel = [] #Galaxy, Universe

	HoverTimeOutFirst = 2000
	HoverTimeOut      = 2000

	def __init__(self, *args, **kw):
		Overlay.__init__(self, *args, **kw)

		self.Selected = None
		self.Hovering = None

		self.Timer = wx.Timer()
		self.Timer.Bind(wx.EVT_TIMER, self.SystemHovering)

		self.Popup = ObjectPopup(self.canvas, wx.SIMPLE_BORDER)

		TrackerObject.__init__(self)

	def CleanUp(self):
		if self.Hovering != None:
			self.SystemLeave(self.Hovering)
		Overlay.CleanUp(self)

	def UpdateOne(self, oid):
		"""\

		"""
		obj = self.cache.objects[oid]

		# Only draw top level objects
		if isinstance(obj, self.TopLevel) or not hasattr(obj, 'parent'):
			return

		# Don't draw objects which parent's are not top level objects
		parent = self.cache.objects[obj.parent]
		if not isinstance(parent, self.TopLevel):
			return

		icon = self.Icon(obj)
		self[oid] = icon

		from extra.wxFloatCanvas.FloatCanvas import EVT_FC_ENTER_OBJECT, EVT_FC_LEAVE_OBJECT
		from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_UP, EVT_FC_RIGHT_UP
		from extra.wxFloatCanvas.FloatCanvas import EVT_FC_LEFT_DOWN, EVT_FC_RIGHT_DOWN

		# These pop-up the name of the object
		icon.Bind(EVT_FC_ENTER_OBJECT, self.SystemEnter)
		icon.Bind(EVT_FC_LEAVE_OBJECT, self.SystemLeave)
		# This is needed to the hit test doesn't fall through
		icon.Bind(EVT_FC_LEFT_DOWN, lambda x: True) 
		icon.Bind(EVT_FC_LEFT_UP, self.SystemLeftClick)
		icon.Bind(EVT_FC_RIGHT_DOWN, lambda x: True) 
		icon.Bind(EVT_FC_RIGHT_UP, self.SystemRightClick)

	def Focus(self):
		"""\
		Returns the coordinates of the currently selected object or the center
		of the universe.
		"""
		try:
			return self.Selected.primary.id, self.Selected.XY
		except Exception, e:
			return 0, (0,0)

	def ObjectSelect(self, oid):
		"""
		Select an object using an external event.

		Simulates this as a mouse click.
		"""
		if oid == None:
			return

		# Figure out which Icon this object is under
		parentid = oid
		while not self.has_key(parentid):
			try:
				parentid = self.cache.objects[parentid].parent
			except AttributeError:
				return

		system = self.cache.objects[parentid]
		real   = self.cache.objects[oid]

		icon = self[system.id].copy()
		icon.SetLoop(real)
		self.Selected = icon

		self.ObjectLeftClick(icon, real)
		#self.SystemEnter(self.Selected)

	def SystemRightClick(self, icon):
		# Leave the currently hovered system
		HoveredOn = self.SystemLeave(self.Hovering)

		self.ObjectRightClick(icon, HoveredOn.current)

	def SystemLeftClick(self, icon):
		# Leave the currently hovered system
		HoveredOn = self.SystemLeave(self.Hovering)

		# Are we clicking on the same object?
		SameSystem = (self.Selected == icon)
		if self.Selected == icon:
			# Cycle throught the children on each click
			self.Selected.NextLoop()

		# Select the same icon we are previewing
		elif HoveredOn == icon:
			self.Selected = HoveredOn

		# Clicking on a new object
		else:
			self.Selected = icon.copy()
			self.Selected.ResetLoop()

		if self.Selected.current == None:
			self.Selected.NextLoop()

		if self.ObjectLeftClick(self.Selected, self.Selected.current, SameSystem):
			# Post a selected event
			self.SelectObject(self.Selected.current.id)

		self.SystemEnter(self.Selected)

	def SystemEnter(self, icon):
		pos	= self.canvas.ClientToScreen(self.canvas.WorldToPixel(icon.XY))

		# Did someone forget to unhover?
		if self.Hovering != icon:
			self.SystemLeave(self.Hovering)

		# Set the new hover object
		self.Hovering = icon.copy()
		self.Hovering.ResetLoop()

		# Start hovering this icon
		self.ObjectHoverEnter(icon, pos)

		if self.Hovering != self.Selected:
			# Start the "preview" mode
			self.Timer.Start(self.HoverTimeOutFirst)

	def SystemHovering(self, event):
		# Reset the timer
		self.Timer.Stop()
		self.Timer.Start(self.HoverTimeOut)

		# Go to the next object
		i, object = self.Hovering.NextLoop()
		if self.ObjectHovering(self.Hovering, object):
			# Post a preview event
			self.PreviewObject(object.id)

	def ObjectPreview(self, id):
		pass

	def SystemLeave(self, icon):
		if icon == None:
			return

		# Stop the timer
		self.Timer.Stop()

		self.ObjectHoverLeave(icon)

		# Return back the originally selected object	
		if self.Hovering != None and self.Selected != None:
			self.SelectObject(self.Selected.current.id, True)

		t = self.Hovering
		# Clear the currently hovering object
		self.Hovering = None

		return t

	##########################################################################
	##########################################################################

	def ObjectLeftClick(self, icon, subobject, samesystem=False):
		"""
		Called when a person clicks on a system icon. 

		The first click with give the system object, each subsquent click with
		give a new subobject.

		Return True if you want a Selection event to be posted.
		"""
		return True

	def ObjectHoverEnter(self, icon, pos):
		"""
		Called when a person mouses over a system icon.
		Gets the icon and the position of the enter.
		"""
		text = self.ObjectPopupText(icon)
		if text != None:
			if sys.platform == "win32":
				pos = self.canvas.ScreenToClient(pos)
			self.Popup.Position(pos, icon.GetSize())
			self.Popup.SetText(text)
			self.Popup.Show()
			self.canvas.SetFocus()

	def ObjectHovering(self, icon, object):
		"""
		Called as a person continues to hover over a system icon.

		Return True if you want a Preview event to be posted.
		"""
		pass

	def ObjectHoverLeave(self, icon):
		"""
		Called when a person mouses over a system icon.
		"""
		self.Popup.Hide()

	def ObjectPopupText(self, icon):
		"""
		FancyText to put in the pop-up box.

		Return None to prevent the popup.
		"""
		pass	

import wx
from wx.lib.fancytext import StaticFancyText
class ObjectPopup(wx.PopupWindow):
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

		self.st = StaticFancyText(self.Window, -1, text.encode('UTF-8'), pos=(self.Padding, self.Padding))
		sz = self.st.GetSize()
		self.SetSize( (sz.width+2*self.Padding, sz.height+2*self.Padding) )

		self.st.Bind(wx.EVT_MOTION, self.parent.MotionEvent)
