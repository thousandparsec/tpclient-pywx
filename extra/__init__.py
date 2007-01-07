
import string
import wx
import wx.gizmos
import wx.lib.mixins.listctrl

########################
# This fix allows me to globaly register XRC handlers
########################
import wx.xrc as xrc
from wx.xrc import EmptyXmlResource as EmptyXmlResourceOrig

EmptyXmlResourceOrig()

xrc.ExtraHandlers = []
def XmlResourceWithHandlers(*args, **kw):
	if len(args)+len(kw) > 1:
		raise RuntimeError("Don't know what to do with all the arguments!")
	if len(args) > 0:
		f = args[0]
	else:
		f = kw['file']

	res = EmptyXmlResourceOrig()
	for handler in xrc.ExtraHandlers:
		res.InsertHandler(handler())
	res.Load(f)
	return res
xrc.XmlResourceWithHandlers = XmlResourceWithHandlers

def EmptyXmlResourceWithHandlers(*args, **kwargs):
	res = EmptyXmlResourceOrig(*args, **kwargs)
	for handler in xrc.ExtraHandlers:
		res.InsertHandler(handler())
	return res
xrc.EmptyXmlResourceWithHandlers = EmptyXmlResourceWithHandlers

import wx.gizmos
from wx.gizmos import EditableListBox
class EditableListBoxXmlHandler(xrc.XmlResourceHandler):
	def __init__(self):
		xrc.XmlResourceHandler.__init__(self)
		# Specify the styles recognized by objects of this type
		self.AddStyle("wxEL_ALLOW_NEW", wx.gizmos.EL_ALLOW_NEW)
		self.AddStyle("wxEL_ALLOW_EDIT", wx.gizmos.EL_ALLOW_EDIT)
		self.AddStyle("wxEL_ALLOW_DELETE", wx.gizmos.EL_ALLOW_DELETE)
		self.AddWindowStyles()

	# This method and the next one are required for XmlResourceHandlers
	def CanHandle(self, node):
		return self.IsOfClass(node, "wxEditableListBox") or self.IsOfClass(node, "EditableListBox")

	def DoCreateResource(self):
		# The simple method assumes that there is no existing
		# instance.  Be sure of that with an assert.
		assert self.GetInstance() is None

		ctrl = EditableListBox(self.GetParentAsWindow(),
								self.GetID(),
								"", #self.GetLabel(),
								self.GetPosition(),
								self.GetSize(),
								self.GetStyle(),
								self.GetName(),
								)

		# These two things should be done in either case:
		# Set standard window attributes
		self.SetupWindow(ctrl)
		# Create any child windows of this node
		self.CreateChildren(ctrl)

		return ctrl
xrc.ExtraHandlers.append(EditableListBoxXmlHandler)

class ListCtrlXmlHandler(xrc.XmlResourceHandler):
	extra_styles = [
		"LC_LIST",
		"LC_REPORT",
		"LC_VIRTUAL",
		"LC_ICON",
		"LC_SMALL_ICON",
		"LC_ALIGN_TOP",
		"LC_ALIGN_LEFT",
		"LC_AUTOARRANGE",
		"LC_EDIT_LABELS",
		"LC_NO_HEADER",
		"LC_SINGLE_SEL",
		"LC_SORT_ASCENDING",
		"LC_SORT_DESCENDING",
		"LC_HRULES",
		"LC_VRULES"]

	def __init__(self):
		xrc.XmlResourceHandler.__init__(self)
		# Specify the styles recognized by objects of this type
		self.AddWindowStyles()
		for style in self.extra_styles:
			self.AddStyle("wx%s" % style, getattr(wx, style))

	# This method and the next one are required for XmlResourceHandlers
	def CanHandle(self, node):
		return self.IsOfClass(node, "wxListCtrl") or self.IsOfClass(node, "ListCtrl")

	def DoCreateResource(self):
		print "DoCreateResource", self
		# The simple method assumes that there is no existing
		# instance.  Be sure of that with an assert.
		if self.GetInstance() is None:
			ctrl = wx.ListCtrl(self.GetParentAsWindow(),
									self.GetID(),
									self.GetPosition(),
									self.GetSize(),
									self.GetStyle(),
									name=self.GetName(),
									)
		else:
			ctrl = self.GetInstance()

			# Now call the ctrl's Create method to actually create the window
			ctrl.Create(self.GetParentAsWindow(),
						 self.GetID(),
						 self.GetPosition(),
						 self.GetSize(),
						 self.GetStyle(),
						 name = self.GetName()
						 )


		# These two things should be done in either case:
		# Set standard window attributes
		self.SetupWindow(ctrl)
		# Create any child windows of this node
		self.CreateChildren(ctrl)

		return ctrl
xrc.ExtraHandlers.append(ListCtrlXmlHandler)

class ChoiceXmlHandler(xrc.XmlResourceHandler):
	def __init__(self):
		xrc.XmlResourceHandler.__init__(self)
		# Specify the styles recognized by objects of this type
		self.AddWindowStyles()

	# This method and the next one are required for XmlResourceHandlers
	def CanHandle(self, node):
		return self.IsOfClass(node, "wxChoice") or self.IsOfClass(node, "Choice")

	def DoCreateResource(self):
		print "DoCreateResource", self
		# The simple method assumes that there is no existing
		# instance.  Be sure of that with an assert.
		if self.GetInstance() is None:
			ctrl = wx.Choice(self.GetParentAsWindow(),
									self.GetID(),
									self.GetPosition(),
									self.GetSize(),
									[],
									self.GetStyle(),
									name=self.GetName(),
									)
		else:
			ctrl = self.GetInstance()

			# Now call the ctrl's Create method to actually create the window
			ctrl.Create(self.GetParentAsWindow(),
						 self.GetID(),
						 self.GetPosition(),
						 self.GetSize(),
						 [],
						 self.GetStyle(),
						 name = self.GetName()
						 )


		# These two things should be done in either case:
		# Set standard window attributes
		self.SetupWindow(ctrl)
		# Create any child windows of this node
		self.CreateChildren(ctrl)

		return ctrl
xrc.ExtraHandlers.append(ChoiceXmlHandler)


########################
# This fix allows me to have tooltips on individual items rather then just the whole control.
########################
class ToolTipItemMixIn:
	def __init__(self):
		self.tooltips = {}

	def SetToolTipDefault(self, tooltip):
		if isinstance(tooltip, wx.ToolTip):
			tooltip = tooltip.GetTip()
		self.tooltips[-1] = tooltip
		self.SetToolTip(wx.ToolTip(tooltip))

	def SetToolTipItem(self, slot, text):
		self.tooltips[slot] = text
	
	def GetToolTipItem(self, slot):
		if self.tooltips.has_key(slot):
			return self.tooltips[slot]
		else:
			return None

	def SetToolTipCurrent(self, slot):
		if self.tooltips.has_key(slot):
			if self.GetToolTip() == None:
				self.SetToolTip(wx.ToolTip(self.tooltips[slot]))
			elif self.GetToolTip().GetTip() != self.tooltips[slot]:
				self.GetToolTip().SetTip(self.tooltips[slot])

wx.ChoiceOrig = wx.Choice
class wxChoice(wx.Choice, ToolTipItemMixIn):
	def __init__(self, *arg, **kw):
		wx.ChoiceOrig.__init__(self, *arg, **kw)
		ToolTipItemMixIn.__init__(self)
		
		self.Bind(wx.EVT_CHOICE, self.OnSelection)

	def OnSelection(self, evt):
		slot = self.GetSelection()
		self.SetToolTipCurrent(slot)

wx.ComboBoxOrig = wx.ComboBox
class wxComboBox(wx.ComboBox, ToolTipItemMixIn):
	def __init__(self, *arg, **kw):
		wx.ComboBoxOrig.__init__(self, *arg, **kw)
		ToolTipItemMixIn.__init__(self)

		self.Bind(wx.EVT_COMBOBOX, self.OnSelection)

	def OnSelection(self, evt):
		slot = self.GetSelection()
		self.SetToolTipCurrent(slot)

########################
# This fix fixes a bunch of broken stuff with the ListCtrl and adds a few more
# functionality which should be default.
########################
import wx.lib.mixins.listctrl as mlc

wx.ListCtrlOrig = wx.ListCtrl
class wxListCtrl(wx.ListCtrlOrig, mlc.ListCtrlAutoWidthMixin, mlc.ColumnSorterMixin, ToolTipItemMixIn):
	def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, *args, **kw):
		wx.ListCtrlOrig.__init__(self, parent, ID, pos, size, *args, **kw)
		mlc.ListCtrlAutoWidthMixin.__init__(self)
		mlc.ColumnSorterMixin.__init__(self, self.GetColumnCount())
		ToolTipItemMixIn.__init__(self)

		self.objects = []
		self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

	#############################################################################
	# ColumnSorterMixin: This adds support for sorting then clicking the headers
	#############################################################################
	def GetColumnSorter(self):
		return self.__ColumnSorter

	def __ColumnSorter(self, key1, key2):
		col = self._col
		ascending = self._colSortFlag[col]

		v1 = self.GetStringItem(key1, col)
		v2 = self.GetStringItem(key2, col)
		if not ascending:
			return cmp(v1, v2)
		else:
			return -cmp(v1, v2)

	def GetSortImages(self):
		# FIXME: This is a strange place to put this.
		# This makes sure the selected items still have focus after sorting
		item = self.GetNextItem(-1)
		while item != -1:
			if self.GetItemState(item, wx.LIST_STATE_SELECTED) == 0:
				self.SetItemState(item, 0, wx.LIST_STATE_FOCUSED)
			else:
				self.SetItemState(item, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)

			item = self.GetNextItem(item)

		# Update the slots as we have reorganised them
		slot = -1
		while True:
			slot = self.GetNextItem(slot, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE)
			if slot == wx.NOT_FOUND:
				break
			self.SetItemData(slot, slot)

		return (-1, -1)

	def InsertColumn(self, *args, **kw):
		super(self.__class__, self).InsertColumn(*args, **kw)
		self.SetColumnCount(self.GetColumnCount())

	def GetListCtrl(self):
		return self
	#############################################################################

	#############################################################################
	# This stuff makes the PyData stuff actually work and allows searching on the
	# pyData
	#############################################################################
	def InsertItem(self, item):
		slot = wx.ListCtrlOrig.InsertItem(self, item)
		self._increasePyData(slot)
		
	def InsertStringItem(self, slot, label):
		wx.ListCtrlOrig.InsertStringItem(self, slot, label)
		self._increasePyData(slot)
		
	def InsertImageItem(self, slot, imageIndex):
		wx.ListCtrlOrig.InsertImageItem(self, slot, imageIndex)
		self._increasePyData(slot)
		
	def InsertImageStringItem(self, slot, label, imageIndex):
		wx.ListCtrlOrig.InsertImageStringItem(self, slot, label, imageIndex)
		self._increasePyData(slot)

	def _increasePyData(self, slot):
		self.objects.insert(slot, None)
		self.SetItemData(slot, slot)

	def SetItemPyData(self, slot, data):
		self.objects[slot] = data

	def GetItemPyData(self, slot):
		try:
			return self.objects[slot]
		except IOError:
			return None

	def DeleteItem(self, slot):
		del self.objects[slot]
		wx.ListCtrlOrig.DeleteItem(self, slot)

	def DeleteAllItems(self):
		self.objects = []
		wx.ListCtrlOrig.DeleteAllItems(self)
	
	def FindItemByPyData(self, data):
		slot = -1
		while True:
			slot = self.GetNextItem(slot, wx.LIST_NEXT_ALL, wx.LIST_STATE_DONTCARE);
			if slot == wx.NOT_FOUND:
				return wx.NOT_FOUND
				
			if self.GetItemPyData(slot) == data:
				return slot

	def GetStringItem(self, slot, col):
		item = self.GetItem(slot, col)
		if item == wx.NOT_FOUND:
			return wx.NOT_FOUND
		else:
			return item.GetText()

	# Display individual line tooltips
	def OnMouseMotion(self, evt):
		slot = self.HitTest(evt.GetPosition())[0]
		self.SetToolTipCurrent(slot)

	# This prevents perious errors about wxPyDeadObject
	def _doResize(self):
		if hasattr(wx, 'core'):
			try:
				if not isinstance(self, wx.core._wxPyDeadObject):
					wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin._doResize(self)
			except wx.core.PyDeadObjectError:
				pass
		else:
			wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin._doResize(self)

	#############################################################################
	# This stuff makes working with selected items much easier
	#############################################################################
	def GetSelected(self):
		slots = [-1,]
		while True:
			slot = self.GetNextItem(slots[-1], wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
			if slot != wx.NOT_FOUND:
				slots.append(slot)
			else:
				slots = slots[1:]
				break
		
		slots.reverse()
		return slots

	def SetSelected(self, slots):
		# Unselect the currently selected items
		for slot in self.GetSelected():
			self.SetItemState(slot, 0, wx.LIST_STATE_SELECTED)

		for slot in slots:
			self.SetItemState(slot, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
		
	def AddSelected(self, slot):
		self.SetItemState(slot, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

########################
# This adds a TreeCtrl which orders itself by the Python Data.
########################
class OrderedTreeCtrl(wx.TreeCtrl):
	def __init__(self, *args, **kw):
		wx.TreeCtrl.__init__(self, *args, **kw)
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self)

	def OnActivate(self, evt):
		item = evt.GetItem()
		self.Toggle(item)

	def OnCompareItems(self, item1, item2):
		t1 = self.GetItemText(item1)
		t2 = self.GetItemText(item2)
		if t1 < t2: return -1
		if t1 == t2: return 0
		return 1

	def GetPyData(self, item):
		if not item.IsOk():
			return None
		return wx.TreeCtrl.GetItemPyData(self, item)

	def FindItemByData(self, pyData, compare=None, item=None):
		if item == None:
			item = self.GetRootItem()

		if not item.IsOk():
			return None

		if not compare is None and compare(pyData, self.GetPyData(item)):
			return item
		elif self.GetPyData(item) == pyData:
			return item
		
		if self.ItemHasChildren(item):
			cookieo = -1
			child, cookie = self.GetFirstChild(item)

			while cookieo != cookie:
				r = self.FindItemByData(pyData, compare, child)
				if r:
					return r
					
				cookieo = cookie
				child, cookie = self.GetNextChild(item, cookie)

		return None

	def FindAllByData(self, pyData, compare=None, item=None, r=None):
		if r == None:
			r = []

		if item == None:
			item = self.GetRootItem()

		if not item.IsOk():
			return None

		if not compare is None:
			if compare(pyData, self.GetPyData(item)):
				r.append(item)
		else:
			if self.GetPyData(item) == pyData:
				r.append(item)
		
		if self.ItemHasChildren(item):
			cookieo = -1
			child, cookie = self.GetFirstChild(item)

			while cookieo != cookie:
				self.FindAllByData(pyData, compare, child, r)
				
				cookieo = cookie
				child, cookie = self.GetNextChild(item, cookie)
		return r

wx.OrderedTreeCtrl = OrderedTreeCtrl

########################
# This adds a simple validator which only takes DIGITs and ALPHA characters.
########################
wx.DIGIT_ONLY = 1
wx.ALPHA_ONLY = 2
class wxSimpleValidator(wx.PyValidator):
	def __init__(self, flag=None, pyVar=None):
		wx.PyValidator.__init__(self)
		self.flag = flag
		self.Bind(wx.EVT_CHAR, self.OnChar)

	def Clone(self):
		return wxSimpleValidator(self.flag)

	def Validate(self, win):
		tc = self.GetWindow()
		val = tc.GetValue()
		
		if self.flag == wx.ALPHA_ONLY:
			for x in val:
				if x not in string.letters:
					return False

		elif self.flag == wx.DIGIT_ONLY:
			try:
				if val != '-':
					long(val)
				return True
			except TypeError:
				return False
		return True

	def OnChar(self, event):
		key = event.KeyCode()
		if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
			event.Skip()
			return
		if self.flag == wx.ALPHA_ONLY and chr(key) in string.letters:
			event.Skip()
			return
		if self.flag == wx.DIGIT_ONLY and chr(key) in string.digits:
			event.Skip()
			return
		if self.flag == wx.DIGIT_ONLY and chr(key) in '-+':
			event.Skip()
			return
		if not wx.Validator_IsSilent():
			wx.Bell()
		# Returning without calling even.Skip eats the event before it
		# gets to the text control
		return

wx.ListCtrl = wxListCtrl
wx.Choice = wxChoice
wx.ComboBox = wxComboBox
wx.SimpleValidator = wxSimpleValidator

from PopupCtrl import PopupCtrl
wx.PopupCtrl = PopupCtrl

if wx.VERSION_STRING < "2.8":
		if wx.VERSION_STRING < "2.7.2" and wx.VERSION_STRING > "2.7.0":
			import wx.aui as aui
		else:
			import PyAUI as aui
			aui.AUI_BUTTON_CUSTOM1 = aui.PaneInfo.buttonCustom1
			aui.AUI_BUTTON_CUSTOM2 = aui.PaneInfo.buttonCustom2
			aui.AUI_BUTTON_CUSTOM3 = aui.PaneInfo.buttonCustom3

		aui.AuiManager		= aui.FrameManager
		aui.AuiManagerEvent = aui.FrameManagerEvent
		aui.AuiPaneInfo		= aui.PaneInfo
		aui.AuiFloatingPane = aui.FloatingPane
else:
	import wx.aui as aui

wx.aui = aui
print "Using the following AUI", wx.aui
