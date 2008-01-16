
from tp.client.decorators import simple_decorator

@simple_decorator
def freeze_wrapper(function):
	def w(self, *args, **kw):
		try:
			try:
				print "Freezing", self
				self.Freeze()
			except AttributeError:
				raise Warning("FreezeWrapper on %r but no Freeze method! (%s)" % (self, e))
		
			function(self, *args, **kw)

		finally:
			try:
				print "Thawing", self
				self.Thaw()
			except AttributeError, e:
				raise Warning("FreezeWrapper on %r but no Thaw method! (%s)" % (self, e))
	return w

