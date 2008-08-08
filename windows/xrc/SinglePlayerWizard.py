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
		res.LoadOnObject(pre, parent, 'SinglePlayerWizard', 'wxWizard')
		self.PreCreate(pre)
		self.PostCreate(pre)

		# Define variables for the controls
		self.RulesetPage = XRCCTRL(self, "RulesetPage")
		self.Ruleset = XRCCTRL(self, "Ruleset")
		if hasattr(self, "OnRuleset"):
			self.Bind(wx.EVT_COMBOBOX, self.OnRuleset, self.Ruleset)
			self.Bind(wx.EVT_TEXT_ENTER, self.OnRuleset, self.Ruleset)
		if hasattr(self, "OnDirtyRuleset"):
			self.Bind(wx.EVT_TEXT, self.OnRuleset, self.Ruleset)

		self.RulesetDesc = XRCCTRL(self, "RulesetDesc")


def strings():
	pass
	_("TP: Single Player Game");
	_("Select Ruleset");
	_("Choose the ruleset for your game from the options below.");
	_("The ruleset to use.");
