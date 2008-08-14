# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class winDesignBase:
	"""\
Unlike a normal XRC generated class, this is a not a full class but a MixIn.
Any class which uses this as a base must also inherit from a proper wx object
such as the wx.Frame class.

This is so that a the same XRC can be used for both MDI and non-MDI frames.
"""

	xrc = os.path.join(location(), "windows", "xrc", 'winDesign.xrc')

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
		if not res.LoadOnFrame(pre, parent, "winDesign"):
			raise IOError("Did not find the winDesign in the XRC file")
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.Panel = XRCCTRL(self, "Panel")
		self.DesignsSearch = XRCCTRL(self, "DesignsSearch")
		self.TitlePanel = XRCCTRL(self, "TitlePanel")
		self.TitleStatic = XRCCTRL(self, "TitleStatic")
		self.TitleEditable = XRCCTRL(self, "TitleEditable")
		self.Used = XRCCTRL(self, "Used")
		self.ComponentsSearch = XRCCTRL(self, "ComponentsSearch")
		self.DesignsPanel = XRCCTRL(self, "DesignsPanel")
		self.DesignsTree = XRCCTRL(self, "DesignsTree")
		self.DesignPanel = XRCCTRL(self, "DesignPanel")
		self.Categories = XRCCTRL(self, "Categories")
		self.DesignInfoPanel = XRCCTRL(self, "DesignInfoPanel")
		self.PartsList = XRCCTRL(self, "PartsList")
		self.DesignProperties = XRCCTRL(self, "DesignProperties")
		self.DesignPropertyGroup1 = XRCCTRL(self, "DesignPropertyGroup1")
		self.DesignButtonsPanel = XRCCTRL(self, "DesignButtonsPanel")
		self.Edit = XRCCTRL(self, "Edit")
		if hasattr(self, "OnEdit"):
			self.Bind(wx.EVT_BUTTON, self.OnEdit, self.Edit)

		self.Duplicate = XRCCTRL(self, "Duplicate")
		if hasattr(self, "OnDuplicate"):
			self.Bind(wx.EVT_BUTTON, self.OnDuplicate, self.Duplicate)

		self.Delete = XRCCTRL(self, "Delete")
		if hasattr(self, "OnDelete"):
			self.Bind(wx.EVT_BUTTON, self.OnDelete, self.Delete)

		self.Revert = XRCCTRL(self, "Revert")
		if hasattr(self, "OnRevert"):
			self.Bind(wx.EVT_BUTTON, self.OnRevert, self.Revert)

		self.Save = XRCCTRL(self, "Save")
		if hasattr(self, "OnSave"):
			self.Bind(wx.EVT_BUTTON, self.OnSave, self.Save)

		self.ComponentsPanel = XRCCTRL(self, "ComponentsPanel")
		self.ComponentsTree = XRCCTRL(self, "ComponentsTree")
		self.ComponentsButtonPanel = XRCCTRL(self, "ComponentsButtonPanel")
		self.ComponentsAdd = XRCCTRL(self, "ComponentsAdd")
		if hasattr(self, "OnComponentsAdd"):
			self.Bind(wx.EVT_BUTTON, self.OnComponentsAdd, self.ComponentsAdd)

		self.ComponentsAddMany = XRCCTRL(self, "ComponentsAddMany")
		if hasattr(self, "OnComponentsAddMany"):
			self.Bind(wx.EVT_BUTTON, self.OnComponentsAddMany, self.ComponentsAddMany)



def strings():
	pass
	_("Design");
	_("Title");
	_("Title");
	_("0000");
	_("Some Categories, Will Go, Here");
	_("Property 1:");
	_("The value of property 1");
	_("Property 2:");
	_("The value of property 2");
	_("Edit");
	_("Duplicate");
	_("Delete");
	_("Revert");
	_("Save");
	_("Add");
	_("Add Many");
