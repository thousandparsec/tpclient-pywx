
import wx
import Image
import Image
import PngImagePlugin
import GifImagePlugin
import JpegImagePlugin
Image._initialized=2


def pil2wx(pil,alpha=True):
	if alpha:
		image = wx.EmptyImage(*pil.size)
		image.SetData( pil.convert( "RGB").tostring() )
		image.SetAlphaData(pil.convert("RGBA").tostring()[3::4])
	else:
		image = wx.EmptyImage(*pil.size)
		image.SetData( pil.convert( "RGB").tostring() )
	return image

class ImagePanel(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, id)
		self.image = None
		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def display(self, image):
		self.image = image
		self.Refresh(True)

	def OnPaint(self, evt):
		dc = wx.PaintDC(self)
		if self.image:
			dc.DrawBitmap(self.image.ConvertToBitmap(), 0,0)

class GIFAnimationCtrl(ImagePanel):
	def __init__(self, parent, id=-1):
		ImagePanel.__init__(self, parent, id)
		self.timer = wx.Timer(self, -1)
	
		self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

	def Play(self):
		print "Starting Animation"
		self.timer.Start(self.delay)

	def Stop(self):
		print "Stoping Animation"
		self.timer.Stop()

	def LoadFile(self, file):

		print "Loading File", file
		self.gif = Image.open(file)
		if self.gif.info['duration'] == 0:
			self.delay = 100
		else:
			self.delay = self.gif.info['duration']
		self.frames = []	# Frame Cache
		self.alldone = False	# Have we cached all the frames?
		self.current = 0
		
		self.SetSize(wx.Size(*self.gif.size))

	def OnTimer(self, evt):
		self.display(self.NextFrame())

	def NextFrame(self):
		if not self.alldone:
			try:
				self.gif.seek(len(self.frames))
				self.frames.append(pil2wx(self.gif, True))
			except EOFError:
				# No more frames left
				self.alldone = True
		
		i = self.frames[self.current % len(self.frames)]
		self.current += 1 
		return i

if __name__ == "__main__":
	a = wx.App()

	class Frame(wx.Frame):
		def __init__(self, parent, id, title):
			wx.Frame.__init__(self, None, id, title, wx.DefaultPosition, wx.Size(500, 400))

			self.panel = GIFAnimationCtrl(self, -1)
			self.panel.LoadFile("barren1.gif")
			self.panel.Play()

	f = Frame(a, -1, "Testing")
	f.Show()
	a.MainLoop()
