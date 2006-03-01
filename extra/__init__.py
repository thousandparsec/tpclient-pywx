
import string
import wx
import wx.gizmos
import wx.lib.mixins.listctrl

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

wx.ListCtrlOrig = wx.ListCtrl
class wxListCtrl(wx.ListCtrlOrig, wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin, ToolTipItemMixIn):
	def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
		wx.ListCtrlOrig.__init__(self, parent, ID, pos, size, style)
		wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin.__init__(self)
		ToolTipItemMixIn.__init__(self)

		self.objects = []
		self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

	def InsertItem(self, item):
		self._increasePyData(slot)
		wx.ListCtrlOrig.InsertItem(self, item)
		
	def InsertStringItem(self, slot, label):
		self._increasePyData(slot)
		wx.ListCtrlOrig.InsertStringItem(self, slot, label)
		
	def InsertImageItem(self, slot, imageIndex):
		self._increasePyData(slot)
		wx.ListCtrlOrig.InsertImageItem(self, slot, imageIndex)
		
	def InsertImageStringItem(self, slot, label, imageIndex):
		self._increasePyData(slot)
		wx.ListCtrlOrig.InsertImageStringItem(self, slot, label, imageIndex)

	def _increasePyData(self, slot):
		self.objects.insert(slot, None)

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

	def OnMouseMotion(self, evt):
		slot = self.HitTest(evt.GetPosition())[0]
		self.SetToolTipCurrent(slot)

	def _doResize(self):
		if hasattr(wx, 'core'):
			try:
				if not isinstance(self, wx.core._wxPyDeadObject):
					wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin._doResize(self)
			except wx.core.PyDeadObjectError:
				pass
		else:
			wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin._doResize(self)
	
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

	def FindItemByData(self, pyData, item=None, compare=None):
		if item == None:
			item = self.GetRootItem()

		if compare is None and self.GetPyData(item) == pyData:
			return item
		elif compare(self.GetPyData(item), pyData):
			return item
		else:
			if self.ItemHasChildren(item):
				cookieo = -1
				child, cookie = self.GetFirstChild(item)

				while cookieo != cookie:
					r = self.FindItemByData(pyData, child)
					if r:
						return r
					
					cookieo = cookie
					child, cookie = self.GetNextChild(item, cookie)

		return None

wx.OrderedTreeCtrl = OrderedTreeCtrl

wx.gizmos.TreeListCtrlOrig = wx.gizmos.TreeListCtrl
class wxTreeListCtrl(wx.gizmos.TreeListCtrlOrig):
	"""\
	Modified object which includes the ability to get an object by the pyData
	"""
	def FindItemByData(self, pyData, item=None, compare=None):
		if item == None:
			item = self.GetRootItem()

		if compare is None and self.GetPyData(item) == pyData:
			return item
		elif compare(self.GetPyData(item), pyData):
			return item
		else:
			if self.ItemHasChildren(item):
				cookieo = -1
				child, cookie = self.GetFirstChild(item)

				while cookieo != cookie:
					r = self.FindItemByData(pyData, child)
					if r:
						return r
					
					cookieo = cookie
					child, cookie = self.GetNextChild(item, cookie)

		return None

	def GetPyData(self, item):
		try:
			return wx.gizmos.TreeListCtrlOrig.GetPyData(self, item)
		except:
			return None

	def CollapseAll(self, item=None):
		if item == None:
			item = self.GetRootItem()

		if self.ItemHasChildren(item):
			cookieo = -1
			child, cookie = self.GetFirstChild(item)

			while cookieo != cookie:
				self.CollapseAll(child)
			
				cookieo = cookie
				child, cookie = self.GetNextChild(item, cookie)

		self.Collapse(item)

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
wx.gizmos.TreeListCtrl = wxTreeListCtrl
wx.SimpleValidator = wxSimpleValidator
