
import wx
from wx.lib.popupctl import *

# Tried to use wxPopupWindow but the control misbehaves on MSW
class PopupDialog(wx.Dialog):
	def __init__(self,parent,content = None):
		wx.Dialog.__init__(self,parent,-1,'', style = wx.BORDER_SIMPLE|wx.STAY_ON_TOP)

		self.ctrl = parent
		self.win = wx.Window(self,-1,pos = (0,0),style = 0)

		if content:
			self.SetContent(content)

	def SetContent(self,content):
		self.content = content
		self.content.Reparent(self.win)
		self.content.Show(True)

	def Display(self):
		self.ctrl.FormatContent()
		self.win.SetClientSize(self.content.GetSize())
		self.SetSize(self.win.GetSize())

		pos = self.ctrl.ClientToScreen( (0,0) )
		dSize = wx.GetDisplaySize()
		selfSize = self.GetSize()
		tcSize = self.ctrl.GetSize()

		print pos, dSize, selfSize, tcSize

		pos.x -= (selfSize.width - tcSize.width) / 2
		if pos.x + selfSize.width > dSize.width:
			pos.x = dSize.width - selfSize.width
		if pos.x < 0:
			pos.x = 0

		pos.y += tcSize.height
		if pos.y + selfSize.height > dSize.height:
			pos.y = dSize.height - selfSize.height
		if pos.y < 0:
			pos.y = 0

		print pos

		self.Move(pos)
		self.ShowModal()

class PopupCtrl(wx.PyControl):
	def __init__(self, *args, **kwargs):
		wx.PyControl.__init__(self, *args, **kwargs)

		self.control = None
		self.content = None
		self.pop = None

		self.Bind(wx.EVT_SIZE, self.OnSize)

	def OnSize(self, evt):
		if not self.control is None:
			self.control.SetSize(self.GetClientSize())

	def SetPopupCtrl(self, control):
		self.control = control
		self.control.Reparent(self)

		self.OnSize(None)

		self.control.Bind(wx.EVT_LEFT_UP, self.OnButton)

	def SetPopupContent(self,content):
		if not self.pop:
			self.content = content
			self.content.Show(False)
		else:
			self.pop.SetContent(content)

	def OnButton(self,evt):
		print self, "OnButton"
		self.PopUp()

	def FormatContent(self):
		pass

	def PopUp(self):
		if not self.pop:
			if self.content:
				self.pop = PopupDialog(self,self.content)
				del self.content
			else:
				print 'No Content to pop'
		if self.pop:
			self.pop.Display()

	def PopDown(self):
		if self.pop:
			self.pop.EndModal(True)

	def Enable(self,flag):
		wx.PyControl.Enable(self,flag)
		self.control.Enable(flag)

	def __getattr__(self, value):
		if hasattr(self.control, value):
			return getattr(self.control, value)
		raise AttributeError("No such attribute " + value)

