"""\
This module contains the code for the network thread which
dispatchs events for incoming packets.
"""

from wxPython.wx import * 

from protocol import *
from events import *

import pprint
import time
import sys

from thread import allocate_lock

class GameThread:

	def __init__(self, windows=[]):
		self.lock = allocate_lock()
		self.windows = windows

	def append(self, window):
		self.windows.append(window)

	def next(self):
		if self.locked():
			self.lock.release()

	def locked(self):
		return self.lock.locked()

	def __call__(self, socket):

		self.socket = socket

		while TRUE:
			print "Waiting on packet"
			packet = read_packet(socket)

			print "Got Packet"
		
			evt = NetworkPacketEvent(packet, self)

			for window in self.windows:
				print "Waiting for lock"
				self.lock.acquire()
				print "Sending to window", window
				wxPostEvent(window, evt)

			# pause for a second
			#time.sleep(30)
