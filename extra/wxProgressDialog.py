"""\
This module creates a fake progress bar for older versions of wxPython 
where it is broken and won't close properly.
"""

try:
	from wxPython.wx import wxVERSION_NUMBER
except ImportError:
	from wxPython.wx import wxVERSION
	wxVERSION_NUMBER = wxVERSION[0]*1000 + wxVERSION[1]*100 + wxVERSION[2]*10 + wxVERSION[3]

if wxVERSION_NUMBER <= 2302:
	class wxProgressDialog:
		def __init__(self, *kw, **args):
			print "Your version of wxPython doesn't have working Progress dialogs."
			print "If you want progress dialogs please upgrade to a newer version."

		def Update(self, no):
			pass
else:
	from wxPython.wx import wxProgressDialog
