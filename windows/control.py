"""\
All the windows are controlled by this class

"""

# wxPython imports
from wxPython.wx import *

# Python Imports
from extra.wxPostEvent import *
from utils import *
from config import *

class MainControl:
	def ConfigLoad(self):
		config = load_data("windows")

		if not config:
			# Create some default positioning, good for 1024x768 on linux
			config = Blank()
			config.main = Blank()
			config.message = Blank()
			config.order = Blank()
			config.starmap = Blank()
			config.system = Blank()

			sc_width = 1024
			sc_height = 768

			map_width = 600
			map_height = 500

			padding = 5

			middle = sc_width-map_width-padding

			config.main.pos = (0,0)
			config.main.size = (middle, 50)
			config.main.show = TRUE
			
			config.message.pos = (0, map_height-padding*4)
			config.message.size = (middle, 200)
			config.message.show = TRUE

			config.order.pos = (0, 55)
			config.order.size = (middle, map_height-55-padding*4)
			config.order.show = TRUE

			config.starmap.pos = (middle+padding, 0)
			config.starmap.size = (map_width-padding, map_height-padding*2)
			config.starmap.show = TRUE

			config.system.pos = (middle+padding, map_height)
			config.system.size = (map_width-padding, 200)
			config.system.show = TRUE
		
			config.raise_ = "All on All" 
	
		return config

	def ConfigSave(self):
		config = self.config
		config.main.pos = self.main.GetPositionTuple()
		config.main.size = self.main.GetSizeTuple()
		config.main.show = self.main.IsShown()
#		config.message.pos = self.message.GetPositionTuple()
#		config.message.size = self.message.GetSizeTuple()
#		config.message.show = self.message.IsShown()
#		config.order.pos = self.order.GetPositionTuple()
#		config.order.size = self.order.GetSizeTuple()
#		config.order.show = self.order.IsShown()
		config.starmap.pos = self.starmap.GetPositionTuple()
		config.starmap.size = self.starmap.GetSizeTuple()
		config.starmap.show = self.starmap.IsShown()
#		config.system.pos = self.system.GetPositionTuple()
#		config.system.size = self.system.GetSizeTuple()
#		config.system.show = self.system.IsShown()

		save_data("windows", config)

	def ConfigActivate(self, show=TRUE):
		config = self.config

		self.main.SetPosition(config.main.pos)
		self.main.SetSize(config.main.size)
#		self.message.SetPosition(config.message.pos)
#		self.message.SetSize(config.message.size)
#		self.order.SetPosition(config.order.pos)
#		self.order.SetSize(config.order.size)
		self.starmap.SetPosition(config.starmap.pos)
		self.starmap.SetSize(config.starmap.size)
#		self.system.SetPosition(config.system.pos)
#		self.system.SetSize(config.system.size)
		
		if show:
			self.main.Show(config.main.show)
#			self.message.Show(config.message.show)
#			self.order.Show(config.order.show)
			self.starmap.Show(config.starmap.show)
#			self.system.Show(config.system.show)

	def __init__(self, app):

		self.app = app
		self.config = self.ConfigLoad()

		config = self.config

		##########
		# Load the windows
		##########
		from windows.winConnect import winConnect
		self.connect = winConnect(app, -1, None)

		from windows.winMain    import winMain
		self.main = winMain(app, config.main.pos, config.main.size)

#		from windows.winConfig  import winConfig
#		self.winconfig = winConfig(app, self.main)

#		from windows.winMessage import winMessage
#		self.message = winMessage(app, self.main, config.message.pos, config.message.size)

#		from windows.winOrder   import winOrder
#		self.order = winOrder(app, self.main, config.order.pos, config.order.size)

		from windows.winStarMap import winStarMap
		self.starmap = winStarMap(app, self.main, config.starmap.pos, config.starmap.size)

#		from windows.winSystem  import winSystem
#		self.system = winSystem(app, self.main, config.system.pos, config.system.size)

		self.ConfigActivate(FALSE)

	def Raise(self):
		"""\
			Raise all the windows.
		"""
		self.connect.Raise()

#		self.system.Raise()
#		self.message.Raise()
#		self.order.Raise()
		self.starmap.Raise()
		self.main.Raise()

#		self.winconfig.Raise()

	def Show(self):
		"""\
			Show the main window
		"""
		config = self.config

		# Move everything to there home positions
		self.ConfigActivate()

		self.main.Show(config.main.show)
#		self.message.Show(config.message.show)
#		self.order.Show(config.order.show)
		self.starmap.Show(config.starmap.show)
#		self.system.Show(config.system.show)

	def Hide(self):
		"""\
			Show the main window
		"""
		pass

		self.main.Show(FALSE)
#		self.message.Show(FALSE)
#		self.order.Show(FALSE)
		self.starmap.Show(FALSE)
#		self.system.Show(FALSE)

