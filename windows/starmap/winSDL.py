import os 
 
from wxPython.wx import * 
pygame = None

class wxSDLMixin:
	def __init__(self):
		self.__init = 0
		self._surface = None

		EVT_IDLE(self, self.OnIdle) 

		if wxPlatform == "__WXGTK__":
			 EVT_WINDOW_CREATE(self, self.Created)
		else:
			 self.Created()

	def Created(self, evt):
		if not self.__init:
			# get the handle
			print "created"
			hwnd = self.GetHandle() 
		
			os.environ['SDL_WINDOWID'] = str(hwnd) 
			if sys.platform == 'win32': 
				os.environ['SDL_VIDEODRIVER'] = 'windib' 

			global pygame
			import pygame as _pygame
			pygame = _pygame
			pygame.init()
			pygame.display.init()
	
			EVT_SIZE(self, self.OnSize)

			self.__init = 1

			wxCallAfter(self.OnSize)
		 
	def OnIdle(self, ev): 
		self.Draw() 
 
	def OnPaint(self, ev): 
		self.Draw()
 
	def OnSize(self, ev=None): 
		if self.__init:
			x,y = self.GetSizeTuple() 
			self._surface = pygame.display.set_mode((x,y)) 

			if ev:
				ev.Skip() 
 
	def Draw(self): 
		raise NotImplementedError('please define a .Draw() method!') 
 
	def GetSurface(self):
		return self._surface 

class wxSDLWindow(wxSDLMixin, wxFrame): 
	def __init__(self, parent, id, title = 'SDL window', **options): 
		options['style'] = wxDEFAULT_FRAME_STYLE | wxTRANSPARENT_WINDOW 
		wxFrame.__init__(*(self, parent, id, title), **options) 
		
		wxSDLMixin.__init__(self)

class wxSDLScrolledWindow(wxScrolledWindow, wxSDLMixin): 
	def __init__(self, parent, id, **options): 
		options['style'] = wxDEFAULT_FRAME_STYLE | wxTRANSPARENT_WINDOW 
		wxScrolledWindow.__init__(*(self, parent, id), **options) 

		wxSDLMixin.__init__(self)

class wxSDLPanel(wxSDLMixin, wxPanel):
	def __init__(self, parent, id, **options): 
		options['style'] = wxDEFAULT_FRAME_STYLE | wxTRANSPARENT_WINDOW 
		wxPanel.__init__(*(self, parent, id), **options) 

		wxSDLMixin.__init__(self)



class CustomStatusBar(wxStatusBar):
	def __init__(self, parent):
		wxStatusBar.__init__(self, parent, -1)
		self.SetFieldsCount(3)
		self.sizeChanged = false
		EVT_SIZE(self, self.OnSize)
		EVT_IDLE(self, self.OnIdle)

		self.SetStatusText("A Custom StatusBar...", 0)

		self.cb = wxCheckBox(self, 1001, "toggle clock")
		EVT_CHECKBOX(self, 1001, self.OnToggleClock)
		self.cb.SetValue(true)

		# set the initial position of the checkbox
		self.Reposition()

		# start our timer
		self.timer = wxPyTimer(self.Notify)
		self.timer.Start(1000)
		self.Notify()

	# Time-out handler
	def Notify(self):
		t = time.localtime(time.time())
		st = time.strftime("%d-%b-%Y   %I:%M:%S", t)
		self.SetStatusText(st, 2)

	# the checkbox was clicked
	def OnToggleClock(self, event):
		if self.cb.GetValue():
			self.timer.Start(1000)
			self.Notify()
		else:
			self.timer.Stop()

	def OnSize(self, evt):
		self.Reposition()  # for normal size events

		# Set a flag so the idle time handler will also do the repositioning.
		# It is done this way to get around a buglet where GetFieldRect is not
		# accurate during the EVT_SIZE resulting from a frame maximize.
		self.sizeChanged = true

	def OnIdle(self, evt):
		if self.sizeChanged:
			self.Reposition()

	# reposition the checkbox
	def Reposition(self):
		rect = self.GetFieldRect(1)
		self.cb.SetPosition(wxPoint(rect.x+2, rect.y+2))
		self.cb.SetSize(wxSize(rect.width-4, rect.height-4))
		self.sizeChanged = false

if __name__ == "__main__": 
 
	import time
 
 	ID_TIMER = 10123

	class CircleWindow(wxSDLScrolledWindow): 
		"draw a circle in a wxPython / PyGame window" 
		def __init__(self, parent, id, title = 'SDL window', **options):
			wxSDLScrolledWindow.__init__(*(self, parent, id), **options)
			
			self.SetScrollbars(20, 20, 50, 50)
			self.EnableScrolling(0,0)

			self.topleft = [0,0]
			self.tick = time.time()
	
			self.timer = wxTimer(self, ID_TIMER)
			EVT_TIMER(self, ID_TIMER, self.OnMove)
			self.timer.Start(100)

		def Draw(self):
			surface = self.GetSurface() 
			if not surface is None: 
				topcolor = 5 
				bottomcolor = 100 
 
 				surface.fill((0,0,0))
				pygame.draw.circle(surface, (250,0,0), self.topleft, 50) 
				 
				pygame.display.flip()
				
		def OnMove(self, ev): 
			self.topleft[0] += 1
			self.topleft[1] += 1
			self.Draw()

	class MyFrame(wxFrame):
		def __init__(self, parent, ID, title, pos=wxDefaultPosition,
						size=wxDefaultSize, style=wxDEFAULT_FRAME_STYLE):
			wxFrame.__init__(self, parent, ID, title, pos, size, style)
			panel = CircleWindow(self, -1)
			
			self.sb = CustomStatusBar(self)
			self.SetStatusBar(self.sb)

			tb = self.CreateToolBar(wxTB_HORIZONTAL|wxNO_BORDER|wxTB_FLAT|wxTB_TEXT)

	def pygametest(): 
		app = wxPySimpleApp() 
		sizeT = (640,480) 
		#w = CircleWindow(None, -1, size = sizeT) 
		w = MyFrame(None, -1, 'Testing', size = sizeT) 
		w.Show(1) 
		app.MainLoop() 
 
	pygametest() 
