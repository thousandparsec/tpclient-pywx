
from struct import *
from cStringIO import StringIO

import string
import socket
import sys
import pprint

CONNECT=0
OK=1
LOGIN=2
FAIL=3
GET_OBJECT=4
OBJECT=5


class Header:
	size=4+4+4
	struct="!4sII"

	def __init__(self, s=None):
		if s:
			self.protocol, self.type, self.length = unpack(Header.struct, s)
			if self.protocol != ("TP01"):
				raise Exception("Invalid creation string")
		else:
			self.protocol = "TP01"
			self.length = 0
		
		self.data = None

	def set_data(self, data=None):
		if self.data == None:
			self.length = 0
		else:
			self.length = len(data)

	def process(self):
		if self.type == CONNECT:
			self.__class__ = Connect
		elif self.type == OK:
			self.__class__ = Ok
		elif self.type == LOGIN:
			self.__class__ = Login
		elif self.type == FAIL:
			self.__class__ = Fail
		elif self.type == GET_OBJECT:
			self.__class__ = GetObject
		elif self.type == OBJECT:
			pass

	def __str__(self):
		output = pack(Header.struct, self.protocol, self.type, self.length)
		return output

class Processed(Header):
	def process(self):
		raise Exception("Cannot reprocess an already processed packet")

class Connect(Processed):
	type = CONNECT

class Ok(Processed):
	type = OK

class Fail(Processed):
	type = FAIL

class Login(Processed):
	type = LOGIN
	
	def __init__(self, s=None, username=None, password=None):
		if s != None:
			if username != None or password != None:
				raise Exception("Username cannot be set when you have given me a string!")
			Header.__init__(self, s[:Header.size])
			set_data(self, s[Header.size:])
		else:
			if username == None or password == None:
				raise Exception("Username and password must be set if you don't set a string")
			Header.__init__(self, None)

		self.username = username
		self.password = password

	def __str__(self):
		temp = prep_string(self.username) + prep_string(self.password)
		self.length = len(temp)
		output = Processed.__str__(self)
		output += temp
		
		return output

	def set_data(self, data):
		username, data = unprep_string(data)
		password, data = unprep_string(data)

def unprep_string(s):
	"""\
	Returns the first string from the input data and any remaining data
	"""
	# Remove the length
	l = int(unpack("!I", s[0:4])[0])
	s = s[4:]
	# Get the string, (we don't need the null terminator so nuke it)
	output = s[:l-1]
	s = s[l:]
	# Remove anyremaining null terminators
	s = s[4 - (l % 4):]
	return string.strip(output), s

def prep_string(s):
	"""\
	Prepares a string to be send out on a wire.
	
	It appends the string length to the beginning, adds a null terminator and padds the string to a 32 bit boundry.
	"""
	temp = s + "\0"
	return pad(pack("!I", len(temp)) + temp)

def pad(s):
	"""\
	Pads a string with null characters untill it gets to a 32 bit boundry
	"""
	if len(s) % 4 != 0:
		s += "\0" * (4 - (len(s) % 4))
	return s

def readpacket(s):
	string = s.recv(Header.size)
	h = Header(string)
	h.process()

	if h.length > 0:
		h.set_data(s.recv(h.length))

	return h

def connect(address, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((address, port))

	packet = Header()
	packet.type = CONNECT

	s.send(str(packet))

	returns = readpacket(s)
	if isinstance(returns, Ok):
		return s
	else:
		socket.close()
		return None

if __name__ == "__main__":
	
	if sys.argv[1] == "Default":
		host, port = ("code-bear.dyndns.org", 6923)
	else:
		host, port = string.split(sys.argv[1], ':', 1)
		port = int(port)
	
	s = connect(host, port)
	
	if not s:
		sys.exit("Could not connect! Please try again later.")
	else:
		print "We connected okay, constructing a login packet"

	username=sys.argv[2]
	password=sys.argv[3]
	l = Login(username=username, password=password)
	pprint.pprint(l)
	pprint.pprint(str(l))
	s.send(str(l))
	r = readpacket(s)
	pprint.pprint(r)
	pprint.pprint(str(r))
