
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

def get_contains(s, r):

	print "Contains:", r.contains
	print "Valid orders:", r.orders_valid
	
	for i in r.contains:
		g = ObjectGet(id=i)
		send(s, g)
		r = recv(s)
		print "Contains:", r.contains
		print "Valid orders:", r.orders_valid
		for order in r.orders_valid:
			gl = OrderDescGet(id=order)
			send(s, gl)
			rl = recv(s)
			print rl.parameters			
		
		get_contains(s, r)

if __name__ == "__main__":
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
	send(s, l)
	recv(s)

	g = ObjectGet(id=0)
	send(s, g)
	r = recv(s)
	get_contains(s, r)

