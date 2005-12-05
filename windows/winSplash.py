
import wx

class winSplash(wx.SplashScreen):
	def __init__(self, application):
		image = wx.Image("graphics/splash.png").ConvertToBitmap()
		wx.SplashScreen.__init__(self, image, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 2500, None, -1)

		self.application = application
		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
	
	def Post(self, evt):
		pass

	def OnClose(self, evt):
		if self.application.gui.current == self:
			self.application.gui.current = None
