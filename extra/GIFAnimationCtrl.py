
import wx

try: 
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
		def __init__(self, parent, id, *args, **kw):
			wx.Panel.__init__(self, parent, id, *args, **kw)
			self.bitmap = None
			self.background = None

			self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnErase)
			self.Bind(wx.EVT_PAINT, self.OnPaint)

		def display(self, image):
			if wx.Platform == '__WXMSW__' and self.IsShown():
				if self.background is None:
					dc = wx.ClientDC(self)
					dc.Clear()
					color = dc.GetPixel(0, 0)
					self.background = (wx.Pen(wx.Color(*color)), wx.Brush(wx.Color(*color)))

				bitmap = image.ConvertToBitmap()
				self.bitmap = wx.EmptyBitmap(*self.GetSize())
				dc = wx.MemoryDC(self.bitmap)
				dc.SetPen(self.background[0])
				dc.SetBrush(self.background[1])

				dc.DrawRectangle(0, 0, *self.GetSize())
				dc.DrawBitmap(bitmap, 0,0)
			else:
				self.bitmap = image.ConvertToBimap() 
			self.Refresh(True)

		def OnPaint(self, evt):
			dc = wx.PaintDC(self)
			if self.bitmap:
				dc.DrawBitmap(self.bitmap, 0,0)

		def OnErase(self, evt):
			return True

	class GIFAnimationCtrl(ImagePanel):
		def __init__(self, parent, id=-1, file="", *args, **kw):
			ImagePanel.__init__(self, parent, id, *args, **kw)
			self.timer = wx.Timer(self, -1)
		
			self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)

		def Play(self):
			#print "Starting Animation"
			self.timer.Start(self.delay)

		def Stop(self):
			#print "Stoping Animation"
			self.timer.Stop()

		def LoadFile(self, file):

			#print "Loading File", file
			self.gif = Image.open(file)
			if not self.gif.info.has_key('duration') or self.gif.info['duration'] == 0:
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
except ImportError, e:
	from wx.animate import GIFAnimationCtrl
	print e

import wx.xrc as xrc
class GIFAnimationCtrlXmlHandler(xrc.XmlResourceHandler):
	def __init__(self):
		xrc.XmlResourceHandler.__init__(self)
		# Specify the styles recognized by objects of this type
		self.AddWindowStyles()

	# This method and the next one are required for XmlResourceHandlers
	def CanHandle(self, node):
		return self.IsOfClass(node, "wxGIFAnimationCtrl") or self.IsOfClass(node, "GIFAnimationCtrl")

	def DoCreateResource(self):
		# The simple method assumes that there is no existing
		# instance.  Be sure of that with an assert.
		assert self.GetInstance() is None

		ctrl = GIFAnimationCtrl(self.GetParentAsWindow(),
								self.GetID(),
								"",
								self.GetPosition(),
								self.GetSize(),
								self.GetStyle(),
								self.GetName(),
								)

		# These two things should be done in either case:
		# Set standard window attributes
		self.SetupWindow(ctrl)
		# Create any child windows of this node
		self.CreateChildren(ctrl)

		return ctrl
xrc.ExtraHandlers.append(GIFAnimationCtrlXmlHandler)

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
