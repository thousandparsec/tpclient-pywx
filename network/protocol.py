"""\
This module contains the code and objects for working with
the Thousand Parsec protocol.
"""

from struct import *
from cStringIO import StringIO

import string
import socket
import sys

CONNECT=0
OK=1
LOGIN=2
FAIL=3
GETOBJ=4
OBJ=5

X = 0
Y = 1
Z = 2

class Header:
	"""\
	Base class for all protocol packets.

	Includes all the common parts for the packets.
	"""
	
	size=4+4+4
	struct="!4sLL"

	def __init__(self, s=None):
		"""\
		Create a new header object.

		It takes a string which contains the "header" data.
		"""
		if s:
			self.protocol, self.type, self.length = unpack(Header.struct, s)
			if self.protocol != ("TP01"):
				raise Exception("Invalid creation string")
		else:
			self.protocol = "TP01"
			self.length = 0
		
		self.data = None

	def SetData(self, data=None):
		"""\
		Processes the data of the packet.
		"""
		if self.data == None:
			self.length = 0
		else:
			self.length = len(data)

	def Process(self):
		"""\
		Look at the packet type and muta this object into the
		correct type.
		"""
		
		if self.type == CONNECT:
			self.__class__ = Connect
		elif self.type == OK:
			self.__class__ = Ok
		elif self.type == LOGIN:
			self.__class__ = Login
		elif self.type == FAIL:
			self.__class__ = Fail
		elif self.type == GETOBJ:
			self.__class__ = GetObject
		elif self.type == OBJ:
			self.__class__ = Object

	def __str__(self):
		"""\
		Produce a string suitable to be send over the wire.
		"""
		output = pack(Header.struct, self.protocol, self.type, self.length)
		return output

class Processed(Header):
	"""\
	Superclass for all objects which have been processed.

	Basicly stops you processing an object twice.
	"""

	def Process(self):
		raise Exception("Cannot reprocess an already processed packet")

class Connect(Processed):
	"""\
	Connect packet.

	Sent just after connecting to the server to check it actually is
	a TP server and uses a compatible protocol.
	"""
	type = CONNECT

class Ok(Processed):
	"""\
	Something succeded..
	"""
	type = OK

class Fail(Processed):
	"""\
	Something failed....
	"""
	type = FAIL

class GetObject(Processed):
	"""\
	Request an object from the server.
	"""
	type = GETOBJ
	struct="!L"

	def __init__(self, s=None, id=None):
		if s != None:
			if id != None:
				raise Exception("ID cannot be set when you have given me a string!")
			
			Header.__init__(self, s[:Header.size])
			SetData(self, s[Header.size:])
		else:
			if id == None:
				raise Exception("ID must be set if you don't set a string")
			Header.__init__(self, None)
			self.length = 4
		
		self.id = long(id)

	def __str__(self):
		output = Processed.__str__(self)
		output += pack(GetObject.struct, self.id)
		return output
	
	def SetData(self, data):
		self.id = unpack(GetObject.struct)

class Object(Processed):
	"""\
	An object returned by the server.
	"""
	type = OBJ

	def __init__(self, s=None, id=None, type=None, name=None, size=None, 
					pos=None, vel=None, accel=None, contains = None):
		if s != None:
			if id != None:
				raise Exception("ID cannot be set when you have given me a string!")
			
			Header.__init__(self, s[:Header.size])
			SetData(self, s[Header.size:])
		else:
			if id == None or type == None or type(name) == StringType or type(size) == LongType or \
				type(pos) == TupleType or len(pos) == 3 or \
				type(vel) == TupleType or len(vel) == 3 or \
				type(accel) == TupleType or len(accel) == 3 or \
				type(contains) == ListType:
				raise Exception("All information must be set if you don't set a string")
			Header.__init__(self, None)
		
		self.id = long(id)
		self.type = type
		self.name = name
		self.size = size
		self.pos = pos
		self.vel = vel
		self.accel = accel
		self.contains = contains

	struct1="!LL"
	struct2="!Q 3q 3q 3q L"
	struct3="!L"

	def __str__(self):
		output = Processed.__str__(self)
		output += pack(Object.struct1, self.id, self.type)
		output += prep_string(self.name)
		output += pack(Object.struct2, self.size, 
						self.pos[X], self.pos[Y], self.pos[Z],
						self.vel[X], self.vel[Y], self.vel[Z],
						self.accel[X], self.accel[Y], self.accel[Z],
						len(self.contains))

		for id in self.contains:
			output += pack(Object.struct3, id)

		return output

	def SetData(self, data):
		# First bit
		struct1_data = data[0:calcsize(Object.struct1)]
		self.id, self.type = unpack(Object.struct1, struct1_data)
		data = data[calcsize(Object.struct1):]
		
		# Extra the name
		self.name, data = unprep_string(data)
		
		# Second bit
		struct2_data = data[0:calcsize(Object.struct2)]
		s, px, py, pz, vx, vy, vz, ax, ay, az, lc = unpack(Object.struct2, struct2_data)
		self.size = s
		self.pos = (px, py, pz)
		self.vel = (vx, vy, vz)
		self.accel = (ax, ay, az)
		data = data[calcsize(Object.struct2):]
		
		# Contains ID's
		struct3_size = calcsize(Object.struct3)
		contains = []
		for i in range(0, lc*struct3_size, struct3_size):
			contains.append(unpack(Object.struct3, data[i:i+struct3_size])[0])
		self.contains = contains


class Login(Processed):
	"""\
	A login packet.
	"""

	type = LOGIN
	
	def __init__(self, s=None, username=None, password=None):
		if s != None:
			if username != None or password != None:
				raise Exception("Username cannot be set when you have given me a string!")
			Header.__init__(self, s[:Header.size])
			SetData(self, s[Header.size:])
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

	def SetData(self, data):
		username, data = unprep_string(data)
		password, data = unprep_string(data)

def unprep_string(s):
	"""\
	Returns the first string from the input data and any remaining data
	"""
	# Remove the length
	l = int(unpack("!I", s[0:4])[0])
	if l > 0:
		s = s[4:]
		# Get the string, (we don't need the null terminator so nuke it)
		output = s[:l-1]
		s = s[l:]
		# Remove anyremaining null terminators
		s = s[4 - (l % 4):]
		return string.strip(output), s
	else:
		return "", s

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

def read_packet(s):
	"""\
	Reads a single TP packet from the socket and returns it.
	"""
	string = s.recv(Header.size)
	h = Header(string)
	h.Process()
	
	if h.length > 0:
		data = s.recv(h.length)
		h.SetData(data)

	return h

def create_socket(address, port):
	"""\
	Creates a socket, just a convience function.
	"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((address, port))
		return s
	except:
		return None

def connect(address, port):
	"""\
	Connects to a TP server.

	Checks that the server is actually a TP server and that
	the protocol is compatible with the client.
	"""
	s = create_socket(address, port)

	packet = Header()
	packet.type = CONNECT

	s.send(str(packet))

	returns = read_packet(s)
	if isinstance(returns, Ok):
		return s
	else:
		socket.close()
		return None

def get_contains(r):
	import pprint

	for i in r.contains:	
		g = GetObject(id=i)
		pprint.pprint(g)
		pprint.pprint(str(g))
		s.send(str(g))
		r = read_packet(s)
		pprint.pprint(r)
		pprint.pprint(str(r))
		
		get_contains(r)
		
if __name__ == "__main__":
	import pprint

	if sys.argv[1].lower() == "default":
		host, port = ("127.0.0.1", 6923)
	else:
		host, port = string.split(sys.argv[1], ':', 1)
		port = int(port)

	print "Connection to", host, port
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
	r = read_packet(s)
	pprint.pprint(r)
	pprint.pprint(str(r))

	g = GetObject(id=0)
	pprint.pprint(g)
	pprint.pprint(str(g))
	s.send(str(g))
	r = read_packet(s)
	pprint.pprint(r)
	pprint.pprint(str(r))

	get_contains(r)

