"""\
This module creates a fake progress bar for older versions of wxPython 
where it is broken and won't close properly.
"""

from wxPython.wx import wxVERSION_NUMBER

if wxVERSION_NUMBER <= 2302:
	class wxProgressDialog:
		def __init__(self, *kw, **args):
			print "Your version of wxPython doesn't have working Progress dialogs."
			print "If you want progress dialogs please upgrade to a newer version."

		def Update(self, no):
			pass
else:
	from wxPython.wx import wxProgressDialog
