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
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.PageDesc = XRCCTRL(self, "PageDesc")
		self.ProceedDesc = XRCCTRL(self, "ProceedDesc")
		self.DownloadLink = XRCCTRL(self, "DownloadLink")


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
		self.skip = False

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
		self.DownloadDesc = XRCCTRL(self, "DownloadDesc")
		self.DownloadLink = XRCCTRL(self, "DownloadLink")


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
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.PageDesc = XRCCTRL(self, "PageDesc")
		self.Server = XRCCTRL(self, "Server")
		if hasattr(self, "OnServer"):
			self.Bind(wx.EVT_COMBOBOX, self.OnServer, self.Server)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnServer, self.Server)
		if hasattr(self, "OnDirtyServer"):
			self.Bind(wx.EVT_TEXT, self.OnServer, self.Server)

		self.ServerDesc = XRCCTRL(self, "ServerDesc")
		self.ServerRulesetDesc = XRCCTRL(self, "ServerRulesetDesc")


class RulesetOptsPageBase(wx.wizard.PyWizardPage):
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
		res.LoadOnPanel(pre, parent, "RulesetOptsPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.PageDesc = XRCCTRL(self, "PageDesc")
		self.SizerRef = XRCCTRL(self, "SizerRef")


class ServerOptsPageBase(wx.wizard.PyWizardPage):
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
		res.LoadOnPanel(pre, parent, "ServerOptsPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.PageDesc = XRCCTRL(self, "PageDesc")
		self.SizerRef = XRCCTRL(self, "SizerRef")


class OpponentPageBase(wx.wizard.PyWizardPage):
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
		res.LoadOnPanel(pre, parent, "OpponentPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.AIListLabel = XRCCTRL(self, "AIListLabel")
		self.Opponents = XRCCTRL(self, "Opponents")
		self.AIClientLabel = XRCCTRL(self, "AIClientLabel")
		self.AIClient = XRCCTRL(self, "AIClient")
		if hasattr(self, "OnAIClient"):
			self.Bind(wx.EVT_COMBOBOX, self.OnAIClient, self.AIClient)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnAIClient, self.AIClient)
		if hasattr(self, "OnDirtyAIClient"):
			self.Bind(wx.EVT_TEXT, self.OnAIClient, self.AIClient)

		self.AIClientDesc = XRCCTRL(self, "AIClientDesc")
		self.AIUserLabel = XRCCTRL(self, "AIUserLabel")
		self.AIUser = XRCCTRL(self, "AIUser")
		self.AIOptionsLabel = XRCCTRL(self, "AIOptionsLabel")
		self.SizerRef = XRCCTRL(self, "SizerRef")
		self.New = XRCCTRL(self, "wxID_NEW")
		if hasattr(self, "OnNew"):
			self.Bind(wx.EVT_BUTTON, self.OnNew, self.New)

		self.Save = XRCCTRL(self, "wxID_SAVE")
		if hasattr(self, "OnSave"):
			self.Bind(wx.EVT_BUTTON, self.OnSave, self.Save)

		self.Delete = XRCCTRL(self, "wxID_DELETE")
		if hasattr(self, "OnDelete"):
			self.Bind(wx.EVT_BUTTON, self.OnDelete, self.Delete)

		self.BoxRef = XRCCTRL(self, "BoxRef")


class NoOpponentPageBase(wx.wizard.PyWizardPage):
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
		res.LoadOnPanel(pre, parent, "NoOpponentPage")
		self.PreCreate(pre)
		self.PostCreate(pre)

		self.parent = parent
		self.next = self.prev = None
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.PageDesc = XRCCTRL(self, "PageDesc")
		self.DownloadLink = XRCCTRL(self, "DownloadLink")


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
		self.skip = False

		self.SetAutoLayout(True)
		self.Fit()
		self.Hide()

		# Define variables for the controls
		self.PageDesc = XRCCTRL(self, "PageDesc")


def strings():
	pass
	_("TP: Single Player Game");
	_("Single Player Game");
	_("This wizard sets up a single player Thousand Parsec game using the servers, rulesets, and AI clients installed locally on your system.");
	_("Download Servers");
	_("Select Ruleset");
	_("Choose a ruleset for your game:");
	_("The ruleset to use.");
	_("Download Additional Servers/Rulesets");
	_("Select Server");
	_("The server to use.");
	_("Ruleset Options");
	_("Server Options");
	_("Opponents");
	_("This page lets you add AI opponents to your game.");
	_("Type");
	_("The AI client to use.");
	_("The AI description will go here.");
	_("Name");
	_("Options");
	_("&New");
	_("&Save");
	_("&Delete");
	_("New Opponent");
	_("No Opponents Found");
	_("Download AI Clients");
	_("Setup Complete");
