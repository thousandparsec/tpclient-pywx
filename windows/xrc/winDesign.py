# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

class winDesignBase:
	xrc = 'winDesign.xrc'

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Figure out what Frame class (MDI, MiniFrame, etc) is actually our base...
		bases = set()
		def findbases(klass, set):
			for base in klass.__bases__:
				set.add(base)
				findbases(base, set)
		findbases(self.__class__, bases)

		for base in bases:
			if base.__name__.endswith("Frame"):
				break
		
		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = getattr(wx, "Pre%s" % base.__name__)()
		res.LoadOnFrame(pre, parent, "winDesign")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.panel = XRCCTRL(self, "panel")
		self.gridpanel = XRCCTRL(self, "gridpanel")
		self.toppanel = XRCCTRL(self, "toppanel")
		self.titleedit = XRCCTRL(self, "titleedit")
		self.titletext = XRCCTRL(self, "titletext")
		self.used = XRCCTRL(self, "used")
		self.designs = XRCCTRL(self, "designs")
		self.middlepanel = XRCCTRL(self, "middlepanel")
		self.categories = XRCCTRL(self, "categories")
		self.designsizerpanel = XRCCTRL(self, "designsizerpanel")
		self.parts = XRCCTRL(self, "parts")
		self.design_pp = XRCCTRL(self, "design_pp")
		self.design_pspanel = XRCCTRL(self, "design_pspanel")
		self.properties = XRCCTRL(self, "properties")
		self.sizerpanel = XRCCTRL(self, "sizerpanel")
		self.box_sizerpanel = XRCCTRL(self, "box_sizerpanel")
		self.prop_sizerpanel = XRCCTRL(self, "prop_sizerpanel")
		self.buttonspanel = XRCCTRL(self, "buttonspanel")
		self.edit = XRCCTRL(self, "edit")
		if hasattr(self, "Onedit"):
			self.Bind(wx.EVT_BUTTON, self.Onedit, self.edit)

		self.duplicate = XRCCTRL(self, "duplicate")
		if hasattr(self, "Onduplicate"):
			self.Bind(wx.EVT_BUTTON, self.Onduplicate, self.duplicate)

		self.delete = XRCCTRL(self, "delete")
		if hasattr(self, "Ondelete"):
			self.Bind(wx.EVT_BUTTON, self.Ondelete, self.delete)

		self.revert = XRCCTRL(self, "revert")
		if hasattr(self, "Onrevert"):
			self.Bind(wx.EVT_BUTTON, self.Onrevert, self.revert)

		self.save = XRCCTRL(self, "save")
		if hasattr(self, "Onsave"):
			self.Bind(wx.EVT_BUTTON, self.Onsave, self.save)

		self.compssizerpanel = XRCCTRL(self, "compssizerpanel")
		self.comps = XRCCTRL(self, "comps")
		self.addsizerpanel = XRCCTRL(self, "addsizerpanel")
		self.add = XRCCTRL(self, "add")
		if hasattr(self, "Onadd"):
			self.Bind(wx.EVT_BUTTON, self.Onadd, self.add)

		self.addmany = XRCCTRL(self, "addmany")
		if hasattr(self, "Onaddmany"):
			self.Bind(wx.EVT_BUTTON, self.Onaddmany, self.addmany)



def strings():
	_("Design");
	_("Title");
	_("Title");
	_("0000");
	_("Edit");
	_("Duplicate");
	_("Delete");
	_("Revert");
	_("Save");
	_("Add");
	_("Add Many");
