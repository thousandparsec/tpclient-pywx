import wx

if wx.Platform == '__WXMSW__':
	winMainDefaultPosition = {(1024, 768): (0,0), }
	winMainDefaultWidth = {(1024, 768): 1024, }
	winMainDefaultShow = {(1024, 768): True, }

	winInfoDefaultPosition = {(1024, 768): (0,0), }
	winInfoDefaultSize = {(1024, 768): (425, 175), }
	winInfoDefaultShow = {(1024, 768): True, }
	
	winOrderDefaultPosition = {(1024, 768): (0, 176), }
	winOrderDefaultSize = {(1024, 768): (213, 327), }
	winOrderDefaultShow = {(1024, 768): True, }
	
	winMessageDefaultPosition = {(1024, 768): (0, 504), }
	winMessageDefaultSize = {(1024, 768): (396, 163), }
	winMessageDefaultShow = {(1024, 768): True, }
	
	winStarmapDefaultPosition = {(1024, 768): (426, 0), }
	winStarmapDefaultSize = {(1024, 768): (600, 523), }
	winStarMapDefaultShow = {(1024, 768): True, }
	
	winSystemDefaultPosition = {(1024, 768): (769, 523), }
	winSystemDefaultSize = {(1024, 768): (257, 218), }
	winSystemDefaultShow = {(1024, 768): True, }
	
	winDesignDefaultPosition = {(1024, 768): (5, 5), }
	winDesignDefaultSize = {(1024, 768): (1000, 700), }
	winDesignDefaultShow = {(1024, 768): False, }
	
elif wx.Platform == '__WXMAC__':
	winMainDefaultPosition = {(1024, 768): (0,38), }
	winMainDefaultWidth = {(1024, 768): 1024, }
	winMainDefaultShow = {(1024, 768): False, }
	
	winInfoDefaultPosition = {(1024, 768): (3,38), }
	winInfoDefaultSize = {(1024, 768): (423, 173), }
	winInfoDefaultShow = {(1024, 768): True, }
	
	winOrderDefaultPosition = {(1024, 768): (62, 229), }
	winOrderDefaultSize = {(1024, 768): (363, 367), }
	winOrderDefaultShow = {(1024, 768): True, }
	
	winMessageDefaultPosition = {(1024, 768): (1032, 38), }
	winMessageDefaultSize = {(1024, 768): (396, 163), }
	winMessageDefaultShow = {(1024, 768): True, }
	
	winStarMapDefaultPosition = {(1024, 768): (426, 38), }
	winStarMapDefaultSize = {(1024, 768): (600, 523), }
	winStarMapDefaultShow = {(1024, 768): True, }
	
	winSystemDefaultPosition = {(1024, 768): (1032, 218), }
	winSystemDefaultSize = {(1024, 768): (257, 218), }
	winSystemDefaultShow = {(1024, 768): True, }
	
	winDesignDefaultPosition = {(1024, 768): (5, 5), }
	winDesignDefaultSize = {(1024, 768): (1000, 700), }
	winDesignDefaultShow = {(1024, 768): False, }
	
else:

	# Create some default Positioning, good for 1024x768 on linux
	winMainDefaultPosition = {
		(1024, 768): (0,0), 
		(1280,1024): (-1,31), 
	}
	winMainDefaultWidth = {
		(1024, 768): 419, 
		(1280,1024): 1272, 
	}
	winMainDefaultShow = {
		(1024, 768): True, 
		(1280,1024): True, 
	}
	
	winInfoDefaultPosition = {
		(1024, 768): (1,75), 
		(1280,1024): (0,85), 
	}
	winInfoDefaultSize = {
		(1024, 768): (425, 176),
		(1280,1024): (480, 300), 
	}
	winInfoDefaultShow = {
		(1024, 768): True, 
		(1280,1024): True,
	}
	
	winOrderDefaultPosition = {
		(1024, 768): (1, 251),
		(1280,1024): (0, 385), 
	}
	winOrderDefaultSize = {
		(1024, 768): (213, 327), 
		(1280,1024): (480, 300), 
	}
	winOrderDefaultShow = {
		(1024, 768): True, 
		(1280,1024): True, 
	}
                  
	winMessageDefaultPosition = {
		(1024, 768): (1, 578), 
		(1280,1024): (0, 685), 
	}
	winMessageDefaultSize = {
		(1024, 768): (396, 163), 
		(1280,1024): (480, 285), 
	}
	winMessageDefaultShow = {
		(1024, 768): True, 
		(1280,1024): True, 
	}
	
	winStarMapDefaultPosition = {
		(1024, 768): (426, 0), 
		(1280,1024): (480, 85), 
	}
	winStarMapDefaultSize = {
		(1024, 768): (600, 523), 
		(1280,1024): (800, 600), 
	}
	winStarMapDefaultShow = {
		(1024, 768): True, 
		(1280,1024): True, 
	}
	
	winSystemDefaultPosition = {
		(1024, 768): (769, 523), 
		(1280,1024): (480, 685), 
	}
	winSystemDefaultSize = {
		(1024, 768): (257, 218), 
		(1280,1024): (300, 285), 
	}
	winSystemDefaultShow = {
		(1024, 768): True, 
		(1280,1024): True, 
	}
	
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
