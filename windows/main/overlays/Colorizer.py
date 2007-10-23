
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

	def __call__(self, owners):
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

	def __call__(self, owners):
		type = (ColorVerses.Unowned, ColorVerses.Enemy)[len(owners)>0]
		if self.pid in owners:
			type = (ColorVerses.Friendly, ColorVerses.Contested)[len(owners)>1]
		return type

class ColorEach(Colorizer):
	"""
	This colorizer gives each player it's own color.

	Alot of the code is based on stuff at http://mg.pov.lt/irclog2html/svn/irclog2html.py
	"""
	name = "Individual"

	def __init__(self, pid, rgbmin=240, rgbmax=125, rgb=None, a=0.95, b=0.5):
		"""Define a range of colors available for choosing.

		`rgbmin` and `rgbmax` define the outmost range of color depth (note
		that it is allowed to have rgbmin > rgbmax).

		`rgb`, if specified, is a list of (r,g,b) values where each component
		is between 0 and 1.0.

		If `rgb` is not specified, then it is constructed as
		   [(a,b,b), (b,a,b), (b,b,a), (a,a,b), (a,b,a), (b,a,a)]

		You can tune `a` and `b` for the starting and ending concentrations of
		RGB.
		"""
		assert 0 <= rgbmin < 256
		assert 0 <= rgbmax < 256
		self.rgbmin = rgbmin
		self.rgbmax = rgbmax
		if not rgb:
			assert 0 <= a <= 1.0
			assert 0 <= b <= 1.0
			rgb = [(a,b,b), (b,a,b), (b,b,a), (a,a,b), (a,b,a), (b,a,a)]
		else:
			for r, g, b in rgb:
				assert 0 <= r <= 1.0
				assert 0 <= g <= 1.0
				assert 0 <= b <= 1.0
		self.rgb = rgb

		# Preserve the mapping
		self.playercount  = 0
		self.playersmax   = 10
		self.playercolor = {}

	def choose(self, i, n):
		"""Choose a color.

		`n` specifies how many different colors you want in total.
		`i` identifies a particular color in a set of `n` distinguishable
		colors.

		Returns a string '#rrggbb'.
		"""
		if n == 0:
			n = 1
		r, g, b = self.rgb[i % len(self.rgb)]
		m = self.rgbmin + (self.rgbmax - self.rgbmin) * float(n - i) / n
		r, g, b = map(int, (r * m, g * m, b * m))
		assert 0 <= r < 256
		assert 0 <= g < 256
		assert 0 <= b < 256
		return '#%x%x%x' % (r, g, b)

	def __getitem__(self, playername):
		color = self.playercolor.get(playername)
		if not color:
			self.playercount += 1
			if self.playercount >= self.playersmax:
				self.playersmax *= 2
			color = self.choose(self.playercount, self.playersmax)
			self.playercolor[playername] = color
		return color

	def __call__(self, owners):
		if len(owners) > 1:
			return "Red"
		elif len(owners) == 0:
			return "White"
		else:
			return self[owners[0]]

