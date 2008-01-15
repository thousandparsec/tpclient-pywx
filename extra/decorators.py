def simple_decorator(decorator):
    """This decorator can be used to turn simple functions
    into well-behaved decorators, so long as the decorators
    are fairly simple. If a decorator expects a function and
    returns a function (no descriptors), and if it doesn't
    modify function attributes or docstring, then it is
    eligible to use this. Simply apply @simple_decorator to
    your decorator and it will automatically preserve the
    docstring and function attributes of functions to which
    it is applied."""
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    # Now a few lines needed to make simple_decorator itself
    # be a well-behaved decorator.
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator

#
# Sample Use:
#
@simple_decorator
def mySimpleLoggingDecorator( func ):
    def YOU_WILL_NEVER_SEE_THIS_NAME( *args, **kwargs ):
        print 'calling %s' % func.__name__
        return func( *args, **kwargs )
    return YOU_WILL_NEVER_SEE_THIS_NAME

@mySimpleLoggingDecorator
def double(x):
    "Doubles a number"
    return 2*x

assert double.__name__ == 'double'
assert double.__doc__ == 'Doubles a number'

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

