"""\
All the windows are controlled by this class

"""

import wx

# Local Imports
from utils import *

class MainControl:
	def ConfigLoad(self):
		config = load_data("pywx_windows")

		if not config:
			config = Blank()
			config.info = Blank()
			config.main = Blank()
			config.message = Blank()
			config.order = Blank()
			config.starmap = Blank()
			config.system = Blank()

			if wx.Platform == '__WXMSW__':
				config.main.pos = (0,0)
				config.main.size = (1024, 768)
				config.main.show = True
				
				config.info.pos = (0,0)
				config.info.size = (425, 175)
				config.info.show = True
				
				config.order.pos = (0, 176)
				config.order.size = (213, 327)
				config.order.show = True

				config.message.pos = (0, 504)
				config.message.size = (396, 163)
				config.message.show = True

				config.starmap.pos = (426, 0)
				config.starmap.size = (600, 523)
				config.starmap.show = True

				config.system.pos = (769, 523)
				config.system.size = (257, 218)
				config.system.show = True
			
				config.raise_ = "Individual" 
				
			elif wx.Platform == '__WXMAC__':
				config.main.pos = (0,38)
				config.main.size = (1024, 768)
				config.main.show = False
			
				config.info.pos = (3,38)
				config.info.size = (423, 173)
				config.info.show = True
				
				config.order.pos = (62, 229)
				config.order.size = (363, 367)
				config.order.show = True

				config.message.pos = (1032, 38)
				config.message.size = (396, 163)
				config.message.show = True

				config.starmap.pos = (426, 38)
				config.starmap.size = (600, 523)
				config.starmap.show = True

				config.system.pos = (1032, 218)
				config.system.size = (257, 218)
				config.system.show = True
			
				config.raise_ = "All on All" 

			else:
				# Create some default positioning, good for 1024x768 on linux
				config.main.pos = (0,0)
				config.main.size = (419, 51)
				config.main.show = True
				
				config.info.pos = (1,75)
				config.info.size = (425, 176)
				config.info.show = True
				
				config.order.pos = (1, 251)
				config.order.size = (213, 327)
				config.order.show = True

				config.message.pos = (1, 578)
				config.message.size = (396, 163)
				config.message.show = True

				config.starmap.pos = (426, 0)
				config.starmap.size = (600, 523)
				config.starmap.show = True

				config.system.pos = (769, 523)
				config.system.size = (257, 218)
				config.system.show = True
			
				config.raise_ = "All on All" 
	
		return config

	def ConfigSave(self):
		config = self.config
		config.main.pos = self.main.GetPositionTuple()
		config.main.size = self.main.GetSizeTuple()
		config.main.show = self.main.IsShown()
		config.info.pos = self.info.GetPositionTuple()
		config.info.size = self.info.GetSizeTuple()
		config.info.show = self.info.IsShown()
		config.message.pos = self.message.GetPositionTuple()
		config.message.size = self.message.GetSizeTuple()
		config.message.show = self.message.IsShown()
		config.order.pos = self.order.GetPositionTuple()
		config.order.size = self.order.GetSizeTuple()
		config.order.show = self.order.IsShown()
		config.starmap.pos = self.starmap.GetPositionTuple()
		config.starmap.size = self.starmap.GetSizeTuple()
		config.starmap.show = self.starmap.IsShown()
		config.system.pos = self.system.GetPositionTuple()
		config.system.size = self.system.GetSizeTuple()
		config.system.show = self.system.IsShown()

		save_data("pywx_windows", config)

	def ConfigActivate(self, show=True):
		config = self.config

		self.main.SetPosition(config.main.pos)
		self.main.SetSize(config.main.size)
		self.info.SetPosition(config.info.pos)
		self.info.SetSize(config.info.size)
		self.message.SetPosition(config.message.pos)
		self.message.SetSize(config.message.size)
		self.order.SetPosition(config.order.pos)
		self.order.SetSize(config.order.size)
		self.starmap.SetPosition(config.starmap.pos)
		self.starmap.SetSize(config.starmap.size)
		self.system.SetPosition(config.system.pos)
		self.system.SetSize(config.system.size)
		
		if show:
			self.main.Show(config.main.show)
			self.info.Show(config.info.show)
			self.message.Show(config.message.show)
			self.order.Show(config.order.show)
			self.starmap.Show(config.starmap.show)
			self.system.Show(config.system.show)

	def __init__(self, application):

		self.application = application
		self.config = self.ConfigLoad()

		config = self.config

		##########
		# Load the windows
		##########
		from windows.winConnect import winConnect
		self.connect = winConnect(application)

		from windows.winMain    import winMain, create_menu
		self.main = winMain(application, config.main.pos, config.main.size)

		from windows.winInfo    import winInfo
		self.info = winInfo(application, self.main, config.info.pos, config.info.size)

		from windows.winConfig  import winConfig
		self.winconfig = winConfig(application, self.main)
		self.winconfig.Show(False)

		from windows.winMessage import winMessage
		self.message = winMessage(application, self.main, config.message.pos, config.message.size)

		from windows.winOrder   import winOrder
		self.order = winOrder(application, self.main, config.order.pos, config.order.size)

		from windows.winStarMap import winStarMap
		self.starmap = winStarMap(application, self.main, config.starmap.pos, config.starmap.size)

		from windows.winSystem  import winSystem
		self.system = winSystem(application, self.main, config.system.pos, config.system.size)

		if wx.Platform == "__WXMAC__":
			for value in self.__dict__.values():
				if hasattr(value, "SetMenuBar"):
					value.SetMenuBar(create_menu(value, self.main))

		self.ConfigActivate(False)

		self.first = True

	def Raise(self):
		"""\
			Raise all the windows.
		"""
		self.connect.Raise()

		self.system.Raise()
		self.message.Raise()
		self.order.Raise()
		self.starmap.Raise()
		self.info.Raise()
		self.main.Raise()

		self.winconfig.Raise()

	def Show(self):
		"""\
			Show the main window
		"""
		config = self.config

		# Move everything to there home positions
		self.ConfigActivate()

		self.main.Show(config.main.show)
		self.info.Show(config.info.show)
		self.message.Show(config.message.show)
		self.order.Show(config.order.show)
		self.starmap.Show(config.starmap.show)
		self.system.Show(config.system.show)

		if self.first:
			self.first = False
			wx.CallAfter(self.main.ShowTips)

	def Hide(self):
		"""\
			Show the main window
		"""
		self.main.Show(False)
		self.info.Show(False)
		self.message.Show(False)
		self.order.Show(False)
		self.starmap.Show(False)
		self.system.Show(False)
	
	def Post(self, event):
		wx.CallAfter(self._Post, event)
		
	def _Post(self, event):
		print "Posting", event.__class__.__name__[:-5]
		func = 'On' + event.__class__.__name__[:-5]
		for window in [self.main, self.info, self.message, self.order, self.starmap, self.system]:
			if hasattr(window, func):
				getattr(window, func)(event)
		
