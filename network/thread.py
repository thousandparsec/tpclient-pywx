
from wxPython.wx import * 

from protocol import *
from events import *

import pprint
import time

class network_thread:

	def __init__(self, windows=[]):
		self.windows = windows

	def append(self, window):
		self.windows.append(window)

	def __call__(self, socket):

		while TRUE:
			print "Looping"
			packet = readpacket(socket)

			print "Got Packet"
			print "----------------------"
			pprint.pprint(packet)
			pprint.pprint(str(packet))
		
			evt = NetworkPacketEvent(packet)

			for window in self.windows:
				print "Sending to window", window
				wxPostEvent(window, evt)

			# pause for a second
			#time.sleep(30)
