
from tp.client import objectutils
import colorsys

class Colorizer(object):
	"""
	These classes deal with figuring out the color of an object.
	"""
	def name(self):
		raise NotImplementedError("The name attribute has not been implemented.")
	name = property(staticmethod(name))

	def __init__(self, playerid):
		"""
		Create a new colorizer, takes a player id.
		"""
		pass

	def __call__(self, cache, oid):
		"""
		This function takes a list of the owners of this object.
		"""
		raise NotImplementedError("This function has not been implimented!")

class ColorVerses(Colorizer):
	"""
	This colorizer shows you in green and all the enemies in red.
	"""
	name = "Verses"

	Friendly  = "Green"
	Enemy     = "Red"
	Unowned   = "White"
	Contested = "Yellow"

	def __init__(self, pid):
		self.pid = pid

	def __call__(self, cache, oid):
		owner = objectutils.getOwner(cache, oid)
		if owner == 0:
			return self.Unowned
		elif owner == -1:
			kids = objectutils.findChildren(cache, oid)
			
			owners = set()
			for kid in kids:
				kidowner = objectutils.getOwner(cache, kid)
				if kidowner in (-1, 0):
					continue
				owners.add(kidowner)

			owners = list(owners)

			if len(owners) == 0:
				return self.Unowned
			elif len(owners) == 1:
				if owners[0] == self.pid:
					return self.Friendly
				else:
					return self.Enemy
			else:
				return self.Contested

		elif owner == self.pid:
			return self.Friendly
		else:
			return self.Enemy


class ColorEach(Colorizer):
	"""
	This colorizer gives each player it's own color.

	Alot of the code is based on stuff at http://mg.pov.lt/irclog2html/svn/irclog2html.py
	"""
	name = "Individual"

	def choose(self, i, n):
		"""Choose a color.

		`n` specifies how many different colors you want in total.
		`i` identifies a particular color in a set of `n` distinguishable
		colors.

		Returns a string '#rrggbb'.
		"""
		t = ((1.0/n * i), .75, 1)
		r = colorsys.hsv_to_rgb(*t)
		rgb = [int(x*255) for x in r]
		return '#%x%x%x' % tuple(rgb)

	def color4pid(self, cache, pid):
		pids = cache.players.keys()
		pid2colorid = dict([(b, a) for a, b in enumerate(pids)])
	
		return self.choose(pid2colorid[pid], len(pids))

	def __call__(self, cache, oid):

		owner = objectutils.getOwner(cache, oid)
		if owner == 0:
			return ColorVerses.Unowned

		elif owner == -1:
			kids = objectutils.findChildren(cache, oid)
			
			owners = set()
			for kid in kids:
				kidowner = objectutils.getOwner(cache, kid)
				if kidowner in (-1, 0):
					continue
				owners.add(kidowner)

			owners = list(owners)

			if len(owners) == 0:
				return ColorVerses.Unowned
			elif len(owners) == 1:
				return self.color4pid(cache, owners[0])
			else:
				return ColorVerses.Contested
		else:
			return self.color4pid(cache, owner)
