
from wxPython.wx import *

class winBase(wxFrame):
	def __init__(self, application, parent, 
			pos=wxDefaultPosition, 
			size=wxDefaultSize, 
			style=wxDEFAULT_FRAME_STYLE):
		wxFrame.__init__(self, parent, -1, 'TP: ' + self.title, pos, size, style)

		self.application = application
		self.parent = parent

		EVT_ACTIVATE(self, self.OnRaise)
		EVT_CLOSE(self, self.OnProgramExit)
		
	def OnProgramExit(self, evt):
		evt.Veto(true)

	def OnRaise(self, evt):
		if wxPlatform != '__WXMSW__':
			self.application.windows.raise_()
		
