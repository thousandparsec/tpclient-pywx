"""\
This module contains the "base" for all main windows. It does things
like prepending "TP:" to the title, vetoing closing of the window
and raising all the other windows when one is clicked.
"""

from wxPython.wx import *

from extra.wxPostEvent import *

class winRealBase:
	def __init__(self, application, parent, 
			pos=wxDefaultPosition, 
			size=wxDefaultSize, 
			style=wxDEFAULT_FRAME_STYLE):
		wxHandler(self)

		self.application = application
		self.parent = parent

		EVT_ACTIVATE(self, self.OnRaise)
		EVT_CLOSE(self, self.OnProgramExit)
		
	def OnProgramExit(self, evt):
		evt.Veto(true)

	def OnRaise(self, evt):
		if wxPlatform != '__WXMSW__':
			if self.application.windows.config.raise_ == "All on All":
				self.application.windows.Raise()
			elif self.application.windows.config.raise_ == "All on Main":
				if self.title == "Thousand Parsec":
					self.application.windows.Raise()
			elif self.application.windows.config.raise_ == "Individual":
				pass
			else:
				print "Unknown raise method:", self.application.windows.config.raise_

class winMainBase(wxMDIParentFrame, winRealBase):
	def __init__(self, application, parent, 
			pos=wxDefaultPosition, 
			size=wxDefaultSize, 
			style=wxDEFAULT_FRAME_STYLE):
		wxMDIParentFrame.__init__(self, None, -1, 'TP: ' + self.title, pos, size, style)
		winRealBase.__init__(self, application, parent, pos, size, style)

class winNormalBase(wxFrame, winRealBase):
	def __init__(self, application, parent, 
			pos=wxDefaultPosition, 
			size=wxDefaultSize, 
			style=wxDEFAULT_FRAME_STYLE):
		wxFrame.__init__(self, parent, -1, 'TP: ' + self.title, pos, size, style)
		winRealBase.__init__(self, application, parent, pos, size, style)
    
class winSubBase(wxMDIChildFrame, winRealBase):
	def __init__(self, application, parent, 
			pos=wxDefaultPosition, 
			size=wxDefaultSize, 
			style=wxDEFAULT_FRAME_STYLE):
		wxMDIChildFrame.__init__(self, parent, -1, 'TP: ' + self.title, pos, size, style)
		winRealBase.__init__(self, application, parent, pos, size, style)

if wxPlatform == '__WXMSW__':
	winBase = winSubBase
else:
	winMainBase = winNormalBase
	winBase = winNormalBase