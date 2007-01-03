import wx

if wx.Platform == '__WXMSW__':
	winInfoDefaultSize    = (425, 175)
	winOrderDefaultSize   = (213, 327)
	winMessageDefaultSize = (396, 163)
	winSystemDefaultSize  = (257, 218)
	
	winDesignDefaultPosition = {(1024, 768): (5, 5), }
	winDesignDefaultSize = {(1024, 768): (1000, 700), }
	winDesignDefaultShow = {(1024, 768): False, }
	
elif wx.Platform == '__WXMAC__':
	# Create some default Positioning, good for 1024x768 on linux
	winInfoDefaultSize    = (425, 176)
	winOrderDefaultSize   = (213, 327) 
	winMessageDefaultSize = (396, 163) 
	winSystemDefaultSize = 	(257, 218)
	
	winDesignDefaultPosition = {(1024, 768): (5, 5)}
	winDesignDefaultSize     = {(1024, 768): (1000, 700)}
	winDesignDefaultShow     = {(1024, 768): False,}

else:
	# Create some default Positioning, good for 1024x768 on linux
	winInfoDefaultSize    = (425, 176)
	winOrderDefaultSize   = (213, 327)
	winMessageDefaultSize = (396, 163)
	winSystemDefaultSize  = (257, 218)
	
	winDesignDefaultPosition = {
		(1024, 768): (5, 5), 
		(1280,1024): (780, 685), 
	}
	winDesignDefaultSize = {
 		(1024, 768): (1000, 700), 
		(1280,1024): (500, 285), 
	}
	winDesignDefaultShow = {
		(1024, 768): False, 
		(1280,1024): False, 
	}
