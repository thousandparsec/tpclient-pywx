import os 
 
from wxPython.wx import * 
pygame = None
 
class wxSDLWindow(wxFrame): 
	def __init__(self, parent, id, title = 'SDL window', **options): 
		options['style'] = wxDEFAULT_FRAME_STYLE | wxTRANSPARENT_WINDOW 
		wxFrame.__init__(*(self, parent, id, title), **options) 

		self._surface = None

		EVT_IDLE(self, self.OnIdle) 

		if wxPlatform == "__WXGTK__":
			 EVT_WINDOW_CREATE(self, self.Created)
		else:
			 self.Created()

	def Created(self, evt):
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

		wxCallAfter(self.OnSize)
		 
	def OnIdle(self, ev): 
		self.draw() 
 
	def OnPaint(self, ev): 
		self.draw()
 
	def OnSize(self, ev=None): 
		x,y = self.GetSizeTuple() 
		self._surface = pygame.display.set_mode((x,y)) 

		if ev:
			ev.Skip() 
 
	def draw(self): 
		raise NotImplementedError('please define a .draw() method!') 
 
	def getSurface(self):
		return self._surface 
 
 
if __name__ == "__main__": 
 
	import time
 
 	ID_TIMER = 10123
	class CircleWindow(wxSDLWindow): 
		"draw a circle in a wxPython / PyGame window" 
		def __init__(self, parent, id, title = 'SDL window', **options):
			wxSDLWindow.__init__(*(self, parent, id, title), **options)

			self.topleft = [0,0]
			self.tick = time.time()
	
			self.timer = wxTimer(self, ID_TIMER)
			EVT_TIMER(self, ID_TIMER, self.OnMove)
			self.timer.Start(100)
	
		def draw(self):
			surface = self.getSurface() 
			if not surface is None: 
				topcolor = 5 
				bottomcolor = 100 
 
 				surface.fill((0,0,0))
				pygame.draw.circle(surface, (250,0,0), self.topleft, 50) 
				 
				pygame.display.flip()
				
		def OnMove(self, ev): 
			self.topleft[0] += 1
			self.topleft[1] += 1
			self.draw()
			
	def pygametest(): 
		app = wxPySimpleApp() 
		sizeT = (640,480) 
		w = CircleWindow(None, -1, size = sizeT) 
		w.Show(1) 
		app.MainLoop() 
 
	pygametest() 
