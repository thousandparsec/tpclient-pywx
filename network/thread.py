
from wxPython.wx import * 

from protocol import *
from events import *

import pprint
import time

class network_thread:

	def __init__(self, windows=[]):
		self.locked = 0
		self.windows = windows

	def append(self, window):
		self.windows.append(window)

	def lock(self):
		self.locked += 1
	
	def unlock(self):
		self.locked -= 1

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

			while self.locked > 0:
				time.sleep(0.1)

			# pause for a second
			#time.sleep(30)
