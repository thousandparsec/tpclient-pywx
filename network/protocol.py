
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
GETOBJ=4
OBJ=5

X = 0
Y = 1
Z = 2


class Header:
	size=4+4+4
	struct="!4sLL"

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
		elif self.type == GETOBJ:
			self.__class__ = GetObject
		elif self.type == OBJ:
			self.__class__ = Object

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

class GetObject(Processed):
	type = GETOBJ
	struct="!L"

	def __init__(self, s=None, id=None):
		if s != None:
			if id != None:
				raise Exception("ID cannot be set when you have given me a string!")
			
			Header.__init__(self, s[:Header.size])
			set_data(self, s[Header.size:])
		else:
			if id == None:
				raise Exception("ID must be set if you don't set a string")
			Header.__init__(self, None)
			self.length = 4
		
		self.id = id

	def __str__(self):
		output = Processed.__str__(self)
		output += pack(GetObject.struct, self.id)
		return output
	
	def set_data(self, data):
		self.id = unpack(GetObject.struct)

class Object(Processed):
	type = OBJ

# int32 object ID, int32 object type, string name, unsigned int64 size (diameter), 3 by signed int64 position, 3 by signed int64 velocity, 3 by signed int64 acceleration, and a list of int32 object IDs of objects contained in the current object, prefixed by the int32 of the number of items in the list

	def __init__(self, s=None, id=None, type=None, name=None, size=None, 
					pos=None, vel=None, accel=None, contains = None):
		if s != None:
			if id != None:
				raise Exception("ID cannot be set when you have given me a string!")
			
			Header.__init__(self, s[:Header.size])
			set_data(self, s[Header.size:])
		else:
			if id == None or type == None or type(name) == StringType or type(size) == LongType or \
				type(pos) == TupleType or len(pos) == 3 or \
				type(vel) == TupleType or len(vel) == 3 or \
				type(accel) == TupleType or len(accel) == 3 or \
				type(contains) == ListType:
				raise Exception("All information must be set if you don't set a string")
			Header.__init__(self, None)
		
		self.id = id
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

	def set_data(self, data):
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

def create_socket(address, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((address, port))
		return s
	except:
		return None

def connect(address, port):
	s = create_socket(address, port)

	packet = Header()
	packet.type = CONNECT

	s.send(str(packet))

	returns = readpacket(s)
	if isinstance(returns, Ok):
		return s
	else:
		socket.close()
		return None

def sprint(data):
	for i in range(0, len(data), 4):
		pprint.pprint(data[i:i+4])

if __name__ == "__main__":
	
	if sys.argv[1] == "Default":
		host, port = ("code-bear.dyndns.org", 6923)
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
	r = readpacket(s)
	pprint.pprint(r)
	pprint.pprint(str(r))

	g = GetObject(id=0)
	pprint.pprint(g)
	pprint.pprint(str(g))
	s.send(str(g))
	r = readpacket(s)
	pprint.pprint(r)
	pprint.pprint(str(r))

	for i in r.contains:	
		g = GetObject(id=i)
		pprint.pprint(g)
		pprint.pprint(str(g))
		s.send(str(g))
		r = readpacket(s)
		pprint.pprint(r)
		pprint.pprint(str(r))
