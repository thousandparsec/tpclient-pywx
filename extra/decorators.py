
from tp.client.decorator import decorator

@decorator
def freeze_wrapper(func, self, *args, **kw):
	try:
		try:
			print "Freezing", self
			self.Freeze()
		except AttributeError:
			raise Warning("FreezeWrapper on %r but no Freeze method! (%s)" % (self, e))
	
		func(self, *args, **kw)

	finally:
		try:
			print "Thawing", self
			self.Thaw()
		except AttributeError, e:
			raise Warning("FreezeWrapper on %r but no Thaw method! (%s)" % (self, e))

