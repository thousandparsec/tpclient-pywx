"""\
This file contains functions used to deal with objects.
"""
from tp.netlib.objects			  			  import Structures
from tp.netlib.objects						  import parameters

# Get a list of the position references of a DynamicObject as tuples.
# Each tuple has the form: (x, y, z, coord name)
def get_position_list(obj):
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