
import wx
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
		try:
			if not isinstance(self, wx.core._wxPyDeadObject):
				wx.lib.mixins.listctrl.ListCtrlAutoWidthMixin._doResize(self)
		except wx.core.PyDeadObjectError:
			pass
	
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

wx.ListCtrl = wxListCtrl
wx.Choice = wxChoice
wx.ComboBox = wxComboBox

