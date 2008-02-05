
import os
from requirements import graphicsdir

try:

	if os.path.exists("NOSPLASHMOVIE"):
		raise ImportError('Splash movie disabled...')

	import time

	os.environ['SDL_VIDEO_CENTERED'] = '1'
	os.environ['SDL_VIDEO_WINDOW_POS'] = "center"
	import pygame

	if not os.path.exists(os.path.join(graphicsdir, "intro-high.mpg")):
		print "Could not find the intro movie", os.path.join(graphicsdir, "intro-high.mpg")
		raise ImportError

	class winSplash(object):
		def __init__(self, application):
			pass

		def Show(self, *args, **kw):
			pygame.init()
			screen = pygame.display.set_mode((640,480), pygame.NOFRAME)
			pygame.mixer.quit()

			self.movie = pygame.movie.Movie(os.path.join(graphicsdir, "intro-high.mpg"))
			self.movie.set_display(screen, (0,0), )
			self.movie.play()
			pygame.display.flip()

		def Hide(self, *args, **kw):
			print "Entered splash hide!"
			while True:
				if not self.movie.get_busy():
					break

				event = pygame.event.poll()
				if event.type == pygame.NOEVENT:
					time.sleep(0.1)
				elif event.type in (pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN, pygame.KEYUP):
					break

			while self.movie.get_busy():
				self.movie.stop()

			pygame.quit()

		def Post(self, evt):
			pass

except ImportError:
	import wx

	class winSplash(wx.SplashScreen):
		def __init__(self, application):
			image = wx.Image(os.path.join(graphicsdir, "splash.png")).ConvertToBitmap()
			wx.SplashScreen.__init__(self, image, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 2500, None, -1)

			self.application = application
		
		def Post(self, evt):
			pass


