"""\
This file contains functions used to deal with objects.
"""
from tp.netlib.objects			  			  import Structures
from tp.netlib.objects						  import parameters

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
	
	# If the object has any properties other than Positional ones, it's not a
	# galaxy.
	for propertygroup in obj.properties:
		if propertygroup.name != "Positional":
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

def hasResources(cache, oid):
	"""
	Returns true if this object has resources.
	"""
	
	obj = cache.objects[oid]
	
	for propertygroup in obj.properties:
		if propertygroup.name == "Resources":
			return True
	
	return False
	
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
				continue;
			
			ordertypes[queue.queueid] = queue.ordertypes
	return ordertypes
