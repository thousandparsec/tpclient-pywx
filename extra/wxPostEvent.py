

from wxPython.wx import wxPostEvent as _wxPostEvent

ghandlers = []

def wxHandler(handler):
	global ghandlers
	
	ghandlers.append(handler)

def wxPostEvent(arg1, arg2=None):
	global ghandlers
	
	if arg2 != None:
		windows = [arg1]
		event = arg2
	else:
		windows = ghandlers
		event = arg1
	
	for w in windows:
		_wxPostEvent(w, event)

