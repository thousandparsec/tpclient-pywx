
from tp.client.decorator import decorator

@decorator
def freeze_wrapper(func, self, *args, **kw):
	"""
	This decorator calls Freeze before calling the function, and then thaw after.
	"""
	frozen = False
	try:
		if hasattr(self, "Freeze"):
			frozen = True
			self.Freeze()
	
		return func(self, *args, **kw)

	finally:
		if frozen:
			self.Thaw()

import wx

@decorator
def onlyshown(func, self, evt, *args, **kw):
	"""
	This decorator prevents a callback being called unless the window that it
	is on is shown.  
	"""
	if not self.IsShown():
		print "WARNING: %s called when %s was not shown!" % (func, self)

		# FIXME: Hack for Mac OS X's crap
		if isinstance(evt, wx.Event):
			if hasattr(self, "application"):
				self.application.gui.current.AddPendingEvent(evt)
		return
	return func(self, evt, *args, **kw)

def onlyenabled(attribute):
	"""
	This decorator prevents a callback being called unless the given wxWindow
	is enabled.  
	"""
	@decorator
	def onlyenabled_decorator(func, self, *args, **kw):
		"""
		This decorator prevents a callback being called unless the given
		wxWindow is enabled.  
		"""
		try:
			tocheck = getattr(self, attribute)
			if not tocheck.IsEnabled():
				print "WARNING: %s called when %s on %s was not enabled!" % (func, tocheck, self)
				return
		except AttributeError, e:
			print "ERROR: Was unable to check enable state of %s when calling %s (%s)" % (attribute, func, e)

		return func(self, *args, **kw)
	return onlyenabled_decorator
