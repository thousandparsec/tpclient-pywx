
from tp.client.decorator import decorator

@decorator
def freeze_wrapper(func, self, *args, **kw):
	try:
		try:
			self.Freeze()
		except AttributeError:
			raise Warning("FreezeWrapper on %r but no Freeze method! (%s)" % (self, e))
	
		func(self, *args, **kw)

	finally:
		try:
			self.Thaw()
		except AttributeError, e:
			raise Warning("FreezeWrapper on %r but no Thaw method! (%s)" % (self, e))

