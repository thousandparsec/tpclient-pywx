#! /usr/bin/python

from protocol import *
import pprint

def print_packet(p):
	pprint.pprint(p)
	pprint.pprint(str(p))

def red(p):
	sys.stdout.write("[01;32m")
	print_packet(p)
	sys.stdout.write("[0m")
	sys.stdout.flush()

def green(p):
	sys.stdout.write("[01;31m")
	print_packet(p)
	sys.stdout.write("[0m")
	sys.stdout.flush()

def recv(s):
	r = read_packet(s, DEBUG=1)
	red(r)
	return r
	
def send(s, p):
	green(p)
	s.send(str(p))

def print_obj(o):
	print "Contains:", o.contains
	print "Valid orders:", o.orders_valid
	print "Number of orders:", o.orders_no

def get_contains(s, r):

	print_obj(r)
	
	for i in r.contains:
	
		g = ObjectGet(id=i)
		send(s, g)
		r = recv(s)
		
		print_obj(r)
		
		for order in r.orders_valid:
			gl = OrderDescGet(id=order)
			send(s, gl)
			rl = recv(s)
			print rl.parameters			
		
			# Okay now we need to build from values for each of these parameters
			print "Order Desc: ", i, rl.id
			args = [None, i, rl.id, -1]
			for name, type, desc in rl.parameters:
				if type == OrderDesc.ARG_COORD:
					args += [10,10,10]
				elif type == OrderDesc.ARG_TIME:
					args += [10]
				elif type == OrderDesc.ARG_OBJECT:
					args += [3]
				elif type == OrderDesc.ARG_PLAYER:
					args += [1]

			go = apply(OrderAdd, args)
			print "Send Args:", go.args
			send(s, go)
			ro = recv(s)
		
		# Update the object
		g = ObjectGet(id=i)
		send(s, g)
		r = recv(s)

		print_obj(r)

		# Get the orders
		for slot in range(0, r.orders_no):
			gl = OrderGet(oid=i, slot=slot)
			send(s, gl)
			rl = recv(s)
			print "Got Args:", rl.args

		# Remove the orders
		l = range(0, r.orders_no)
		l.reverse()
		for slot in l:
			gl = OrderRemove(oid=i, slot=slot)
			send(s, gl)
			rl = recv(s)

		# Update the object
		g = ObjectGet(id=i)
		send(s, g)
		r = recv(s)

		print_obj(r)

		get_contains(s, r)

def testall(host, port):

	print "Connection to", host, port
	s = connect(host, port)
	
	if not s:
		sys.exit("Could not connect! Please try again later.")
	else:
		print "We connected okay, constructing a login packet"

	username=sys.argv[2]
	password=sys.argv[3]
	
	l = Login(username=username, password=password)
	send(s, l)
	recv(s)

	g = ObjectGet(id=0)
	send(s, g)
	r = recv(s)
	get_contains(s, r)

import curses

def main(stdsrc):
	print "Peanut"

if __name__ == "__main__":
	if sys.argv[1].lower() == "default":
		host, port = ("127.0.0.1", 6923)
	else:
		host, port = string.split(sys.argv[1], ':', 1)
		port = int(port)

	testall(host, port)

	#curses.wrapper(main)
