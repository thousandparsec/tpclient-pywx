"""\
This file contains functions used to deal with objects.
"""
from tp.netlib.objects			  			  import Structures
from tp.netlib.objects						  import parameters
from tp.netlib import objects
from tp.netlib import GenericRS
#from tp.netlib.objects import OrderDescs

def getPositionList(obj):
	"""
	Get a list of the position references of a DynamicObject as tuples.
	Each tuple has the form: (x, y, z, coord name)
	"""
	positionslist = []
	for propertygroup in obj.properties:
		if type(propertygroup) != Structures.GroupStructure:
			continue
			
		positionattrsstruct = getattr(obj, propertygroup.name)
		for property in propertygroup.structures:
			if type(property) != parameters.ObjectParamPosition3d:
				continue
			
			coords = getattr(positionattrsstruct, property.name).vector
			relative = getattr(positionattrsstruct, property.name).relative
			
			if relative == 0:
				positionslist.append((coords.x, coords.y, coords.z, property.name))
				continue
				
			refpositions = get_position_list(cache.objects[relative])
			
			if refpositions == []:
				raise ValueError("Reference object for coordinates does not have a position.")
				continue
			
			positionslist.append((coords.x + refpositions[0][0], coords.y + refpositions[0][1], coords.z + refpositions[0][2], property.name))
				
	return positionslist
	
def isTopLevel(cache, oid):
	"""
	Attempt to determine whether an object is the universe or a galaxy.
	"""
	# FIXME: This is a hack, currently we determine this by assuming any object 
	# which has no useful information and is parented to Universe is "Top Level"

	obj = cache.objects[oid]

	# If the object doesn't have a parent, it is top level.
	if not hasattr(obj, 'parent'):
		return True
	
	# If the object has ID 0, it's the Universe.
	if obj.id == 0:
		return True
		
	# If the object's parent is the universe, it could be a galaxy (but it might 
	# not be, so keep checking). 
	# Otherwise, it's not top level.
	if cache.objects[obj.parent].id != 0:
		return False
	
	# If the object has any properties other than Positional and Media ones, it's not a
	# galaxy.
	for propertygroup in obj.properties:
		if propertygroup.name != "Positional" and propertygroup.name != "Informational" and propertygroup.name != "Media":
			print propertygroup.name
			return False
	
	# If it only has a positional property list, it's a galaxy.
	return True

def isFleet(cache, oid):
	"""
	Returns true if this object is a fleet. Relies on the fact that fleets have ship lists.
	"""
	
	obj = cache.objects[oid]
	
	for propertygroup in obj.properties:
		positionattrsstruct = getattr(obj, propertygroup.name)
		if hasattr(positionattrsstruct, 'Ship List'):
			return True
	
	return False


def canObjectMove(cache, oid):
	ordertypes = getOrderTypes(cache, oid)
	# Check if this object can move so we can enable waypoint mode
	for queueid, typelist in ordertypes.items():
		for otype in typelist:
			order = objects.OrderDescs()[otype]

			# FIXME: Needs to be a better way to do this... what if there's an order
			# type where the object can't move but it can place or throw something to
			# a specific point? Then the order will have coordinates, and this will
			# give a false positive, enabling the waypoint button.
			for property in order.properties:
				if type(property) == parameters.OrderParamAbsSpaceCoords \
					or type(property) == parameters.OrderParamRelSpaceCoords:
					return True

	return False

def hasResources(cache, oid):
	"""
	Returns true if this object has resources.
	"""
	
	obj = cache.objects[oid]
	
	for propertygroup in obj.properties:
		group = getattr(obj, propertygroup.name)
		
		for paramlist in group.structures:
			if type(paramlist) != parameters.ObjectParamResourceList:
				continue
				
			return True
	
	return False
	
def getResources(cache, oid):
	"""
	Get a list of tuples of resources in an object.
	
	@return a list of tuples in the form (id, amount stored, amount available to be mined, amount unavailable)
	"""
	
	obj = cache.objects[oid]
	resources = []
	
	for propertygroup in obj.properties:
		group = getattr(obj, propertygroup.name)
		
		for paramlist in group.structures:
			if type(paramlist) != parameters.ObjectParamResourceList:
				continue
				
			resourcelist = getattr(group, paramlist.name).resources
			for resource in resourcelist:
				resources.append(resource)
	return resources
	
def getOrderTypes(cache, oid):
	"""
	Returns a dictionary of lists of order types an object can support for each order queue,
	or [] if none. Keyed by order queue ID.
	"""
	ordertypes = {}
	obj = cache.objects[oid]
	for propertygroup in obj.properties:
		group = getattr(obj, propertygroup.name)
		
		for queue in group.structures:
			if type(queue) != parameters.ObjectParamOrderQueue:
				continue
			
			ordertypes[getattr(group, queue.name).queueid] = getattr(group, queue.name).ordertypes
	return ordertypes

def getOrderQueueList(cache, oid):
	"""
	Returns a list of tuples representing order queues for an object.
	
	@return a list of tuples, each has the form (order queue name, order queue ID)
	"""
	orderqueuelist = []
	obj = cache.objects[oid]
	for propertygroup in obj.properties:
		group = getattr(obj, propertygroup.name)
		
		for queue in group.structures:
			if type(queue) != parameters.ObjectParamOrderQueue:
				continue
			
			orderqueuelist.append((queue.name, getattr(group, queue.name).queueid))
	return orderqueuelist

def getOrderQueueLimit(cache, oid, qid):
	"""
	Returns the maximum orders the queue with the given qid can hold, or -1 if no limit.
	"""
	obj = cache.objects[oid]
	desc = objects.ObjectDescs()[obj.subtype]
	for propertygroup in obj.properties:
		group = getattr(obj, propertygroup.name)
		
		for queue in group.structures:
			if type(queue) != parameters.ObjectParamOrderQueue:
				continue
			
			return queue.maxslots
	return -1

def getOwner(cache, oid):
	"""
	Returns the ID of the object's owner, if it has one, or -1 if it does not.
	"""
	ordertypes = {}
	obj = cache.objects[oid]
	for propertygroup in obj.properties:
		if not "Owner" in propertygroup.name:
			continue
			
		group = getattr(obj, propertygroup.name)
		for struct in group.structures:
			if type(struct) != parameters.ObjectParmReference:
				continue
			
			ownerref = getattr(group, struct.name)
			if ownerref.type != GenericRS.Types["Player"]:
				continue
		
			return ownerref.id
	return -1

def getMediaURLs(cache, oid):
	"""
	Returns a dictionary of media URLs for this object, keyed by the name of the media.
	"""
	obj = cache.objects[oid]
	mediaurls = {}
	for propertygroup in obj.properties:
		group = getattr(obj, propertygroup.name)
		
		for param in group.structures:
			if type(param) == parameters.ObjectParamMedia:
				url = getattr(group, param.name).url
				if url == "":
					continue
					
				mediaurls[param.name] = url
	
	return mediaurls

def getImages(application, oid):
	"""
	Returns a list of image URLs for this object.
	"""
	cache = application.cache
	mediaurls = getMediaURLs(cache, oid)
	imageurls = {}
	animationurls = []
	staticurls = []
	for (name, url) in mediaurls.items():
		if "Icon" in name:
			continue
		
		filenames = application.media.GetFilenames(url)
		for filename in filenames:
			if filename.endswith("png"):
				staticurls.append(filename)
			elif filename.endswith("gif"):
				animationurls.append(filename)
	
	imageurls['animation'] = animationurls
	imageurls['still'] = staticurls

	return imageurls
	
def getIconURLs(application, oid):
	"""
	Returns a list of icon URLs for this object.
	"""
	cache = application.cache
	mediaurls = getMediaURLs(cache, oid)
	iconurls = []
	
	for (name, url) in mediaurls.items():
		if not "Icon" in name:
			continue
		
		filenames = application.media.GetFilenames(url)
		for filename in filenames:
			iconurls.append(filename)
			
	return iconurls
