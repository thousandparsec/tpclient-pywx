"""\
This module contains the code for the base of the network and 
game threads.
"""
# Python imports
import time

# wxWindows imports
from wxPython.wx import * 
from extra.wxPostEvent import *

class BaseThread(wxEvtHandler):
	def __init__(self):
		wxEvtHandler.__init__(self)
		wxHandler(self)
		
		self.windows = []

	def WinConnect(self, window):
		"""\
		Starts a window recieving the events from the thread.
		"""
		self.windows.append(window)

	def WinDisconnect(self, window):
		"""\
		Stops a window from recieving events from the thread.
		"""
		self.windows.remove(window)

	def __call__(self):
		"""\
		This is the main loop. It will never terminate and should be
		called in it's own thread.
		"""
		# Main thread loop
		while TRUE:
			time.sleep(120)
