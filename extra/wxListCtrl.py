
from wxPython.wx import wxListCtrl as _wxListCtrl
from wxPython.lib.mixins.listctrl import wxListCtrlAutoWidthMixin

import random

class wxListCtrl(_wxListCtrl, wxListCtrlAutoWidthMixin):
	def __init__(self,*_args,**_kwargs):
		self.data = {}
		self.generator = random.Random()
		
		apply(_wxListCtrl.__init__,(self,) + _args, _kwargs)
		wxListCtrlAutoWidthMixin.__init__(self)
	
	def GetRandom(self):
		return int(self.generator.random()*100000000)
	
	def SetItemData(self, index, data):
		# Generate a random number
		no = self.GetRandom()
		while (self.data.has_key(no)):
			no = self.GetRandom()

		# Store the data
		self.data[no] = data

		# Put the long into the control
		val = _wxListCtrl.SetItemData(self, index, no)
		return val
	
	def GetItemData(self, index):
		# Get the random number
		no = _wxListCtrl.GetItemData(self, index)
		if no:
			return self.data[no]
		else:
			return None

	def DeleteItem(self, index):
		no = _wxListCtrl.GetItemData(self, index)
		if no:
			del self.data[no]

		val = _wxListCtrl.DeleteItem(self, index)
		return val

	def DeleteAllItems(self, *_args, **_kwargs):
		self.data.clear()
		val = apply(_wxListCtrl.DeleteAllItems,(self,) + _args, _kwargs)
		return val
		
	def ClearAll(self, *_args, **_kwargs):
		self.data.clear()
		val = apply(_wxListCtrl.ClearAll,(self,) + _args, _kwargs)
		return val
		
	def FindItemData(self, *_args, **_kwargs):
		no = apply(_wxListCtrl.FindItemData,(self,) + _args, _kwargs)
		if no:
			return self.data[no]
		else:
			return None
		
	def InsertItem(self, *_args, **_kwargs):
		val = apply(_wxListCtrl.InsertItem,(self,) + _args, _kwargs)
		return val
	def GetItem(self, *_args, **_kwargs):
		val = apply(_wxListCtrl.GetItem,(self,) + _args, _kwargs)
		return val
	def SetItem(self, *_args, **_kwargs):
		val = apply(_wxListCtrl.SetItem,(self,) + _args, _kwargs)
		return val
