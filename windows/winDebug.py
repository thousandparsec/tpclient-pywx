
import wx
from wx import py

from winBase import winMainBase

class winDebug(winMainBase):
	title = _("Debug")
	
	def __init__(self, application):
		winMainBase.__init__(self, application)

		py.crust.Crust(self, locals=locals(), rootObject=application, rootLabel="Application")

