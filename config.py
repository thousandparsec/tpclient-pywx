
import os
import cPickle as pickle

class Blank:
	pass

cache = {}
def load_data(file):
	global cache
	
	if file not in cache.keys():
		try:
			cache[file] = _load_data(file)
		except IOError:
			return None
		
	return cache[file]
	
def _load_data(file):
	f = open(os.path.join("var", file), "r")
	return pickle.load(f)

def save_data(file, data):
	f = open(os.path.join("var", file), "w")
	pickle.dump(data, f)

def load_conf(file):

	returns = {}

	f = open(os.path.join("var", file))
	data = string.split(f.read(), '\n')

	bits = None
	for i in data:
		try:
			#print i
			if i[0] == '#':
				continue
			if i[0] == '/':
				if bits:
					if type(bits[1]) == type([]):
						bits[1] = string.join(bits[1], " ")
					bits[1] = bits[1] + "\n" + i[1:]
					returns[bits[0]] = bits[1]
				else:
					continue
			else:
				bits = string.split(i,"=",1)
				bits = [string.strip(bits[0]), string.strip(bits[1])]
				
				if len(string.split(bits[1])) > 1:
					bits[1] = string.split(bits[1])
			
				returns[bits[0]] = bits[1]
		except:
			do_traceback()

	return returns
	
