# This file has been automatically generated.
# Please do not edit it manually.

# Python Imports
import os.path

# wxPython imports
import wx
from wx.xrc import XRCCTRL, XmlResourceWithHandlers

# Local imports
from requirements import location

class SinglePlayerWizardBase(wx.wizard.Wizard):
	xrc = os.path.join(location(), "windows", "xrc", 'SinglePlayerWizard.xrc')

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.wizard.PreWizard()
		res.LoadOnObject(pre, parent, "SinglePlayerWizard", 'wxWizard')
		self.PreCreate(pre)
		self.PostCreate(pre)

class StartPageBase(wx.wizard.PyWizardPage):
	xrc = os.path.join(location(), "windows", "xrc", 'SinglePlayerWizard.xrc')

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def SetNext(self, next):
		self.next = next
	
	def SetPrev(self, prev):
		self.prev = prev

	def GetNext(self):
		return self.next

	def GetPrev(self):
		return self.prev

	def validate(self):
		return True

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.wizard.PrePyWizardPage()
		res.LoadOnPanel(pre, parent, "StartPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.ProceedDesc = XRCCTRL(self, "ProceedDesc")


class RulesetPageBase(wx.wizard.PyWizardPage):
	xrc = os.path.join(location(), "windows", "xrc", 'SinglePlayerWizard.xrc')

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def SetNext(self, next):
		self.next = next
	
	def SetPrev(self, prev):
		self.prev = prev

	def GetNext(self):
		return self.next

	def GetPrev(self):
		return self.prev

	def validate(self):
		return True

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.wizard.PrePyWizardPage()
		res.LoadOnPanel(pre, parent, "RulesetPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.Ruleset = XRCCTRL(self, "Ruleset")
		if hasattr(self, "OnRuleset"):
			self.Bind(wx.EVT_COMBOBOX, self.OnRuleset, self.Ruleset)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnRuleset, self.Ruleset)
		if hasattr(self, "OnDirtyRuleset"):
			self.Bind(wx.EVT_TEXT, self.OnRuleset, self.Ruleset)

		self.RulesetDesc = XRCCTRL(self, "RulesetDesc")


class ServerPageBase(wx.wizard.PyWizardPage):
	xrc = os.path.join(location(), "windows", "xrc", 'SinglePlayerWizard.xrc')

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def SetNext(self, next):
		self.next = next
	
	def SetPrev(self, prev):
		self.prev = prev

	def GetNext(self):
		return self.next

	def GetPrev(self):
		return self.prev

	def validate(self):
		return True

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.wizard.PrePyWizardPage()
		res.LoadOnPanel(pre, parent, "ServerPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.Server = XRCCTRL(self, "Server")
		if hasattr(self, "OnServer"):
			self.Bind(wx.EVT_COMBOBOX, self.OnServer, self.Server)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnServer, self.Server)
		if hasattr(self, "OnDirtyServer"):
			self.Bind(wx.EVT_TEXT, self.OnServer, self.Server)

		self.ServerDesc = XRCCTRL(self, "ServerDesc")


class EndPageBase(wx.wizard.PyWizardPage):
	xrc = os.path.join(location(), "windows", "xrc", 'SinglePlayerWizard.xrc')

	def PreCreate(self, pre):
		""" This function is called during the class's initialization.
		
		Override it for custom setup before the window is created usually to
		set additional window styles using SetWindowStyle() and SetExtraStyle()."""
		pass

	def SetNext(self, next):
		self.next = next
	
	def SetPrev(self, prev):
		self.prev = prev

	def GetNext(self):
		return self.next

	def GetPrev(self):
		return self.prev

	def validate(self):
		return True

	def __init__(self, parent, *args, **kw):
		""" Pass an initialized wx.xrc.XmlResource into res """
		f = os.path.join(os.path.dirname(__file__), self.xrc)
		res = XmlResourceWithHandlers(f)		

		# Two stage creation (see http://wiki.wxpython.org/index.cgi/TwoStageCreation)
		pre = wx.wizard.PrePyWizardPage()
		res.LoadOnPanel(pre, parent, "EndPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls


def strings():
	pass
	_("TP: Single Player Game");
	_("Single Player Game");
	_("This wizard sets up a single player Thousand Parsec \ngame using the servers, rulesets, and AI clients \ninstalled locally on your system.");
	_("Select Ruleset");
	_("Choose a ruleset for your game:");
	_("The ruleset to use.");
	_("Select Server");
	_("Multiple servers implement the ruleset you selected. Please select a server to use:");
	_("The server to use.");
	_("Setup Complete");
	_("The Thousand Parsec client will now connect to your \nlocal single player game.");
