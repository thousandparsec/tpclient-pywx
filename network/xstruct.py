
import struct
import sys
import string
from types import *

pack = struct.pack
unpack = struct.unpack
calcsize = struct.calcsize

def hexbyteprint(string):
	for i in string:
		print hex(ord(i)),
	print


def xpack(struct, *args):
	"""\
	For advanced version of pack which works with all
	TP constructs.

	Everything is assumed to be network order, ie you don't need to
	prepend every struct with !

	L	Unsigned Long		unsigned int64
	Q	Unsigned Int		unsigned int32
	q	Signed Int			int32
	
	S	String
	[	List Start			The structure of the data in the list is 
	]	List End			described by the data inside the []
							Example:
								[L] would be a list of unsigned longs
							It is actually transmitted as
							<length><data><data><data>
	
	Obviously you can't calculate size of an xpack string.
	"""
	args = list(args)
	output = ""

	while len(struct) > 0:
		char = struct[0]
		struct = struct[1:]
		
		if char == ' ' or char == '!':
			continue
		elif char == '[':
			# Find the closing brace
			substruct, struct = string.split(struct, ']', maxsplit=1)
			output += pack_list('L', substruct, args.pop(0))
		elif char == '{':
			# Find the closing brace
			substruct, struct = string.split(struct, '}', maxsplit=1)
			output += pack_shortlist('I', args.pop(0))
		elif char == 'S':
			output += pack_string(args.pop(0))
		elif char in string.digits:
			# Get all the numbers
			substruct = char
			while struct[0] in string.digits:
				substruct += struct[0]
				struct = struct[1:]
			# And the value the number applies to
			substruct += struct[0]
			struct = struct[1:]
			
			output += pack("!"+substruct, args.pop(0))
		else:
			output += pack("!"+char, args.pop(0))
			
	return output


def unxpack(struct, s):
	output = []
	
	while len(struct) > 0:
		char = struct[0]
		struct = struct[1:]

		if char == ' ' or char == '!':
			continue
		elif char == '[':
			# Find the closing brace
			substruct, struct = string.split(struct, ']', maxsplit=1)
			data, s = unpack_list("L", substruct, s)

			output.append(data)
		elif char == '{':
			# Find the closing brace
			substruct, struct = string.split(struct, '}', maxsplit=1)
			data, s = unpack_list("I", substruct, s)

			output.append(data)
		elif char == 'S':
			data, s = unpack_string(s)
			output.append(data)
			
		elif char in string.digits:
			# Get all the numbers
			substruct = char
			while struct[0] in string.digits:
				substruct += struct[0]
				struct = struct[1:]
			# And the value the number applies to
			substruct += struct[0]
			struct = struct[1:]
			
			size = calcsize(substruct)
			data = unpack("!"+substruct, s[:size])
			s = s[size:]

			output += data
		else:
			substruct = "!"+char

			size = calcsize(substruct)

			data = unpack(substruct, s[:size])
			s = s[size:]

			output += data

	return tuple(output), s

def pack_list(length_struct, struct, args):
	"""\
	Packs the id list so it can be send.
	"""
	# The length
	output = xpack(length_struct, len(args))

	# The list
	for id in args:
		if type(id) == ListType or type(id) == TupleType:
			args = [struct] + list(id)
			output += apply(xpack, args)
		else:
			output += xpack(struct, id)
		
	return output

def unpack_list(length_struct, struct, s):
	"""\
	Returns the first string from the input data and any remaining data
	"""
	output, s = unxpack(length_struct, s)
	length, = output

	list = []
	for i in range(0, length):
		output, s = unxpack(struct, s)
		if len(output) == 1:
			list.append(output[0])
		else:
			list.append(output)

	return list, s

def pack_string(s):
	"""\
	Prepares a string to be send out on a wire.
	
	It appends the string length to the beginning, adds a 
	null terminator and padds the string to a 32 bit boundry.
	"""
	temp = s + "\0"
	return pad(pack("!I", len(temp)) + temp)

def unpack_string(s):
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
		return output, s
	else:
		return "", s

def pad(s):
	"""\
	Pads a string with null characters untill it gets to a
	32 bit boundry
	"""
	if len(s) % 4 != 0:
		s += "\0" * (4 - (len(s) % 4))
	return s
