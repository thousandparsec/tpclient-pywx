"""\
This module contains the code for the network thread which
dispatchs events for incoming packets.
"""
# Python imports
import time
from thread import allocate_lock

# wxWindows imports
from wxPython.wx import * 

# Game imports
from utils import *

# Local imports
from protocol import *
from events import *
from extra.evtmgr import eventManager

class NetworkThread:
	def __init__(self):
		self.windows = []

		self.socket = None
		self.lock = allocate_lock()

	def win_connect(self, window):
		"""\
		Starts a window recieving the events from the network thread.
		"""
		self.windows.append(window)

	def win_disconnect(self, window):
		"""\
		Stops a window from recieving events from the network thread.
		"""
		self.windows.remove(window)

	def connect(self, host, port):
		"""\
		Causes the network thread to connect to a host/port

		After the connection has succeded the EVT_NETWORK_CONNECT will
		be raised.

		This function does block until the socket is created.
		"""
		debug(DEBUG_NETWORK, "Connecting to %s:%s" % (host, port))
		self.socket = create_socket(host, port)

		# Need to issue a EVT_NETWORK_CONNECT here

		return self.socket

	def disconnect(self):
		"""\
		Causes the network thread to disconnect.

		A EVT_NETWORK_DISCONNECT will be raised just before the
		socket is destroyed. The socket may not be still valid
		however.

		This function does block until the socket is destroyed.
		"""
		debug(DEBUG_NETWORK, "Disconnection")
		# Need to issue a EVT_NETWORK_DISCONNECT here
		
		self.socket = None

	def send(self, object):
		"""\
		Sends an object out onto the wire. 
		
		Only objects based protocol.Header will be accepted and sent.

		This function currently block until the data has been sent. This
		may not be the case always however.
		"""
		debug(DEBUG_NETWORK, "Trying to send an %s of %s" % (repr(object), type(object)))
		if isinstance(object, Header):
			self.socket.send(str(object))
		else:
			raise IOError("Trying to send an invalid object")

	def next(self):
		"""\
		This function will allow the network thread to process
		the next packet. 
		
		It MUST be called after an event occurs or the thread will
		block forever!!!!!!!!
		"""
		if self.locked():
			self.lock.release()

	def locked(self):
		"""\
		Find out if the network thread is currently locked because
		it is processing a packet.
		"""
		return self.lock.locked()

	def __call__(self):
		"""\
		This is the main loop. It will never terminate and should be
		called in it's own thread.
		"""
		# Main thread loop
		while TRUE:
			s = self.socket
			
			if s == None:
				debug(DEBUG_NETWORK, "No socket.")
				time.sleep(1)
			else:
				# We have a socket lets do some work
				debug(DEBUG_NETWORK, "Waiting on packet")
				packet = read_packet(s)

				debug(DEBUG_NETWORK, "Got Packet")
		
				evt = NetworkPacketEvent(packet, self)

				for window in self.windows:
					# The lock is used so the functions can be certain that another packet
					# won't appear until they call unlock
					debug(DEBUG_NETWORK, "Waiting for lock")
					self.lock.acquire()
					debug(DEBUG_NETWORK, "Sending to window %s" % window)
					wxPostEvent(window, evt)

