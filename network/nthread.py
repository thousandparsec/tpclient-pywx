"""\
This module contains the code for the network thread which
dispatchs events for incoming packets.
"""

from wxPython.wx import * 

from protocol import *
from events import *

import pprint
import time

from thread import allocate_lock

class network_thread:

	def __init__(self, windows=[]):
		self.lock = allocate_lock()
		self.windows = windows

	def append(self, window):
		self.windows.append(window)

	def next(self):
		self.lock.release()

	def locked(self):
		return self.lock.locked()

	def __call__(self, socket):

		while TRUE:
			packet = readpacket(socket)

			print "Got Packet"
			print "----------------------"
			pprint.pprint(packet)
			pprint.pprint(str(packet))
		
			evt = NetworkPacketEvent(packet)

			for window in self.windows:
				self.lock.acquire()
				print "Sending to window", window
				wxPostEvent(window, evt)

			# pause for a second
			#time.sleep(30)
