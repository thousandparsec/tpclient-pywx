"""\
This module contains the code and objects for working with
the Thousand Parsec protocol.
"""

from xstruct import *
from cStringIO import StringIO

import pprint
import string
import socket
import sys

CONNECT=0
OK=1
LOGIN=2
FAIL=3
OBJ_GET=4
OBJ=5
ORD_GET=6
ORD=7
ORD_ADD=8
ORD_RM=9
ORD_DESCGET=10
ORD_DESC=11
OUT_GET=12
OUT=13
RSTL_GET=14
RSTL=15
TIME_GET=16
TIME=17

X = 0
Y = 1
Z = 2

class Header:
	"""\
	Base class for all protocol packets.

	Includes all the common parts for the packets.
	"""
	
	size=4+4+4
	struct="4sLL"

	def __init__(self, s=None):
		"""\
		Create a new header object.

		It takes a string which contains the "header" data.
		"""
		if s:
			output, trash = unxpack(Header.struct, s)
			self.protocol, self.type, self.length = output 
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
		elif self.type == OBJ_GET:
			self.__class__ = ObjectGet
		elif self.type == OBJ:
			self.__class__ = Object
		elif self.type == ORD_GET:
			self.__class__ = OrderGet
		elif self.type == ORD:
			self.__class__ = Order
		elif self.type == ORD_ADD:
			self.__class__ = OrderAdd
		elif self.type == ORD_RM:
			self.__class__ = OrderRemove
		elif self.type == ORD_DESCGET:
			self.__class__ = OrderDescGet
		elif self.type == ORD_DESC:
			self.__class__ = OrderDesc
		elif self.type == RSTL_GET:
			self.__class__ = ResultGet
		elif self.type == RSTL:
			self.__class__ = Result
		elif self.type == TIME_GET:
			self.__class__ = TimeRemainGet
		elif self.type == TIME:
			self.__class__ = TimeRemain

	def __str__(self):
		"""\
		Produce a string suitable to be send over the wire.
		"""
		output = xpack(Header.struct, self.protocol, self.type, self.length)
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
	
class Login(Processed):
	"""\
	A login packet.
	"""
	
	struct = "SS"

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
		# Set length of packet
		temp = xpack(Login.struct, self.username, self.password)
		self.length = len(temp)
		
		output = Processed.__str__(self)
		output += temp
		
		return output

	def SetData(self, data):
		username, password, data = xpack(Login.struct, data)

class Fail(Processed):
	"""\
	Something failed....
	"""
	type = FAIL

class ObjectGet(Processed):
	"""\
	Request an object from the server.
	"""

	type = OBJ_GET
	
	struct="L"

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
			self.length = calcsize(ObjectGet.struct)
		
		self.id = id

	def __str__(self):
		output = Processed.__str__(self)
		output += xpack(ObjectGet.struct, self.id)
		return output
	
	def SetData(self, data):
		self.id, data = xunpack(ObjectGet.struct)

class Object(Processed):
	"""\
	An object returned by the server.
	"""
	type = OBJ
	struct="LLSQ qqq qqq qqq [L] [L] I"

	def __init__(self, s=None, id=None, 
					type=None, name=None, size=None, 
					pos=[None,None,None], vel=[None,None,None], accel=[None,None,None], 
					contains=None, orders_valid=None, orders_no=None
				):
		if s != None:
			if id != None:
				raise Exception("ID cannot be set when you have given me a string!")
			
			Header.__init__(self, s[:Header.size])
			SetData(self, s[Header.size:])
		else:
			if id == None or type == None or type(name) == StringType or type(size) == LongType or \
				type(pos) != TupleType or len(pos) != 3 or \
				type(vel) != TupleType or len(vel) != 3 or \
				type(accel) != TupleType or len(accel) != 3 or \
				type(contains) != ListType or type(orders_valid) != ListType or \
				orders_no != None:
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
		self.orders_valid = orders_valid
		self.orders_no = orders_no

	def __str__(self):
		output = Processed.__str__(self)
		output += xpack(Object.struct,
							self.id,
							self.type,
							self.name,
							self.size,
							self.pos[X], self.pos[Y], self.pos[Z],
							self.vel[X], self.vel[Y], self.vel[Z],
							self.accel[X], self.accel[Y], self.accel[Z],
							self.contains,
							self.orders_valid,
							self.orders_no)
		return output

	def SetData(self, data):
		# First bit
		self.pos = [None, None, None]
		self.vel = [None, None, None]
		self.accel = [None, None, None]

		output, trash = unxpack(Object.struct, data)
		self.id, \
		self.type, \
		self.name, \
		self.size, \
		self.pos[X], self.pos[Y], self.pos[Z], \
		self.vel[X], self.vel[Y], self.vel[Z], \
		self.accel[X], self.accel[Y], self.accel[Z], \
		self.contains, \
		self.orders_valid, \
		self.orders_no = output
		
		# Check to see if we have any data left, if so we have stuffed up
		if len(trash) > 0:
			pprint.pprint("Leftover: (" + trash + ")")
			raise "Leftover data was found, something went wrong!"
			
class OrderDescGet(Processed):
	"""\
	A get order desc packet.
	"""

	type = ORD_DESCGET

	struct="L"

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
			self.length = calcsize(ObjectGet.struct)
		
		self.id = long(id)

	def __str__(self):
		output = Processed.__str__(self)
		output += xpack(OrderDescGet.struct, self.id)
		return output
	
	def SetData(self, data):
		self.id = unxpack(OrderDescGet.struct)

class OrderDesc(Processed):
	"""\
	A order description packet.
	"""

	type = ORD_DESC
	
	struct="L SS [SIS]"

	orders = {}
	ARG_COORD = 0
	ARG_TIME = 1
	ARG_OBJECT = 2
	ARG_PLAYER = 3

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
		output += xpack(OrderDesc.struct,
							self.type,
							self.name,
							self.desc,
							self.parameters)
		return output
	
	def SetData(self, data):
		# Type
		output, trash = unxpack(OrderDesc.struct, data)
		self.type, self.name, self.desc, self.parameters = output

		OrderDesc.orders[self.type] = self

	def get_struct(self):
		# Build a struct defenition for this order.
		pass

class OrderGet(Processed):
	pass

class Order(Processed):
	"""\
	An order object.
	"""

	struct = ""

	def __init__(self, s=None, type=None, **kw):
		pass


	def check_type(self):
		# Check that the type we have has been described.
		pass
		

	def SetData(self, data):
		pass		


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

